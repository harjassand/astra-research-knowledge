#!/usr/bin/env python3
"""Exact diagnostics for pair-volume random-phase determinant projection.

The test family is F = direct_sum_m [[0,1],[1,0]], with n=2m sites and
target k=m.  All calculations below use integer Laurent coefficients.
"""

from fractions import Fraction
from itertools import combinations


def swap_block_volume(site_count: int) -> int:
    """Pair Gram determinant in one 2-site block for 0, 1, or 2 sites."""
    if site_count == 2:
        return 0  # selected pair columns are duplicated, rank 2 < 4
    return 1  # empty determinant or one site's two orthonormal columns


def target_normalizer(m: int) -> int:
    """Enumerate the site subsets of size m and sum their pair volumes."""
    n = 2 * m
    z = 0
    for chosen in combinations(range(n), m):
        chosen_set = set(chosen)
        volume = 1
        for b in range(m):
            count = int(2 * b in chosen_set) + int(2 * b + 1 in chosen_set)
            volume *= swap_block_volume(count)
        z += volume
    return z


def multiply_laurent(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            out[i + j] = out.get(i + j, Fraction(0)) + x * y
    return out


def main() -> None:
    # One block's top determinant coefficient is Y(u)=2+u+u^{-1}.
    y = {-1: Fraction(1), 0: Fraction(2), 1: Fraction(1)}
    y2 = multiply_laurent(y, y)
    mean_one_block = y.get(0, Fraction(0))
    second_one_block = y2.get(0, Fraction(0))
    assert mean_one_block == 2
    assert second_one_block == 6

    print("m sites n=2m target_Z second_moment relative_second_moment")
    for m in (1, 2, 3, 4, 6, 8):
        z = target_normalizer(m)
        assert z == 2**m
        second = second_one_block**m
        relative_second = Fraction(second, z * z)
        assert relative_second == Fraction(3, 2) ** m
        print(m, 2 * m, z, second, relative_second)

    print("one_block_Y_squared_laurent_coefficients", dict(sorted(y2.items())))
    print("exact conclusion: Var(X)/E[X]^2 = (3/2)^m - 1")


if __name__ == "__main__":
    main()
