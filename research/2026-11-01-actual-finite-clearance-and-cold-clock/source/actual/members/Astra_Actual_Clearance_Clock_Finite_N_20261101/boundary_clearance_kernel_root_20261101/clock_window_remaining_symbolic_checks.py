#!/usr/bin/env python3
"""Exact algebra checks only; not a stochastic or validated numerical certificate."""
import hashlib
import json
from pathlib import Path
import sympy as s

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    "STOPPED_CLOCK_WINDOW_CONSUMER.md": "6e76a11da95461c91ad7ee708fd893b4752b661b342dd87289d7564907f01a94",
    "HISTORY_REMAINING_CLOCK_V1_f0ade880.md": "f0ade8800f84315e818adabdf9a7fdf7f9773487aea19e139603a5d08b647067",
    "REMAINING_CLOCK_OBSERVABLE.md": "3738ec11751d5e094e70c5f32d7dedfe2ff978403cd7b4b6be18816bbf0cf555",
}
hashes = {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in EXPECTED}
assert hashes == EXPECTED, (hashes, EXPECTED)
l,e,J,v,j,H,E,c,z = s.symbols("l e J v j H E c z", positive=True)
m = j*H/3+s.sqrt(2*v*H+(j*H/3)**2)
bl = J-1
be = s.Rational(3,2)*e*(1-J)-J/(2*l*l)
freedman_residual = s.simplify(m*m-2*H*(v+j*m/3))
pde_residual = s.simplify((1+3*l*l*e)*bl+2*l*l*be+1)
sensitivity = s.integrate((s.Rational(3,4)*z*z)**-3, (z,e,s.oo))
tail = s.integrate((s.Rational(64,135)*z**-5)**2 *
                   (s.Rational(8,9)*z**-4+s.Rational(3,2)*z), (z,E,s.oo))
expected_tail = s.Rational(4096,18225)*(s.Rational(8,117)*E**-13+s.Rational(3,16)*E**-8)
cone_bl = s.integrate((c*z*z)**-3, (z,e,s.oo))
cone_bll = s.integrate(3*(c*z*z)**-4, (z,e,s.oo))
assert freedman_residual == 0
assert pde_residual == 0
assert s.simplify(sensitivity-s.Rational(64,135)*e**-5) == 0
assert s.simplify(tail-expected_tail) == 0
assert s.simplify(cone_bl-1/(5*c**3*e**5)) == 0
assert s.simplify(cone_bll-3/(7*c**4*e**7)) == 0
total = s.Rational(11,4)+tail.subs(E,1)
result = {
    "scope": "exact symbolic consistency only; no stochastic bridge or validated scalar solver",
    "history": "Initial hash check rejected the concurrently repaired main file; the preserved original and complete repair diff were inspected, then all three exact inputs were bound here.",
    "source_sha256": hashes,
    "sympy_version": s.__version__,
    "freedman_quadratic_residual": str(freedman_residual),
    "transport_pde_residual": str(pde_residual),
    "origin_orbit_sensitivity_integral": str(sensitivity),
    "origin_orbit_variance_tail": str(s.factor(tail)),
    "variance_tail_difference_from_source": str(s.simplify(tail-expected_tail)),
    "deterministic_total_variance_ceiling": str(total),
    "deterministic_total_variance_ceiling_decimal_informational_only": str(s.N(total,18)),
    "separate_cone_bl_upper_bound": str(cone_bl),
    "separate_cone_bll_upper_bound": str(cone_bll),
    "all_assertions_passed": True,
}
out = ROOT/"clock_window_remaining_symbolic_checks.json"
out.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
