#!/usr/bin/env python3
"""Exact l1-orientation exchange check after all 15 coordinate-pair auxiliaries.

Every auxiliary edge has activity w=t^2, so a selected edge contributes t to
an orientation amplitude. Two selected auxiliary edges may not share a
coordinate: the corresponding determinant has repeated coordinate columns.
"""
from fractions import Fraction
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
T = frozenset({2, 4, 5, 6})
S = frozenset()
A = 2
TAMP = Fraction(1, 100)  # sqrt(activity); activity w=10^-4 for each edge


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


def base_coefficients(holes):
    retained = [i for i in range(N) if i + 1 not in holes]
    if len(retained) % 2:
        return 0, 0
    k = len(retained) // 2
    l1 = z = 0
    for rows in combinations(retained, k):
        rowset = set(rows)
        cols = [i for i in retained if i not in rowset]
        d = det([[F[i][j] for j in cols] for i in rows])
        l1 += abs(d)
        z += d*d
    return l1, z


def matching_terms(vertices):
    """Yield the vertex union and size of every matching on vertices."""
    vertices = tuple(vertices)
    if not vertices:
        yield 0, 0
        return
    first = vertices[0]
    # First vertex is not covered by an auxiliary pair.
    for union, size in matching_terms(vertices[1:]):
        yield union, size
    # First vertex is paired with one later vertex.
    for pos, other in enumerate(vertices[1:]):
        remaining = vertices[1:pos+1] + vertices[pos+2:]
        for union, size in matching_terms(remaining):
            yield union | (1 << first) | (1 << other), size + 1


def extended_coefficients(holes):
    holes = frozenset(holes)
    available = [i for i in range(N) if i + 1 not in holes]
    l1 = Fraction(0)
    z = Fraction(0)
    for union, size in matching_terms(available):
        extra_holes = {i + 1 for i in range(N) if union >> i & 1}
        old_l1, old_z = base_coefficients(holes | extra_holes)
        l1 += TAMP**size * old_l1
        z += (TAMP*TAMP)**size * old_z
    return l1, z


# S, T and exchanged endpoints for a=2, j=4,5,6.
neighbors = []
for j in sorted(T - {A}):
    hs = S ^ {A, j}
    ht = T ^ {A, j}
    neighbors.append({"j": j,
                      "S_exchange": {"holes": sorted(hs),
                                     "ell": extended_coefficients(hs)[0]},
                      "T_exchange": {"holes": sorted(ht),
                                     "ell": extended_coefficients(ht)[0]}})

ell_s, z_s = extended_coefficients(S)
ell_t, z_t = extended_coefficients(T)
lhs = ell_s * ell_t
rhs = sum(nb["S_exchange"]["ell"] * nb["T_exchange"]["ell"]
          for nb in neighbors)

# The exact fractions verify the positive-activity counterexample.
assert lhs > rhs

result = {
    "all_coordinate_auxiliaries": {
        "edge_set": "all 15 unordered pairs of [6]",
        "activity_per_edge": "1/10000",
        "amplitude_factor_per_selected_edge": "1/100",
        "selected_edges_in_a_basis_must_be_a_matching": True
    },
    "endpoint_ell": {"S_empty": str(ell_s), "T_2456": str(ell_t)},
    "endpoint_z": {"S_empty": str(z_s), "T_2456": str(z_t)},
    "neighbors": [
        {"j": nb["j"],
         "S_exchange": {"holes": nb["S_exchange"]["holes"],
                         "ell": str(nb["S_exchange"]["ell"])},
         "T_exchange": {"holes": nb["T_exchange"]["holes"],
                         "ell": str(nb["T_exchange"]["ell"])},
         "product": str(nb["S_exchange"]["ell"] *
                        nb["T_exchange"]["ell"])}
        for nb in neighbors
    ],
    "l1_exchange": {"left": str(lhs), "right": str(rhs),
                    "difference": str(lhs-rhs),
                    "ratio_decimal": float(lhs/rhs)},
    "formula": "ell_w(U)=sum_{matching K subset [6]\\U} t^|K| ell_0(U union V(K)); z_w(U)=sum_K t^(2|K|) z_0(U union V(K))",
    "scope": "exact finite check; positive auxiliary activity at every coordinate pair; no algorithmic consequence"
}
(HERE / "orientation_entropy_auxiliary_extension.json").write_text(
    json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
