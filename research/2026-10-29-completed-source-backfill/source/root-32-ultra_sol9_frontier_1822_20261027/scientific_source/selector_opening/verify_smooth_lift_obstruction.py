#!/usr/bin/env python3
"""Exact finite algebra for PROOF.md; the compactness proof remains analytic.

Run with the shared solver_runtime/.venv/bin/python. No optimizer, numerical
eigenvalue, source import, or previously accepted Gram identity is used.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import sympy as sp

START = time.perf_counter()
OUT = Path(__file__).resolve().parent
a, b, c, d, t, alpha, eta = sp.symbols("a b c d t alpha eta", real=True)
entries = (a, b, c, d)
u, v, w, q = a*a+c*c, b*b+d*d, a*b+c*d, a*d-b*c
T = u+v
p0 = sp.Rational(55220381, 10000000000)
p2 = sp.Rational(114430029, 625000000)
p3 = sp.Rational(-801761987, 5000000000)
ell = sp.Rational(118849817, 4000000000)
F = sp.expand(p0*(u*u+v*v)+p2*u*v+p3*w*w+ell*q*(u-v))
I, E, D = (1, 0, 0, 1), (1, 0, 0, 0), (-1, 0, 0, 1)


def d2(poly, base, direction):
    line = poly.subs(dict(zip(entries, (x+t*y for x, y in zip(base, direction)))))
    return sp.expand(sp.diff(line, t, 2).subs(t, 0))


def functional(poly):
    return sp.expand(d2(poly, I, D)/4+d2(poly, E, D)/2)


def rat(value):
    return str(sp.factor(value))


H = F-alpha*q*q
curv_I, curv_E = d2(H, I, D), d2(H, E, D)
assert sp.expand(curv_I-(24*p0-4*p2+4*alpha)) == 0
assert sp.expand(curv_E-(12*p0+2*p2-6*ell-2*alpha)) == 0
assert sp.expand(curv_I+2*curv_E-12*(4*p0-ell)) == 0
gap = ell-4*p0
assert gap == sp.Rational(152486037, 20000000000) > 0
assert functional(q*q) == 0
assert functional(F) == -3*gap

monomial_values = {}
for aa in range(5):
    for bb in range(5-aa):
        for cc in range(5-aa-bb):
            dd = 4-aa-bb-cc
            exponents = (aa, bb, cc, dd)
            monomial = sp.prod(x**power for x, power in zip(entries, exponents))
            monomial_values[exponents] = functional(monomial)
assert len(monomial_values) == 35
nonzero = {powers: value for powers, value in monomial_values.items() if value}
assert nonzero == {(4, 0, 0, 0): 9, (3, 0, 0, 1): -3, (0, 0, 0, 4): 3}
l1_norm = sum(abs(value) for value in monomial_values.values())
assert l1_norm == 15
radius = gap/10
assert functional(F)+radius*l1_norm == -3*gap/2 < 0
accepted_pc_radius = sp.Rational(1, 4928000000)
assert radius > accepted_pc_radius

# A literal general determinant midpoint identity used in the compact bounds.
y = sp.symbols("y0:4", real=True)
q_plus = q.subs(dict(zip(entries, (x+yy for x, yy in zip(entries, y)))), simultaneous=True)
q_minus = q.subs(dict(zip(entries, (x-yy for x, yy in zip(entries, y)))), simultaneous=True)
q_y = y[0]*y[3]-y[1]*y[2]
assert sp.expand(q_plus+q_minus-2*q-2*q_y) == 0

# Ordinary comparator: no C2 lift already occurs for the classical PC ADM
# energy, and for its explicit strict convex perturbation. PC itself is a
# primary-source input; these are separate exact local Hessian computations.
ADM = sp.expand(T*T-2*T*q)
A_control, X_control = (1, 0, 0, 2), (3, 0, 0, 1)
assert ADM.subs(dict(zip(entries, I))) == 0
assert d2(ADM, A_control, X_control) == -20
assert d2(T*T, A_control, X_control) == 400
assert d2(q*q, A_control, X_control) == 122
strict_control = sp.expand(ADM+T*T/100)
assert d2(strict_control-alpha*q*q, A_control, X_control) == -16-122*alpha

# Positive control for the classification: F_plus=T^2+5q^2 admits the
# polynomial lift T^2+5s^2. Its entry restriction has a globally PSD Hessian.
x = sp.symbols("x0:4", real=True)
norm_hessian = d2(T*T, entries, x)
assert sp.expand(norm_hessian-(8*sum(z*zz for z, zz in zip(entries, x))**2
                                   +4*T*sum(zz*zz for zz in x))) == 0

result = {
    "status": "EXACT_FINITE_ALGEBRA_PASSED",
    "scope": "Analytic C2 blowup proof is in PROOF.md; this replay checks its finite application and comparators.",
    "literal_F_sha256": hashlib.sha256(str(F).encode()).hexdigest(),
    "curvature_at_I": rat(curv_I),
    "curvature_at_E": rat(curv_E),
    "curvature_sum_alpha_independent": rat(curv_I+2*curv_E),
    "gap_L_minus_4p0": rat(gap),
    "functional_F": rat(functional(F)),
    "functional_det_squared": rat(functional(q*q)),
    "ordinary_full35_monomials_checked": len(monomial_values),
    "functional_nonzero_monomials": {str(k): int(v) for k, v in nonzero.items()},
    "functional_coefficient_l1": int(l1_norm),
    "no_C2_box_radius": rat(radius),
    "no_C2_box_remaining_negative_margin": rat(3*gap/2),
    "accepted_PC_box_radius_input": rat(accepted_pc_radius),
    "no_C2_radius_contains_accepted_PC_radius": True,
    "ordinary_ADM_curvature": -20,
    "ordinary_strict_ADM_eta": "1/100",
    "ordinary_strict_ADM_curvature_after_alpha_det_squared": "-16-122*alpha",
    "positive_control": "T^2+5q^2 with lift T^2+5s^2; exact Hessian identity checked",
    "determinant_midpoint_identity": "PASSED",
    "runtime_seconds": time.perf_counter()-START,
}
(OUT/"EXACT_SMOOTH_LIFT_OBSTRUCTION.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
