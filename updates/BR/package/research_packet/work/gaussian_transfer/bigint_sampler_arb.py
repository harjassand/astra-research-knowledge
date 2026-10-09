"""Integer-valued samplers with finite-support dyadic rejection envelopes.

The graph algorithm can generate occupations much larger than 64-bit integers.
This module does not simulate individual successes or failures. It uses
unimodality, O(log support) rectangles, interval log-gamma evaluations, and
integer random choices. FLINT/Arb supplies rigorous numerical enclosures;
the library and wrapper remain ordinary software, not formally kernel-verified.

For each scalar call, truncation + downward dyadic rounding + an attempt cap
have an explicit total-variation budget `tolerance`, conditional on valid
interval enclosures and independent unbiased random bits.
"""
from __future__ import annotations
from fractions import Fraction
from functools import lru_cache
from bisect import bisect_right
import math
import random
from flint import arb, ctx


def frac(x):
    """Convert exact values only: use strings or Fraction, never floats."""
    if isinstance(x, float):
        raise TypeError('Use a string or Fraction, not a binary floating input')
    return Fraction(x)


def _ceil(q: Fraction) -> int:
    return -(-q.numerator // q.denominator)


def _floor_scaled_arb(endpoint, bits):
    man, exponent = endpoint.man_exp()
    man, exponent = int(man), int(exponent)
    if man <= 0: return 0
    shift = exponent + bits
    if shift >= 0: return man << shift
    return 0 if -shift >= man.bit_length() else man >> (-shift)

def _ceil_scaled_arb(endpoint, bits):
    man, exponent = endpoint.man_exp()
    man, exponent = int(man), int(exponent)
    if man < 0: raise ArithmeticError('Negative probability upper bound')
    if man == 0: return 0
    shift = exponent + bits
    if shift >= 0: return man << shift
    shift = -shift
    if shift >= man.bit_length(): return 1
    return (man+(1<<shift)-1)>>shift

def _as_iv(q):
    q=Fraction(q)
    return arb(q.numerator)/arb(q.denominator)



class DyadicUnimodal:
    """Finite unimodal integer law supplied by interval log mass ratios."""
    def __init__(self, maximum: int, mode: int, logratio, tolerance: Fraction,
                 input_bits: int = 0):
        self.maximum, self.mode = int(maximum), int(mode)
        self.tolerance = frac(tolerance)
        if not 0 < self.tolerance < Fraction(1, 4):
            raise ValueError('Tolerance must lie in (0, 1/4)')
        if not 0 <= self.mode <= self.maximum:
            raise ValueError('Mode lies outside the support')
        # 2*(M+1)*2^-bits <= tolerance/16, conservatively.
        precision_factor = _ceil(Fraction(64) / self.tolerance)
        self.bits = (self.maximum + 1).bit_length() + precision_factor.bit_length()
        self.scale = 1 << self.bits
        self.working_precision = max(100, 2*int(input_bits) + self.bits + 64)
        self.logratio = logratio
        self.interval_refinements = 0
        self.max_precision_used = 0
        self.num_bounds = 0
        self.num_draws = 0
        self.total_attempts = 0
        self.fallback_count = 0

        @lru_cache(maxsize=None)
        def bounds(k: int):
            if k == self.mode:
                return self.scale, self.scale
            # Evaluate at increasing precision until a two-grid-unit enclosure
            # is achieved. An explicit failure is preferable to silently
            # claiming an error guarantee if interval evaluation is unreliable.
            old = ctx.prec
            try:
                factor = 1
                while True:
                    ctx.prec = self.working_precision * factor
                    self.max_precision_used = max(self.max_precision_used, ctx.prec)
                    self.num_bounds += 1
                    value = self.logratio(k, self.mode).exp()
                    lo = max(0, _floor_scaled_arb(value.lower(), self.bits))
                    hi = min(self.scale, _ceil_scaled_arb(value.upper(), self.bits))
                    if lo <= hi and hi-lo <= 2:
                        self.interval_refinements += factor > 1
                        return lo, hi
                    factor *= 2
            finally:
                ctx.prec = old
        self.bounds = bounds
        # Every dyadic block is dominated by the mass at its nearest-to-mode
        # endpoint. Two-sided monotonicity gives envelope mass <= 3*true mass,
        # before the explicitly budgeted dyadic upward rounding.
        blocks = [(self.mode, self.mode, self.mode)]
        distance = 1
        while distance <= max(self.mode, self.maximum-self.mode):
            if distance <= self.mode:
                low = max(0, self.mode-(2*distance-1))
                high = self.mode-distance
                blocks.append((low, high, high))
            if self.mode+distance <= self.maximum:
                low = self.mode+distance
                high = min(self.maximum, self.mode+2*distance-1)
                blocks.append((low, high, low))
            distance *= 2
        self.blocks = []
        self.cumulative = []
        total = 0
        for low, high, peak in blocks:
            _, height = self.bounds(peak)
            total += (high-low+1)*height
            self.blocks.append((low, high, height))
            self.cumulative.append(total)
        self.total = total
        # Success probability >1/5 by the envelope and rounding bounds.
        # log(1/tolerance) obtained from integer bit lengths without underflow.
        self.max_attempts = 4*(self.tolerance.denominator.bit_length()+4)
        # (4/5)^4 < 1/2, so cap-failure <= tolerance/16.
        # This integer bound avoids relying on floating logarithms.
        self.last_attempts = 0
        self.used_fallback = False

    def draw(self, rng: random.Random) -> int:
        self.num_draws += 1
        for attempts in range(1, self.max_attempts+1):
            ticket = rng.randrange(self.total)
            j = bisect_right(self.cumulative, ticket)
            low, high, height = self.blocks[j]
            point = rng.randrange(low, high+1)
            accepted_height, _ = self.bounds(point)
            if accepted_height > height:
                raise ArithmeticError('Unimodality/envelope consistency failed')
            if rng.randrange(height) < accepted_height:
                self.last_attempts = attempts
                self.total_attempts += attempts
                return point
        self.last_attempts = self.max_attempts
        self.used_fallback = True
        self.fallback_count += 1
        self.total_attempts += self.max_attempts
        return self.mode


def _parameter_bits(*values):
    ans = 1
    for value in values:
        q=Fraction(value)
        ans=max(ans, abs(q.numerator).bit_length(), q.denominator.bit_length())
    return ans


def binomial(n: int, p, rng: random.Random, tolerance=Fraction(1, 10**12)) -> int:
    n=int(n); p=frac(p); tolerance=frac(tolerance)
    if n<0 or not 0 <= p <= 1:
        raise ValueError('Invalid binomial parameters')
    if n == 0 or p == 0: return 0
    if p == 1: return n
    mode=((n+1)*p.numerator)//p.denominator
    mode=min(n,mode)
    def logratio(k,m):
        # Normalization cancels: no factorial with O(n) digits is constructed.
        pp=_as_iv(p); qq=_as_iv(1-p)
        return (arb(m+1).lgamma()+arb(n-m+1).lgamma()
                -arb(k+1).lgamma()-arb(n-k+1).lgamma()
                +(k-m)*(pp.log()-qq.log()))
    law=DyadicUnimodal(n,mode,logratio,tolerance,
                       _parameter_bits(n,p))
    return law.draw(rng)


def negative_binomial(shape, p, rng: random.Random,
                      tolerance=Fraction(1,10**12)) -> int:
    shape=frac(shape); p=frac(p); tolerance=frac(tolerance)
    if shape<=0 or not 0<p<=1:
        raise ValueError('Invalid negative-binomial parameters')
    if p==1: return 0
    mean=shape*(1-p)/p
    maximum=_ceil(4*mean/tolerance)  # Markov upper-tail budget tolerance/4.
    mode=max(0, ((shape-1)*(1-p)/p).numerator // ((shape-1)*(1-p)/p).denominator)
    def logratio(k,m):
        rr=_as_iv(shape); qq=_as_iv(1-p)
        return ((k+rr).lgamma()-arb(k+1).lgamma()
                -(m+rr).lgamma()+arb(m+1).lgamma()
                +(k-m)*qq.log())
    law=DyadicUnimodal(maximum,mode,logratio,tolerance,
                       _parameter_bits(maximum,shape,p))
    return law.draw(rng)


def rational_choice(weights, rng: random.Random) -> int:
    weights=[Fraction(w) for w in weights]
    if not weights or any(w<0 for w in weights) or not any(weights):
        raise ValueError('Choice needs nonnegative weights with positive sum')
    denom=1
    for w in weights: denom=math.lcm(denom,w.denominator)
    iw=[w.numerator*(denom//w.denominator) for w in weights]
    ticket=rng.randrange(sum(iw))
    for j,w in enumerate(iw):
        if ticket<w: return j
        ticket-=w
    raise AssertionError('Invalid random choice')


def poisson(rate, rng: random.Random, tolerance=Fraction(1,10**12)) -> int:
    rate=frac(rate); tolerance=frac(tolerance)
    if rate<0: raise ValueError('Poisson rate must be nonnegative')
    if rate==0: return 0
    maximum=_ceil(4*rate/tolerance)
    mode=rate.numerator//rate.denominator
    def logratio(k,m):
        return (arb(m+1).lgamma()-arb(k+1).lgamma()
                +(k-m)*_as_iv(rate).log())
    law=DyadicUnimodal(maximum,mode,logratio,tolerance,
                       _parameter_bits(maximum,rate))
    return law.draw(rng)
