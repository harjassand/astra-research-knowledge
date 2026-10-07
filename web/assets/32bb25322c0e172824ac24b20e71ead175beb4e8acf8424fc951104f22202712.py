#!/usr/bin/env python3
"""Exact same-hole-polynomial, different-orientation-entropy certificate."""
from itertools import combinations, permutations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
MATRICES = {
    "F1": [
        [0, 0, -1, 1],
        [-1, 1, -1, 1],
        [0, -1, 1, 0],
        [-1, 0, 1, -1],
    ],
    "F2": [
        [-1, 0, -1, 1],
        [-1, 1, -1, 0],
        [0, 1, -1, -1],
        [-1, 1, 0, 1],
    ],
}
N = 4
EVEN_HOLES = [m for m in range(1 << N) if m.bit_count() % 2 == 0]


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


def coefficient_data(F, holes_mask):
    retained = [i for i in range(N) if not (holes_mask >> i & 1)]
    if len(retained) % 2:
        return {"z": 0, "ell": 0, "orientations": []}
    k = len(retained) // 2
    z = ell = 0
    orientations = []
    for rows in combinations(retained, k):
        rowset = set(rows)
        cols = tuple(i for i in retained if i not in rowset)
        value = det([[F[i][j] for j in cols] for i in rows])
        z += value * value
        ell += abs(value)
        if value:
            orientations.append({"I_rows_1based": [i + 1 for i in rows],
                                 "J_cols_1based": [j + 1 for j in cols],
                                 "det": value})
    return {"z": z, "ell": ell, "orientations": orientations}


DATA = {name: {m: coefficient_data(F, m) for m in range(1 << N)}
        for name, F in MATRICES.items()}
assert [DATA["F1"][m]["z"] for m in range(1 << N)] == \
       [DATA["F2"][m]["z"] for m in range(1 << N)]
assert [DATA["F1"][m]["z"] for m in EVEN_HOLES] == [6, 1, 1, 2, 2, 1, 1, 1]
assert DATA["F1"][0]["ell"] == 4
assert DATA["F2"][0]["ell"] == 6
assert DATA["F1"][0]["orientations"] == [
    {"I_rows_1based": [1, 3], "J_cols_1based": [2, 4], "det": 1},
    {"I_rows_1based": [2, 4], "J_cols_1based": [1, 3], "det": -2},
    {"I_rows_1based": [3, 4], "J_cols_1based": [1, 2], "det": -1},
]
assert len(DATA["F2"][0]["orientations"]) == 6

result = {
    "F1": MATRICES["F1"],
    "F2": MATRICES["F2"],
    "same_z_for_every_hole_mask": True,
    "coefficient_order": "hole bitmasks 0..15; odd masks are zero",
    "even_hole_z_vector": [DATA["F1"][m]["z"] for m in EVEN_HOLES],
    "even_hole_l1_vectors": {
        name: [DATA[name][m]["ell"] for m in EVEN_HOLES]
        for name in MATRICES
    },
    "empty_hole_orientations": {
        name: DATA[name][0]["orientations"] for name in MATRICES
    },
    "tensor_consequence": {
        "block_diagonal_q_blocks": "z functions remain identical by factorization",
        "ell_empty_F1_q": "4^q",
        "ell_empty_F2_q": "6^q",
        "ratio": "(3/2)^q",
        "H_half_F1_q": "q*log(8/3)",
        "H_half_F2_q": "q*log(6)",
        "entropy_difference": "q*log(9/4)"
    },
    "scope": "exact n=4 certificate plus proved block factorization; no algorithmic claim"
}
(HERE / "aggregate_entropy_nonidentifiability.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
