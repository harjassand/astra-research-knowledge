#!/usr/bin/env python3
"""Exact audit of the near-top Jacobi transform and a false low-hole shortcut."""

from itertools import combinations
import json
import random

import sympy as sp


def minor(M, rows, cols):
    if not rows:
        return sp.Integer(1)
    return sp.Matrix([[M[i, j] for j in cols] for i in rows]).det(method="domain-ge")


def c_disjoint(F, k):
    n = F.rows
    sets = list(combinations(range(n), k))
    total = sp.Integer(0)
    for I in sets:
        for J in sets:
            if set(I).isdisjoint(J):
                d = minor(F, I, J)
                total += sp.expand(d * sp.conjugate(d))
    return sp.simplify(total)


def dual_overlap(G, k):
    """Sum over |K|=|L|=n-k, K union L=V, |K intersect L|=n-2k."""
    n = G.rows
    q, h = n - k, n - 2 * k
    sets = list(combinations(range(n), q))
    total = sp.Integer(0)
    for K in sets:
        for L in sets:
            if len(set(K) | set(L)) == n and len(set(K) & set(L)) == h:
                d = minor(G, K, L)
                total += sp.expand(d * sp.conjugate(d))
    return sp.simplify(total)


def random_invertible(n, rng):
    while True:
        M = sp.Matrix(n, n,
                      [sp.Rational(rng.randrange(-2, 3), rng.choice((1, 2, 3)))
                       for _ in range(n * n)])
        if M.det() != 0:
            return M


def verify_jacobi_family():
    rng = random.Random(20261007)
    cases = []
    for n in range(2, 6):
        for trial in range(5):
            F = random_invertible(n, rng)
            G = F.inv()
            for k in range(n // 2 + 1):
                lhs = c_disjoint(F, k)
                rhs = sp.simplify((F.det() * sp.conjugate(F.det())) * dual_overlap(G, k))
                assert sp.simplify(lhs - rhs) == 0, (n, trial, k, lhs, rhs)
                cases.append({"n": n, "trial": trial, "k": k, "c_k": str(lhs),
                              "dual_overlap": str(dual_overlap(G, k)), "pass": True})
    return cases


def counterexample_to_naive_disjoint_dual():
    # For k=1, n=4, the Jacobi complement has 3x3 minors with 2 common
    # indices. Replacing those by disjoint 2x2 minors is false.
    n, k = 4, 1
    F = sp.eye(n)
    F[0, 1] = 2
    G = F.inv()
    h = n - 2 * k
    target = sp.simplify((F.det() * sp.conjugate(F.det())) * dual_overlap(G, k))
    naive = c_disjoint(G, h)
    direct = c_disjoint(F, k)
    assert direct == 4
    assert target == direct
    assert naive == 0
    return {"F": str(F.tolist()), "F_inverse": str(G.tolist()), "n": n, "k": k,
            "h": h, "c_k_F": str(direct), "jacobi_overlap_expression": str(target),
            "naive_c_h_inverse": str(naive), "result": "NAIVE_DUAL_REFUTED"}


if __name__ == "__main__":
    cases = verify_jacobi_family()
    counterexample = counterexample_to_naive_disjoint_dual()
    print(json.dumps({"scope": "exact finite Jacobi identity audit only",
                      "random_invertible_cases": len(cases),
                      "cases": cases,
                      "naive_shortcut_counterexample": counterexample}, indent=2))
