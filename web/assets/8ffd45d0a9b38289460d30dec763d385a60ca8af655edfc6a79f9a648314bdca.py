#!/usr/bin/env python3
"""Exact certificates showing p=2 is the only possible universal l_p exchange exponent."""
from itertools import combinations, permutations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASES = {
    "p_less_than_2": {
        "F": [
            [0, -1, -1, -1, 0, 0],
            [0,  0,  0,  0, 0, 0],
            [1,  0,  0,  0, 0, 0],
            [0,  0,  0,  0, 0, 0],
            [0,  0, -1, -1, 0, 0],
            [0, -1, -1,  0, 0, 0],
        ],
        "S": [], "T": [2, 4, 5, 6], "a": 2,
        "expected_abs_amplitudes": {
            "S": [1, 1], "T": [1, 1],
            "j=4:S": [], "j=4:T": [],
            "j=5:S": [1], "j=5:T": [1],
            "j=6:S": [1], "j=6:T": [1],
        },
        "p_condition": "0<p<2",
        "lhs": "2^(2/p)", "rhs": "2",
    },
    "p_greater_than_2": {
        "F": [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [-1, 0, 0, 0, -1, 0],
            [1, 0, 0, 0, -1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, -1, 1, 0, 0],
        ],
        "S": [1, 5], "T": [2, 6], "a": 1,
        "expected_abs_amplitudes": {
            "S": [2], "T": [2],
            "j=2:S": [1, 1], "j=2:T": [1, 1],
            "j=5:S": [], "j=5:T": [],
            "j=6:S": [1, 1], "j=6:T": [1, 1],
        },
        "p_condition": "2<p<=infinity",
        "lhs": "4", "rhs": "2^(1+2/p)",
    },
}
N = 6


def det(a):
    k = len(a)
    if k == 0:
        return 1
    total = 0
    for p in permutations(range(k)):
        inversions = sum(p[i] > p[j]
                         for i in range(k) for j in range(i + 1, k))
        term = -1 if inversions % 2 else 1
        for i, j in enumerate(p):
            term *= a[i][j]
        total += term
    return total


def orientations(F, holes):
    holes = set(holes)
    retained = [i for i in range(N) if i + 1 not in holes]
    if len(retained) % 2:
        return []
    k = len(retained) // 2
    out = []
    for rows in combinations(retained, k):
        rowset = set(rows)
        cols = [j for j in retained if j not in rowset]
        value = det([[F[i][j] for j in cols] for i in rows])
        if value:
            out.append({"I_rows_1based": [i + 1 for i in rows],
                        "J_cols_1based": [j + 1 for j in cols],
                        "det": value})
    return out


def toggle(U, i, j):
    out = set(U)
    for x in (i, j):
        if x in out:
            out.remove(x)
        else:
            out.add(x)
    return sorted(out)


results = {}
for name, case in CASES.items():
    F, S, T, a = case["F"], case["S"], case["T"], case["a"]
    D = set(S) ^ set(T)
    rows = {
        "S": orientations(F, S),
        "T": orientations(F, T),
    }
    for j in sorted(D - {a}):
        rows[f"j={j}:S"] = orientations(F, toggle(S, a, j))
        rows[f"j={j}:T"] = orientations(F, toggle(T, a, j))
    abs_vectors = {key: sorted(abs(o["det"]) for o in vals)
                   for key, vals in rows.items()}
    assert abs_vectors == case["expected_abs_amplitudes"]
    results[name] = {
        "F": F, "S": S, "T": T, "a": a,
        "orientation_minors": rows,
        "absolute_amplitude_vectors": abs_vectors,
        "symbolic_p_exchange": {"range": case["p_condition"],
                                 "lhs": case["lhs"], "rhs": case["rhs"]},
    }

result = {
    "claim": "For every finite p>0 other than p=2, the universal l_p orientation exchange fails on one of two exact n=6 integer instances.",
    "cases": results,
    "conclusion": {
        "p_less_than_2": "2^(2/p)>2",
        "p_greater_than_2": "2^(1+2/p)<4",
        "p_equals_2": "both examples attain equality; universal p=2 inequality is the aggregate square-root exchange"
    },
    "scope": "exact counterexamples for p!=2; no claim about other nonlinear orientation functionals"
}
(HERE / "lp_orientation_exchange_boundary.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
