#!/usr/bin/env python3
"""Exact finite checks for the independent-orientation purification and MH lift.

Standard library only. Integer determinants and rational transition identities.
This checks the displayed examples; the general marginal/detailed-balance
claims are proved in INITIAL.txt.
"""
from fractions import Fraction
from itertools import combinations
import json
from math import comb
from pathlib import Path


def det_bareiss(a):
    a = [list(map(int, row)) for row in a]
    n = len(a)
    if n == 0:
        return 1
    sign = 1
    prev = 1
    for k in range(n - 1):
        pivot = next((i for i in range(k, n) if a[i][k] != 0), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        p = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * p - a[i][k] * a[k][j]
                assert numerator % prev == 0
                a[i][j] = numerator // prev
        for i in range(k + 1, n):
            a[i][k] = 0
        prev = p
    return sign * a[n - 1][n - 1]


def minor(f, rows, cols):
    return det_bareiss([[f[i][j] for j in cols] for i in rows])


def orientation_weights(f, retained):
    retained = tuple(sorted(retained))
    assert len(retained) % 2 == 0
    k = len(retained) // 2
    out = {}
    for I in combinations(retained, k):
        I = tuple(I)
        J = tuple(i for i in retained if i not in I)
        d = minor(f, I, J)
        out[I] = d * d
    return out


def directed_cycle(n):
    f = [[0] * n for _ in range(n)]
    for i in range(n):
        f[i][(i + 1) % n] = 1
    return f


def check_sewing_counter():
    n = 8
    f = [[0] * n for _ in range(n)]
    for i, j in [(0, 3), (2, 1), (1, 6), (4, 0), (5, 7)]:
        f[i][j] = 1
    R1 = (0, 1, 2, 3)
    R2 = (0, 1, 4, 5, 6, 7)
    C = {0, 1}
    w1 = orientation_weights(f, R1)
    w2 = orientation_weights(f, R2)
    Z1, Z2 = sum(w1.values()), sum(w2.values())
    supp1 = [I for I, w in w1.items() if w]
    supp2 = [I for I, w in w2.items() if w]
    assert Z1 == Z2 == 1
    assert supp1 == [(0, 2)]
    assert supp2 == [(1, 4, 5)]
    I1, I2 = supp1[0], supp2[0]
    mismatch = tuple(sorted((set(I1) & C) ^ (set(I2) & C)))
    assert mismatch == (0, 1)
    # All lifted mass is retained by the explicit mismatch label; the old
    # equality projector keeps no mass.
    lifted_norm2 = Z1 * Z2
    equal_core_projected_norm2 = sum(
        w1[I] * w2[J]
        for I in w1 for J in w2
        if (set(I) & C) == (set(J) & C)
    )
    assert lifted_norm2 == 1 and equal_core_projected_norm2 == 0
    return {
        "n": n,
        "Z_R1": Z1,
        "Z_R2": Z2,
        "positive_I1": list(I1),
        "positive_I2": list(I2),
        "common_core": sorted(C),
        "mismatch_register": list(mismatch),
        "lifted_product_norm_squared": lifted_norm2,
        "equal_core_projected_norm_squared": equal_core_projected_norm2,
    }


def check_cycle_global_mh(q):
    n = 2 * q
    f = directed_cycle(n)
    weights = orientation_weights(f, tuple(range(n)))
    positive = [(I, w) for I, w in weights.items() if w]
    N = comb(n, q)
    assert len(weights) == N
    assert len(positive) == 2
    assert all(w == 1 for _, w in positive)
    # Product chain proposes two arbitrary orientations independently.
    # It has four positive product states, each equal weight. Every distinct
    # positive-state transition has probability 1/N^2; its exact gap is 4/N^2.
    product_support_size = len(positive) ** 2
    proposal_space = N * N
    gap = Fraction(product_support_size, proposal_space)
    assert product_support_size == 4
    assert gap == Fraction(4, N * N)
    # Confirm detailed balance for every pair in the positive support.
    pweights = [Fraction(w1 * w2) for _, w1 in positive for _, w2 in positive]
    assert len(pweights) == 4 and len(set(pweights)) == 1
    for i in range(4):
        for j in range(4):
            if i != j:
                forward = pweights[i] * Fraction(1, proposal_space)
                reverse = pweights[j] * Fraction(1, proposal_space)
                assert forward == reverse
    return {
        "q": q,
        "n": n,
        "orientation_space_size": N,
        "positive_orientations": [list(I) for I, _ in positive],
        "positive_two_replica_states": product_support_size,
        "proposal_space_size": proposal_space,
        "exact_product_chain_spectral_gap": f"4/{N*N}",
        "gap_fraction": str(gap),
    }


def check_product_marginals():
    # Nonuniform tiny fibers verify that mismatch is a deterministic isometric
    # tag and summing it out gives the exact independent product law.
    w1 = {(0,): 1, (1,): 3}
    w2 = {(0,): 2, (1,): 5}
    z1, z2 = sum(w1.values()), sum(w2.values())
    joint = {}
    marginal1 = {I: Fraction(0) for I in w1}
    marginal2 = {J: Fraction(0) for J in w2}
    for I, a in w1.items():
        for J, b in w2.items():
            delta = tuple(sorted(set(I) ^ set(J)))
            p = Fraction(a * b, z1 * z2)
            joint[(I, J, delta)] = p
            marginal1[I] += p
            marginal2[J] += p
    assert sum(joint.values()) == 1
    assert marginal1 == {I: Fraction(a, z1) for I, a in w1.items()}
    assert marginal2 == {J: Fraction(b, z2) for J, b in w2.items()}
    return {"normalizer": [z1, z2], "all_marginals_exact": True,
            "joint_states": len(joint)}


def main():
    result = {
        "scope": "finite exact diagnostics only; not a mixing/FPRAS proof",
        "sewing_counter": check_sewing_counter(),
        "product_marginal_fixture": check_product_marginals(),
        "directed_cycle_uniform_mh": [check_cycle_global_mh(q) for q in (2, 3, 4)],
        "determinant_arithmetic": "Bareiss exact integers",
        "transition_arithmetic": "fractions.Fraction",
    }
    out = Path(__file__).with_name("lifted_orientation_checks.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
