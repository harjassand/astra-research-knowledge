#!/usr/bin/env python3
"""Finite exact check for the selected-column Strassen construction.

The recursive 2x2 identity is applied to every D x D tile of
X (N x D) times Y[:, J] (D x |J|), with zero padding only in edge tiles.
Python integers make every check exact.
"""
from __future__ import annotations

import json
from math import isqrt
from pathlib import Path


def add(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def sub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def block(a, r0, c0, h):
    return [row[c0 : c0 + h] for row in a[r0 : r0 + h]]


def join(c11, c12, c21, c22):
    top = [r1 + r2 for r1, r2 in zip(c11, c12)]
    bot = [r1 + r2 for r1, r2 in zip(c21, c22)]
    return top + bot


def strassen(a, b):
    n = len(a)
    assert n == len(b) and n and n & (n - 1) == 0
    assert all(len(row) == n for row in a)
    assert all(len(row) == n for row in b)
    if n == 1:
        return [[a[0][0] * b[0][0]]]

    h = n // 2
    a11, a12 = block(a, 0, 0, h), block(a, 0, h, h)
    a21, a22 = block(a, h, 0, h), block(a, h, h, h)
    b11, b12 = block(b, 0, 0, h), block(b, 0, h, h)
    b21, b22 = block(b, h, 0, h), block(b, h, h, h)

    p1 = strassen(add(a11, a22), add(b11, b22))
    p2 = strassen(add(a21, a22), b11)
    p3 = strassen(a11, sub(b12, b22))
    p4 = strassen(a22, sub(b21, b11))
    p5 = strassen(add(a11, a12), b22)
    p6 = strassen(sub(a21, a11), add(b11, b12))
    p7 = strassen(sub(a12, a22), add(b21, b22))

    c11 = add(sub(add(p1, p4), p5), p7)
    c12 = add(p3, p5)
    c21 = add(p2, p4)
    c22 = add(add(sub(p1, p2), p3), p6)
    return join(c11, c12, c21, c22)


def ceil_power_of_two(n):
    return 1 << (n - 1).bit_length()


def selected_column_product(X, Y, columns):
    n, d = len(X), len(X[0])
    assert len(Y) == d and all(len(row) == n for row in Y)
    assert len(set(columns)) == len(columns)
    side = ceil_power_of_two(d)
    out = {}

    for row0 in range(0, n, side):
        row_ids = list(range(row0, min(row0 + side, n)))
        a = [[0] * side for _ in range(side)]
        for r, i in enumerate(row_ids):
            a[r][:d] = X[i]

        for col0 in range(0, len(columns), side):
            col_ids = columns[col0 : col0 + side]
            b = [[0] * side for _ in range(side)]
            for k in range(d):
                for c, j in enumerate(col_ids):
                    b[k][c] = Y[k][j]

            tile = strassen(a, b)
            for r, i in enumerate(row_ids):
                for c, j in enumerate(col_ids):
                    out[(i, j)] = tile[r][c]
    return out


def fixture(n, d):
    s = isqrt(isqrt(n ** 3))
    # A deterministic noncontiguous column set with exactly s distinct indices.
    columns = sorted({(7 * t + 3) % n for t in range(s)})
    assert len(columns) == s
    X = [
        [(-1 if (i + 2 * k) % 3 == 0 else 1) * (13 * i + 5 * k - 17)
         for k in range(d)]
        for i in range(n)
    ]
    Y = [
        [(-1 if (3 * k + j) % 4 == 0 else 1) * (11 * k - 7 * j + 19)
         for j in range(n)]
        for k in range(d)
    ]
    return X, Y, columns


def run():
    cases = []
    for n, d in [(16, 2), (256, 4)]:
        X, Y, columns = fixture(n, d)
        got = selected_column_product(X, Y, columns)
        expected = {
            (i, j): sum(X[i][k] * Y[k][j] for k in range(d))
            for i in range(n)
            for j in columns
        }
        assert got == expected
        cases.append({
            "N": n,
            "D": d,
            "selected_columns": len(columns),
            "mask_entries": n * len(columns),
            "tile_side": ceil_power_of_two(d),
            "tile_products": (n + ceil_power_of_two(d) - 1) // ceil_power_of_two(d)
                             * ((len(columns) + ceil_power_of_two(d) - 1)
                                // ceil_power_of_two(d)),
            "exact_match": True,
            "integer_domain": "Python arbitrary-precision integers",
        })
    return {
        "check": "Strassen-tiled selected-column product equals direct exact dots",
        "status": "PASS",
        "cases": cases,
        "scope": "finite implementation diagnostic; not an asymptotic proof",
    }


if __name__ == "__main__":
    result = run()
    out = Path(__file__).with_name("exact_check.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
