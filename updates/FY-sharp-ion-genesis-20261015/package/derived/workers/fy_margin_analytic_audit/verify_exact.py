#!/usr/bin/env python3
"""Independent symbolic support for the analytic audit, not its analytic proof."""

import hashlib
import json
from pathlib import Path
import platform

import sympy as s

HERE = Path(__file__).resolve().parent
r, t, p, b, c, z, S = s.symbols("r t p b c z S", real=True)
alpha = 3 * r / (8 * (r + 2))
beta = r * (r - 1) / 6
lam = r * (r + 2) / 3


def J(a, bb, cc, d):
    u = a * a + cc * cc
    j = a * d - bb * cc
    h = ((a - d) ** 2 + (bb + cc) ** 2) ** 2
    return alpha * h + beta * u * u + j * j + r * u * j


checks = {}


def zero(name, value):
    reduced = s.factor(value)
    checks[name] = {"passed": reduced == 0, "residual": str(reduced)}
    if reduced != 0:
        raise AssertionError((name, reduced))


poly = s.Poly(s.expand(J(t + p, b, c, t + z) - J(t, 0, 0, t)), t)
detq = p * z - b * c
soft = (r + 1) * p + z
zero("quadratic_contact_form_mod_determinant", poly.coeff_monomial(t**2) - soft**2 - lam*c**2 - (r+2)*detq)
zero("cubic_contact_expression", poly.coeff_monomial(t).subs(z, S-(r+1)*p) - (2*p*S**2 + S*(-2*b*c+r*c**2-(r+2)*p**2) - lam*p*(c**2+p**2)))
zero("constant_coefficient", poly.coeff_monomial(1) - J(p,b,c,z))
zero("linear_cubic_background_term", poly.coeff_monomial(t**3) - (r+2)*((2*r+3)*p+3*z)/3)
zero("determinant_soft_reexpression", detq.subs(z, S-(r+1)*p) - (p*S-(r+1)*p**2-b*c))
zero("sharp_pure_shear_at_every_t", J(t,b,0,t)-J(t,0,0,t)-alpha*b**4)

a, bb, cc = s.symbols("a bb cc", positive=True)
zero("scalar_rank_one_completion", a+bb+3*bb**2/(8*a) - (a/3+3*(bb+4*a/3)**2/(8*a)))

x1,x2,k1,k2=s.symbols("x1 x2 k1 k2", real=True)
rankone=J(x1*k1,x1*k2,x2*k1,x2*k2)
zero("rank_one_quartic_value", rankone - ((x1*x1+x2*x2)**2)*(alpha*(k1*k1+k2*k2)**2+beta*k1**4))

report = {
    "status": "PASS_EXACT_ALGEBRA_ONLY",
    "python": platform.python_version(),
    "sympy": s.__version__,
    "source_pin": "b32943eeb62d0d79929a9e572a344219a785ebf9",
    "checks": checks,
    "analytic_scope": "No mechanical certification of interpolation, multiplier bounds, compactness, novelty, or unrestricted coercivity.",
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
out = json.dumps(report, indent=2, sort_keys=True) + "\n"
(HERE / "EXACT_RECEIPT.json").write_text(out)
print(out, end="")
