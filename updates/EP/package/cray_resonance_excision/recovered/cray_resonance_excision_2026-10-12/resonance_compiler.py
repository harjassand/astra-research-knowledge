"""Research prototype: auxiliary-field resonance excision for complex phi^4.

The representation is exact before excision. The supplied mathematical bounds
are ideal-real-arithmetic bounds. This floating implementation does not provide
interval arithmetic or certified finite-bit Gaussian draws. No independent
review or historical novelty claim is made.
"""
from __future__ import annotations
import math, time
from dataclasses import dataclass
import numpy as np
from scipy.linalg import lu_factor, lu_solve, cholesky, solve_triangular
from scipy.special import ndtr

@dataclass
class Model:
    A: np.ndarray
    C: np.ndarray
    g: float
    kappa: float
    amin: float
    amax: float
    cmax: float

    def validate(self) -> None:
        n = self.A.shape[0]
        assert self.A.shape == self.C.shape == (n,n)
        assert self.g > 0 and self.kappa > 0 and self.amin > 0
        assert np.allclose(self.A,self.A.T) and np.allclose(self.C,self.C.T)
        assert np.linalg.eigvalsh(self.A)[0] >= self.amin-1e-10
        assert np.linalg.eigvalsh(self.C)[0] >= self.kappa-1e-10
        assert np.linalg.norm(self.A,2) <= self.amax+1e-10
        assert np.linalg.norm(self.C,2) <= self.cmax+1e-10

    @property
    def n(self): return self.A.shape[0]

def make_grid(L: int, kappa: float, seed: int = 20261012, chain=False) -> Model:
    """Connected heterogeneous explicit input. Integer-generated edge weights.
    A=.5 I+Laplacian(a_e), C=kappa I+Laplacian(c_e).
    All input coefficients are rational; spectral bounds follow by Gershgorin.
    """
    rng=np.random.default_rng(seed)
    n=L if chain else L*L
    A=.5*np.eye(n); C=kappa*np.eye(n)
    edges=[]
    if chain: edges=[(i,i+1) for i in range(n-1)]
    else:
        for i in range(L):
            for j in range(L):
                q=i*L+j
                if i+1<L: edges.append((q,q+L))
                if j+1<L: edges.append((q,q+1))
    for i,j in edges:
        a=float(rng.integers(4,16))/100
        c=float(rng.integers(25,76))/100
        for M,w in ((A,a),(C,c)):
            M[i,i]+=w; M[j,j]+=w; M[i,j]-=w; M[j,i]-=w
    amax=float(np.max(np.diag(A)+np.sum(np.abs(A),axis=1)-np.abs(np.diag(A))))
    cmax=float(np.max(np.diag(C)+np.sum(np.abs(C),axis=1)-np.abs(np.diag(C))))
    return Model(A,C,1.,float(kappa),.5,amax,cmax)

def soft_floor(d: np.ndarray, kappa: float):
    b=kappa/4.
    s=d.copy(); deriv=np.ones_like(d)
    low=d<=-2*b; middle=(d>-2*b)&(d<-b)
    s[low]=-1.5*b; deriv[low]=0.
    s[middle]=-1.5*b+(d[middle]+2*b)**2/(2*b)
    deriv[middle]=(d[middle]+2*b)/b
    return s,deriv

class Compiler:
    def __init__(self, model: Model):
        model.validate(); self.m=model
        self.a=math.sqrt(2*model.g)
        self.F0=self.logw(np.zeros(model.n), clipped=False)[0]

    def logw(self, sigma, clipped=True, grad=False):
        d=self.a*np.asarray(sigma)
        if clipped: d,ds=soft_floor(d,self.m.kappa)
        else: ds=np.ones(self.m.n)
        H=self.m.A-1j*(self.m.C+np.diag(d))
        lu,piv=lu_factor(H,check_finite=False)
        if np.array_equal(piv,np.arange(self.m.n)):
            # Accretivity of H makes no-pivot Schur diagonals right-half-plane;
            # sum of their principal logs selects the real Gaussian cycle.
            F=-.5*np.sum(np.log(np.diag(lu)))
        else:
            # General Gaussian branch via a real congruence, NOT principal
            # square root of det(H), which loses the winding.
            L=cholesky(self.m.A,lower=True,check_finite=False)
            B=self.m.C+np.diag(d)
            tmp=solve_triangular(L,B,lower=True,check_finite=False)
            T=solve_triangular(L,tmp.T,lower=True,check_finite=False).T
            ev=np.linalg.eigvalsh((T+T.T)/2)
            F=-np.sum(np.log(np.diag(L)))-.5*np.sum(np.log(1-1j*ev))
        if not grad: return complex(F),None
        G=lu_solve((lu,piv),np.eye(self.m.n),check_finite=False)
        gradient=-.5*self.a*ds*np.imag(np.diag(G))
        return complex(F),gradient

    def mode(self,tol=1e-12,maxiter=100):
        mu=np.zeros(self.m.n)
        for iteration in range(maxiter):
            _,new=self.logw(mu,grad=True)
            mu=new
            _,grad=self.logw(mu,grad=True)
            residual=float(np.linalg.norm(mu-grad))
            if residual<tol:
                return mu,residual,iteration+1
        raise RuntimeError('Mode iteration did not converge; do not certify.')

    def certificate(self,residual=0.):
        m=self.m; n=m.n; g=m.g; k=m.kappa
        beta=224*g/(25*k*k)
        alpha=1-64*g/(25*k*k)
        ell=1-2*beta
        t=k/(4*math.sqrt(2*g))
        # Mills ratio bound, valid for t>=1. Exact normal tail is not required.
        p=min(1.,3*math.exp(-t*t/2)/(t*math.sqrt(2*math.pi))) if t>=1 else 1.
        B=m.amax+m.cmax+3*k/8+8*(m.amax+m.cmax)**2/(5*k)
        K=max(1.,math.sqrt(B/m.amin))
        e=n*math.log1p((K-1)*p)
        Delta=math.expm1(e)+2*n*p if e<700 else math.inf
        v=2048*n*g*m.amax**2/(625*alpha*k**4) if alpha>0 else math.inf
        s=1-v/2
        if ell>0:
            exponent=(residual*(1+2*beta/ell)+beta*math.sqrt(n/ell))**2/ell
            cv=math.expm1(exponent)/s**2+(1/s**2-1) if s>0 else math.inf
        else: exponent=cv=math.inf
        relative_bias=Delta/(s-Delta) if s>Delta else math.inf
        return dict(n=n,kappa=k,g=g,beta=beta,alpha=alpha,phase_variance_bound=v,
                    phase_lower_bound=s,one_site_defect_bound=p,rank_factor=K,
                    defect_mass_bound=Delta,relative_clipping_bias_bound=relative_bias,
                    proposal_residual=residual,log_second_moment_bound=exponent,
                    relative_variance_bound=cv,certificate_pass=bool(ell>0 and s>Delta))

    def iid(self,N,seed=123,center=True,clipped=True,save_samples=False):
        tic=time.perf_counter()
        mu,res,it=self.mode() if center else (np.zeros(self.m.n),0.,0)
        pre=time.perf_counter()-tic
        rng=np.random.default_rng(seed)
        vals=np.empty(N,dtype=complex)
        tic=time.perf_counter()
        for j in range(N):
            z=rng.standard_normal(self.m.n); sigma=z+mu
            F,_=self.logw(sigma,clipped=clipped)
            vals[j]=np.exp(F-self.F0-np.dot(mu,z)-.5*np.dot(mu,mu))
        elapsed=time.perf_counter()-tic
        mean=complex(np.mean(vals)); var=float(np.mean(abs(vals-mean)**2))
        out=dict(N=N,mean=[mean.real,mean.imag],log_ratio=[np.log(mean).real,np.log(mean).imag],
                 empirical_relative_variance=var/abs(mean)**2,
                 empirical_complex_standard_error=math.sqrt(var/N),
                 sample_seconds=elapsed,mode_seconds=pre,mode_iterations=it,
                 certificate=self.certificate(res))
        if save_samples: return out,vals
        return out

def wick_two_orders(model: Model):
    tic=time.perf_counter(); G=np.linalg.inv(model.A-1j*model.C)
    d=np.diag(G); g=model.g
    first=-.75*g*np.sum(d*d)
    second=2.25*g*g*np.sum(d[:,None]*d[None,:]*G**2)+.75*g*g*np.sum(G**4)
    return dict(first_order=[first.real,first.imag],
                second_order_correction=[second.real,second.imag],
                two_order_log_ratio=[(first+second).real,(first+second).imag],
                seconds=time.perf_counter()-tic)
