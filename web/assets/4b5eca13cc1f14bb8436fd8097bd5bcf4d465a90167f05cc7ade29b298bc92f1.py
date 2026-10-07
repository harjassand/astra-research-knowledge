#!/usr/bin/env python3
"""Exact audit of the apolar/determinant encoding for c_k(F)."""

from itertools import combinations
import json
import random

import sympy as sp


def abs_square(z):
    return sp.expand(z * sp.conjugate(z))


def determinant(M):
    return sp.Matrix(M).det(method="domain-ge")


def build_pair_matrix(F):
    n = F.rows
    V = sp.zeros(n, 2 * n)
    for i in range(n):
        V[i, 2 * i] = 1
        for j in range(n):
            V[j, 2 * i + 1] = F[i, j]
    return V


def build_augmented(V):
    n = V.rows
    I = sp.eye(n)
    return V.row_join(I)


def c_k(F, k):
    n = F.rows
    sets = list(combinations(range(n), k))
    total = sp.Integer(0)
    for I in sets:
        for J in sets:
            if set(I).isdisjoint(J):
                d = determinant([[F[i, j] for j in J] for i in I])
                total += abs_square(d)
    return sp.simplify(total)


def apolar_sum_from_minors(F, k):
    """Compute <det(W diag(y,y,z) W*), e_k(y^2)e_{n-2k}(z)> directly."""
    n = F.rows
    V = build_pair_matrix(F)
    W = build_augmented(V)
    pair_sets = list(combinations(range(n), k))
    filler_sets = list(combinations(range(n), n - 2 * k))
    total = sp.Integer(0)
    for S in pair_sets:
        pair_cols = [col for i in S for col in (2 * i, 2 * i + 1)]
        for Q in filler_sets:
            cols = pair_cols + [2 * n + j for j in Q]
            d = determinant(W[:, cols])
            # In the apolar pairing each selected y_i has exponent two,
            # contributing 2!; filler variables have exponent one.
            total += (2 ** k) * abs_square(d)
    return sp.simplify(total)


def random_matrix(n, rng):
    values = []
    for _ in range(n * n):
        re = sp.Rational(rng.randrange(-2, 3), rng.choice((1, 2, 3)))
        im = sp.Rational(rng.randrange(-2, 3), rng.choice((1, 2, 3)))
        values.append(re + sp.I * im)
    return sp.Matrix(n, n, values)


def run():
    rng = random.Random(20261007)
    out = []
    for n in (2, 3, 4):
        for seed in range(3):
            F = random_matrix(n, rng)
            for k in range(n // 2 + 1):
                direct = c_k(F, k)
                apolar = apolar_sum_from_minors(F, k)
                assert sp.simplify(apolar - (2 ** k) * direct) == 0
                out.append({"n": n, "seed": seed, "k": k,
                            "c_k": str(direct),
                            "apolar_value": str(apolar),
                            "pass": True})
    return out


if __name__ == "__main__":
    checks = run()
    print(json.dumps({"scope": "finite exact identity check; symbolic differentiation algorithm not implemented",
                      "checks": len(checks), "instances": checks}, indent=2))
