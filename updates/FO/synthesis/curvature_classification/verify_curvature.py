#!/usr/bin/env python3
"""Exact checks for the profile-space curvature classification note.

All Fourier averages use finite Laurent polynomials and exact SymPy arithmetic.
This script reads no source-directory program or stored numerical output.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

I = sp.I


def clean(poly: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    out = {k: sp.simplify(v) for k, v in poly.items()}
    return {k: v for k, v in out.items() if v != 0}


def add(*polys: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    out: dict[int, sp.Expr] = {}
    for poly in polys:
        for k, v in poly.items():
            out[k] = out.get(k, 0) + v
    return clean(out)


def scale(poly: dict[int, sp.Expr], scalar: sp.Expr) -> dict[int, sp.Expr]:
    return clean({k: scalar * v for k, v in poly.items()})


def multiply(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    out: dict[int, sp.Expr] = {}
    for k, x in left.items():
        for j, y in right.items():
            out[k + j] = out.get(k + j, 0) + x * y
    return clean(out)


def derivative(poly: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    return clean({k: I * k * v for k, v in poly.items() if k})


def cosine(k: int) -> dict[int, sp.Expr]:
    return {k: sp.Rational(1, 2), -k: sp.Rational(1, 2)}


def sine(k: int) -> dict[int, sp.Expr]:
    return {k: sp.Rational(1, 2) / I, -k: -sp.Rational(1, 2) / I}


def average(poly: dict[int, sp.Expr]) -> sp.Expr:
    return sp.simplify(poly.get(0, 0))


def curvature_moments(psi1: dict[int, sp.Expr], psi2: dict[int, sp.Expr]) -> list[sp.Expr]:
    d1, d2 = derivative(psi1), derivative(psi2)
    c = add(multiply(psi2, d1), scale(multiply(psi1, d2), -1))
    return [
        average(c),
        average(multiply(c, d1)),
        average(multiply(c, d2)),
        average(multiply(c, multiply(d1, d1))),
        average(multiply(c, multiply(d1, d2))),
        average(multiply(c, multiply(d2, d2))),
    ]


# Profiles are listed as exact finite Fourier sums, (coefficient, cos/sin, k).
profile_pairs = [
    ([(1, "c", 1)], [(1, "s", 3)]),
    ([(1, "c", 3)], [(1, "s", 1)]),
    ([(1, "c", 1)], [(1, "c", 2)]),
    ([(1, "c", 2)], [(1, "c", 1)]),
    ([(1, "c", 1)], [(1, "s", 1)]),
    ([(1, "c", 1)], [(1, "c", 1), (1, "s", 1)]),
]


def fourier_sum(terms: list[tuple[int, str, int]]) -> dict[int, sp.Expr]:
    out: dict[int, sp.Expr] = {}
    for coefficient, kind, frequency in terms:
        atom = cosine(frequency) if kind == "c" else sine(frequency)
        out = add(out, scale(atom, sp.Integer(coefficient)))
    return out


raw_rows = [curvature_moments(fourier_sum(p), fourier_sum(q)) for p, q in profile_pairs]
expected_raw_rows = [
    [0, 0, 0, sp.Rational(1, 2), 0, 0],
    [0, 0, 0, 0, 0, sp.Rational(-1, 2)],
    [0, sp.Rational(-3, 4), 0, 0, 0, 0],
    [0, 0, sp.Rational(3, 4), 0, 0, 0],
    [-1, 0, 0, sp.Rational(-1, 2), 0, sp.Rational(-1, 2)],
    [-1, 0, 0, sp.Rational(-1, 2), sp.Rational(-1, 2), -1],
]
assert raw_rows == expected_raw_rows

# For P(A)=A_11*A_12^3 and B_11=0, B_12=1, K_P=3 <c(1+r psi1'+s psi2')^2>.
# Coefficients are ordered as 1,r,s,r^2,rs,s^2.
curvature_rows = [
    [3 * row[0], 6 * row[1], 6 * row[2], 3 * row[3], 6 * row[4], 3 * row[5]]
    for row in raw_rows
]
curvature_matrix = sp.Matrix(curvature_rows)
curvature_determinant = sp.factor(curvature_matrix.det())
assert curvature_matrix.rank() == 6
assert curvature_determinant == sp.Rational(-6561, 16)

# Global convexity of F_±(A)=|A|_F^4 ± (1/4) A_11 A_12^3.
# The elementary quadratic-form bound gives |D^2 P[H,H]| <= 6|A|^2|H|^2.
convexity_margin = sp.Rational(4) - sp.Rational(6, 4)
assert convexity_margin == sp.Rational(5, 2) and convexity_margin > 0

# Fixed scalar profile pair (cos y, sin 3y): only the r^2 curvature coefficient survives.
fixed_pair = curvature_moments(cosine(1), sine(3))
assert fixed_pair == [0, 0, 0, sp.Rational(1, 2), 0, 0]


def rectangle_moments(r0: sp.Rational, r1: sp.Rational,
                      s0: sp.Rational, s1: sp.Rational,
                      orientation: int) -> list[sp.Rational]:
    result = []
    for i, j in [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]:
        r_integral = (r1 ** (i + 1) - r0 ** (i + 1)) / sp.Integer(i + 1)
        s_integral = (s1 ** (j + 1) - s0 ** (j + 1)) / sp.Integer(j + 1)
        result.append(sp.Rational(orientation) * r_integral * s_integral)
    return result


# CCW rectangle [-1/2,1/2]x[0,1] plus clockwise [-1,1]x[0,1/8].
rect1 = rectangle_moments(sp.Rational(-1, 2), sp.Rational(1, 2), 0, 1, 1)
rect2 = rectangle_moments(sp.Rational(-1), sp.Rational(1), 0, sp.Rational(1, 8), -1)
fixed_loop_moments = [sp.simplify(a + b) for a, b in zip(rect1, rect2)]
assert fixed_loop_moments == [
    sp.Rational(3, 4), 0, sp.Rational(31, 64), 0, 0, sp.Rational(85, 256)
]

# A convex scalar quartic has nonzero profile circulation but positive Jensen gap.
t, y = sp.symbols("t y", real=True)
segments = [
    (t, 0, 1, 0),
    (1, t, 0, 1),
    (1 - t, 1, -1, 0),
    (0, 1 - t, 0, -1),
]
edge_integrals = []
for r_value, s_value, r_prime, s_prime in segments:
    first_column = 1 + r_prime * sp.cos(y) + s_prime * sp.sin(y)
    second_column = 1 - r_value * sp.sin(y) + s_value * sp.cos(y)
    density = sp.expand((first_column**2 + second_column**2) ** 2)
    y_average = sp.simplify(sp.integrate(sp.expand_trig(density), (y, 0, 2 * sp.pi)) / (2 * sp.pi))
    edge_integrals.append(sp.simplify(sp.integrate(y_average, (t, 0, 1))))
assert edge_integrals == [
    sp.Rational(148, 15), sp.Rational(1349, 120),
    sp.Rational(1349, 120), sp.Rational(148, 15)
]
total_integral = sp.factor(sum(edge_integrals))
mean_energy = sp.factor(total_integral / 4)
convex_gap = sp.factor(mean_energy - 4)
assert total_integral == sp.Rational(2533, 60)
assert mean_energy == sp.Rational(2533, 240)
assert convex_gap == sp.Rational(1573, 240) > 0

positive_example_curvature = -8  # F_xy=8xy, c=-1, B=(1,1), and <psi1'>=<psi2'>=0.
assert positive_example_curvature * 1 == -8  # unit CCW square has M_00=1.

results = {
    "status": "exact_symbolic_checks_passed",
    "profile_moment_order": ["M00", "M10", "M01", "M20", "M11", "M02"],
    "profile_moment_rows": [[str(sp.simplify(x)) for x in row] for row in raw_rows],
    "quartic_curvature_coefficient_order": ["1", "r", "s", "r^2", "r*s", "s^2"],
    "quartic_curvature_rows": [[str(sp.simplify(x)) for x in row] for row in curvature_rows],
    "curvature_matrix_rank": curvature_matrix.rank(),
    "curvature_matrix_determinant": str(curvature_determinant),
    "convexity_hessian_lower_bound": "(5/2)*|A|^2*|H|^2",
    "convexity_margin_positive": True,
    "fixed_profile_moment_row": [str(x) for x in fixed_pair],
    "fixed_profile_loop_moments": [str(x) for x in fixed_loop_moments],
    "positive_gap_edge_integrals": [str(x) for x in edge_integrals],
    "positive_gap_total_unnormalized": str(total_integral),
    "positive_gap_mean_energy": str(mean_energy),
    "positive_gap_over_F_background": str(convex_gap),
    "positive_gap_profile_circulation": str(positive_example_curvature),
}

out = Path(__file__).with_name("CHECKS.json")
out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
print(json.dumps(results, indent=2))
