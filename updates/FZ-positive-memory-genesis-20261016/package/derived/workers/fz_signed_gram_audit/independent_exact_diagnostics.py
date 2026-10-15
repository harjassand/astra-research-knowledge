#!/usr/bin/env python3
"""Independent exact diagnostics for the signed Choi/rate theorem.

The producer script is never imported or executed. This script starts from
left/right multiplication supermatrices, reshuffles their entries into the
normalized Choi matrix, and tests additional singular/complex edge cases.
All writes are confined to this audit directory.
"""
from __future__ import annotations

import datetime
import hashlib
import json
from pathlib import Path

import sympy as s

Q = s.Rational
I2 = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
Y = s.Matrix([[0, -s.I], [s.I, 0]])
Z = s.diag(1, -1)
OUT = Path(__file__).resolve().parent


def simplified(M):
    return M.applyfunc(s.simplify)


def equals(A, B):
    residual = simplified(A - B)
    assert residual == s.zeros(*residual.shape), residual


def rowvec(A):
    return s.Matrix(list(A))


def basis_matrix(modes):
    d = modes[0].rows
    return s.Matrix.hstack(*(rowvec(A) / s.sqrt(d) for A in [s.eye(d), *modes]))


def left_right(A, B):
    # rowvec(A rho B) = (A tensor B^T) rowvec(rho).
    return s.kronecker_product(A, B.T)


def trace_row(d):
    return rowvec(s.eye(d)).T


def reshuffled_choi(S, d):
    # S[(u,v),(p,q)] = <u|Phi(|p><q|)|v>.
    return s.Matrix(d * d, d * d,
                    lambda up, vq: S[(up // d) * d + vq // d,
                                    (up % d) * d + vq % d] / d)


def partial_output_trace(J, d):
    return s.Matrix(d, d,
                    lambda p, q: sum(J[u * d + p, u * d + q] for u in range(d)))


def generator_supermatrix(modes, gamma, C, h):
    n, d = len(modes), modes[0].rows
    ident = s.eye(d)
    D = s.diag(*gamma) + C
    rate_operator = sum((D[i, j] * modes[j] * modes[i]
                         for i in range(n) for j in range(n)), s.zeros(d))
    H = sum((h[i] * modes[i] for i in range(n)), s.zeros(d))
    cp = sum((D[i, j] * left_right(modes[i], modes[j])
              for i in range(n) for j in range(n)), s.zeros(d * d))
    S = cp - (left_right(rate_operator, ident) + left_right(ident, rate_operator)) / 2
    S -= s.I * (left_right(H, ident) - left_right(ident, H))
    return simplified(S), simplified(D), simplified(rate_operator)


def expected_block(modes, gamma, C, h, r):
    n, d = len(modes), modes[0].rows
    K = sum((C[i, j] * modes[j] * modes[i]
             for i in range(n) for j in range(n)), s.zeros(d))
    k0 = s.simplify(s.trace(K) / d)
    k = s.Matrix([s.simplify(s.trace(P * K) / d) for P in modes])
    missing = simplified(K - k0 * s.eye(d)
                         - sum((k[i] * modes[i] for i in range(n)), s.zeros(d)))
    assert missing == s.zeros(d), missing
    assert s.simplify(k0 - s.trace(C)) == 0
    a = -k / 2 - s.I * s.Matrix(h)
    D = s.diag(*gamma) + C
    M = s.zeros(n + 1)
    M[0, 0] = r - s.trace(D)
    M[0, 1:] = a.H
    M[1:, 0] = a
    M[1:, 1:] = D
    return simplified(M), simplified(a), simplified(k)


def verify_choi(modes, gamma, C, h, r):
    d = modes[0].rows
    S, D, rate_operator = generator_supermatrix(modes, gamma, C, h)
    M, a, k = expected_block(modes, gamma, C, h, r)
    W = basis_matrix(modes)
    equals(W.H * W, s.eye(len(modes) + 1))
    J = reshuffled_choi(r * s.eye(d * d) + S, d)
    equals(J, W * M * W.H)
    equals(trace_row(d) * S, s.zeros(1, d * d))
    equals(partial_output_trace(J, d), r * s.eye(d) / d)
    equals(rate_operator + sum((2 * s.re(a[i]) * modes[i]
                                for i in range(len(modes))), s.zeros(d)),
           s.trace(D) * s.eye(d))
    return S, D, M, a, k


def symbolic_complex_one_qubit():
    c1, c2, c3, x12, y12, x13, y13, x23, y23 = s.symbols(
        'c1 c2 c3 x12 y12 x13 y13 x23 y23', real=True)
    h = s.symbols('h1 h2 h3', real=True)
    gamma = s.symbols('g1 g2 g3', real=True)
    r = s.symbols('r', real=True)
    C = s.Matrix([[c1, x12 + s.I * y12, x13 + s.I * y13],
                  [x12 - s.I * y12, c2, x23 + s.I * y23],
                  [x13 - s.I * y13, x23 - s.I * y23, c3]])
    _, _, M, a, k = verify_choi([X, Y, Z], gamma, C, h, r)
    equals(k, s.Matrix([2 * y23, -2 * y13, 2 * y12]))
    equals(a, s.Matrix([-y23 - s.I * h[0], y13 - s.I * h[1],
                       -y12 - s.I * h[2]]))
    return {'case': 'generic_symbolic_complex_Hermitian_C',
            'dimension': 2, 'independent_real_C_parameters': 9,
            'k_coefficients': [str(x) for x in k],
            'a_coefficients': [str(x) for x in a],
            'full_supermatrix_reshuffle_choi_identity': True,
            'trace_annihilation_and_normalized_partial_trace': True,
            'note': 'No positivity or floating-point assumptions used in this identity.'}


def singular_signed_complex_success_and_range_failure():
    modes = [s.kronecker_product(Z, I2), s.kronecker_product(I2, Z),
             s.kronecker_product(Z, Z)]
    U = s.diag(1, s.I, -1, 1)
    c = s.simplify(s.trace(U) / 4)
    v = s.Matrix([s.simplify(s.trace(P * U) / 4) for P in modes])
    equals(U, c * s.eye(4) + sum((v[i] * modes[i] for i in range(3)), s.zeros(4)))
    equals(U.H * U, s.eye(4))
    D_target = v * v.H
    gamma = [Q(1, 16)] * 3
    C = D_target - s.diag(*gamma)
    h = [0, 0, Q(1, 4)]
    S, D, M, a, k = verify_choi(modes, gamma, C, h, s.Integer(1))
    equals(D, D_target)
    equals(a, v * s.conjugate(c))
    Dplus = D.pinv()
    equals(D * Dplus * a, a)
    schur_cost = s.simplify((a.H * Dplus * a)[0])
    rmin = s.simplify(s.trace(D) + schur_cost)
    assert D.rank() == 1 and M.rank() == 1 and rmin == 1
    assert schur_cost == Q(1, 8)
    assert C.eigenvals() == {Q(-1, 16): 2, Q(13, 16): 1}
    equals(S, left_right(U, U.H) - s.eye(16))
    witness = s.Matrix.vstack(s.ones(1, 1), -Dplus * a)
    Mbelow = M.copy()
    Mbelow[0, 0] -= Q(1, 100)
    assert s.simplify((witness.H * Mbelow * witness)[0]) == -Q(1, 100)
    r, eps = s.symbols('r eps', real=True)
    _, _, Mbad, abad, _ = verify_choi(modes, gamma, C,
                                    [eps, eps, Q(1, 4)], r)
    z = s.Matrix([1, 1, 0])
    equals(D * z, s.zeros(3, 1))
    assert s.simplify((z.H * abad)[0]) == -2 * s.I * eps
    compression = s.Matrix([[Mbad[0, 0], (abad.H * z)[0]],
                            [(z.H * abad)[0], (z.H * D * z)[0]]])
    assert s.simplify(compression.det()) == -4 * eps**2
    return {'case': 'singular_signed_complex_exact_CPTP_boundary',
            'dimension': 4, 'catalog': ['ZI', 'IZ', 'ZZ'],
            'unitary': ['1', 'I', '-1', '1'],
            'identity_Kraus_coefficient': str(c),
            'nonidentity_Kraus_coefficients': [str(x) for x in v],
            'C_eigenvalues_with_multiplicity': {'-1/16': 2, '13/16': 1},
            'D_rank': D.rank(), 'k': [str(x) for x in k],
            'a': [str(x) for x in a], 'a_dagger_Dplus_a': str(schur_cost),
            'r_min': str(rmin), 'normalized_Choi_rank_at_minimum': M.rank(),
            'generator_equals_Ad_U_minus_Id': True,
            'below_minimum_exact_negative_witness': '-1/100',
            'kernel_perturbation': 'delta h = eps*(1,1,0)',
            'range_failure_compression_determinant_for_every_r': '-4*eps**2'}


def missing_product_modes():
    eps, g, r = s.symbols('eps g r', real=True)
    original = [s.kronecker_product(X, I2), s.kronecker_product(Z, I2)]
    omitted = s.kronecker_product(Y, I2)
    C = s.Matrix([[0, s.I * eps], [-s.I * eps, 0]])
    S, _, _ = generator_supermatrix(original, [g, g], C, [0, 0])
    W = basis_matrix([omitted])
    minor = simplified(W.H * reshuffled_choi(r * s.eye(16) + S, 4) * W)
    assert s.simplify(minor.det()) == -eps**2
    # Complete the catalog once; the extra row/column of C remains zero.
    completed = [*original, omitted]
    C3 = s.zeros(3)
    C3[:2, :2] = C
    _, D, _, a, k = verify_choi(completed, [g, g, g], C3, [0, 0, 0], r)
    rate = s.simplify(s.trace(D) + (a.H * D.inv() * a)[0])
    assert rate == 3 * g + eps**2 / g
    assert k == s.Matrix([0, 0, -2 * eps])
    # A real offdiagonal between commuting modes also generates a product.
    commuting = [s.kronecker_product(X, I2), s.kronecker_product(I2, X)]
    product = s.kronecker_product(X, X)
    positive_C = eps * s.ones(2)
    Spos, _, _ = generator_supermatrix(commuting, [g, g], positive_C, [0, 0])
    Wpos = basis_matrix([product])
    minorpos = simplified(Wpos.H * reshuffled_choi(r * s.eye(16) + Spos, 4) * Wpos)
    assert s.simplify(minorpos.det()) == -eps**2
    return {'case': 'arbitrarily_small_unfloored_anticommutator_products',
            'signed_imaginary_C_catalog': ['XI', 'ZI'],
            'signed_C': [['0', 'I*eps'], ['-I*eps', '0']],
            'missing_product': 'YI',
            'principal_block': [[str(x) for x in row] for row in minor.tolist()],
            'determinant_for_every_r': '-eps**2',
            'completed_catalog': ['XI', 'ZI', 'YI'],
            'completed_D_positive_hypothesis': 'g > abs(eps)',
            'completed_r_min': str(rate),
            'positive_commuting_jump_catalog': ['XI', 'IX'],
            'positive_C': 'eps*ones(2,2), eps>0',
            'positive_jump_missing_product': 'XX',
            'positive_jump_principal_block': [[str(x) for x in row] for row in minorpos.tolist()],
            'positive_jump_determinant_for_every_r': '-eps**2',
            'implication': 'Small coefficient/norm error without the catalog-support hypothesis is insufficient.'}


def correlated_signed_rate_not_diagonal_formula():
    C = s.Matrix([[0, Q(1, 2), 0], [Q(1, 2), 0, 0], [0, 0, 0]])
    gamma = [1, 1, 1]
    output = []
    for h in ([1, 1, 0], [1, -1, 0]):
        _, D, _, a, _ = verify_choi([X, Y, Z], gamma, C, h, s.Integer(10))
        output.append(str(s.simplify(s.trace(D) + (a.H * D.inv() * a)[0])))
    assert output == ['13/3', '7']
    return {'case': 'signed_correlated_D_changes_directional_Hamiltonian_cost',
            'C_eigenvalues': ['-1/2', '0', '1/2'],
            'gamma': ['1', '1', '1'], 'h_vectors': [['1', '1', '0'], ['1', '-1', '0']],
            'exact_r_min': output, 'incorrect_diagonal_only_formula': '5',
            'implication': 'The root C=0 formula cannot replace the full signed Gram inverse.'}


def independent_worker_receipt_crosscheck():
    modes = [s.kronecker_product(X, I2), s.kronecker_product(Y, Z),
             s.kronecker_product(Z, Z)]
    C = s.Matrix([[Q(1, 20), -s.I / 40, 0],
                  [s.I / 40, -Q(1, 50), 0], [0, 0, 0]])
    gamma = [Q(1, 5)] * 3
    h = [Q(1, 30), 0, Q(1, 40)]
    _, D, _, a, k = verify_choi(modes, gamma, C, h, s.Integer(1))
    rate = s.simplify(s.trace(D) + (a.H * D.inv() * a)[0])
    frozen_receipt = json.loads((OUT / 'frozen_inputs/worker_receipt.json').read_text())
    reported = frozen_receipt['cases'][0]
    assert str(rate) == reported['minimum_proposal_rate'] == '7279/11360'
    minors = [s.simplify(D[:j, :j].det()) for j in range(1, 4)]
    assert [str(x) for x in minors] == reported['D_leading_principal_minors']
    assert [str(x) for x in k] == reported['K_nonidentity_coefficients']
    return {'case': 'frozen_worker_signed_example_independent_crosscheck',
            'r_min': str(rate), 'D_leading_principal_minors': [str(x) for x in minors],
            'K_nonidentity_coefficients': [str(x) for x in k],
            'method': 'Independent supermatrix-to-Choi reshuffling; producer script not executed.',
            'reported_values_match': True}


def spectator_dimension_normalization():
    dimensions = []
    rates = []
    for q in (1, 2, 3):
        spectator = s.eye(2 ** (q - 1))
        P = s.kronecker_product(X, spectator)
        _, D, _, a, _ = verify_choi([P], [Q(2, 5)], s.zeros(1), [Q(3, 10)], Q(5, 8))
        dimensions.append(P.rows)
        rates.append(str(s.simplify(s.trace(D) + (a.H * D.inv() * a)[0])))
    assert rates == ['5/8'] * 3
    return {'case': 'spectator_qubits_add_no_hidden_d_factor',
            'ambient_dimensions': dimensions, 'same_catalog_size': 1,
            'r_min_each': rates, 'normalized_HS_orthonormality': True,
            'full_Choi_Gram_and_partial_trace_identity_each': True}


def exact_budget_constants():
    nu = s.symbols('nu', positive=True)
    N = s.symbols('N', positive=True, integer=True)
    gamma = nu / (2 * N)
    b = nu / (8 * N)
    u2 = nu**2 / (16 * N)
    bound = s.factor(nu / 2 + b + (b**2 / 4 + u2) / (gamma - b))
    assert s.simplify(bound - nu * (Q(2, 3) + Q(13, 96) / N)) == 0
    assert s.simplify((nu - bound) / nu - (32 * N - 13) / (96 * N)) == 0
    delta = nu / (8 * N)
    norm_bound = s.factor(nu / 2 + delta + delta**2 / (gamma - delta))
    assert s.simplify(norm_bound - nu * (Q(1, 2) + 1 / (6 * N))) == 0
    radius2 = nu**2 / (4 * N)
    assert s.simplify(nu / 2 + radius2 / gamma - nu) == 0
    t, kappa = s.symbols('t kappa', positive=True)
    eta = s.sqrt(1 + nu / (8 * N * t * kappa)) - 1
    assert s.simplify(t * kappa * (2 * eta + eta**2) - b) == 0
    return {'case': 'all_structured_budget_constants',
            'hypotheses': ['N>=1 integer', 'nu>0', 'catalog support verified',
                           'b bounds op(C), abs(tr(C)), Euclidean(k)', 'h and k real'],
            'signed_floor_gamma': 'nu/(2*N)', 'signed_b_limit': 'nu/(8*N)',
            'signed_h_limit': 'nu/(4*sqrt(N))',
            'D_lower_bound': '3*nu/(8*N)',
            'signed_r_upper_bound': str(bound),
            'largest_signed_upper_fraction_at_N_1': '77/96',
            'signed_slack_fraction': '(32*N-13)/(96*N)>0',
            'diamond_delta_limit': 'nu/(8*N)', 'diamond_r_upper_bound': str(norm_bound),
            'largest_diamond_upper_fraction_at_N_1': '2/3',
            'pure_coherent_sharp_radius': 'nu/(2*sqrt(N))',
            'pure_coherent_rate_at_boundary': 'nu',
            'relative_jump_eta_limit': str(eta),
            'relative_jump_B_at_eta_boundary': 'nu/(8*N)',
            'classification': 'All cited constants are sufficient; signed/diamond constants are not claimed optimal.'}


def negative_direction_obstruction():
    g, eps, r = s.symbols('g eps r', real=True)
    _, D, M, _, _ = verify_choi([X], [g], s.Matrix([[-eps]]), [0], r)
    assert D[0, 0] == g - eps
    return {'case': 'negative_signed_conditional_block_cannot_be_repaired_by_r',
            'C': '-eps', 'D': 'g-eps', 'no_finite_rate_when': 'eps>g',
            'unrestricted_Pauli_floor_consequence': 'Gamma >= (d^2-1)*eps',
            'diamond_ball_parameter_conversion': '||-eps*(Ad_P-Id)||_diamond=2*eps for nonidentity Pauli P'}


def verify_frozen_inputs():
    receipt = json.loads((OUT / 'INPUT_RECEIPT.json').read_text())
    result = []
    for record in receipt['input_records']:
        frozen_hash = hashlib.sha256(Path(record['frozen_path']).read_bytes()).hexdigest()
        current_hash = hashlib.sha256(Path(record['source_path']).read_bytes()).hexdigest()
        assert frozen_hash == record['sha256']
        result.append({'source_path': record['source_path'], 'frozen_sha256': frozen_hash,
                       'live_sha256': current_hash, 'live_matches_freeze': current_hash == frozen_hash})
    return result


def main():
    cases = [symbolic_complex_one_qubit(), singular_signed_complex_success_and_range_failure(),
             missing_product_modes(), correlated_signed_rate_not_diagonal_formula(),
             independent_worker_receipt_crosscheck(), spectator_dimension_normalization(),
             exact_budget_constants(), negative_direction_obstruction()]
    receipt = {'status': 'PASS_INDEPENDENT_EXACT_ALGEBRA_WITH_SCOPE_BOUNDARIES',
               'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'method': 'Analytic proof in SIGNED_GRAM_AUDIT.md plus exact symbolic supermatrix/Choi reshuffling.',
               'arithmetic': 'SymPy rational, Gaussian rational, exact symbols; no floating-point tolerance.',
               'sympy_version': s.__version__,
               'producer_script_executed': False,
               'case_count': len(cases), 'cases': cases,
               'input_hash_recheck': verify_frozen_inputs(),
               'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'not_established': ['historical originality', 'external peer correctness',
                                   'universal memory good-schedule premise',
                                   'physical implementation or useful finite-device advantage',
                                   'unstructured ambient error guarantee']}
    path = OUT / 'EXACT_DIAGNOSTIC_RECEIPT.json'
    path.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': receipt['status'], 'case_count': len(cases),
                      'all_sources_unchanged_since_freeze': all(x['live_matches_freeze'] for x in receipt['input_hash_recheck']),
                      'receipt': str(path)}))


if __name__ == '__main__':
    main()
