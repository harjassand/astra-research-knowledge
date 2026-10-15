#!/usr/bin/env python3
"""Exact algebra checks accompanying REPORT.md.

These checks do not verify the infinite-dimensional proof. The true-projection
examples are justified by their variational inequalities in the report.
"""
from pathlib import Path
import datetime
import hashlib
import json
import platform
import sys

import sympy as sp

OUT = Path(__file__).resolve().parent
results = {}


def record(name, expression, expected=0):
    value = sp.simplify(expression)
    difference = sp.simplify(value - expected)
    if difference != 0:
        raise AssertionError((name, value, expected, difference))
    results[name] = {
        "status": "PASS_EXACT_SYMBOLIC_IDENTITY",
        "value": str(value),
        "expected": str(expected),
    }


x, y = sp.symbols("x y", nonnegative=True)
p = sp.symbols("p", real=True)
s = x + y
record("row_factorization", x*x-y*y-2*x+1-(1-x-y)*(1-x+y))
record(
    "mellin_p_below_2_coefficient",
    (x-y)/(2-p)+2*x/(p-1)-s/p
    - 2*(x/(p-1)-y)/(p*(2-p)),
)
record(
    "mellin_p_above_2_coefficient",
    2*x/(p-1)-s/p-(x-y)/(p-2)
    - 2*((p-1)*y-x)/(p*(p-1)*(p-2)),
)

# An exact finite cyclic analogue of the periodic change-of-variables identity.
n = 7
hh = sp.symbols("h0:7")
zz = sp.symbols("z0:7")
lhs = sum(hh[j]*(zz[(j+1)%n]+zz[(j-1)%n]-2*zz[j]) for j in range(n))
rhs = -sum((hh[(j+1)%n]-hh[j])*(zz[(j+1)%n]-zz[j]) for j in range(n))
record("periodic_translation_identity", sp.expand(lhs-rhs))

t = sp.symbols("t", real=True)
lam = 1/(30*sp.pi**2)
v = lam*sp.sin(2*sp.pi*t)**3
h = -sp.diff(v, t)
hp = sp.diff(h, t)
point = sp.Rational(1, 12)
record("true_projection_pointwise_pairing", hp.subs(t, point), -sp.Rational(1, 4))
record("true_projection_input_gradient", 1+hp.subs(t, point), sp.Rational(3, 4))
record(
    "true_projection_integrated_gradient_pairing",
    sp.integrate(hp, (t,0,sp.Rational(1,2)))
    -sp.integrate(hp, (t,sp.Rational(1,2),1)),
    0,
)
record(
    "true_projection_nonorthogonal_potential_pairing",
    2*sp.integrate(v, (t,0,sp.Rational(1,2))),
    2/(45*sp.pi**3),
)

ls = sp.symbols("lambda", positive=True)
vs = ls*sp.sin(2*sp.pi*t)
hps = -sp.diff(vs, t, 2)
record(
    "second_true_projection_strict_integrated_pairing",
    sp.integrate(hps, (t,0,sp.Rational(1,2)))
    -sp.integrate(hps, (t,sp.Rational(1,2),1)),
    8*sp.pi*ls,
)

u, w = sp.symbols("u w", real=True)
eta = sp.sin(2*sp.pi*u)*sp.sin(2*sp.pi*w)
q1, q2 = sp.diff(eta, u), sp.diff(eta, w)
radius = sp.sqrt(q1*q1+q2*q2)
# This point is in the smooth active-clipping region radius > 1.
at = {u: sp.Rational(1,12), w: sp.Rational(1,8)}
record("clipping_active_radius", radius.subs(at), sp.sqrt(2)*sp.pi)
curl = sp.diff(q2/radius, u)-sp.diff(q1/radius, w)
record("clipped_gradient_nonzero_curl", curl.subs(at), sp.pi*sp.sqrt(3)/2)

# Majorization tangency, checked at representative exact exponents. The report
# supplies the proof for every real p >= 2; this finite check does not.
aa = sp.symbols("a", real=True)
for pp in (sp.Rational(5,2), sp.Integer(3), sp.Integer(4), sp.Integer(6)):
    cc = pp-1
    alpha = pp*(1-1/pp)**(pp-1)
    f = cc**pp*(1-aa)**pp-aa**pp-alpha*(cc-pp*aa)
    a0 = cc/pp
    record(f"majorization_tangent_value_p_{pp}", f.subs(aa,a0))
    record(f"majorization_tangent_derivative_p_{pp}", sp.diff(f,aa).subs(aa,a0))

output = {
    "schema": "astra.worker.projection_claim_audit.checks.v1",
    "run_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "python": sys.version,
    "platform": platform.platform(),
    "sympy": sp.__version__,
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "scope": "Exact finite algebra and displayed counterexample calculations only.",
    "infinite_dimensional_proof_verified_by_script": False,
    "premise_admission": False,
    "checks": results,
}
(OUT/"checks.json").write_text(json.dumps(output,indent=2)+"\n")
print(json.dumps({
    "status": "PASS",
    "exact_checks": len(results),
    "checks_path": str(OUT/"checks.json"),
    "infinite_dimensional_proof_verified_by_script": False,
    "premise_admission": False,
},indent=2))
