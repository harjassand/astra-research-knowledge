"""Outward dyadic intervals for the Gaussian calculations in this experiment.

Only Python integers and Fraction enter certified arithmetic. Gaussian integrals
use an integrated Taylor polynomial and its Lagrange remainder, not an adaptive
quadrature error estimate. This small module is not a reviewed interval library.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from math import isqrt

BITS = 1024
SCALE = 1 << BITS


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


@dataclass(frozen=True)
class IV:
    lo: int
    hi: int

    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError("Invalid interval")

    @staticmethod
    def exact(x=0):
        if isinstance(x, IV):
            return x
        x = Fraction(x)
        n = x.numerator * SCALE
        d = x.denominator
        return IV(n // d, ceil_div(n, d))

    def __add__(self, other):
        other = IV.exact(other)
        return IV(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return IV(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-IV.exact(other))

    def __rsub__(self, other):
        return IV.exact(other) - self

    def __mul__(self, other):
        other = IV.exact(other)
        ps = (self.lo * other.lo, self.lo * other.hi,
              self.hi * other.lo, self.hi * other.hi)
        return IV(min(ps) // SCALE, ceil_div(max(ps), SCALE))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = IV.exact(other)
        if other.lo <= 0 <= other.hi:
            raise ArithmeticError("Division by an interval containing zero")
        qs = [(n * SCALE, d) for n in (self.lo, self.hi)
              for d in (other.lo, other.hi)]
        lows = [n // d for n, d in qs]
        highs = [ceil_div(n, d) for n, d in qs]
        return IV(min(lows), max(highs))

    def __rtruediv__(self, other):
        return IV.exact(other) / self

    def sqrt(self):
        if self.lo < 0:
            raise ArithmeticError("Square root of a negative interval")
        low = isqrt(self.lo * SCALE)
        high = isqrt(self.hi * SCALE)
        if high * high < self.hi * SCALE:
            high += 1
        return IV(low, high)

    def abs_bound(self):
        return max(abs(self.lo), abs(self.hi))

    def clip_probability(self):
        if self.hi < 0 or self.lo > SCALE:
            raise ArithmeticError("Probability interval misses [0,1]")
        return IV(max(0, self.lo), min(SCALE, self.hi))

    def width(self):
        return Fraction(self.hi - self.lo, SCALE)

    def midpoint(self):
        return Fraction(self.lo + self.hi, 2 * SCALE)

    def contains(self, x):
        x = Fraction(x)
        return self.lo * x.denominator <= x.numerator * SCALE <= self.hi * x.denominator

    def decimal_bounds(self, digits=45):
        # Integer-directed conversion avoids rounding a near-one probability
        # to one before printing the lower decimal endpoint.
        decimal_scale = 10**digits
        low = self.lo * decimal_scale // SCALE
        high = ceil_div(self.hi * decimal_scale, SCALE)

        def render(n):
            sign = "-" if n < 0 else ""
            t = str(abs(n)).zfill(digits + 1)
            return sign + (t if not digits else t[:-digits] + "." + t[-digits:])

        return [render(low), render(high)]


@lru_cache(maxsize=None)
def arctan_recip(q: int) -> IV:
    """Alternating arctan series, plus the next-term remainder enclosure."""
    q2 = q * q
    power = q
    total = IV.exact(0)
    n = 0
    sign = 1
    while True:
        term = IV.exact(Fraction(1, power * (2 * n + 1)))
        total = total + sign * term
        n += 1
        power *= q2
        next_term = IV.exact(Fraction(1, power * (2 * n + 1)))
        if next_term.hi <= 1:
            # The ordinary alternating-series remainder has this magnitude.
            return total + IV(-next_term.hi, next_term.hi)
        sign = -sign


@lru_cache(maxsize=None)
def pi_interval() -> IV:
    # Machin's identity is exact.
    return 16 * arctan_recip(5) - 4 * arctan_recip(239)


@lru_cache(maxsize=None)
def normal_constant() -> IV:
    return 1 / (2 * pi_interval()).sqrt()


@lru_cache(maxsize=None)
def exp_neg(z: Fraction) -> IV:
    """Enclose exp(-z), z>=0, by Taylor and repeated squaring."""
    z = Fraction(z)
    if z < 0:
        raise ValueError("exp_neg needs z >= 0")
    if not z:
        return IV.exact(1)
    squares = 0
    while z > 1:
        z /= 2
        squares += 1
    term = IV.exact(1)
    total = term
    n = 0
    while True:
        n += 1
        term = term * z / n
        total = total + (-term if n % 2 else term)
        nxt = term * z / (n + 1)
        if nxt.hi <= 2:
            # Taylor's Lagrange remainder: exp(-xi)<=1 on [0,z].
            total = total + IV(-nxt.hi, nxt.hi)
            break
    for _ in range(squares):
        total = total * total
    return total


@lru_cache(maxsize=150000)
def normal_pdf(x: Fraction) -> IV:
    x = Fraction(x)
    return normal_constant() * exp_neg(x * x / 2)


@lru_cache(maxsize=150000)
def normal_cdf(x: Fraction) -> IV:
    """Certified integral over [0,x] of the Gaussian density.

    integral(exp(-t^2/2),0,z)=sum_n(-1)^n z^(2n+1)/(2^n n!(2n+1)).
    Taylor's Lagrange formula under the integral bounds the remainder by
    z^(2N+3)/(2^(N+1)(N+1)!(2N+3)), for every z>=0, even before
    the terms become decreasing. No float participates in this enclosure.
    """
    x = Fraction(x)
    if x < 0:
        return (1 - normal_cdf(-x)).clip_probability()
    if not x:
        return IV.exact(Fraction(1, 2))
    z2 = x * x / 2
    # base_n=x^(2n+1)/(2^n n!), divided by 2n+1 below.
    base = IV.exact(x)
    total = base
    n = 0
    while True:
        n += 1
        base = base * z2 / n
        term = base / (2 * n + 1)
        total = total + (-term if n % 2 else term)
        nxt_base = base * z2 / (n + 1)
        nxt = nxt_base / (2 * n + 3)
        if nxt.hi <= 2 and n > z2:
            total = total + IV(-nxt.hi, nxt.hi)
            break
        if n > 20000:
            raise ArithmeticError("CDF Taylor series exceeded bounded-job guard")
    return (Fraction(1, 2) + normal_constant() * total).clip_probability()


def normal_mass(left: Fraction | None, right: Fraction | None, mean=Fraction(0)) -> IV:
    mean = Fraction(mean)
    fl = IV.exact(0) if left is None else normal_cdf(Fraction(left) - mean)
    fr = IV.exact(1) if right is None else normal_cdf(Fraction(right) - mean)
    return (fr - fl).clip_probability()


@lru_cache(maxsize=None)
def atanh_series(z: Fraction) -> IV:
    z = Fraction(z)
    if not 0 <= z <= Fraction(1, 3):
        raise ValueError("atanh series argument outside [0,1/3]")
    zi = IV.exact(z)
    z2 = zi * zi
    power = zi
    total = IV.exact(0)
    n = 0
    while True:
        total = total + 2 * power / (2 * n + 1)
        n += 1
        power = power * z2
        # All omitted positive terms are bounded by this geometric remainder.
        rem = 2 * power / (2 * n + 1) / (1 - z2)
        if rem.hi <= 4:
            return total + IV(0, rem.hi)


@lru_cache(maxsize=150000)
def log_point(n: int) -> IV:
    """Certified ln(n/2^BITS), n>0, using binary scaling and atanh."""
    if n <= 0:
        raise ArithmeticError("log requires positive endpoint")
    k = n.bit_length() - BITS - 1
    # u=(n/SCALE)/2^k lies in [1,2).
    u = Fraction(n, SCALE << k) if k >= 0 else Fraction(n << (-k), SCALE)
    z = (u - 1) / (u + 1)
    return atanh_series(z) + k * atanh_series(Fraction(1, 3))


def log_interval(x: IV) -> IV:
    if x.lo <= 0:
        raise ArithmeticError("Increase precision: positive probability has zero lower bound")
    return IV(log_point(x.lo).lo, log_point(x.hi).hi)


def sqrt_log_upper_endpoint(a: Fraction, h: Fraction, fractional_bits=50) -> Fraction:
    """Dyadic upper bound on a+sqrt(2 ln(8/h^2)); comparisons remain rational."""
    bound = IV.exact(a) + (2 * log_interval(IV.exact(8 / (h * h)))).sqrt()
    den = 1 << fractional_bits
    return Fraction(ceil_div(bound.hi * den, SCALE), den)


def interval_json(x: IV):
    return {"decimal_interval": x.decimal_bounds(),
            "dyadic_integer_low": str(x.lo),
            "dyadic_integer_high": str(x.hi),
            "dyadic_denominator_power": BITS}
