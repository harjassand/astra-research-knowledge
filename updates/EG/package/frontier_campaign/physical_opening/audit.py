#!/usr/bin/env python3
"""Exact formulas and independent Fock-sum checks for a rejected bath route.

This is a deterministic mathematical audit, not an experimental demonstration.
Run: python3 research/2026-10-12-frontier/physical_opening/audit.py
"""

import json
import math
from pathlib import Path

H = 6.62607015e-34
KB = 1.380649e-23


def occupation(frequency_hz, temperature_k):
    return 1.0 / math.expm1(H * frequency_hz / (KB * temperature_k))


def entropy_nats(n):
    if n == 0:
        return 0.0
    # Avoid catastrophic subtraction of n log(n) at large n.
    return math.log1p(n) + n * math.log1p(1.0 / n)


def correlation_cost_nats(n, chi):
    return 2 * entropy_nats(n) - entropy_nats(n * (1 + chi)) - entropy_nats(n * (1 - chi))


def dark_occupation(n, chi, transmission=1.0, warm_environment=0.0, phase_error=0.0):
    """Equal arms; independent identical loss baths; no anomalous moments."""
    return transmission * n * (1 - chi * math.cos(phase_error)) + (1 - transmission) * warm_environment


def single_rail_entanglement_fidelity(eta, environment_n):
    """Overlap with (|0_R0_B>+|1_R1_B>)/sqrt(2), no postselection.

    Channel is a passive thermal attenuator of transmissivity eta.
    Decomposition into quantum-limited loss eta/G then amplification G gives
    the closed form. Leakage outside the |0>,|1> output code is charged.
    """
    mu = (1 - eta) * environment_n
    gain = 1 + mu
    p0_given0 = 1 / gain
    p1_given1 = (eta + mu * (gain - eta)) / gain**3
    coherence = math.sqrt(eta) / gain**2
    return (p0_given0 + p1_given1 + 2 * coherence) / 4


def independent_fock_sum_fidelity(eta, environment_n, tail=1e-13):
    """Direct beam-splitter amplitudes with a thermal number-state bath.

    For bath photon number l, the relevant output amplitudes are eta^(l/2)
    and eta^((l-1)/2) * [eta-l*(1-eta)]. The thermal tail bounds omitted
    density-matrix weight; no amplifier decomposition is used here.
    """
    p = 1 / (1 + environment_n)
    ratio = environment_n / (1 + environment_n)
    p0 = p1 = coherence = 0.0
    l = 0
    while True:
        amp0 = eta ** (l / 2)
        amp1 = eta ** ((l - 1) / 2) * (eta - l * (1 - eta))
        p0 += p * amp0 * amp0
        p1 += p * amp1 * amp1
        coherence += p * amp0 * amp1
        l += 1
        remaining_weight = ratio**l if ratio else 0.0
        if remaining_weight < tail:
            break
        p *= ratio
    return (p0 + p1 + 2 * coherence) / 4, l, remaining_weight


def rotation_covariance(n, angle):
    """U(n I)U^T for a passive real beam splitter."""
    c, s = math.cos(angle), math.sin(angle)
    return [[n * (c * c + s * s), n * (c * (-s) + s * c)],
            [n * ((-s) * c + c * s), n * (s * s + c * c)]]


def correlated_splitter_inputs(n, chi):
    """The two input occupations needed for a 50:50 splitter preparation."""
    plus, minus = n * (1 + chi), n * (1 - chi)
    local = (plus + minus) / 2
    cross = (plus - minus) / 2
    return {"input_hot": plus, "input_cold": minus, "output_local": local,
            "output_normal_cross_moment": cross}


def main():
    checks = []
    for eta in [0.2, 0.5, 0.8, 0.99]:
        for n in [0.0, 0.1, 1.0, 10.0]:
            analytic = single_rail_entanglement_fidelity(eta, n)
            direct, terms, tail = independent_fock_sum_fidelity(eta, n)
            assert abs(analytic - direct) < 1e-12
            checks.append({"eta": eta, "environment_n": n,
                           "analytic_F_e": analytic, "direct_Fock_F_e": direct,
                           "Fock_terms": terms, "omitted_thermal_weight": tail})

    passive_checks = []
    for n in [0.1, 1.0, 100.0, 1e7]:
        for angle in [0.0, 0.1, math.pi / 4, math.pi / 2]:
            covariance = rotation_covariance(n, angle)
            assert abs(covariance[0][0] - n) <= 1e-14 * max(n, 1)
            assert abs(covariance[1][1] - n) <= 1e-14 * max(n, 1)
            assert covariance[0][1] == covariance[1][0] == 0
            passive_checks.append({"n": n, "angle": angle, "covariance": covariance})

    engineering = []
    for frequency, temperature in [(1e6, 300.0), (10e9, 300.0), (10e9, 4.0), (1.473e6, 0.1)]:
        n = occupation(frequency, temperature)
        entropy_cost = correlation_cost_nats(n, 1.0)
        engineering.append({
            "frequency_hz": frequency, "temperature_k": temperature, "thermal_n": n,
            "maximum_1_minus_chi_for_dark_n_below_one": min(1.0, 1.0 / n),
            "maximum_independent_warm_loss_fraction_for_dark_n_below_one": min(1.0, 1.0 / n),
            "maximum_phase_error_radians_for_dark_n_below_one_at_chi_one":
                math.acos(max(-1.0, 1.0 - 1.0 / n)) if n >= 0.5 else math.pi,
            "perfect_correlation_information_nats_per_pair": entropy_cost,
            "same_temperature_cyclic_work_lower_bound_joules_per_pair": KB * temperature * entropy_cost,
            "one_mode_cooling_entropy_nats": entropy_nats(n),
            "correlation_entropy_cost_over_one_mode_cooling_entropy": entropy_cost / entropy_nats(n),
            "one_mode_vacuum_cooling_work_lower_bound_joules": KB * temperature * math.log1p(n),
            "correlation_work_over_one_mode_vacuum_cooling_work": entropy_cost / math.log1p(n),
        })

    n, chi, eta = 100.0, 0.999, 0.8
    ideal_n = dark_occupation(n, chi)
    warm_loss_n = dark_occupation(n, chi, transmission=0.99, warm_environment=n)
    ideal = correlated_splitter_inputs(n, chi)
    assert math.isclose(ideal["output_local"], n)
    assert math.isclose(ideal["output_normal_cross_moment"], n * chi)
    assert math.isclose(ideal_n, ideal["input_cold"], abs_tol=1e-13)

    # A bare shared bath cannot be substituted for a prepared correlated state.
    # With diagonal damping A=-gamma I/2 and noise commutator Gamma=[[g,r g],[r g,g]],
    # canonical commutators C obey dC/dt=A C+C A^T+Gamma. Starting C=I,
    # the forbidden off-diagonal commutator is r(1-exp(-g t)).
    shared_bath_inconsistency = {"gamma": 1.0, "bath_commutator_correlation": 0.9,
                                "time": 1.0,
                                "spurious_system_cross_commutator": 0.9 * (1 - math.exp(-1))}

    result = {
        "status": "MATHEMATICAL_AUDIT_ONLY_NO_NEW_DEVICE_ADVANTAGE",
        "scope": "Gauge-invariant two-mode Gaussian bath; equal local occupation; passive phase-preserving signal channel",
        "fidelity_formula_independent_checks": checks,
        "equal_temperature_passive_mixing_checks": passive_checks,
        "engineering_thresholds": engineering,
        "worked_example": {"eta": eta, "source_local_n": n, "source_chi": chi,
                           "source_preparation": ideal, "ideal_dark_n": ideal_n,
                           "independent_bath_F_e": single_rail_entanglement_fidelity(eta, n),
                           "ideal_correlated_bath_F_e": single_rail_entanglement_fidelity(eta, ideal_n),
                           "one_percent_independent_warm_loss_dark_n": warm_loss_n,
                           "one_percent_independent_warm_loss_F_e": single_rail_entanglement_fidelity(eta, warm_loss_n)},
        "bare_shared_bath_with_unchanged_diagonal_damping_counterexample": shared_bath_inconsistency,
        "markov_causality_counterexample": {
            "past_output_cross_moment": "Can be nonzero after a preparation interaction",
            "future_fresh_input_cross_moment": 0,
            "assumption": "Independent Markov bath time bins; no routing, memory, or feedback boundary condition",
            "consequence": "Past output covariance does not supply a future correlated input covariance"
        },
    }
    output = Path(__file__).with_name("results.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"checks_passed": len(checks) + len(passive_checks),
                      "worked_example": result["worked_example"],
                      "engineering_thresholds": engineering,
                      "result_path": str(output)}, indent=2))


if __name__ == "__main__":
    main()
