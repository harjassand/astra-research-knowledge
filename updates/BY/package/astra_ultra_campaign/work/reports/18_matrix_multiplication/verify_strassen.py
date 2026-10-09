#!/usr/bin/env python3
"""Exact coefficient check for Strassen's 2x2 bilinear algorithm.

Uses only integer coefficient dictionaries; no random inputs or floating point.
Each polynomial is stored as (A-entry, B-entry) -> integer coefficient.
"""

from collections import defaultdict


def linear(**terms):
    return {name: int(coeff) for name, coeff in terms.items() if coeff}


def add_linear(*forms):
    out = defaultdict(int)
    for form in forms:
        for name, coeff in form.items():
            out[name] += coeff
    return {name: coeff for name, coeff in out.items() if coeff}


def sub_linear(left, right):
    return add_linear(left, {name: -coeff for name, coeff in right.items()})


def product(left, right):
    return {(a, b): ca * cb for a, ca in left.items() for b, cb in right.items()}


def add_poly(*polys):
    out = defaultdict(int)
    for poly in polys:
        for monomial, coeff in poly.items():
            out[monomial] += coeff
    return {monomial: coeff for monomial, coeff in out.items() if coeff}


a11, a12, a21, a22 = (linear(**{name: 1}) for name in ("a11", "a12", "a21", "a22"))
b11, b12, b21, b22 = (linear(**{name: 1}) for name in ("b11", "b12", "b21", "b22"))

m1 = product(add_linear(a11, a22), add_linear(b11, b22))
m2 = product(add_linear(a21, a22), b11)
m3 = product(a11, sub_linear(b12, b22))
m4 = product(a22, sub_linear(b21, b11))
m5 = product(add_linear(a11, a12), b22)
m6 = product(sub_linear(a21, a11), add_linear(b11, b12))
m7 = product(sub_linear(a12, a22), add_linear(b21, b22))

actual = (
    add_poly(m1, m4, {k: -v for k, v in m5.items()}, m7),
    add_poly(m3, m5),
    add_poly(m2, m4),
    add_poly(m1, {k: -v for k, v in m2.items()}, m3, m6),
)

expected = (
    {("a11", "b11"): 1, ("a12", "b21"): 1},
    {("a11", "b12"): 1, ("a12", "b22"): 1},
    {("a21", "b11"): 1, ("a22", "b21"): 1},
    {("a21", "b12"): 1, ("a22", "b22"): 1},
)

assert actual == expected, (actual, expected)
print("PASS: all four outputs match the matrix-product polynomials coefficient-for-coefficient over Z")
print(f"bilinear products: {len((m1, m2, m3, m4, m5, m6, m7))}")
print("scalar products at n=2: 7 versus 8 in the direct dot-product formula")
print("exactness: sparse integer polynomial identity; no sampling or floating point")
