#!/usr/bin/env python3
"""Exact small-instance replay for the directed-cycle Gutzwiller witness.

This is finite evidence only. The proof for every even cycle is in RESULT.txt.
No third-party packages are required.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path


def det_integer(matrix: list[list[int]]) -> int:
    """Exact determinant by the Leibniz formula (fixtures have k <= 4)."""
    n = len(matrix)
    if n == 0:
        return 1
    total = 0
    for perm in itertools.permutations(range(n)):
        inversions = sum(
            perm[i] > perm[j]
            for i in range(n)
            for j in range(i + 1, n)
        )
        term = (-1 if inversions & 1 else 1)
        for i, j in enumerate(perm):
            term *= matrix[i][j]
        total += term
    return total


def rayleigh_at_ones(monomials: list[tuple[int, ...]], i: int, j: int) -> int:
    """Return (d_i f)(d_j f) - f(d_i d_j f) at the all-ones point."""
    value = len(monomials)
    di = sum(m[i] for m in monomials)
    dj = sum(m[j] for m in monomials)
    dij = sum(m[i] * m[j] for m in monomials)
    return di * dj - value * dij


def cycle_fixture(n: int) -> dict[str, object]:
    assert n >= 4 and n % 2 == 0
    k = n // 2
    # A[i, pi(i)] = 1, where pi is the directed successor cycle.
    a = [[0] * n for _ in range(n)]
    for i in range(n):
        a[i][(i + 1) % n] = 1

    supports: list[dict[str, object]] = []
    z = 0
    for rows in itertools.combinations(range(n), k):
        for cols in itertools.combinations((j for j in range(n) if j not in rows), k):
            minor = [[a[i][j] for j in cols] for i in rows]
            d = det_integer(minor)
            if d:
                z += d * d
                supports.append({"I_zero_based": list(rows), "J_zero_based": list(cols), "det": d})

    expected = [tuple(range(0, n, 2)), tuple(range(1, n, 2))]
    observed_rows = sorted(tuple(item["I_zero_based"]) for item in supports)
    assert z == 2
    assert observed_rows == sorted(expected)
    assert len(supports) == 2
    assert all(abs(int(item["det"])) == 1 for item in supports)

    return {
        "n": n,
        "k": k,
        "candidate_pair_count": math.comb(n, k),
        "positive_pair_count": len(supports),
        "Z_k": z,
        "positive_support_fraction": f"2/{math.comb(n, k)}",
        "positive_atoms": supports,
        "exact_check": "PASS",
    }


def block_pair_fixture() -> dict[str, object]:
    """Brute-force the exact DP formula on two rational 2-site blocks."""
    n = 4
    blocks = [(1, 2), (3, 5)]
    a = [[0] * n for _ in range(n)]
    for b, (left_to_right, right_to_left) in enumerate(blocks):
        i = 2 * b
        a[i][i + 1] = left_to_right
        a[i + 1][i] = right_to_left

    by_k: dict[str, int] = {}
    for k in (1, 2):
        z = 0
        for rows in itertools.combinations(range(n), k):
            for cols in itertools.combinations((j for j in range(n) if j not in rows), k):
                z += det_integer([[a[i][j] for j in cols] for i in rows]) ** 2
        expected = sum(
            math.prod((blocks[b][0] ** 2 + blocks[b][1] ** 2) for b in chosen)
            for chosen in itertools.combinations(range(len(blocks)), k)
        )
        assert z == expected
        by_k[str(k)] = z

    # The unfiltered fixed-k norm is the coefficient of
    # prod_b (1+t*a_b^2)(1+t*b_b^2).
    all_weights = [v * v for pair in blocks for v in pair]
    s2 = sum(all_weights[i] * all_weights[j] for i in range(n) for j in range(i + 1, n))
    assert by_k["1"] == sum(all_weights) == 39
    assert by_k["2"] == 170 and s2 == 399
    return {
        "blocks": [[a, b] for a, b in blocks],
        "Z_by_k": by_k,
        "unfiltered_S2": s2,
        "fixed_sector_acceptance_k2": "170/399",
        "exact_check": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    cases = [cycle_fixture(n) for n in (4, 6, 8)]
    # Exponent vectors for h=x1*x3+x2*x4 and
    # P=x1*x3*y2*y4+x2*x4*y1*y3, respectively.
    rayleigh_h = rayleigh_at_ones([(1, 0, 1, 0), (0, 1, 0, 1)], 0, 2)
    rayleigh_joint = rayleigh_at_ones(
        [
            (1, 0, 1, 0, 0, 1, 0, 1),
            (0, 1, 0, 1, 1, 0, 1, 0),
        ],
        0,
        5,
    )
    assert rayleigh_h < 0 and rayleigh_joint < 0

    result = {
        "status": "FINITE-EVIDENCE",
        "cases": cases,
        "block_pair_case": block_pair_fixture(),
        "n4_paired_gram_rayleigh_difference_at_ones": rayleigh_h,
        "n4_joint_determinant_square_rayleigh_difference_at_ones": rayleigh_joint,
        "notes": [
            "The exact all-even-n proof is in RESULT.txt; these enumerations do not replace it.",
            "A negative Rayleigh difference refutes real stability by Borcea-Branden-Liggett Theorem 4.1.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
