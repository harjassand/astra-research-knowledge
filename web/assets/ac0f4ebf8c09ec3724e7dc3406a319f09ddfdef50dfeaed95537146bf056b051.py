"""Independent finite diagnostics for the conditional XXZ Euler/LC transfer.

These check local Hessians and global small-matrix error. They do not execute
the Chen--Liu FPRAS, certify its proof, or establish any asymptotic theorem.
"""
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np

RNG = np.random.default_rng(261006724)
I2 = np.eye(2)
X = np.array([[0., 1.], [1., 0.]])
Y = np.array([[0., -1j], [1j, 0.]])
Z = np.diag([1., -1.])


def embed(n, operators):
    out = np.ones((1, 1), dtype=complex)
    for v in range(n):
        out = np.kron(out, operators.get(v, I2))
    return np.real_if_close(out).real


def logsumexp(a):
    peak = float(np.max(a))
    return peak + float(np.log(np.sum(np.exp(a - peak))))


thermal = []
max_generator_error_fraction = 0.0
max_log_trace_error_fraction = 0.0
max_shift_over_largest_eigenvalue = 0.0
max_gibbs_distance_over_tanh_bound = 0.0
for case in range(120):
    n = 2 + case % 5
    eye = np.eye(2**n)
    h = np.zeros_like(eye)
    shifted = []
    shift = 0.0
    edge_count = 0
    # Every n>=3 fixture includes a triangle, and hence is not bipartite.
    for u, v in itertools.combinations(range(n), 2):
        if case % 3 == 0 or (u, v) in [(0, 1), (0, 2), (1, 2)] or RNG.random() < .45:
            alpha = float(RNG.uniform(.02, 1.1))
            ratio = [-1., 1., 0.][case % 3] if edge_count == 0 else float(RNG.uniform(-1., 1.))
            gamma = alpha * ratio
            local = alpha * (embed(n, {u: X, v: X}) + embed(n, {u: Y, v: Y})) + gamma * embed(n, {u: Z, v: Z})
            h += local
            shifted.append(local + 3 * alpha * eye)
            shift += 3 * alpha
            edge_count += 1
    for v in range(n):
        b = 0.0 if (case + v) % 7 == 0 else float(RNG.uniform(0., 1.5))
        c = float(RNG.uniform(-2.5, 2.5))
        r = b + abs(c)
        local = b * embed(n, {v: X}) + c * embed(n, {v: Z})
        h += local
        shifted.append(local + r * eye)
        shift += r
    d = 2 * shift
    beta = [.025, .15, .5, 1.5, 3.][case % 5]
    eps = [.1, .03, .01][case % 3]
    tau = beta * d
    m = math.ceil(max(1., 4 * tau, 20 * tau**2 / eps))
    delta = tau / m
    s = beta / (2 * m)
    w = eye.copy()
    minimum_shifted_eigenvalue = math.inf
    for a in shifted:
        minimum_shifted_eigenvalue = min(minimum_shifted_eigenvalue, float(np.linalg.eigvalsh(a)[0]))
        w = w @ (eye + s * a)
    bmat = w @ w.T
    evals, evecs = np.linalg.eigh(bmat)
    assert float(evals[0]) >= 1. - 1e-10
    logarithm = (evecs * np.log(evals)) @ evecs.T
    q = (h + shift * eye) / d
    error = float(np.linalg.norm(logarithm - delta * q, 2))
    analytic_one_step_bound = 5 * delta**2
    total_error = m * error
    # The tolerance accounts for numerical eigendecomposition at extremely
    # small step sizes, not for a mathematical allowance in the theorem.
    assert error <= analytic_one_step_bound + 3e-13
    assert total_error <= eps / 4 + 3e-6
    log_approx = logsumexp(m * np.log(evals)) - beta * shift
    log_exact = logsumexp(beta * np.linalg.eigvalsh(h))
    largest_eigenvalue = float(np.linalg.eigvalsh(h)[-1])
    assert shift/5 <= largest_eigenvalue + 1e-10
    assert largest_eigenvalue <= shift + 1e-10
    max_shift_over_largest_eigenvalue = max(max_shift_over_largest_eigenvalue, shift/largest_eigenvalue)
    log_error = abs(log_approx - log_exact)
    assert log_error <= eps / 4 + 3e-6
    max_generator_error_fraction = max(max_generator_error_fraction, total_error / (eps / 4))
    max_log_trace_error_fraction = max(max_log_trace_error_fraction, log_error / (eps / 4))
    heigen, hvectors = np.linalg.eigh(h)
    rho_weights = np.exp(beta*heigen - np.max(beta*heigen))
    rho_weights /= np.sum(rho_weights)
    rho = (hvectors*rho_weights) @ hvectors.T
    sigma_logs = m*np.log(evals)
    sigma_weights = np.exp(sigma_logs - np.max(sigma_logs))
    sigma_weights /= np.sum(sigma_weights)
    sigma = (evecs*sigma_weights) @ evecs.T
    state_distance = float(np.sum(np.abs(np.linalg.eigvalsh(rho-sigma)))/2)
    tanh_bound = math.tanh(total_error/2)
    assert state_distance <= tanh_bound + 3e-8
    max_gibbs_distance_over_tanh_bound = max(max_gibbs_distance_over_tanh_bound, state_distance/tanh_bound)
    thermal.append({"case": case, "n": n, "edges": edge_count, "beta": beta,
                    "eps": eps, "m": m, "tau": tau, "minimum_shifted_eigenvalue": minimum_shifted_eigenvalue,
                    "effective_generator_norm_error": total_error,
                    "log_partition_ratio_error": log_error, "gibbs_trace_distance": state_distance,
                    "gibbs_tanh_bound": tanh_bound})


def test_log_hessian(matrix, point):
    value = float(point @ matrix @ point / 2)
    gradient = matrix @ point
    hessian = matrix / value - np.outer(gradient, gradient) / value**2
    eigen = np.linalg.eigvalsh(hessian)
    scale = max(1., float(np.linalg.norm(hessian, 2)))
    assert float(eigen[-1]) <= 2e-12 * scale
    return float(eigen[-1]) / scale


gate_tests = 0
max_scaled_positive_log_hessian = -math.inf
for j in range(2400):
    alpha = 10. ** float(RNG.uniform(-8., 4.))
    gamma = alpha * ([-1., 1., 0.][j % 3] if j % 4 == 0 else float(RNG.uniform(-1., 1.)))
    s = 10. ** float(RNG.uniform(-8., 4.))
    a, b, c = 1+s*(3*alpha+gamma), 1+s*(3*alpha-gamma), 2*s*alpha
    # Rows stay unchanged, columns are complemented. The ordering used here
    # is a on 12/34, b on 14/23, and c on 13/24.
    matrix = np.array([[0., a, c, b], [a, 0., b, c], [c, b, 0., a], [b, c, a, 0.]])
    eigen = np.linalg.eigvalsh(matrix)
    assert eigen[-2] <= 3e-12 * max(1., abs(eigen[-1]))
    point = 10. ** RNG.uniform(-3., 3., 4)
    max_scaled_positive_log_hessian = max(max_scaled_positive_log_hessian, test_log_hessian(matrix, point))
    gate_tests += 1

    xf = 0. if j % 11 == 0 else 10. ** float(RNG.uniform(-6., 3.))
    zf = float(RNG.uniform(-1., 1.)) * 10. ** float(RNG.uniform(-6., 3.))
    r = xf + abs(zf)
    t = s*xf
    p, qcoef = 1+s*(r-zf), 1+s*(r+zf)
    # q1=t+p*x+q*y+t*x*y. Its reciprocal swaps p and q.
    for p, qcoef in [(p, qcoef), (qcoef, p)]:
        px, py = 10. ** RNG.uniform(-3., 3., 2)
        value = t + p*px + qcoef*py + t*px*py
        grad = np.array([p+t*py, qcoef+t*px])
        hess = np.array([[0., t], [t, 0.]]) / value - np.outer(grad, grad)/value**2
        eigen = np.linalg.eigvalsh(hess)
        scale = max(1., float(np.linalg.norm(hess, 2)))
        assert eigen[-1] <= 2e-12 * scale
        max_scaled_positive_log_hessian = max(max_scaled_positive_log_hessian, float(eigen[-1])/scale)
        gate_tests += 1

outside_cone = []
for gamma in [-1.1, 1.1]:
    alpha, s = 1., .1
    a, b, c = 1+s*(3*alpha+gamma), 1+s*(3*alpha-gamma), 2*s*alpha
    matrix = np.array([[0., a, c, b], [a, 0., b, c], [c, b, 0., a], [b, c, a, 0.]])
    point = np.ones(4)
    value = float(point @ matrix @ point / 2)
    grad = matrix @ point
    loghess = matrix/value - np.outer(grad, grad)/value**2
    largest = float(np.linalg.eigvalsh(loghess)[-1])
    assert largest > .001
    outside_cone.append({"gamma": gamma, "alpha": alpha, "s": s, "largest_log_hessian_eigenvalue": largest})


def matrix_multiply_exact(a, b):
    k = len(a)
    return [[sum((a[i][l]*b[l][j] for l in range(k)), Fraction(0)) for j in range(k)] for i in range(k)]


def homogeneous_lift_exact_case(n, gate_spec):
    # Each local lifted polynomial has four fresh variables and degree two.
    locals_ = []
    physical_uses = [[] for _ in range(n)]
    dummy_bits = []
    product = [[Fraction(i == j) for j in range(2**n)] for i in range(2**n)]
    for gi, (vertices, local, s) in enumerate(gate_spec):
        base = 4 * gi
        if len(vertices) == 2:
            alpha, gamma = map(Fraction, local)
            a, b, c = 1+s*(3*alpha+gamma), 1+s*(3*alpha-gamma), 2*s*alpha
            local_matrix = [[a, 0, 0, 0], [0, b, c, 0], [0, c, b, 0], [0, 0, 0, a]]
            terms = [(3, a), (12, a), (9, b), (6, b), (5, c), (10, c)]
            for j, vertex in enumerate(vertices):
                physical_uses[vertex].append((base+j, base+2+j))
        else:
            xf, zf = map(Fraction, local)
            r = xf + abs(zf)
            d, u, v = s*xf, 1+s*(r-zf), 1+s*(r+zf)
            local_matrix = [[v, d], [d, u]]
            terms = [(12, d), (5, u/2), (9, u/2), (6, v/2), (10, v/2), (3, d)]
            physical_uses[vertices[0]].append((base, base+1))
            dummy_bits += [base+2, base+3]
        locals_.append([(bits << base, Fraction(weight)) for bits, weight in terms if weight])
        full = [[Fraction(0) for _ in range(2**n)] for _ in range(2**n)]
        for row in range(2**n):
            rb = [(row >> (n-1-v)) & 1 for v in range(n)]
            for col in range(2**n):
                cb = [(col >> (n-1-v)) & 1 for v in range(n)]
                if all(rb[v] == cb[v] for v in range(n) if v not in vertices):
                    lr = sum(rb[v] << (len(vertices)-1-j) for j, v in enumerate(vertices))
                    lc = sum(cb[v] << (len(vertices)-1-j) for j, v in enumerate(vertices))
                    full[row][col] = Fraction(local_matrix[lr][lc])
        product = matrix_multiply_exact(product, full)
    wire_pairs = []
    for uses in physical_uses:
        if uses:
            wire_pairs += [(uses[j][1], uses[(j+1) % len(uses)][0]) for j in range(len(uses))]
    isolated = sum(not uses for uses in physical_uses)
    fields = len(dummy_bits)//2
    total = Fraction(0)
    accepted = 0
    enumerated = 0
    for selection in itertools.product(*locals_):
        enumerated += 1
        mask = 0
        weight = Fraction(1)
        for bits, coeff in selection:
            mask |= bits
            weight *= coeff
        if not all(((mask >> first) & 1) + ((mask >> second) & 1) == 1 for first, second in wire_pairs):
            continue
        # The partner law is pair-wise exact once times e_fields on the
        # dummy coordinates. In the coefficient convolution it selects the
        # complementary dummy subset, which must also have size fields.
        selected_dummy = sum((mask >> bit) & 1 for bit in dummy_bits)
        assert selected_dummy == fields
        total += weight
        accepted += 1
    total *= 2**isolated
    direct = sum((product[i][i] for i in range(2**n)), Fraction(0))
    assert total == direct
    # Open the last-to-first cut wire on the selected physical vertices.
    chosen = [0] if n == 1 else [0, n-1]
    k = len(chosen)
    cut_pairs = [(physical_uses[v][-1][1], physical_uses[v][0][0]) for v in chosen]
    closed_pairs = [pair for pair in wire_pairs if pair not in cut_pairs]
    reduced_lift = [[Fraction(0) for _ in range(2**k)] for _ in range(2**k)]
    for selection in itertools.product(*locals_):
        mask = 0
        weight = Fraction(1)
        for bits, coeff in selection:
            mask |= bits
            weight *= coeff
        if not all(((mask >> first) & 1) + ((mask >> second) & 1) == 1 for first, second in closed_pairs):
            continue
        ar = [(mask >> row_end) & 1 for col_end, row_end in cut_pairs]
        bc = [1 - ((mask >> col_end) & 1) for col_end, row_end in cut_pairs]
        charge = sum(ar)-sum(bc)
        dummy_selected = sum((mask >> bit) & 1 for bit in dummy_bits)
        # Thus the complementary dummy law must be e_(fields+charge).
        assert dummy_selected == fields-charge
        assert 0 <= fields+charge <= 2*fields
        ri = sum(bit << (k-1-j) for j, bit in enumerate(ar))
        ci = sum(bit << (k-1-j) for j, bit in enumerate(bc))
        reduced_lift[ri][ci] += weight
    reduced_direct = [[Fraction(0) for _ in range(2**k)] for _ in range(2**k)]
    for row in range(2**n):
        rb = [(row >> (n-1-v)) & 1 for v in range(n)]
        for col in range(2**n):
            cb = [(col >> (n-1-v)) & 1 for v in range(n)]
            if all(rb[v] == cb[v] for v in range(n) if v not in chosen):
                ri = sum(rb[v] << (k-1-j) for j, v in enumerate(chosen))
                ci = sum(cb[v] << (k-1-j) for j, v in enumerate(chosen))
                reduced_direct[ri][ci] += product[row][col]
    assert reduced_lift == reduced_direct
    nonzero_off_charge = sum(reduced_lift[a][b] != 0 and a.bit_count() != b.bit_count()
                              for a in range(2**k) for b in range(2**k))
    return {"qubits": n, "two_qubit_gates": len(gate_spec)-fields, "field_gates": fields,
            "lifted_monomials_enumerated": enumerated, "contributing_lifted_monomials": accepted,
            "trace_exact": str(direct), "lifted_exact_once_coefficient": str(total),
            "open_boundary_reduced_entries_checked": 4**k,
            "nonzero_off_charge_entries_needing_adjusted_dummy_rank": nonzero_off_charge}


F = Fraction
exact_lift_cases = [
    homogeneous_lift_exact_case(1, [((0,), (2, -3), F(1, 7)), ((0,), (1, 4), F(2, 9)), ((0,), (3, 1), F(1, 5))]),
    homogeneous_lift_exact_case(3, [((0, 1), (2, -1), F(1, 7)), ((1, 2), (3, 3), F(1, 11)),
                                  ((0,), (1, -2), F(1, 13)), ((1,), (2, 3), F(1, 17)), ((2,), (1, -4), F(1, 19))]),
    homogeneous_lift_exact_case(2, [((0, 1), (3, -3), F(1, 11)), ((0,), (0, 3), F(1, 7)),
                                  ((1,), (2, -1), F(1, 5)), ((0,), (1, -3), F(1, 9)), ((1,), (3, 1), F(1, 13))]),
]

summary = {
    "seed": 261006724,
    "status": "PASS: finite diagnostics only; counting FPRAS not executed",
    "thermal_cases": len(thermal), "largest_tested_m": max(t["m"] for t in thermal),
    "max_generator_error_fraction_of_eps_over_four": max_generator_error_fraction,
    "max_log_trace_error_fraction_of_eps_over_four": max_log_trace_error_fraction,
    "largest_observed_shift_over_largest_eigenvalue": max_shift_over_largest_eigenvalue,
    "max_gibbs_distance_fraction_of_tanh_generator_bound": max_gibbs_distance_over_tanh_bound,
    "gate_hessian_fixtures": gate_tests,
    "max_scaled_positive_log_hessian_eigenvalue": max_scaled_positive_log_hessian,
    "outside_cone_counterexamples": outside_cone,
    "exact_homogeneous_field_lift_cases": exact_lift_cases,
    "thermal_details": thermal,
}
destination = Path(__file__).with_suffix(".json")
destination.write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({key: value for key, value in summary.items() if key != "thermal_details"}, indent=2))
