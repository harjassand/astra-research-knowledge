#!/usr/bin/env python3
"""Numerical diagnostics for exact adversarial lemmas; no capacity certificate.

The proofs are in ../e4_adversarial.txt.  This script checks their constants
and independently compares the rare-excitation Holevo upper bound with a
finite, physical cutoff-erasure calculation of coherent information.
Requires Python and numpy.  All logarithms in information quantities use 2.
"""

import json
import math
from pathlib import Path

import numpy as np


def h2(p):
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def bosonic_entropy(n):
    if n <= 0.0:
        return 0.0
    return (n + 1.0) * math.log2(n + 1.0) - n * math.log2(n)


def entropy_from_eigenvalues(values):
    values = np.asarray(values, dtype=float)
    values = values[values > 1e-16]
    return float(-np.dot(values, np.log2(values)))


def fock_output_probabilities(eta, nu, n, cutoff):
    """Retained diagonal of Phi(|n><n|), using loss then amplification."""
    gain = 1.0 + (1.0 - eta) * nu
    transmission = eta / gain
    out = np.zeros(cutoff + 1)
    for lost in range(n + 1):
        surviving = n - lost
        loss_probability = (
            math.comb(n, lost)
            * transmission**surviving
            * (1.0 - transmission) ** lost
        )
        for final in range(surviving, cutoff + 1):
            added = final - surviving
            amplifier_probability = (
                math.comb(final, added)
                * (gain - 1.0) ** added
                / gain ** (final + 1)
            )
            out[final] += loss_probability * amplifier_probability
    return out


def vacuum_fock_offdiagonal(eta, nu, n, cutoff):
    """Retained Phi(|0><n|); row k, column k+n is its sole band."""
    gain = 1.0 + (1.0 - eta) * nu
    transmission = eta / gain
    out = np.zeros((cutoff + 1, cutoff + 1))
    for added in range(cutoff - n + 1):
        out[added, added + n] = (
            transmission ** (n / 2.0)
            * math.sqrt(math.comb(n + added, added))
            * (gain - 1.0) ** added
            / gain ** (n / 2.0 + added + 1.0)
        )
    return out


def rare_excitation_check(eta, nu, n, epsilon, cutoff=100):
    p0 = fock_output_probabilities(eta, nu, 0, cutoff)
    pn = fock_output_probabilities(eta, nu, n, cutoff)
    z = vacuum_fock_offdiagonal(eta, nu, n, cutoff)
    # The physical cutoff-erasure channel preserves the entire tail in a flag.
    tail0 = max(0.0, 1.0 - float(p0.sum()))
    tailn = max(0.0, 1.0 - float(pn.sum()))
    dimension = cutoff + 2
    reference_output = np.zeros((2 * dimension, 2 * dimension))
    reference_output[: cutoff + 1, : cutoff + 1] = np.diag((1.0 - epsilon) * p0)
    reference_output[dimension : dimension + cutoff + 1,
                     dimension : dimension + cutoff + 1] = np.diag(epsilon * pn)
    reference_output[: cutoff + 1, dimension : dimension + cutoff + 1] = (
        math.sqrt(epsilon * (1.0 - epsilon)) * z
    )
    reference_output[dimension : dimension + cutoff + 1, : cutoff + 1] = (
        math.sqrt(epsilon * (1.0 - epsilon)) * z.T
    )
    reference_output[dimension - 1, dimension - 1] = (1.0 - epsilon) * tail0
    reference_output[-1, -1] = epsilon * tailn
    receiver_probabilities = np.append(
        (1.0 - epsilon) * p0 + epsilon * pn,
        (1.0 - epsilon) * tail0 + epsilon * tailn,
    )
    eigenvalues = np.linalg.eigvalsh(reference_output)
    ic = entropy_from_eigenvalues(receiver_probabilities) - entropy_from_eigenvalues(eigenvalues)
    gain = 1.0 + (1.0 - eta) * nu
    transmission = eta / gain
    kappa = 1.0 - transmission**n
    s = gain - 1.0
    # Relative entropy to the exact untruncated vacuum thermal output.
    # The omitted geometric tail is far below double precision in these cases.
    relative_entropy = (
        bosonic_entropy(s)
        + eta * n * math.log2((s + 1.0) / s)
        - entropy_from_eigenvalues(pn)
    )
    bound = (
        epsilon * relative_entropy
        - h2(epsilon * kappa)
        + epsilon * h2(kappa)
    )
    conservative_d = bosonic_entropy(s) + eta * n * math.log2((s + 1.0) / s)
    sufficient_epsilon = 2.0 ** (-(conservative_d + h2(kappa)) / kappa)
    return {
        "eta": eta,
        "nu": nu,
        "fock_level": n,
        "epsilon": epsilon,
        "kappa": kappa,
        "cutoff_erasure_Ic": ic,
        "exact_formula_upper_bound_evaluated_numerically": bound,
        "conservative_epsilon_threshold": sufficient_epsilon,
        "retained_probability_defect": max(tail0, tailn),
        "minimum_RB_eigenvalue": float(eigenvalues[0]),
        "offdiagonal_trace_norm": float(np.linalg.svd(z, compute_uv=False).sum()),
        "offdiagonal_trace_norm_upper_bound": transmission ** (n / 2.0),
    }


def thermal_ic(eta, nu, mean):
    """Compute S(B)-S(RB) from the two-mode Gaussian symplectic spectrum."""
    a = mean + 0.5
    b = eta * mean + (1.0 - eta) * nu + 0.5
    c_squared = eta * mean * (mean + 1.0)
    discriminant = math.sqrt((a + b) ** 2 - 4.0 * c_squared)
    v1 = 0.5 * (discriminant + a - b)
    v2 = 0.5 * (discriminant - a + b)
    return bosonic_entropy(b - 0.5) - bosonic_entropy(v1 - 0.5) - bosonic_entropy(v2 - 0.5)


def covariance_extension_check(eta, nu, mean):
    """Finite-energy test in doubled convention V_vac=I, Eq.(5) LKA+19."""
    a = 2.0 * mean + 1.0
    y = (1.0 - eta) * (2.0 * nu + 1.0)
    b = eta * a + y
    c = 2.0 * math.sqrt(eta * mean * (mean + 1.0))
    identity = np.eye(2)
    omega = np.array([[0.0, 1.0], [-1.0, 0.0]])
    correlation = c * np.diag([1.0, -1.0])
    covariance = np.block([[a * identity, correlation], [correlation, b * identity]])
    extension_matrix = covariance.astype(complex)
    extension_matrix[:2, :2] -= 1j * omega
    schur = b * identity - correlation @ np.linalg.inv(a * identity - 1j * omega) @ correlation
    return {
        "eta": eta,
        "nu": nu,
        "input_mean_photons": mean,
        "2_extendibility_test_minimum_eigenvalue": float(np.linalg.eigvalsh(extension_matrix)[0]),
        "Schur_minimum_eigenvalue": float(np.linalg.eigvalsh(schur)[0]),
        "Schur_exact_minimum": y - eta,
        "thermal_coherent_information": thermal_ic(eta, nu, mean),
    }


def main():
    records = {"status": "floating_point_diagnostics_only_not_capacity_certification"}
    records["route_constants"] = []
    records["finite_resource_bounds"] = []
    for eta in (0.75001, 0.7501, 0.751, 0.76, 0.7841, 0.8):
        delta = eta - 0.75
        theta_difference = abs(math.acos(math.sqrt(eta)) - math.pi / 6.0)
        gap = 0.99 - 0.75
        mean_per_use = 10.0
        records["route_constants"].append({
            "eta": eta,
            "nu": 1,
            "postamplification_displacement_variance": 2.0 * (1.0 - eta) / eta,
            "preamplification_displacement_variance": 2.0 * (1.0 - eta),
            "receiver_gain_antidegradability_threshold": 1.0 / (1.0 - 4.0 * delta),
            "receiver_attenuation_antidegradability_threshold": 1.0 / (1.0 + 4.0 * delta),
            "twisted_decomposition_capacity_upper_bound": math.log2((2.0 * eta - 1.0) / (2.0 - 2.0 * eta)),
        })
        records["finite_resource_bounds"].append({
            "eta": eta,
            "theta_difference": theta_difference,
            "target_entanglement_fidelity": 0.99,
            "mean_photons_per_use": mean_per_use,
            "necessary_minimum_blocklength": math.ceil(gap**2 / (theta_difference**2 * (3.0 * mean_per_use + 1.0))),
        })
    records["rare_excitation_checks"] = [
        rare_excitation_check(eta, 1.0, n, epsilon)
        for eta in (0.751, 0.7841, 0.8)
        for n in (1, 4, 10)
        for epsilon in (1e-2, 1e-4, 1e-6)
    ]
    records["finite_energy_nonextendibility"] = [
        covariance_extension_check(eta, 1.0, mean)
        for eta in (0.74, 0.75, 0.751, 0.76)
        for mean in (0.001, 1.0, 100.0)
    ]
    eta, nu, mean = 0.7, 1.0, 100.0
    records["missing_environment_purifier_counterexample"] = {
        "eta": eta, "nu": nu, "thermal_input_mean": mean,
        "weak_complement_difference": bosonic_entropy(eta * mean + (1.0 - eta) * nu)
            - bosonic_entropy((1.0 - eta) * mean + eta * nu),
        "true_coherent_information": thermal_ic(eta, nu, mean),
        "channel_antidegradable": True,
    }
    records["postselection_counterexample"] = {
        "perfect_success_probability": 0.49,
        "conditional_success_Ic_qubits": 1.0,
        "full_flagged_channel_Ic_at_maximally_mixed_qubit": -0.02,
        "unassisted_quantum_capacity": 0.0,
    }
    for row in records["rare_excitation_checks"]:
        assert row["cutoff_erasure_Ic"] <= row["exact_formula_upper_bound_evaluated_numerically"] + 2e-12
        assert row["offdiagonal_trace_norm"] <= row["offdiagonal_trace_norm_upper_bound"] + 2e-12
        assert row["minimum_RB_eigenvalue"] >= -2e-12
    for row in records["finite_energy_nonextendibility"]:
        assert abs(row["Schur_minimum_eigenvalue"] - row["Schur_exact_minimum"]) < 2e-10
    out = Path(__file__).with_name("obstruction_checks.json")
    out.write_text(json.dumps(records, indent=2) + "\n")
    print(json.dumps({
        "diagnostics_saved": str(out.resolve()),
        "rare_excitation_cases": len(records["rare_excitation_checks"]),
        "all_checked_Ic_negative": all(row["cutoff_erasure_Ic"] < 0 for row in records["rare_excitation_checks"]),
        "extension_cases": len(records["finite_energy_nonextendibility"]),
        "finite_resource_bounds": records["finite_resource_bounds"],
        "missing_environment_purifier_counterexample": records["missing_environment_purifier_counterexample"],
    }, indent=2))


if __name__ == "__main__":
    main()
