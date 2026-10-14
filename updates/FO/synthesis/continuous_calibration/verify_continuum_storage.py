#!/usr/bin/env python3
"""Exact replay of the two-real-mode continuum storage certificate.

All source algebra is imported only from this worker's copied input tree.
This verifies the profile identity, the rational SOS Gram, its positive
definiteness, and the averaged determinant identity. The background
polyconvex completion is proved in REPORT.md by Calderon's 2x2 theorem;
this script does not claim to compute a symbolic lambda(B).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "source-copy" / "resonant"))
from profile_algebra import averaged  # type: ignore  # copied, pinned source

r, s, p, q = sp.symbols("r s p q", real=True)
G0, N0, _, det_mean = averaged(1, -1, False)
G0_report = (
    sp.Rational(107,24)*(p**4+q**4) + sp.Rational(107,6)*p**2*q**2
    - sp.Rational(29,2)*p**3*r + sp.Rational(29,2)*q**3*s
    + 19*p**2*r**2 + sp.Rational(25,2)*p**2*s**2
    + sp.Rational(25,2)*q**2*r**2 + 19*q**2*s**2
    + 29*p**2*q*s - 29*p*q**2*r - 51*p*q*r*s
    + 3*r**4 + 12*r**2*s**2 + 3*s**4
    - 12*p*r**3 - 24*p*r*s**2 + 24*q*r**2*s + 12*q*s**3
)
N0_report = (p**4+q**4+4*p**2*q**2 + 2*p**2*r**2+2*p**2*s**2
             + 2*q**2*r**2+2*q**2*s**2 - 4*p*q*r*s
             + r**4+4*r**2*s**2+s**4)
assert sp.expand(G0-G0_report) == 0
assert sp.expand(N0-N0_report) == 0
P0 = -3*r**4 + 3*s**4
residual = sp.Poly(sp.expand(G0 - sp.Rational(1,4)*N0
                              - p*sp.diff(P0,r) - q*sp.diff(P0,s)),
                    r, s, p, q)

# The monomial vector order used by quartic_sos_gram.txt:
# (q^2, p q, p^2, s q, s p, s^2, r q, r p, r s, r^2).
m = sp.Matrix([q**2, p*q, p**2, s*q, s*p, s**2, r*q, r*p, r*s, r**2])
Q = sp.Matrix([[sp.Rational(t) for t in line.split()]
               for line in (ROOT / "quartic_sos_gram.txt").read_text().splitlines()])
assert Q.shape == (10, 10)
assert Q == Q.T
assert sp.Poly(sp.expand((m.T*Q*m)[0] - residual.as_expr()), r,s,p,q).is_zero

leading = []
for k in range(1, 11):
    d = sp.factor(Q[:k,:k].det())
    assert d > 0, (k, d)
    leading.append(str(d))
pivots = [str(sp.factor(sp.Rational(leading[k]) / sp.Rational(leading[k-1])))
          if k else leading[k] for k in range(10)]

# Independently reconstruct the Hessian quadratic at arbitrary B and check
# that its profile average has the advertised determinant coefficient.
a,b,c,d = sp.symbols("a b c d", real=True)
B0,B1,B2,B3 = sp.symbols("B0 B1 B2 B3", real=True)
X = sp.Matrix([a,b,c,d]); B = sp.Matrix([B0,B1,B2,B3])
u = a*a+c*c; v = b*b+d*d; det = a*d-b*c
G = 3*(u+v-2*det)**2 + sp.Rational(35,24)*u**2 + det**2 - sp.Rational(5,2)*det*u
H = sp.hessian(G, X).subs(dict(zip(X, B)), simultaneous=True) / 2
xp = sp.Matrix([(p+q)*sp.cos(sp.Symbol('y')),
                 -(r+s)*sp.sin(sp.Symbol('y')),
                 (p-q)*sp.sin(sp.Symbol('y')),
                 (r-s)*sp.cos(sp.Symbol('y'))])
y=sp.Symbol('y', real=True)
# Rebuild with one common y symbol (the temporary symbol above is same-name).
xp = sp.Matrix([(p+q)*sp.cos(y), -(r+s)*sp.sin(y),
                (p-q)*sp.sin(y), (r-s)*sp.cos(y)])
Qprofile = sp.expand(sp.integrate((xp.T*H*xp)[0], (y,0,2*sp.pi))/(2*sp.pi))
det_profile = sp.simplify(sp.integrate(
    ((p+q)*(r-s)*sp.cos(y)**2 + (p-q)*(r+s)*sp.sin(y)**2),
    (y,0,2*sp.pi))/(2*sp.pi))
assert sp.expand(det_profile - (p*r-q*s)) == 0

A = (107*B0**2-174*B0*B3+75*B1**2+174*B1*B2+107*B2**2+75*B3**2)/6
C = (107*B0**2-174*B0*B3-78*B1**2-174*B1*B2-107*B2**2+78*B3**2)/6
L = -29*B0**2+51*B0*B3-24*B1**2-51*B1*B2-29*B2**2-24*B3**2
M = (29*B0**2-50*B0*B3-24*B1**2-50*B1*B2-29*B2**2+24*B3**2)/2
E = (25*B0**2-48*B0*B3+24*B1**2+48*B1*B2+25*B2**2+24*B3**2)/2
F = -13*B0**2+24*B0*B3+12*B1**2+24*B1*B2+13*B2**2-12*B3**2
expected_profile = (A*(p**2+q**2)+C*p*q+L*(p*r-q*s)
                    +M*(p*s-q*r)+E*(r**2+s**2)+F*r*s)
assert sp.expand(Qprofile-expected_profile) == 0

# The full homogeneous-quartic expansion has no odd-in-X y-average terms.
Gfull, _, _, _ = averaged(1, -1, True)
Gbackground = G.subs(dict(zip(X, B)), simultaneous=True)
assert sp.expand(Gfull-Gbackground-G0-Qprofile) == 0

out = {
    "scope": "Exact rational algebra for the two-real-mode profile storage; analytic background step is stated in REPORT.md.",
    "zero_background": {
        "eta": "1/4",
        "P0": "-3*r^4+3*s^4",
        "printed_G0_and_N0_formulas_match_source": True,
        "residual_total_degree": 4,
        "gram_basis": ["q^2","p*q","p^2","s*q","s*p","s^2","r*q","r*p","r*s","r^2"],
        "gram_positive_definite": True,
        "leading_principal_minors": leading,
        "ldl_pivots": pivots,
        "coefficient_identity": True,
    },
    "background": {
        "hessian_definition": "H_B = (1/2) D^2 G(B)",
        "profile_average_equals": str(Qprofile),
        "compact_coefficient_form_verified": True,
        "odd_terms_cancelled_exactly": True,
        "average_determinant_equals": str(det_profile),
        "lambda_lmi": "lambda(B)=sup{lambda in R: H_B-lambda*D is positive semidefinite}, D represents det(X)",
        "background_storage": "P_B(r,s)=P0(r,s)+lambda(B)*(r^2-s^2)/2",
    },
}
(ROOT / "continuum_storage_verification.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps({"gram_positive_definite": True,
                  "leading_principal_minors": leading,
                  "average_determinant": str(det_profile),
                  "profile_hessian_quadratic": str(Qprofile)}, indent=2))
