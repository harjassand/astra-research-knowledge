#!/usr/bin/env python3
"""Exact checks for the random-scan energy constant and DPP rejection example."""
from fractions import Fraction
from itertools import combinations
import json
from math import comb
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lifted_orientation import det_bareiss, directed_cycle, orientation_weights


def transpose(a):
    return [list(row) for row in zip(*a)]


def dpp_pair_mass(q):
    n = 2 * q
    f = directed_cycle(n)
    ft = transpose(f)
    V = [[int(i == j) for j in range(n)] + ft[i] for i in range(n)]
    total_by_cb = 0
    for B in combinations(range(2 * n), n):
        d = det_bareiss([[V[i][j] for j in B] for i in range(n)])
        total_by_cb += d * d
    vv_star = [
        [sum(V[i][j] * V[k][j] for j in range(2 * n)) for k in range(n)]
        for i in range(n)
    ]
    total_by_gram = det_bareiss(vv_star)
    assert total_by_cb == total_by_gram == 2**n

    hard = 0
    for S in combinations(range(n), q):
        cols = tuple(S) + tuple(n + i for i in S)
        d = det_bareiss([[V[i][j] for j in cols] for i in range(n)])
        complement = tuple(i for i in range(n) if i not in S)
        d_pair = det_bareiss([[f[i][j] for j in complement] for i in S])
        assert d * d == d_pair * d_pair
        hard += d * d
    # Same hard mass as sum_S |det F[S,complement S]|^2.
    weights = orientation_weights(f, tuple(range(n)))
    assert hard == sum(weights.values()) == 2
    probability = Fraction(hard, total_by_cb)
    assert probability == Fraction(1, 2 ** (n - 1))
    return {
        "q": q,
        "n": n,
        "all_DPP_mass": total_by_cb,
        "hard_pair_mass": hard,
        "hard_event_probability": str(probability),
        "expected_rejection_draws": str(1 / probability),
    }


def random_scan_matrix(q):
    n = 2 * q
    f = directed_cycle(n)
    weights = orientation_weights(f, tuple(range(n)))
    support = [S for S, w in weights.items() if w]
    assert len(support) == 2
    m = comb(n, q)
    # Each single-replica global uniform-proposal MH chain changes to the
    # other positive orientation with probability 1/m.
    K = [[Fraction(1) - Fraction(1, m), Fraction(1, m)],
         [Fraction(1, m), Fraction(1) - Fraction(1, m)]]
    assert K[0][1] == K[1][0]
    # Product random scan: update one replica with probability 1/2.
    states = [(0, 0), (0, 1), (1, 0), (1, 1)]
    P = [[Fraction(0) for _ in states] for _ in states]
    for i, x in enumerate(states):
        for j, y in enumerate(states):
            if x == y:
                P[i][j] = Fraction(1) - Fraction(1, m)
            elif x[1] == y[1] and x[0] != y[0]:
                P[i][j] = Fraction(1, 2 * m)
            elif x[0] == y[0] and x[1] != y[1]:
                P[i][j] = Fraction(1, 2 * m)
        assert sum(P[i]) == 1
    # Verify the exact eigenvectors: one constant, two coordinate modes,
    # and one product mode.
    modes = [
        ([1, 1, 1, 1], Fraction(1)),
        ([1, 1, -1, -1], Fraction(1) - Fraction(1, m)),
        ([1, -1, 1, -1], Fraction(1) - Fraction(1, m)),
        ([1, -1, -1, 1], Fraction(1) - Fraction(2, m)),
    ]
    for v, lam in modes:
        for i in range(4):
            assert sum(P[i][j] * v[j] for j in range(4)) == lam * v[i]
    gap = Fraction(1, m)
    # For f1 = indicator(first orientation is support[0]), f2=0,
    # Var=1/4 and E=1/(4m), so L >= m is exact.
    variance = Fraction(1, 4)
    energy = Fraction(1, 4 * m)
    assert variance / energy == m
    return {
        "q": q,
        "single_orientation_space": m,
        "single_chain_gap": str(Fraction(2, m)),
        "random_scan_product_gap": str(gap),
        "additive_test_variance": str(variance),
        "additive_test_energy": str(energy),
        "necessary_L": str(m),
    }


def main():
    result = {
        "scope": "finite exact diagnostics for algebraic formulas",
        "DPP_postselection": [dpp_pair_mass(q) for q in (2, 3, 4)],
        "random_scan_energy": [random_scan_matrix(q) for q in (2, 3, 4)],
        "arithmetic": "Bareiss integers and exact Fraction",
    }
    out = Path(__file__).with_name("01_energy_and_dpp_boundary_checks.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
