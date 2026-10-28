"""An ordinary rational Bernstein-envelope factory, specialized to N1073's K.

One persistent classical X and an iid cheap proxy stream are REQUIRED. For
Pr(Z=0) <= 1/4 it outputs K's columns 1/2; for Pr(Z=0) >= 7/12 it outputs
column 0. There is no raw callback. The function in the gap is an explicit
smooth interpolation. Expected cheap calls are 44351/32. This is not a claim
that naive exact coefficient arithmetic has finite expected bit complexity.

The general construction is prior art: Nacu-Peres / Holtz-Nazarov-Peres.
The concrete constants and specialization are derived in PROOF_EXTENSION.md.
"""
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt

from operation import exact_choice

START = 1024
RADIUS_CONSTANT = F(3861, 4)


def comb(n, k):
    """Explicit polynomial-work exact binomial recurrence for cost accounting."""
    if k < 0 or k > n:
        return 0
    k = min(k, n-k)
    value = 1
    for j in range(1, k+1):
        value = value * (n-k+j) // j
    return value


def smooth_probability(p):
    p = F(p)
    if p <= F(1, 4):
        return F(49, 120)
    if p >= F(7, 12):
        return F(2, 15)
    t = 3 * p - F(3, 4)
    return F(49, 120) - F(11, 40) * (10 * t**3 - 15 * t**4 + 6 * t**5)


def second_derivative(p):
    p = F(p)
    if p <= F(1, 4) or p >= F(7, 12):
        return F(0)
    t = 3 * p - F(3, 4)
    return -F(99, 40) * (60 * t - 180 * t**2 + 120 * t**3)


def center(n, k):
    p = F(k, n)
    return smooth_probability(p) - p * (1 - p) * second_derivative(p) / (2 * n)


def radius(n):
    root = isqrt(n)
    if root * root != n:
        raise ValueError("degree must be a square")
    return RADIUS_CONSTANT / (n * root)


def coefficient_envelope(n, k):
    h, e = center(n, k), radius(n)
    return h - e, h + e


@lru_cache(maxsize=2)
def integer_centers(n):
    # A common denominator for the piecewise quintic and its correction.
    scale = 122880 * n**6
    values = []
    for k in range(n + 1):
        scaled = center(n, k) * scale
        if scaled.denominator != 1:
            raise AssertionError("declared common denominator failed")
        values.append(scaled.numerator)
    return scale, values


def elevated_center(n, m, k):
    """Exact hypergeometric coefficient elevation n -> m; O(n) big-int terms.

    There is deliberately no precision/runtime truncation hidden in this call.
    Integers may have Theta(m) bits; finite expected proxy calls alone does not
    certify finite expected total bit work for this naive implementation.
    """
    scale, values = integer_centers(n)
    lower, upper = max(0, k - (m - n)), min(n, k)
    weight = comb(n, lower) * comb(m - n, k - lower)
    weighted, mass = 0, 0
    for j in range(lower, upper + 1):
        weighted += values[j] * weight
        mass += weight
        if j != upper:
            numerator = weight * (n - j) * (k - j)
            denominator = (j + 1) * (m - n - k + j + 1)
            weight, remainder = divmod(numerator, denominator)
            if remainder:
                raise AssertionError("hypergeometric recurrence not integral")
    normalization = comb(m, k)
    if mass != normalization:
        raise AssertionError("Vandermonde normalization failed")
    return F(weighted, scale * normalization)


def refinement_weights(n, m, total_heads):
    if m != 4 * n:
        raise ValueError("this factory refines by a factor of four")
    old_center = elevated_center(n, m, total_heads)
    new_center = center(m, total_heads)
    old_radius, new_radius = radius(n), radius(m)
    difference = new_center - old_center
    weights = [(difference + old_radius - new_radius) / (2 * old_radius),
               (-difference + old_radius - new_radius) / (2 * old_radius),
               new_radius / old_radius]
    if any(v < 0 for v in weights) or sum(weights) != 1:
        raise AssertionError("envelope compatibility failed")
    if weights[2] != F(1, 8):
        raise AssertionError("unexpected continuation law")
    return weights  # head, tail, continue


def factory_coin(coin_callback, rng=None, *, choose=None, trace=None):
    """Exact f(p)-coin in the ideal iid/unbiased-bit contract; no hard budget.

    `choose` is a deterministic path-testing hook. Normal callers leave it None.
    This function has unbounded worst-case memory/time and naive exact arithmetic.
    """
    if choose is None:
        choose = lambda weights: exact_choice(weights, rng)
    n = START
    total_heads = sum(bool(coin_callback()) for _ in range(n))
    lower, upper = coefficient_envelope(n, total_heads)
    weights = [lower, 1 - upper, upper - lower]
    while True:
        decision = choose(weights)
        if trace is not None:
            trace.append({"degree": n, "heads": total_heads,
                          "decision": decision, "weights": weights})
        if decision in (0, 1):
            return decision == 0
        if decision != 2:
            raise ValueError("invalid testing-hook decision")
        previous = n
        n *= 4
        total_heads += sum(bool(coin_callback()) for _ in range(n - previous))
        weights = refinement_weights(previous, n, total_heads)


def factory_output(proxy_callback, rng=None, *, choose=None, trace=None):
    """Exact source K on the separated p plateaux; internal records stay private."""
    def coin():
        z = proxy_callback()
        if z not in (0, 1, 2):
            raise ValueError("proxy record outside source alphabet")
        return z == 0
    if factory_coin(coin, rng, choose=choose, trace=trace):
        return 0
    return 1 + exact_choice([F(1, 2), F(1, 2)], rng)
