"""Count-compressed sampling for nonnegative Gaussian Bargmann kernels.

Input is exact rational K, ell, where the density kernel is proportional to
exp( xi.T K xi / 2 + ell.T xi ), xi=(ket variables, bra variables).
For a quantum interpretation, the supplied kernel MUST represent a physical
Gaussian density operator. The sampler checks symmetry, exchange symmetry,
nonnegativity and trace convergence, NOT general complete quantum physicality.
`pure_kernel` constructs a physical subclass without that additional promise.

Matching dynamic programming is exact and exponential in the worst herald
size. This is not an implementation of OpenAI's perfect-matching FPRAS.
All occupations use arbitrary-size Python integers. Scalar sampling uses
interval arithmetic and an explicit finite total-variation budget; see README.
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
from dataclasses import dataclass
from typing import Sequence
import random
from bigint_sampler import frac, binomial, negative_binomial, poisson, rational_choice


def zeros(n,m=None):
    if m is None: m=n
    return [[F(0) for _ in range(m)] for _ in range(n)]


def pure_kernel(B, g=None):
    B=[[frac(x) for x in row] for row in B]
    m=len(B)
    if not m or any(len(row)!=m for row in B):
        raise ValueError('B must be a nonempty square matrix')
    if any(B[i][j]<0 or B[i][j]!=B[j][i] for i in range(m) for j in range(m)):
        raise ValueError('B must be symmetric and nonnegative')
    # Exact LDL pivots of I-B establish lambda_max(B)<1; for a nonnegative
    # symmetric matrix Perron-Frobenius also bounds every absolute eigenvalue.
    T=[[F(i==j)-B[i][j] for j in range(m)] for i in range(m)]
    for v in range(m):
        pivot=T[v][v]
        if pivot<=0: raise ValueError('B is not a strict contraction')
        for i in range(v+1,m):
            for j in range(v+1,m):
                T[i][j]-=T[i][v]*T[v][j]/pivot
    if g is None: g=[F(0)]*m
    g=[frac(x) for x in g]
    if len(g)!=m or any(x<0 for x in g):
        raise ValueError('g must be a nonnegative vector')
    K=zeros(2*m)
    for i in range(m):
        for j in range(m):
            K[i][j]=K[i+m][j+m]=B[i][j]
    return K,g+g


@dataclass
class RationalRecord:
    vertex: int
    survivors: list[int]
    through: list[list[F]]
    escape: F


class RationalElimination:
    def __init__(self, W, n_internal, alpha=F(1,2)):
        W=[[frac(x) for x in row] for row in W]
        self.size=len(W); self.d=int(n_internal); self.alpha=frac(alpha)
        if any(len(row)!=self.size for row in W) or any(x<0 for row in W for x in row):
            raise ValueError('W must be square and nonnegative')
        if not 0<=self.d<=self.size or self.alpha<=0:
            raise ValueError('Invalid internal dimension or loop intensity')
        self.records=[]; self.determinant=F(1)
        for v in range(self.d):
            rem=list(range(v+1,self.size))
            p=1-W[v][v]
            if p<=0: raise ValueError('The internal Gaussian trace does not converge')
            through=zeros(len(rem))
            for a,i in enumerate(rem):
                for b,j in enumerate(rem):
                    via=W[i][v]*W[v][j]/p
                    W[i][j]+=via
                    through[a][b]=via/W[i][j] if W[i][j] else F(0)
            self.records.append(RationalRecord(v,rem,through,p))
            self.determinant*=p
        self.boundary=[row[self.d:] for row in W[self.d:]]
        self.max_scalar_calls=self.d+sum(len(r.survivors)**2 for r in self.records)

    def sample(self, boundary_counts, rng, scalar_tolerance):
        C=[[0]*self.size for _ in range(self.size)]
        t=self.size-self.d
        if len(boundary_counts)!=t or any(len(row)!=t for row in boundary_counts):
            raise ValueError('Invalid boundary counts')
        for a in range(t):
            for b in range(t):
                x=int(boundary_counts[a][b])
                if x<0: raise ValueError('Counts must be nonnegative')
                C[self.d+a][self.d+b]=x
        occupations=[0]*self.d
        for rec in reversed(self.records):
            rem=rec.survivors; incoming=[0]*len(rem); outgoing=[0]*len(rem)
            total=0
            for a,i in enumerate(rem):
                for b,j in enumerate(rem):
                    count=C[i][j]; prob=rec.through[a][b]
                    routed=binomial(count,prob,rng,scalar_tolerance) if count and prob else 0
                    C[i][j]-=routed
                    incoming[a]+=routed; outgoing[b]+=routed; total+=routed
            for a,i in enumerate(rem):
                C[i][rec.vertex]=incoming[a]
                C[rec.vertex][i]=outgoing[a]
            loops=negative_binomial(self.alpha+total,rec.escape,rng,scalar_tolerance)
            C[rec.vertex][rec.vertex]=loops
            occupations[rec.vertex]=total+loops
        if any(occupations[v]!=sum(C[v]) for v in range(self.d)):
            raise AssertionError('Occupation bookkeeping failed')
        return occupations


class RationalLoopMatching:
    def __init__(self, S, singles, counts):
        self.S=S; self.singles=singles; self.initial=tuple(map(int,counts))
        t=len(self.initial)
        if len(S)!=t or len(singles)!=t or any(x<0 for x in self.initial):
            raise ValueError('Inconsistent matching input')
        if any(S[i][j]!=S[j][i] for i in range(t) for j in range(t)):
            raise ValueError('The effective pairing matrix is not symmetric')
        @lru_cache(None)
        def Z(state):
            if not any(state): return F(1)
            a=next(i for i,n in enumerate(state) if n)
            rest=list(state); rest[a]-=1
            value=singles[a]*Z(tuple(rest)) if singles[a] else F(0)
            for b in range(t):
                mult=rest[b]
                if mult and S[a][b]:
                    nxt=rest.copy(); nxt[b]-=1
                    value+=mult*S[a][b]*Z(tuple(nxt))
            return value
        self.Z=Z; self.partition=Z(self.initial)
        if not self.partition:
            raise ValueError('The prescribed photon event has zero probability')

    def sample(self, rng):
        state=self.initial; t=len(state); C=[[0]*(t+1) for _ in range(t+1)]
        while any(state):
            a=next(i for i,n in enumerate(state) if n)
            rest=list(state); rest[a]-=1
            choices=[]; weights=[]
            if self.singles[a]:
                value=self.singles[a]*self.Z(tuple(rest))
                if value:
                    choices.append((t,tuple(rest))); weights.append(value)
            for b in range(t):
                mult=rest[b]
                if mult and self.S[a][b]:
                    nxt=rest.copy(); nxt[b]-=1; nxt=tuple(nxt)
                    value=mult*self.S[a][b]*self.Z(nxt)
                    if value:
                        choices.append((b,nxt)); weights.append(value)
            b,state=choices[rational_choice(weights,rng)]
            C[a][b]+=1
        return C


class RationalGaussian:
    def __init__(self, K, ell, herald_modes:Sequence[int]=(), herald_counts:Sequence[int]=()):
        K=[[frac(x) for x in row] for row in K]; ell=list(map(frac,ell))
        d0=len(K)
        if not d0 or d0%2 or len(ell)!=d0 or any(len(row)!=d0 for row in K):
            raise ValueError('K needs a doubled, nonempty mode dimension')
        self.m=m=d0//2
        if any(x<0 for row in K for x in row) or any(x<0 for x in ell):
            raise ValueError('The Bargmann coefficients must be nonnegative')
        swap=lambda i: (i+m)%(2*m)
        if any(K[i][j]!=K[j][i] or K[i][j]!=K[swap(i)][swap(j)]
               for i in range(d0) for j in range(d0)) or any(ell[i]!=ell[swap(i)] for i in range(d0)):
            raise ValueError('Kernel lacks real ket/bra exchange symmetry')
        self.K=K; self.ell=ell
        H=list(map(int,herald_modes)); hc=list(map(int,herald_counts))
        if len(H)!=len(hc) or len(set(H))!=len(H) or any(not 0<=i<m for i in H) or any(x<0 for x in hc):
            raise ValueError('Invalid herald specification')
        self.H=H; self.hc=hc; self.U=U=[i for i in range(m) if i not in H]
        ui=U+[i+m for i in U]; hi=H+[i+m for i in H]
        d=len(ui); t=len(hi); W=zeros(d+t+1)
        # A single ghost vertex encodes displacement as positive open paths.
        for a,i in enumerate(ui):
            si=swap(i)
            for b,j in enumerate(ui): W[a][b]=K[si][j]
            for b,j in enumerate(hi): W[a][d+b]=K[si][j]
            W[a][-1]=ell[si]
        for a,i in enumerate(hi):
            for b,j in enumerate(ui): W[d+a][b]=K[i][j]
            for b,j in enumerate(hi): W[d+a][d+b]=K[i][j]
            W[d+a][-1]=ell[i]
        for b,j in enumerate(ui): W[-1][b]=ell[j]
        for b,j in enumerate(hi): W[-1][d+b]=ell[j]
        self.W=W; self.engine=RationalElimination(W,d)
        S=[row[:t] for row in self.engine.boundary[:t]]
        singles=[self.engine.boundary[a][-1] for a in range(t)]
        self.source_rate=self.engine.boundary[-1][-1]/2
        self.matching=RationalLoopMatching(S,singles,hc+hc)
        # Check convergence of the entire supplied state, not just the residual.
        if H:
            fullW=[[K[swap(i)][j] for j in range(d0)] for i in range(d0)]
            RationalElimination(fullW,d0)

    @classmethod
    def from_pure(cls, B, g=None, herald_modes=(), herald_counts=()):
        K,ell=pure_kernel(B,g)
        return cls(K,ell,herald_modes,herald_counts)

    def sample(self, rng:random.Random, tolerance=F(1,10**10)):
        tolerance=frac(tolerance)
        if not 0<tolerance<F(1,4): raise ValueError('Invalid total-variation budget')
        scalar=tolerance/(self.engine.max_scalar_calls+1)
        C=self.matching.sample(rng)
        C[-1][-1]+=poisson(self.source_rate,rng,scalar)
        aux=self.engine.sample(C,rng,scalar)
        n=len(self.U)
        return [aux[i]+aux[i+n] for i in range(n)]

    def pgf_parts(self,z):
        """Exact rational ingredients of the conditional PGF.

        PGF = sqrt(det_ratio) * exp(source_difference) * matching_ratio.
        No numerical differentiation or photon enumeration is used here.
        """
        z=list(map(frac,z)); n=len(self.U)
        if len(z)!=n or any(not 0<=x<=1 for x in z):
            raise ValueError('z needs one [0,1] value per output mode')
        W=[row.copy() for row in self.W]
        for i in range(2*n): W[i]=[x*z[i%n] for x in W[i]]
        engine=RationalElimination(W,2*n)
        t=2*len(self.H)
        S=[row[:t] for row in engine.boundary[:t]]
        singles=[engine.boundary[a][-1] for a in range(t)]
        try: matching=RationalLoopMatching(S,singles,self.hc+self.hc).partition
        except ValueError as ex:
            if 'zero probability' not in str(ex): raise
            matching=F(0)
        return (self.engine.determinant/engine.determinant,
                engine.boundary[-1][-1]/2-self.source_rate,
                matching/self.matching.partition)


def trace_modes(K, ell, keep):
    """Trace out other modes; preserve a supplied physical positive kernel."""
    keep=list(map(int,keep))
    model=RationalGaussian(K,ell,keep,[0]*len(keep))
    t=2*len(keep)
    return ([row[:t] for row in model.engine.boundary[:t]],
            [model.engine.boundary[a][-1] for a in range(t)])


def _inverse(A):
    n=len(A)
    rows=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    for k in range(n):
        pivot=next((i for i in range(k,n) if rows[i][k]),None)
        if pivot is None: raise ValueError('Singular matrix')
        rows[k],rows[pivot]=rows[pivot],rows[k]
        p=rows[k][k]; rows[k]=[x/p for x in rows[k]]
        for i in range(n):
            if i!=k and rows[i][k]:
                p=rows[i][k]
                rows[i]=[a-p*b for a,b in zip(rows[i],rows[k])]
    return [row[n:] for row in rows]


def _matmul(A,B):
    if not A: return []
    r=len(A); c=len(B[0]) if B else 0; n=len(B)
    return [[sum((A[i][k]*B[k][j] for k in range(n)),F(0)) for j in range(c)] for i in range(r)]


def mean_counts(model:RationalGaussian):
    """Exact conditional first moments via differentiated marginalization."""
    n=len(model.U); d=2*n; t=2*len(model.H)
    if not n: return []
    M=[row[:d] for row in model.W[:d]]
    G=_inverse([[F(i==j)-M[i][j] for j in range(d)] for i in range(d)])
    GX=[[G[i][(j+n)%d] for j in range(d)] for i in range(d)]
    ui=model.U+[i+model.m for i in model.U]
    hi=model.H+[i+model.m for i in model.H]
    KUH=[[model.K[i][j] for j in hi] for i in ui]
    KHU=[[model.K[i][j] for j in ui] for i in hi]
    lu=[[model.ell[i]] for i in ui]
    baseS=model.matching.S; singles=model.matching.singles
    means=[]
    for mode in range(n):
        Jp=[[sum((G[i][a]*GX[a][j] for a in (mode,mode+n)),F(0))
             for j in range(d)] for i in range(d)]
        Sp=_matmul(_matmul(KHU,Jp),KUH) if t else []
        lp=_matmul(_matmul(KHU,Jp),lu) if t else []
        source=sum((lu[i][0]*Jp[i][j]*lu[j][0] for i in range(d) for j in range(d)),F(0))/2
        loops=(G[mode][mode]+G[mode+n][mode+n]-2)/2
        @lru_cache(None)
        def derivative(state):
            if not any(state): return F(0)
            a=next(i for i,k in enumerate(state) if k)
            rest=list(state); rest[a]-=1; rt=tuple(rest)
            value=lp[a][0]*model.matching.Z(rt)+singles[a]*derivative(rt)
            for b in range(t):
                mult=rest[b]
                if mult:
                    nxt=rest.copy(); nxt[b]-=1; nxt=tuple(nxt)
                    value+=mult*(Sp[a][b]*model.matching.Z(nxt)+baseS[a][b]*derivative(nxt))
            return value
        boundary=derivative(model.matching.initial)/model.matching.partition if t else F(0)
        means.append(loops+source+boundary)
    return means


def log_herald_probability(model:RationalGaussian, digits:int=80):
    """High-precision diagnostic only. Sampling never uses this probability."""
    import mpmath as mp
    if not model.H: return mp.mpf(0)
    full=RationalGaussian(model.K,model.ell)
    def logF(q):
        return mp.log(q.numerator)-mp.log(q.denominator)
    with mp.workdps(digits):
        result=(logF(full.engine.determinant)-logF(model.engine.determinant))/2
        ds=model.source_rate-full.source_rate
        result+=mp.mpf(ds.numerator)/ds.denominator
        result+=logF(model.matching.partition)
        result-=sum(mp.loggamma(k+1) for k in model.hc)
        return +result
