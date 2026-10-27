#!/usr/bin/env python3
"""Independent exact multivariate-Hermite check of the full-source gauge.

Hermite polynomials are unnormalized, so differentiation, creation, inner
products and all coefficients are rational. No symbolic package is needed.
"""
from fractions import Fraction as F
from math import factorial
import random

D = 2
VARS = 2 * D


def add(*ps):
    out = {}
    for p in ps:
        for key, value in p.items():
            out[key] = out.get(key, F(0)) + value
    return {key: value for key, value in out.items() if value}


def scale(p, c):
    return {key: value * c for key, value in p.items() if value * c}


def deriv(p, j):
    out = {}
    for key, value in p.items():
        if key[j]:
            other = list(key)
            other[j] -= 1
            other = tuple(other)
            out[other] = out.get(other, F(0)) + value * key[j]
    return out


def delta(p, j):
    out = {}
    for key, value in p.items():
        other = list(key)
        other[j] += 1
        other = tuple(other)
        out[other] = out.get(other, F(0)) + value
    return out


def norm2(p):
    return sum(value * value *
               factorial(key[0]) * factorial(key[1]) *
               factorial(key[2]) * factorial(key[3])
               for key, value in p.items())


def norm_slot(items):
    return sum(norm2(p) for p in items)


def check(n, m, seed):
    rng = random.Random(seed)
    r = [[{} for _ in range(D)] for _ in range(D)]
    for i in range(D):
        for j in range(i, D):
            p = {(g, n-g, z, m-z): F(rng.randint(-3, 3))
                 for g in range(n+1) for z in range(m+1)}
            p = {key: value for key, value in p.items() if value}
            r[i][j] = p
            r[j][i] = p
    total = n+m
    dr = [add(*(delta(r[i][j], D+j) for j in range(D)))
          for i in range(D)]
    s = add(*(delta(dr[i], D+i) for i in range(D)))
    u = [scale(deriv(s, D+i), -F(1, (m+2)*(total+2)))
         for i in range(D)]
    w = [add(dr[i], scale(deriv(s, D+i), -F(1, m+2)))
         for i in range(D)]
    b = [[scale(add(deriv(w[i], D+j), scale(deriv(w[j], D+i), -1)),
                F(1, m+2)) for j in range(D)] for i in range(D)]
    jg = [[scale(deriv(u[i], j), -1) for j in range(D)] for i in range(D)]
    jz = [[add(scale(r[i][j], -1), scale(deriv(u[j], D+i), -1), b[i][j])
           for j in range(D)] for i in range(D)]
    for i in range(D):
        div = add(*(delta(jg[i][j], j) for j in range(D)),
                  *(delta(jz[i][j], D+j) for j in range(D)))
        assert div == u[i], (n, m, seed, "divergence", i)
        for j in range(D):
            sym = scale(add(jz[i][j], deriv(u[j], D+i),
                            jz[j][i], deriv(u[i], D+j)), F(1, 2))
            assert add(sym, r[i][j]) == {}, (n, m, seed, "symmetry", i, j)
    r2 = norm_slot([p for row in r for p in row])
    j2 = norm_slot([p for row in jg+jz for p in row])
    dr2 = norm_slot(dr)
    s2 = norm2(s)
    formula = (r2 + F(2, m+2)*dr2
               - (F(2, (m+2)**2) +
                  F(total+3, (m+2)*(total+2)**2))*s2)
    assert j2 == formula, (n, m, seed, "exact norm identity")
    assert j2 <= 3*r2, (n, m, seed, "kernel bound")
    ug2 = norm_slot([deriv(u[i], j) for i in range(D) for j in range(D)])
    du2 = norm_slot([deriv(u[i], j) for i in range(D) for j in range(VARS)])
    assert 4*ug2 <= r2, (n, m, seed, "source gradient")
    assert du2 <= r2, (n, m, seed, "full gradient")
    assert 4*norm_slot(u) <= r2, (n, m, seed, "vector")
    return float(j2/r2) if r2 else 0


if __name__ == "__main__":
    ratios = [check(n, m, seed)
              for n in range(6) for m in range(6) for seed in range(5)]
    print(f"Passed {len(ratios)} exact d=2 bichaos checks.")
    print("Checked divergence, symmetric inverse, exact norm identity,")
    print("and all degree-independent u, D_Gu, Du, J norm inequalities.")
    print(f"Largest observed ||J||²/||R||²: {max(ratios):.12f}")
