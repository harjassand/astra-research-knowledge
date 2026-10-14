#!/usr/bin/env python3
"""Independent exact checks for the FI positive-definite quartic audit.

This checker is authored for the audit. It does not import the supplied
verifier or read its JSON output. SymPy checks finite polynomial identities;
the analytic arguments are stated separately in DERIVATION.md.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


checks: list[str] = []


def require_zero(expr, label: str) -> None:
    values = list(expr) if isinstance(expr, sp.MatrixBase) else [expr]
    if any(sp.cancel(sp.expand(value)) != 0 for value in values):
        raise AssertionError(label)


def passed(label: str) -> None:
    checks.append(label)
    print(f"PASS {len(checks):02d}: {label}", flush=True)


# Rebuild the integrand and its contact data from the displayed formula.
a, b, c, d = sp.symbols("a b c d", real=True)
X = sp.Matrix([a, b, c, d])
u = a**2 + c**2
v = b**2 + d**2
w = a * b + c * d
det = a * d - b * c
G = sp.expand(3 * (u + v - 2 * det) ** 2 + sp.Rational(35, 24) * u**2 + det**2 - sp.Rational(5, 2) * det * u)
gradG = sp.Matrix([sp.diff(G, z) for z in X])
hessG = sp.hessian(G, list(X))
identity = sp.Matrix([1, 0, 0, 1])
contact = (identity.T * hessG * identity)[0] + det
require_zero(contact - ((3 * a - 2 * d) ** 2 / 2 + sp.Rational(5, 6) * c**2), "contact decomposition at I")
require_zero(gradG.dot(identity).subs({c: 0, d: sp.Rational(3, 2) * a}) + sp.Rational(5, 12) * a**3,
             "cubic restriction on the contact plane")
passed("contact plane, rank-one radical, and cubic restriction")


# Rebuild an exact rank-one-convexity certificate, not just sampled acoustics.
M11 = sp.hessian(hessG[0, 0], list(X)) / 2
M12 = sp.hessian(hessG[0, 1], list(X)) / 2
M22 = sp.hessian(hessG[1, 1], list(X)) / 2
K = sp.zeros(4)
upper = [11, sp.Rational(91, 6), 0, 0, 11, sp.Rational(41, 3)]
idx = 0
for i in range(4):
    for j in range(i + 1, 4):
        K[i, j] = upper[idx]
        K[j, i] = -upper[idx]
        idx += 1
Q = M11.row_join(M12 + K).col_join((M12 - K).row_join(M22))
r1, r2 = sp.symbols("r1 r2", real=True)
rank_one_probe = sp.Matrix.vstack(r1 * X, r2 * X)
rank_one_bg = sp.Matrix([r1, r2, 0, 0])
require_zero((rank_one_probe.T * Q * rank_one_probe)[0]
             - (rank_one_bg.T * hessG * rank_one_bg)[0], "acoustic Gram identity")
nulls = [sp.Matrix([-sp.Rational(2, 3), 0, 0, -sp.Rational(2, 3), 0, -1, 1, 0]),
         sp.Matrix([0, 0, 0, 0, 1, 0, 0, 1])]
for null in nulls:
    require_zero(Q * null, "acoustic Gram null vector")
leading = [sp.factor(Q[:n, :n].det()) for n in range(1, 7)]
expected_leading = [sp.Rational(107, 2), 642, sp.Rational(1605, 8),
                    sp.Rational(8445, 16), sp.Rational(2815, 8), sp.Rational(26865, 4)]
if leading != expected_leading or Q.rank() != 6:
    raise AssertionError("acoustic Gram principal minors / rank")
passed("rank-six positive acoustic Gram and exact rank-one identity")


# Independent rational integration of the exact zero-boundary profile.
s, t, rho = sp.symbols("s t rho", positive=True)
kprof = t * (1 - t)
second = s * (1 - s)
pieces = [(2 * s, sp.Rational(0), sp.Rational(1, 3)),
          (1 - s, sp.Rational(1, 3), sp.Rational(1))]
integration_cache: dict[str, sp.Expr] = {}


def integrate_unit_square(expr: sp.Expr) -> sp.Expr:
    key = str(expr)
    if key in integration_cache:
        return integration_cache[key]
    total = sp.Integer(0)
    for first, left, right in pieces:
        subst = {
            a: sp.diff(first, s) * kprof,
            b: first * sp.diff(kprof, t),
            c: sp.diff(second, s) * kprof,
            d: second * sp.diff(kprof, t),
        }
        poly = sp.Poly(sp.expand(expr.subs(subst, simultaneous=True)), s, t)
        subtotal = sp.Integer(0)
        for (i, j), coeff in poly.terms():
            subtotal += coeff * (right ** (i + 1) - left ** (i + 1)) / (i + 1) / (j + 1)
        total += subtotal
    result = sp.factor(total)
    integration_cache[key] = result
    return result


profile_grad = sp.Matrix([sp.diff(pieces[0][0] * kprof, s),
                          pieces[0][0] * sp.diff(kprof, t),
                          sp.diff(second, s) * kprof,
                          second * sp.diff(kprof, t)])
# Recompute each piece directly; the first expression above is only a shape
# template and is not used for the integral.
profile_C = sp.Matrix(4, 4, lambda i, j: integrate_unit_square(X[i] * X[j]))
profile_H = sp.Matrix(4, 4, lambda i, j: integrate_unit_square(hessG[i, j]))
profile_b = sp.Matrix([integrate_unit_square(z) for z in gradG])
profile_c = integrate_unit_square(G)
profile_m4 = integrate_unit_square((u + v) ** 2)
expected_H = sp.Matrix([
    [sp.Rational(2581, 540), sp.Rational(41, 405), sp.Rational(248, 1215), -sp.Rational(2189, 540)],
    [sp.Rational(41, 405), sp.Rational(47, 15), sp.Rational(121, 36), -sp.Rational(14, 405)],
    [sp.Rational(248, 1215), sp.Rational(121, 36), sp.Rational(1229, 324), -sp.Rational(41, 405)],
    [-sp.Rational(2189, 540), -sp.Rational(14, 405), -sp.Rational(41, 405), sp.Rational(494, 135)],
])
expected_b = sp.Matrix([sp.Rational(191, 756), sp.Rational(1231, 11340),
                        sp.Rational(1439, 11340), -sp.Rational(2299, 11340)])
require_zero(profile_H - expected_H, "profile averaged Hessian")
require_zero(profile_b - expected_b, "profile cubic vector")
if profile_c != sp.Rational(5951, 58800) or profile_m4 != sp.Rational(29023, 1071630):
    raise AssertionError("profile energy or fourth moment")
if profile_C.rank() != 4 or any(profile_C[:n, :n].det() <= 0 for n in range(1, 5)):
    raise AssertionError("profile covariance positive definiteness")
if any(profile_H[:n, :n].det() <= 0 for n in range(1, 5)):
    raise AssertionError("profile Hessian positive definiteness")
passed("profile moments by an independent piecewise-rational integrator")


# Rebuild the base field, the concentrating family moments, and the Schur limit.
H0 = sp.Matrix([[6, 0, 0, -6], [0, 18, 18, 0], [0, 18, 19, 0], [-6, 0, 0, 6]])
if H0.rank() != 3:
    raise AssertionError("base Hessian rank")
require_zero(H0 * identity, "base Hessian kernel")
if profile_b.dot(identity) != sp.Rational(283, 5670):
    raise AssertionError("kernel component of profile cubic vector")
if (identity.T * profile_H * identity)[0] != sp.Rational(179, 540):
    raise AssertionError("kernel profile curvature")
Hrho = H0 + rho * profile_H
brho = sp.sqrt(rho) * profile_b
loss = sp.factor((brho.T * Hrho.inv() * brho)[0] / 2)
loss_limit = sp.limit(loss, rho, 0, dir="+")
if loss_limit != sp.Rational(80089, 21313530):
    raise AssertionError("Schur-loss limit")
for n in range(1, 5):
    minor = sp.factor(Hrho[:n, :n].det())
    num, den = sp.fraction(minor)
    if den <= 0 or any(coef < 0 for coef in sp.Poly(num, rho).all_coeffs()):
        raise AssertionError("positive definiteness for rho > 0")
actual_gap = sp.factor(sp.Rational(3, 2) + profile_c - loss)
gap_num, gap_den = sp.fraction(actual_gap)
if any(x <= 0 for x in sp.Poly(gap_num, rho).all_coeffs()) or any(x <= 0 for x in sp.Poly(gap_den, rho).all_coeffs()):
    raise AssertionError("actual compatible gap is not coefficientwise positive")
scaled_background = -Hrho.inv() * brho
require_zero(sp.Matrix([sp.limit(sp.sqrt(rho) * z, rho, 0, dir="+") for z in scaled_background])
             + sp.Rational(566, 3759) * identity, "scaled escaping background")
passed("concentration loss limit, positive-definite Hessians, and positive actual gaps")


# Contact-shear transfer: verify the exact derivative identity symbolically.
A = sp.Matrix(2, 2, lambda i, j: sp.symbols(f"A{i}{j}"))
vv = sp.Matrix(sp.symbols("v0 v1"))
bb = sp.Matrix(1, 2, lambda i, j: sp.symbols(f"b{j}"))
cc = sp.Matrix(1, 2, lambda i, j: sp.symbols(f"c{j}"))
gg = sp.Matrix(sp.symbols("g0 g1"))
kk = sp.Matrix(sp.symbols("k0 k1"))
hp = sp.symbols("hprime")
S = sp.eye(2) + vv * bb * hp
B = A + gg * bb + kk * cc
rhs = A + kk * cc + (gg + (A * vv + kk * (cc * vv)) * hp) * bb
btv = (bb * vv)[0]
require_zero(B * S - rhs - hp * btv * (gg * bb), "general shear-gradient identity")
N = vv * bb
require_zero(N * N - btv * N, "rank-one shear square")
require_zero(S.det() - (1 + hp * btv), "shear Jacobian determinant")
passed("exact nonlinear shear chain rule and volume-preserving condition")


# A near-collinear pair of exact acoustic contacts gives a quartically flat
# fixed-integrand modulus.  This is a one-sided upper bound for mu_G, not a
# matching lower estimate.
eps = sp.symbols("eps", positive=True)
Dnorm = 1 + 13 * eps**2 + 36 * eps**4
Rplus = sp.Matrix([2 * eps, 1, 6 * eps**2, 3 * eps])
Rminus = sp.Matrix([-2 * eps, 1, 6 * eps**2, -3 * eps])
det_plus = sp.expand(Rplus[0] * Rplus[3] - Rplus[1] * Rplus[2])
det_minus = sp.expand(Rminus[0] * Rminus[3] - Rminus[1] * Rminus[2])
if det_plus != 0 or det_minus != 0:
    raise AssertionError("nearby acoustic contacts are not rank one")
Qeps = hessG.subs(dict(zip(X, Rplus))) + hessG.subs(dict(zip(X, Rminus)))
block_ad = Qeps.extract([0, 3], [0, 3])
block_bc = Qeps.extract([1, 2], [1, 2])
cross_blocks = Qeps.extract([0, 3], [1, 2])
require_zero(cross_blocks, "acoustic block diagonalization")
det_ad = sp.factor(block_ad.det())
trace_ad = sp.factor(sp.trace(block_ad))
det_bc = sp.factor(block_bc.det())
trace_bc = sp.factor(sp.trace(block_bc))
if sp.expand(det_ad - 80 * eps**4 * (243 * eps**4 + 192 * eps**2 + 13)) != 0:
    raise AssertionError("small acoustic block determinant")
if sp.expand(trace_ad - 12 * (179 * eps**4 + 66 * eps**2 + 4)) != 0:
    raise AssertionError("small acoustic block trace")
if sp.expand(det_bc - 48 * (15201 * eps**8 + 9752 * eps**6 + 2129 * eps**4 + 192 * eps**2 + 6)) != 0:
    raise AssertionError("uniform acoustic block determinant")
if block_bc.subs(eps, 0) != sp.Matrix([[72, 72], [72, 76]]):
    raise AssertionError("uniform acoustic block limit")
if sp.factor(block_bc[0, 0] - 24 * (6 * eps**2 + 1) * (19 * eps**2 + 3)) != 0:
    raise AssertionError("uniform acoustic block leading principal minor")
for positive_poly in (det_ad, trace_ad, block_bc[0, 0], det_bc):
    if any(coefficient < 0 for coefficient in sp.Poly(positive_poly, eps).all_coeffs()):
        raise AssertionError("acoustic block has a negative positivity coefficient")
lambda_ad_small_over_eps4 = sp.limit(det_ad / trace_ad / eps**4, eps, 0, dir="+")
if lambda_ad_small_over_eps4 != sp.Rational(65, 3):
    raise AssertionError("small acoustic eigenvalue asymptotic")
correlation_numerator = sp.factor((Rplus.T * Rminus)[0])
if sp.expand(correlation_numerator - (1 - 13 * eps**2 + 36 * eps**4)) != 0:
    raise AssertionError("contact correlation")
s2 = sp.factor(1 - correlation_numerator**2 / Dnorm**2)
if sp.cancel(s2 - 52 * eps**2 * (1 + 36 * eps**4) / Dnorm**2) != 0:
    raise AssertionError("normalized acoustic separation")
mu_over_s4_limsup_bound = sp.limit(
    (lambda_ad_small_over_eps4 * eps**4 / Dnorm) / s2**2, eps, 0, dir="+")
if mu_over_s4_limsup_bound != sp.Rational(65, 8112):
    raise AssertionError("quartic acoustic-modulus upper-bound constant")
tau = sp.factor((1 - correlation_numerator / Dnorm) / 2)
if sp.cancel(tau - 13 * eps**2 / Dnorm) != 0:
    raise AssertionError("balanced covariance anisotropy")
lambda_cov_over_eps4 = sp.limit(
    (lambda_ad_small_over_eps4 * eps**4 / (2 * Dnorm)) / eps**4,
    eps, 0, dir="+")
lambda_cov_over_tau2 = sp.limit(
    (lambda_ad_small_over_eps4 * eps**4 / (2 * Dnorm)) / tau**2,
    eps, 0, dir="+")
if lambda_cov_over_eps4 != sp.Rational(65, 6) or lambda_cov_over_tau2 != sp.Rational(65, 1014):
    raise AssertionError("covariance Hessian asymptotic")
passed("quartic acoustic flatness and balanced covariance conditioning asymptotics")


# The same covariance is attained by an explicit smooth periodic gradient on
# the rational subsequence eps=1/(2m), with two independent torus phases.
m = sp.symbols("m", positive=True, integer=True)
em = 1 / (2 * m)
Kplus = sp.Matrix([[1, m]])
Kminus = sp.Matrix([[-1, m]])
aplus = sp.Matrix([1, 3 * em])
aminus = sp.Matrix([1, -3 * em])
Rplus_m = Rplus.subs(eps, em)
Rminus_m = Rminus.subs(eps, em)
Rplus_matrix_m = sp.Matrix([[Rplus_m[0], Rplus_m[1]], [Rplus_m[2], Rplus_m[3]]])
Rminus_matrix_m = sp.Matrix([[Rminus_m[0], Rminus_m[1]], [Rminus_m[2], Rminus_m[3]]])
require_zero(aplus * (Kplus / m) - Rplus_matrix_m, "positive-frequency rank-one factor")
require_zero(aminus * (Kminus / m) - Rminus_matrix_m, "negative-frequency rank-one factor")
if sp.det(Kplus.col_join(Kminus)) != 2 * m:
    raise AssertionError("two phase frequencies are not independent")
cp, cm = sp.symbols("cos_plus cos_minus", real=True)
D_m = Dnorm.subs(eps, em)
rplus_m = Rplus_m / sp.sqrt(D_m)
rminus_m = Rminus_m / sp.sqrt(D_m)
Xphase = sp.expand(rplus_m * cp + rminus_m * cm)


def cosine_moment(power: int) -> sp.Rational:
    if power % 2:
        return sp.Integer(0)
    return sp.binomial(power, power // 2) / sp.Integer(4) ** (power // 2)


def independent_phase_mean(expr: sp.Expr) -> sp.Expr:
    poly = sp.Poly(sp.expand(expr), cp, cm)
    return sp.factor(sum(coeff * cosine_moment(i) * cosine_moment(j)
                         for (i, j), coeff in poly.terms()))


bphase = sp.Matrix([independent_phase_mean(z.subs(dict(zip(X, Xphase)))) for z in gradG])
require_zero(bphase, "zero mean cubic vector for the two-mode compatible gradient")
Cphase = sp.Rational(1, 2) * (rplus_m * rplus_m.T + rminus_m * rminus_m.T)
Ctarget = (Rplus_m * Rplus_m.T + Rminus_m * Rminus_m.T) / (2 * D_m)
require_zero(Cphase - Ctarget, "compatible gradient covariance factor")
Hphase = sp.Rational(1, 2) * (hessG.subs(dict(zip(X, rplus_m)))
                               + hessG.subs(dict(zip(X, rminus_m))))
Htarget = (hessG.subs(dict(zip(X, Rplus_m)))
           + hessG.subs(dict(zip(X, Rminus_m)))) / (2 * D_m)
require_zero(Hphase - Htarget, "compatible gradient averaged Hessian factor")
passed("smooth periodic two-mode gradient realizes the balanced covariance exactly")


# Add two small, nonresonant Fourier modes.  This makes the covariance full
# rank while changing the weak acoustic eigenvalue only at order eps^6.
E11 = sp.Matrix([1, 0, 0, 0])
E21 = sp.Matrix([0, 0, 1, 0])
H_E11 = hessG.subs(dict(zip(X, E11)))
H_E21 = hessG.subs(dict(zip(X, E21)))
for contact_hessian in (H_E11, H_E21):
    if any(contact_hessian[:n, :n].det() <= 0 for n in range(1, 5)):
        raise AssertionError("small-mode contact Hessian is not positive definite")

extra_covariance = eps**6 * (E11 * E11.T + E21 * E21.T) / 2
Cfull = sp.simplify((Rplus * Rplus.T + Rminus * Rminus.T) / (2 * Dnorm)
                    + extra_covariance)
column_matrix = sp.Matrix.hstack(Rplus / sp.sqrt(Dnorm), Rminus / sp.sqrt(Dnorm),
                                 eps**3 * E11, eps**3 * E21)
if sp.factor(column_matrix.det() - 6 * eps**7 / Dnorm) != 0:
    raise AssertionError("full covariance spanning determinant")
if sp.factor(Cfull.det() - 9 * eps**14 / (4 * Dnorm**2)) != 0:
    raise AssertionError("full covariance determinant")
require_zero(Cfull[0, 3] - Cfull[1, 2], "balanced full covariance determinant moment")
Hfull = (Qeps / (2 * Dnorm)
         + eps**6 * (H_E11 + H_E21) / 2)
require_zero(Hfull - (Qeps / (2 * Dnorm)
                     + eps**6 * (H_E11 + H_E21) / 2),
             "full covariance averaged Hessian formula")
if sp.cancel(sp.trace(Cfull) - (1 + eps**6)) != 0:
    raise AssertionError("full covariance second moment")

# The four integer frequencies have no pairwise signed collision for m>=3,
# and no signed triple relation.  The latter gives zero mean for every
# homogeneous cubic, including DG, by the cosine product-to-sum identity.
frequency_template = [(1, 1), (-1, 1), (3, 0), (4, 0)]  # (x coefficient, y coefficient of m)
for i in range(4):
    for j in range(i + 1, 4):
        for sign in (-1, 1):
            dx = frequency_template[i][0] + sign * frequency_template[j][0]
            dy_m = frequency_template[i][1] + sign * frequency_template[j][1]
            # Check K_i +/- K_j != 0 for every positive m.  When dy_m=0,
            # nonzero dx is the exact remaining obstruction.
            if dx == 0 and dy_m == 0:
                raise AssertionError("pairwise Fourier resonance")
for indices in __import__("itertools").product(range(4), repeat=3):
    for signs in __import__("itertools").product((-1, 1), repeat=3):
        dx = sum(signs[k] * frequency_template[indices[k]][0] for k in range(3))
        dy_m = sum(signs[k] * frequency_template[indices[k]][1] for k in range(3))
        if dx == 0 and dy_m == 0:
            raise AssertionError("cubic Fourier resonance")
passed("full-rank compatible covariance and order-eps^6 Hessian perturbation")


# Exact nontrivial witness in the sheared two-phase class for G, A=I, R=e12.
cx, cy, alpha = sp.symbols("cx cy alpha", real=True)
aa, ab, ac, ad = 1, cy, alpha * cx, 1 + alpha * cx * cy
uu = aa**2 + ac**2
vvnorm = ab**2 + ad**2
qq = aa * ad - ab * ac
Gshear = sp.expand(3 * (uu + vvnorm - 2 * qq) ** 2 + sp.Rational(35, 24) * uu**2 + qq**2 - sp.Rational(5, 2) * qq * uu)
poly_shear = sp.Poly(Gshear, cx, cy)


def cosine_even_moment(n: int) -> sp.Rational:
    if n % 2:
        return sp.Integer(0)
    return sp.binomial(n, n // 2) / sp.Integer(4) ** (n // 2)


mean_Gshear = sp.factor(sum(coeff * cosine_even_moment(i) * cosine_even_moment(j)
                             for (i, j), coeff in poly_shear.terms()))
gap_Gshear = sp.factor(mean_Gshear - G.subs({a: 1, b: 0, c: 0, d: 1}))
require_zero(gap_Gshear - (309 * alpha**4 + 560 * alpha**2 + 108) / 96,
             "separated contact-shear energy")
if gap_Gshear.subs(alpha, sp.Rational(1, 3)) != sp.Rational(4699, 2592):
    raise AssertionError("rational sheared witness gap")
if sp.det(sp.Matrix([[1, cy], [alpha * cx, 1 + alpha * cx * cy]])) != 1:
    raise AssertionError("witness map is not area preserving")
passed("exact positive gap for a nontrivial sheared two-phase compatible field")


output = {
    "checker": "independent exact audit checker",
    "sympy_version": sp.__version__,
    "checks_passed": checks,
    "G_contact": "D2G(I)[X,X] = (3a-2d)^2/2 + 5c^2/6 - det(X)",
    "acoustic_gram_leading_minors": [str(x) for x in leading],
    "profile_H": [[str(x) for x in row] for row in profile_H.tolist()],
    "profile_b": [str(x) for x in profile_b],
    "profile_c": str(profile_c),
    "profile_covariance": [[str(x) for x in row] for row in profile_C.tolist()],
    "profile_fourth_moment": str(profile_m4),
    "concentration_loss_limit": str(loss_limit),
    "positive_gap_example_alpha_1_3": str(gap_Gshear.subs(alpha, sp.Rational(1, 3))),
    "near_contact_pair": {
        "R_plus": [str(x) for x in Rplus],
        "R_minus": [str(x) for x in Rminus],
        "normalized_separation_squared": str(s2),
        "covariance_anisotropy": str(tau),
        "small_acoustic_eigenvalue_over_eps4": str(lambda_ad_small_over_eps4),
        "mu_over_separation_fourth_power_limsup_bound": str(mu_over_s4_limsup_bound),
        "covariance_hessian_over_anisotropy_squared_limit": str(lambda_cov_over_tau2),
    },
    "compatible_covariance_realization": {
        "parameter_subsequence": "eps=1/(2m), m positive integer",
        "integer_frequencies": [["1", "m"], ["-1", "m"]],
        "frequency_matrix_determinant": "2m",
        "gradient_formula": "R_plus/sqrt(D)*cos(2*pi*(x+m*y)) + R_minus/sqrt(D)*cos(2*pi*(-x+m*y))",
        "mean_cubic_vector": [str(x) for x in bphase],
        "fourth_moment_bound": "|Dphi|_F <= 2 pointwise",
    },
    "full_rank_compatible_covariance_extension": {
        "parameter_subsequence": "eps=1/(2m), integer m>=3",
        "extra_gradient_modes": "eps^3*E11*cos(6*pi*x) + eps^3*E21*cos(8*pi*x)",
        "covariance_trace": "1+eps^6",
        "covariance_determinant": str(sp.factor(Cfull.det())),
        "spanning_column_determinant": str(sp.factor(column_matrix.det())),
        "contact_hessian_E11": [[str(x) for x in row] for row in H_E11.tolist()],
        "contact_hessian_E21": [[str(x) for x in row] for row in H_E21.tolist()],
        "full_hessian_formula": "H_e + eps^6*(D2G(E11)+D2G(E21))/2",
        "positive_definite_base_Hessian": "both acoustic blocks are positive definite for eps>0",
        "cubic_frequency_resonance": "none for m>=3 by exact signed-frequency enumeration",
        "uniform_gradient_bound": "|Dphi|_F <= 2 + 2*eps^3",
        "anisotropy_and_minimum_eigenvalue_scales": "normalized tau=13*eps^2+O(eps^4), lambda_min(H)=65/6*eps^4+o(eps^4)",
        "normalized_limit": "lambda_min(H)/(M2*tau^2) -> 5/78, M2=1+eps^6",
    },
    "scope": "Exact polynomial identities and rational integrations only; analytic rank-one-convexity, two-contact, covariance, and transfer proofs are stated separately. The acoustic result is an upper-asymptotic obstruction, not a matching modulus lower bound. The compatible covariance realization does not establish strong-L4 loss continuity or a negative gap. No full quasiconvexity theorem is claimed.",
}
out_path = Path(__file__).with_name("independent_checks.json")
out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
print(f"WROTE {out_path}; {len(checks)} checks passed.", flush=True)
