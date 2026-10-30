"""Spinless STAR: full-gauge local gates and balanced capacitance.

The exact local identities act on all sixteen Fock states. The encoded
subsystem has dimension 2 x 4. The two-block finite-gap calculation is
an explicitly qualified approximation, not an all-bath theorem.
"""
from pathlib import Path
import math
import json
from itertools import combinations
import numpy as np
from scipy.linalg import eigh, expm, polar


I2=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)


def norm(a): return float(np.linalg.norm(a,2))


def fock(n=4):
    d=2**n
    c=[]
    for k in range(n):
        op=np.zeros((d,d),complex)
        for b in range(d):
            if (b>>k)&1:
                op[b^(1<<k),b]=(-1)**((b&((1<<k)-1)).bit_count())
        c.append(op)
    return c,[a.conj().T@a for a in c]


def second_quantize(u):
    n=len(u); d=2**n
    out=np.zeros((d,d),complex)
    for p in range(n+1):
        sets=list(combinations(range(n),p))
        for rr in sets:
            r=sum(1<<i for i in rr)
            for cc in sets:
                col=sum(1<<j for j in cc)
                out[r,col]=np.linalg.det(u[np.ix_(rr,cc)]) if p else 1.
    return out


def model():
    c,n=fock()
    b=sum(c[1:])/math.sqrt(3)
    d0=(c[1]-c[2])/math.sqrt(2)
    d1=(c[1]+c[2]-2*c[3])/math.sqrt(6)
    nb=b.conj().T@b
    ne=d0.conj().T@d0+d1.conj().T@d1
    no=sum(n[1:])
    u=np.column_stack([np.array([1,0,0,0]),np.array([0,1,1,1])/math.sqrt(3),
                       np.array([0,1,-1,0])/math.sqrt(2),
                       np.array([0,1,1,-2])/math.sqrt(6)]).astype(complex)
    gamma=second_quantize(u)
    indices=[g+(1<<(2+logical)) for logical in [0,1] for g in range(4)]
    E=gamma[:,indices]
    return dict(c=c,n=n,b=b,nb=nb,ne=ne,no=no,E=E,u=u)


def partial_logical(h,dl,dg):
    tensor=h.reshape(dl,dg,dl,dg)
    return np.einsum('agbg->ab',tensor)/dg


def partial_gauge(h,dl,dg):
    tensor=h.reshape(dl,dg,dl,dg)
    return np.einsum('agah->gh',tensor)/dl


def gauge_hamiltonian(m,scale=1.,variation=0.):
    c,n,b,nb,no=m['c'],m['n'],m['b'],m['nb'],m['no']
    return scale*((.17+variation)*n[0]-.23*nb
                  +(.31-variation)*(c[0].conj().T@b+b.conj().T@c[0])
                  +.29*n[0]@no+.13*no@(no-np.eye(16))/2)


def local_checks():
    m=model(); E=m['E']; p=E@E.conj().T
    H0=gauge_hamiltonian(m)
    hg=partial_gauge(E.conj().T@H0@E,2,4)
    rows=[]
    for i,j in [(1,2),(2,3),(1,3)]:
        dm=(m['c'][i]-m['c'][j])/math.sqrt(2)
        nm=dm.conj().T@dm
        h=partial_logical(E.conj().T@nm@E,2,4)
        perm=np.eye(4);perm[:,[i,j]]=perm[:,[j,i]]
        pp=second_quantize(perm)
        duration=2.3;strength=.73
        exact=expm(-1j*(H0+strength*nm)*duration)@E
        target=E@np.kron(expm(-1j*strength*h*duration),expm(-1j*hg*duration))
        rows.append(dict(pair=[i,j],parity_identity_residual=norm(pp-(np.eye(16)-2*nm)),
                         code_leakage_generator=norm((np.eye(16)-p)@nm@E),
                         factorization_residual=norm(E.conj().T@nm@E-np.kron(h,np.eye(4))),
                         central_port_commutator=norm(nm@m['c'][0]-m['c'][0]@nm),
                         bright_port_commutator=norm(nm@m['b']-m['b']@nm),
                         interacting_idle_commutator=norm(nm@H0-H0@nm),
                         joint_gate_isometry_error=norm(exact-target)))
    return dict(code_rank=int(round(np.trace(p).real)),
                gauge_hamiltonian_factorization=norm(E.conj().T@H0@E-np.kron(I2,hg)),
                local_gates=rows)


def geometry_matrix(height=2.,radius=1.,scale=1.,apex=0.):
    positions=[np.array([0.,0.,apex])]+[np.array([radius*np.cos(2*np.pi*k/3),radius*np.sin(2*np.pi*k/3),0.]) for k in range(3)]
    return np.array([[scale/np.linalg.norm(a-b-np.array([0,0,height])) for b in positions] for a in positions])


def two_code(E):
    return np.column_stack([np.kron(E[:,la*4+ga],E[:,lb*4+gb])
                            for la in range(2) for lb in range(2)
                            for ga in range(4) for gb in range(4)])


def capacitive_projection():
    m=model(); E=two_code(m['E']); V=geometry_matrix()
    cap=sum(V[i,j]*np.kron(m['n'][i],m['n'][j]) for i in range(4) for j in range(4))
    hp=E.conj().T@cap@E
    delta=V[1,1]-V[1,2]
    hl=delta/6*(np.kron(X,X)+np.kron(Z,Z))
    hg=partial_gauge(hp,4,16)
    return dict(V=V.tolist(),leaf_row_sums=V[1:,1:].sum(axis=1).tolist(),
                delta=delta,logical_entangler_coefficient=delta/6,
                full_gauge_factorization_residual=norm(hp-np.kron(hl,np.eye(16))-np.kron(np.eye(4),hg)),
                off_code_capacitance_norm=norm(cap@E-E@hp))


def tetrahedron_checks():
    m=model(); E=two_code(m['E']); eye=np.eye(16)
    V=geometry_matrix(height=4.,apex=math.sqrt(2))
    cap=sum(V[i,j]*np.kron(m['n'][i],m['n'][j]) for i in range(4) for j in range(4))
    hp=E.conj().T@cap@E
    delta=V[1,1]-V[1,2]
    hl=delta/6*(np.kron(X,X)+np.kron(Z,Z))
    hg=partial_gauge(hp,4,16)
    nt=sum(m['n'])
    charging=nt@(nt-eye)/2
    hlocal=gauge_hamiltonian(m)+m['ne']
    monopole=np.kron(nt,nt)
    hclosed=np.kron(hlocal,eye)+np.kron(eye,hlocal)+cap
    gamma=second_quantize(m['u'])
    leaked=[]
    for occupation,offset in [(0,0),(2,12)]:
        eb=gamma[:,[g+offset for g in range(4)]]
        code=np.column_stack([np.kron(m['E'][:,la*4+ga],eb[:,gb])
                              for la in range(2) for ga in range(4) for gb in range(4)])
        projected=code.conj().T@cap@code
        gh=partial_gauge(projected,2,16)
        leaked.append(dict(neighbor_dark_occupation=occupation,
                           valid_logical_scalar_residual=norm(projected-np.kron(I2,gh))))
    return dict(V=V.tolist(),delta=delta,
                projected_logical_plus_gauge_residual=norm(hp-np.kron(hl,np.eye(16))-np.kron(np.eye(4),hg)),
                uniform_internal_charging_commutator=norm(charging@hlocal-hlocal@charging),
                uniform_interblock_monopole_commutator=norm(monopole@hclosed-hclosed@monopole),
                leaked_neighbor_projection=leaked)


def gate_check(cap_scale=.01,delta_a=1.,delta_b=2.,gauge_scale=.1):
    m=model(); E=two_code(m['E']); eye=np.eye(16)
    V=geometry_matrix(scale=cap_scale)
    cap=sum(V[i,j]*np.kron(m['n'][i],m['n'][j]) for i in range(4) for j in range(4))
    HA=delta_a*m['ne']+gauge_hamiltonian(m,gauge_scale)
    HB=delta_b*m['ne']+gauge_hamiltonian(m,gauge_scale,variation=.04)
    H=np.kron(HA,eye)+np.kron(eye,HB)+cap
    hp=E.conj().T@H@E
    delta=V[1,1]-V[1,2]
    kappa=delta/6
    time=np.pi/(4*kappa)
    en,vec=eigh(H)
    output=vec@(np.exp(-1j*en*time)[:,None]*(vec.conj().T@E))
    projected=E.conj().T@output
    logical=expm(-1j*time*kappa*(np.kron(X,X)+np.kron(Z,Z)))
    corrected=np.kron(logical.conj().T,np.eye(16))@projected
    vg,_=polar(partial_gauge(corrected,4,16))
    target=E@np.kron(logical,vg)
    leak=norm(output-E@projected)
    direct_target=E@expm(-1j*time*hp)
    Hrest=H-np.kron(delta_a*m['ne'],eye)-np.kron(eye,delta_b*m['ne'])
    er=eigh(Hrest,eigvals_only=True)
    half_bandwidth=float((er[-1]-er[0])/2)
    off=cap@E-E@(E.conj().T@cap@E)
    w=norm(off)
    gap=delta_a-2*half_bandwidth if abs(delta_b-2*delta_a)<1e-12 else None
    bound=None
    if gap is not None and gap>0:
        snorm=math.sqrt(2)*w/gap
        bound=2*snorm+time*snorm*w*math.exp(2*snorm)
    return dict(capacitive_scale=cap_scale,dark_offsets=[delta_a,delta_b],
                gauge_scale=gauge_scale,gate_duration=time,
                internal_gauge_motion_scale_times_duration=.31*gauge_scale*time,
                leakage_isometry_norm=leak,
                uniform_logical_product_isometry_error=norm(output-target),
                projected_H_target_isometry_error=norm(output-direct_target),
                rest_half_spectral_bandwidth=half_bandwidth,
                sufficient_P_Q_spectral_gap=gap,
                off_diagonal_norm=w,
                explicit_uniform_isometry_bound=bound,
                best_gauge_fit_unitarity_residual=norm(vg.conj().T@vg-np.eye(16)),
                scope='Finite 256-state Hamiltonian and full 64-dimensional logical-plus-gauge input; no reservoir or certified rounding enclosures.')


def spinful_quadratic_obstruction():
    # Two E orbitals x,y, with two spin flavors each.
    c,n=fock(4)
    vacuum=np.eye(16)[:,0]
    xx=c[0].conj().T@c[1].conj().T@vacuum
    yy=c[2].conj().T@c[3].conj().T@vacuum
    xy=(c[0].conj().T@c[3].conj().T-c[1].conj().T@c[2].conj().T)@vacuum/math.sqrt(2)
    scalar=(xx+yy)/math.sqrt(2)
    # The minus sign on xy intertwines the Sym² E copy with the N=1 E.
    ee=np.column_stack([(xx-yy)/math.sqrt(2),-xy])
    out={}
    for name,h in [('X',X),('Y',Y),('Z',Z)]:
        H=sum(h[i,j]*c[2*i+s].conj().T@c[2*j+s]
              for i in range(2) for j in range(2) for s in range(2))
        h2=ee.conj().T@H@ee
        out[name]=dict(leakage_to_A1=float(np.linalg.norm(scalar.conj()@H@ee)),
                       E_copy_generator_real=h2.real.tolist(),E_copy_generator_imag=h2.imag.tolist(),
                       mismatch_with_one_particle_E=norm(h2-h))
    return out


if __name__=='__main__':
    out=dict(local=local_checks(),balanced_capacitance=capacitive_projection(),
             tetrahedron=tetrahedron_checks(),
             staggered_gates=[gate_check(cap_scale=s) for s in [.02,.01,.005,.002]],
             equal_offset_failure=[gate_check(cap_scale=s,delta_b=1.,gauge_scale=0.) for s in [.02,.005,.002]],
             spinful_gaussian_obstruction=spinful_quadratic_obstruction(),
             status='Working exact finite-model identities and numerical checks, not a device claim.')
    Path(__file__).with_name('spinless_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
