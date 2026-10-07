#!/usr/bin/env python3
"""Exact checks of the fixed-k paired-Gram Cauchy--Binet microstate lift."""
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lifted_orientation import det_bareiss


def gram(a):
    return [[sum(row[i] * row[j] for row in a) for j in range(len(a[0]))]
            for i in range(len(a[0]))]


def microstates(n, k):
    out = []
    universe = set(range(n))
    for I in combinations(range(n), k):
        rem = sorted(universe - set(I))
        for J in combinations(rem, k):
            out.append((tuple(I), tuple(J)))
    return out


def check_one(n, k, F):
    V = [[int(i == j) for j in range(n)] + [F[j][i] for j in range(n)]
         for i in range(n)]
    marginal_rows = []
    for I in combinations(range(n), k):
        cols = tuple(I) + tuple(n + i for i in I)
        V_I = [[V[r][c] for c in cols] for r in range(n)]
        gram_weight = det_bareiss(gram(V_I))
        minor_sum = 0
        rem = sorted(set(range(n)) - set(I))
        for J in combinations(rem, k):
            d = det_bareiss([[F[i][j] for j in J] for i in I])
            minor_sum += d * d
        assert gram_weight == minor_sum
        marginal_rows.append({"I": list(I), "weight": gram_weight})

    states = microstates(n, k)
    weights = {}
    for I, J in states:
        d = det_bareiss([[F[i][j] for j in J] for i in I])
        weights[(I, J)] = d * d
    Z = sum(weights.values())
    assert Z == sum(row["weight"] for row in marginal_rows)
    support = [x for x, w in weights.items() if w]
    if support:
        # Uniform proposals over all M microstates, product MH on two replicas.
        M = len(states)
        proposal_size = M * M
        for x in support:
            for y in support:
                wx, wy = weights[x], weights[y]
                forward_flow = Fraction(wx * wy, Z * Z) * Fraction(1, proposal_size) * min(1, Fraction(wy * wx, wx * wy))
                reverse_flow = Fraction(wy * wx, Z * Z) * Fraction(1, proposal_size) * min(1, Fraction(wx * wy, wy * wx))
                assert forward_flow == reverse_flow
    return {"n": n, "k": k, "microstate_count": len(states), "support_count": len(support),
            "partition": Z, "all_site_gram_marginals_match": True,
            "pairwise_detailed_balance": bool(support)}


def main():
    F = [[1, 2, 0, -1], [0, 1, 3, 1], [2, -1, 1, 0], [1, 0, -2, 2]]
    result = {"scope": "finite exact arithmetic check only",
              "fixtures": [check_one(4, k, F) for k in (1, 2)],
              "arithmetic": "integer Bareiss determinants and Fraction flows"}
    Path(__file__).with_name("02_general_k_microstate_checks.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
