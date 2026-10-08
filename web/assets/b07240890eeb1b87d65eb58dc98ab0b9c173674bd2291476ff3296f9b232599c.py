#!/usr/bin/env python3
"""Exact rational checks for the rank-one pure-qubit cutoff construction.

This is finite evidence only.  The proof in finite_rank_boundary.txt uses the
same factorial-moment inequality for arbitrary n and R.
"""

from fractions import Fraction
from math import comb, factorial
import argparse
import json


def binomial_tail(n: int, p: Fraction, m: int) -> Fraction:
    """P[Bin(n,p) >= m], computed exactly."""
    if m > n:
        return Fraction(0)
    q = 1 - p
    return sum(
        (Fraction(comb(n, k)) * p**k * q ** (n - k) for k in range(m, n + 1)),
        Fraction(0),
    )


def cutoff_m(r: Fraction, eps: Fraction) -> int:
    """Smallest m>=1 with r^(2m)/m! <= eps^2/4, exactly."""
    r2 = r * r
    m = 1
    while r2**m / factorial(m) > eps * eps / 4:
        m += 1
    return m


def check_case(n: int, b: int, r: Fraction) -> dict[str, object]:
    """Check the cutoff/tail/error inequalities for eps=2^-b."""
    eps = Fraction(1, 2**b)
    m = cutoff_m(r, eps)
    # Exact Dicke truncation is used only if the cutoff is below the full
    # symmetric-space dimension.  Otherwise the exact n+1-dimensional archive
    # is cheaper.
    memory_dimension = min(n + 1, m + 1)
    if m <= n:
        p = r * r / (n + r * r)
        tail = binomial_tail(n, p, m)
        factorial_bound = r ** (2 * m) / factorial(m)
        assert tail <= factorial_bound
        assert factorial_bound <= eps * eps / 4
        assert tail <= eps * eps / 4
        # The trace-distance bound is sqrt(tail)+tail.  For eps<=1, the
        # displayed tail premise implies this is <= 3 eps/4 <= eps.
        output = {
            "n": n,
            "epsilon": str(eps),
            "radius": str(r),
            "tail_start_m": m,
            "archive_dimension": memory_dimension,
            "binomial_tail_exact": str(tail),
            "factorial_moment_bound_exact": str(factorial_bound),
            "tail_le_epsilon_squared_over_4": True,
            "trace_distance_bound_le_epsilon": True,
        }
    else:
        output = {
            "n": n,
            "epsilon": str(eps),
            "radius": str(r),
            "tail_start_m": m,
            "archive_dimension": memory_dimension,
            "exact_symmetric_archive": True,
            "trace_distance": "0",
            "trace_distance_bound_le_epsilon": True,
        }
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--radius", default="1", help="nonnegative rational radius")
    parser.add_argument("--n", nargs="+", type=int, default=[1, 2, 4, 8, 16, 64, 256])
    parser.add_argument("--bits", nargs="+", type=int, default=[2, 4, 8, 16, 32])
    args = parser.parse_args()
    radius = Fraction(args.radius)
    if radius <= 0:
        raise SystemExit("radius must be positive")
    if any(n < 1 for n in args.n) or any(b < 1 for b in args.bits):
        raise SystemExit("n and precision bits must be positive")
    rows = [check_case(n, b, radius) for n in args.n for b in args.bits]
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
