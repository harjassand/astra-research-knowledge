"""Finite, full-channel checks for the late-selector payload construction.

This program is diagnostic evidence for the analytic proof. It does not
simulate an asymptotically large expander or certify a laboratory device.
All Choi states below are normalized to trace one; errors reported for
Choi states are half trace distances, not computed diamond norms.
"""
from itertools import product
from pathlib import Path
import json
import numpy as np

SEED = 2026110502
RNG = np.random.default_rng(SEED)
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
H = (X + Z) / np.sqrt(2)
PAULIS = [I2, X, Y, Z]
LOCAL_EIGENBASES = [I2, H, np.array([[1, 1], [1j, -1j]]) / np.sqrt(2), I2]


def kron_all(factors):
    answer = np.ones((1, 1), complex)
    for factor in factors:
        answer = np.kron(answer, factor)
    return answer


def trace_norm(matrix):
    if np.linalg.norm(matrix - matrix.conj().T) < 1e-10:
        return float(np.sum(np.abs(np.linalg.eigvalsh(matrix))))
    return float(np.sum(np.linalg.svd(matrix, compute_uv=False)))


def choi(kraus, input_dimension):
    answer = np.zeros((kraus[0].size, kraus[0].size), complex)
    for operator in kraus:
        vector = operator.reshape(-1, order="F")
        answer += np.outer(vector, vector.conj()) / input_dimension
    return answer


def partial_trace_kraus(gauge_dimension):
    return [np.kron(I2, np.eye(gauge_dimension)[k:k+1])
            for k in range(gauge_dimension)]


def controlled_zero(unitary):
    dimension = len(unitary)
    answer = np.eye(2 * dimension, dtype=complex)
    answer[:dimension, :dimension] = unitary
    return answer


def pauli_selector(n, labels):
    gauge = kron_all([PAULIS[k] for k in labels])
    return controlled_zero(gauge) @ np.kron(H, np.eye(2**n))


def local_eigenmeasurement_decoder(n, labels):
    """Return actual product-eigenmeasurement / recorded-parity Kraus maps.

    A branch consists of one single-qubit eigenmeasurement on each gauge
    carrier, accumulation of its Pauli eigenvalue, and H Z^parity on the
    flag. No global eigenbasis diagonalization or bath labels are used.
    """
    encoding = pauli_selector(n, labels)
    branches = []
    for outcomes in product(range(2), repeat=n):
        vectors = [LOCAL_EIGENBASES[label][:, outcome:outcome+1]
                   for label, outcome in zip(labels, outcomes)]
        gauge_bra = kron_all(vectors).conj().T
        parity = sum(outcome for label, outcome in zip(labels, outcomes)
                     if label != 0) % 2
        correction = H @ (Z if parity else I2)
        branches.append(correction @ np.kron(I2, gauge_bra) @ encoding)
    return branches


def early_decoder_checks():
    results = []
    for n in range(1, 5):
        dimension = 2**n
        expected = choi(partial_trace_kraus(dimension), 2 * dimension)
        worst_choi, worst_tp, count, branches = 0.0, 0.0, 0, 0
        for labels in product(range(4), repeat=n):
            operators = local_eigenmeasurement_decoder(n, labels)
            actual = choi(operators, 2 * dimension)
            worst_choi = max(worst_choi, 0.5 * trace_norm(actual - expected))
            tp = sum(k.conj().T @ k for k in operators)
            worst_tp = max(worst_tp, float(np.linalg.norm(tp - np.eye(2 * dimension))))
            count += 1
            branches += len(operators)
        # The Z-anchor encoder is identity and its decoder discards gauge.
        anchor_error = 0.5 * trace_norm(
            choi(partial_trace_kraus(dimension), 2 * dimension) - expected)
        # A separate fixed correlated mixed gauge channel check.
        ghz = np.zeros(dimension, complex)
        ghz[0] = ghz[-1] = 1 / np.sqrt(2)
        gauge = 0.7 * np.outer(ghz, ghz.conj()) + 0.3 * np.eye(dimension) / dimension
        eigenvalues, eigenvectors = np.linalg.eigh(gauge)
        operators = local_eigenmeasurement_decoder(n, tuple((i % 3) + 1 for i in range(n)))
        payload_kraus = [np.sqrt(value) * operator @ np.kron(I2, eigenvectors[:, k:k+1])
                         for operator in operators
                         for k, value in enumerate(eigenvalues)]
        bell_choi = choi([I2], 2)
        mixed_gauge_error = 0.5 * trace_norm(choi(payload_kraus, 2) - bell_choi)
        results.append({
            "gauge_qubits": n, "pauli_selectors_checked": count,
            "local_measurement_branches_checked": branches,
            "max_full_input_choi_half_trace_error_to_partial_trace": worst_choi,
            "max_trace_preservation_frobenius_residue": worst_tp,
            "anchor_choi_half_trace_error": anchor_error,
            "correlated_mixed_gauge_payload_choi_half_trace_error": mixed_gauge_error,
            "gauge_distance_from_product_tracial_in_frobenius_norm":
                float(np.linalg.norm(gauge - np.eye(dimension) / dimension)),
        })
    return results


def selector_observables(n):
    dimension = 2**n
    observables = [np.kron(Z, np.eye(dimension))]
    weights = [1 / 3]
    for labels in product(range(4), repeat=n):
        observables.append(np.kron(X, kron_all([PAULIS[k] for k in labels])))
        weights.append((2 / 3) / 4**n)
    return observables, np.array(weights)


def gap_checks():
    results = []
    for n in range(1, 4):
        observables, weights = selector_observables(n)
        dimension = len(observables[0])
        # Direct matrix on the entire complex operator space, column vec.
        laplacian = 2 * np.eye(dimension**2, dtype=complex)
        for weight, observable in zip(weights, observables):
            laplacian -= 2 * weight * np.kron(observable.conj(), observable)
        eigenvalues = np.linalg.eigvalsh(laplacian)
        nonzero = eigenvalues[eigenvalues > 1e-10]
        results.append({
            "gauge_qubits": n, "operator_space_dimension": dimension**2,
            "nullity": int(np.sum(np.abs(eigenvalues) <= 1e-10)),
            "computed_commutator_gap": float(nonzero[0]),
            "error_to_4_over_3": float(abs(nonzero[0] - 4/3)),
            "spectrum": [{"eigenvalue": value,
                          "multiplicity": int(np.sum(np.abs(eigenvalues - value) <= 1e-9))}
                         for value in [0, 4/3, 8/3, 4]],
        })
    return results


def random_isometry(rows, columns):
    matrix = RNG.normal(size=(rows, columns)) + 1j * RNG.normal(size=(rows, columns))
    q, _ = np.linalg.qr(matrix)
    return q[:, :columns]


def random_hybrid_compression(dimension, memory, branches, environment):
    isometry = random_isometry(branches * environment * memory, dimension)
    isometry = isometry.reshape(branches, environment, memory, dimension)
    return [[isometry[r, e] for e in range(environment)] for r in range(branches)]


def damped_block_compression(dimension, memory, complete_damping=False):
    unitary = random_isometry(dimension, dimension)
    blocks = []
    for r in range(dimension // memory):
        block = unitary[r * memory:(r + 1) * memory]
        gamma = 1.0 if complete_damping else (0.15 + 0.65 * RNG.random())
        e0 = np.array([[1, 0], [0, np.sqrt(1-gamma)]], complex)
        e1 = np.array([[0, np.sqrt(gamma)], [0, 0]], complex)
        blocks.append([np.kron(e, np.eye(memory // 2)) @ block for e in [e0, e1]])
    return blocks


def petz_check(n, blocks, kind):
    observables, weights = selector_observables(n)
    dimension, memory = len(observables[0]), blocks[0][0].shape[0]
    sigmas, inverse_roots = [], []
    largest_nontraciality, singular_blocks = 0.0, 0
    for operators in blocks:
        sigma = sum(a @ a.conj().T for a in operators) / dimension
        values, vectors = np.linalg.eigh(sigma)
        singular_blocks += int(np.any(values < 1e-12))
        inverse_values = np.zeros_like(values)
        inverse_values[values > 1e-12] = 1 / np.sqrt(values[values > 1e-12])
        inverse_roots.append((vectors * inverse_values) @ vectors.conj().T)
        sigmas.append(sigma)
        probability = np.trace(sigma).real
        largest_nontraciality = max(largest_nontraciality, 0.5 * trace_norm(
            sigma / probability - np.eye(memory) / memory))
    composite_kraus = [a.conj().T @ inverse @ b / np.sqrt(dimension)
                      for operators, inverse in zip(blocks, inverse_roots)
                      for a in operators for b in operators]
    fe = sum(abs(np.trace(k))**2 for k in composite_kraus) / dimension**2
    q_values, t_values = [], []
    max_correlation_identity_error = 0.0
    for observable in observables:
        t, q = 0.0, 0.0
        for operators, inverse in zip(blocks, inverse_roots):
            x = sum(a @ observable @ a.conj().T for a in operators) / dimension
            t += trace_norm(x)
            q += np.trace(x @ inverse @ x @ inverse).real
        reconstructed = sum(k @ observable @ k.conj().T for k in composite_kraus)
        q_direct = np.trace(observable @ reconstructed).real / dimension
        max_correlation_identity_error = max(max_correlation_identity_error, abs(q - q_direct))
        t_values.append(t)
        q_values.append(q)
    q_values, t_values = np.array(q_values), np.array(t_values)
    gap_fe_lower_bound = 1 - 1.5 * (1 - np.dot(weights, q_values))
    return {
        "kind": kind, "gauge_qubits": n, "input_dimension": dimension,
        "memory_dimension_per_classical_branch": memory,
        "classical_branches": len(blocks), "singular_sigma_blocks": singular_blocks,
        "max_conditional_sigma_half_trace_distance_from_tracial": largest_nontraciality,
        "min_q_minus_t_squared": float(np.min(q_values - t_values**2)),
        "max_direct_vs_weighted_petz_correlation_error": float(max_correlation_identity_error),
        "petz_entanglement_fidelity": float(fe),
        "memory_fidelity_upper_bound": memory / dimension,
        "fidelity_upper_bound_slack": float(memory / dimension - fe),
        "commutator_gap_fidelity_lower_bound": float(gap_fe_lower_bound),
        "gap_lower_bound_slack": float(fe - gap_fe_lower_bound),
        "composite_trace_preservation_residue": float(np.linalg.norm(
            sum(k.conj().T @ k for k in composite_kraus) - np.eye(dimension))),
        "max_composite_kraus_rank": max(int(np.linalg.matrix_rank(k, tol=1e-10))
                                         for k in composite_kraus),
    }


def petz_checks():
    results = []
    settings = [(1, 1, 3, 2), (1, 2, 2, 2),
                (2, 2, 3, 3), (2, 4, 2, 2)]
    for n, memory, branches, environment in settings:
        for _ in range(6):
            results.append(petz_check(n, random_hybrid_compression(
                2**(n+1), memory, branches, environment), "random_isometry_hybrid"))
    for n, memory in [(1, 2), (2, 2), (2, 4)]:
        for complete in [False, True]:
            results.append(petz_check(n, damped_block_compression(
                2**(n+1), memory, complete),
                "random_block_measurement_then_" + ("full_reset" if complete else "amplitude_damping")))
    # Constants are also tested on a boundary case: measuring one gauge Z
    # and retaining its classical result saturates both Fe <= m/N and the
    # commutator-gap Fe bound, with Fe=m/N=1/2.
    for n in [1, 2]:
        rest_dimension = 2**(n-1)
        blocks = [[np.kron(I2, np.kron(np.eye(2)[r:r+1], np.eye(rest_dimension)))]
                  for r in range(2)]
        results.append(petz_check(n, blocks, "fixed_one_gauge_Z_boundary_case"))
    return results


def payload_choi_from_action(action):
    result = np.zeros((4, 4), complex)
    for a, b in product(range(2), repeat=2):
        matrix = np.zeros((2, 2), complex)
        matrix[a, b] = 1
        result[2*a:2*a+2, 2*b:2*b+2] = action(matrix) / 2
    return result


def measure_one_gauge_baseline(n):
    gauge_dimension, rest_dimension = 2**n, 2**(n-1)
    target = (5 / 6) * choi([I2], 2) + (1 / 6) * choi([X], 2)
    total = (1 / 3) * choi([I2], 2)  # anchor branch
    for labels in product(range(4), repeat=n):
        encoding = pauli_selector(n, labels)
        rest_pauli = kron_all([PAULIS[k] for k in labels[1:]])
        corrections = []
        measurements = []
        for outcome in range(2):
            phase = outcome if labels[0] == 3 else 0
            correction = np.kron(H @ (Z if phase else I2), np.eye(rest_dimension))
            corrections.append(correction @ controlled_zero(rest_pauli).conj().T)
            measurements.append(np.kron(I2, np.kron(
                np.eye(2)[outcome:outcome+1], np.eye(rest_dimension))))

        def action(payload):
            encoded = encoding @ np.kron(payload, np.eye(gauge_dimension) / gauge_dimension) @ encoding.conj().T
            answer = np.zeros((2, 2), complex)
            for measurement, correction in zip(measurements, corrections):
                reduced = measurement @ encoded @ measurement.conj().T
                corrected = correction @ reduced @ correction.conj().T
                answer += np.trace(corrected.reshape(2, rest_dimension, 2, rest_dimension),
                                   axis1=1, axis2=3)
            return answer

        total += ((2 / 3) / 4**n) * payload_choi_from_action(action)
    return {
        "gauge_qubits": n,
        "choi_half_trace_error_to_5_over_6_identity_plus_1_over_6_X":
            0.5 * trace_norm(total - target),
        "choi_half_trace_error_to_identity": 0.5 * trace_norm(total - choi([I2], 2)),
        "memory_dimension_after_flag": gauge_dimension,
        "uncompressed_dimension_after_flag": 2 * gauge_dimension,
        "analytic_half_diamond_error_for_target_pauli_channel": 1 / 6,
    }


def main():
    results = {
        "seed": SEED,
        "conventions": {
            "analytic_error": "half diamond distance",
            "executed_channel_check": "half trace distance of normalized Choi states",
            "commutator_gap": "sum p_j ||[K,H_j]||_2^2 >= kappa ||K-Tr(K)I/N||_2^2",
            "selector_weights": "Z anchor 1/3; each of 4^n lifted Pauli selectors (2/3)/4^n",
        },
        "early_local_measurement_decoder": early_decoder_checks(),
        "direct_commutator_superoperator_spectra": gap_checks(),
        "petz_and_hybrid_memory_checks": petz_checks(),
        "measure_one_gauge_Z_baseline": [measure_one_gauge_baseline(n) for n in range(1, 4)],
        "scope": [
            "The early check compares the entire flag-plus-gauge input channel to partial trace, so it tests more than independent tracial gauge.",
            "The full input Choi check includes arbitrary correlations of the initial gauge with other systems at the operation level.",
            "No large expander, fault-tolerant factory, physical calibration, or laboratory execution is simulated.",
            "Small numerical checks supplement the analytic proof; they do not prove its all-dimension statement.",
        ],
    }
    assert max(r["max_full_input_choi_half_trace_error_to_partial_trace"]
               for r in results["early_local_measurement_decoder"]) < 1e-11
    assert max(r["error_to_4_over_3"] for r in results["direct_commutator_superoperator_spectra"]) < 1e-10
    for check in results["petz_and_hybrid_memory_checks"]:
        assert check["min_q_minus_t_squared"] > -1e-10
        assert check["fidelity_upper_bound_slack"] > -1e-10
        assert check["gap_lower_bound_slack"] > -1e-10
        assert check["composite_trace_preservation_residue"] < 1e-9
        assert check["max_composite_kraus_rank"] <= check["memory_dimension_per_classical_branch"]
    assert max(r["choi_half_trace_error_to_5_over_6_identity_plus_1_over_6_X"]
               for r in results["measure_one_gauge_Z_baseline"]) < 1e-11
    destination = Path(__file__).with_name("payload_memory_verification.json")
    destination.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({
        "saved": str(destination),
        "early_selectors_checked": sum(r["pauli_selectors_checked"] + 1
                                       for r in results["early_local_measurement_decoder"]),
        "maximum_early_full_choi_error": max(r["max_full_input_choi_half_trace_error_to_partial_trace"]
                                             for r in results["early_local_measurement_decoder"]),
        "gap_checks": len(results["direct_commutator_superoperator_spectra"]),
        "hybrid_compression_checks": len(results["petz_and_hybrid_memory_checks"]),
        "minimum_petz_q_minus_t_squared": min(r["min_q_minus_t_squared"]
                                              for r in results["petz_and_hybrid_memory_checks"]),
        "maximum_baseline_channel_error": max(r["choi_half_trace_error_to_5_over_6_identity_plus_1_over_6_X"]
                                              for r in results["measure_one_gauge_Z_baseline"]),
    }, indent=2))


if __name__ == "__main__":
    main()
