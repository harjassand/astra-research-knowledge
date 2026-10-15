#!/usr/bin/env python3
"""Exact algebraic verification of the independent sharp acoustic certificate.

Dependencies: sympy. Reads only the adjacent certificate; writes only the
adjacent receipt. No grids, floating point, optimization, or external files.
Analytic sign implications and universal quantifiers are proved in REPORT.md.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import sympy as s

HERE = Path(__file__).resolve().parent
CERT_PATH = HERE / "ACOUSTIC_CERTIFICATE.json"
cert_bytes = CERT_PATH.read_bytes()
certificate = json.loads(cert_bytes)

a, b, c, d, x, y, n, m, r, alpha, beta, gamma, delta, k, tau = s.symbols(
    "a b c d x y n m r alpha beta gamma delta k tau", real=True
)
loc = {str(q): q for q in (a, b, c, d, x, y, n, m, r, alpha, beta, gamma, delta)}
checks: dict[str, bool] = {}


def parse(expr: str):
    return s.sympify(expr, locals=loc)


def matrix(entries):
    return s.Matrix([[parse(v) for v in row] for row in entries])


def zero(name, expression):
    expressions = list(expression) if isinstance(expression, s.MatrixBase) else [expression]
    ok = all(s.cancel(v) == 0 for v in expressions)
    checks[name] = bool(ok)
    if not ok:
        raise AssertionError(f"{name}: nonzero residual")


def exact_true(name, value):
    checks[name] = bool(value)
    if not value:
        raise AssertionError(name)


def positive_rational_coefficients(expr, variable):
    """Certify positivity for variable>0 from positive polynomial coefficients."""
    numerator, denominator = s.fraction(s.cancel(expr))
    polys = [s.Poly(numerator, variable), s.Poly(denominator, variable)]
    return all(
        all(coefficient >= 0 for coefficient in polynomial.all_coeffs())
        and any(coefficient > 0 for coefficient in polynomial.all_coeffs())
        for polynomial in polys
    )


variables = s.Matrix([a, b, c, d])
u = a * a + c * c
j = a * d - b * c
H = ((a - d) ** 2 + (b + c) ** 2) ** 2
F = alpha * H + r * (r - 1) * u**2 / 6 + j**2 + r * u * j
zero("certificate_polynomial", F - parse(certificate["family"]))

direction = s.Matrix([n, m, 0, 0])
hessian = s.hessian(F, variables)
q_abcd = (direction.T * hessian * direction)[0]
q = s.expand(q_abcd.subs({b: y - c, d: a - x}))
J = a * a + c * c - a * x - c * y
Jp = (a - x) * n - c * m
q_displayed = (
    4 * alpha * ((x * x + y * y) * (n * n + m * m) + 2 * (n * x + m * y) ** 2)
    + s.Rational(2, 3) * r * (r - 1) * n * n * (3 * a * a + c * c)
    + 2 * Jp**2
    + r * (2 * n * n * J + 4 * a * n * Jp)
)
zero("direct_hessian_coordinate_formula", q - q_displayed)

z = s.Matrix([a, c, x, y])
M = s.hessian(q, z) / 2
floor = parse(certificate["sharp_floor"])
L = matrix(certificate["factor_L"])
weights = [parse(entry) for entry in certificate["factor_W_diagonal"]]
W = s.diag(*weights)
N = matrix(certificate["alpha_slack_matrix"])
zero("universal_acoustic_matrix_factor", M - L.T * W * L - (alpha - floor) * N)
zero("universal_four_square_identity", q - (z.T * L.T * W * L * z)[0] - (alpha - floor) * (z.T * N * z)[0])
zero("H_slack_exact", (z.T * N * z)[0] - 4 * ((x*x+y*y)*(n*n+m*m)+2*(n*x+m*y)**2))

positive_parameter = s.symbols("positive_parameter", positive=True)
for lane, substitution in [("r_lt_minus_two", -2 - positive_parameter), ("r_gt_zero", positive_parameter)]:
    for index, coefficient in enumerate(weights):
        exact_true(f"positive_SOS_weight_{lane}_{index+1}", positive_rational_coefficients(coefficient.subs(r, substitution), positive_parameter))

P = M[:2, :2]
U = M[:2, 2:]
V = M[2:, 2:]
zero("first_block_determinant", P.det() - s.Rational(4, 3) * n**4 * r * (r+2) * (r+1)**2)
T = (V - U.T * P.inv() * U).applyfunc(s.cancel)
B = 4 * s.Matrix([[m*m+3*n*n, 2*m*n], [2*m*n, 3*m*m+n*n]])
K = r / (2 * (r+2)) * s.Matrix([
    [(3*m*m+(5*r+4)*(r+2)*n*n)/(r+1)**2, 3*m*n/(r+1)],
    [3*m*n/(r+1), 3*n*n],
])
zero("Schur_complement_formula", T - alpha*B + K)
wv = s.Matrix([(2*r+1)*n/(r+1), 3*m])
T_floor_factor = r/(2*(r+2)) * (wv*wv.T + s.diag(3*r*(r+2)*m*m/(r+1)**2, 0))
zero("Schur_complement_PSD_factor", T.subs(alpha, floor) - T_floor_factor)
zero("Schur_floor_determinant", T_floor_factor.det() - 27*m**4*r**3/(4*(r+1)**2*(r+2)))


def hessian_at(background, direction_vec):
    sub = dict(zip(list(variables), list(background)))
    return (direction_vec.T * hessian.subs(sub) * direction_vec)[0]


sharp_A = matrix(certificate["sharp_witness_A"])
sharp_P = matrix(certificate["sharp_witness_P"])
sharp_value = hessian_at(sharp_A, s.Matrix(list(sharp_P)))
zero("sharp_necessity_witness", sharp_value - parse(certificate["sharp_witness_value"]))
zero("sharp_necessity_floor", sharp_value - 16*(r+2)**2*(alpha-floor))

bad_A = matrix(certificate["excluded_open_interval_witness_A"])
bad_value = hessian_at(bad_A, s.Matrix([1, 0, 0, 0]))
zero("excluded_open_interval_witness", bad_value - parse(certificate["excluded_open_interval_value"]))
exact_true("excluded_open_interval_strict_sign", positive_rational_coefficients((-bad_value).subs(r, -2*positive_parameter/(1+positive_parameter)), positive_parameter))

endpoint_A = matrix(certificate["excluded_endpoint_witness_A"])
endpoint_value = hessian_at(endpoint_A, s.Matrix([1, 0, 0, 0])).subs(r, -2)
zero("excluded_r_minus_two_witness", endpoint_value - parse(certificate["excluded_endpoint_value"]))

q_zero_r = q.subs(r, 0)
zero("r_zero_acoustic_certificate", q_zero_r - 2*Jp**2 - 4*alpha*((x*x+y*y)*(n*n+m*m)+2*(n*x+m*y)**2))

# Left rotation invariance: invariants suffice for every proper rotation.
rotation_parameter = s.symbols("rotation_parameter", real=True)
rotation = s.Matrix([
    [(1-rotation_parameter**2)/(1+rotation_parameter**2), -2*rotation_parameter/(1+rotation_parameter**2)],
    [2*rotation_parameter/(1+rotation_parameter**2), (1-rotation_parameter**2)/(1+rotation_parameter**2)],
])
A = s.Matrix([[a, b], [c, d]])
rotated = rotation*A
rotation_sub = dict(zip(list(variables), list(rotated)))
for invariant_name, invariant in [("u", u), ("j", j), ("H", H)]:
    zero(f"left_rotation_invariance_{invariant_name}", invariant.subs(rotation_sub, simultaneous=True) - invariant)
zero("left_minus_identity_invariance", F.subs({a:-a,b:-b,c:-c,d:-d}, simultaneous=True)-F)

interval = [parse(value) for value in certificate["requested_interval"]]
for index, endpoint in enumerate(interval):
    zero(f"endpoint_floor_{index+1}", floor.subs(r, endpoint) - parse(certificate["pointwise_endpoint_floors"][index]))
zero("floor_derivative", s.diff(floor, r) - 3/(4*(r+2)**2))
zero("uniform_floor", floor.subs(r, interval[1]) - parse(certificate["uniform_floor"]))
zero("failed_heat_continuation_parameter_floor", floor.subs(r, -s.Rational(8,3)) - s.Rational(3,2))

# Full four-coefficient cone: derive acoustic tests and check decomposition.
G = alpha*H + beta*u**2 + gamma*j**2 + delta*u*j
G_hessian = s.hessian(G, variables)
At = s.Matrix([[1, -k*tau], [k*tau, 1]])
Pt = s.Matrix([tau, 1, 0, 0])
At_sub = dict(zip(list(variables), list(At)))
q_t = (Pt.T * G_hessian.subs(At_sub) * Pt)[0]
first_bracket = 6*beta+delta - 2*delta*(k-1) + gamma*(k-1)**2
zero("full_cone_first_acoustic_necessity", q_t - 2*tau**2*first_bracket - 2*(2*beta+delta)*k**2*tau**4)
first_matrix = matrix(certificate["full_coefficient_cone"]["first_PSD_matrix"])
zero("full_cone_first_matrix_quadratic", first_bracket - (s.Matrix([1,1-k]).T*first_matrix*s.Matrix([1,1-k]))[0])

offdiag_A = s.Matrix([[0, y-c], [c, 0]])
offdiag_sub = dict(zip(list(variables), list(offdiag_A)))
offdiag_dir = s.Matrix([1,0,0,0])
offdiag_q = (offdiag_dir.T*G_hessian.subs(offdiag_sub)*offdiag_dir)[0]
zero("full_cone_second_acoustic_necessity", offdiag_q - 2*(2*beta+delta)*c*c + 2*delta*c*y - 4*alpha*y*y)
second_matrix = matrix(certificate["full_coefficient_cone"]["second_PSD_matrix"])
congruence = s.diag(1/s.sqrt(2), -s.sqrt(2))
zero("full_cone_second_matrix_congruence", congruence.T*second_matrix*congruence - s.Matrix([[4*alpha,-delta],[-delta,2*(2*beta+delta)]]))

rho = parse(certificate["full_coefficient_cone"]["rho_for_delta_nonzero"])
lam = parse(certificate["full_coefficient_cone"]["lambda_for_delta_nonzero"])
residual_j = parse(certificate["full_coefficient_cone"]["residual_j_squared_coefficient"])
residual_H = parse(certificate["full_coefficient_cone"]["residual_H_coefficient"])
sharp_rho_F = F.subs(alpha, floor).subs(r, rho)
zero("full_cone_polynomial_decomposition", G - lam*sharp_rho_F - residual_j*j*j - residual_H*H)
zero("full_cone_rho_plus_two", rho+2 - 3*(2*beta+delta)/delta)
zero("full_cone_lambda_delta_over_rho", lam - delta/rho)
zero("full_cone_beta_coefficient", lam*rho*(rho-1)/6 - beta)
zero("full_cone_alpha_coefficient", lam*floor.subs(r,rho) - delta**2/(8*(2*beta+delta)))
zero("full_cone_first_determinant", first_matrix.det() - gamma*(6*beta+delta)+delta**2)
zero("full_cone_second_determinant", second_matrix.det() - 8*alpha*(2*beta+delta)+delta**2)
for name, singular_sub in [
    ("gamma_zero", {gamma:0}),
    ("first_diagonal_zero", {beta:-delta/6}),
]:
    zero(f"full_cone_{name}_forces_delta_zero", first_matrix.det().subs(singular_sub) + delta**2)
for name, singular_sub in [
    ("alpha_zero", {alpha:0}),
    ("second_diagonal_zero", {beta:-delta/2}),
]:
    zero(f"full_cone_{name}_forces_delta_zero", second_matrix.det().subs(singular_sub) + delta**2)
zero("full_cone_delta_zero_decomposition", G.subs(delta,0) - alpha*H - beta*u*u - gamma*j*j)

receipt = {
    "schema": "astra-independent-sharp-acoustic-verification/v1",
    "status": "PASS",
    "certificate_sha256": hashlib.sha256(cert_bytes).hexdigest(),
    "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "python": sys.version.split()[0],
    "sympy": s.__version__,
    "checks_count": len(checks),
    "checks": checks,
    "family_ROC_floor": str(floor),
    "family_ROC_domain": certificate["admissible_r"],
    "full_four_coefficient_ROC_cone_audited": True,
    "no_grid_or_floating_point": True,
    "qc_below_inherited_floor": "UNKNOWN",
    "qc_full_four_coefficient_cone": "UNKNOWN",
    "historical_priority": "UNKNOWN",
    "external_mathematical_review": "NOT_PERFORMED",
}
receipt_path = HERE / "VERIFICATION.json"
receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({"status": "PASS", "checks_count": len(checks), "certificate_sha256": receipt["certificate_sha256"], "receipt": str(receipt_path)}))
