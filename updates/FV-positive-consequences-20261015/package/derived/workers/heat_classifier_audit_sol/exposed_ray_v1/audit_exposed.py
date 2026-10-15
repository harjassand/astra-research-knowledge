"""Independent exact reconstruction of the exposed-ray obstruction.

No author module, JSON certificate, optimizer result, numerical eigenvalue,
or finite positivity sample is an input. The closed-form correction basis
is derived directly from all 60 coefficients, independently of the author's
15-primitive gauge. The two finite jet tests are an exact dual contradiction.
"""
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import hashlib
import json
import subprocess
import time
import sympy as s

OUT = Path(__file__).resolve().parent
CAPITAL = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-positive-consequences-20261015')
PIN = 'a6190a1083f688a7e4bf64adbc5244ef150ff2c4'


def zero(poly):
    assert s.expand(poly) == 0


def matrix_zero(matrix):
    assert all(s.expand(entry) == 0 for entry in matrix)


def main():
    started = time.monotonic()
    actual = subprocess.check_output(['git', '-C', str(CAPITAL), 'rev-parse', 'HEAD'], text=True).strip()
    assert actual == PIN
    a, b, c, d = x = s.symbols('a b c d', real=True)
    h = s.symbols('h0:6', real=True)
    k, n0, n1 = s.symbols('k n0 n1', real=True)
    u, v, w, q = a*a+c*c, b*b+d*d, a*b+c*d, a*d-b*c
    basis = [u*u, v*v, u*v, w*w, u*w, v*w, q*u, q*v, q*w]
    p = s.Matrix([1, 1, s.Rational(166, 3), -s.Rational(460, 9),
                  0, 0, -s.Rational(52, 9), s.Rational(52, 9), 0])
    F = sum(ci*fi for ci, fi in zip(p, basis))
    HF = s.hessian(F, x)
    left = s.Matrix([-c, -d, a, b])
    zero(sum(left[i]*s.diff(F, x[i]) for i in range(4)))
    swap_x = dict(zip(x, [b, a, d, c]))
    paired_x = dict(zip(x, [a, -b, -c, d]))
    zero(F.subs(swap_x, simultaneous=True)-F)
    zero(F.subs(paired_x, simultaneous=True)-F)

    # Verify the candidate acoustic factor in all six variables (A,n),
    # including n0=0, without deriving it from an SDP output.
    B = s.Matrix([[2, 1, 0, 0], [0, 0, 3, 1], [0, 0, 2, 1],
                  [-1, -9, 0, 0], [0, 0, 3, -1], [2, -1, 0, 0],
                  [-1, 9, 0, 0], [0, 0, 2, -1]])
    weights = s.diag(s.Rational(8, 3), s.Rational(4, 3),
                     s.Rational(8, 9), s.Rational(4, 9))
    Q = B*weights*B.T
    Rn = s.Matrix([n0, n1, 0, 0])
    Y = s.Matrix([n0*xx for xx in x]+[n1*xx for xx in x])
    zero((Y.T*Q*Y)[0]-(Rn.T*HF*Rn)[0])
    assert B.rank() == 4 and all(z > 0 for z in weights.diagonal())
    R = s.Matrix([1, k, 0, 0])
    M = s.hessian((R.T*HF*R)[0], x)/2
    M11, M12, M22 = M.subs(k, 0), M.diff(k).subs(k, 0)/2, M.diff(k, 2)/2
    matrix_zero(Q[:4, :4]-M11)
    matrix_zero(Q[4:, 4:]-M22)
    matrix_zero((Q[:4, 4:]+Q[4:, :4])/2-M12)

    r, t, dd = u-v, 2*w, 2*q
    zero((u+v)**2-r*r-t*t-dd*dd)
    zero(F-(r-s.Rational(13, 9)*dd)**2-s.Rational(14, 9)*t*t-s.Rational(992, 81)*dd*dd)
    coerce = s.Matrix([[s.Rational(1, 2), 0, -s.Rational(13, 9)],
                        [0, s.Rational(19, 18), 0],
                        [-s.Rational(13, 9), 0, s.Rational(83, 6)]])
    coercive_minors = [coerce[:j, :j].det() for j in range(1, 4)]
    assert all(val > 0 for val in coercive_minors)

    P = 17*k**4-314*k*k+17
    Ak = s.Matrix([203-17*k*k, k*(85*k*k-1551), 2*k*(944-51*k*k), 134])

    def rem(poly):
        return s.rem(s.expand(poly), P, k)

    def coeff4(poly):
        reduced = s.Poly(rem(poly), k)
        return [reduced.nth(i) for i in range(4)]

    assert s.Poly(P, k).count_roots(-s.oo, s.oo) == 4
    assert s.gcd(P, s.diff(P, k)) == 1
    assert all(rem(z) == 0 for z in M*Ak)
    zero(M.det()-s.Rational(1024, 729)*P*P)
    detder = rem(Ak[3]-k*Ak[2])
    zero(detder-4*(8-k*k))
    assert s.gcd(P, detder) == 1

    # Exposure comes from nonnegative acoustic evaluations, not extremality
    # of the particular eight-by-eight Gram.
    critical_cols, raw_exposing = [], []
    for fi in basis:
        Mi = s.hessian((R.T*s.hessian(fi, x)*R)[0], x)/2
        col = [entry for zz in Mi*Ak for entry in coeff4(zz)]
        col += coeff4((Ak.T*Mi.diff(k)*Ak)[0])
        critical_cols.append(s.Matrix(col))
        ev = coeff4((Ak.T*Mi*Ak)[0])
        raw_exposing.append(4*ev[0]+s.Rational(628, 17)*ev[2])
    critical = s.Matrix.hstack(*critical_cols)
    assert critical.shape == (20, 9) and critical.rank() == 8
    matrix_zero(critical*p)
    common_denominator = s.ilcm(*(s.denom(z) for z in raw_exposing))
    integer_exposing = [int(z*common_denominator) for z in raw_exposing]
    common_gcd = s.igcd(*integer_exposing)
    exposing = [int(z/common_gcd) for z in integer_exposing]
    assert exposing == [910741, 1453621, 324775, 321232, 0, 0, 244987, -432907, 0]
    assert sum(val*ci for val, ci in zip(exposing, p)) == 0
    raw_scale = s.Rational(common_gcd, common_denominator)
    assert raw_scale > 0

    # Check contact zero for any output-coupled principal symbol. The acoustic
    # output matrix S is PSD by ROC, and its entire e1 column vanishes.
    Ra = [s.Matrix([1, k, 0, 0]), s.Matrix([0, 0, 1, k])]
    asub = dict(zip(x, Ak))
    output_acoustic = s.Matrix(2, 2, lambda i, j: (Ra[i].T*HF*Ra[j])[0])
    for i in range(2):
        assert rem(output_acoustic[i, 0].subs(asub, simultaneous=True)) == 0

    b1, b2 = s.Matrix([h[0], h[1], h[3], h[4]]), s.Matrix([h[1], h[2], h[4], h[5]])
    J4 = s.Matrix([[0, 0, -1, 0], [0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 0]])
    heat = s.expand((b1.T*HF*b1)[0]+(b2.T*HF*b2)[0])
    rotating = s.expand((b1.T*HF*J4*b2)[0]+(b2.T*HF*J4*b1)[0])
    hzero = dict(zip(h, [1, k, k*k, 0, 0, 0]))
    for density in (heat, rotating):
        assert rem(density.subs(hzero).subs(asub, simultaneous=True)) == 0

    # Derive every closed left-SO(2)-invariant quadratic two-form from its
    # full 60 coefficients. No supplied 15-primitive basis is used here.
    pairs = list(combinations(range(4), 2))
    qmons = list(combinations_with_replacement(range(4), 2))
    z = s.symbols('w0:60')
    W = s.zeros(4)
    for ip, (i, j) in enumerate(pairs):
        W[i, j] = sum(z[10*ip+iq]*x[m]*x[n] for iq, (m, n) in enumerate(qmons))
        W[j, i] = -W[i, j]
    closure = []
    for i, j, m in combinations(range(4), 3):
        closure += s.Poly(s.diff(W[j, m], x[i])-s.diff(W[i, m], x[j])
                          +s.diff(W[i, j], x[m]), *x).coeffs()
    closure_matrix, _ = s.linear_eq_to_matrix(closure, z)
    assert closure_matrix.rank() == 15
    jac = left.jacobian(x)
    lie = W.applyfunc(lambda fi: sum(left[i]*s.diff(fi, x[i]) for i in range(4)))
    lie += jac.T*W+W*jac
    equations = list(closure)
    for i, j in pairs:
        equations += s.Poly(s.expand(lie[i, j]), *x).coeffs()
    invariant_matrix, _ = s.linear_eq_to_matrix(equations, z)
    assert invariant_matrix.rank() == 45
    left_basis = invariant_matrix.nullspace()
    assert len(left_basis) == 15
    coordinates = s.Matrix.hstack(*left_basis)
    matrix_zero(invariant_matrix*coordinates)
    assert coordinates.rank() == 15
    omegas = []
    densities = []
    for col in left_basis:
        om = W.subs(dict(zip(z, col)))
        omegas.append(om)
        densities.append(s.expand((b1.T*om*b2)[0]))

    unknowns = s.symbols('v0:15')+(s.symbols('beta'),)
    corrected = heat+sum(cc*di for cc, di in zip(unknowns, densities+[rotating]))

    def contact_gradient(density):
        return s.Matrix([entry for hh in h for entry in
             coeff4(s.diff(density, hh).subs(hzero).subs(asub, simultaneous=True))])

    contact = s.Matrix.hstack(*[contact_gradient(di) for di in densities+[rotating]])
    rhs = -contact_gradient(heat)
    swap = dict(zip(x+h, [b, a, d, c, h[2], h[1], h[0], h[5], h[4], h[3]]))
    paired = dict(zip(x+h, [a, -b, -c, d, h[0], -h[1], h[2], -h[3], h[4], -h[5]]))
    symmetry_equations = []
    for change in (swap, paired):
        symmetry_equations += s.Poly(s.expand(corrected-corrected.subs(change, simultaneous=True)), *(x+h)).coeffs()
    symmetry, symmetry_rhs = s.linear_eq_to_matrix(symmetry_equations, unknowns)
    linear = contact.col_join(symmetry)
    target = rhs.col_join(symmetry_rhs)
    assert linear.rank() == linear.row_join(target).rank() == 15
    solution, parameters = linear.gauss_jordan_solve(target)
    assert parameters.rows == 1
    assert solution[-1] == 0
    independent_family = s.expand(corrected.subs(dict(zip(unknowns, solution)), simultaneous=True))
    atoms = [([1, 0, 0, 2], [0, 1, 0, 0, 0, -1]),
             ([1, -1, 0, 2], [0, 0, 1, -1, 0, 0])]
    atom_values = [s.expand(independent_family.subs(dict(zip(x+h, A0+H0))))
                   for A0, H0 in atoms]
    dual = s.expand(586*atom_values[0]+411*atom_values[1])
    assert dual == -s.Rational(81691400, 531)

    # Match the independently derived one-dimensional family to the explicit
    # cubic primitive in the narrative. This is a polynomial identity check.
    tau = s.symbols('t', real=True)
    theta_u, theta_v = s.Matrix([-c, 0, a, 0]), s.Matrix([0, -d, 0, b])
    zeta, dw = s.Matrix([-b, a, -d, c]), s.Matrix([b, a, d, c])
    primitive = (-93*tau/s.Integer(59)-s.Rational(5456, 177))*(u-v)*dw
    primitive += (83*tau/s.Integer(177)-s.Rational(9920, 531))*(u*theta_u-v*theta_v)
    primitive += (s.Rational(21328, 531)-382*tau/s.Integer(177))*(u*theta_v-v*theta_u)
    primitive += tau*(u+v)*zeta
    physical_omega = s.Matrix(4, 4, lambda i, j:
        s.diff(primitive[j], x[i])-s.diff(primitive[i], x[j]))
    physical_family = s.expand(heat+(b1.T*physical_omega*b2)[0])
    family_equations = s.Poly(independent_family-physical_family, *(x+h)).coeffs()
    mapping = s.solve(family_equations, list(parameters), dict=True)
    assert len(mapping) == 1
    zero((independent_family-physical_family).subs(mapping[0]))
    physical_values = [s.factor(physical_family.subs(dict(zip(x+h, A0+H0))))
                       for A0, H0 in atoms]
    zero(physical_values[0]-(s.Rational(274, 59)*tau-s.Rational(192260, 531)))
    zero(physical_values[1]-(s.Rational(25120, 177)-s.Rational(1172, 177)*tau))

    # Independently project a fully general constant output-matrix diffusion
    # by the admitted symmetries. Analytic positivity is addressed in AUDIT.txt.
    cc = s.symbols('c0:12', real=True)
    C11, C12, C22 = s.Matrix(2, 2, cc[:4]), s.Matrix(2, 2, cc[4:8]), s.Matrix(2, 2, cc[8:])
    J, D = s.Matrix([[0, -1], [1, 0]]), s.diag(1, -1)
    output_average = lambda C: (C+J*C*J.T)/2
    A11, A12, A22 = map(output_average, (C11, C12, C22))
    diagonal_swap_average = (A11+A22)/2
    projected11 = (diagonal_swap_average+D*diagonal_swap_average*D)/2
    projected22 = projected11
    projected12 = (A12-D*A12*D)/2
    scalar = (s.trace(C11)+s.trace(C22))/4
    skew = (C12[1, 0]-C12[0, 1])/2
    matrix_zero(projected11-scalar*s.eye(2))
    matrix_zero(projected22-scalar*s.eye(2))
    matrix_zero(projected12-skew*J)

    receipt = {
        'status': 'INDEPENDENT_EXACT_PASS', 'capital_pin': actual,
        'author_modules_imported': False, 'optimization_used': False,
        'coefficient_vector': list(map(str, p)),
        'acoustic_factor_rank': 4, 'positive_acoustic_weights': list(map(str, weights.diagonal())),
        'acoustic_identity_all_A_and_all_input_directions': True,
        'pointwise_coercivity_bound': 'F >= |A|^4/2',
        'coercivity_principal_minors': list(map(str, coercive_minors)),
        'contact_polynomial': str(P), 'four_distinct_real_contacts': True,
        'contact_determinant_derivative': str(detder), 'determinant_derivative_nonzero_at_every_contact': True,
        'contact_output_acoustic_e1_column_zero': True,
        'contact_criticality_shape': list(critical.shape), 'contact_criticality_rank': 8,
        'exposing_functional': exposing, 'sum_of_four_contact_evaluations_equals': str(raw_scale)+' * ell',
        'closed_form_coefficients': 60, 'closure_constraint_rank': 15,
        'closed_left_SO2_constraint_rank': 45, 'independent_left_SO2_closed_basis_dimension': 15,
        'contact_and_symmetry_system_unknowns': 16, 'contact_and_symmetry_system_rank': 15,
        'forced_skew_output_diffusion_parameter': str(solution[-1]),
        'independent_to_narrative_parameter_map': {str(key): str(value) for key, value in mapping[0].items()},
        'physical_correction_family_matches_all_polynomial_coefficients': True,
        'pointwise_atom_values': list(map(str, physical_values)),
        'positive_dual_weights': [586, 411], 'negative_dual_constant': str(dual),
        'general_diffusion_projection': {'scalar': str(scalar), 'skew': str(skew),
             'normal_form': 'scalar*Delta + 2*skew*J*dxy'},
        'normalization_lambda': str(16*(p[0]+p[1])+8*p[2]+4*p[3]),
        'polyconvexity': 'UNKNOWN', 'quasiconvexity': 'UNKNOWN',
        'exposedness_scope': 'nine-dimensional left-SO2-invariant homogeneous quartic ROC cone',
        'obstruction_scope': 'all pointwise closed quadratic two-form corrections for every fixed real constant strongly parabolic output-matrix diffusion',
        'no_periodic_gradient_counterexample_claimed': True,
        'external_review': 'UNKNOWN', 'historical_novelty': 'UNKNOWN',
        'seconds': time.monotonic()-started,
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (OUT/'INDEPENDENT_EXPOSED_RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
