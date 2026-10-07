#!/usr/bin/env python3
"""Exact l-infinity exchange failure with all coordinate auxiliaries positive."""
from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
F = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0],
    [-1, 0, 0, 0, -1, 0],
    [1, 0, 0, 0, -1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, -1, 1, 0, 0],
]
N = 6
TAMP = Fraction(1, 100)


def det(a):
    k = len(a)
    if k == 0:
        return 1
    total = 0
    for p in permutations(range(k)):
        inv = sum(p[i] > p[j]
                  for i in range(k) for j in range(i + 1, k))
        term = -1 if inv % 2 else 1
        for i, j in enumerate(p):
            term *= a[i][j]
        total += term
    return total


def old_linf(holes_mask):
    retained = [i for i in range(N) if not (holes_mask >> i & 1)]
    if len(retained) % 2:
        return 0
    k = len(retained) // 2
    maximum = 0
    for rows in combinations(retained, k):
        rowset = set(rows)
        cols = [j for j in retained if j not in rowset]
        value = abs(det([[F[i][j] for j in cols] for i in rows]))
        maximum = max(maximum, value)
    return maximum


def matchings(vertices):
    if not vertices:
        yield 0, 0
        return
    first = vertices[0]
    for union, size in matchings(vertices[1:]):
        yield union, size
    for pos, other in enumerate(vertices[1:]):
        remaining = vertices[1:pos+1] + vertices[pos+2:]
        for union, size in matchings(remaining):
            yield union | (1 << first) | (1 << other), size + 1


def lifted_linf(holes_mask):
    available = [i for i in range(N) if not (holes_mask >> i & 1)]
    return max((TAMP**size) * old_linf(holes_mask | union)
               for union, size in matchings(available))

# Zero-based masks: S={1,5}=17, T={2,6}=34, a=1.
S, T, A = 17, 34, 1
D = S ^ T
neighbors = []
for j in sorted(i + 1 for i in range(N)
                if i + 1 != A and (D >> i & 1)):
    hs = S ^ (1 << (A - 1)) ^ (1 << (j - 1))
    ht = T ^ (1 << (A - 1)) ^ (1 << (j - 1))
    neighbors.append({"j": j, "S_mask": hs, "T_mask": ht,
                      "S_linf": lifted_linf(hs),
                      "T_linf": lifted_linf(ht)})

s, t = lifted_linf(S), lifted_linf(T)
lhs = s*t
rhs = sum(row["S_linf"] * row["T_linf"] for row in neighbors)
assert max(old_linf(m) for m in range(1 << N)) == 2
assert (s, t) == (2, 2)
assert [(row["S_linf"], row["T_linf"]) for row in neighbors] == [
    (Fraction(1), Fraction(1)),
    (Fraction(1, 50), Fraction(1, 100)),
    (Fraction(1), Fraction(1)),
]
assert lhs == 4 and rhs == Fraction(10001, 5000) and lhs > rhs

result = {
    "auxiliaries": "all 15 unordered coordinate pairs in [6]",
    "activity_per_pair": "1/10000",
    "amplitude_factor_per_selected_pair": "1/100",
    "matrix_F": F,
    "S": [1, 5], "T": [2, 6], "a": 1,
    "endpoint_linf": {"S": str(s), "T": str(t)},
    "neighbors": [
        {"j": row["j"], "S_mask": row["S_mask"],
         "T_mask": row["T_mask"], "S_linf": str(row["S_linf"]),
         "T_linf": str(row["T_linf"]),
         "product": str(row["S_linf"] * row["T_linf"])}
        for row in neighbors
    ],
    "exchange": {"lhs": str(lhs), "rhs": str(rhs),
                 "strict_gap": str(lhs-rhs)},
    "matching_formula": "lifted_linf(U)=max_K t^|K| old_linf(U union V(K)), K a matching disjoint from U",
    "scope": "exact finite positive-activity counterexample"
}
(HERE / "linf_auxiliary_extension.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
