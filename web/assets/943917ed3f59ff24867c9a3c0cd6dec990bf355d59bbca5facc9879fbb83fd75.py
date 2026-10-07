#!/usr/bin/env python3
"""Exact small checks for the c03_l06 promise/normalization audit.

This is diagnostic arithmetic, not a proof of the uniform reductions.
Only the standard library is used.
"""

from fractions import Fraction
from itertools import combinations
import json


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def perfect_matchings(vertices, edges):
    if not vertices:
        return 1
    v = min(vertices)
    rest = vertices - {v}
    total = 0
    for w in sorted(rest):
        if tuple(sorted((v, w))) in edges:
            total += perfect_matchings(rest - {w}, edges)
    return total


def parity_zero_example():
    # F = J - I on four sites. Its off-diagonal support is K4.
    n = 4
    F = [[int(i != j) for j in range(n)] for i in range(n)]
    disjoint_minor_dets = []
    for I in combinations(range(n), 2):
        for J in combinations(range(n), 2):
            if set(I).isdisjoint(J):
                sub = [[F[i][j] for j in J] for i in I]
                disjoint_minor_dets.append(det2(sub))
    edges = {tuple(sorted((i, j))) for i in range(n) for j in range(i + 1, n)}
    matchings = perfect_matchings(set(range(n)), edges)
    assert len(disjoint_minor_dets) == 6
    assert all(d == 0 for d in disjoint_minor_dets)
    assert matchings == 3
    return {
        "ordered_disjoint_2x2_minors": len(disjoint_minor_dets),
        "all_determinants": disjoint_minor_dets,
        "hard_pair_partition_c2": sum(d * d for d in disjoint_minor_dets),
        "support_graph_perfect_matchings": matchings,
    }


def scaling_invariance():
    # For F=[[0,1],[1,0]], k=1 has two unit-weight outcomes.
    weights = [Fraction(1), Fraction(1)]
    scale = Fraction(1, 8)
    scaled_weights = [w * scale**2 for w in weights]
    z = sum(weights)
    z_scaled = sum(scaled_weights)
    law = [w / z for w in weights]
    scaled_law = [w / z_scaled for w in scaled_weights]
    assert law == scaled_law == [Fraction(1, 2), Fraction(1, 2)]
    assert z_scaled == z * scale**2
    return {
        "scale": str(scale),
        "partition_before": str(z),
        "partition_after": str(z_scaled),
        "normalized_law_before": [str(p) for p in law],
        "normalized_law_after": [str(p) for p in scaled_law],
    }


def tv_gap_check():
    # R=4 is an exact fixture. The proof uses a_R>3/5 for every R>=4.
    R = 4
    a = 1 - Fraction(R - 1, R) ** R
    p_yes, p_no = Fraction(2, 3), Fraction(1, 3)
    one_yes = Fraction(1, 2) + a * (p_yes - Fraction(1, 2))
    one_no = Fraction(1, 2) + a * (p_no - Fraction(1, 2))
    error = Fraction(1, 100) + Fraction(1, 200) + Fraction(1, 256)
    half_gap = a / 6
    margin = half_gap - error
    assert one_yes - Fraction(1, 2) == half_gap
    assert Fraction(1, 2) - one_no == half_gap
    assert margin > Fraction(3, 40)
    return {
        "R": R,
        "readout_success_probability": str(a),
        "yes_probability_one": str(one_yes),
        "no_probability_one": str(one_no),
        "one_side_gap": str(half_gap),
        "rounding_plus_filter_plus_sampler_error": str(error),
        "remaining_margin_at_R4": str(margin),
    }


def filter_bound_check():
    # p*=2^-q, p0' >= p*/2, ell >= ceil((q+10)/2).
    # Then 2*g^2/p0' <= 4*g^2/p* <= 1/256.
    q = 12
    ell = (q + 10 + 1) // 2
    p_star = Fraction(1, 2**q)
    g2 = Fraction(1, 2 ** (2 * ell))
    upper = 4 * g2 / p_star
    assert upper == Fraction(1, 256)
    return {"q_fixture": q, "ell": ell, "filter_tv_upper_bound": str(upper)}


if __name__ == "__main__":
    result = {
        "status": "exact finite diagnostics only",
        "parity_zero_example": parity_zero_example(),
        "normalization_scaling": scaling_invariance(),
        "rare_herald_tv_gap": tv_gap_check(),
        "filter_bound": filter_bound_check(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
