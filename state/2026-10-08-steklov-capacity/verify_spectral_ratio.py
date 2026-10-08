#!/usr/bin/env python3
"""Finite diagnostics for the spectral-capacity research note.

Python >=3.8, standard library only. These numerical checks validate
closed-form capacity/collar algebra, not the infinite-dimensional PDE
comparison or the existence of a Ricci-nonnegative saturating metric.
"""

from math import exp, isclose, sqrt, factorial


def cone_frequency(l, v):
    """Indicial exponent for a round two-sphere cone of AVR v."""
    assert 0 < v <= 1 and isinstance(l, int) and l >= 0
    return (sqrt(1 + 4 * l * (l + 1) / v) - 1) / 2


def cone_cycle_ratio(M, v):
    """Number of round harmonics / squared mean radial exponent."""
    assert M >= 1
    size = (M + 1) ** 2
    weighted_sum = sum((2 * l + 1) * cone_frequency(l, v) for l in range(M + 1))
    mean = weighted_sum / size
    return size / mean ** 2


def neumann_collar_frequency(lam, a, d, delta):
    """Scaled DtN eigenvalue on e^-delta <=r<=1, Neumann at inner edge."""
    assert lam >= 0 and a > 0 and d >= 2 and delta > 0
    p = (sqrt((d - 1) ** 2 + 4 * lam / (a * a)) - (d - 1)) / 2
    x = exp(-delta * (2 * p + d - 1))
    return p * (1 - x) / (1 + p / (p + d - 1) * x)


def general_capacity(d, v):
    """Abstract sharp asymptotic spectral transport coefficient."""
    assert d >= 2 and v > 0
    return (2 / factorial(d)) * v * ((d + 1) / d) ** d


def run():
    v = 0.81
    print("3D capacity; v=0.81")
    limit = 9 * v / 4
    print("Predicted coefficient:", format(limit, ".10f"))
    for M in (10, 30, 100, 300, 1000):
        print(f"M={M:4d}: {cone_cycle_ratio(M, v):.8f}")
    assert abs(cone_cycle_ratio(1000, v) - limit) < 0.003
    assert isclose(general_capacity(2, v), limit, abs_tol=1e-14)

    print("\nNeumann collar eigenvalue over sqrt(lambda)/a; d=2 a=0.9 delta=0.4")
    for lam in (1, 5, 100, 10000, 1000000):
        nu = neumann_collar_frequency(lam, sqrt(v), 2, 0.4)
        ratio = nu / (sqrt(lam) / sqrt(v))
        print(f"lambda={lam:7d} ratio={ratio:.9f}")
    assert abs(neumann_collar_frequency(1e6, sqrt(v), 2, 0.4)
               / (sqrt(1e6) / sqrt(v)) - 1) < 0.001

    print("\nALL finite coefficient checks passed")
    print("LIMITATION: no numerical test certifies a PDE theorem or metric existence.")


if __name__ == "__main__":
    run()
