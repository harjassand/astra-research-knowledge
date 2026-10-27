"""Runtime for the certified module. No numerical or symbolic dependencies.

The caller supplies a cheap record z and a callback that returns the current
ALREADY CLASSICAL x only when charged. The controller must not observe the
returned cost flag. Passing this flag back to it changes the experiment.
"""
from fractions import Fraction as F
from math import lcm, comb
from verify_certificate import verify


class BudgetExceeded(Exception):pass


class Table:
    def __init__(self,weights):
        assert weights and sum(weights)==1 and all(v>=0 for v in weights)
        self.den=lcm(*(v.denominator for v in weights));self.cuts=[];acc=0
        for w in weights:
            acc+=w.numerator*(self.den//w.denominator);self.cuts.append(acc)
        assert acc==self.den
    def sample(self,rng):
        bits=(self.den-1).bit_length()
        r=rng.getrandbits(bits)
        while r>=self.den:r=rng.getrandbits(bits)
        return next(i for i,cut in enumerate(self.cuts) if r<cut)


class Replacement:
    def __init__(self,cert,rng,budget=None):
        check=verify(cert);self.rng=rng;self.budget=budget;self.reads=0
        U=[[F(v) for v in row] for row in cert['U']]
        self.ny=len(U);nz=len(U[0]);nx=len(cert['K'][0])
        self.branch=[Table([U[y][z] for y in range(self.ny)]+[1-sum(U[y][z] for y in range(self.ny))]) for z in range(nz)]
        D=[[F(v) for v in row] for row in check['residual']];qx=list(map(F,check['q_by_input']))
        self.after_read=[Table([D[y][x]/qx[x] for y in range(self.ny)]) if qx[x] else None for x in range(nx)]
    def step(self,z,read_raw):
        branch=self.branch[z].sample(self.rng)
        if branch<self.ny:return branch,False
        if self.budget is not None and self.reads>=self.budget:raise BudgetExceeded
        x=read_raw();self.reads+=1
        table=self.after_read[x]
        if table is None:raise ValueError('supplied (x,z) or raw callback violates channel contract')
        return table.sample(self.rng),True


def binomial_tail(T,q,B):
    """Exact Pr[Bin(T,q)>B], with integer arithmetic.

    Output bits can grow linearly with T; no poly(log T) claim is possible.
    """
    q=F(q);assert isinstance(T,int) and T>=0 and 0<=q<=1
    if B<0:return F(1)
    if B>=T or not q:return F(0)
    if q==1:return F(1)
    a,b=q.numerator,q.denominator
    num=(b-a)**T;cdf=0
    for k in range(B+1):
        cdf+=num
        if k<B:
            dividend=num*(T-k)*a;divisor=(k+1)*(b-a)
            num,rem=divmod(dividend,divisor);assert rem==0
    return F(b**T-cdf,b**T)


def budget_for_error(T,q,delta):
    """Smallest budget certified by this binomial tail bound, no global claim."""
    delta=F(delta);assert 0<=delta<=1
    lo,hi=-1,T
    while hi-lo>1:
        mid=(lo+hi)//2
        if binomial_tail(T,q,mid)<=delta:hi=mid
        else:lo=mid
    return hi
