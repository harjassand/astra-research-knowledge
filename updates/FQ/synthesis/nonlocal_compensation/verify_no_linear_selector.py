#!/usr/bin/env python3
"""Exact finite identities supporting NO_LINEAR_SELECTOR.md.

The analytic slow-strip limits and averaging argument are proved in the report;
this script checks their algebra, not a universal quantifier by finite sampling.
"""
import json
from pathlib import Path
import sympy as s

a, b, c, d, t, rho = s.symbols("a b c d t rho", real=True)
u, v, w, q = a*a+c*c, b*b+d*d, a*b+c*d, a*d-b*c
N = u+v
checks = {}

# Every even invariant quartic lies in the span of these six inputs.
U, V, W, Q = s.symbols("u v w q")
even_basis = [U**2, V**2, U*V, W**2, U*W, V*W]
poly = s.Poly((U+2*t*W+t*t*V)**2, t)
columns = []
for k in range(5):
    pk = s.Poly(poly.coeff_monomial(t**k), U, V, W)
    columns.append([pk.coeff_monomial(m) for m in even_basis])
columns.append([0, 0, 1, -1, 0, 0])  # q^2 = uv-w^2.
even_matrix = s.Matrix.hstack(*map(s.Matrix, columns))
assert even_matrix.det() != 0
checks["even_span"] = {"rank": even_matrix.rank(), "determinant": str(even_matrix.det())}

# Norm-square of X + (t+i*rho)Y and its reflection decomposition.
linear_x = a+t*b-rho*d
linear_y = c+t*d+rho*b
norm_square = s.expand(linear_x**2+linear_y**2)
assert s.expand(norm_square-(u+2*t*w+(t*t+rho*rho)*v-2*rho*q)) == 0
complex_energy = s.expand(norm_square**2)
even_part = (u+2*t*w+(t*t+rho*rho)*v)**2 + 4*rho*rho*q*q
odd_part = -4*rho*q*(u+2*t*w+(t*t+rho*rho)*v)
assert s.expand(complex_energy-even_part-odd_part) == 0
checks["complex_tilt_decomposition"] = True

# Compatible drift path: X = rho*A - t*B, Y=B.
ar, ai, br, bi = s.symbols("ar ai br bi", real=True)
sub = {a:rho*ar-t*br, c:rho*ai-t*bi, b:br, d:bi}
assert s.expand(complex_energy.subs(sub, simultaneous=True)
                -rho**4*((ar-bi)**2+(ai+br)**2)**2) == 0
checks["complex_drift_action_power"] = "rho^4 density times rho^-1 duration = rho^3"

# Real drift has density T^-4 and duration T; determinant square T^-2 times T.
T = s.symbols("T", positive=True)
real_energy = s.expand((u+2*t*w+t*t*v)**2)
sub_real = {a:ar/T-t*br, c:ai/T-t*bi, b:br, d:bi}
assert s.expand(real_energy.subs(sub_real, simultaneous=True)-(ar*ar+ai*ai)**2/T**4) == 0
assert s.expand((q*q).subs({a:ar/T,c:ai/T,b:br,d:bi}, simultaneous=True)
                -(ar*bi-ai*br)**2/T**2) == 0
checks["slow_strip_powers"] = {"real_convex_action":"T^-3", "determinant_square_action":"T^-1"}

# Three values of the shear parameter recover all three odd storage components.
odd_recovery = s.Matrix([[1, 0, 0], [1, 2, 1], [1, -2, 1]])
assert odd_recovery.det() == 4
checks["odd_recovery_determinant"] = str(odd_recovery.det())

# DM endpoint acoustic identity in e11; SO(2)xSO(2) gives every rank-one direction.
Fdm = N*N-4/s.sqrt(3)*N*q
acoustic_squares = (12*(a-d/s.sqrt(3))**2
    +2*(1+1/s.sqrt(3))*(b+c)**2
    +2*(1-1/s.sqrt(3))*(b-c)**2)
assert s.simplify(s.diff(Fdm,a,2)-acoustic_squares) == 0
checks["dm_acoustic_identity"] = True

# Direct finite negative strip Phi(x,y)=(x/2)(cos y,sin y), 0<=x<=2.
r = s.symbols("r", real=True)
H_density = (s.Rational(1,4)+r*r)**2
Fdm_density = H_density-4/s.sqrt(3)*(s.Rational(1,4)+r*r)*r/2
dm_action = s.simplify(2*s.integrate(Fdm_density,(r,0,1)))
H_action = s.simplify(2*s.integrate(H_density,(r,0,1)))
assert dm_action == s.Rational(103,120)-s.sqrt(3)/2
strict_action = s.simplify(dm_action+H_action/1000)
strict_rational_part = s.Rational(103103,120000)
assert strict_action == strict_rational_part-s.sqrt(3)/2
sign_margin = s.Rational(3,4)-strict_rational_part**2
assert sign_margin > 0
checks["strict_rank_one_convex_negative_entry"] = {
    "integrand":"F_DM + (1/1000)|A|^4",
    "action":str(strict_action),
    "squared_sign_margin":str(sign_margin),
    "action_approximation":str(s.N(strict_action,20)),
}

# Exact equality control for the convex family's arbitrary-interior optimum.
# Symmetry averaging reduces arbitrary competitors to one mode; this part is
# an analytic proof in EXACT_TILTED_CONVEX_ACTION.md, not a symbolic premise.
lam, duration = s.symbols("lam duration", positive=True)
ss = s.symbols("ss", real=True)
I = 3*(s.exp(4*lam*duration/3)-1)/(4*lam)
assert s.simplify(s.integrate(s.exp(4*lam*(duration-ss)/3),
                             (ss,0,duration))-I) == 0
equality_control = s.exp(lam*(duration-ss)/3)/I
# Clear the nonzero, x-independent normalizer before symbolic integration.
# It is positive for the present lam,T>0, but SymPy does not infer exp(z)>1
# in all integration branches and otherwise returns a spurious Piecewise.
endpoint_numerator = s.simplify(s.exp(lam*(duration-ss))*equality_control*I)
action_numerator = s.simplify(equality_control**4*I**4)
assert s.simplify(s.integrate(endpoint_numerator,(ss,0,duration))/I-1) == 0
assert s.simplify(s.integrate(action_numerator,(ss,0,duration))/I**4-I**(-3)) == 0
assert s.limit(I**(-3),duration,s.oo) == 0
assert s.limit(s.exp(4*lam*duration)*I**(-3),duration,s.oo) == 64*lam**3/27
I_negative = 3*(1-s.exp(-4*lam*duration/3))/(4*lam)
assert s.limit(I_negative**(-3),duration,s.oo) == 64*lam**3/27
assert s.limit(s.exp(-4*lam*duration)*I_negative**(-3),duration,s.oo) == 0
checks["exact_convex_mode_control"] = {
    "finite_duration": "incoming = |a|^4 / I(lambda,T)^3",
    "positive_frequency_free_incoming": "0",
    "negative_frequency_free_incoming": "(64/27) rho^3 |k|^3 |a|^4",
    "free_return": "opposite frequency orientation",
}

out = {"status":"PASS", "groups":len(checks), "checks":checks,
       "scope":"Finite exact algebra only. Analytic proof and universal quantifiers are in NO_LINEAR_SELECTOR.md."}
path = Path(__file__).with_name("exact_checks.json")
path.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
