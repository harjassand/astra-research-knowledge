#!/usr/bin/env python3
"""Exact rational intervals for the geometric-affinity ring witness.

The three-state ring has clockwise rate 1, counterclockwise rate q=1/20,
uniform stationary distribution, and visible set B={1,2}.  At t=3/10,
the formulas for a and D below follow from diagonalizing the circulant
generator.  All asserted bounds use Fraction; Decimal is display only.
"""

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as F
from math import factorial, isqrt


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F

    def __post_init__(self):
        assert self.lo <= self.hi

    @staticmethod
    def of(x):
        return x if isinstance(x, Interval) else Interval(F(x), F(x))

    def __add__(self, other):
        other = Interval.of(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-Interval.of(other))

    def __rsub__(self, other):
        return Interval.of(other) - self

    def __mul__(self, other):
        other = Interval.of(other)
        p = [a * b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return Interval(min(p), max(p))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Interval.of(other)
        assert other.lo > 0
        return self * Interval(1 / other.hi, 1 / other.lo)


def alt_series(x, coefficient, odd_terms=19, even_terms=20):
    """Bounds from successive alternating partial sums for x in [0,1)."""
    assert 0 <= x.lo <= x.hi < 1

    def partial(z, last):
        return sum((F((-1) ** k) * coefficient(z, k)
                    for k in range(last + 1)), F(0))

    # For exp(-x) and cos(x), the function decreases on this interval.
    # For sin(x), it increases.  The caller selects endpoints below.
    return partial, odd_terms, even_terms


def exp_minus(x):
    x = Interval.of(x)
    partial, odd, even = alt_series(x, lambda z, k: z ** k / factorial(k))
    return Interval(partial(x.hi, odd), partial(x.lo, even))


def sin_pos(x):
    x = Interval.of(x)
    partial, odd, even = alt_series(
        x, lambda z, k: z ** (2 * k + 1) / factorial(2 * k + 1)
    )
    return Interval(partial(x.lo, odd), partial(x.hi, even))


def cos_pos(x):
    x = Interval.of(x)
    partial, odd, even = alt_series(
        x, lambda z, k: z ** (2 * k) / factorial(2 * k)
    )
    return Interval(partial(x.hi, odd), partial(x.lo, even))


def rational_sqrt_interval(n, digits=35):
    base = 10 ** digits
    low_int = isqrt(n * base * base)
    out = Interval(F(low_int, base), F(low_int + 1, base))
    assert out.lo ** 2 < n < out.hi ** 2
    return out


def as_decimal(x):
    return Decimal(x.numerator) / Decimal(x.denominator)


q = F(1, 20)
t = F(3, 10)
s = 1 + q
theta = F(57, 400) * rational_sqrt_interval(3)
assert theta.hi < F(1, 4)
e_half = exp_minus(3 * s * t / 2)
e_full = exp_minus(3 * s * t)

# Circulant ring propagator: P_{AA}(t) = (1+2e_half*cos(theta))/3.
# Given X_0 in B uniformly, a=P(X_t in B | X_0 in B).
a = F(2, 3) + e_half * cos_pos(theta) / 3

# The past and future B probabilities are swapped across the two B states.
# Their conditional deviations from a are opposite; hence
# E[1_B(X_0)(1_B(X_-t)-a)(1_B(X_t)-a)] = -D.
# D=(2/9)e^{-3st}sin^2(theta), with theta=sqrt(3)(1-q)t/2.
sin_theta = sin_pos(theta)
D = F(2, 9) * e_full * (sin_theta * sin_theta)
assert F(86, 100) < a.lo < a.hi < F(87, 100)
assert D.lo > F(5155, 1_000_000)

# a>1/2, so a(1-a) decreases as a rises.
C = Interval(a.hi * (1 - a.hi), a.lo * (1 - a.lo))
z = D / C
assert z.hi < F(1, 10)

# -log(1-z)=sum_{k>=1} z^k/k.  Positive partial sum bounds below;
# tail <= z^(N+1)/[(N+1)(1-z)] bounds above.
N = 15
log_lower = sum((z.lo ** k / k for k in range(1, N + 1)), F(0))
log_upper = (sum((z.hi ** k / k for k in range(1, N + 1)), F(0))
             + z.hi ** (N + 1) / ((N + 1) * (1 - z.hi)))
sigma_floor = Interval(log_lower / t, log_upper / t)
assert sigma_floor.lo > F(1536, 10000)
assert sigma_floor.hi < F(154, 1000)

getcontext().prec = 40
for name, value in [("a", a), ("D", D), ("z=D/[a(1-a)]", z),
                    ("sigma floor", sigma_floor)]:
    print(name, "in (", as_decimal(value.lo), ",", as_decimal(value.hi), ")")
print("rigorous bound for every compatible finite stationary Q: sigma > 0.1536")
