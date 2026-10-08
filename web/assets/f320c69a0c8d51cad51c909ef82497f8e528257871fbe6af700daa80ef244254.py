#!/usr/bin/env python3
"""Reproduce exact 1D contrast and coupon-count arithmetic (not a proof)."""

from fractions import Fraction
from math import ceil, log


def main() -> None:
    K = 100
    gamma = Fraction(K - 1, K)
    D = gamma / (1 - Fraction(3, 4) * gamma) ** 2
    assert gamma == Fraction(99, 100)
    assert D == Fraction(158400, 10609)

    print(f"K={K}; gamma={gamma}={float(gamma):.8f}")
    print(f"D_K={D}={float(D):.8f}")
    for eps in (0.1, 0.01):
        delta = 0.05
        sufficient = ceil(float(D) ** 2 / (2 * eps**2) * log(2 / delta))
        necessary_threshold = (
            3 * float(D) ** 2 / (1024 * eps**2) * log(1 / (4 * delta))
        )
        print(
            f"eps={eps:g}, delta={delta:g}: Hoeffding sufficient M={sufficient}; "
            f"two-point necessary threshold={necessary_threshold:.3f}"
        )
        for n in (1, 100, 1000):
            N = ceil(sufficient / n)
            assert n * N >= sufficient
            print(f"  width n={n} cells -> coupon count N={N}, total cells={n*N}")


if __name__ == "__main__":
    main()
