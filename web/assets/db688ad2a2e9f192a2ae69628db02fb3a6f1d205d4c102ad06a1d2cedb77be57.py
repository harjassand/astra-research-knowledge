from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from typing import Sequence
import math, time
import numpy as np

@dataclass
class Record:
    vertex: int
    survivors: np.ndarray
    through_probability: np.ndarray
    escape_probability: float

class EliminationSampler:
    """Nonnegative loop soup, optionally with fixed boundary-to-boundary paths.

    The internal block must have spectral radius below one. Boundary vertices
    are never traversed internally. Counts are directed edge multiplicities.
    The ideal-arithmetic construction is exact; this implementation uses
    double-precision arithmetic and NumPy integer-valued random variates.
    """
    def __init__(self, W: np.ndarray, n_internal: int, alpha: float = 0.5):
        W=np.array(W,dtype=float,copy=True)
        if W.ndim!=2 or W.shape[0]!=W.shape[1]:
            raise ValueError('W must be square')
        if not np.all(np.isfinite(W)) or np.any(W<0):
            raise ValueError('W must be finite and entrywise nonnegative')
        if not 0<=n_internal<=len(W) or not alpha>0:
            raise ValueError('Invalid internal size or alpha')
        self.size=len(W); self.n_internal=n_internal; self.alpha=alpha
        self.records=[]; self.logdet=0.0
        for v in range(n_internal):
            rem=np.arange(v+1,self.size)
            escape=1.0-W[v,v]
            if not escape>0:
                raise ValueError('Nonpositive pivot: unstable block or insufficient precision')
            via=np.outer(W[rem,v], W[v,rem])/escape
            direct=W[np.ix_(rem,rem)]
            reduced=direct+via
            probs=np.divide(via,reduced,out=np.zeros_like(via),where=reduced>0)
            if np.any(probs<0) or np.any(probs>1):
                raise ArithmeticError('Invalid routing probability')
            self.records.append(Record(v,rem,probs,escape))
            self.logdet+=math.log(escape)
            W[np.ix_(rem,rem)]=reduced
        self.boundary=W[n_internal:,n_internal:].copy()

    def sample(self, rng: np.random.Generator, boundary_counts: np.ndarray|None=None)->np.ndarray:
        C=np.zeros((self.size,self.size),dtype=np.int64)
        if boundary_counts is not None:
            bc=np.asarray(boundary_counts,dtype=np.int64)
            if bc.shape!=self.boundary.shape or np.any(bc<0):
                raise ValueError('Invalid boundary edge counts')
            C[self.n_internal:,self.n_internal:]=bc
        occ=np.zeros(self.n_internal,dtype=np.int64)
        for rec in reversed(self.records):
            rem=rec.survivors; sub=C[np.ix_(rem,rem)]
            via=rng.binomial(sub,rec.through_probability)
            C[np.ix_(rem,rem)]=sub-via
            # Refuse a regime where an int64 reduction could overflow.
            if sum(int(x) for x in via.flat)>np.iinfo(np.int64).max//4:
                raise OverflowError('Use the rational arbitrary-integer backend')
            incoming=via.sum(axis=1); outgoing=via.sum(axis=0)
            K=int(incoming.sum())
            C[rem,rec.vertex]=incoming
            C[rec.vertex,rem]=outgoing
            if rec.escape_probability==1:
                loops=0
            else:
                loops=int(rng.negative_binomial(self.alpha+K,rec.escape_probability))
            if K+loops>np.iinfo(np.int64).max:
                raise OverflowError('Use arbitrary-precision backend for these counts')
            C[rec.vertex,rec.vertex]=loops
            occ[rec.vertex]=K+loops
        assert np.array_equal(occ,C[:self.n_internal].sum(axis=1))
        return occ

class MatchingSampler:
    """Exact finite-state recurrence for labeled matchings with repeated types.

    Arithmetic is log-domain floating point. State count is bounded by
    product(counts[a]+1), not the number of pairings.
    """
    def __init__(self,S:np.ndarray,counts:Sequence[int]):
        self.S=np.asarray(S,dtype=float)
        self.initial=tuple(int(n) for n in counts)
        t=len(self.initial)
        if self.S.shape!=(t,t) or any(n<0 for n in self.initial):
            raise ValueError('Inconsistent matching input')
        if sum(self.initial)%2:
            raise ValueError('Odd number of matching tokens')
        if not np.allclose(self.S,self.S.T,rtol=1e-9,atol=0):
            raise ArithmeticError('Effective pairing matrix lost symmetry')
        self.S=(self.S+self.S.T)/2
        @lru_cache(None)
        def logZ(state):
            if not any(state): return 0.0
            a=next(i for i,n in enumerate(state) if n)
            terms=[]
            for b in range(t):
                multiplicity=state[b]-(b==a)
                if multiplicity<=0 or self.S[a,b]<=0: continue
                nxt=list(state); nxt[a]-=1; nxt[b]-=1
                rest=logZ(tuple(nxt))
                if math.isfinite(rest):
                    terms.append(math.log(multiplicity)+math.log(self.S[a,b])+rest)
            if not terms: return -math.inf
            mx=max(terms)
            return mx+math.log(sum(math.exp(x-mx) for x in terms))
        self.logZ=logZ
        self.log_partition=logZ(self.initial)
        if not math.isfinite(self.log_partition):
            raise ValueError('The prescribed photon event has zero probability')

    def sample(self,rng):
        state=self.initial; C=np.zeros_like(self.S,dtype=np.int64)
        while any(state):
            a=next(i for i,n in enumerate(state) if n)
            opts=[]; vals=[]
            for b in range(len(state)):
                mult=state[b]-(b==a)
                if mult<=0 or self.S[a,b]<=0: continue
                nxt=list(state); nxt[a]-=1; nxt[b]-=1; nxt=tuple(nxt)
                rest=self.logZ(nxt)
                if math.isfinite(rest):
                    opts.append((b,nxt))
                    vals.append(math.log(mult)+math.log(self.S[a,b])+rest)
            vmax=max(vals); probs=np.exp(np.array(vals)-vmax); probs/=probs.sum()
            b,state=opts[int(rng.choice(len(opts),p=probs))]
            C[a,b]+=1
        return C

class PositiveGBS:
    def __init__(self,B:np.ndarray,herald_modes:Sequence[int]=(),herald_counts:Sequence[int]=()):
        B=np.asarray(B,dtype=float)
        if B.ndim!=2 or B.shape[0]!=B.shape[1] or not np.allclose(B,B.T,rtol=1e-13,atol=0):
            raise ValueError('B must be symmetric and square')
        if np.any(B<0) or not np.all(np.isfinite(B)):
            raise ValueError('B must be finite and entrywise nonnegative')
        if np.max(np.abs(np.linalg.eigvalsh(B)))>=1:
            raise ValueError('B must be a strict contraction')
        self.B=B; self.m=len(B)
        H=list(map(int,herald_modes)); hc=list(map(int,herald_counts))
        if len(H)!=len(hc) or len(set(H))!=len(H) or any(not 0<=i<self.m for i in H) or any(n<0 for n in hc):
            raise ValueError('Invalid herald specification')
        U=[i for i in range(self.m) if i not in H]
        self.H=H; self.U=U; self.hc=hc
        K=np.block([[B,np.zeros_like(B)],[np.zeros_like(B),B]])
        ui=U+[i+self.m for i in U]; hi=H+[i+self.m for i in H]
        d=len(ui); t=len(hi)
        X=np.zeros((d,d)); s=len(U)
        X[:s,s:]=np.eye(s); X[s:,:s]=np.eye(s)
        W=np.zeros((d+t,d+t))
        W[:d,:d]=X@K[np.ix_(ui,ui)]
        W[:d,d:]=X@K[np.ix_(ui,hi)]
        W[d:,:d]=K[np.ix_(hi,ui)]
        W[d:,d:]=K[np.ix_(hi,hi)]
        self.W=W; self.engine=EliminationSampler(W,d)
        self.matching=MatchingSampler(self.engine.boundary,hc+hc)
        # No success probability is used by the sampling routine.
        _,ldm=np.linalg.slogdet(np.eye(self.m)-B)
        _,ldp=np.linalg.slogdet(np.eye(self.m)+B)
        self.log_herald_probability=.5*(ldm+ldp-self.engine.logdet)+self.matching.log_partition-sum(math.lgamma(n+1) for n in hc)

    def sample(self,rng:np.random.Generator)->np.ndarray:
        bc=self.matching.sample(rng)
        aux=self.engine.sample(rng,bc)
        s=len(self.U)
        if any(int(a)+int(b)>np.iinfo(np.int64).max for a,b in zip(aux[:s],aux[s:])):
            raise OverflowError('Use the rational arbitrary-integer backend')
        return aux[:s]+aux[s:]

    def sample_many(self,n:int,seed:int=0)->np.ndarray:
        rng=np.random.default_rng(seed)
        return np.array([self.sample(rng) for _ in range(n)],dtype=np.int64)

    def conditional_pgf(self,z:Sequence[float])->float:
        z=np.array(z,dtype=float)
        if z.shape!=(len(self.U),) or np.any(z<0) or np.any(z>1):
            raise ValueError('z must have one [0,1] entry per unobserved mode')
        d=2*len(self.U); W=self.W.copy()
        W[:d,:]*=np.r_[z,z][:,None]
        e=EliminationSampler(W,d)
        try:
            ms=MatchingSampler(e.boundary,self.hc+self.hc)
        except ValueError as exc:
            if 'zero probability' in str(exc): return 0.0
            raise
        return math.exp(.5*(self.engine.logdet-e.logdet)+ms.log_partition-self.matching.log_partition)

if __name__=='__main__':
    B=np.array([[.13,.21,.08],[.21,.19,.12],[.08,.12,.10]])
    for H,h in [((),()),((0,),(1,)),((0,),(2,)),((0,1),(1,1)),((0,),(0,))]:
        p=PositiveGBS(B,H,h)
        t=time.perf_counter(); samples=p.sample_many(10000,7)
        z=np.linspace(.65,.85,len(p.U))
        values=np.prod(z**samples,axis=1)
        mean=values.mean(); se=values.std(ddof=1)/np.sqrt(len(values)); exact=p.conditional_pgf(z)
        print(H,h,'pgf',mean,'target',exact,'zscore',(mean-exact)/se,'Pherald',math.exp(p.log_herald_probability),'sec',time.perf_counter()-t)
