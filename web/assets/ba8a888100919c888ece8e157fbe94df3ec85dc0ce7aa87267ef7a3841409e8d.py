#!/usr/bin/env python3
"""Exact small-instance audit for the low-sector Pfaffian estimator."""

from itertools import combinations, product
import json
import random

import sympy as sp


def det(M):
    if not M:
        return sp.Integer(1)
    return sp.Matrix(M).det(method="domain-ge")


def pfaffian(M):
    n = len(M)
    if n == 0:
        return sp.Integer(1)
    if n % 2:
        return sp.Integer(0)
    total = sp.Integer(0)
    for j in range(1, n):
        rest = [[M[a][b] for b in range(n) if b not in (0, j)]
                for a in range(n) if a not in (0, j)]
        total += (-1) ** (j + 1) * M[0][j] * pfaffian(rest)
    return sp.expand(total)


def c_k_bruteforce(F, k):
    n = F.rows
    total = sp.Integer(0)
    choices = list(combinations(range(n), k))
    for I in choices:
        for J in choices:
            if set(I).isdisjoint(J):
                value = det([[F[i, j] for j in J] for i in I])
                total += sp.expand(value * sp.conjugate(value))
    return sp.simplify(total)


def pair_vectors(F):
    n = F.rows
    V = sp.zeros(n, 2 * n)
    for i in range(n):
        V[i, 2 * i] = 1
        for j in range(n):
            V[j, 2 * i + 1] = F[i, j]
    return V


def skew_for_signs(F, signs):
    n = F.rows
    A = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            A[i, j] = signs[i] * F[i, j] - signs[j] * F[j, i]
    assert A.T == -A
    return A


def sqrt_det_coefficient(A, k, t):
    B = A.conjugate().T * A
    d = [sp.Integer(1)]
    for degree in range(1, k + 1):
        coeff = sp.Integer(0)
        for rows in combinations(range(A.rows), degree):
            coeff += det([[B[i, j] for j in rows] for i in rows])
        d.append(sp.simplify(coeff))
    q = [sp.Integer(1)]
    for m in range(1, k + 1):
        q.append(sp.simplify((d[m] - sum(q[j] * q[m - j]
                                         for j in range(1, m))) / 2))
    return q[k]


def direct_principal_pfaffian_norm(A, k):
    n = A.rows
    total = sp.Integer(0)
    for R in combinations(range(n), 2 * k):
        sub = [[A[i, j] for j in R] for i in R]
        value = pfaffian(sub)
        total += sp.expand(value * sp.conjugate(value))
    return sp.simplify(total)


def fixture(n, seed):
    rng = random.Random(seed)
    entries = []
    for _ in range(n * n):
        re = rng.randrange(-2, 3)
        im = rng.randrange(-2, 3)
        den = rng.choice((1, 2, 3))
        entries.append(sp.Rational(re, den) + sp.I * sp.Rational(im, den))
    return sp.Matrix(n, n, entries)


def audit(n, seed):
    F = fixture(n, seed)
    t = sp.symbols("t")
    max_c = n // 2
    exact = {k: c_k_bruteforce(F, k) for k in range(max_c + 1)}
    sign_sums = {k: sp.Integer(0) for k in range(max_c + 1)}
    sign_count = 0
    for signs in product((-1, 1), repeat=n):
        A = skew_for_signs(F, signs)
        sign_count += 1
        for k in range(max_c + 1):
            q = sqrt_det_coefficient(A, k, t)
            direct = direct_principal_pfaffian_norm(A, k)
            assert sp.simplify(q - direct) == 0, ("square-root/Pfaffian", n, k, signs)
            assert sp.simplify(q - sp.conjugate(q)) == 0
            assert q >= 0
            sign_sums[k] += q
    for k in range(max_c + 1):
        mean = sp.simplify(sign_sums[k] / sign_count)
        assert sp.simplify(mean - exact[k]) == 0, ("Rademacher mean", n, k, mean, exact[k])
    return {
        "n": n,
        "seed": seed,
        "sign_vectors": sign_count,
        "c_k": {str(k): str(exact[k]) for k in range(max_c + 1)},
        "result": "PASS",
    }


if __name__ == "__main__":
    results = [audit(2, 2101), audit(4, 2102)]
    print(json.dumps({"claim_scope": "finite exact identity checks only", "fixtures": results}, indent=2))
