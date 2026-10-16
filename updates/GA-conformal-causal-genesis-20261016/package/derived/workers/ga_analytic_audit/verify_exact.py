#!/usr/bin/env python3
"""Exact finite checks for REPORT.md, not an analytic proof.

Uses only Python's standard library. Fourier polynomials below have rational
coefficients; all derivatives checked are second derivatives of cosine sums.
"""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def clean(p):
    return {k: v for k, v in p.items() if v}


def add(*polys):
    out = {}
    for p in polys:
        for k, v in p.items():
            out[k] = out.get(k, F(0)) + v
    return clean(out)


def scale(p, factor):
    return clean({k: factor * v for k, v in p.items()})


def multiply(*polys):
    dims = len(next(iter(polys[0])))
    out = {(0,) * dims: F(1)}
    for p in polys:
        new = {}
        for k, v in out.items():
            for l, w in p.items():
                m = tuple(a + b for a, b in zip(k, l))
                new[m] = new.get(m, F(0)) + v * w
        out = clean(new)
    return out


def const(value, dims=2):
    return {(0,) * dims: F(value)}


def cosine(kx, ky):
    if kx == ky == 0:
        return const(1)
    return {(kx, ky): F(1, 2), (-kx, -ky): F(1, 2)}


def hessian(p, i, j):
    return clean({k: -k[i] * k[j] * v for k, v in p.items()})


def average(p):
    return p.get((0, 0), F(0))


def derivative(p, index):
    """Formal derivative for ordinary polynomial exponent dictionaries."""
    out = {}
    for k, v in p.items():
        if k[index]:
            l = list(k)
            l[index] -= 1
            out[tuple(l)] = v * k[index]
    return clean(out)


def monomial(exponents, coefficient=1):
    return {tuple(exponents): F(coefficient)}


checks = []


def check(label, actual, expected):
    if actual != expected:
        raise RuntimeError(f"{label}: actual={actual}, expected={expected}")
    checks.append({"label": label, "actual": str(actual), "expected": str(expected)})


psi = add(
    scale(cosine(1, 1), -1),
    scale(cosine(0, 1), -1),
    scale(cosine(1, 2), -F(1, 2)),
)
A = hessian(psi, 0, 1)
B = hessian(psi, 1, 1)
R = hessian(psi, 0, 0)
check("three-mode <A B^2>", average(multiply(A, B, B)), F(3, 2))
check("three-mode <R^2>", average(multiply(R, R)), F(5, 8))
check("three-mode <A^2 B>", average(multiply(A, A, B)), F(1, 2))
check("three-mode <R B^2>", average(multiply(R, B, B)), F(5, 4))

psi_sep = multiply(add(const(1), cosine(1, 0)), add(const(1), cosine(0, 1)))
As = hessian(psi_sep, 0, 1)
Bs = hessian(psi_sep, 1, 1)
Rs = hessian(psi_sep, 0, 0)
check("separable <R B^2>", average(multiply(Rs, Bs, Bs)), -F(1, 2))
check("separable <A^2 B>", average(multiply(As, As, Bs)), F(0))
check("separable <R^2>", average(multiply(Rs, Rs)), F(3, 4))

shear_b = add(cosine(0, 1), cosine(0, 2))
check("pure shear <b^3>", average(multiply(shear_b, shear_b, shear_b)), F(3, 4))
check(
    "vertical q test <cos(2y) cos(y)^2>",
    average(multiply(cosine(0, 2), cosine(0, 1), cosine(0, 1))),
    F(1, 4),
)

# Ordinary-polynomial coordinates here are (a,b,X,Y,theta).
# Multiply the claimed Hessian identity by theta to avoid denominators.
a = monomial((1, 0, 0, 0, 0))
b = monomial((0, 1, 0, 0, 0))
X = monomial((0, 0, 1, 0, 0))
Y = monomial((0, 0, 0, 1, 0))
theta = monomial((0, 0, 0, 0, 1))
theta_K = add(
    monomial((4, 0, 0, 0, 1), F(1, 12)),
    monomial((4, 0, 0, 0, 2), F(1, 12)),
    monomial((2, 2, 0, 0, 1), F(1, 2)),
    monomial((0, 4, 0, 0, 0), F(1, 3)),
)
lhs = add(
    multiply(derivative(derivative(theta_K, 0), 0), X, X),
    scale(multiply(derivative(derivative(theta_K, 0), 1), X, Y), F(2)),
    multiply(derivative(derivative(theta_K, 1), 1), Y, Y),
    scale(multiply(theta, a, a, X, X), -1),
    scale(multiply(theta, a, a, Y, Y), -1),
)
rhs = add(
    multiply(theta, theta, a, a, X, X),
    scale(multiply(theta, a, b, X, Y), 4),
    scale(multiply(b, b, Y, Y), 4),
    multiply(theta, b, b, X, X),
)
check("theta times heat Hessian identity", lhs, rhs)

# The finite algebraic classification concerns (a,b,c,q), degree three.
monomials = [k for k in product(range(4), repeat=4) if sum(k) == 3]
forbid_big_o = {(0, 3, 0, 0), (1, 2, 0, 0)}
forbid_little_o = forbid_big_o | {(0, 2, 0, 1), (0, 2, 1, 0), (2, 1, 0, 0)}
check("total homogeneous cubic dimension", len(monomials), 20)
check("finite-bound cubic dimension", len(set(monomials) - forbid_big_o), 18)
check("UI little-o cubic dimension", len(set(monomials) - forbid_little_o), 15)

# Check the exact remainder powers under q=0 anisotropic scaling:
# a=N^-1 A, b=B, c=-sigma N^-2 R. Once b^3,ab^2,cb^2,a^2b
# are absent, every surviving monomial has N power >= 3.
remaining_q_zero = [
    k for k in monomials
    if k[3] == 0 and k not in forbid_little_o
]
check("minimum surviving anisotropic N decay", min(k[0] + 2 * k[2] for k in remaining_q_zero), 3)

receipt = {
    "status": "all exact finite checks passed",
    "number_of_checks": len(checks),
    "scope": "Exact rational Fourier averages, quartic Hessian algebra, and monomial counts only.",
    "not_verified_by_this_script": [
        "mixed-derivative interpolation",
        "periodic multiplier and Riesz-transform theorems",
        "Sobolev density and heat convergence",
        "uniform-integrability convergence",
        "the sharp conformal quasiconvexity inequality",
        "historical originality or external validation",
    ],
    "checks": checks,
}
out = Path(__file__).resolve().parent / "EXACT_CHECK_RECEIPT.json"
out.write_text(json.dumps(receipt, indent=2) + "\n")
print(f"All {len(checks)} exact finite checks passed. Receipt: {out}")
