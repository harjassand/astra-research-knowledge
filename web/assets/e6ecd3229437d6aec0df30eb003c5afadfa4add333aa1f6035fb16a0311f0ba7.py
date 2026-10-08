#!/usr/bin/env python3
"""Exact rational check of a dense-gauged Strassen 2x2x2 decomposition."""

from fractions import Fraction as Q
from itertools import product


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0:
        raise ValueError("singular 2x2 matrix")
    return [[a[1][1] / det, -a[0][1] / det],
            [-a[1][0] / det, a[0][0] / det]]


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]


def scale(c, a):
    return [[c * a[i][j] for j in range(2)] for i in range(2)]


def eval_form(form, matrix):
    return sum(form[2 * i + j] * matrix[i][j]
               for i in range(2) for j in range(2))


def main():
    # Rows are coefficients in (x11,x12,x21,x22) or (y11,y12,y21,y22).
    a_forms = [
        [1, 0, 0, 1],   # x11 + x22
        [0, 0, 1, 1],   # x21 + x22
        [1, 0, 0, 0],   # x11
        [0, 0, 0, 1],   # x22
        [1, 1, 0, 0],   # x11 + x12
        [-1, 0, 1, 0],  # x21 - x11
        [0, 1, 0, -1],  # x12 - x22
    ]
    b_forms = [
        [1, 0, 0, 1],   # y11 + y22
        [1, 0, 0, 0],   # y11
        [0, 1, 0, -1],  # y12 - y22
        [-1, 0, 1, 0],  # y21 - y11
        [0, 0, 0, 1],   # y22
        [1, 1, 0, 0],   # y11 + y12
        [0, 0, 1, 1],   # y21 + y22
    ]
    c_matrices = [
        [[1, 0], [0, 1]],
        [[0, 0], [1, -1]],
        [[0, 1], [0, 1]],
        [[1, 0], [1, 0]],
        [[-1, 1], [0, 0]],
        [[0, 0], [0, 1]],
        [[1, 0], [0, 0]],
    ]

    p = [[Q(7), Q(5)], [Q(1), Q(2)]]
    q = [[Q(6), Q(6)], [Q(5), Q(1)]]
    r = [[Q(5), Q(5)], [Q(4), Q(1)]]
    pinv, qinv, rinv = inv2(p), inv2(q), inv2(r)

    a_prime = []
    b_prime = []
    c_prime = []
    for ell in range(7):
        a_prime.append([
            eval_form(a_forms[ell], matmul(matmul(p, basis), qinv))
            for basis in [
                [[Q(i == u and j == v) for j in range(2)] for i in range(2)]
                for u, v in product(range(2), repeat=2)
            ]
        ])
        b_prime.append([
            eval_form(b_forms[ell], matmul(matmul(q, basis), rinv))
            for basis in [
                [[Q(i == u and j == v) for j in range(2)] for i in range(2)]
                for u, v in product(range(2), repeat=2)
            ]
        ])
        c_prime.append(matmul(matmul(pinv, c_matrices[ell]), r))

    coeffs = [*a_prime, *b_prime,
              [x for matrix in c_prime for row in matrix for x in row]]
    if any(value == 0 for block in coeffs for value in block):
        raise AssertionError("a transformed leg coefficient vanished")

    basis = [
        [[Q(i == u and j == v) for j in range(2)] for i in range(2)]
        for u, v in product(range(2), repeat=2)
    ]
    for ia, ib in product(range(4), repeat=2):
        left = matmul(basis[ia], basis[ib])
        right = [[Q(0), Q(0)], [Q(0), Q(0)]]
        for ell in range(7):
            term_scale = (eval_form(a_prime[ell], basis[ia])
                          * eval_form(b_prime[ell], basis[ib]))
            right = add(right, scale(term_scale, c_prime[ell]))
        if left != right:
            raise AssertionError(f"coefficient identity failed at ({ia},{ib})")

    print("field: Q")
    print("determinants:", p[0][0] * p[1][1] - p[0][1] * p[1][0],
          q[0][0] * q[1][1] - q[0][1] * q[1][0],
          r[0][0] * r[1][1] - r[0][1] * r[1][0])
    print("rank-one terms: 7")
    print("nonzero transformed leg coefficients: 84/84")
    print("verified bilinear basis-pair identities: 16/16")
    print("equivalently, all 64 scalar tensor coefficients agree")
    print("for every k, a singleton supported input reaches all 7^k leaves")


if __name__ == "__main__":
    main()
