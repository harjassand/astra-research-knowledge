#!/usr/bin/env python3
"""Finite-state pulse-order witness for a reversible cotranscriptional switch.

The model has three conformations 0 <-> 1 <-> 2.  Input A raises the
conductance of edge 0--1 from epsilon to k; input B raises edge 1--2 from
epsilon to k.  Each fixed-input generator is symmetric, so both have exactly
the same uniform equilibrium distribution.  The observable is occupancy of
state 2 after equal-duration A/B pulses.

Only Python's standard library is required.  Matrix exponentials are applied
to row vectors by CTMC uniformization; the returned Poisson-tail bound is
reported as a numerical diagnostic, not as a biological error bound.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Sequence

Vector = list[float]
Matrix = list[list[float]]


def zeros(n: int) -> Matrix:
    return [[0.0 for _ in range(n)] for _ in range(n)]


def eye(n: int) -> Matrix:
    out = zeros(n)
    for i in range(n):
        out[i][i] = 1.0
    return out


def matmul(a: Matrix, b: Matrix) -> Matrix:
    n, m, p = len(a), len(b), len(b[0])
    return [[sum(a[i][k] * b[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def rowmul(row: Vector, a: Matrix) -> Vector:
    return [sum(row[i] * a[i][j] for i in range(len(row))) for j in range(len(a[0]))]


def add_scaled(dst: Vector, src: Vector, scale: float) -> None:
    for i in range(len(dst)):
        dst[i] += scale * src[i]


def generator(k: float, eps: float, strong_edge: int) -> Matrix:
    """Return a symmetric row generator; strong_edge is 0 (A) or 1 (B)."""
    rates = [eps, eps]
    rates[strong_edge] = k
    q = zeros(3)
    for i, rate in enumerate(rates):
        q[i][i + 1] = rate
        q[i + 1][i] = rate
        q[i][i] -= rate
        q[i + 1][i + 1] -= rate
    return q


def exp_action(row: Vector, q: Matrix, t: float) -> tuple[Vector, float]:
    """Apply exp(tQ) to a row vector by uniformization; return omitted tail."""
    if t < 0:
        raise ValueError("duration must be nonnegative")
    rate = max(-q[i][i] for i in range(len(q)))
    if t == 0 or rate == 0:
        return row[:], 0.0
    x = rate * t
    p = eye(len(q))
    for i in range(len(q)):
        for j in range(len(q)):
            p[i][j] += q[i][j] / rate
    nmax = int(x + 16.0 * math.sqrt(x + 1.0) + 100.0)
    weight = math.exp(-x)
    power_row = row[:]
    result = [0.0] * len(row)
    weight_sum = 0.0
    for n in range(nmax + 1):
        add_scaled(result, power_row, weight)
        weight_sum += weight
        power_row = rowmul(power_row, p)
        weight *= x / (n + 1.0)
    return result, max(0.0, 1.0 - weight_sum)


def pulse_order(k: float, eps: float, tau_a: float, tau_b: float) -> dict[str, float]:
    qa = generator(k, eps, 0)
    qb = generator(k, eps, 1)
    e0 = [1.0, 0.0, 0.0]
    ab_mid, tail_a1 = exp_action(e0, qa, tau_a)
    ab_end, tail_b2 = exp_action(ab_mid, qb, tau_b)
    ba_mid, tail_b1 = exp_action(e0, qb, tau_b)
    ba_end, tail_a2 = exp_action(ba_mid, qa, tau_a)
    p_ab, p_ba = ab_end[2], ba_end[2]
    return {
        "p_state2_AB": p_ab,
        "p_state2_BA": p_ba,
        "order_contrast": p_ab - p_ba,
        "uniformization_tail_bound": max(tail_a1, tail_b2, tail_b1, tail_a2),
    }


def max_exit(q: Matrix) -> float:
    return max(-q[i][i] for i in range(len(q)))


def commutator_projection(k: float, eps: float) -> float:
    qa = generator(k, eps, 0)
    qb = generator(k, eps, 1)
    qab, qba = matmul(qa, qb), matmul(qb, qa)
    return qab[0][2] - qba[0][2]


def pulse_kernel(k: float, eps: float, t: float) -> float:
    """Closed-form scalar for the exact mirrored-pulse commutator identity."""
    s = k + eps
    rho = math.sqrt(k * k - k * eps + eps * eps)
    lam_minus, lam_plus = s - rho, s + rho
    return (math.exp(-lam_minus * t) - math.exp(-lam_plus * t)) / (2.0 * rho)


def exact_order_contrast(k: float, eps: float, tau_a: float, tau_b: float) -> float:
    """Exact formula for state-2 contrast under mirrored edge conductances."""
    return (k * k - eps * eps) * pulse_kernel(k, eps, tau_a) * pulse_kernel(k, eps, tau_b)


def exact_state_exchange(k: float, eps: float, tau_a: float, tau_b: float) -> Vector:
    """AB-minus-BA distribution: exactly (0,-Delta,+Delta) in this model."""
    d = exact_order_contrast(k, eps, tau_a, tau_b)
    return [0.0, -d, d]


def exact_output_contrast(k: float, eps: float, tau_a: float, tau_b: float,
                          output_given_state: Sequence[float]) -> float:
    """Order contrast for any common state-conditional output probability."""
    if len(output_given_state) != 3:
        raise ValueError("output_given_state must have one value per RNA state")
    d = exact_order_contrast(k, eps, tau_a, tau_b)
    return d * (output_given_state[2] - output_given_state[1])


def optimal_pulse_width(k: float, eps: float) -> float:
    """Peak of h(t); eps=0 is the monotone limiting case (+infinity)."""
    if eps == 0.0:
        return math.inf
    s = k + eps
    rho = math.sqrt(k * k - k * eps + eps * eps)
    return math.log((s + rho) / (s - rho)) / (2.0 * rho)


def triangle_generator(g01: float, g12: float, g02: float) -> Matrix:
    """Common post-pulse symmetric generator, including a possible shortcut."""
    q = zeros(3)
    for i, j, rate in ((0, 1, g01), (1, 2, g12), (0, 2, g02)):
        q[i][j] = q[j][i] = rate
        q[i][i] -= rate
        q[j][j] -= rate
    return q


def delayed_readout_contrast(k: float, eps: float, tau_a: float, tau_b: float,
                             q_common: Matrix, delay: float) -> float:
    """State-2 contrast after common post-pulse dynamics for a stated delay."""
    qa, qb = generator(k, eps, 0), generator(k, eps, 1)
    e0 = [1.0, 0.0, 0.0]
    ab, _ = exp_action(e0, qa, tau_a)
    ab, _ = exp_action(ab, qb, tau_b)
    ba, _ = exp_action(e0, qb, tau_b)
    ba, _ = exp_action(ba, qa, tau_a)
    ab, _ = exp_action(ab, q_common, delay)
    ba, _ = exp_action(ba, q_common, delay)
    return ab[2] - ba[2]


def main() -> None:
    # The finite positive-leak fixture keeps each pulse generator irreducible
    # and has the same equilibrium pi=(1/3,1/3,1/3) in both pulse states.
    k, eps, tau = 1.0, 0.02, 1.0
    observed = pulse_order(k, eps, tau, tau)
    ideal = 0.25 * (1.0 - math.exp(-2.0 * k * tau)) ** 2
    leak_bound = ideal - 4.0 * eps * tau
    timing_eta = 0.05
    robust_bound = (
        0.25 * (1.0 - math.exp(-2.0 * k * (tau - timing_eta))) ** 2
        - 4.0 * eps * (tau + timing_eta)
    )
    h_jitter_min = min(pulse_kernel(k, eps, tau - timing_eta),
                       pulse_kernel(k, eps, tau + timing_eta))
    exact_jitter_bound = (k * k - eps * eps) * h_jitter_min**2
    sign_detection_pairs_95 = math.ceil(2.0 * math.log(20.0) / exact_jitter_bound**2)
    half_margin_pairs_95 = math.ceil(8.0 * math.log(40.0) / exact_jitter_bound**2)
    readout_states = [0.1, 0.25, 0.8]
    small_t = 1e-5
    small = pulse_order(k, eps, small_t, small_t)["order_contrast"] / small_t**2
    comm = commutator_projection(k, eps)

    # A coarse pulse-width sweep is included to expose the finite-rate
    # operating window; each point is a model calculation, not data.
    sweep = []
    for j in range(1, 301):
        t = j / 50.0
        sweep.append((pulse_order(k, eps, t, t)["order_contrast"], t))
    peak, peak_tau = max(sweep)
    plateau_long = pulse_order(k, eps, 30.0, 30.0)["order_contrast"]

    # Exact-formula checks across symmetric, asymmetric and reversed-rate
    # fixtures. These compare two independent implementations: uniformization
    # and the closed-form commutator identity.
    formula_checks = []
    for kk, ee, ta, tb in (
        (1.0, 0.02, 0.2, 1.7),
        (1.0, 0.4, 1.3, 0.6),
        (0.5, 0.8, 0.9, 1.1),
        (1.0, 1.0, 0.7, 2.0),
    ):
        numeric = pulse_order(kk, ee, ta, tb)["order_contrast"]
        analytic = exact_order_contrast(kk, ee, ta, tb)
        qa, qb = generator(kk, ee, 0), generator(kk, ee, 1)
        ab, _ = exp_action([1.0, 0.0, 0.0], qa, ta)
        ab, _ = exp_action(ab, qb, tb)
        ba, _ = exp_action([1.0, 0.0, 0.0], qb, tb)
        ba, _ = exp_action(ba, qa, ta)
        state_delta = [ab[i] - ba[i] for i in range(3)]
        err = abs(numeric - analytic)
        formula_checks.append({"k": kk, "eps": ee, "tau_a": ta, "tau_b": tb,
                               "numeric": numeric, "analytic": analytic,
                               "absolute_error": err,
                               "state_distribution_difference": state_delta,
                               "max_state_exchange_error": max(abs(state_delta[i] - exact_state_exchange(kk, ee, ta, tb)[i]) for i in range(3))})
        if err > 2e-12:
            raise AssertionError("uniformization and exact pulse formula disagree")
        if max(abs(state_delta[i] - exact_state_exchange(kk, ee, ta, tb)[i]) for i in range(3)) > 2e-12:
            raise AssertionError("pulse order is not an exact state-1/state-2 mass exchange")

    # With an at-most pulse-time budget and equal time costs, strict log-
    # concavity makes the optimal symmetric width min(B/2,t_peak).
    time_budget = 4.0
    time_peak = optimal_pulse_width(k, eps)
    width_star = min(time_budget / 2.0, time_peak)
    budget_optimum = exact_order_contrast(k, eps, width_star, width_star)

    # A common, reversible but non-nearest-neighbor post-pulse evolution can
    # reverse the state-2 scalar readout after a delay. This is a numerical
    # counterexample to unqualified timing-alignment robustness.
    q_shortcut = triangle_generator(g01=0.01, g12=1.0, g02=0.1)
    immediate = pulse_order(k, eps, tau, tau)["order_contrast"]
    delayed = delayed_readout_contrast(k, eps, tau, tau, q_shortcut, 10.0)
    if not (immediate > 0.0 and delayed < 0.0):
        raise AssertionError("delayed-readout sign-reversal fixture failed")

    result = {
        "model": {
            "states": ["0", "1", "2"],
            "input_A_strong_edge": "0<->1",
            "input_B_strong_edge": "1<->2",
            "strong_rate_per_s": k,
            "cross_talk_rate_per_s": eps,
            "fixed_input_stationary_distribution": [1 / 3, 1 / 3, 1 / 3],
            "equilibrium_is_shared": True,
        },
        "equal_pulse_fixture": {"duration_s": tau, **observed},
        "ideal_zero_leak_exact_contrast": ideal,
        "positive_leak_contrast_lower_bound": leak_bound,
        "duration_error_bound": {
            "per_pulse_absolute_error_s": timing_eta,
            "coarse_zero_leak_comparison_bound": robust_bound,
            "exact_positive_leak_contrast_lower_bound": exact_jitter_bound,
            "scope": "bounded independent pulse-duration errors in this exact mirrored model; pulse start alignment, intervening evolution and output latency remain separate",
        },
        "paired_binary_assay_cost": {
            "robust_expected_contrast_lower_bound": exact_jitter_bound,
            "independent_AB_BA_pairs_for_95pct_one_sided_sign_detection": sign_detection_pairs_95,
            "independent_AB_BA_pairs_for_95pct_two_sided_half_margin": half_margin_pairs_95,
            "assumption": "each independent pair is two condition-level Bernoulli runs; this is not a molecule count when molecules share a reaction batch",
        },
        "small_pulse_check": {
            "contrast_over_tau_squared_at_tau_1e-5": small,
            "commutator_projection_exact": comm,
        },
        "exact_formula": {
            "rho": math.sqrt(k * k - k * eps + eps * eps),
            "lambda_minus": k + eps - math.sqrt(k * k - k * eps + eps * eps),
            "lambda_plus": k + eps + math.sqrt(k * k - k * eps + eps * eps),
            "pulse_kernel_at_fixture": pulse_kernel(k, eps, tau),
            "exact_contrast_at_fixture": exact_order_contrast(k, eps, tau, tau),
            "checks_against_uniformization": formula_checks,
            "state_exchange_identity": "p_AB-p_BA=(0,-Delta,+Delta)",
            "generic_common_readout_identity": "Delta_output=Delta*(r_2-r_1) for state-conditional output probabilities r_i",
            "readout_example": {
                "state_conditional_output_probabilities": readout_states,
                "predicted_AB_minus_BA_output": exact_output_contrast(k, eps, tau, tau, readout_states),
            },
            "formula_scope": "mirrored symmetric edge rates, state-0 start, state-2 immediate readout; exact all positive pulse durations",
        },
        "time_budget_design": {
            "at_most_total_pulse_time_s": time_budget,
            "equal_cost_optimal_width_s": width_star,
            "individual_pulse_peak_width_s": time_peak,
            "predicted_contrast": budget_optimum,
            "derivation": "log h(t) is strictly concave; equal durations maximize at fixed sum, and unused time is optimal beyond the single-pulse peak",
            "scope": "actuator-on time only; excludes initialization, buffer exchange, transcription, assay, and biochemical actuator work",
        },
        "duration_sweep": {
            "grid_step_s": 0.02,
            "max_contrast_on_grid": peak,
            "duration_at_grid_max_s": peak_tau,
            "contrast_at_30s": plateau_long,
            "interpretation": "finite-input-rate noncommutativity has an operating window; both generators mix to the same uniform equilibrium at long durations",
        },
        "post_pulse_delay_counterexample": {
            "common_symmetric_generator_edges_per_s": {"0<->1": 0.01, "1<->2": 1.0, "0<->2": 0.1},
            "delay_s": 10.0,
            "immediate_state2_contrast": immediate,
            "delayed_state2_contrast": delayed,
            "scope": "a finite CTMC numerical counterexample; same common reversible post-pulse dynamics in both arms, but one-state readout sign reverses",
        },
        "numerical_scope": "uniformization finite-sum calculations with explicit Poisson-tail truncation diagnostic; model parameters are illustrative, not fitted biological rates",
    }
    if observed["order_contrast"] <= robust_bound:
        raise AssertionError("computed contrast failed the conservative leakage bound")
    if abs(small - comm) > 2e-4:
        raise AssertionError("small-time commutator expansion failed")
    out = Path(__file__).with_name("pulse_order_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
