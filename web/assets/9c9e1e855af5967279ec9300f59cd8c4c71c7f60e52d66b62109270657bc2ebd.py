#!/usr/bin/env python3
"""Exact finite replay for the universal Pfaffian-quadrature theorem.

Uses only the Python standard library. It checks every pairing at n=6,
enumerates the associated half-sector Z exactly, verifies the block
Pfaffian-square expectation, and checks that the forced even Walsh
characters uniquely determine all 2^(n-1) quotient-class masses.

This is finite evidence; the all-even-n lower bound is proved in RESULT.md.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json
import math


def pairings(items: tuple[int, ...]):
    if not items:
        yield ()
        return
    first = items[0]
    for j in range(1, len(items)):
        second = items[j]
        rest = items[1:j] + items[j + 1 :]
        for tail in pairings(rest):
            yield ((first, second),) + tail


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    a = [row[:] for row in matrix]
    n = len(a)
    sign = 1
    value = Fraction(1)
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign = -sign
        p = a[col][col]
        value *= p
        for r in range(col + 1, n):
            if a[r][col]:
                factor = a[r][col] / p
                for c in range(col + 1, n):
                    a[r][c] -= factor * a[col][c]
                a[r][col] = Fraction(0)
    return sign * value


def make_matrix(n: int, matching: tuple[tuple[int, int], ...],
                weights: tuple[tuple[Fraction, Fraction], ...]):
    a = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for (u, v), (x, y) in zip(matching, weights):
        a[u][v] = x
        a[v][u] = y
    return a


def half_sector_z(a: list[list[Fraction]]) -> Fraction:
    n = len(a)
    k = n // 2
    total = Fraction(0)
    universe = set(range(n))
    for rows in combinations(range(n), k):
        row_set = set(rows)
        cols = tuple(sorted(universe - row_set))
        minor = [[a[i][j] for j in cols] for i in rows]
        d = determinant(minor)
        total += d * d
    return total


def sign_vectors(n: int):
    for bits in product((1, -1), repeat=n):
        yield bits


def block_pfaffian_square(sigma: tuple[int, ...],
                           matching: tuple[tuple[int, int], ...],
                           weights: tuple[tuple[Fraction, Fraction], ...]):
    value = Fraction(1)
    for (u, v), (a, b) in zip(matching, weights):
        value *= (sigma[u] * a - sigma[v] * b) ** 2
    return value


def union_mask(matching: tuple[tuple[int, int], ...], selected: int) -> int:
    mask = 0
    for j, (u, v) in enumerate(matching):
        if (selected >> j) & 1:
            mask |= (1 << u) | (1 << v)
    return mask


def even_nonzero_masks(n: int) -> set[int]:
    return {mask for mask in range(1, 1 << n)
            if mask.bit_count() % 2 == 0}


def quotient_char_matrix(n: int):
    # One representative per global-sign class: coordinate 0 is +1.
    reps = [
        tuple(1 if ((bits >> i) & 1) == 0 else -1 for i in range(n))
        for bits in range(1 << (n - 1))
    ]
    masks = [0] + sorted(even_nonzero_masks(n))
    matrix = []
    for mask in masks:
        row = []
        for sigma in reps:
            value = 1
            for i in range(n):
                if (mask >> i) & 1:
                    value *= sigma[i]
            row.append(Fraction(value))
        matrix.append(row)
    return masks, reps, matrix


def rank(matrix: list[list[Fraction]]) -> int:
    a = [row[:] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][c]
        a[r] = [x / p for x in a[r]]
        for i in range(rows):
            if i != r and a[i][c]:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == rows:
            break
    return r


def main() -> None:
    n = 6
    all_pairings = list(pairings(tuple(range(n))))
    assert len(all_pairings) == 15
    weights = (
        (Fraction(1), Fraction(2, 3)),
        (Fraction(3, 5), Fraction(4, 7)),
        (Fraction(5, 8), Fraction(7, 9)),
    )

    target_checks = []
    for matching in all_pairings:
        a = make_matrix(n, matching, weights)
        z = half_sector_z(a)
        product_formula = Fraction(1)
        for x, y in weights:
            product_formula *= x * x + y * y
        assert z == product_formula

        average = sum(
            (block_pfaffian_square(sigma, matching, weights)
             for sigma in sign_vectors(n)),
            Fraction(0),
        ) / (1 << n)
        assert average == z
        quotient_average = sum(
            (block_pfaffian_square(sigma, matching, weights)
             for sigma in sign_vectors(n) if sigma[0] == 1),
            Fraction(0),
        ) / (1 << (n - 1))
        assert quotient_average == z

        # The normalized sample factors are exactly 1-gamma_i*sigma_u*sigma_v.
        normalized_values = []
        for sigma in sign_vectors(n):
            sample = block_pfaffian_square(sigma, matching, weights) / z
            expanded = Fraction(1)
            for (u, v), (x, y) in zip(matching, weights):
                gamma = 2 * x * y / (x * x + y * y)
                expanded *= 1 - gamma * sigma[u] * sigma[v]
            assert sample == expanded
            normalized_values.append(sample)
        assert sum(normalized_values, Fraction(0)) / (1 << n) == 1

        target_checks.append({
            "pairing": [[u + 1, v + 1] for u, v in matching],
            "Z_half": str(z),
            "uniform_pfaffian_square_mean": str(average),
            "quotient_representative_mean": str(quotient_average),
        })

    forced_masks: set[int] = set()
    for matching in all_pairings:
        for selected in range(1, 1 << (n // 2)):
            forced_masks.add(union_mask(matching, selected))
    expected_masks = even_nonzero_masks(n)
    assert forced_masks == expected_masks

    coverage_counts = []
    for sigma in sign_vectors(n):
        covered = sum(
            all(sigma[u] != sigma[v] for u, v in matching)
            for matching in all_pairings
        )
        balanced = sum(1 for x in sigma if x == 1) == n // 2
        assert covered == (math.factorial(n // 2) if balanced else 0)
        coverage_counts.append(covered)
    pairing_cover_lower_bound = math.ceil(
        len(all_pairings) / math.factorial(n // 2)
    )
    assert pairing_cover_lower_bound == math.ceil(
        math.comb(n, n // 2) / (1 << (n // 2))
    )

    masks, reps, char_matrix = quotient_char_matrix(n)
    char_rank = rank(char_matrix)
    assert len(reps) == (1 << (n - 1))
    assert len(masks) == (1 << (n - 1))
    assert char_rank == (1 << (n - 1))
    # The unique normalized solution to the Fourier constraints is uniform.
    uniform_mass = Fraction(1, len(reps))
    for mask in masks[1:]:
        moment = sum(
            (char_matrix[masks.index(mask)][j] * uniform_mass
             for j in range(len(reps))),
            Fraction(0),
        )
        assert moment == 0

    receipt = {
        "status": "PASS",
        "n": n,
        "k": n // 2,
        "pairing_count": len(all_pairings),
        "pairing_family_checks": target_checks,
        "nontrivial_even_characters": len(expected_masks),
        "characters_forced_by_pairing_families": len(forced_masks),
        "quotient_classes": len(reps),
        "quotient_walsh_matrix_rank": char_rank,
        "minimum_exact_universal_quadrature_atoms": 1 << (n - 1),
        "balanced_sign_pairing_coverage": math.factorial(n // 2),
        "unbalanced_sign_pairing_coverage": 0,
        "relative_error_below_one_support_lower_bound": pairing_cover_lower_bound,
        "scope": (
            "Finite exact check at n=6 only. The proof covers all even n; "
            "the approximate bound is only for a fixed atom support."
        ),
    }
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
