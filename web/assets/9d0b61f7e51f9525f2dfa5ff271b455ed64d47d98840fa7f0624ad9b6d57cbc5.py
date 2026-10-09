#!/usr/bin/env python3
"""Finite arithmetic checks for the A01 rare-event derivations.

This script checks formulas on finite parameter grids; it is not proof evidence.
"""
from math import isclose, prod


def geometric_clock_second_moment(lam: float, rho: float) -> float:
    threshold = 2 * lam - lam * lam
    if rho >= threshold:
        return float("inf")
    return lam * lam * (1 - rho) / (rho * (threshold - rho))


def finite_geometric_sum(lam: float, rho: float, terms: int = 2_000_000) -> float:
    p = lam
    q = rho
    ratio = (1 - lam) ** 2 / (1 - rho)
    if ratio >= 1:
        return float("inf")
    # Closed partial sum avoids looping over millions of terms.
    return lam * lam / rho * (1 - ratio**terms) / (1 - ratio)


def product_second_moment(theta, n):
    p = prod(theta)
    second_ratio = prod(1 + (1 - x) / (n * x) for x in theta)
    return p, second_ratio


def main():
    # Check the clock formula against its convergent geometric partial sum.
    clock_cases = [(0.01, 0.005), (0.01, 0.01), (0.01, 0.015), (0.1, 0.05)]
    for lam, rho in clock_cases:
        closed = geometric_clock_second_moment(lam, rho)
        partial = finite_geometric_sum(lam, rho, 100_000)
        assert isclose(closed, partial, rel_tol=1e-10, abs_tol=1e-10), (lam, rho, closed, partial)
    assert geometric_clock_second_moment(0.01, 0.01995) == float("inf")

    # Check the product-estimator moment identity for a non-identical chain.
    theta = [0.3, 0.7, 0.51, 0.91]
    n = 10_000
    p, ratio = product_second_moment(theta, n)
    direct = prod(x * x + x * (1 - x) / n for x in theta) / (p * p)
    assert isclose(ratio, direct, rel_tol=1e-12, abs_tol=1e-12)

    # Show the cost scale separation on a modest rare event.
    T, alpha, eps, eta = 40, 0.5, 0.1, 0.05
    p = alpha**T
    n_row = int(10 * T / (alpha * eps**2) + 0.999999)
    k = int((32 / 9) * __import__("math").log(1 / eta) + 0.999999)
    local_calls = T * n_row * k
    crude_scale = 1 / (p * eps**2)
    print(f"clock cases checked: {len(clock_cases)}")
    print(f"product p={p:.8g}; local calls upper scale={local_calls:,}; crude relative-MSE scale={crude_scale:.3e}")


if __name__ == "__main__":
    main()
