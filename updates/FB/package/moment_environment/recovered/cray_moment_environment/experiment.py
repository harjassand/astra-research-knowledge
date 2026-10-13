"""Numerical diagnostics for finite-moment environment enclosures.
Floating-point calculations are tests, not exact certificates.
"""
from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigvalsh
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh

@dataclass
class MomentBand:
    sign: int
    a: float
    b: float
    W: np.ndarray
    T: np.ndarray

def psd_factor(W, tol=1e-12):
    W=np.asarray(W,complex)
    lam,Q=np.linalg.eigh((W+W.conj().T)/2)
    if lam[0] < -tol*max(1.,np.linalg.norm(W)):
        raise ValueError('Weight is not positive semidefinite')
    keep=lam>tol*max(1.,np.max(lam))
    return Q[:,keep]*np.sqrt(lam[keep])

def moment_baths(bands, m):
    """Return endpoint/lower-energy bath and mean/upper-energy bath.
    A bath is (signed one-particle energies, m x bath_modes coupling matrix).
    T is the first ABSOLUTE-energy moment, not the squared-energy moment.
    """
    el,vl,eu,vu=[],[],[],[]
    for z in bands:
        if z.sign not in [-1,1] or not 0<=z.a<z.b:
            raise ValueError('Invalid signed interval')
        L=psd_factor(z.W)
        if L.shape[1]==0:
            continue
        Linv=np.linalg.pinv(L)
        B=Linv@z.T@Linv.conj().T
        e,Q=np.linalg.eigh((B+B.conj().T)/2)
        if e[0]<z.a-1e-9 or e[-1]>z.b+1e-9:
            raise ValueError('Moment support constraint fails')
        eu.extend(z.sign*e); vu.append(L@Q)
        for e,W in [(z.a,(z.b*z.W-z.T)/(z.b-z.a)),
                    (z.b,(z.T-z.a*z.W)/(z.b-z.a))]:
            R=psd_factor(W)
            el.extend([z.sign*e]*R.shape[1]); vl.append(R)
    def out(e,v):
        return np.array(e), np.concatenate(v,axis=1) if v else np.zeros((m,0),complex)
    return out(el,vl),out(eu,vu)

def fermionic_hamiltonian(h, interactions):
    """Exact Fock-basis sparse matrix, with density-density interactions."""
    h=np.asarray(h,complex); n=len(h)
    if n>17:
        raise ValueError('Diagnostic ED is restricted to at most 17 modes')
    rows,cols,vals=[],[],[]
    nonzero=[(i,j,h[i,j]) for i in range(n) for j in range(n)
             if i!=j and abs(h[i,j])>1e-14]
    for x in range(1<<n):
        diag=sum(h[i,i].real for i in range(n) if (x>>i)&1)
        diag+=sum(u for i,j,u in interactions if ((x>>i)&1) and ((x>>j)&1))
        rows.append(x); cols.append(x); vals.append(diag)
        for i,j,coef in nonzero:
            if not ((x>>j)&1) or ((x>>i)&1):
                continue
            y=x^(1<<j)
            parity=(x&((1<<j)-1)).bit_count()+(y&((1<<i)-1)).bit_count()
            rows.append(y|(1<<i)); cols.append(x)
            vals.append(coef*(-1 if parity%2 else 1))
    return coo_matrix((vals,(rows,cols)),shape=(1<<n,1<<n)).tocsr()

def full_h(ha,bath):
    e,V=bath
    return np.block([[ha,V],[V.conj().T,np.diag(e)]])

def impurity_energy(ha,bath,interactions):
    e,V=bath; H=fermionic_hamiltonian(full_h(ha,bath),interactions)
    if H.shape[0]<=128:
        en=eigvalsh(H.toarray())[0]
    else:
        en=eigsh(H,k=1,which='SA',tol=1e-11,return_eigenvectors=False)[0]
    return float(en-np.minimum(e,0).sum())

def free_ph_energy(s,w):
    """Bath-subtracted free resonant-level ground energy, one impurity mode.
    s: squared paired bath energies. w: pair-total coupling weights.
    """
    s=np.asarray(s,float); w=np.asarray(w,float)
    if len(s)==0: return 0.
    lam=eigvalsh(np.diag(s)+np.outer(np.sqrt(w),np.sqrt(w)))
    return float(np.sqrt(s).sum()-np.sqrt(np.maximum(lam,0)).sum())

def ph_envelopes(edges,W,T):
    """Squared-energy moment bounds (not the signed first-moment theorem).
    Returns (lower hybridization, upper hybridization), each (s,w).
    """
    sl,wl=[],[]; atom={}
    for a,b,w,t in zip(edges[:-1],edges[1:],W,T):
        if w<1e-16: continue
        aa,bb=a*a,b*b
        sl.append(t/w); wl.append(w)
        for s,q in [(aa,(bb*w-t)/(bb-aa)),(bb,(t-aa*w)/(bb-aa))]:
            if q>1e-16: atom[s]=atom.get(s,0.)+q
    su=np.array(sorted(atom)); wu=np.array([atom[s] for s in su])
    return (np.array(sl),np.array(wl)),(su,wu)

def flat_ph(edges,total_weight=.125):
    edges=np.asarray(edges,float)
    return ph_envelopes(edges,total_weight*np.diff(edges),
                         total_weight*np.diff(edges**3)/3)

def grid(ratio=1.5,cutoff=1e-4):
    x=[1.]
    while x[-1]>cutoff: x.append(x[-1]/ratio)
    return np.array([0.]+list(reversed(x)))

def numeric_tests(seed=73017):
    rng=np.random.default_rng(seed); ans=[]
    for k in range(6):
        m=2
        e=np.array([-.94,-.53,-.24,.18,.57,.83])
        V=(rng.normal(size=(m,6))+1j*rng.normal(size=(m,6)))*.17
        bands=[]
        for sign in [-1,1]:
            ix=e*sign>0; vb=V[:,ix]; eb=abs(e[ix])
            bands.append(MomentBand(sign,.1,1.,vb@vb.conj().T,(vb*eb)@vb.conj().T))
        low,high=moment_baths(bands,m)
        A=(rng.normal(size=(m,m))+1j*rng.normal(size=(m,m)))*.35
        ha=(A+A.conj().T)/2; u=float(rng.uniform(-2,4))
        vals=[impurity_energy(ha,b,[(0,1,u)]) for b in [low,(e,V),high]]
        assert vals[0]<=vals[1]+1e-8 and vals[1]<=vals[2]+1e-8, vals
        ans.append(dict(trial=k,U=u,lower=vals[0],true=vals[1],upper=vals[2],
                        lower_modes=len(low[0]),true_modes=len(e),upper_modes=len(high[0])))
    return ans

def spectral_benchmarks():
    ans=[]
    for name,edges in [('linear_4',np.linspace(0,1,5)),('linear_8',np.linspace(0,1,9)),
                       ('linear_16',np.linspace(0,1,17)),('linear_32',np.linspace(0,1,33)),
                       ('geo_2',grid(2)),('geo_1.5',grid(1.5)),('geo_1.25',grid(1.25))]:
        lo,hi=flat_ph(edges)
        radius=free_ph_energy(*lo)-free_ph_energy(*hi)
        ans.append(dict(bath='flat',grid=name,bins=len(edges)-1,scalar_radius=radius,
                        lower_gamma_poles=len(lo[0]),upper_gamma_poles=len(hi[0])))
    # Independently specified finite-range 256x256 square-lattice reservoir.
    # Antiperiodic x, periodic y; hopping t=1/4; half-bandwidth <=1; local V=.3.
    L=256
    kx=2*np.pi*(np.arange(L)+.5)/L; ky=2*np.pi*np.arange(L)/L
    eps=(-.5*(np.cos(kx)[:,None]+np.cos(ky)[None,:])).ravel()
    ep=eps[eps>1e-12]; pair_weight=2*.3**2/(L*L)
    assert len(ep)==L*L//2
    for name,edges in [('linear_8',np.linspace(0,1,9)),('linear_16',np.linspace(0,1,17)),
                       ('geo_2',grid(2)),('geo_1.5',grid(1.5))]:
        W=[]; T=[]
        for i,(a,b) in enumerate(zip(edges[:-1],edges[1:])):
            ix=(ep>=a)&((ep<b) if i<len(edges)-2 else (ep<=b))
            W.append(pair_weight*np.count_nonzero(ix)); T.append(pair_weight*np.sum(ep[ix]**2))
        lo,hi=ph_envelopes(edges,W,T)
        ans.append(dict(bath='square_lattice_65536',grid=name,bins=len(edges)-1,
                        scalar_radius=free_ph_energy(*lo)-free_ph_energy(*hi),
                        lower_gamma_poles=len(lo[0]),upper_gamma_poles=len(hi[0]),
                        total_weight=sum(W)))
    return ans

def counterexample():
    # Two baths with identical vacuum one-particle spectral functions but different
    # two-particle interaction. Bath vacuum remains its unique ground state.
    ha=np.diag([-1.,-1.]); bath=(np.array([1.,1.]),.8*np.eye(2))
    ans=[]
    for ub in [-1.8,0.,2.]:
        H=fermionic_hamiltonian(full_h(ha,bath),[(0,1,1.0),(2,3,ub)])
        ans.append(dict(bath_U=ub,ground_energy=float(eigvalsh(H.toarray())[0])))
    return ans

if __name__=='__main__':
    out=dict(signed_moment_tests=numeric_tests(),spectral_benchmarks=spectral_benchmarks(),
             non_gaussian_counterexample=counterexample())
    dest=Path(__file__).with_name('numerical_results.json')
    dest.write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
