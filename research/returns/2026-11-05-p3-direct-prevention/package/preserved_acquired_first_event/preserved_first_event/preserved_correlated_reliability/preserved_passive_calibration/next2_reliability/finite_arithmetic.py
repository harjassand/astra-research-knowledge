"""Finite rational operations for the whole-CDF theorem.

Implemented: outward tail queries, exact finite Poisson tables, finite grids.
Not implemented here: generic Karger counting or the huge worst-case
Monte Carlo preprocessing budget. See PROOF.md for its completed algorithm.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from math import factorial, isqrt
from bisect import bisect_left
from random import Random
from typing import Sequence

F = Fraction


def ceil_fraction(x: F) -> int:
    return -((-x.numerator) // x.denominator)


def ceil_log2(x: F) -> int:
    if x <= 0:
        raise ValueError("positive input required")
    k = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    while (1 << k) * x.denominator < x.numerator:
        k += 1
    while k and (1 << (k - 1)) * x.denominator >= x.numerator:
        k -= 1
    return k


def dyadic_sqrt_upper(x: F, bits: int = 48) -> F:
    if x < 0:
        raise ValueError("nonnegative input required")
    numerator = x.numerator << (2 * bits)
    root = isqrt(numerator // x.denominator)
    if root * root * x.denominator < numerator:
        root += 1
    return F(root, 1 << bits)


@dataclass(frozen=True)
class Interval:
    lower: F
    upper: F

    def __post_init__(self):
        if not 0 <= self.lower <= self.upper <= 1:
            raise ValueError("invalid probability interval")

    @property
    def ratio(self):
        return self.upper / self.lower if self.lower else None


def failure_exp_interval(x: F, xi: F) -> Interval:
    """Outward rational interval for 1-exp(-x), relative errors <=xi/64."""
    if x < 0 or not 0 < xi <= F(1, 40):
        raise ValueError("x>=0 and 0<xi<=1/40 required")
    if not x:
        return Interval(F(0), F(0))
    limit = ceil_log2(F(64) / xi)
    if x >= limit:
        return Interval(1 - xi / 64, F(1))
    scale = 1 << ceil_log2(2 * x)
    y = x / scale
    degree = ceil_log2(F(128 * limit) / xi)
    degree += degree % 2
    term = F(1)
    upper_exp = F(1)
    for k in range(1, degree + 1):
        term *= -y / k
        upper_exp += term
    lower_exp = upper_exp + term * (-y) / (degree + 1)
    if not 0 <= lower_exp <= upper_exp <= 1:
        raise AssertionError("alternating Taylor bracket failed")
    return Interval(1 - upper_exp**scale, 1 - lower_exp**scale)


def failure_power_interval(lam: F, n: int, xi: F,
                           lambda_floor: F | None = None) -> Interval:
    """Outward rational interval for 1-(1-lam)**n, using O(log n) products."""
    if not 0 < lam <= 1 or n < 1 or not 0 < xi <= F(1, 40):
        raise ValueError("invalid discrete query")
    floor = lam if lambda_floor is None else lambda_floor
    if not 0 < floor <= lam:
        raise ValueError("positive lower floor required")
    bits = ceil_log2(F(16 * n) / (xi * floor))
    unit = 1 << bits
    q = 1 - lam
    low = (q.numerator * unit) // q.denominator
    high = ceil_fraction(q * unit)
    acc_low = acc_high = None
    exponent = n
    while exponent:
        if exponent & 1:
            if acc_low is None:
                acc_low, acc_high = low, high
            else:
                acc_low = (acc_low * low) // unit
                acc_high = min(unit, (acc_high * high + unit - 1) // unit)
        exponent >>= 1
        if exponent:
            low = (low * low) // unit
            high = min(unit, (high * high + unit - 1) // unit)
    return Interval(F(unit - acc_high, unit), F(unit - acc_low, unit))


def geometric_grid(xi: F, horizon: F) -> list[F]:
    if not 0 < xi <= horizon:
        raise ValueError("invalid grid")
    mesh = xi * xi / 4
    result = [xi]
    while result[-1] < horizon:
        candidate = mesh * ceil_fraction((1 + xi) * result[-1] / mesh)
        result.append(min(horizon, candidate))
    return result


class IntegerDistribution:
    """Exact finite categorical draw; a declared cap can turn timeout into abort."""
    def __init__(self, weights: Sequence[int]):
        if not weights or min(weights) < 0 or sum(weights) <= 0:
            raise ValueError("nonnegative nonzero weights required")
        self.weights = tuple(weights)
        total = 0
        cumulative = []
        for w in weights:
            total += w
            cumulative.append(total)
        self.total = total
        self.cumulative = tuple(cumulative)
        self.bits = max(1, (total - 1).bit_length())

    def draw(self, rng: Random, cap: int | None = None) -> int:
        attempts = 0
        while cap is None or attempts < cap:
            attempts += 1
            value = rng.getrandbits(self.bits)
            if value < self.total:
                return bisect_left(self.cumulative, value + 1)
        raise RuntimeError("declared categorical rejection cap exceeded")


def poisson_table(u: F, tolerance: F) -> IntegerDistribution:
    """Exact Poisson(u) conditional on 0..K, with total-variation error <=tol."""
    if u < 0 or not 0 < tolerance < 1:
        raise ValueError("invalid Poisson parameters")
    cutoff = ceil_fraction(2 * u) + ceil_log2(1 / tolerance)
    if not u:
        return IntegerDistribution([1] + [0] * cutoff)
    A, B = u.numerator, u.denominator
    weight = pow(B, cutoff) * factorial(cutoff)
    weights = [weight]
    for k in range(cutoff):
        weight, remainder = divmod(weight * A, B * (k + 1))
        if remainder:
            raise AssertionError("Poisson integer recurrence lost integrality")
        weights.append(weight)
    return IntegerDistribution(weights)


@dataclass
class ContinuousCertificate:
    """Deterministic query interface for the proved finite acquired intervals."""
    xi: F
    rate_R: F
    p_interval: Interval
    c_interval: Interval
    nodes: list[F]
    node_intervals: list[Interval]
    lambda_interval: tuple[F, F] | None

    def query(self, time: F) -> Interval:
        if time < 0:
            raise ValueError("deadline must be nonnegative")
        u = time * self.rate_R
        if not u:
            return Interval(F(0), F(0))
        pL, pU = self.p_interval.lower, self.p_interval.upper
        cL, cU = self.c_interval.lower, self.c_interval.upper
        aL, aU = 1 - pU, 1 - pL
        if u <= self.xi:
            return Interval((1 - self.xi / 2) * pL * cL * u / aU,
                            min(F(1), pU * cU * u / aL))
        if u <= self.nodes[-1]:
            i = bisect_left(self.nodes, u)
            if self.nodes[i] == u:
                return self.node_intervals[i]
            return Interval(self.node_intervals[i - 1].lower,
                            self.node_intervals[i].upper)
        if self.lambda_interval is None:
            return Interval(1 - self.xi, F(1))
        lo, hi = self.lambda_interval
        lower = failure_exp_interval(lo * u, self.xi).lower
        upper = min(F(1), (1 + self.xi) *
                    failure_exp_interval(hi * u, self.xi).upper)
        return Interval(lower, upper)
