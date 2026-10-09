#!/usr/bin/env python3
"""Exact moment checks for the countable reversible two-state mixture.

This script validates finite Hankel minors of the analytic counterexample in
v1 and prints the uniform path-law truncation bound. The infinite-rank proof
is the polynomial-support argument in v1, not the finite computations here.
"""

from fractions import Fraction
from math import comb


def moment(k: int) -> Fraction:
    """m_k = sum_{n>=1} 2^-n (2(1-2^-n))^k, exactly."""
    return Fraction(2**k) * sum(
        (Fraction((-1) ** j * comb(k, j), 2 ** (j + 1) - 1)
         for j in range(k + 1)),
        Fraction(0),
    )


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    """Bareiss elimination over rationals; exact for the small demo matrices."""
    a = [row[:] for row in matrix]
    n = len(a)
    if n == 0:
        return Fraction(1)
    sign = 1
    previous = Fraction(1)
    for k in range(n - 1):
        if a[k][k] == 0:
            swap = next((r for r in range(k + 1, n) if a[r][k] != 0), None)
            if swap is None:
                return Fraction(0)
            a[k], a[swap] = a[swap], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * pivot - a[i][k] * a[k][j]) / previous
        for i in range(k + 1, n):
            a[i][k] = Fraction(0)
        previous = pivot
    return sign * a[-1][-1]


def main() -> None:
    max_degree = 6
    print("degree, hankel_determinant_positive")
    for degree in range(max_degree + 1):
        hankel = [
            [moment(i + j) for j in range(degree + 1)]
            for i in range(degree + 1)
        ]
        det = determinant(hankel)
        print(f"{degree}, {det > 0}")

    print("\nmixture truncation, omitted mass / path-TV upper bound")
    for cutoff in (2, 4, 8, 12, 16):
        print(f"{cutoff}, {Fraction(1, 2**cutoff)}")


if __name__ == "__main__":
    main()
