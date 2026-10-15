#!/usr/bin/env python3
"""Finite algebra and local-ramp checks; this does not prove the infinite theorem."""
from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import sympy as sp

HERE = Path(__file__).resolve().parent
mp.mp.dps = 70
checks = []


def record(name, passed, **detail):
    checks.append({"name": name, "passed": bool(passed), **detail})


g = sp.symbols("g", real=True)
n = sp.symbols("n", positive=True, integer=True)
numerator = sp.exp(2*g)/16 + sp.exp(-2*g) - sp.Rational(1, 2) + 1/n
square = (sp.exp(g)/4-sp.exp(-g))**2+1/n
record("diagonal_counterexample_Laplace_square", sp.simplify(numerator-square) == 0)
record("diagonal_counterexample_mass", sp.simplify(numerator.subs(g, 0)-(sp.Rational(9, 16)+1/n)) == 0)
critical = sp.simplify(numerator.subs(g, sp.log(2))/(sp.Rational(9, 16)+1/n))
record("diagonal_counterexample_critical_value", sp.simplify(critical-16/(9*n+16)) == 0,
       formula=str(critical), values={str(k): str(Fraction(16, 9*k+16)) for k in [1, 2, 10, 100, 10000]})
variations = []
for k in [1, 2, 3, 10, 100, 10000]:
    var = (Fraction(1, 16)+1+abs(-Fraction(1, 2)+Fraction(1, k)))/(Fraction(9, 16)+Fraction(1, k))
    variations.append({"n": k, "total_variation": str(var)})
record("diagonal_counterexample_uniform_variation_sample", all(Fraction(x["total_variation"]) <= Fraction(25, 9) for x in variations),
       values=variations, scope="Exact rational values at six finite indices; the proof supplies the all-index bound.")

# For exp(-F), the absolute sum of coefficients in each formal derivative
# equals the corresponding Bell number, exactly the bound used in the proof.
x = sp.symbols("x")
F = sp.Function("F")
bell_values = []
for k in range(1, 9):
    expression = sp.expand(sp.diff(sp.exp(-F(x)), x, k)/sp.exp(-F(x)))
    derivatives = [sp.diff(F(x), x, j) for j in range(1, k+1)]
    substitutions = {derivatives[j-1]: sp.Symbol(f"z{j}") for j in range(1, k+1)}
    polynomial = sp.Poly(expression.xreplace(substitutions), *substitutions.values())
    coefficient_sum = sum(abs(c) for c in polynomial.coeffs())
    bell_values.append({"order": k, "coefficient_sum": int(coefficient_sum), "Bell": int(sp.bell(k))})
record("partition_chain_rule_counts_orders_1_to_8", all(row["coefficient_sum"] == row["Bell"] for row in bell_values), values=bell_values)

# A two-dimensional radial derivative fixture. The stated constants A_k
# bound each coordinate derivative via partitions of singleton/pair blocks.
def radial_constant(k):
    result = Fraction(0)
    for pairs in range(k//2+1):
        singles = k-2*pairs
        blocks = singles+pairs
        partitions = math.factorial(k)//(math.factorial(singles)*math.factorial(pairs)*2**pairs)
        falling = Fraction(1)
        for j in range(blocks):
            falling *= Fraction(1, 2)-j
        result += partitions*abs(falling)*2**blocks
    return result

xx, yy = sp.symbols("xx yy", real=True)
radial = sp.sqrt(9+xx*xx+yy*yy)
radial_rows = []
for k in range(2, 7):
    constant = radial_constant(k)
    for j in range(k+1):
        derivative = sp.diff(radial, xx, j, yy, k-j)
        evaluate = sp.lambdify((xx, yy), derivative, "mpmath")
        for xval, yval in [(0, 0), (1, 2), (20, -3), (mp.mpf("1e6"), mp.mpf("-1e6"))]:
            rho = mp.sqrt(9+xval*xval+yval*yval)
            bound = mp.mpf(constant.numerator)/constant.denominator*rho**(1-k)
            ratio = abs(evaluate(xval, yval))/bound
            radial_rows.append({"order": k, "x_derivatives": j, "point": [str(xval), str(yval)], "ratio": float(ratio)})
record("Cartesian_radial_derivative_bound_finite_fixture", all(row["ratio"] <= 1+1e-30 for row in radial_rows),
       max_ratio=max(row["ratio"] for row in radial_rows), tested_cases=len(radial_rows),
       constants={str(k): str(radial_constant(k)) for k in range(1, 9)},
       scope="Finite derivative fixtures; the partition argument proves the general bound.")

# Local finite prefix of the literal C-infinity ramp construction, for
# T=delta+delta'', m=a=1, C=2, N=2, epsilon=1/4. H(g)=1+g^2 has margin >=1.
# Only one ramp is evaluated, in a region where the full construction
# agrees with that prefix. This prefix alone is not an all-moment kernel.
epsilon = mp.mpf(1)/4
B = mp.mpf(4)
A0 = 16*mp.e
beta0 = min(1/B, epsilon/(A0*mp.e*4))
beta1 = min(1/B, epsilon/(A0*mp.exp(2)*9))
L0 = max(1, 2/beta0)

def bump(t):
    if t <= 0 or t >= 1:
        return mp.mpf(0)
    return mp.exp(-1/(t*(1-t)))

bump_integral = mp.quad(bump, [0, mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf("0.75"), 1])
# d_1 <= 2 exp(4/3) < 8 follows by integrating b over [1/4,3/4].
D = mp.mpf(13)  # 1+A2+B21+B22*8 = 1+2+2+8
L1 = max(1, 4*D/beta1)
R1 = max(4, 2+8*D/beta1)

def theta(t):
    if t <= 0:
        return mp.mpf(0)
    if t >= 1:
        return mp.mpf(1)
    return mp.quad(bump, [0, t])/bump_integral

def slope_and_curvature(r):
    t = (r-R1)/L1
    slope = r/mp.sqrt(L0*L0+r*r)+theta(t)
    curvature = L0*L0/(L0*L0+r*r)**mp.mpf("1.5") + bump(t)/(bump_integral*L1)
    return slope, curvature

ramp_rows = []
points = [mp.mpf(0), L0, R1-2, R1-1, R1, R1+L1/4, R1+L1/2, R1+3*L1/4, R1+L1, R1+L1+10]
for r in points:
    slope, curvature = slope_and_curvature(r)
    H = 1+slope*slope
    output_ratio = 1+slope*slope-curvature
    relative_error = curvature/H
    target = beta0 if r < R1-1 else beta1
    neighborhood_values = [slope_and_curvature(abs(r-1+mp.mpf(2)*j/20))[1] for j in range(21)]
    ramp_rows.append({"radius": mp.nstr(r, 20), "slope": mp.nstr(slope, 20),
                      "curvature": mp.nstr(curvature, 20), "relative_error": mp.nstr(relative_error, 20),
                      "M_over_p": mp.nstr(output_ratio, 20), "sampled_local_curvature_max": mp.nstr(max(neighborhood_values), 20),
                      "tolerance": mp.nstr(target, 20),
                      "positive": output_ratio > 0, "relative_bound": relative_error <= epsilon,
                      "sampled_jet_bound": max(neighborhood_values) <= target})
record("literal_smooth_first_ramp_local_fixture", all(row["positive"] and row["relative_bound"] and row["sampled_jet_bound"] for row in ramp_rows),
       beta0=mp.nstr(beta0, 25), beta1=mp.nstr(beta1, 25), L0=mp.nstr(L0, 25), L1=mp.nstr(L1, 25), R1=mp.nstr(R1, 25),
       d1_numerical=mp.nstr(mp.exp(-4)/bump_integral, 25), d1_analytic_upper_bound="2*exp(4/3) < 8",
       values=ramp_rows, scope="Ten radii and 21-point local neighborhoods. Finite diagnostics, not a global or interval proof.")

out = {"status": "PASS" if all(c["passed"] for c in checks) else "FAIL",
       "scope": "Exact finite symbolic checks and high-precision finite local diagnostics only. No theorem certification or physical validation.",
       "mpmath_decimal_precision": mp.mp.dps, "checks": checks,
       "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/"CHECKS.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps({"status": out["status"], "checks": [{"name": c["name"], "passed": c["passed"]} for c in checks]}, indent=2))
raise SystemExit(0 if out["status"] == "PASS" else 1)
