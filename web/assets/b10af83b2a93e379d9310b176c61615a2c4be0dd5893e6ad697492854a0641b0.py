#!/usr/bin/env python3
"""Exact counterexample to diagonal-only counting via hard-projected c_2(F)."""
from itertools import combinations

n = 4
F = [[0, 1, 1, 1],
     [-1, 0, 1, 1],
     [-1, -1, 0, 1],
     [-1, -1, -1, 0]]

c2 = 0
same_matching_terms = 0
cross_terms = 0
rows = []
for I in combinations(range(n), 2):
    J = tuple(j for j in range(n) if j not in I)
    # det F[I,J] = a - b, with the two bijection/perfect-matching terms a,b.
    a = F[I[0]][J[0]] * F[I[1]][J[1]]
    b = F[I[0]][J[1]] * F[I[1]][J[0]]
    det = a - b
    c2 += det * det
    same_matching_terms += a * a + b * b
    cross_terms += -2 * a * b
    rows.append({"I": list(I), "J": list(J), "term_a": a,
                 "term_b": b, "det": det, "square": det * det,
                 "diagonal": a * a + b * b, "cross": -2 * a * b})

perfect_matchings_K4 = 3
orientation_diagonal_prediction = (2 ** 2) * perfect_matchings_K4
assert c2 == 8
assert same_matching_terms == 12
assert cross_terms == -4
assert c2 == same_matching_terms + cross_terms
assert c2 != orientation_diagonal_prediction

print({"c2": c2, "diagonal_matching_terms": same_matching_terms,
       "off_diagonal_interference": cross_terms,
       "K4_perfect_matchings": perfect_matchings_K4,
       "2^k_times_perfect_matchings": orientation_diagonal_prediction,
       "cuts": rows})
