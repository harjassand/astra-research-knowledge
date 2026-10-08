#!/usr/bin/env python3
"""Exact rational fixture checks for the cycle-two mixing lower bound."""
from fractions import Fraction as F
import json


RHO = F(1, 2)
A0 = F(1, 8)
S = F(3, 4)
C = ((F(1), F(-1)), (F(-1), F(1)))


def zeros(n, p):
    return [[F(0) for _ in range(p)] for _ in range(n)]


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def matadd(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]


def scale(c, a):
    return [[c * x for x in row] for row in a]


def transpose(a):
    return [list(col) for col in zip(*a)]


def tv_rows(a, b):
    return sum((abs(x - y) for x, y in zip(a, b)), F(0)) / 2


def make_theta(m):
    # All corners, with a non-symmetric checkerboard of signs.
    return [[A0 if (i + 2 * j) % 2 == 0 else -A0 for j in range(m)]
            for i in range(m)]


def build(m, theta, s=S):
    k = 2 * m
    a = zeros(k, k)
    for i in range(m):
        for j in range(m):
            for u in range(2):
                for v in range(2):
                    a[2 * i + u][2 * j + v] = theta[i][j] * C[u][v]
    eye = [[F(int(i == j)) for j in range(k)] for i in range(k)]
    ones = [[F(1) for _ in range(k)] for _ in range(k)]
    p0 = matadd(scale(RHO, eye), scale((1 - RHO) / k, ones))
    p = matadd(p0, scale(F(1, k), a))
    e = matadd(scale(s, eye), scale((1 - s) / k, ones))
    q = matmul(matmul(e, p), e)
    q0 = matmul(matmul(e, p0), e)
    q_expected = matadd(q0, scale(s * s / k, a))
    return a, p0, p, e, q, q_expected


def check(m):
    k = 2 * m
    theta = make_theta(m)
    a, p0, p, e, q, q_expected = build(m, theta)
    assert q == q_expected
    assert all(sum(row, F(0)) == 1 for row in p)
    assert all(sum(row, F(0)) == 1 for row in e)
    assert all(sum((p[i][j] for i in range(k)), F(0)) == 1
               for j in range(k))
    assert all(sum((e[i][j] for i in range(k)), F(0)) == 1
               for j in range(k))
    assert min(min(row) for row in p) >= F(3, 8 * k)
    assert min(min(row) for row in e) >= F(1, 4 * k)

    # ||A||_F/K <= a0, checked by squaring to avoid floating point.
    frob_sq = sum((x * x for row in a for x in row), F(0))
    assert frob_sq / (k * k) <= A0 * A0

    dobrushin = max(tv_rows(p[i], p[j]) for i in range(k) for j in range(k))
    assert dobrushin <= F(5, 8)

    # A one-coordinate sign flip changes exactly four transition cells and
    # affects exactly the two source rows in that 2x2 block.
    neighbor = [row[:] for row in theta]
    neighbor[0][0] = -neighbor[0][0]
    _, _, p_neighbor, _, _, _ = build(m, neighbor)
    changed = [(i, j) for i in range(k) for j in range(k)
               if p[i][j] != p_neighbor[i][j]]
    assert len(changed) == 4
    assert len({i for i, _ in changed}) == 2
    assert all(abs(p[i][j] - p_neighbor[i][j]) == F(1, 4 * k)
               for i, j in changed)

    # Uniform hidden law maps to uniform observed one-symbol contexts.
    assert all(sum(e[x], F(0)) == 1 for x in range(k))
    return {
        "K": k,
        "free_parameters": m * m,
        "min_transition": str(min(min(row) for row in p)),
        "min_emission": str(min(min(row) for row in e)),
        "dobrushin": str(dobrushin),
        "Q_equals_EPE_and_affine_formula": True,
        "neighbor_changed_cells": len(changed),
        "neighbor_changed_rows": 2,
        "analytic_sigma_lower_bounds": {
            "P": "3/8",
            "E": "3/4",
            "Q": "27/128",
            "joint_J": f"27/{128 * k}",
        },
    }


if __name__ == "__main__":
    print(json.dumps({"status": "FINITE-RATIONAL-CHECKS-PASS",
                      "fixtures": [check(m) for m in (1, 2, 3, 4)]},
                     indent=2))
