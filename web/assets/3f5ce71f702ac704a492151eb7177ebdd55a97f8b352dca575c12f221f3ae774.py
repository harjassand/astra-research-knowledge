#!/usr/bin/env python3
"""Finite arithmetic checks for the robust block witness and mixing lower bound.

This script checks matrix stochasticity, Dobrushin coefficients, the finite
cycle-law alias, short-history conditional KL inequalities, robust sample caps,
and the two-sided replacement thresholds. It is not a proof about an assay.
"""
from __future__ import annotations

import json
import math


def cycle_matrix(rate_sum: float, theta: float) -> list[list[float]]:
    decay = math.exp(-1.5 * rate_sum * 0.05)
    row = [(1 + 2 * decay * math.cos(theta + shift)) / 3
           for shift in (0.0, -2 * math.pi / 3, 2 * math.pi / 3)]
    return [
        row[:],
        [row[2], row[0], row[1]],
        [row[1], row[2], row[0]],
    ]


def max_row_sum_error(P):
    return max(abs(sum(row) - 1) for row in P)


def dob_coefficient(P):
    return max(
        0.5 * sum(abs(P[i][k] - P[j][k]) for k in range(len(P)))
        for i in range(len(P)) for j in range(len(P))
    )


def row_mul(mu, P):
    return [sum(mu[i] * P[i][j] for i in range(len(mu)))
            for j in range(len(mu))]


def channel_law(mu, kappa):
    K = len(mu)
    return [(1 - kappa) / K + kappa * mu[y] for y in range(K)]


def bayes(mu, y, kappa):
    q = channel_law(mu, kappa)[y]
    K = len(mu)
    return [
        mu[i] * ((1 - kappa) / K + kappa * (i == y)) / q
        for i in range(K)
    ]


def kl(p, q):
    return sum(a * math.log(a / b) for a, b in zip(p, q) if a > 0)


def verify_histories(P0, P1, kappa, depth=5):
    K = len(P0)
    u = [1 / K] * K
    r = max(dob_coefficient(P0), dob_coefficient(P1))
    per_obs_bound = 8 * K**3 * kappa**4 * (r / (1 - r))**2
    max_cond_kl = 0.0
    max_filter_dist = 0.0

    def rec(mu0, mu1, steps_left):
        nonlocal max_cond_kl, max_filter_dist
        q0 = channel_law(mu0, kappa)
        q1 = channel_law(mu1, kappa)
        value = kl(q0, q1)
        max_cond_kl = max(max_cond_kl, value)
        max_filter_dist = max(
            max_filter_dist,
            sum(abs(mu0[i] - u[i]) for i in range(K)),
            sum(abs(mu1[i] - u[i]) for i in range(K)),
        )
        if steps_left == 0:
            return
        for y in range(K):
            next0 = row_mul(bayes(mu0, y, kappa), P0)
            next1 = row_mul(bayes(mu1, y, kappa), P1)
            rec(next0, next1, steps_left - 1)

    rec(u, u, depth)
    filter_bound = K * kappa * r / (1 - r)
    assert max_cond_kl <= per_obs_bound + 1e-12
    assert max_filter_dist <= filter_bound + 1e-12
    return {
        "max_conditional_KL_seen": max_cond_kl,
        "per_observation_KL_upper_bound": per_obs_bound,
        "max_filter_L1_from_uniform_seen": max_filter_dist,
        "filter_L1_upper_bound": filter_bound,
        "history_depth": depth,
    }


def main():
    K = 3
    t = 0.05
    P0 = cycle_matrix(10.0, 0.0)
    P1 = cycle_matrix(10.0, 2 * math.pi * t)
    alias0 = cycle_matrix(10.0, 0.0)
    alias1 = cycle_matrix(10.0, 2 * math.pi)
    alias_gap = max(abs(alias0[i][j] - alias1[i][j])
                    for i in range(K) for j in range(K))

    delta0 = dob_coefficient(P0)
    delta1 = dob_coefficient(P1)
    r = max(delta0, delta1)

    histories = {
        str(k): verify_histories(P0, P1, k, depth=5)
        for k in (0.1, 0.25, 0.5)
    }
    delta_test = 0.05
    n_lower_coefficient = ((1 - 2 * delta_test)**2 * (1 - r)**2) / (4 * K**3 * r**2)

    alpha = 0.05
    p_star = 1 / 3
    Gamma = 0.20900495072877529
    Gamma_bar = min(1.0, Gamma)
    kappa = 0.1
    read_seconds = 0.01
    Lambda = 10.0
    epsilon = p_star * Gamma_bar / 192
    q_cap = epsilon / 4
    p_action = p_star * (1 - q_cap)
    m = math.ceil(
        64 * K / Gamma**2
        * (1 + math.sqrt(math.log(4 * K / alpha)))**2
    )
    n_row = math.ceil(2 * m / p_action)
    n_occupancy = math.ceil(8 / p_action * math.log(8 * K / alpha))
    n_bad = math.ceil(8 / epsilon * math.log(8 / alpha))
    N_t = max(n_row, n_occupancy, n_bad)

    J = 0
    while True:
        delta_j = epsilon / (4 * (J + 1) * (J + 2))
        radius = (1 + math.sqrt(math.log(1 / delta_j))) / math.sqrt(2**J)
        if radius <= math.sqrt(2) * kappa / 16:
            break
        J += 1
    R_J = 2**J
    rho_gate = q_cap / (Lambda * R_J * read_seconds)
    blocks = 2 * N_t
    frames = blocks * R_J
    seconds = frames * read_seconds

    # For a common pre marginal and a row with mass p and endpoint-law TV tau,
    # whole-pair replacement neighborhoods overlap exactly at p*tau/2.
    p, tau = 0.1, 0.4
    pair_overlap = p * tau / 2
    post_block_overlap = p * tau / 2
    all_endpoint_overlap = p * tau / 4
    one_sided_post = p * tau

    result = {
        "status": "finite numerical check only",
        "cycle_witness": {
            "probe_duration": t,
            "lag_one_alias_max_abs": alias_gap,
            "P0_dobrushin": delta0,
            "P1_dobrushin": delta1,
            "uniform_action_bound_r": r,
            "testing_error_delta": delta_test,
            "n_lower_bound_coefficient_for_kappa_minus4": n_lower_coefficient,
            "n_lower_bound_at_kappa_0.1": n_lower_coefficient / (0.1**4),
            "conditional_KL_history_checks": histories,
        },
        "robust_block_cost": {
            "K": K, "p_star": p_star, "Gamma": Gamma, "alpha": alpha,
            "kappa": kappa, "read_interval_seconds": read_seconds,
            "epsilon_block_fraction": epsilon,
            "physical_per_block_gate": q_cap,
            "ramp_gate_if_rho_zero": q_cap,
            "m_per_transition_row": m,
            "N_row_bound": n_row,
            "N_occupancy_bound": n_occupancy,
            "N_bad_count_bound": n_bad,
            "episodes_N_t": N_t,
            "max_epoch_j": J,
            "frames_per_block": R_J,
            "slow_factor_if_q_ramp_zero": rho_gate,
            "total_blocks": blocks,
            "maximum_frames": frames,
            "held_read_seconds": seconds,
            "held_read_years": seconds / (365.25 * 24 * 3600),
            "excludes": [
                "all physical ramps",
                "probe action time",
                "founder preparation and calibration",
                "control, detector, culture, viability, and recovery costs",
            ],
        },
        "replacement_overlap_example": {
            "row_mass_p": p,
            "endpoint_law_TV_tau": tau,
            "whole_pair_fraction_threshold": pair_overlap,
            "post_block_fraction_threshold": post_block_overlap,
            "all_endpoint_fraction_threshold": all_endpoint_overlap,
            "one_sided_post_fraction_to_clean_other_world": one_sided_post,
        },
    }
    assert alias_gap < 1e-12
    assert max_row_sum_error(P0) < 1e-12 and max_row_sum_error(P1) < 1e-12
    for j in range(K):
        assert abs(sum(P0[i][j] for i in range(K)) - 1) < 1e-12
        assert abs(sum(P1[i][j] for i in range(K)) - 1) < 1e-12
    assert blocks == 2 * N_t
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
