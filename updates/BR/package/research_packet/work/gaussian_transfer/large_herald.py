"""Binary-large one-mode heralds, zero displacement, positive Gaussian kernels.
New aggregate matching layer; inherited experimental interval scalar backend.
This software does not establish certified mpmath interval correctness.
"""
from fractions import Fraction as F
import mpmath as mp
from bigint_sampler import DyadicUnimodal, _as_iv, _parameter_bits, frac
from rational_gaussian import RationalGaussian, pure_kernel

class AggregateMatching:
    def __init__(self, a, b, h):
        self.a, self.b, self.h = a, b, int(h)
        if h<0 or a<0 or b<0: raise ValueError('Nonnegative parameters required')
        self.parity=h%2; self.maximum=h//2; self.cached={}
        self.deterministic=None
        if h==0: self.deterministic=0
        elif a==0 and b>0: self.deterministic=h
        elif b==0 and a>0 and h%2==0: self.deterministic=0
        elif not a or not b: raise ValueError('Zero-probability herald')
        if self.deterministic is not None:
            self.mode=(self.deterministic-self.parity)//2
            return
        # Locate first decreasing adjacent step. The upper endpoint has no next step.
        lo,hi=0,self.maximum
        while lo<hi:
            j=(lo+hi)//2; k=self.parity+2*j
            if b*b*(h-k)**2 <= a*a*(k+1)*(k+2): hi=j
            else: lo=j+1
        self.mode=lo
    def law(self,tolerance):
        tolerance=frac(tolerance)
        if tolerance in self.cached:return self.cached[tolerance]
        h,e,a,b=self.h,self.parity,self.a,self.b
        def logratio(j,mode):
            k=e+2*j; km=e+2*mode
            q=(h-k)//2; qm=(h-km)//2
            return ((k-km)*mp.iv.log(2*_as_iv(b)/_as_iv(a))
                    +mp.iv.loggamma(km+1)-mp.iv.loggamma(k+1)
                    +2*(mp.iv.loggamma(qm+1)-mp.iv.loggamma(q+1)))
        law=DyadicUnimodal(self.maximum,self.mode,logratio,tolerance,
                          _parameter_bits(h,a,b))
        self.cached[tolerance]=law
        return law
    def draw_k(self,rng,tolerance):
        if self.deterministic is not None:return self.deterministic
        return self.parity+2*self.law(tolerance).draw(rng)
    def sample(self,rng,tolerance):
        k=self.draw_k(rng,tolerance); q=(self.h-k)//2
        return [[q,k,0],[0,q,0],[0,0,0]]

class LargeHeraldGaussian:
    def __init__(self,K,herald_mode,h):
        # Construct h=0 to bypass inherited token DP altogether.
        self.base=RationalGaussian(K,[F(0)]*len(K),[herald_mode],[0])
        boundary=self.base.engine.boundary
        if boundary[0][0]!=boundary[1][1] or boundary[0][1]!=boundary[1][0]:
            raise AssertionError('Schur boundary exchange symmetry failed')
        self.matching=AggregateMatching(boundary[0][0],boundary[0][1],int(h))
        self.h=int(h)
    @classmethod
    def from_pure(cls,B,herald_mode,h):
        K,_=pure_kernel(B)
        return cls(K,herald_mode,h)
    def sample(self,rng,tolerance=F(1,10**10)):
        tolerance=frac(tolerance)
        if not 0<tolerance<F(1,4):raise ValueError('Invalid tolerance')
        C=self.matching.sample(rng,tolerance/2)
        engine=self.base.engine
        aux=engine.sample(C,rng,tolerance/(2*max(1,engine.max_scalar_calls)))
        n=len(self.base.U)
        return [aux[i]+aux[i+n] for i in range(n)]
