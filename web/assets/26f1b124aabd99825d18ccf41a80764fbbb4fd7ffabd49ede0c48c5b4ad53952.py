#!/usr/bin/env python3
"""Exact 4-site hard-BCS witness for equality with a one-sided exchange zero."""

from fractions import Fraction
from itertools import combinations, permutations
import json


F = (
    (0, 1, 0, 0),
    (0, 0, 0, 1),
    (0, 0, 0, 1),
    (0, 0, 0, 0),
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
    k = len(R) // 2
    assert len(R) % 2 == 0
    total = 0
    for I in combinations(R, k):
        J = tuple(i for i in R if i not in I)
        block = tuple(tuple(F[i][j] for j in J) for i in I)
        total += det(block) ** 2
    return total


def f(holes):
    return z_partition(E - frozenset(holes)) if len(holes) % 2 == 0 else 0


coefficients = {}
for size in (0, 2, 4):
    for U in combinations(range(4), size):
        coefficients["".join(str(i + 1) for i in U) or "empty"] = f(U)

S = E
T = frozenset()
a = 0
terms = {}
for j in sorted(S ^ T ^ {a}):
    if j == a:
        continue
    S2 = S ^ {a, j}
    T2 = T ^ {a, j}
    terms[str(j + 1)] = {"A": f(T2), "B": f(S2), "product": f(T2) * f(S2)}

assert coefficients == {
    "empty": 1,
    "12": 1,
    "13": 1,
    "14": 0,
    "23": 0,
    "24": 0,
    "34": 1,
    "1234": 1,
}
assert terms["2"] == {"A": 1, "B": 1, "product": 1}
assert terms["3"] == {"A": 1, "B": 0, "product": 0}
assert terms["4"] == {"A": 0, "B": 0, "product": 0}

epsilon = Fraction(1, 1000)
slice_coefficients = [Fraction(1), 1 + epsilon, Fraction(1), Fraction(1)]
endpoint_ratio = slice_coefficients[1] * slice_coefficients[2] / (
    slice_coefficients[0] * slice_coefficients[3]
)
assert endpoint_ratio == Fraction(1001, 1000)

print(json.dumps({
    "status": "EXACT_ASSERTIONS_PASSED",
    "F_1_based_rows": [list(row) for row in F],
    "hole_coefficients_1_based": coefficients,
    "S": [1, 2, 3, 4],
    "T": [],
    "a": 1,
    "exchange_terms": terms,
    "exchange_lhs": 1,
    "exchange_rhs": 1,
    "one_sided_case": "j=3 has A=1 and B=0",
    "weights": {"w2": "1", "w3": "epsilon", "w4": "1/epsilon"},
    "slice": "1 + (1+epsilon) z + z^2 + z^3",
    "epsilon_fixture": "1/1000",
    "endpoint_ratio": str(endpoint_ratio),
    "limit_slice": "(1+z)(1+z^2)",
    "scope": "Exact finite hard-BCS coefficients and equality witness; not a classification theorem.",
}, indent=2))
