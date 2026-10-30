"""Local singlet blocks, fixed-U charge capture, and a capacitive CZ.

Different hardware from the signed-spin native handles. Coherent scalar
controls are qualified to fixed precision. Unknown deviations are counted
as local faults; the old broad-gain promises do not imply these controls.
"""
import math
from functools import lru_cache, reduce
import numpy as np
from scipy.linalg import expm

I2=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1.,-1.]).astype(complex)
PAULIS=[X,Y,Z]

def norm(a): return float(np.linalg.norm(a,2))
def kron(*a): return reduce(np.kron,a)


@lru_cache(None)
def fock(sites=4,particles=4):
    modes=2*sites
    basis=[x for x in range(1<<modes) if x.bit_count()==particles]
    index={x:k for k,x in enumerate(basis)}; d=len(basis)
    def bilinear(i,j):
        a=np.zeros((d,d),complex)
        for col,x in enumerate(basis):
            if not ((x>>j)&1): continue
            z=x^(1<<j); sign=(-1)**((x&((1<<j)-1)).bit_count())
            if (z>>i)&1: continue
            sign*=(-1)**((z&((1<<i)-1)).bit_count())
            z|=1<<i
            a[index[z],col]=sign
        return a
    ns=[np.diag([((x>>(2*i))&1)+((x>>(2*i+1))&1) for x in basis]).astype(complex)
        for i in range(sites)]
    ds=[np.diag([((x>>(2*i))&1)*((x>>(2*i+1))&1) for x in basis]).astype(complex)
        for i in range(sites)]
    spins=[]
    for i in range(sites):
        spins.append([sum(p[a,b]*bilinear(2*i+a,2*i+b)/2
                          for a in [0,1] for b in [0,1]) for p in PAULIS])
    total=[sum(spins[i][a] for i in range(sites)) for a in range(3)]
    hopping={}
    for i in range(sites):
        for j in range(i+1,sites):
            hopping[i,j]=-sum(bilinear(2*i+s,2*j+s)+bilinear(2*j+s,2*i+s)
                              for s in [0,1])
    sep=np.zeros((d,2**sites),complex)
    if particles==sites:
        for col in range(2**sites):
            spinbits=[(col>>(sites-1-i))&1 for i in range(sites)]
            state=sum(1<<(2*i+spinbits[i]) for i in range(sites))
            sep[index[state],col]=1
    return dict(basis=basis,index=index,n=ns,double=ds,spin=spins,total=total,
                hop=hopping,sep=sep,charging=sum(ds),dimension=d)


def spin_code4():
    s=np.array([0,1,-1,0],complex)/math.sqrt(2)
    tp=np.array([1,0,0,0],complex); tm=np.array([0,0,0,1],complex)
    tz=np.array([0,1,1,0],complex)/math.sqrt(2)
    zero=np.kron(s,s)
    one=(np.kron(tp,tm)+np.kron(tm,tp)-np.kron(tz,tz))/math.sqrt(3)
    return np.column_stack([zero,one])


def code4(): return fock()['sep']@spin_code4()


def source_pulses(U=1.,pair=(0,1),reverse=False):
    """Five real-symmetric forward Hamiltonians, fixed charging energy U.

    H=U sum_i D_i + g hopping_ij + eps*(n_i-n_j)/2.
    During this capture the other two sites are singly occupied.
    The reversed order supplies C^T, not C^dagger or a bath inverse.
    """
    alpha=math.atan(1/math.sqrt(2))
    a=math.asin(math.sqrt(2/3))
    g=math.sqrt(3)*U/4
    beta=2*math.pi-2*alpha
    specs=[(g,0.,a/U),(0.,0.,beta/U),(g,0.,a/U),
           (0.,U,math.pi/(4*U)),(g,0.,math.pi/U)]
    if reverse: specs=list(reversed(specs))
    model=fock(); i,j=pair
    return [dict(H=U*model['charging']+gg*model['hop'][tuple(sorted(pair))]
                   +eps*(model['n'][i]-model['n'][j])/2,
                 time=t,g=gg,detuning=eps,pair=pair)
            for gg,eps,t in specs]


def capture_phase():
    return 3*math.pi/4+math.atan(1/math.sqrt(2))-math.asin(math.sqrt(2/3))


@lru_cache(None)
def source_unitary(U=1.,pair=(0,1),reverse=False):
    out=np.eye(fock()['dimension'],dtype=complex)
    for p in source_pulses(U,pair,reverse): out=expm(-1j*p['time']*p['H'])@out
    return out


def pair_phase(phi,U=1.,pair=(0,1)):
    c=source_unitary(U,pair); rev=source_unitary(U,pair,True)
    beta=(2*capture_phase()+phi)%(2*math.pi)
    hold=expm(-1j*beta*fock()['charging'])
    return rev@hold@c


def pair_phase_duration(phi,U=1.):
    cap=sum(p['time'] for p in source_pulses(U))
    beta=(2*capture_phase()+phi)%(2*math.pi)
    return 2*cap+beta/U


def swap_spin(i,j,n=4):
    out=np.zeros((2**n,2**n),complex)
    for x in range(2**n):
        bits=[(x>>(n-1-k))&1 for k in range(n)]
        bits[i],bits[j]=bits[j],bits[i]
        y=sum(bits[k]<<(n-1-k) for k in range(n))
        out[y,x]=1
    return out


def pair_singlet_spin(i,j): return (np.eye(16)-swap_spin(i,j))/2


def logical_hadamard_program():
    """Reuse the earlier exact bisector construction for the two axes.

    Entries (pair, phi) implement exp(-i phi P_s(pair)).
    Overall phases are immaterial. This has seven pair-phase calls.
    """
    theta=math.pi/4; z=math.sqrt(3)/2
    b=math.asin(math.sin(theta)/(2*z))
    a=.5*(math.atan2(z*math.sin(theta),math.cos(theta))
          -math.atan2((2*z*z-1)*math.sin(b),math.cos(b)))
    swaps=[((0,1),-theta),((1,2),a),((0,1),-math.pi/2),
           ((1,2),-b),((0,1),math.pi/2),((1,2),a),((0,1),-theta)]
    return [(pair,-2*t) for pair,t in swaps]


def hadamard_physical():
    u=np.eye(70,dtype=complex)
    for pair,phi in logical_hadamard_program(): u=pair_phase(phi,pair=pair)@u
    return u


def apply_local_two(v,ua,ub):
    """v has shape (d*d, columns); avoids a dense two-block matrix."""
    d=len(ua); tensor=v.reshape(d,d,-1)
    return np.einsum('ai,bj,ijk->abk',ua,ub,tensor,optimize=True).reshape(d*d,-1)


def apply_cz(v,U=1.,chi=1.):
    c=source_unitary(U); rev=source_unitary(U,reverse=True)
    model=fock(); d=model['dimension']; n=np.diag(model['n'][0]).real
    charge=np.diag(model['charging']).real
    out=apply_local_two(v,c,c)
    tc=math.pi/chi
    corr=(2*capture_phase()-U*tc)%(2*math.pi)
    angles=U*tc*(charge[:,None]+charge[None,:])+math.pi*n[:,None]*n[None,:]
    angles+=corr*(charge[:,None]+charge[None,:])
    out*=np.exp(-1j*angles).reshape(d*d,1)
    return apply_local_two(out,rev,rev)


def cz_duration(U=1.,chi=1.):
    cap=sum(p['time'] for p in source_pulses(U))
    tc=math.pi/chi
    return 2*cap+tc+((2*capture_phase()-U*tc)%(2*math.pi))/U


def charge_patterns():
    """Fixed occupations of C|0_L> and C|1_L>."""
    return np.array([[2.,0.,1.,1.],[1.,1.,1.,1.]])


def capacitive_energies(V):
    """Logical energies from an actual 4x4 inter-block capacitance matrix.

    This describes the frozen-charge interval. It does not turn off the
    same electrostatic interaction during capture or other gates.
    """
    q=charge_patterns()
    return q@np.asarray(V)@q.T


def apply_diagonal_charge_gate(v,V,time=1.,U=1.):
    """Capture, arbitrary density-density hold, reciprocal return.

    The fixed-U local phases are compensated; the electrostatic local
    phases are deliberately retained. This works for any input outside
    one block while preserving the other block's computational subspace.
    """
    model=fock(); c=source_unitary(U); rev=source_unitary(U,reverse=True)
    ns=np.array([np.diag(n).real for n in model['n']]).T
    charge=np.diag(model['charging']).real
    phases=time*(ns@np.asarray(V)@ns.T)
    phases+=2*capture_phase()*(charge[:,None]+charge[None,:])
    out=apply_local_two(v,c,c)
    out*=np.exp(-1j*phases).reshape(70*70,1)
    return apply_local_two(out,rev,rev)


def phase_distance(u,v):
    z=np.vdot(v,u)
    return norm(u-(z/abs(z))*v)
