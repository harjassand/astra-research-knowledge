#!/usr/bin/env python3
"""Exact finite checks for the order-10 stochastic explosive route in Example 3.2.

This validates the state updates and propensity-degree gaps. Infinite-product
positivity and finite total explosion time require the analytic summability
argument in the primary source; these finite checks are not a proof of those
infinite assertions.
"""
from fractions import Fraction


def falling(n: int, k: int) -> int:
    if n < k:
        return 0
    out = 1
    for j in range(k):
        out *= n - j
    return out


def cycle(n: int) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
    x0 = (n, 0)
    x1 = (x0[0] + 2, x0[1] + 1)  # 2A -> 4A+B
    x2 = (x1[0] + 2, x1[1] + 3)  # 4A+B -> 6A+4B
    x3 = (x2[0] - 3, x2[1] - 4)  # 6A+4B -> 3A
    assert x3 == (n + 1, 0)
    return x0, x1, x2, x3


def route_failure(n: int) -> tuple[Fraction, Fraction, Fraction]:
    # All rate constants are 1. These are the selected propensity and the
    # other enabled reactions at each state on the cited route.
    a0 = falling(n, 2)
    fail0 = Fraction(1, a0 + 1)  # 0 -> 2A competes at constant rate 1

    a1 = falling(n + 2, 4)  # selected 4A+B; B=1
    b1 = falling(n + 2, 2) + 1  # 2A and 0 sources
    fail1 = Fraction(b1, a1 + b1)

    a2 = falling(n + 4, 6) * falling(4, 4)  # selected 6A+4B
    b2 = falling(n + 4, 4) * 4 + falling(n + 4, 2) + 1
    fail2 = Fraction(b2, a2 + b2)
    return fail0, fail1, fail2


def main() -> None:
    # Sources in 0 -> 2A -> 4A+B -> 6A+4B -> 3A.
    source_molecularities = (0, 2, 5, 10)
    assert max(source_molecularities) == 10

    worst_scaled_failure = Fraction(0, 1)
    for n in range(10, 1001):
        xs = cycle(n)
        assert xs[1] == (n + 2, 1)
        assert xs[2] == (n + 4, 4)
        assert xs[3] == (n + 1, 0)
        for p_fail in route_failure(n):
            worst_scaled_failure = max(worst_scaled_failure, n * n * p_fail)

    print("source molecularities:", source_molecularities)
    print("cycle state update verified for n=10..1000: (n,0)->(n+2,1)->(n+4,4)->(n+1,0)")
    print("max over n=10..1000 and three stages of n^2 * route-failure probability:",
          float(worst_scaled_failure))
    print("All checks use exact integer/Fraction arithmetic; the printed maximum is finite-range evidence only.")


if __name__ == "__main__":
    main()
