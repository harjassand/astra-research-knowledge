#!/usr/bin/env python3
"""Exact checks for the explicit 2x2 Strassen kernel and tile interface.

The exhaustive tensor-coordinate check is an exact finite proof of the listed
rank-7 bilinear identity. Random matrix fixtures only check the recursive
implementation and selective tiling on the tested sizes.
"""
from __future__ import annotations

import json
import random
from pathlib import Path


# Flatten A and B as (11, 12, 21, 22); outputs in the same order.
U = [
    [1, 0, 0, 1],   # a11 + a22
    [0, 0, 1, 1],   # a21 + a22
    [1, 0, 0, 0],   # a11
    [0, 0, 0, 1],   # a22
    [1, 1, 0, 0],   # a11 + a12
    [-1, 0, 1, 0],  # a21 - a11
    [0, 1, 0, -1],  # a12 - a22
]
V = [
    [1, 0, 0, 1],   # b11 + b22
    [1, 0, 0, 0],   # b11
    [0, 1, 0, -1],  # b12 - b22
    [-1, 0, 1, 0],  # b21 - b11
    [0, 0, 0, 1],   # b22
    [1, 1, 0, 0],   # b11 + b12
    [0, 0, 1, 1],   # b21 + b22
]
W = [
    [1, 0, 0, 1],   # p1 + p4 - p5 + p7 contributes c11,c22
    [0, 0, 1, -1],  # p2 + p4 contributes c21; -p2 contributes c22
    [0, 1, 0, 1],   # p3 contributes c12,c22
    [1, 0, 1, 0],   # p4 contributes c11,c21
    [-1, 1, 0, 0],  # -p5 contributes c11; +p5 contributes c12
    [0, 0, 0, 1],   # p6 contributes c22
    [1, 0, 0, 0],   # p7 contributes c11
]


def add(A, B, sign=1):
    n = len(A)
    return [[A[i][j] + sign * B[i][j] for j in range(n)] for i in range(n)]


def subblock(A, r0, c0, h):
    return [row[c0:c0 + h] for row in A[r0:r0 + h]]


def strassen(A, B):
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]
    h = n // 2
    a11, a12 = subblock(A, 0, 0, h), subblock(A, 0, h, h)
    a21, a22 = subblock(A, h, 0, h), subblock(A, h, h, h)
    b11, b12 = subblock(B, 0, 0, h), subblock(B, 0, h, h)
    b21, b22 = subblock(B, h, 0, h), subblock(B, h, h, h)
    p1 = strassen(add(a11, a22), add(b11, b22))
    p2 = strassen(add(a21, a22), b11)
    p3 = strassen(a11, add(b12, b22, -1))
    p4 = strassen(a22, add(b21, b11, -1))
    p5 = strassen(add(a11, a12), b22)
    p6 = strassen(add(a21, a11, -1), add(b11, b12))
    p7 = strassen(add(a12, a22, -1), add(b21, b22))
    c11 = add(add(add(p1, p4), p5, -1), p7)
    c12 = add(p3, p5)
    c21 = add(p2, p4)
    c22 = add(add(add(p1, p2, -1), p3), p6)
    out = [[0] * n for _ in range(n)]
    for i in range(h):
        out[i][:h] = c11[i]
        out[i][h:] = c12[i]
        out[i + h][:h] = c21[i]
        out[i + h][h:] = c22[i]
    return out


def naive(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def padded_tile(X, Y, rows, cols, D):
    m = 1
    while m < D:
        m *= 2
    A = [[0] * m for _ in range(m)]
    B = [[0] * m for _ in range(m)]
    for i, ri in enumerate(rows):
        A[i][:D] = X[ri][:]
    for j, cj in enumerate(cols):
        for k in range(D):
            B[k][j] = Y[k][cj]
    C = strassen(A, B)
    return {(ri, cj): C[i][j] for i, ri in enumerate(rows) for j, cj in enumerate(cols)}


def selective(X, Y, rectangles, residual, D):
    out = {}
    for R, C in rectangles:
        rlist, clist = list(R), list(C)
        for ri in range(0, len(rlist), D):
            for cj in range(0, len(clist), D):
                out.update(padded_tile(X, Y, rlist[ri:ri + D], clist[cj:cj + D], D))
    for i, j in residual:
        out[(i, j)] = sum(X[i][k] * Y[k][j] for k in range(D))
    return out


def tensor_check():
    checked = 0
    for ia in range(4):
        ar, ac = divmod(ia, 2)
        for ib in range(4):
            br, bc = divmod(ib, 2)
            for io in range(4):
                orow, ocol = divmod(io, 2)
                expected = int(ac == br and ar == orow and bc == ocol)
                actual = sum(U[t][ia] * V[t][ib] * W[t][io] for t in range(7))
                assert actual == expected, (ia, ib, io, actual, expected)
                checked += 1
    nz = sum(x != 0 for T in (U, V, W) for row in T for x in row)
    assert nz == 36
    assert all(x in (-1, 0, 1) for T in (U, V, W) for row in T for x in row)
    return {"tensor_coordinates_checked": checked, "nonzero_coefficients": nz,
            "coefficient_alphabet": [-1, 0, 1], "field": "Q"}


def main():
    rng = random.Random(20261008)
    recursive_cases = 0
    for n in (1, 2, 4, 8):
        for _ in range(12):
            A = [[rng.randrange(-7, 8) for _ in range(n)] for _ in range(n)]
            B = [[rng.randrange(-7, 8) for _ in range(n)] for _ in range(n)]
            assert strassen(A, B) == naive(A, B)
            recursive_cases += 1

    D, N = 2, 16
    X = [[rng.randrange(-5, 6) for _ in range(D)] for _ in range(N)]
    Y = [[rng.randrange(-5, 6) for _ in range(N)] for _ in range(D)]
    rectangles = [
        (list(range(0, 8)), list(range(0, 8))),
        (list(range(4, 12)), list(range(4, 12))),  # deliberate overlap
    ]
    residual = [(15, 0), (0, 15)]
    got = selective(X, Y, rectangles, residual, D)
    requested = {(i, j) for R, C in rectangles for i in R for j in C} | set(residual)
    expected = { (i, j): sum(X[i][k] * Y[k][j] for k in range(D)) for i, j in requested }
    assert got == expected
    assert len(got) == len(requested)  # overlap is deduplicated in the output map

    k = 3
    assert 7**k == 343
    assert 6 * (7**k - 4**k) == 6 * (343 - 64)
    assert 7**100 < 2**281  # exact certificate log_2(7) < 2.81
    results = {
        **tensor_check(),
        "recursive_random_integer_products": recursive_cases,
        "selective_mask_fixture": {
            "N": N, "D": D, "rectangles": len(rectangles),
            "residual_pairs": len(residual), "requested_distinct_pairs": len(requested),
            "overlap_present": True, "all_outputs_exact": True,
        },
        "operation_formula_checks": {
            "multiplications_at_n8": 7**k,
            "add_subtract_at_n8": 6 * (7**k - 4**k),
            "log2_7_less_than_281_over_100": True,
        },
        "limitations": [
            "Finite checks do not validate a 9/4 kernel or arbitrary-mask complexity.",
            "Random fixtures do not replace the tensor-coordinate identity check.",
        ],
    }
    target = Path(__file__).with_name("checks.json")
    target.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
