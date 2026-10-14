#!/usr/bin/env python3
"""Exact rational interval certificate for q=1/20 at h=1/5.

No floating-point arithmetic is used in any assertion.  Decimal printing at
the end is display only.  The exponential interval uses the alternating
Taylor series for exp(-x), valid here because 0 <= x < 1.
"""

from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction as F
from math import factorial


@dataclass(frozen=True)
class I:
    lo: F
    hi: F

    def __post_init__(self):
        assert self.lo <= self.hi

    @staticmethod
    def of(x):
        return x if isinstance(x, I) else I(F(x), F(x))

    def __add__(self, other):
        other = I.of(other)
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-I.of(other))

    def __rsub__(self, other):
        return I.of(other) - self

    def __mul__(self, other):
        other = I.of(other)
        products = [a * b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return I(min(products), max(products))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = I.of(other)
        assert 0 < other.lo
        return self * I(F(1) / other.hi, F(1) / other.lo)

    def __pow__(self, power):
        assert isinstance(power, int) and power >= 0
        result = I.of(1)
        for _ in range(power):
            result *= self
        return result


def alternating_sum(x: F, order: int) -> F:
    return sum(((-x) ** k / factorial(k) for k in range(order + 1)), F(0))


def exp_minus(x: I) -> I:
    assert 0 <= x.lo <= x.hi < 1
    # Odd truncation is below exp(-x), even truncation above it.
    return I(alternating_sum(x.hi, 19), alternating_sum(x.lo, 18))


q = F(1, 20)
sqrt_q_lo = F(22360679774997896964, 10**20)
sqrt_q_hi = F(22360679774997896965, 10**20)
assert sqrt_q_lo**2 < q < sqrt_q_hi**2
sqrt_q = I(sqrt_q_lo, sqrt_q_hi)

s = F(1) + q
b = 2 * q / s
c = F(1) + q + q**2
mean_b = (2 * s - b) / c  # minus derivative at zero of the Laplace transform
assert mean_b == 2 / s
ell = s - sqrt_q
high = s + sqrt_q
denom = high - ell
a_pos = (c - b * ell) / denom
a_neg = (b * high - c) / denom
assert a_pos.lo > 0 and a_neg.hi < 0
assert a_pos.lo + a_neg.lo <= b <= a_pos.hi + a_neg.hi

entry_rate = s / 3
f_prime_zero = c - b * 2 * s
assert f_prime_zero == F(341, 400)
stationary_third_derivative = entry_rate * f_prime_zero
assert entry_rate == F(7, 20)
assert stationary_third_derivative == F(2387, 8000)
stationary_b_mass = entry_rate * mean_b
assert stationary_b_mass == F(2, 3)
stationary_no_exit_at_zero = entry_rate * (
    a_pos / (ell**2) + a_neg / (high**2)
)
assert stationary_no_exit_at_zero.lo < stationary_b_mass < stationary_no_exit_at_zero.hi

h = F(1, 5)
e_ell = exp_minus(ell * h)
e_high = exp_minus(high * h)
delta_three = entry_rate * (
    (a_pos / (ell**2)) * ((e_ell - 1) ** 3)
    + (a_neg / (high**2)) * ((e_high - 1) ** 3)
)
assert delta_three.lo > F(1, 1000)
assert delta_three.hi < F(12, 10000)

# For a width-three witness on [0,3h], Pinsker and the KL/EP comparison
# give sigma >= 8*d^2/(27*h).  The strict d lower bound gives:
sigma_lower = 8 * F(1, 1000) ** 2 / (27 * h)
assert sigma_lower == F(1, 675000)

getcontext().prec = 30
as_decimal = lambda x: Decimal(x.numerator) / Decimal(x.denominator)
print("sqrt(q) interval:", as_decimal(sqrt_q.lo), as_decimal(sqrt_q.hi))
print("f_B'(0):", f_prime_zero)
print("A_B'''(0):", stationary_third_derivative)
print("stationary B mass:", stationary_b_mass)
print("Delta^3 A_B(0), h=1/5 interval:", as_decimal(delta_three.lo), as_decimal(delta_three.hi))
print("rigorous all-dimension EP lower bound: sigma > 1/675000")
