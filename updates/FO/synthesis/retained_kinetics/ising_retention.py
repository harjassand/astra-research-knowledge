#!/usr/bin/env python3
"""Exact finite-state Glauber model for phase-selective domain writing.

Dimensionless, illustrative model only: no GaAs/BTO material parameters.
The state is a periodic chain of inversion-related +/- variants. Single-site
heat-bath flips explicitly include pair-wall nucleation, wall migration,
domain growth and regrowth. The driven field is a hypothetical effective
conjugate field h(phi); its optical realization is not acquired.
"""
from __future__ import annotations

import itertools
import json
import math
import pathlib
import sys

import numpy as np
from scipy.linalg import expm


N = 8
BETA = 1.0
J = 1.0
H = 0.30
NU = 1.0
PULSE_TIME = 40.0
RETENTION_TIME = 2.0


def states_for(n: int) -> np.ndarray:
    return np.asarray(list(itertools.product((-1, 1), repeat=n)), dtype=np.int8)


def energy(s: np.ndarray, h: float, j: float = J) -> float:
    return -j * float(np.sum(s * np.roll(s, -1))) - h * float(np.sum(s))


def generator(states: np.ndarray, h: float, nu: float = NU, j: float = J) -> np.ndarray:
    lookup = {tuple(row): k for k, row in enumerate(states)}
    q = np.zeros((len(states), len(states)), dtype=float)
    for a, s in enumerate(states):
        for i in range(len(s)):
            sp = s.copy()
            sp[i] *= -1
            b = lookup[tuple(sp)]
            de = energy(sp, h, j) - energy(s, h, j)
            rate = nu / (1.0 + math.exp(BETA * de))
            q[a, b] = rate
        q[a, a] = -q[a].sum()
    return q


def gibbs(states: np.ndarray, h: float) -> np.ndarray:
    e = np.asarray([energy(s, h) for s in states])
    z = np.exp(-BETA * (e - e.min()))
    return z / z.sum()


def evolve(p: np.ndarray, q: np.ndarray, t: float) -> np.ndarray:
    return p @ expm(q * t)


def obs(p: np.ndarray, states: np.ndarray) -> dict[str, float]:
    m = states.sum(axis=1) / len(states[0])
    walls = (states != np.roll(states, -1, axis=1)).sum(axis=1) / 2
    p_positive = float(p @ (states.sum(axis=1) > 0))
    p_negative = float(p @ (states.sum(axis=1) < 0))
    p_tie = float(p @ (states.sum(axis=1) == 0))
    return {
        "mean_polarity": float(p @ m),
        "prob_all_plus": float(p @ np.all(states == 1, axis=1)),
        "prob_all_minus": float(p @ np.all(states == -1, axis=1)),
        "prob_positive_majority": p_positive,
        "prob_negative_majority": p_negative,
        "prob_tied": p_tie,
        "mean_domain_walls": float(p @ walls),
    }


def main() -> None:
    s = states_for(N)
    p0 = gibbs(s, 0.0)
    qplus = generator(s, H)
    qminus = generator(s, -H)
    qzero = generator(s, 0.0)
    qfast = generator(s, 0.0, nu=10.0)

    p_plus_on = evolve(p0, qplus, PULSE_TIME)
    p_pulse_kernel = expm(qplus * PULSE_TIME)
    p_minus_on = evolve(p0, qminus, PULSE_TIME)
    p_plus = evolve(p_plus_on, qzero, RETENTION_TIME)
    p_minus = evolve(p_minus_on, qzero, RETENTION_TIME)
    p_unbiased = evolve(evolve(p0, qzero, PULSE_TIME), qzero, RETENTION_TIME)
    p_fast = evolve(evolve(p0, qfast, PULSE_TIME), qzero, RETENTION_TIME)
    p_long = evolve(p_plus_on, qzero, 1000.0)
    # A genuinely nonequilibrium, inversion-symmetric domain mosaic isolates
    # the clock/coarsening effect of a common mobility multiplier.
    p_mosaic0 = np.full(len(s), 1.0 / len(s))
    p_mosaic_slow = evolve(p_mosaic0, qzero, 1.0)
    p_mosaic_fast = evolve(p_mosaic0, qfast, 1.0)

    # Row-generator detailed balance and global inversion identities.
    pi_h = gibbs(s, H)
    db_residual = max(
        abs(pi_h[a] * qplus[a, b] - pi_h[b] * qplus[b, a])
        for a in range(len(s)) for b in range(len(s))
    )
    inv = {tuple(row): i for i, row in enumerate(s)}
    inversion_residual = max(
        abs(p_plus[i] - p_minus[inv[tuple(-row)]]) for i, row in enumerate(s)
    )
    # Mean work for sudden h: 0 -> +H -> 0, in kBT units, starts in pi_0.
    # W_on=-H M(before); <M(before)>=0. W_off=+H M(after pulse).
    m_on = float(p_plus_on @ (s.sum(axis=1) / N))
    work_beta = H * N * m_on
    total_m = s.sum(axis=1).astype(float)
    joint_work = H * (total_m[None, :] - total_m[:, None])
    joint_prob = p0[:, None] * p_pulse_kernel
    work_second_beta2 = float(np.sum(joint_prob * joint_work * joint_work))
    work_variance_beta2 = work_second_beta2 - work_beta * work_beta
    work_support = np.unique(np.round(joint_work, 12))
    work_histogram = {
        f"{float(w):.12g}": float(joint_prob[np.isclose(joint_work, w)].sum())
        for w in work_support
    }
    # Nonequilibrium free energy at final h=0 relative to equilibrium pi_0.
    e0 = np.asarray([energy(row, 0.0) for row in s])
    safe = np.maximum(p_plus, np.finfo(float).tiny)
    rel_entropy = float(np.sum(safe * np.log(safe / p0)))
    free_energy_beta = rel_entropy
    sign_obs = obs(p_plus, s)
    record_probs = [
        sign_obs["prob_positive_majority"],
        sign_obs["prob_negative_majority"],
        sign_obs["prob_tied"],
    ]
    record_reset_entropy = -sum(x * math.log(x) for x in record_probs if x > 0)
    non_tie_pplus = record_probs[0] / (record_probs[0] + record_probs[1])
    binary_write_info = math.log(2.0) + non_tie_pplus * math.log(non_tie_pplus) + (1.0 - non_tie_pplus) * math.log(1.0 - non_tie_pplus)

    # Coarse two-variant demonstration that a small per-site field can have
    # extensive coupling. k is a hypothetical whole-domain attempt rate.
    coarse_n = 100
    coarse_beta_h = 0.01
    coarse_k = 0.001
    coarse_pulse_t = 3000.0
    coarse_hold_t = 10.0
    x = coarse_n * coarse_beta_h
    coarse_m_pulse = math.tanh(x) * (1.0 - math.exp(-2.0 * coarse_k * math.cosh(x) * coarse_pulse_t))
    coarse_m_ret = coarse_m_pulse * math.exp(-2.0 * coarse_k * coarse_hold_t)
    coarse_p_ret = 0.5 * (1.0 + coarse_m_ret)
    coarse_free_energy_beta = (
        coarse_p_ret * math.log(2.0 * coarse_p_ret)
        + (1.0 - coarse_p_ret) * math.log(2.0 * (1.0 - coarse_p_ret))
    )
    coarse_record_entropy = -(
        coarse_p_ret * math.log(coarse_p_ret)
        + (1.0 - coarse_p_ret) * math.log(1.0 - coarse_p_ret)
    )

    result = {
        "status": "dimensionless finite-state countermodel; not material data",
        "parameters": {
            "N_ring_sites": N,
            "beta_J": BETA * J,
            "beta_h": BETA * H,
            "attempt_rate_nu": NU,
            "pulse_duration_nu_t": PULSE_TIME * NU,
            "field_free_retention_nu_t": RETENTION_TIME * NU,
            "state_count": len(s),
            "field_coupling": "hypothetical F(s;h)=-J sum_i s_i s_(i+1)-h sum_i s_i",
        },
        "metrics": {
            "plus_field_then_field_free_hold": obs(p_plus, s),
            "minus_field_then_field_free_hold": obs(p_minus, s),
            "unbiased_thermal_same_time": obs(p_unbiased, s),
            "unbiased_common_mobility_x10": obs(p_fast, s),
            "symmetric_random_mosaic_unbiased_same_elapsed_time": obs(p_mosaic_slow, s),
            "symmetric_random_mosaic_common_mobility_x10": obs(p_mosaic_fast, s),
            "same_positive_field_after_long_field_free_wait": obs(p_long, s),
            "pulse_end_mean_polarity_before_field_removal": m_on,
            "mean_work_kBT_sudden_field_on_off": work_beta,
            "mean_work_kBT_per_site_sudden_field_on_off": work_beta / N,
            "work_variance_kBT_squared_sudden_field_on_off": work_variance_beta2,
            "final_nonequilibrium_free_energy_kBT": free_energy_beta,
            "mean_dissipated_work_above_final_nonequilibrium_free_energy_kBT": work_beta - free_energy_beta,
            "three_outcome_measurement_record_reset_floor_kBT": record_reset_entropy,
            "binary_sign_write_information_floor_conditional_on_no_tie_kBT": binary_write_info,
            "coarse_two_variant_small_per_site_field_countermodel": {
                "N_sites": coarse_n,
                "beta_h_per_site": coarse_beta_h,
                "N_beta_h": x,
                "whole_domain_attempt_rate_nu": coarse_k,
                "pulse_duration_nu_t": coarse_k * coarse_pulse_t,
                "field_free_hold_nu_t": coarse_k * coarse_hold_t,
                "polarity_after_pulse": coarse_m_pulse,
                "polarity_after_field_free_hold": coarse_m_ret,
                "selected_probability_after_hold": coarse_p_ret,
                "mean_pulse_work_kBT": x * coarse_m_pulse,
                "final_nonequilibrium_free_energy_kBT": coarse_free_energy_beta,
                "binary_record_reset_floor_kBT": coarse_record_entropy,
                "status": "exact two-state kinetics with illustrative dimensionless rates; no material data",
            },
        },
        "exact_distributions": {
            "work_kBT_sudden_on_then_off_histogram": work_histogram,
            "configuration_probabilities_after_plus_pulse_and_field_free_hold": {
                "".join("+" if bit > 0 else "-" for bit in row): float(prob)
                for row, prob in zip(s, p_plus)
            },
        },
        "checks": {
            "max_detailed_balance_flux_residual": db_residual,
            "max_phase_reversal_inversion_residual": inversion_residual,
            "probability_mass_plus": float(p_plus.sum()),
            "probability_mass_minus": float(p_minus.sum()),
            "plus_retained_configuration_distribution_mass": float(p_plus.sum()),
            "sudden_on_off_work_histogram_mass": float(sum(work_histogram.values())),
            "symmetric_random_mosaic_mean_polarity_slow": obs(p_mosaic_slow, s)["mean_polarity"],
            "symmetric_random_mosaic_mean_polarity_fast": obs(p_mosaic_fast, s)["mean_polarity"],
            "x10_mobility_reduces_mosaic_wall_density_at_equal_elapsed_time": (
                obs(p_mosaic_fast, s)["mean_domain_walls"] < obs(p_mosaic_slow, s)["mean_domain_walls"]
            ),
        },
        "interpretation": [
            "The effective field biases both nucleation and interface drift while present.",
            "Field-free dynamics retains a finite-time polarity but is symmetric and eventually erases it for finite N and T.",
            "A common mobility multiplier changes the coarsening clock and leaves an exactly symmetric initial ensemble unbiased.",
            "An electric conjugate field that produces the same h(t) has the identical Markov law; optical advantage needs a measured lower-cost or otherwise inaccessible coupling.",
            "The binary sign-record reset floor is kBT times its Shannon entropy; this is optional for open-loop operation and excludes sensing/control work.",
        ],
    }
    out = pathlib.Path(__file__).with_name("ising_results.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
