#!/usr/bin/env python3
"""Exact n=6 counterexample to l1 / Renyi-1/2 orientation exchange.

This only enumerates at most C(6,3)=20 complementary row orientations per
coefficient and computes integer determinants by the Leibniz formula.
"""
from itertools import combinations, permutations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
F = [
    [0, -1, -1, -1, 0, 0],
    [0,  0,  0,  0, 0, 0],
    [1,  0,  0,  0, 0, 0],
    [0,  0,  0,  0, 0, 0],
    [0,  0, -1, -1, 0, 0],
    [0, -1, -1,  0, 0, 0],
]
N = len(F)


def determinant(a):
    k = len(a)
    if k == 0:
        return 1
    total = 0
    for p in permutations(range(k)):
        inversions = sum(p[i] > p[j]
                         for i in range(k) for j in range(i + 1, k))
        term = (-1 if inversions % 2 else 1)
        for i, j in enumerate(p):
            term *= a[i][j]
        total += term
    return total


def orientations(holes):
    retained = [i for i in range(N) if i + 1 not in holes]
    assert len(retained) % 2 == 0
    k = len(retained) // 2
    out = []
    for rows in combinations(retained, k):
        rowset = set(rows)
        cols = tuple(i for i in retained if i not in rowset)
        minor = [[F[i][j] for j in cols] for i in rows]
        value = determinant(minor)
        if value:
            out.append({"I_rows_1based": [i + 1 for i in rows],
                        "J_cols_1based": [j + 1 for j in cols],
                        "det": value})
    return out


def summary(holes):
    ori = orientations(holes)
    amplitudes = [o["det"] for o in ori]
    return {"holes_1based": sorted(holes),
            "nonzero_orientations": ori,
            "l1": sum(abs(x) for x in amplitudes),
            "Z_sum_squares": sum(x*x for x in amplitudes),
            "support_size": len(amplitudes),
            "equal_absolute_amplitudes": len(set(map(abs, amplitudes))) <= 1}

S = frozenset()
T = frozenset({2, 4, 5, 6})
a = 2
D = S ^ T
assert a in D
neighbors = []
for j in sorted(D - {a}):
    hs = S ^ {a, j}
    ht = T ^ {a, j}
    neighbors.append({"j": j, "S_exchange": summary(hs),
                      "T_exchange": summary(ht)})

s = summary(S)
t = summary(T)
root_lhs_squared = s["Z_sum_squares"] * t["Z_sum_squares"]
root_rhs = sum((nb["S_exchange"]["Z_sum_squares"] *
                nb["T_exchange"]["Z_sum_squares"]) ** 0.5
               for nb in neighbors)
l1_lhs = s["l1"] * t["l1"]
l1_rhs = sum(nb["S_exchange"]["l1"] *
             nb["T_exchange"]["l1"] for nb in neighbors)

# Exact audited values. The square-root exchange holds with equality, while
# replacing each coefficient's l2 orientation norm by its l1 norm fails.
assert (s["Z_sum_squares"], t["Z_sum_squares"]) == (2, 2)
assert (s["l1"], t["l1"]) == (2, 2)
assert [nb["S_exchange"]["Z_sum_squares"] *
        nb["T_exchange"]["Z_sum_squares"] for nb in neighbors] == [0, 1, 1]
assert [nb["S_exchange"]["l1"] * nb["T_exchange"]["l1"]
        for nb in neighbors] == [0, 1, 1]
assert root_lhs_squared == 4 and root_rhs == 2
assert (l1_lhs, l1_rhs) == (4, 2)
assert all(summary(holes)["equal_absolute_amplitudes"]
           for holes in [S, T] +
           [nb["S_exchange"]["holes_1based"] for nb in neighbors] +
           [nb["T_exchange"]["holes_1based"] for nb in neighbors])

result = {
    "claim": "l1 (equivalently Renyi-1/2 orientation entropy) exchange fails",
    "matrix_F": F,
    "endpoint_S": s,
    "endpoint_T": t,
    "distinguished_coordinate_a": a,
    "neighbors": neighbors,
    "aggregate_sqrt_exchange": {
        "left_squared": root_lhs_squared,
        "rhs_sum_of_sqrt_products": root_rhs,
        "equality": root_lhs_squared ** 0.5 == root_rhs,
    },
    "orientation_l1_exchange": {
        "left": l1_lhs,
        "right": l1_rhs,
        "violation_ratio": l1_lhs / l1_rhs,
    },
    "entropy_identity": "||v_U||_1 = sqrt(Z_U) * exp(H_{1/2}(p_U)/2)",
    "endpoint_Renyi_half_entropies": ["log(2)", "log(2)"],
    "neighbor_Renyi_half_entropies_on_nonzero_terms": ["0", "0"],
    "scope": "exact finite counterexample only; no algorithm or general hardness claim",
}
(HERE / "orientation_entropy_counterexample.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
