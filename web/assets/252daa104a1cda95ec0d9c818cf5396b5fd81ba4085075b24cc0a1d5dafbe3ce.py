#!/usr/bin/env python3
"""Exact rational audit of the direct exp(-u) matched baseline.

For each tested N,k, this constructs an odd Taylor under-approximation after
power-of-two range reduction and verifies its relative sandwich against the
adjacent even Taylor upper bound using exact Fraction arithmetic. The symbolic
proof and asymptotic bit accounting are in RESULT.txt; fixtures do not validate
the general proof or benchmark the MPO consumer.
"""

from fractions import Fraction as F


def ceil_power_two(x):
    r = 1
    while F(r) < 1 + x:
        r <<= 1
    return r


def ceil_log2_ratio(q):
    """Smallest m with 2**m >= rational q."""
    m = 0
    while F(1 << m) < q:
        m += 1
    return m


def taylor(v, degree):
    term = F(1)
    total = term
    for j in range(1, degree + 1):
        term *= -v
        term /= j
        total += term
    return total


def direct_weight(n, k, delta):
    u = F((2 * k - n) ** 2, 4 * n)
    r = ceil_power_two(u)
    v = u / r
    m = ceil_log2_ratio(F(6 * r, 1) / delta)
    if m % 2 == 0:
        m += 1
    lower = taylor(v, m)
    upper = taylor(v, m + 1)
    assert 0 < lower <= upper
    g = lower ** r
    # The exact alternating-series bracket is lower <= exp(-v) <= upper.
    # Thus g/f >= (lower/upper)^r; this rational check is stronger than the
    # theorem's requested 1-delta bound for each finite fixture.
    assert g >= (1 - delta) * (upper ** r)
    assert g <= upper ** r
    return u, r, m, g


def main():
    delta = F(1, 16)
    cases = []
    for n in (1, 2, 4, 8, 20):
        weights = [direct_weight(n, k, delta)[3] for k in range(n + 1)]
        assert all(w > 0 for w in weights)
        for k in range(n + 1):
            u, r, m, g = direct_weight(n, k, delta)
            cases.append((n, k, u, r, m, g))
    assert len(cases) == sum(n + 1 for n in (1, 2, 4, 8, 20))
    max_bits = max(max(g.numerator.bit_length(), g.denominator.bit_length())
                   for _, _, _, _, _, g in cases)
    print("direct rational relative exponential fixtures:", len(cases))
    print("N tested:", [1, 2, 4, 8, 20], "delta:", delta)
    print("maximum g numerator/denominator bits:", max_bits)
    print("all exact rational Taylor-bracket comparisons pass")


if __name__ == "__main__":
    main()
