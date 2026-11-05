#!/usr/bin/env python3
"""Finite algebra checks for robust Gibbs-state block preparation.

These are small matrix checks of the newly used identities and inequalities.
They do not reconstruct the large-constant source sampler, prove its theorem,
simulate a device, or test a lifetime or resource advantage.

Dependencies: numpy, scipy, matplotlib.  Run from any directory:
    python verify_robust_blocks.py
The deterministic seed and all numerical residuals are written to JSON.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy.linalg import expm

SEED = 20261105
TOL = 2e-10
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1.0, -1.0]).astype(complex)
PAULI = (I2, X, Y, Z)


def kron_all(matrices):
    out = np.ones((1, 1), dtype=complex)
    for matrix in matrices:
        out = np.kron(out, matrix)
    return out


def hermitian(matrix):
    return (matrix + matrix.conj().T) / 2


def min_eig(matrix):
    return float(np.linalg.eigvalsh(hermitian(matrix))[0])


def op_norm(matrix):
    return float(np.linalg.norm(matrix, 2))


def trace_norm_hermitian(matrix):
    return float(np.abs(np.linalg.eigvalsh(hermitian(matrix))).sum())


def relative_residual(left, right):
    return float(np.linalg.norm(left - right) / max(1.0, np.linalg.norm(right)))


def positive_power(matrix, power):
    vals, vecs = np.linalg.eigh(hermitian(matrix))
    assert vals[0] > 0
    return (vecs * vals**power) @ vecs.conj().T


def random_hermitian(rng, dimension):
    a = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    return hermitian(a)


def random_density(rng, dimension, floor=0.35):
    a = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    rho = a @ a.conj().T
    rho /= np.trace(rho)
    return (1 - floor) * rho + floor * np.eye(dimension) / dimension


def apply_axis_matrix(tensor, matrix, axes):
    axes = list(axes)
    order = axes + [i for i in range(tensor.ndim) if i not in axes]
    reverse = np.argsort(order)
    moved = np.transpose(tensor, order)
    shape = moved.shape
    flat = moved.reshape(matrix.shape[1], -1)
    return np.transpose((matrix @ flat).reshape(shape), reverse)


def local_congruence(rho, operator, targets, n):
    tensor = rho.reshape((2,) * (2 * n))
    tensor = apply_axis_matrix(tensor, operator, targets)
    tensor = apply_axis_matrix(tensor, operator.conj(), [n + i for i in targets])
    return tensor.reshape(2**n, 2**n)


def local_superoperator(rho, superoperator, site, n):
    tensor = rho.reshape((2,) * (2 * n))
    tensor = apply_axis_matrix(tensor, superoperator.reshape(4, 4), [site, n + site])
    return tensor.reshape(2**n, 2**n)


def replacement_at_site(rho, site, n):
    tensor = rho.reshape((2,) * (2 * n))
    reduced = np.trace(tensor, axis1=site, axis2=n + site)
    expanded = np.expand_dims(np.expand_dims(reduced, site), n + site)
    shape = [1] * (2 * n)
    shape[site] = shape[n + site] = 2
    return (expanded * I2.reshape(shape) / 2).reshape(rho.shape)


def inverse_depolarizing(rho, contraction, n):
    out = rho.copy()
    for site in range(n):
        out = (out - (1 - contraction) * replacement_at_site(out, site, n)) / contraction
    return hermitian(out)


def forward_depolarizing(rho, contraction, n):
    out = rho.copy()
    for site in range(n):
        out = contraction * out + (1 - contraction) * replacement_at_site(out, site, n)
    return hermitian(out)


def permute_to_physical_order(operator, site_order):
    n = len(site_order)
    order = [site_order.index(i) for i in range(n)]
    axes = order + [n + i for i in order]
    return np.transpose(operator.reshape((2,) * (2 * n)), axes).reshape(operator.shape)


def make_sandwich(rng, k=2):
    d = 2**k
    q, _ = np.linalg.qr(rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d)))
    g = (q * rng.uniform(0.8, 1.2, size=d)) @ q.conj().T
    local = []
    for _ in range(k):
        direction = rng.normal(size=3)
        direction /= np.linalg.norm(direction)
        local.append(I2 + 0.1 * sum(direction[j] * PAULI[j + 1] for j in range(3)))
    f = 0.25 * kron_all(local)
    return hermitian(g), hermitian(f)


def soft_resolution(g, f, a):
    d = g.shape[0]
    s = a / 2
    delta = g - f
    root = positive_power(g, 0.5)
    invroot = positive_power(g, -0.5)
    matrix = hermitian(invroot @ delta @ invroot)
    vals, vecs = np.linalg.eigh(matrix)
    q = [(1 - s) * np.outer(vecs[:, t], vecs[:, t].conj()) + s * np.eye(d) / d
         for t in range(d)]
    b = (vals - s * vals.mean()) / (1 - s)
    e = [hermitian(root @ qt @ root) for qt in q]
    return delta, matrix, vals, q, b, e


def check_soft_spectral_and_first_cut(rng):
    a, k, trials = 0.1, 2, 16
    s, d = a / 2, 2**k
    residuals, margins, b_values = [], [], []
    samples = []
    for _ in range(trials):
        g, f = make_sandwich(rng, k)
        delta, matrix, vals, q, b, e = soft_resolution(g, f, a)
        margins.extend([min_eig(f - a * g), min_eig(g / 2 - f),
                        min_eig(delta - g / 2), min_eig((1 - a) * g - delta)])
        residuals.extend([relative_residual(sum(q), np.eye(d)),
                          relative_residual(sum(bt * qt for bt, qt in zip(b, q)), matrix),
                          relative_residual(sum(e), g),
                          relative_residual(sum(bt * et for bt, et in zip(b, e)), delta)])
        margins.extend(min_eig(et - (s / d) * g) for et in e)
        b_values.extend(b.tolist())
        assert vals.min() >= 0.5 - TOL and vals.max() <= 1 - a + TOL
        samples.append((g, f, delta, b, e))
    assert min(margins) >= -TOL
    assert min(b_values) >= -TOL and max(b_values) <= 1 - a / 2 + TOL
    assert max(residuals) < TOL

    # Three blocks suffice to check the exact expansion, not the large-L bound.
    triples = samples[:3]
    gs, fs, ds = ([row[j] for row in triples] for j in range(3))
    original = kron_all(gs)
    first_cut = kron_all([fs[0], gs[1], gs[2]]) + kron_all(ds)
    for b in (1, 2):
        first_cut += kron_all([ds[j] if j < b else fs[j] if j == b else gs[j]
                              for j in range(3)])
    expansion_residual = relative_residual(first_cut, original)
    exceptional = kron_all([fs[0], gs[1], gs[2]]) + kron_all(ds)
    reconstructed = np.zeros_like(exceptional)
    for t1, t2 in itertools.product(range(d), repeat=2):
        coefficient = triples[1][3][t1] * triples[2][3][t2]
        central = fs[0] + coefficient * ds[0]
        reconstructed += kron_all([central, triples[1][4][t1], triples[2][4][t2]])
    exceptional_residual = relative_residual(reconstructed, exceptional)
    assert max(expansion_residual, exceptional_residual) < TOL

    # The large-L estimate uses only 4x4 matrices, never a 4^L matrix.
    large_l = math.ceil(1 + 2 / a * (math.log(2 / a) + k * math.log(8)))
    central_factor = positive_power(fs[0], -0.5) @ ds[0] @ positive_power(fs[0], -0.5)
    actual_worst_norm = op_norm(central_factor) * max(triples[1][3]) ** (large_l - 1)
    analytic_bound = a**-1 * math.exp(-a * (large_l - 1) / 2)
    required_bound = 0.5 * 8**-k
    assert actual_worst_norm <= analytic_bound + TOL
    assert analytic_bound <= required_bound + TOL
    return {
        "status": "pass", "random_trials": trials, "elementary_qubits": k,
        "a": a, "s": s, "maximum_identity_residual": max(residuals),
        "minimum_sandwich_or_floor_margin": min(margins),
        "minimum_b": min(b_values), "maximum_b": max(b_values),
        "first_cut_three_block_residual": expansion_residual,
        "exceptional_remainder_residual": exceptional_residual,
        "large_L_scalar_check": {"L": large_l, "actual_worst_central_norm": actual_worst_norm,
                                  "analytic_bound": analytic_bound, "required_bound": required_bound},
        "scope": "Finite identities and scalar norm estimate; no large tensor product or source sampler."
    }


def check_mixed_pauli_decomposition(rng):
    k, u = 3, 0.5
    d = 2**k
    perturbation = random_hermitian(rng, d)
    perturbation *= (0.5 * 8**-k) / op_norm(perturbation)
    coefficients = []
    for word in itertools.product(range(4), repeat=k):
        matrix = kron_all(PAULI[p] for p in word)
        coefficient = float(np.trace(matrix @ perturbation).real / d)
        coefficients.append((word, coefficient))
    alpha_identity = coefficients[0][1]
    c = 1 + alpha_identity
    terms = [(word, coefficient, abs(coefficient) * u**-sum(p != 0 for p in word))
             for word, coefficient in coefficients[1:] if coefficient != 0]
    total_w = sum(weight for _, _, weight in terms)
    leftover = c - total_w
    assert leftover > 0
    delivered = (leftover / c) * np.eye(d, dtype=complex) / d
    all_weights = [leftover / c]
    minimum_product_eigenvalue = 1 / d
    product_count = 1
    for word, coefficient, weight in terms:
        support = [i for i, p in enumerate(word) if p]
        parity = 1 if coefficient > 0 else -1
        for initial in itertools.product((-1, 1), repeat=len(support) - 1):
            signs = list(initial) + [parity * math.prod(initial)]
            sign_by_site = dict(zip(support, signs))
            factors = [(I2 + sign_by_site[i] * u * PAULI[p]) / 2 if p else I2 / 2
                       for i, p in enumerate(word)]
            state = kron_all(factors)
            probability = weight / c / 2**(len(support) - 1)
            delivered += probability * state
            all_weights.append(probability)
            minimum_product_eigenvalue = min(minimum_product_eigenvalue, min_eig(state))
            product_count += 1
    target = (np.eye(d) + perturbation) / (d * c)
    residual = trace_norm_hermitian(delivered - target)
    assert residual < TOL
    assert min(all_weights) >= 0 and abs(sum(all_weights) - 1) < TOL
    assert minimum_product_eigenvalue >= 4**-k - TOL
    return {
        "status": "pass", "qubits": k, "bloch_radius": u,
        "perturbation_operator_norm": op_norm(perturbation),
        "sum_pauli_weights_before_normalization": total_w, "identity_leftover": leftover,
        "positive_product_components": product_count,
        "minimum_component_weight": min(all_weights),
        "minimum_product_state_eigenvalue": minimum_product_eigenvalue,
        "required_product_floor": 4**-k,
        "trace_norm_reconstruction_error": residual
    }


def check_ring_transfer_and_dressing(rng):
    q, m = 3, 3
    n = q * m
    cuts = (1, 2)
    local = []
    for _ in range(q):
        choices = []
        for label, cut in enumerate(cuts):
            left = (0.4 + 0.2 * label) * random_density(rng, 2**cut)
            right = random_density(rng, 2**(m - cut))
            choices.append((left, right))
        local.append(choices)
    dressing = []
    for _ in range(q):
        a, b = random_hermitian(rng, 4), random_hermitian(rng, 4)
        dressing.append(expm(0.10 * a / op_norm(a)) @ expm(0.07 * b / op_norm(b)))
    edge_operators, transfers = [], []
    for s in range(q):
        edge = {}
        transfer = np.zeros((2, 2))
        for a, b in itertools.product(range(2), repeat=2):
            right, left = local[s][a][1], local[(s + 1) % q][b][0]
            right_sites, left_sites = m - cuts[a], cuts[b]
            operator = local_congruence(np.kron(right, left), dressing[s],
                                       [right_sites - 1, right_sites], right_sites + left_sites)
            edge[a, b] = operator
            transfer[a, b] = float(np.trace(operator).real)
        edge_operators.append(edge)
        transfers.append(transfer)

    def dress_global(rho):
        for s, operator in enumerate(dressing):
            rho = local_congruence(rho, operator, [(s * m + m - 1) % n, ((s + 1) * m) % n], n)
        return rho

    totals = [sum(np.kron(left, right) for left, right in choices) for choices in local]
    target_raw = dress_global(kron_all(totals))
    partition_function = float(np.trace(target_raw).real)
    matrix_product = transfers[0] @ transfers[1] @ transfers[2]
    transfer_z = float(np.trace(matrix_product))
    assert abs(partition_function - transfer_z) < TOL
    probabilities0 = np.diag(matrix_product) / transfer_z
    mixture = np.zeros_like(target_raw)
    trace_weight_residuals, factorization_residuals, sampler_residuals = [], [], []
    configurations = []
    for labels in itertools.product(range(2), repeat=q):
        factors = [np.kron(*local[s][labels[s]]) for s in range(q)]
        direct = dress_global(kron_all(factors))
        weight = float(np.trace(direct).real)
        edge_weight = math.prod(transfers[s][labels[s], labels[(s + 1) % q]] for s in range(q))
        trace_weight_residuals.append(abs(weight - edge_weight))
        block_operators, site_order = [], []
        for s in range(q):
            a, b = labels[s], labels[(s + 1) % q]
            block = edge_operators[s][a, b]
            block_operators.append(block / np.trace(block))
            site_order.extend(range(s * m + cuts[a], (s + 1) * m))
            next_s = (s + 1) % q
            site_order.extend(range(next_s * m, next_s * m + cuts[b]))
        block_product = permute_to_physical_order(kron_all(block_operators), site_order)
        factorization_residuals.append(relative_residual(block_product, direct / weight))
        mixture += (edge_weight / transfer_z) * block_product

        # Actual forward/backward conditional-probability formula, not simulation.
        a0, a1, a2 = labels
        forward1 = transfers[0][a0]
        forward2 = forward1 @ transfers[1]
        p2 = forward2[a2] * transfers[2][a2, a0] / (matrix_product[a0, a0])
        p1 = forward1[a1] * transfers[1][a1, a2] / forward2[a2]
        probability = float(probabilities0[a0] * p2 * p1)
        sampler_residuals.append(abs(probability - edge_weight / transfer_z))
        configurations.append({"labels": list(labels), "weight": edge_weight,
                               "probability": probability})
    mixture_error = trace_norm_hermitian(mixture - target_raw / partition_function)
    assert max(trace_weight_residuals + factorization_residuals + sampler_residuals) < TOL
    assert mixture_error < TOL
    return {
        "status": "pass", "ring_qubits": n, "superblocks": q,
        "superblock_qubits": m, "cut_positions_per_superblock": list(cuts),
        "enumerated_label_configurations": len(configurations),
        "maximum_B5_trace_weight_error": max(trace_weight_residuals),
        "maximum_dressed_block_factorization_residual": max(factorization_residuals),
        "maximum_forward_backward_probability_error": max(sampler_residuals),
        "global_trace_norm_mixture_error": mixture_error,
        "transfer_partition_function_error": abs(transfer_z - partition_function),
        "minimum_dressing_singular_value": min(float(np.linalg.svd(operator, compute_uv=False)[-1])
                                                for operator in dressing),
        "configurations": configurations,
        "scope": "Toy full-rank cut ensembles with nonunitary local dressings; verifies B5 algebra and actual global state, not the source QPI sampler."
    }


def check_nonunital_norm_bound(rng):
    n = 3
    rho = random_density(rng, 2**n)
    eta = 2**n * min_eig(rho)
    gammas = (0.001, 0.0015, 0.0007)
    maps, inverses, diamond_bounds = [], [], []
    for gamma in gammas:
        k0 = np.diag([1.0, math.sqrt(1 - gamma)]).astype(complex)
        k1 = np.array([[0.0, math.sqrt(gamma)], [0.0, 0.0]], dtype=complex)
        channel = sum(np.einsum("ac,bd->abcd", k, k.conj()) for k in (k0, k1))
        maps.append(channel)
        inverses.append(np.linalg.inv(channel.reshape(4, 4)).reshape(2, 2, 2, 2))
        # Triangle/Kraus bound: ||K0-I|| (||K0||+1) + ||K1||^2.
        diamond_bounds.append(2 * (1 - math.sqrt(1 - gamma)) + gamma)
    preimage = rho.copy()
    for site, inverse in enumerate(inverses):
        preimage = local_superoperator(preimage, inverse, site, n)
    restored = preimage.copy()
    for site, channel in enumerate(maps):
        restored = local_superoperator(restored, channel, site, n)
    bound = math.prod(1 / (1 - delta) for delta in diamond_bounds) - 1
    uniform_bound = (1 - max(diamond_bounds))**-n - 1
    observed = trace_norm_hermitian(preimage - rho)
    assert observed <= bound + TOL
    assert uniform_bound <= eta / 2**(n + 1)
    assert min_eig(preimage) >= eta / (2 * 2**n) - TOL
    assert trace_norm_hermitian(restored - rho) < TOL
    return {
        "status": "pass", "qubits": n, "channel": "heterogeneous amplitude damping",
        "gamma_by_site": list(gammas), "rigorous_diamond_distance_upper_bounds": diamond_bounds,
        "initial_normalized_spectral_floor_eta": eta,
        "observed_inverse_trace_norm_correction": observed,
        "heterogeneous_Neumann_bound": bound, "uniform_Neumann_bound": uniform_bound,
        "permitted_correction_for_half_floor": eta / 2**(n + 1),
        "preimage_minimum_eigenvalue": min_eig(preimage),
        "required_half_floor": eta / (2 * 2**n),
        "forward_restoration_trace_norm_error": trace_norm_hermitian(restored - rho)
    }


def embedded_pauli(n, assignments):
    return kron_all(PAULI[assignments.get(site, 0)] for site in range(n))


def partial_trace_keep(rho, keep, n):
    tensor = rho.reshape((2,) * (2 * n))
    remaining = list(range(n))
    for site in reversed(range(n)):
        if site not in keep:
            index = remaining.index(site)
            tensor = np.trace(tensor, axis1=index, axis2=len(remaining) + index)
            remaining.remove(site)
    return tensor.reshape(2**len(keep), 2**len(keep))


def threshold_contraction(rho, n):
    low, high = 0.05, 1.0
    if min_eig(inverse_depolarizing(rho, low, n)) >= 0:
        return low
    for _ in range(46):
        middle = (low + high) / 2
        if min_eig(inverse_depolarizing(rho, middle, n)) >= 0:
            high = middle
        else:
            low = middle
    return high


def check_finite_noncommuting_gibbs():
    n = 5
    h = np.zeros((2**n, 2**n), dtype=complex)
    for site in range(n):
        h -= 0.62 * embedded_pauli(n, {site: 3, (site + 1) % n: 3})
        h -= 0.27 * embedded_pauli(n, {site: 1})
        h -= 0.11 * embedded_pauli(n, {site: 3})
    local_h = -0.62 * np.kron(Z, Z) - 0.27 * np.kron(X, I2) - 0.11 * np.kron(Z, I2)
    assert op_norm(local_h) <= 1 + TOL
    energies, vectors = np.linalg.eigh(h)

    def thermal(beta):
        weights = np.exp(-beta * (energies - energies.min()))
        return (vectors * (weights / weights.sum())) @ vectors.conj().T

    beta_grid = np.linspace(0.2, 3.0, 22)
    curve = []
    for beta in beta_grid:
        rho = thermal(float(beta))
        curve.append({"beta": float(beta), "critical_lambda_numeric": threshold_contraction(rho, n)})
    examples = []
    for beta in (0.2, 0.5, 1.0, 2.0, 3.0):
        rho = thermal(beta)
        critical = threshold_contraction(rho, n)
        good_lambda = (1 + critical) / 2
        bad_lambda = max(0.05, critical - 0.02)
        good = inverse_depolarizing(rho, good_lambda, n)
        bad = inverse_depolarizing(rho, bad_lambda, n)
        restored = forward_depolarizing(good, good_lambda, n)
        pair = partial_trace_keep(rho, [0, 1], n)
        pair_pt = np.transpose(pair.reshape(2, 2, 2, 2), [0, 3, 2, 1]).reshape(4, 4)
        error = trace_norm_hermitian(restored - rho)
        assert min_eig(good) >= -TOL and min_eig(bad) < -1e-8
        assert error < TOL
        examples.append({"beta": beta, "target_minimum_eigenvalue": min_eig(rho),
                         "critical_lambda_numeric": critical, "positive_example_lambda": good_lambda,
                         "positive_preimage_minimum_eigenvalue": min_eig(good),
                         "negative_example_lambda": bad_lambda,
                         "negative_preimage_minimum_eigenvalue": min_eig(bad),
                         "forward_restoration_trace_norm_error": error,
                         "neighbor_partial_transpose_minimum_eigenvalue": min_eig(pair_pt)})
    commutator = np.kron(Z, Z) @ np.kron(X, I2) - np.kron(X, I2) @ np.kron(Z, Z)
    return {
        "status": "pass", "qubits": n, "boundary": "periodic",
        "hamiltonian": "H=sum_i[-0.62 Z_i Z_(i+1)-0.27 X_i-0.11 Z_i]",
        "local_term_operator_norm": op_norm(local_h),
        "noncommuting_term_commutator_frobenius_norm": float(np.linalg.norm(commutator)),
        "examples": examples, "threshold_curve": curve,
        "scope": "Numerically exact five-qubit matrices. These thresholds are not the uniform theorem threshold and imply no scaling, hardware, sampler-runtime, or lifetime claim."
    }


def check_heisenberg_dimer():
    h = (np.kron(X, X) + np.kron(Y, Y) + np.kron(Z, Z)) / 3
    pair_sum = 3 * h
    max_target_error, max_min_eig_error, max_restore_error = 0.0, 0.0, 0.0
    points = []
    for beta, contraction in itertools.product((0.0, 0.4, 0.9, 1.4, 2.0, 3.0), (0.5, 0.65, 0.8, 0.95)):
        x = math.exp(4 * beta / 3)
        t = (x - 1) / (x + 3)
        rho = expm(-beta * h)
        rho /= np.trace(rho)
        formula = (np.eye(4) - t * pair_sum) / 4
        preimage = inverse_depolarizing(rho, contraction, 2)
        predicted_min = (1 - t / contraction**2) / 4
        max_target_error = max(max_target_error, trace_norm_hermitian(rho - formula))
        max_min_eig_error = max(max_min_eig_error, abs(min_eig(preimage) - predicted_min))
        max_restore_error = max(max_restore_error, trace_norm_hermitian(
            forward_depolarizing(preimage, contraction, 2) - rho))
        if abs(t - contraction**2) > 1e-10:
            assert (min_eig(preimage) > 0) == (t < contraction**2)
        points.append({"beta": beta, "lambda": contraction, "t": t,
                       "inverse_minimum_eigenvalue": min_eig(preimage),
                       "positive_preimage": bool(t <= contraction**2),
                       "entangled_target": bool(t > 1 / 3)})
    assert max(max_target_error, max_min_eig_error, max_restore_error) < TOL
    beta_entangled = 0.75 * math.log(3)
    lambda_example = 0.8
    beta_max_example = 0.75 * math.log((1 + 3 * lambda_example**2) / (1 - lambda_example**2))
    return {
        "status": "pass", "hamiltonian": "(XX+YY+ZZ)/3", "grid_points": len(points),
        "exact_positive_preimage_condition": "t <= lambda^2; t=(exp(4 beta/3)-1)/(exp(4 beta/3)+3)",
        "exact_entangled_target_condition": "t > 1/3",
        "maximum_thermal_formula_trace_norm_error": max_target_error,
        "maximum_inverse_minimum_eigenvalue_formula_error": max_min_eig_error,
        "maximum_forward_restoration_trace_norm_error": max_restore_error,
        "entangled_preparable_example": {"lambda": lambda_example,
                                        "beta_open_lower_bound": beta_entangled,
                                        "beta_closed_upper_bound": beta_max_example},
        "points": points
    }


def make_plot(results, output_dir):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.8))
    curve = results["finite_noncommuting_gibbs"]["threshold_curve"]
    beta = np.array([point["beta"] for point in curve])
    allowance = np.array([1 - point["critical_lambda_numeric"] for point in curve])
    axes[0].semilogy(beta, allowance, "o-", color="#135b83", markersize=4)
    axes[0].set(xlabel=r"Inverse temperature $\beta$", ylabel=r"Maximum contraction loss $1-\lambda_{\rm crit}$",
                title="A. Finite noncommuting five-spin ring")
    axes[0].grid(alpha=0.2, which="both")
    axes[0].text(0.03, 0.04, "Finite matrix thresholds\nNot a size-independent bound", transform=axes[0].transAxes,
                 fontsize=9, va="bottom")

    beta = np.linspace(0, 3, 350)
    x = np.exp(4 * beta / 3)
    critical = np.sqrt((x - 1) / (x + 3))
    boundary = results["heisenberg_dimer"]["entangled_preparable_example"]["beta_open_lower_bound"]
    axes[1].fill_between(beta, critical, 1, color="#c8e4e2", label="Positive exact preimage")
    axes[1].fill_between(beta, critical, 1, where=beta > boundary, color="#5fae9b", alpha=0.75,
                         label="Also an entangled target")
    axes[1].plot(beta, critical, color="#184a46", linewidth=1.8, label=r"Exact boundary: $\lambda=\sqrt{t(\beta)}$")
    axes[1].axvline(boundary, color="#7a4a65", linestyle="--", linewidth=1)
    axes[1].set(xlabel=r"Inverse temperature $\beta$", ylabel=r"Depolarizing Bloch contraction $\lambda$",
                title="B. Exact Heisenberg-dimer boundary", xlim=(0, 3), ylim=(0, 1))
    axes[1].legend(loc="lower right", frameon=False, fontsize=8)
    fig.suptitle("Finite checks of positive inverse-noise preparation", fontsize=13)
    fig.text(0.5, 0.01, "Algebra and small matrices only; no source-sampler, apparatus, lifetime, or resource-advantage simulation.",
             ha="center", fontsize=8)
    fig.tight_layout(rect=(0, 0.045, 1, 0.93))
    for suffix in ("png", "pdf"):
        fig.savefig(output_dir / f"verification_summary.{suffix}", dpi=180)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    rng = np.random.default_rng(SEED)
    results = {
        "schema": "robust-blocks-finite-verification-v1", "seed": SEED,
        "numerical_assertion_tolerance": TOL,
        "scope": "Finite matrix identities, positive decompositions, transfer weights, and inverse-noise examples only. No huge-constant source sampler, physical experiment, device simulation, lifetime, or resource advantage is tested.",
        "soft_spectral_and_first_cut": check_soft_spectral_and_first_cut(rng),
        "mixed_pauli": check_mixed_pauli_decomposition(rng),
        "ring_transfer_and_dressing": check_ring_transfer_and_dressing(rng),
        "nonunital_norm_bound": check_nonunital_norm_bound(rng),
        "finite_noncommuting_gibbs": check_finite_noncommuting_gibbs(),
        "heisenberg_dimer": check_heisenberg_dimer()
    }
    make_plot(results, args.output_dir)
    results["elapsed_seconds"] = time.perf_counter() - started
    results["all_checks_passed"] = True
    output = args.output_dir / "verification_results.json"
    output.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"all_checks_passed": True, "elapsed_seconds": results["elapsed_seconds"],
                      "json": str(output), "figures": [str(args.output_dir / ("verification_summary." + suffix))
                                                         for suffix in ("png", "pdf")],
                      "global_ring_trace_error": results["ring_transfer_and_dressing"]["global_trace_norm_mixture_error"],
                      "mixed_pauli_trace_error": results["mixed_pauli"]["trace_norm_reconstruction_error"]}, indent=2))


if __name__ == "__main__":
    main()
