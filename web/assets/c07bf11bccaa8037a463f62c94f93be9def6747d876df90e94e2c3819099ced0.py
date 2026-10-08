"""Exact small-instance diagnostics for the reversible escape witness.

These checks exercise the displayed formulas for finite n and d. The general
claim is proved algebraically in CANDIDATE_PROOF.md; this script is not a proof
of novelty, recurrence for a general CRN, or a large-volume result.
"""
from fractions import Fraction as F
from math import factorial


# Internal complexes after Q is clamped at unit activity; every reaction has
# effective directional constant one.
PAIRS = (
    ((0, 0, 2, 0), (1, 1, 1, 0)),
    ((1, 1, 1, 0), (3, 2, 0, 0)),
    ((3, 2, 0, 0), (0, 0, 2, 0)),
    ((0, 0, 2, 0), (0, 0, 2, 1)),
)


def falling_factorial(x, k):
    out = 1
    for j in range(k):
        out *= x - j
    return out


def propensity(x, complex_):
    out = 1
    for count, requirement in zip(x, complex_):
        out *= falling_factorial(count, requirement)
    return out


def phase_weights(n):
    raw = (
        F(1, 2),
        F(1, n + 1),
        F(1, 2 * (n + 1) * (n + 2) * (n + 3)),
    )
    z = sum(raw)
    return tuple(w / z for w in raw), z


def check(n):
    p, z = phase_weights(n)
    p0, p1, p2 = p
    expected = F(1, 1) / z
    directed_stationary_rates = (
        2 * p0, (n + 1) * p1,
        (n + 1) * p1,
        2 * (n + 1) * (n + 2) * (n + 3) * p2,
        2 * (n + 1) * (n + 2) * (n + 3) * p2,
        2 * p0,
        2 * p0,
        2 * p0,
    )
    assert all(rate == expected for rate in directed_stationary_rates)

    phases = ((n, 0, 2), (n + 1, 1, 1), (n + 3, 2, 0))
    for a, b, c in phases:
        assert b + c == 2
        assert a - b * (b + 1) // 2 == n

    # Check every enabled oriented reaction from sample states of each class.
    for a, b, c in phases:
        for d in range(6):
            x = (a, b, c, d)
            for y, yp in PAIRS:
                for source, target in ((y, yp), (yp, y)):
                    if propensity(x, source) > 0:
                        x_next = tuple(xi - yi + ypi for xi, yi, ypi in zip(x, source, target))
                        aa, bb, cc, _ = x_next
                        assert bb + cc == 2
                        assert aa - bb * (bb + 1) // 2 == n

    # Detailed-balance ratios across the three internal phase edges.
    assert p1 * (n + 1) == p0 * 2
    assert p2 * 2 * (n + 2) * (n + 3) == p1
    assert p2 * (n + 1) * (n + 2) * (n + 3) == p0
    # On the phase-0 edges changing D: π(d)·2 = π(d+1)·2(d+1), exactly.
    for d in range(10):
        poisson_d = F(1, factorial(d))
        poisson_next = F(1, factorial(d + 1))
        assert poisson_d * 2 == poisson_next * 2 * (d + 1)
    return z, p, expected


if __name__ == "__main__":
    for n in range(8):
        z, p, rate = check(n)
        print(f"n={n}: Z={z}, phases={p}, each_oriented_rate={rate}")
