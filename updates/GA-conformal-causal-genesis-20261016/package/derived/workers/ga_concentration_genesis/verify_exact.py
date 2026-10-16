#!/usr/bin/env python3
"""Finite exact receipts; this is not a verifier of continuum compactness."""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "originals" / "conformal_packet" / "RESEARCH_REPORT.md"
checks: list[dict[str, object]] = []


def equal(name: str, actual: sp.Expr, expected: sp.Expr = sp.Integer(0)) -> None:
    residual = sp.factor(sp.simplify(actual - expected))
    if residual != 0:
        raise RuntimeError(f"{name}: nonzero residual {residual}")
    checks.append({"name": name, "passed": True})


def require(name: str, condition: bool) -> None:
    if not condition:
        raise RuntimeError(name)
    checks.append({"name": name, "passed": True})


r = sp.symbols("r", positive=True)
a, b, c, d, background = sp.symbols("a b c d background", real=True)
sigma = r + 1
kappa = r * (r + 2) / 3
alpha = 3 * r / (8 * (r + 2))
beta = r * (r - 1) / 6
t = (2 * r + 1) / 3


def energy(aa: sp.Expr, bb: sp.Expr, cc: sp.Expr, dd: sp.Expr) -> sp.Expr:
    uu = aa**2 + cc**2
    vv = bb**2 + dd**2
    jj = aa * dd - bb * cc
    return alpha * (uu + vv - 2 * jj)**2 + beta * uu**2 + jj**2 + r * uu * jj


u, v, j, w = a*a+c*c, b*b+d*d, a*d-b*c, a*b+c*d
q = sigma*a+d
P = 2*a*q*q-(r+2)*q*a*a+r*q*c*c-2*q*b*c-kappa*a**3-kappa*a*c*c
J = energy(a, b, c, d)
expanded = sp.Poly(
    sp.expand(energy(a + background, b, c, d + background)
              - energy(background, 0, 0, background)),
    background,
)
equal("conformal constant coefficient", expanded.nth(0), J)
equal("cubic density", expanded.nth(1), P)
equal("raw quadratic coefficient", expanded.nth(2),
      q*q+kappa*c*c+(r+2)*j)
equal("linear Taylor integral is a gradient-linear expression",
      expanded.nth(3), (r+2)*((2*r+3)*a/3+d))

M = sp.Matrix([
    [t*t, sp.Rational(1, 3), 2*t],
    [sp.Rational(1, 3), 1, -2],
    [2*t, -2, sp.Rational(16, 3)+1/alpha],
])
z = sp.Matrix([u, v, j])
equal("positive Gram identity", J, alpha*(z.T*M*z)[0]+4*alpha*w*w/3)
equal("first principal minor", M[:1, :1].det(), t*t)
equal("second principal minor", M[:2, :2].det(), 4*r*(r+1)/9)
equal("third principal minor", M.det(), 16*(r+1)/27)
inverse_trace = (15*r**3+31*r**2+46*r+40)/(4*r*(r+1))
equal("inverse trace", sp.trace(M.inv()), inverse_trace)
coercivity = 3*r*r*(r+1)/(4*(r+2)*(15*r**3+31*r*r+46*r+40))
equal("explicit coercivity constant", alpha/(2*inverse_trace), coercivity)
equal("coercivity at r=1", coercivity.subs(r, 1), sp.Rational(1, 264))

# Scaling formulas use independently positive amplitude and length.
s, length, A0, C0, Q0, epsilon, weight = sp.symbols(
    "s length A0 C0 Q0 epsilon weight", positive=True
)
equal("quartic density scaling", J.subs({a:s*a,b:s*b,c:s*c,d:s*d}), s**4*J)
equal("cubic density scaling", P.subs({a:s*a,b:s*b,c:s*c,d:s*d}), s**3*P)
equal("quadratic density scaling",
      (q*q+kappa*c*c).subs({a:s*a,b:s*b,c:s*c,d:s*d}),
      s**2*(q*q+kappa*c*c))
equal("ratio scaling invariance",
      (s**3*length**2*C0)**2/
      (4*(s**4*length**2*A0)*(s**2*length**2*Q0)),
      C0*C0/(4*A0*Q0))

normalized_s = sp.sqrt(Q0/(A0*epsilon))
normalized_length = sp.sqrt(A0*epsilon**2/Q0**2)
equal("single bubble A normalization", normalized_s**4*normalized_length**2*A0, 1)
equal("single bubble Q normalization", normalized_s**2*normalized_length**2*Q0, epsilon)
equal("single bubble C normalization", normalized_s**3*normalized_length**2*C0,
      sp.sqrt(epsilon)*C0/sp.sqrt(A0*Q0))
cloud_length = sp.sqrt(A0*epsilon**2*weight/Q0**2)
equal("cloud component A", normalized_s**4*cloud_length**2*A0, weight)
equal("cloud component Q", normalized_s**2*cloud_length**2*Q0, epsilon*weight)
equal("cloud component C", normalized_s**3*cloud_length**2*C0,
      sp.sqrt(epsilon)*weight*C0/sp.sqrt(A0*Q0))
equal("cloud fourth power", normalized_s**4*cloud_length**2, weight/A0)
equal("cloud support area exponent", cloud_length**2,
      A0*epsilon**2*weight/Q0**2)

target_A, target_Q = sp.symbols("target_A target_Q", positive=True)
cone_s = sp.sqrt(target_A*Q0/(target_Q*A0))
cone_length = sp.sqrt(target_Q**2*A0/(target_A*Q0**2))
equal("cone rescaling A", cone_s**4*cone_length**2*A0, target_A)
equal("cone rescaling Q", cone_s**2*cone_length**2*Q0, target_Q)
equal("cone rescaling C squared", (cone_s**3*cone_length**2*C0)**2,
      target_A*target_Q*C0*C0/(A0*Q0))

bound_D, h, threshold, bound_B, delta = sp.symbols(
    "bound_D h threshold bound_B delta", positive=True
)
equal("low a cubed exponent",
      threshold**sp.Rational(1,3)*(bound_D*h)**sp.Rational(4,3)/h,
      bound_D**sp.Rational(4,3)*(threshold*h)**sp.Rational(1,3))
equal("low a squared exponent",
      threshold**sp.Rational(2,3)*(bound_D*h)**sp.Rational(2,3),
      bound_D**sp.Rational(2,3)*(threshold*h)**sp.Rational(2,3))
require("high cubic Holder exponents",
        Fraction(2, 1)/Fraction(8, 3)+Fraction(1, 4) == 1)
equal("critical Markov exponent", bound_B**4/(delta/sp.sqrt(epsilon))**4,
      bound_B**4*epsilon**2/delta**4)
equal("high quadratic coefficient",
      2*(sigma+1)+(r+2)+r+2+sp.sqrt(kappa),
      4*r+8+sp.sqrt(kappa))

# Exact compact tent template. Piecewise products remain compatible.
x, y = sp.symbols("x y", real=True)
F_pieces = [(x, 1, 0, 2), (6-2*x, -2, 2, 3)]
G_pieces = [(y, 1, 0, 1), (2-y, -1, 1, 2)]


def one_dimensional_moment(pieces, variable, function_power, derivative_power):
    return sum(
        sp.integrate(function**function_power*derivative**derivative_power,
                     (variable, left, right))
        for function, derivative, left, right in pieces
    )


a4 = one_dimensional_moment(F_pieces,x,0,4)*one_dimensional_moment(G_pieces,y,4,0)
b4 = one_dimensional_moment(F_pieces,x,4,0)*one_dimensional_moment(G_pieces,y,0,4)
a2b2 = one_dimensional_moment(F_pieces,x,2,2)*one_dimensional_moment(G_pieces,y,2,2)
a3 = one_dimensional_moment(F_pieces,x,0,3)*one_dimensional_moment(G_pieces,y,3,0)
a2 = one_dimensional_moment(F_pieces,x,0,2)*one_dimensional_moment(G_pieces,y,2,0)
equal("tent a fourth", a4, sp.Rational(36,5))
equal("tent b fourth", b4, sp.Rational(96,5))
equal("tent mixed fourth", a2b2, sp.Rational(16,3))
equal("tent a cubic", a3, -3)
equal("tent a quadratic", a2, 4)
tent_A = alpha*(a4+2*a2b2+b4)+beta*a4
tent_C = r*t*a3
tent_Q = sigma*sigma*a2
equal("tent A", tent_A, r*(12*r*r+12*r+115)/(10*(r+2)))
equal("tent C", tent_C, -r*(2*r+1))
equal("tent Q", tent_Q, 4*(r+1)**2)
tent_ratio = sp.factor(tent_C**2/(4*tent_A*tent_Q))
equal("tent positive ratio", tent_ratio,
      5*r*(r+2)*(2*r+1)**2/(8*(r+1)**2*(12*r*r+12*r+115)))
equal("tent ratio at r=1", tent_ratio.subs(r,1), sp.Rational(135,4448))

actual_A0 = tent_A.subs(r, 1)
actual_Q0 = tent_Q.subs(r, 1)
actual_C0 = tent_C.subs(r, 1)
actual_epsilon = sp.Rational(1, 10000)
actual_s = sp.sqrt(actual_Q0/(actual_A0*actual_epsilon))
weights = [sp.Rational(1,10),sp.Rational(2,10),sp.Rational(7,10)]
component_moments = []
for ww in weights:
    ll = sp.sqrt(actual_A0*actual_epsilon**2*ww/actual_Q0**2)
    component_moments.append((
        sp.simplify(actual_s**4*ll**2*actual_A0),
        sp.simplify(actual_s**3*ll**2*actual_C0),
        sp.simplify(actual_s**2*ll**2*actual_Q0),
    ))
cloud_A = sum(mm[0] for mm in component_moments)
cloud_C = sum(mm[1] for mm in component_moments)
cloud_Q = sum(mm[2] for mm in component_moments)
equal("rational-weight cloud A", cloud_A, 1)
equal("rational-weight cloud Q", cloud_Q, actual_epsilon)
equal("rational-weight cloud ratio", cloud_C**2/(4*cloud_A*cloud_Q),
      sp.Rational(135,4448))
equal("cloud Cauchy-Schwarz equality",
      sum(sp.sqrt(mm[0]*mm[2]) for mm in component_moments)**2,
      cloud_A*cloud_Q)

# Independent Laurent arithmetic for a periodic field and its integer replications.
def multiply(p, qq):
    out = {}
    for i, coefficient in p.items():
        for jj, second in qq.items():
            out[i+jj] = out.get(i+jj, Fraction(0))+coefficient*second
    return {key: value for key, value in out.items() if value}


def moment(p, degree):
    out = {0:Fraction(1)}
    for _ in range(degree):
        out = multiply(out, p)
    return out.get(0, Fraction(0))


carrier = {-2:Fraction(1,4),-1:Fraction(1,2),1:Fraction(1,2),2:Fraction(1,4)}
expected = {2:Fraction(5,8),3:Fraction(3,8),4:Fraction(99,128)}
for degree, expected_value in expected.items():
    require(f"periodic carrier moment degree {degree}",
            moment(carrier, degree) == expected_value)
for integer_frequency in (1,2,7,41):
    replicated = {integer_frequency*key:value for key,value in carrier.items()}
    require(f"periodic frequency replication n={integer_frequency}",
            all(moment(replicated,degree) == expected_value
                for degree,expected_value in expected.items()))
periodic_A = expected[4]/8
periodic_C = expected[3]
periodic_Q = 4*expected[2]
periodic_ratio = periodic_C**2/(4*periodic_A*periodic_Q)
require("periodic replication ratio", periodic_ratio == Fraction(8,55))

source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest() if SOURCE.exists() else None
receipt = {
    "status":"PASS",
    "scope":"Finite algebra and specified exact integrals only; no continuum theorem is machine-certified.",
    "analytic_inputs_not_machine_certified":[
        "Mixed-derivative interpolation and Hodge estimate",
        "Localized Holder and Markov arguments",
        "Periodic cutoff and Sobolev density arguments",
        "Weak convergence of cloud measures and vanishing spatial profiles",
        "Closure and dual characterization of the continuum moment cone",
    ],
    "source_report_sha256":source_hash,
    "checks":checks,
    "group_count":len(checks),
    "exact_tent_template":{
        "A":str(sp.factor(tent_A)),
        "C":str(sp.factor(tent_C)),
        "Q":str(sp.factor(tent_Q)),
        "ratio":str(tent_ratio),
        "ratio_r1":"135/4448",
    },
    "cloud_r1":{
        "epsilon":str(actual_epsilon),
        "weights":[str(ww) for ww in weights],
        "component_moments":[[str(value) for value in mm] for mm in component_moments],
        "total_A":str(cloud_A),
        "total_C":str(sp.simplify(cloud_C)),
        "total_Q":str(cloud_Q),
        "ratio":"135/4448",
    },
    "periodic_fixture_r1":{
        "map":"phi=(sin(x)+(1/4)sin(2x),0)",
        "replication":"phi_n(x,y)=phi(nx,ny)/n",
        "A":str(periodic_A),
        "C":str(periodic_C),
        "Q":str(periodic_Q),
        "ratio":str(periodic_ratio),
    },
}
out = HERE/"EXACT_RECEIPT.json"
out.write_text(json.dumps(receipt,indent=2)+"\n")
print(f"PASS: {len(checks)} finite exact checks")
print(f"Receipt: {out}")
