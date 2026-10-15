#!/usr/bin/env python3
"""Reconstruct the exact polynomial-support obstruction for the FV exposed ray.

Only SymPy and the standard library are used. No saved numerical output,
optimizer, certificate JSON, local source manuscript, or pickle is read.
The analytic scaling and averaging steps are proved in REPORT.md.
"""
from pathlib import Path
import hashlib
import json
import platform
import sympy as S

out = Path(__file__).resolve().parent
x = S.Matrix(S.symbols('a b c d'))
a, b, c, d = x
h = S.Matrix(S.symbols('h0:4'))
u = a*a+c*c
v = b*b+d*d
w = a*b+c*d
q = a*d-b*c
r = u-v
F = S.expand(u*u+v*v+S.Rational(166,3)*u*v-S.Rational(460,9)*w*w-S.Rational(52,9)*q*r)
grad = S.Matrix([S.diff(F, t) for t in x])
Hess = S.hessian(F, x)
J = S.hessian(q, x)


def at(expr, vec):
    return expr.subs(dict(zip(x, vec)), simultaneous=True)


def zero(expr):
    if isinstance(expr, S.MatrixBase):
        return all(S.expand(t) == 0 for t in expr)
    return S.expand(expr) == 0


# Reconstruct F's exact symmetries, rather than importing a symmetry list.
assert zero(at(F, S.Matrix([-c, -d, a, b]))-F)  # target quarter turn
assert zero(at(F, S.Matrix([b, a, d, c]))-F)    # input column swap
rotation_generator = S.Matrix([-c, -d, a, b])
assert zero(grad.dot(rotation_generator))      # all proper target rotations

# A general invariant quadratic multiplier is alpha*q+beta*(u-v).
quadratic_monomials = [x[i]*x[j] for i in range(4) for j in range(i,4)]
coef = S.Matrix(S.symbols('l0:10'))
lam_general = sum(z*t for z, t in zip(coef, quadratic_monomials))
rot_derivative = sum(S.diff(lam_general, x[i])*rotation_generator[i] for i in range(4))
swap_defect = lam_general + at(lam_general, S.Matrix([b, a, d, c]))
eqs = S.Poly(rot_derivative, *x).coeffs()+S.Poly(swap_defect, *x).coeffs()
symmetry_map = S.Matrix([[S.diff(e, z) for z in coef] for e in eqs])
assert symmetry_map.rank() == 8
quadratic_kernel = symmetry_map.nullspace()
assert len(quadratic_kernel) == 2
alpha, beta = S.symbols('alpha beta')
lam = alpha*q+beta*r
assert zero(sum(S.diff(lam, x[i])*rotation_generator[i] for i in range(4)))
assert zero(lam+at(lam, S.Matrix([b,a,d,c])))

# Exact quartic Bregman identity.
R0 = S.expand(at(F, x+h)-F-grad.dot(h))
quartic_remainder = S.expand(at(F,h)+at(grad,h).dot(x)+h.dot(Hess*h)/2)
assert zero(R0-quartic_remainder)

# Reconstruct the acoustic-contact implication without using the old lambda.
k = S.symbols('k')
P = 17*k**4-314*k*k+17
Ak = S.Matrix([203-17*k*k, k*(85*k*k-1551), 2*k*(944-51*k*k), 134])
Rk = S.Matrix([1,k,0,0])


def rem(e):
    return S.rem(S.Poly(S.expand(e),k), S.Poly(P,k)).as_expr()


assert rem(Rk.dot(at(Hess,Ak)*Rk)) == 0
qAk = rem(at(q,Ak))
rAk = rem(at(r,Ak))
assert qAk == 185744-11024*k*k
assert rAk == S.Rational(6,13)*qAk
assert S.gcd(S.Poly(P,k),S.Poly(qAk,k)).degree() == 0
assert S.discriminant(17*k*k-314*k+17,k) > 0
# Its two roots in k^2 have positive sum and product, hence four real roots.
assert S.Rational(314,17) > 0 and S.Rational(17,17) > 0
contact_equations = []
for entry in at(Hess,Ak)*Rk-at(lam,Ak)*(J*Rk):
    contact_equations.extend(S.Poly(rem(entry),k).coeffs())
contact_solutions = S.linsolve(contact_equations, (alpha,beta))
assert contact_solutions == S.FiniteSet((S.Rational(3968,39)-S.Rational(6,13)*beta,beta))

# The old-FV contact has no additional non-rank-one null direction.
contact_lambda = S.Rational(3968,39)*at(q,Ak)
contact_hessian = (at(Hess,Ak)-contact_lambda*J).applyfunc(rem)
assert all(rem(t) == 0 for t in contact_hessian*Rk)
contact_minor = S.factor(rem(contact_hessian[1:4,1:4].det()))
assert zero(contact_minor+S.Rational(193857643872256,459)*(2465740*k*k-45411777))
assert S.gcd(S.Poly(P,k),S.Poly(contact_minor,k)).degree() == 0
assert rem(at(grad,Rk).dot(Ak)) == 0

# Necessity of the support discriminant for each real radial increment t*V.
# F(V)>0 in both chosen directions, so its quadratic polynomial in t must
# have nonpositive discriminant; no SOS strengthening is used.
alpha0 = S.Rational(3968,39)
lam_forced = alpha0*q + beta*(r-S.Rational(6,13)*q)
tests = [
    ('upper', S.Matrix([-6,-3,-1,6]), S.Matrix([1,-2,0,1]),
     -S.Rational(1142144,27), S.Rational(14560,3), -S.Rational(35692,4095)),
    ('lower', S.Matrix([2,0,0,1]), S.Matrix([3,0,0,-2]),
     S.Rational(957266072,1053), -S.Rational(1465992,13), -S.Rational(119658259,14843169)),
]
results = []
for name, A, V, C0_expected, Cb_expected, bound_expected in tests:
    FV = at(F,V)
    assert FV > 0
    HAA = V.dot(at(Hess,A)*V)
    cubic = at(grad,V).dot(A)
    expression = S.expand(2*FV*HAA-cubic*cubic-4*at(lam_forced,A)*FV*at(q,V))
    C0 = S.factor(expression.subs(beta,0))
    Cb = -S.diff(expression,beta)
    assert C0 == C0_expected and Cb == Cb_expected
    bound = S.factor(C0/Cb)
    assert bound == bound_expected
    assert (Cb>0) if name == 'upper' else (Cb<0)
    radial_t = S.factor(-cubic/(2*FV))
    actual_remainder = S.expand(at(R0, A).subs(dict(zip(h,radial_t*V)),simultaneous=True)
                                -at(lam_forced,A)*radial_t*radial_t*at(q,V))
    assert zero(actual_remainder-radial_t*radial_t*expression/(4*FV))
    results.append({
        'name': name, 'A': [str(t) for t in A], 'V': [str(t) for t in V],
        'F_V': str(FV), 'q_V': str(at(q,V)), 'hessian_value': str(HAA),
        'cubic': str(cubic), 'C0': str(C0), 'Cb': str(Cb), 'bound': str(bound),
        'radial_countertest_t': str(radial_t),
    })
upper = tests[0][-1]
lower = tests[1][-1]
assert lower > -S.Rational(17,2) > upper
separation = S.factor(lower-upper)
assert separation > 0
U = -S.Rational(1142144,27)-S.Rational(14560,3)*beta
L = S.Rational(957266072,1053)+S.Rational(1465992,13)*beta
dual_identity = S.expand(549747*U+23660*L)
assert dual_identity == -S.Rational(141446461664,81)

receipt = {
    'schema': 'astra.exact_pc_multiplier_obstruction.v1',
    'status': 'EXACT_ALGEBRA_PASS_ANALYTIC_PROOF_INTERNAL_UNREVIEWED',
    'python': platform.python_version(), 'sympy': S.__version__,
    'checks': {
        'left_SO2_and_input_swap_invariance': True,
        'invariant_antisymmetric_quadratic_multiplier_space_dimension': 2,
        'quartic_Bregman_identity': True,
        'four_real_acoustic_contacts': True,
        'contact_null_second_variation': True,
        'contact_forced_multiplier_relation': True,
        'two_integer_support_discriminant_cuts': True,
        'strict_rational_cut_incompatibility': True,
        'positive_combination_dual_identity': True,
        'actual_rational_radial_remainder_countertests': True,
        'contact_hessian_rank_three_and_null_cubic_zero': True,
    },
    'forced_relation': 'alpha + 6*beta/13 = 3968/39',
    'tests': results, 'lower_minus_upper': str(separation),
    'positive_combination_dual_value': str(dual_identity),
    'contact_rank_three_minor': str(contact_minor),
    'analytic_obligations': [
        'A second-order Peano support selection at zero reduces by homogeneity to its quadratic Taylor part.',
        'Compact target-rotation and determinant-sign input-swap averaging preserve support inequalities.',
        'A nonnegative support remainder has PSD Hessian at H=0 and annihilates each acoustic-null direction.',
        'Every polynomial minor support, and hence every SOS-polyconvex certificate, supplies such a polynomial lambda.',
    ],
    'scope': {
        'no_second_order_Peano_support_selection_at_zero': 'PROVED_IN_REPORT_INTERNAL',
        'no_polynomial_minor_support_any_degree': 'PROVED_IN_REPORT_INTERNAL',
        'not_SOS_polyconvex_any_degree': 'PROVED_IN_REPORT_INTERNAL',
        'no_convex_polynomial_lift_any_degree': 'PROVED_IN_REPORT_INTERNAL',
        'polyconvex': 'UNKNOWN', 'quasiconvex': 'UNKNOWN',
        'historical_priority': 'UNKNOWN', 'external_correctness_review': 'UNKNOWN',
    },
    'reads_saved_optimizer_or_certificate_data': False,
}
receipt['verifier_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
(out/'PC_MULTIPLIER_OBSTRUCTION_VERIFICATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
