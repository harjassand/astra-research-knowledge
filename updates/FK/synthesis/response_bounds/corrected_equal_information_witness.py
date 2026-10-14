#!/usr/bin/env python3
"""Append-only precision-aligned rerun of the frozen equal-information witness.

The original frozen file remains unchanged.  Here, the intended decimal
frequencies and rational Euclidean times are constructed after the requested
mpmath precision is set.  A separate interval implementation rebuilds those
same input strings/rationals and encloses the determinant, Cramer vector,
weights, and target gap.  The old module-import-at-15-dps construction is also
recreated solely to quantify the correction.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import mpmath as mp
import numpy as np


HERE = Path(__file__).resolve().parent
BETA_TEXT = "1"
ETA_TEXT = "1"
TAU_NUMERATORS = [0, 1, 2, 3, 4, 5]
TAU_DENOMINATOR = 12
OMEGA_TEXTS = ["0.07", "0.16", "1.9", "5.3", "9", "15", "21.5", "28.5", "40"]
DELTA_TEXT = "0.000001"
RNG_SEED = 20261014


def intended_mp_inputs() -> tuple[mp.mpf, mp.mpf, list[mp.mpf], list[mp.mpf]]:
    """Create intended rational/decimal inputs in the caller's high-dps context."""
    beta = mp.mpf(BETA_TEXT)
    eta = mp.mpf(ETA_TEXT)
    taus = [mp.mpf(k) / TAU_DENOMINATOR for k in TAU_NUMERATORS]
    omegas = [mp.mpf(x) for x in OMEGA_TEXTS]
    return beta, eta, taus, omegas


def frozen_rounded_mp_inputs() -> tuple[mp.mpf, mp.mpf, list[mp.mpf], list[mp.mpf]]:
    """Recreate the frozen script's module-level construction at 15 dps."""
    with mp.workdps(15):
        beta = mp.mpf(1)
        eta = mp.mpf(1)
        taus = [mp.mpf(0)] + [mp.mpf(k) / 12 for k in range(1, 6)]
        omegas = list(map(mp.mpf, OMEGA_TEXTS))
    # mpf values retain the 15-dps binary mantissas after the context exits.
    return beta, eta, taus, omegas


def kernels(beta: mp.mpf, taus: list[mp.mpf], omegas: list[mp.mpf]) -> mp.matrix:
    def euclidean(tau: mp.mpf, omega: mp.mpf) -> mp.mpf:
        return (mp.exp(-tau * omega) + mp.exp(-(beta - tau) * omega)) / (
            1 - mp.exp(-beta * omega)
        )

    def static(omega: mp.mpf) -> mp.mpf:
        return 2 / omega

    return mp.matrix(
        [[euclidean(tau, omega) for omega in omegas] for tau in taus]
        + [[2 * omega for omega in omegas], [static(omega) for omega in omegas]]
    )


def pair_from_matrix(
    beta: mp.mpf,
    eta: mp.mpf,
    taus: list[mp.mpf],
    omegas: list[mp.mpf],
    a: mp.matrix,
) -> dict:
    v = list(mp.lu_solve(a[:, 0:8], -a[:, 8])) + [mp.mpf(1)]
    base = [1 / (2 * len(omegas) * omega) for omega in omegas]
    delta = mp.mpf(DELTA_TEXT)
    plus = [b + delta * q for b, q in zip(base, v)]
    minus = [b - delta * q for b, q in zip(base, v)]
    if min(plus + minus) <= 0:
        raise ArithmeticError("witness weights lost positivity")

    def integrate(weights: list[mp.mpf], fn) -> mp.mpf:
        return mp.fsum(w * fn(x) for w, x in zip(weights, omegas))

    # Use the supplied beta explicitly, so comparison instances are evaluated
    # under their own inputs rather than silently sharing beta=1.
    euclidean_means = [
        integrate(
            plus,
            lambda omega, tau=tau: (
                mp.exp(-tau * omega) + mp.exp(-(beta - tau) * omega)
            )
            / (1 - mp.exp(-beta * omega)),
        )
        for tau in taus
    ]
    static_plus = integrate(plus, lambda omega: 2 / omega)
    static_minus = integrate(minus, lambda omega: 2 / omega)
    chi_plus = integrate(plus, lambda omega: 2 * omega / (omega * omega + eta * eta))
    chi_minus = integrate(minus, lambda omega: 2 * omega / (omega * omega + eta * eta))
    m1_plus = integrate(plus, lambda omega: 2 * omega)
    m1_minus = integrate(minus, lambda omega: 2 * omega)
    numeric_null_residuals = [
        mp.fsum(a[row, col] * v[col] for col in range(len(omegas)))
        for row in range(a.rows)
    ]
    euclidean_minus = [
        integrate(
            minus,
            lambda omega, tau=tau: (
                mp.exp(-tau * omega) + mp.exp(-(beta - tau) * omega)
            )
            / (1 - mp.exp(-beta * omega)),
        )
        for tau in taus
    ]
    return {
        "matrix": a,
        "v": v,
        "base": base,
        "delta": delta,
        "plus": plus,
        "minus": minus,
        "euclidean_means": euclidean_means,
        "euclidean_minus": euclidean_minus,
        "numeric_null_residuals": numeric_null_residuals,
        "static_plus": static_plus,
        "static_minus": static_minus,
        "chi_plus": chi_plus,
        "chi_minus": chi_minus,
        "m1_plus": m1_plus,
        "m1_minus": m1_minus,
        "gap": abs(chi_plus - chi_minus),
    }


def interval_instance() -> dict:
    """Independent interval construction from the exact decimal/rational text."""
    iv = mp.iv
    iv.dps = 80
    beta = iv.mpf(BETA_TEXT)
    eta = iv.mpf(ETA_TEXT)
    taus = [iv.mpf(k) / TAU_DENOMINATOR for k in TAU_NUMERATORS]
    omegas = [iv.mpf(x) for x in OMEGA_TEXTS]

    def k(tau, omega):
        return (iv.exp(-tau * omega) + iv.exp(-(beta - tau) * omega)) / (
            1 - iv.exp(-beta * omega)
        )

    a = iv.matrix(
        [[k(tau, omega) for omega in omegas] for tau in taus]
        + [[2 * omega for omega in omegas], [2 / omega for omega in omegas]]
    )
    square = a[:, 0:8]
    det = iv.det(square)
    if not float(det.b) < 0:
        raise ArithmeticError("intended-instance determinant interval failed to exclude zero")

    v = []
    for col in range(8):
        repl = iv.matrix(square)
        for row in range(8):
            repl[row, col] = a[row, 8]
        v.append(-iv.det(repl) / det)
    v.append(iv.mpf(1))

    delta = iv.mpf(DELTA_TEXT)
    base = [1 / (18 * omega) for omega in omegas]
    wplus, wminus = [], []
    for b, x in zip(base, v):
        wp, wm = b + delta * x, b - delta * x
        if min(float(wp.a), float(wm.a)) <= 0:
            raise ArithmeticError("intended-instance interval positivity failed")
        wplus.append(wp)
        wminus.append(wm)

    g = [2 * omega / (omega * omega + eta * eta) for omega in omegas]
    target_plus = sum((w * x for w, x in zip(wplus, g)), iv.mpf(0))
    target_minus = sum((w * x for w, x in zip(wminus, g)), iv.mpf(0))
    gap = target_plus - target_minus
    if not (float(gap.a) > 0 or float(gap.b) < 0):
        raise ArithmeticError("intended-instance response-gap interval contains zero")
    euclidean = [
        sum((w * k(tau, omega) for w, omega in zip(wplus, omegas)), iv.mpf(0))
        for tau in taus
    ]
    m1 = sum((w * 2 * omega for w, omega in zip(wplus, omegas)), iv.mpf(0))
    static = sum((w * 2 / omega for w, omega in zip(wplus, omegas)), iv.mpf(0))
    return {
        "determinant": det,
        "v": v,
        "weights_plus": wplus,
        "weights_minus": wminus,
        "target_plus": target_plus,
        "target_minus": target_minus,
        "gap": gap,
        "euclidean": euclidean,
        "m1": m1,
        "static": static,
    }


def iv_contains_mp(interval, value: mp.mpf) -> bool:
    iv_value = mp.iv.mpf(mp.nstr(value, 110))
    difference = iv_value - interval
    return float(difference.a) <= 0 <= float(difference.b)


def thermal_realization(pair: dict, beta: mp.mpf, omegas: list[mp.mpf]) -> dict:
    z = 1 + mp.fsum(mp.exp(-beta * omega) for omega in omegas)
    probabilities = [1 / z] + [mp.exp(-beta * omega) / z for omega in omegas]

    def observable_norm(weights: list[mp.mpf]) -> mp.mpf:
        # H is diagonal; A is the star matrix with only A_0i entries.
        row_norm_sq = mp.fsum(
            weight * z / (1 - mp.exp(-beta * omega))
            for weight, omega in zip(weights, omegas)
        )
        return mp.sqrt(row_norm_sq)

    # Shannon entropy is descriptive; it is not a preparation-cost guarantee.
    entropy_bits = -mp.fsum(p * mp.log(p, 2) for p in probabilities)
    return {
        "dimension": len(omegas) + 1,
        "partition_function": z,
        "thermal_probabilities": probabilities,
        "hamiltonian_operator_norm": max(omegas),
        "observable_operator_norm_plus": observable_norm(pair["plus"]),
        "observable_operator_norm_minus": observable_norm(pair["minus"]),
        "thermal_shannon_entropy_bits": entropy_bits,
        "preparation_model": {
            "classical_mixture": "sample one of 10 diagonal energy-basis states using the Gibbs probabilities, then prepare that basis label; finite-precision sampling uses O(log(1/eps)+log d) random bits and O(d) probability setup",
            "coherent_purification": "one possible O(d)-rotation state-preparation circuit with O(log(1/eps)) angle precision; actual gate synthesis and device thermalization costs are not supplied",
            "algorithm_access": "neither these probabilities nor this preparation oracle is granted to a Euclidean-data estimator",
        },
    }


def main() -> None:
    mp.mp.dps = 110
    beta_exact, eta_exact, taus_exact, omegas_exact = intended_mp_inputs()
    exact_matrix = kernels(beta_exact, taus_exact, omegas_exact)
    exact_pair = pair_from_matrix(beta_exact, eta_exact, taus_exact, omegas_exact, exact_matrix)

    beta_old, eta_old, taus_old, omegas_old = frozen_rounded_mp_inputs()
    old_matrix = kernels(beta_old, taus_old, omegas_old)
    rounded_pair = pair_from_matrix(beta_old, eta_old, taus_old, omegas_old, old_matrix)

    iv_pair = interval_instance()
    containment = {
        "determinant": iv_contains_mp(iv_pair["determinant"], mp.det(exact_matrix[:, 0:8])),
        "null_vector": [iv_contains_mp(box, x) for box, x in zip(iv_pair["v"], exact_pair["v"])],
        "weights_plus": [iv_contains_mp(box, x) for box, x in zip(iv_pair["weights_plus"], exact_pair["plus"])],
        "weights_minus": [iv_contains_mp(box, x) for box, x in zip(iv_pair["weights_minus"], exact_pair["minus"])],
        "target_plus": iv_contains_mp(iv_pair["target_plus"], exact_pair["chi_plus"]),
        "target_minus": iv_contains_mp(iv_pair["target_minus"], exact_pair["chi_minus"]),
        "gap": iv_contains_mp(iv_pair["gap"], exact_pair["chi_plus"] - exact_pair["chi_minus"]),
        "euclidean_means": [iv_contains_mp(box, x) for box, x in zip(iv_pair["euclidean"], exact_pair["euclidean_means"])],
        "M1": iv_contains_mp(iv_pair["m1"], exact_pair["m1_plus"]),
        "static_response": iv_contains_mp(iv_pair["static"], exact_pair["static_plus"]),
    }
    if not all(containment["null_vector"] + containment["weights_plus"] + containment["weights_minus"]):
        raise ArithmeticError("independent interval instance failed to enclose corrected witness")
    if not all(containment[k] for k in ["determinant", "target_plus", "target_minus", "gap", "M1", "static_response"]):
        raise ArithmeticError("independent interval instance failed to enclose a corrected scalar")
    if not all(containment["euclidean_means"]):
        raise ArithmeticError("independent interval instance failed to enclose Euclidean means")

    realization = thermal_realization(exact_pair, beta_exact, omegas_exact)
    input_differences = {
        "max_abs_tau_old_rounded_minus_exact": max(abs(x - y) for x, y in zip(taus_old, taus_exact)),
        "max_abs_omega_old_rounded_minus_exact": max(abs(x - y) for x, y in zip(omegas_old, omegas_exact)),
        "max_abs_chi_plus_old_minus_corrected": abs(rounded_pair["chi_plus"] - exact_pair["chi_plus"]),
        "max_abs_chi_minus_old_minus_corrected": abs(rounded_pair["chi_minus"] - exact_pair["chi_minus"]),
        "abs_target_gap_old_minus_corrected": abs(rounded_pair["gap"] - exact_pair["gap"]),
        "max_abs_mean_old_minus_corrected": max(abs(x - y) for x, y in zip(rounded_pair["euclidean_means"], exact_pair["euclidean_means"])),
    }

    # Deterministic simulated Gaussian readout from corrected exact means.
    rng = np.random.default_rng(RNG_SEED)
    sigma_c = 0.02
    observed_c = [float(x) for x in exact_pair["euclidean_means"]]
    observed_c = [x + float(rng.normal(0.0, sigma_c)) for x in observed_c]

    result = {
        "schema": "fk-response-bounds-correction-results/1",
        "delta_scope": "precision alignment and realization-cost correction only; original REPORT.md, RESULTS.json, and MANIFEST.json are unchanged",
        "precision": {
            "corrected_mp_dps": 110,
            "input_construction": "decimal strings and tau numerators/12 are converted only after mp.mp.dps=110",
            "interval_construction": "independent mpmath.iv instance at 80 dps from the same decimal strings and rational tau definitions",
            "old_reconstruction": "frozen module-level input construction repeated at mp.workdps(15), then arithmetic performed at 110 dps",
            "corrected_mp_instance_enclosed_by_independent_interval_instance": containment,
            "containment_all_pass": all(containment["null_vector"] + containment["weights_plus"] + containment["weights_minus"] + containment["euclidean_means"])
                and all(containment[k] for k in ["determinant", "target_plus", "target_minus", "gap", "M1", "static_response"]),
            "differences_old_rounded_vs_corrected_exact": {k: mp.nstr(v, 20) for k, v in input_differences.items()},
            "status": "precision mismatch confirmed in frozen v1; intended exact-decimal/rational witness independently interval-enclosed; existence and separated-target conclusion preserved",
        },
        "corrected_equal_information_pair": {
            "exact_definition": "A is the exact real 8x9 matrix generated by beta=1, tau=k/12 (k=0,...,5), exact decimal omega strings, and rows K_beta(tau,omega), 2 omega, 2/omega. Define v_9=1 and v_1:8=-A_1:8^{-1}A_9 by Cramer's rule over the exact inputs; define b_i=1/(18 omega_i) and w_i^plus/minus=b_i +/- 10^-6 v_i. The interval receipts certify det(A_1:8) excludes zero and every weight is positive. Thus A v=0 and equal-observation constraints hold exactly; mp values below are approximations enclosed by independent intervals.",
            "beta": mp.nstr(beta_exact, 20),
            "eta": mp.nstr(eta_exact, 20),
            "tau": [mp.nstr(x, 20) for x in taus_exact],
            "omega": [mp.nstr(x, 20) for x in omegas_exact],
            "delta": mp.nstr(exact_pair["delta"], 20),
            "null_vector": [mp.nstr(x, 20) for x in exact_pair["v"]],
            "weights_plus": [mp.nstr(x, 20) for x in exact_pair["plus"]],
            "weights_minus": [mp.nstr(x, 20) for x in exact_pair["minus"]],
            "euclidean_means_common": [mp.nstr(x, 20) for x in exact_pair["euclidean_means"]],
            "max_numeric_null_residual": mp.nstr(max(abs(x) for x in exact_pair["numeric_null_residuals"]), 8),
            "max_numeric_plus_minus_Euclidean_difference": mp.nstr(max(abs(x-y) for x,y in zip(exact_pair["euclidean_means"], exact_pair["euclidean_minus"])), 8),
            "numeric_plus_minus_M1_difference": mp.nstr(abs(exact_pair["m1_plus"] - exact_pair["m1_minus"]), 8),
            "numeric_plus_minus_static_difference": mp.nstr(abs(exact_pair["static_plus"] - exact_pair["static_minus"]), 8),
            "M1_plus": mp.nstr(exact_pair["m1_plus"], 20),
            "M1_minus": mp.nstr(exact_pair["m1_minus"], 20),
            "static_plus": mp.nstr(exact_pair["static_plus"], 20),
            "static_minus": mp.nstr(exact_pair["static_minus"], 20),
            "chi_eta_plus": mp.nstr(exact_pair["chi_plus"], 20),
            "chi_eta_minus": mp.nstr(exact_pair["chi_minus"], 20),
            "target_gap": mp.nstr(exact_pair["gap"], 20),
            "interval_receipts": {
                "determinant": str(iv_pair["determinant"]),
                "target_plus": str(iv_pair["target_plus"]),
                "target_minus": str(iv_pair["target_minus"]),
                "gap": str(iv_pair["gap"]),
            },
        },
        "realization_scope_and_cost": {
            "construction": "H=diag(0,omega_1,...,omega_9); A has only A_0i=A_i0=sqrt(w_i*Z/(1-exp(-beta*omega_i))) entries",
            "dimension": realization["dimension"],
            "partition_function": mp.nstr(realization["partition_function"], 20),
            "thermal_probabilities": [mp.nstr(x, 20) for x in realization["thermal_probabilities"]],
            "hamiltonian_operator_norm": mp.nstr(realization["hamiltonian_operator_norm"], 20),
            "observable_operator_norm_plus": mp.nstr(realization["observable_operator_norm_plus"], 20),
            "observable_operator_norm_minus": mp.nstr(realization["observable_operator_norm_minus"], 20),
            "thermal_shannon_entropy_bits": mp.nstr(realization["thermal_shannon_entropy_bits"], 20),
            "preparation_model": realization["preparation_model"],
            "bounded_unit_observable_claim": False,
            "interpretation": "the finite-dimensional witness is valid for the unbounded-A access class used in the proof; it does not establish the same numerical gap under an externally imposed ||A||<=1 promise",
        },
        "simulated_noisy_euclidean_vector": {
            "seed": RNG_SEED,
            "sigma_per_reading": sigma_c,
            "observed_values": observed_c,
            "same_law_under_corrected_pair": True,
            "physical_or_mcmc_data": False,
        },
    }
    (HERE / "CORRECTION_01_RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    (HERE / "CORRECTION_01_noisy_euclidean.csv").write_text(
        "tau,observed_C,simulated_sigma\n"
        + "".join(
            f"{float(tau):.12g},{value:.17g},{sigma_c:.17g}\n"
            for tau, value in zip(taus_exact, observed_c)
        )
    )
    print(json.dumps({
        "old_vs_corrected": result["precision"]["differences_old_rounded_vs_corrected_exact"],
        "chi_plus": result["corrected_equal_information_pair"]["chi_eta_plus"],
        "chi_minus": result["corrected_equal_information_pair"]["chi_eta_minus"],
        "gap": result["corrected_equal_information_pair"]["target_gap"],
        "interval_all_pass": result["precision"]["containment_all_pass"],
        "A_norm_plus": result["realization_scope_and_cost"]["observable_operator_norm_plus"],
        "A_norm_minus": result["realization_scope_and_cost"]["observable_operator_norm_minus"],
    }, indent=2))


if __name__ == "__main__":
    main()
