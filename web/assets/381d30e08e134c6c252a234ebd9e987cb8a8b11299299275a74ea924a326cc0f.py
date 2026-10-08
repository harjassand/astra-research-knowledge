#!/usr/bin/env python3
"""Exact rational verification of the P5 fixed-sector stability witness."""

from fractions import Fraction
from itertools import combinations
import json


A = [
    [0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 0, 1, 0],
]


def det2(rows, cols):
    return (
        A[rows[0]][cols[0]] * A[rows[1]][cols[1]]
        - A[rows[0]][cols[1]] * A[rows[1]][cols[0]]
    )


sets = list(combinations(range(5), 2))
weights = {}
for rows in sets:
    allowed_cols = [j for j in range(5) if j not in rows]
    weights[rows] = sum(
        det2(rows, cols) ** 2 for cols in combinations(allowed_cols, 2)
    )

expected = {
    (0, 1): 0,
    (0, 2): 1,
    (0, 3): 2,
    (0, 4): 1,
    (1, 2): 1,
    (1, 3): 3,
    (1, 4): 2,
    (2, 3): 1,
    (2, 4): 1,
    (3, 4): 0,
}
assert weights == expected

# Each complex rational is represented as (real, imaginary) Fractions.
z = [
    (Fraction(-3), Fraction(1, 100)),
    (Fraction(2), Fraction(29397, 20500)),
    (Fraction(0), Fraction(2)),
    (Fraction(-2), Fraction(1, 100)),
    (Fraction(3), Fraction(1, 100)),
]
value_re = Fraction(0)
value_im = Fraction(0)
for (i, j), weight in weights.items():
    ai, bi = z[i]
    aj, bj = z[j]
    value_re += weight * (ai * aj - bi * bj)
    value_im += weight * (ai * bj + bi * aj)
assert all(im > 0 for _, im in z)
assert value_re == value_im == 0

# At x=(1,1,1,1,1), g=12, grad=(4,6,4,6,4), and
# Hessian(g) has off-diagonal entries w_ij and zero diagonal.
g_one = sum(weights.values())
grad = [
    sum(weights.get(tuple(sorted((i, j))), 0) for j in range(5) if j != i)
    for i in range(5)
]
v = [-5, 3, 0, -3, 5]
hess_quad = sum(
    2 * weights.get((i, j), 0) * v[i] * v[j]
    for i in range(5)
    for j in range(i + 1, 5)
)
grad_dot_v = sum(grad[i] * v[i] for i in range(5))
assert g_one == 12
assert grad == [4, 6, 4, 6, 4]
assert grad_dot_v == 0
assert hess_quad == 16
log_hess_quad = Fraction(hess_quad, g_one) - Fraction(grad_dot_v**2, g_one**2)
assert log_hess_quad == Fraction(4, 3)


def frac(q):
    return f"{q.numerator}/{q.denominator}"


receipt = {
    "matrix": A,
    "sector_k": 2,
    "weights_lexicographic_1_based": [weights[s] for s in sets],
    "polynomial_terms_1_based": [
        {"S": [i + 1 for i in s], "coefficient": weights[s]}
        for s in sets
        if weights[s]
    ],
    "upper_half_plane_zero": {
        "x_real": [frac(re) for re, _ in z],
        "x_imag": [frac(im) for _, im in z],
        "value_real": frac(value_re),
        "value_imag": frac(value_im),
    },
    "all_ones_log_hessian_witness": {
        "g": g_one,
        "gradient": grad,
        "v": v,
        "gradient_dot_v": grad_dot_v,
        "hessian_g_quadratic": hess_quad,
        "hessian_log_g_quadratic": frac(log_hess_quad),
    },
    "status": "exact rational assertions passed",
}
print(json.dumps(receipt, indent=2))
