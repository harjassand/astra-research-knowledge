#!/usr/bin/env python3
"""Exact 4-site hard-BCS equality with two active moves and non-pair support."""

from itertools import combinations, permutations
import json


F = (
    (0, 1, 1, 0),
    (0, 0, 0, 0),
    (0, 0, 0, 0),
    (0, -1, 1, 0),
)
E = frozenset(range(4))


def det(M):
    n = len(M)
    if n == 0:
        return 1
    total = 0
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = 1
        for i, j in enumerate(p):
            term *= M[i][j]
        total += (-1 if inversions % 2 else 1) * term
    return total


def z_partition(R):
    R = tuple(sorted(R))
    assert len(R) % 2 == 0
    k = len(R) // 2
    total = 0
    for I in combinations(R, k):
        J = tuple(i for i in R if i not in I)
        block = tuple(tuple(F[i][j] for j in J) for i in I)
        total += det(block) ** 2
    return total


def f(holes):
    holes = frozenset(holes)
    return z_partition(E - holes) if len(holes) % 2 == 0 else 0


coefficients = {}
for size in (0, 2, 4):
    for U in combinations(range(4), size):
        coefficients["".join(str(i + 1) for i in U) or "empty"] = f(U)

S, T, a = E, frozenset(), 0
terms = {}
for j in sorted(E - {a}):
    terms[str(j + 1)] = {
        "A": f({a, j}),
        "B": f(S ^ {a, j}),
        "product": f({a, j}) * f(S ^ {a, j}),
    }

assert coefficients == {
    "empty": 4,
    "12": 1,
    "13": 1,
    "14": 0,
    "23": 0,
    "24": 1,
    "34": 1,
    "1234": 1,
}
assert terms == {
    "2": {"A": 1, "B": 1, "product": 1},
    "3": {"A": 1, "B": 1, "product": 1},
    "4": {"A": 0, "B": 0, "product": 0},
}

print(json.dumps({
    "status": "EXACT_ASSERTIONS_PASSED",
    "F_1_based_rows": [list(row) for row in F],
    "hole_coefficients_1_based": coefficients,
    "S": [1, 2, 3, 4],
    "T": [],
    "a": 1,
    "exchange_terms": terms,
    "exchange_lhs": 2,
    "exchange_rhs": 2,
    "balanced_weights": {"w2": "1", "w3": "1", "w4": "1"},
    "balanced_slice": "4 + 2 z + 2 z^2 + z^3 = (z+2)(z^2+2)",
    "support": ["empty", "12", "13", "24", "34", "1234"],
    "scope": "Exact finite hard-BCS equality fixture; not a general classification.",
}, indent=2))
