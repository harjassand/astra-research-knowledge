"""Binary-large one-mode heralds, zero displacement, positive Gaussian kernels.
New aggregate matching layer with FLINT/Arb interval scalar backend.
Ordinary software dependency; this is not a formal verification claim.
"""
from fractions import Fraction as F
import operator
from flint import arb
from bigint_sampler_arb import DyadicUnimodal, _as_iv, _parameter_bits, frac
from rational_gaussian_arb import RationalGaussian, pure_kernel

def _strict_integer(value, name):
    if isinstance(value, bool):
        raise TypeError(name+' must be an integer, not bool')
    try:
        return operator.index(value)
    except TypeError:
        raise TypeError(name+' must be an integer') from None

class TicketBudgetExceeded(RuntimeError):
    pass

class CappedTickets:
    """Uniform integer tickets, capped with a caller-allocated TV budget.

    On exhaustion the whole sample returns its documented fixed fallback.
    getrandbits is the unbiased-independent-bit interface in the theorem.
    """
    def __init__(self, rng, max_calls, failure_budget):
        self.rng=rng; self.max_calls=max_calls; self.calls=0; self.bits=0
        q=F(max_calls)/failure_budget
        target=-(-q.numerator//q.denominator)
        self.attempt_cap=target.bit_length()
    def randrange(self, low, high=None):
        if high is None: low,high=0,low
        width=high-low
        if width<=0: raise ValueError('Empty ticket range')
        self.calls+=1
        if self.calls>self.max_calls:
            raise AssertionError('Internal random-ticket bound was exceeded')
        if width==1:return low
        k=(width-1).bit_length()
        for _ in range(self.attempt_cap):
            self.bits+=k
            value=self.rng.getrandbits(k)
            if value<width:return low+value
        raise TicketBudgetExceeded('Random-ticket attempt cap reached')

class AggregateMatching:
    def __init__(self, a, b, h):
        h=_strict_integer(h,'herald count')
        a,b=frac(a),frac(b)
        self.a, self.b, self.h = a, b, h
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
            return ((k-km)*(2*_as_iv(b)/_as_iv(a)).log()
                    +arb(km+1).lgamma()-arb(k+1).lgamma()
                    +2*(arb(qm+1).lgamma()-arb(q+1).lgamma()))
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
        h=_strict_integer(h,'herald count')
        herald_mode=_strict_integer(herald_mode,'herald mode')
        if h<0:raise ValueError('Negative herald count')
        # Construct h=0 to bypass inherited token DP altogether.
        self.base=RationalGaussian(K,[F(0)]*len(K),[herald_mode],[0])
        boundary=self.base.engine.boundary
        if boundary[0][0]!=boundary[1][1] or boundary[0][1]!=boundary[1][0]:
            raise AssertionError('Schur boundary exchange symmetry failed')
        self.matching=AggregateMatching(boundary[0][0],boundary[0][1],h)
        self.h=h
    @classmethod
    def from_pure(cls,B,herald_mode,h):
        K,_=pure_kernel(B)
        return cls(K,herald_mode,h)
    def sample(self,rng,tolerance=F(1,10**10)):
        tolerance=frac(tolerance)
        if not 0<tolerance<F(1,4):raise ValueError('Invalid tolerance')
        engine=self.base.engine
        scalar_calls=max(1,engine.max_scalar_calls)
        # Reserve epsilon/4 for capped uniform tickets, and split the rest.
        matching_tolerance=3*tolerance/8
        scalar_tolerance=3*tolerance/(8*scalar_calls)
        max_attempts=max(4*(q.denominator.bit_length()+4)
                         for q in (matching_tolerance,scalar_tolerance))
        max_tickets=3*(engine.max_scalar_calls+1)*max_attempts
        tickets=CappedTickets(rng,max_tickets,tolerance/4)
        self.last_ticket_fallback=False
        try:
            C=self.matching.sample(tickets,matching_tolerance)
            aux=engine.sample(C,tickets,scalar_tolerance)
            n=len(self.base.U)
            answer=[aux[i]+aux[i+n] for i in range(n)]
        except TicketBudgetExceeded:
            self.last_ticket_fallback=True
            answer=[0]*len(self.base.U)
        self.last_ticket_count=tickets.calls
        self.last_random_bits=tickets.bits
        self.last_ticket_attempt_cap=tickets.attempt_cap
        self.last_ticket_bound=max_tickets
        return answer
