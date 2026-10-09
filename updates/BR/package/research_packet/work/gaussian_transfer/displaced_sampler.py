"""Displaced, nonnegative, one-herald Gaussian count sampler.

Supplemental implementation: frozen undisplaced files are imported unchanged.
Arb is an ordinary trusted numerical library, not a formal proof kernel. Input
kernels must satisfy the physical-state promise documented by RationalGaussian.
The exact-rational kernel is supplied input; its acquisition cost is excluded.

For independent unbiased getrandbits, successful numerical enclosures imply
output TV error <= tolerance. Explicit numerical precision failures raise;
they are NOT turned into samples. No uniform runtime bound for the installed
Arb implementation is asserted. Python's seeded Random is for diagnostics.
"""
from fractions import Fraction as F
from functools import lru_cache
from bisect import bisect_right
from flint import arb, ctx
from bigint_sampler_arb import (DyadicUnimodal, frac, _as_iv, _parameter_bits,
                               _floor_scaled_arb, _ceil_scaled_arb, poisson)
from large_herald_arb import (AggregateMatching, CappedTickets,
                              TicketBudgetExceeded, _strict_integer)
from rational_gaussian_arb import RationalGaussian, pure_kernel
from displaced_evaluator import log_H


def _ceil(q):
    q=F(q)
    return -(-q.numerator//q.denominator)


class EnclosureFailure(ArithmeticError):
    """A requested numerical enclosure could not be established."""


class ParityEnvelope:
    """Cross-count law b**k/k! * H_(h-k)(a,c)**2, with b,c positive.

    Each parity subsequence is log-concave. An approximate anchor is located by
    comparisons of interval ratios, terminating near ties without deciding
    equality of transcendental numbers. Along either side, an increase away
    from the anchor is bounded by exp(h*delta)<2. Heights twice the nearest
    endpoint therefore dominate each dyadic distance block. Predecessor block
    charging bounds the exact envelope mass by 12 times the target mass.
    """
    def __init__(self,a,b,c,h,tolerance):
        self.a,self.b,self.c=map(frac,(a,b,c))
        self.h=_strict_integer(h,'herald count')
        self.tolerance=frac(tolerance)
        if self.h<1 or self.a<0 or self.b<=0 or self.c<=0:
            raise ValueError('Need h>=1, a>=0, b>0, c>0')
        if not 0<self.tolerance<F(1,4):raise ValueError('Invalid tolerance')
        h=self.h
        self.bits=(h+1).bit_length()+_ceil(128/self.tolerance).bit_length()
        self.scale=1<<self.bits
        self.input_bits=_parameter_bits(a,b,c,h)
        self.num_log_H=0
        self.max_precision_used=0
        self.interval_refinements=0
        self.num_bounds=0
        self.total_attempts=0
        self.num_draws=0
        self.fallback_count=0
        self.last_attempts=0
        self.used_fallback=False
        self.delta=F(1,4*(h+1))
        self.anchor_diagnostics=[]
        self.anchors=[]
        for parity in (0,1):
            maximum=(h-parity)//2
            self.anchors.append(self._anchor(parity,maximum))
        # Absolute logweight intervals of width <= 1/8 suffice for a scale.
        # Store their exact upper endpoint, not a persistent uncertain ball.
        values=[self._logweight_narrow(e+2*self.anchors[e],4) for e in (0,1)]
        # Arb endpoint extraction itself rounds at the current ctx precision.
        # Extract inside high precision; default 53 bits can shift a huge log
        # center by thousands and invalidate the lower bound on scaled mass.
        with ctx.workprec(self._precision(self.bits+16)):
            upper=[v.upper() for v in values]
            lower=[v.lower() for v in values]
            if any(hi-lo>arb(1)/8 for hi,lo in zip(upper,lower)):
                raise EnclosureFailure('Reference interval is too wide')
            selected=max(range(2),key=lambda e:upper[e])
            self.reference=upper[selected]
            self.reference_k=selected+2*self.anchors[selected]
        self.bounds=lru_cache(maxsize=None)(self._bounds)
        self.blocks=[]
        self.cumulative=[]
        total=0
        for e in (0,1):
            maximum=(h-e)//2; mode=self.anchors[e]
            rectangles=[(mode,mode,mode)]
            distance=1
            while distance<=max(mode,maximum-mode):
                if distance<=mode:
                    rectangles.append((max(0,mode-(2*distance-1)),mode-distance,mode-distance))
                if mode+distance<=maximum:
                    rectangles.append((mode+distance,min(maximum,mode+2*distance-1),mode+distance))
                distance*=2
            for low,high,near in rectangles:
                _,upper=self.bounds(e+2*near)
                height=2*upper
                total+=(high-low+1)*height
                self.blocks.append((e,low,high,height))
                self.cumulative.append(total)
        if total<=0:raise EnclosureFailure('Empty positive-law envelope')
        self.total=total
        # G >= exp(-1/8)>1/2. Downward rounding loses <=2(h+1)/scale;
        # upward envelope rounding adds <=4(h+1)/scale. Thus acceptance >1/64.
        # (63/64)**128 < 1/2, giving cap-failure far below tolerance/16.
        self.max_attempts=128*(self.tolerance.denominator.bit_length()+8)

    def _precision(self,p):
        return max(128,p+2*self.input_bits+2*self.h.bit_length()+128)

    @lru_cache(maxsize=None)
    def _coefficient(self,n,p):
        self.num_log_H+=1
        value,meta=log_H(n,self.a,self.c,p)
        if value is None or not value.is_finite():
            raise EnclosureFailure('Positive coefficient had no finite enclosure')
        self.max_precision_used=max(self.max_precision_used,meta.get('working_bits',p))
        return value

    def _logweight(self,k,p):
        with ctx.workprec(self._precision(p)):
            return (k*_as_iv(self.b).log()-arb(k+1).lgamma()
                    +2*self._coefficient(self.h-k,p))

    def _logweight_narrow(self,k,target_bits):
        p=max(16,target_bits+8)
        while True:
            with ctx.workprec(self._precision(p)):
                value=self._logweight(k,p)
                if value.is_finite() and 2*value.rad()<=arb(2)**(-target_bits):
                    return value
            p*=2

    def _anchor(self,e,maximum):
        lo,hi=0,maximum
        while lo<hi:
            j=(lo+hi)//2; k=e+2*j; n=self.h-k
            p=max(16,self.h.bit_length()+12)
            while True:
                with ctx.workprec(self._precision(p)):
                    ratio=(2*_as_iv(self.b).log()-arb(k+1).log()-arb(k+2).log()
                           +2*(self._coefficient(n-2,p)-self._coefficient(n,p)))
                    delta=_as_iv(self.delta)
                    if ratio.upper()<0:
                        hi=j;break
                    if ratio.lower()>0:
                        lo=j+1;break
                    if ratio.lower()>=-delta and ratio.upper()<=delta:
                        self.anchor_diagnostics.append({'parity':e,'kind':'near_tie','index':j,'precision':p})
                        return j
                p*=2
        self.anchor_diagnostics.append({'parity':e,'kind':'sign_bracket','index':lo})
        return lo

    def _bounds(self,k):
        # A coarse preliminary evaluation cheaply certifies many negligible
        # tails. Otherwise increase precision until at most two grid units.
        p=24
        refinement=0
        while True:
            with ctx.workprec(self._precision(max(p,self.bits+16))):
                logvalue=self._logweight(k,p)-self.reference
                if logvalue.upper() < -(self.bits+1)*arb(2).log():
                    return 0,1
                value=logvalue.exp()
                if not value.is_finite():raise EnclosureFailure('Nonfinite normalized weight')
                self.num_bounds+=1
                lo=max(0,_floor_scaled_arb(value.lower(),self.bits))
                hi=_ceil_scaled_arb(value.upper(),self.bits)
                # No clamping at 1: a near-tie anchor can lie below the peak.
                if lo<=hi and hi-lo<=2:
                    self.interval_refinements+=refinement>0
                    return lo,hi
            p=max(2*p,self.bits+8)
            refinement+=1

    def draw(self,rng):
        self.num_draws+=1
        for attempts in range(1,self.max_attempts+1):
            j=bisect_right(self.cumulative,rng.randrange(self.total))
            e,low,high,height=self.blocks[j]
            point=e+2*rng.randrange(low,high+1)
            accepted,_=self.bounds(point)
            if accepted>height:raise ArithmeticError('Parity envelope consistency failed')
            if rng.randrange(height)<accepted:
                self.last_attempts=attempts
                self.total_attempts+=attempts
                return point
        self.used_fallback=True
        self.fallback_count+=1
        self.last_attempts=self.max_attempts
        self.total_attempts+=self.max_attempts
        return self.reference_k


class DisplacedAggregateMatching:
    """Count-compressed matching of a two-colour equal-count boundary."""
    def __init__(self,a,b,c,h):
        self.a,self.b,self.c=map(frac,(a,b,c))
        self.h=_strict_integer(h,'herald count')
        if self.h<0 or min(self.a,self.b,self.c)<0:
            raise ValueError('Nonnegative matching inputs required')
        self.undisplaced=AggregateMatching(self.a,self.b,self.h) if not self.c else None
        self.cached={}
        self.conditional_cached={}

    def law(self,tolerance):
        tolerance=frac(tolerance)
        if not 0<tolerance<F(1,4):raise ValueError('Invalid tolerance')
        if self.undisplaced is not None:
            return (None if self.undisplaced.deterministic is not None
                    else self.undisplaced.law(tolerance))
        if not self.h or not self.b:return None
        if tolerance not in self.cached:
            self.cached[tolerance]=ParityEnvelope(self.a,self.b,self.c,self.h,tolerance)
        return self.cached[tolerance]

    def conditional_law(self,n,tolerance):
        n=_strict_integer(n,'residual count');tolerance=frac(tolerance)
        if n<0 or n>self.h:raise ValueError('Invalid residual count')
        if not 0<tolerance<F(1,4):raise ValueError('Invalid tolerance')
        if n<2 or not self.a:return None
        if not self.c:raise ValueError('Use the undisplaced matching route')
        key=(n,tolerance)
        if key in self.conditional_cached:return self.conditional_cached[key]
        a,c=self.a,self.c
        lo,hi=0,n//2
        while lo<hi:
            q=(lo+hi)//2
            if a*(n-2*q)*(n-2*q-1)<=2*c*c*(q+1):hi=q
            else:lo=q+1
        mode=lo
        def logratio(q,m):
            return ((q-m)*(_as_iv(a)/2).log()+2*(m-q)*_as_iv(c).log()
                    +arb(m+1).lgamma()+arb(n-2*m+1).lgamma()
                    -arb(q+1).lgamma()-arb(n-2*q+1).lgamma())
        law=DyadicUnimodal(n//2,mode,logratio,tolerance,_parameter_bits(n,a,c))
        self.conditional_cached[key]=law
        return law

    def sample(self,rng,tolerance):
        tolerance=frac(tolerance)
        if not 0<tolerance<F(1,4):raise ValueError('Invalid tolerance')
        if self.undisplaced is not None:return self.undisplaced.sample(rng,tolerance)
        law=self.law(tolerance)
        k=law.draw(rng) if law is not None else 0
        n=self.h-k
        qlaw=self.conditional_law(n,tolerance)
        q1=qlaw.draw(rng) if qlaw else 0
        q2=qlaw.draw(rng) if qlaw else 0
        return [[q1,k,n-2*q1],[0,q2,n-2*q2],[0,0,0]]


class DisplacedHeraldGaussian:
    """Nonnegative exact-rational Gaussian kernel with one binary-large herald."""
    def __init__(self,K,ell,herald_mode,h):
        h=_strict_integer(h,'herald count')
        herald_mode=_strict_integer(herald_mode,'herald mode')
        if h<0:raise ValueError('Negative herald count')
        self.base=RationalGaussian(K,ell,[herald_mode],[0])
        boundary=self.base.engine.boundary
        if (boundary[0][0]!=boundary[1][1] or boundary[0][1]!=boundary[1][0]
            or boundary[0][-1]!=boundary[1][-1]):
            raise AssertionError('Schur boundary exchange symmetry failed')
        self.matching=DisplacedAggregateMatching(boundary[0][0],boundary[0][1],boundary[0][-1],h)
        self.h=h

    @classmethod
    def from_pure(cls,B,g,herald_mode,h):
        K,ell=pure_kernel(B,g)
        return cls(K,ell,herald_mode,h)

    def sample(self,rng,tolerance=F(1,10**10)):
        tolerance=frac(tolerance)
        if not 0<tolerance<F(1,4):raise ValueError('Invalid tolerance')
        engine=self.base.engine
        # Three matching laws, one ghost Poisson, and all elimination scalars.
        # Adaptive composition uses this per-call budget; unused slots are safe.
        slots=engine.max_scalar_calls+4
        scalar=3*tolerance/(4*slots)
        max_attempts=128*(scalar.denominator.bit_length()+8)
        max_tickets=3*slots*max_attempts
        tickets=CappedTickets(rng,max_tickets,tolerance/4)
        self.last_ticket_fallback=False
        try:
            C=self.matching.sample(tickets,scalar)
            C[-1][-1]+=poisson(self.base.source_rate,tickets,scalar)
            aux=engine.sample(C,tickets,scalar)
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
