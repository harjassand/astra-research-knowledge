"""All four-orbital Coulomb integrals for orthogonalized Gaussian rails.

Direct spin-independent charge controls, exchange and wrong-rail terms
are computed from the same Coulomb kernel. This is an explicit projected
orbital fixture. Gaussian orbitals are not certified exact low-energy
states of the double-harmonic confinement used for the one-body check.
"""
from pathlib import Path
import math,json
from itertools import combinations
import numpy as np
from scipy.integrate import quad
from scipy.special import erfc
from scipy.linalg import expm

HERE=Path(__file__).resolve().parent
I=np.eye(2); X=np.array([[0.,1.],[1.,0.]]); Z=np.diag([1.,-1.])

def norm(a):return float(np.linalg.norm(a,2))

def lowdin(s):
    u=1/math.sqrt(1+s);v=1/math.sqrt(1-s)
    return np.array([[(u+v)/2,(u-v)/2],[(u-v)/2,(u+v)/2]])

def hopping(s):
    x=s/2;S=math.exp(-x*x)
    return S/(1-S*S)*(x/math.sqrt(math.pi)*(1-S)+x*x*erfc(x))

def integrals(sx=4.,sy=9.,sz=9.):
    widths=np.array([1/sx,1/sy,1/sz])
    centers=np.array([[.5,.5,0],[-.5,.5,0],[-.5,-.5,0],[.5,-.5,0]])
    cache={}
    def potential(r):
        key=tuple(np.round(np.abs(r),12))
        if key not in cache:
            rr=np.asarray(key)**2
            def f(t):
                den=1+widths**2*t*t
                return math.sqrt(2/math.pi)*math.exp(-.5*t*t*np.sum(rr/den))/math.sqrt(np.prod(den))
            cache[key]=quad(f,0,np.inf,epsabs=2e-12,epsrel=2e-12,limit=200)[0]
        return cache[key]
    overlap=np.exp(-np.sum((centers[:,None,:]-centers[None,:,:])**2/(4*widths**2),axis=2))
    mx=(centers[:,None,:]+centers[None,:,:])/2
    raw=np.empty((4,4,4,4))
    for i,j,k,l in np.ndindex(4,4,4,4):raw[i,j,k,l]=overlap[i,j]*overlap[k,l]*potential(mx[i,j]-mx[k,l])
    lx=lowdin(math.exp(-sx*sx/4));ly=lowdin(math.exp(-sy*sy/4))
    labels=[(0,0),(1,0),(1,1),(0,1)]
    c=np.array([[lx[a,aa]*ly[r,rr] for aa,rr in labels] for a,r in labels])
    eri=np.einsum('ia,jb,kc,ld,abcd->ijkl',c,c,c,c,raw,optimize=True)
    return eri,dict(widths_over_d=widths.tolist(),Gaussian_overlap_matrix=overlap.tolist(),
                    Lowdin_orthonormality_error=norm(c@overlap@c.T-np.eye(4)),
                    raw_potential_values={str(k):v for k,v in cache.items()})

def fixture(sx=4.,sy=9.,sz=9.):
    eri,metadata=integrals(sx,sy,sz)
    charges=[(0,2),(0,3),(1,2),(1,3)]
    hd=np.array([[eri[a,c,b,d] for c,d in charges] for a,b in charges])
    coeff={}
    for la,a in [('I',I),('X',X),('Z',Z)]:
        for lb,b in [('I',I),('X',X),('Z',Z)]:coeff[la+lb]=float(np.trace(np.kron(a,b)@hd)/4)
    reconstructed=sum(v*np.kron({'I':I,'X':X,'Z':Z}[k[0]],{'I':I,'X':X,'Z':Z}[k[1]]) for k,v in coeff.items())
    gap=-2*coeff['ZZ'];jx=(coeff['IX']+coeff['XI'])/2;jxx=coeff['XX']
    t_eff=.25*math.sqrt(4*(gap+4*jxx)**2-gap**2)
    t_bare=t_eff+jx
    A=hopping(sx)*sx*sx/t_bare
    transverse_t=hopping(sy)*sy*sy/A
    time=math.pi/(gap+4*jxx)
    charge_h=hd-t_bare*(np.kron(X,I)+np.kron(I,X))
    e=np.eye(4)[:,[0,3]]
    actual=expm(-1j*charge_h*time)@e
    target=expm(1j*math.pi*X/4)
    phase=np.angle(np.trace(target.conj().T@(e.T@actual)))
    pairs=list(combinations(range(8),2))
    hc=np.empty((28,28))
    for i,(p,q) in enumerate(pairs):
        for j,(r,s) in enumerate(pairs):
            hc[i,j]=(eri[p//2,r//2,q//2,s//2] if p%2==r%2 and q%2==s%2 else 0.)-(eri[p//2,s//2,q//2,r//2] if p%2==s%2 and q%2==r%2 else 0.)
    rail_basis=[pairs.index((2*a+s,2*b+t)) for a,b in charges for s in [0,1] for t in [0,1]]
    other=[k for k in range(28) if k not in rail_basis]
    hpp=hc[np.ix_(rail_basis,rail_basis)]
    # Form the small exchange block directly; subtracting it from O(1)
    # direct energies can lose digits when transverse overlap is tiny.
    he=np.array([[eri[a,d,b,c] for c,d in charges] for a,b in charges])
    swap=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],float)
    exchange=norm(he)
    spin_reconstruction=norm(hpp-np.kron(hd,np.eye(4))+np.kron(he,swap))
    wrongrail=norm(hc[np.ix_(other,rail_basis)])
    return dict(shape=dict(sx=sx,sy=sy,sz=sz),metadata=metadata,
                direct_charge_coefficients_in_K_over_d=coeff,
                direct_charge_Pauli_reconstruction=norm(hd-reconstructed),
                Delta_in_K_over_d=gap,Jxx_in_K_over_d=jxx,
                required_effective_longitudinal_hopping=t_eff,
                required_bare_longitudinal_hopping=t_bare,
                consistent_d_over_effective_Bohr_radius=A,
                Gaussian_projected_transverse_hopping=transverse_t,
                quarter_gate_duration_in_hbar_d_over_K=time,
                repaired_quarter_gate_isometry_error=norm(actual-np.exp(1j*phase)*e@target),
                full_16_state_spin_exchange_remainder=exchange,
                spin_direct_plus_exchange_reconstruction=spin_reconstruction,
                full_rail_to_wrongrail_Coulomb_norm=wrongrail,
                conservative_quarter_gate_transfer_plus_exchange_action=time*(2*transverse_t+wrongrail+exchange),
                transverse_energy_over_Delta=sy*sy/(A*gap),
                longitudinal_energy_over_Delta=sx*sx/(A*gap),
                scope="All ERIs and spin/charge remainders in an orthogonalized four-Gaussian orbital fixture; acquired direct terms repaired analytically. No assertion that omitted orbitals or ramp deformation have these small bounds.")

if __name__=='__main__':
    out=fixture()
    (HERE/'projected_rails_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
