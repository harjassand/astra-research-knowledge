#!/usr/bin/env python3
"""Exact integer check of the skew-K4 determinant-interference witness."""

from itertools import combinations
import json
from pathlib import Path


def det2(m):
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


A = [[0 if i == j else (1 if i < j else -1) for j in range(4)] for i in range(4)]
records = []
target = 0
diagonal = 0
cross = 0
for rows in combinations(range(4), 2):
    cols = tuple(i for i in range(4) if i not in rows)
    m = [[A[i][j] for j in cols] for i in rows]
    x = m[0][0] * m[1][1]
    y = m[0][1] * m[1][0]
    value = det2(m)
    term_diagonal = x * x + y * y
    term_cross = -2 * x * y
    assert value * value == term_diagonal + term_cross
    records.append({
        "rows_1based": [i + 1 for i in rows],
        "cols_1based": [j + 1 for j in cols],
        "determinant": value,
        "squared_determinant": value * value,
        "diagonal_monomial_sum": term_diagonal,
        "interference": term_cross,
    })
    target += value * value
    diagonal += term_diagonal
    cross += term_cross

# Each of the three perfect matchings of K4 appears under four choices of
# which endpoint of each edge lies in the row set: 3 * 2^2 = 12.
assert [r["determinant"] for r in records] == [0, 2, 0, 0, 2, 0]
assert target == 8
assert diagonal == 12
assert cross == -4
assert target == diagonal + cross

receipt = {
    "status": "PASS",
    "matrix": A,
    "k": 2,
    "minor_determinants_in_lex_row_order": [r["determinant"] for r in records],
    "Z_k": target,
    "positive_diagonal_monomial_total": diagonal,
    "signed_interference_total": cross,
    "identity": "8 = 12 + (-4)",
    "scope": "Exact counterexample to dropping determinant cross terms; not a no-go theorem for all AP reductions.",
    "minors": records,
}
Path(__file__).with_name("k4_interference.json").write_text(
    json.dumps(receipt, indent=2) + "\n"
)
print(json.dumps(receipt, indent=2))
