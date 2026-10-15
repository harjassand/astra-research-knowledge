#!/usr/bin/env python3
"""Exact identities for the independent left-SO(2) contact-face audit.

This is symbolic identity checking, not a finite-search proof of convexity.
The universal arguments are in REPORT.md. No construction report is read.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


OUT = Path(__file__).resolve().parent
CHECKS = []


def equal(name, left, right=0):
    residual = sp.factor(sp.expand(left - right))
    if residual != 0:
        raise AssertionError(f"{name}: {residual}")
    CHECKS.append({"name": name, "status": "PASS", "residual": "0"})


a, b, c, d = sp.symbols("a b c d", real=True)
alpha, k, ell, m = sp.symbols("alpha k ell m", real=True)
eps, t = sp.symbols("epsilon t", real=True)
u = a**2 + c**2
v = b**2 + d**2
w = a*b + c*d
j = a*d - b*c
H = ((a-d)**2 + (b+c)**2)**2
G = k*w**2 + ell*v*j + m*v**2
F = alpha*H + G
variables = (a, b, c, d)
at_I = {a: 1, b: 0, c: 0, d: 1}

equal("Gram relation", u*v, w**2+j**2)
equal("H invariant expansion", H, u**2+v**2+6*u*v-4*u*j-4*v*j-4*w**2)
equal("contact in the reduced family", sp.diff(F, a, 2).subs(at_I))

# The nine-dimensional invariant quartic space, with j^2 eliminated.
basis = (u**2, u*v, v**2, u*w, v*w, w**2, u*j, v*j, w*j)
monomials = sorted(set().union(*(sp.Poly(q, variables).monoms() for q in basis)))
coeff_matrix = sp.Matrix([[sp.Poly(q, variables).coeff_monomial(mon)
                          for q in basis] for mon in monomials])
assert coeff_matrix.rank() == 9
CHECKS.append({"name": "independence of invariant basis", "status": "PASS", "rank": 9})
cs = sp.symbols("x0:9")
P = sum(x*q for x, q in zip(cs, basis))
acoustic = sp.diff(P, a, 2)
constraints = [acoustic.subs(at_I)]
constraints += [sp.diff(acoustic, z).subs(at_I) for z in variables]
constraints += [sp.diff(P, a, z).subs(at_I) for z in (b, c)]
constraint_matrix, _ = sp.linear_eq_to_matrix(constraints, cs)
assert constraint_matrix.rank() == 5
solution = (-cs[6]/4, -3*cs[6]/2, cs[2], 0, 0, cs[5], cs[6], cs[7], 0)
for n, q in enumerate(constraints):
    equal(f"stationary acoustic constraint {n}", q.subs(dict(zip(cs, solution))))
CHECKS.append({"name": "contact plus ROC acoustic constraints", "status": "PASS", "rank": 5,
               "dimension": 4, "solution": str(solution),
               "constraints": [str(q) for q in constraints]})

# Contact by itself is insufficient for the four-dimensional conclusion.
contact_only_counterexample = u**2 - 6*u*v
equal("contact-only counterexample has contact", sp.diff(contact_only_counterexample, a, 2).subs(at_I))
assert sp.diff(contact_only_counterexample, a, 3).subs(at_I) == 24
CHECKS.append({"name": "contact-only counterexample violates acoustic stationarity", "status": "PASS",
               "polynomial": str(contact_only_counterexample), "third_a_derivative_at_I": 24})

# Taylor coefficients at I. The variable names again denote increments.
G_at_I_plus = sp.expand(G.subs({a: 1+a, d: 1+d}, simultaneous=True))
G_poly = sp.Poly(G_at_I_plus, variables)
parts = {degree: sum(coef*sp.prod(z**power for z, power in zip(variables, mon))
                     for mon, coef in G_poly.terms() if sum(mon) == degree)
         for degree in range(5)}
L = ell+2*m
D = 2*k*m-k*ell-ell**2
Q = (k+ell+2*m)*b**2 + 2*(k+ell)*b*c + k*c**2 + 3*L*d**2
C = a*((2*k+ell)*b**2 + 2*k*b*c + 3*ell*d**2) + d*((ell+4*m)*b**2
    + 2*(k-ell)*b*c + 2*k*c**2 + (ell+4*m)*d**2)
equal("corrected quadratic Taylor coefficient", parts[2], Q+3*ell*j)
equal("cubic Taylor coefficient", parts[3], C)
equal("no two a slots in cubic", sp.diff(C, a, 2))
equal("determinant of transverse 2x2 block", (k+ell+2*m)*k-(k+ell)**2, D)

# A rank-one matrix realizes any (b,c,d) with d nonzero by setting a=bc/d.
equal("rank-one parametrization for acoustic necessity", j.subs(a, b*c/d))

# L=0 obstruction. The completion contributes only quadratically in t.
L_zero_hessian = sp.expand(sp.diff(F, d, 2).subs({a: 1+t, b: 0, c: 0, d: 1, m: -ell/2}))
equal("L=0 first derivative obstruction", L_zero_hessian, 6*ell*t+12*alpha*t**2)

# D=0 obstruction: the negative cubic cannot be repaired by any finite alpha.
Z = (1, k*eps, -(k+ell)*eps, -k*(k+ell)*eps**2)
equal("D=0 witness rank-one identity", Z[0]*Z[3]-Z[1]*Z[2])
rank_one_hessian = sum(sp.diff(F, x, y)*Z[ii]*Z[jj]
                       for ii, x in enumerate(variables) for jj, y in enumerate(variables))
rank_one_hessian = sp.expand(rank_one_hessian.subs({a: 1, b: -eps**2, c: 0, d: 1,
                                                   m: (k*ell+ell**2)/(2*k)}))
c4 = 4*alpha+2*k+6*k*ell*(2*k+ell)*(k+ell)**2
c5 = 4*k*(k+ell)*(-k**2+3*k*ell+3*ell**2)
c6 = 4*alpha*(2*k**2+2*k*ell+3*ell**2)+10*k*ell*(k+ell)
c8 = 4*alpha*k**2*(k+ell)**2+2*k*ell*(k+ell)**3
equal("D=0 exact witness polynomial", rank_one_hessian,
      -4*k**2*eps**3+c4*eps**4+c5*eps**5+c6*eps**6+c8*eps**8)
assert sp.Poly(rank_one_hessian, eps).coeff_monomial(eps**3) == -4*k**2
for degree in (0, 1, 2):
    equal(f"D=0 witness has no epsilon^{degree} term", rank_one_hessian.coeff(eps, degree))

# H's pointwise Bregman bounds used in the universal integral proof.
s, r, h = sp.symbols("s r h", real=True)
R = 2*s*r+4*h**2+4*h*r+r**2
equal("H Bregman square identity 1", R-2*s*r, 4*(h+r/2)**2)
equal("H Bregman square identity 2", R-r**2/3, 2*(s*r-h**2)+6*(h+r/3)**2)

# Explicit polarization checks for the mixed Taylor terms.
Ua, Ub, Uc, Ud, rho, zeta = sp.symbols("Ua Ub Uc Ud rho zeta", real=True)
U = (Ua, Ub, Uc, Ud)
sub_background = {a: rho+Ua+zeta*a, b: Ub+zeta*b, c: Uc+zeta*c, d: rho+Ud+zeta*d}
expanded_background = sp.Poly(sp.expand(G.subs(sub_background, simultaneous=True)), zeta)
G_U_plus = sp.Poly(sp.expand(G.subs({z: uz+zeta*z for z, uz in zip(variables, U)}, simultaneous=True)), zeta)
DC_U = sum(sp.diff(C, z)*uz for z, uz in zip(variables, U))
equal("mixed quadratic Taylor identity", expanded_background.coeff_monomial(zeta**2),
      rho**2*(Q+3*ell*j)+rho*DC_U+G_U_plus.coeff_monomial(zeta**2))
equal("mixed cubic Taylor identity", expanded_background.coeff_monomial(zeta**3),
      rho*C+G_U_plus.coeff_monomial(zeta**3))

result = {
    "status": "ALL_EXACT_IDENTITIES_PASS",
    "scope": "Symbolic identities only; REPORT.md supplies the universal mathematical proof.",
    "sympy_version": sp.__version__,
    "checks": CHECKS,
    "construction_report_read": False,
    "pinned_checkout": "/Users/harjas/Documents/ChatGPT/ultra/work/astra-global-completion-axis-20261015",
    "pinned_revision": "ab5118e70a7e6a0dd39e75dd563d3a3f50b06b25",
    "D_zero_witness_coefficients": {f"c{n}": str(q) for n, q in ((4,c4),(5,c5),(6,c6),(8,c8))},
}
(OUT / "verification.json").write_text(json.dumps(result, indent=2)+"\n")
receipt = {
    "recorded_utc": datetime.now(timezone.utc).isoformat(),
    "status": result["status"],
    "verification_sha256": hashlib.sha256((OUT / "verification.json").read_bytes()).hexdigest(),
    "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "report_sha256": hashlib.sha256((OUT / "REPORT.md").read_bytes()).hexdigest() if (OUT / "REPORT.md").exists() else None,
    "read_scope": ["parent task message and candidate polynomial", "pinned W/AGENTS.md and W/00_START_HERE.txt",
                   "memory registry lines 1-50 for provenance and scope guidance"],
    "construction_proof_read": False,
    "finite_tests_used_as_universal_proof": False,
    "analytic_dependency": "Standard L4 boundedness of the planar Beurling transform / constant-coefficient elliptic estimate, explicitly stated in REPORT.md.",
}
(OUT / "receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
print(json.dumps({"status": result["status"], "exact_checks": len(CHECKS),
                  "construction_report_read": False, "output": str(OUT)}, indent=2))
