#!/usr/bin/env python3
"""Discriminating experiment for signed, pre-ADC sigma-delta accumulation.

No equipment or external services. All alternatives see exactly the same
passive specimen, probes and warm-field trajectory. NumPy is the only dependency.
Run: python3 check_pre_adc_accumulation.py
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np


OUT = Path(__file__).resolve().parent
ALPHA = 0.7
FEEDBACK = 0.75
E0 = 16.0
DARK_ENERGY = 9.0
DELTA = 0.02
A_MAX = 1.0
B = 0.4
LAM = 0.5
U_MAX = 0.7


def passive_ring(n: int, r: float, delay: int, seed: int):
    """Exactly lossless delay-line scattering; target instantaneous gain a=-r.

    At the active ring slot:
      [x_new,y] = [[r,g],[g,-r]] [x_old,u].
    Rotating the ring is energy-preserving. A dark coordinate keeps energy 9.
    The experimenter is given E0 and |a|<=1, but not r, g, delay or state.
    """
    rng = np.random.default_rng(seed)
    signs = 2 * rng.integers(0, 2, size=n) - 1
    x = rng.normal(size=delay)
    x *= math.sqrt((E0 - DARK_ENERGY) / float(x @ x))
    g = math.sqrt(1.0 - r * r)
    y = np.empty(n)
    h = np.empty(n)
    max_balance_error = 0.0
    for t in range(n):
        slot = t % delay
        old = float(x[slot])
        u = ALPHA * int(signs[t])
        h[t] = g * old
        y[t] = h[t] - r * u
        new = r * old + g * u
        max_balance_error = max(
            max_balance_error, abs(new * new + y[t] ** 2 - old * old - u * u)
        )
        x[slot] = new
    return signs, y, h, {
        "actual_gain": -r,
        "delay": delay,
        "initial_energy": E0,
        "dark_energy_initial_and_final": DARK_ENERGY,
        "final_specimen_energy": float(x @ x) + DARK_ENERGY,
        "incident_energy": n * ALPHA * ALPHA,
        "output_energy": float(y @ y),
        "old_field_squared_sum_audit_only": float(h @ h),
        "local_energy_balance_max_absolute_error": max_balance_error,
        "global_energy_balance_absolute_error": abs(
            E0 + n * ALPHA * ALPHA
            - float(x @ x) - DARK_ENERGY - float(y @ y)
        ),
    }


def stochastic_adc(y: np.ndarray, radius: float, levels: int, seed: int):
    """Fresh stochastic rounding, conditionally mean equal to clipped y."""
    rng = np.random.default_rng(seed)
    clipped = np.clip(y, -radius, radius)
    step = 2 * radius / (levels - 1)
    grid = (clipped + radius) / step
    lower = np.floor(grid)
    report = -radius + step * (lower + (rng.random(len(y)) < grid - lower))
    return report, np.abs(y) > radius


def accumulator(z: np.ndarray, feedback: float):
    """Ideal analog recurrence; digital record consists only of q/feedback bits."""
    state = 0.0
    q = np.empty(len(z))
    states = np.empty(len(z))
    max_pre = 0.0
    for t, value in enumerate(z):
        pre = state + float(value)
        max_pre = max(max_pre, abs(pre))
        q[t] = feedback if pre >= 0 else -feedback
        state = pre - q[t]
        states[t] = state
    return q, states, max_pre


def gain_radius(n: int):
    # Weak L2 martingale maximal bound, not a fitted simulation constant.
    v = E0 + n * ALPHA * ALPHA
    ell = math.sqrt(v / DELTA)
    return (FEEDBACK + 3 * ell) / (ALPHA * n), FEEDBACK + 2 * ell


def task_interval(ahat: float, beta: float):
    """Exact scalar ridge optimum range over a certified gain interval."""
    lo, hi = max(-A_MAX, ahat - beta), min(A_MAX, ahat + beta)
    if lo > hi:
        return {"consistent_gain_interval": False}
    candidates = [lo, hi]
    for a in (-math.sqrt(LAM), math.sqrt(LAM)):
        if lo <= a <= hi:
            candidates.append(a)
    values = [max(-U_MAX, min(U_MAX, a * B / (a * a + LAM))) for a in candidates]
    low_u, high_u = min(values), max(values)
    return {
        "consistent_gain_interval": True,
        "gain_interval": [lo, hi],
        "command": (low_u + high_u) / 2,
        "certified_command_radius": (high_u - low_u) / 2,
    }


def one_run(n: int, r: float, delay: int, seed: int, detailed=False):
    signs, y, h, physical = passive_ring(n, r, delay, seed)
    a = -r
    demodulated = signs * y
    q, states, max_pre = accumulator(demodulated, FEEDBACK)
    sd = float(q.sum() / (ALPHA * n))
    full = float(demodulated.sum() / (ALPHA * n))
    beta, capacity = gain_radius(n)
    m = np.cumsum(signs * h)
    max_m = float(np.max(np.abs(m)))
    state_lemma_residual = float(np.max(np.abs(states) - FEEDBACK - 2 * np.maximum.accumulate(np.abs(m))))
    identity_error = abs(float(q.sum()) - (ALPHA * n * a + float(m[-1]) - float(states[-1])))
    adc, flags = stochastic_adc(y, FEEDBACK, 257, seed + 10_000)
    clipped_estimate = float(np.sum(signs * adc) / (ALPHA * n))
    mu = ALPHA * a
    conditional_clipped_mean = (
        np.clip(h + mu, -FEEDBACK, FEEDBACK)
        - np.clip(h - mu, -FEEDBACK, FEEDBACK)
    ) / (2 * ALPHA)

    # A stronger ordinary competitor for this globally LTI, contractive fixture.
    # The no-clipping threshold uses only E0, passivity, IID probe signs and N.
    # The LTI impulse-response l2 bound <=1 is an additional premise, unlike SD.
    delta_range, delta_memory, delta_adc = 0.005, 0.01, 0.005
    wide_radius = ALPHA * A_MAX + math.sqrt(E0) + ALPHA * math.sqrt(
        2 * math.log(2 * n / delta_range)
    )
    wide, wide_flags = stochastic_adc(y, wide_radius, 257, seed + 20_000)
    wide_estimate = float(np.sum(signs * wide) / (ALPHA * n))
    wide_step = 2 * wide_radius / 256
    wide_beta = (
        math.sqrt((E0 + ALPHA * ALPHA * n) / delta_memory)
        + wide_step * math.sqrt(2 * n * math.log(2 / delta_adc))
    ) / (ALPHA * n)

    result = {
        "physical": physical,
        "sigma_delta": {
            "estimate": sd,
            "audited_gain_error": abs(sd - a),
            "certified_gain_radius": beta,
            "allocated_failure_probability": DELTA,
            "predetermined_post_pulse_capacity": capacity,
            "predetermined_pre_pulse_capacity": capacity + FEEDBACK,
            "observed_max_post_pulse_state_audit_only": float(np.max(np.abs(states))),
            "observed_max_pre_pulse_state_audit_only": max_pre,
            "overload_encounters": int(np.count_nonzero(np.abs(states) > capacity)),
            "bits": n,
            "feedback_pulses": n,
            "feedback_amplitude": FEEDBACK,
            "conservative_stored_accumulator_energy_if_W_equals_half_state_squared": 0.5 * (capacity + FEEDBACK) ** 2,
            "feedback_positive_energy_bound_same_normalization": 0.5 * FEEDBACK * FEEDBACK * n,
            "task": task_interval(sd, beta),
            "uniform_task_radius_via_global_lipschitz_bound": min(B / (2 * math.sqrt(LAM)), B / LAM * beta),
        },
        "full_signed_read_ordinary_correlation": {
            "estimate": full,
            "audited_gain_error": abs(full - a),
            "certified_gain_radius_same_weak_L2_method": math.sqrt((E0 + ALPHA * ALPHA * n) / DELTA) / (ALPHA * n),
            "readout": "full signed analog samples; not available to the SD estimator",
        },
        "fixed_range_257_level_memoryless_adc": {
            "estimate": clipped_estimate,
            "audited_gain_error": abs(clipped_estimate - a),
            "retained_saturated_reads": int(flags.sum()),
            "conditional_mean_bias_audit_only": float(conditional_clipped_mean.mean() - a),
            "qualification": "naive correlation is biased; this is a failed attack, not the strongest ordinary estimator",
        },
        "ordinary_LTI_wide_range_257_level_adc": {
            "estimate": wide_estimate,
            "audited_gain_error": abs(wide_estimate - a),
            "certified_gain_radius": wide_beta,
            "allocated_failure_probability": delta_range + delta_memory + delta_adc,
            "range": wide_radius,
            "range_relative_to_SD_feedback": wide_radius / FEEDBACK,
            "saturated_reads": int(wide_flags.sum()),
            "bits_fixed_width": 9 * n,
            "additional_assumption": "the full specimen is a contractive LTI system, not merely fixed instantaneous gain plus passive predictable memory",
        },
        "zero_command": {"experiments": 0, "deterministic_radius": B / (2 * math.sqrt(LAM))},
        "scientific_checks": {
            "telescoping_identity_absolute_error": identity_error,
            "last_crossing_state_bound_max_violation": max(0.0, state_lemma_residual),
            "actual_martingale_max_audit_only": max_m,
            "theorem_event_satisfied_this_path_audit_only": max_m <= math.sqrt((E0 + ALPHA * ALPHA * n) / DELTA),
            "all_methods_used_same_specimen_fields": True,
            "specimen_resets": 0,
            "inactive_windows": 0,
        },
    }
    if detailed:
        prefix_q = np.cumsum(q)
        prefix_raw = np.cumsum(demodulated)
        prefix_adc = np.cumsum(signs * adc)
        result["prefixes"] = []
        for k in (4096, 16384, 65536, 262144):
            if k <= n:
                kbeta, kcapacity = gain_radius(k)
                khat = float(prefix_q[k - 1] / (ALPHA * k))
                result["prefixes"].append({
                    "windows": k,
                    "sigma_delta_estimate": khat,
                    "sigma_delta_gain_radius": kbeta,
                    "uniform_command_radius": min(B / (2 * math.sqrt(LAM)), B / LAM * kbeta),
                    "full_read_gain_error_audit_only": abs(float(prefix_raw[k - 1]) / (ALPHA * k) - a),
                    "memoryless_adc_gain_error_audit_only": abs(float(prefix_adc[k - 1]) / (ALPHA * k) - a),
                    "predetermined_accumulator_capacity": kcapacity,
                    "incident_specimen_energy": k * ALPHA * ALPHA,
                })
    return result


def exhaustive_last_crossing_check():
    """All 3^8 disturbance strings and four admissible constant signals."""
    max_violation = 0.0
    max_identity = 0.0
    count = 0
    for mu in (-FEEDBACK, -0.2, 0.3, FEEDBACK):
        for values in itertools.product((-2.0, 0.0, 2.0), repeat=8):
            w = np.asarray(values)
            q, states, _ = accumulator(mu + w, FEEDBACK)
            m = np.cumsum(w)
            max_violation = max(max_violation, float(np.max(np.abs(states) - FEEDBACK - 2 * np.maximum.accumulate(np.abs(m)))))
            max_identity = max(max_identity, abs(float(q.sum()) - (8 * mu + float(m[-1]) - float(states[-1]))))
            count += 1
    return {"disturbance_signal_cases": count, "max_state_lemma_violation": max(0.0, max_violation), "max_identity_error": max_identity}


def release_instance(n=16384, release=8192, r=0.7, seed=440):
    """Causal energy-balance adversary, beyond global LTI assumptions.

    Energy is kept at an unobserved port until a fixed release window. Selection
    of the stored-energy port is allowed as part of the hidden passive dynamics.
    This checks the operational model; no hardware realization is asserted.
    """
    rng = np.random.default_rng(seed)
    signs = 2 * rng.integers(0, 2, n) - 1
    g = math.sqrt(1 - r * r)
    energy = E0
    ys, hs = np.empty(n), np.zeros(n)
    balance_error = 0.0
    for t in range(n):
        active_port = math.sqrt(energy) if t == release else 0.0
        parked_energy = energy - active_port * active_port
        u = ALPHA * int(signs[t])
        ys[t] = g * active_port - r * u
        hs[t] = g * active_port
        new = parked_energy + (r * active_port + g * u) ** 2
        balance_error = max(balance_error, abs(new + ys[t] ** 2 - energy - u * u))
        energy = new
    q, states, pre = accumulator(signs * ys, FEEDBACK)
    estimate = float(q.sum() / (ALPHA * n))
    beta, capacity = gain_radius(n)
    return {
        "windows": n,
        "actual_gain": -r,
        "release_window_zero_based": release,
        "old_field_amplitude_at_release": float(hs[release]),
        "sigma_delta_estimate": estimate,
        "audited_gain_error": abs(estimate + r),
        "certified_gain_radius": beta,
        "observed_max_state": float(np.max(np.abs(states))),
        "predetermined_capacity": capacity,
        "observed_max_pre_pulse_state": pre,
        "max_energy_balance_error": balance_error,
        "qualification": "admissible causal passivity model, not a physical hardware construction or an impossibility result",
    }


def passive_initial_energy_lower_bound(n=64, trials=20000, seed=992):
    """Two passive gain instances, with every initial state energy <=E0.

    A delay of n ensures no injected signal returns during the observation
    horizon. The uniform guarantee lower bound permits arbitrary adaptive
    forward commands and even full analog readout; the numerical LRT check
    below uses full-magnitude constant commands.
    """
    separation = min(0.5, math.sqrt(E0) / (8 * ALPHA * n))
    gain = separation / 2
    g = math.sqrt(1 - gain * gain)
    state_std = math.sqrt(E0 / (4 * n))
    # Chernoff upper bound for P(chi-square_n > 4n).
    rejected_prior_mass_bound = math.exp(-n * (3 - math.log(4)) / 2)
    gaussian_tv_pinsker = separation * ALPHA * n / (g * math.sqrt(E0))
    truncated_tv_bound = min(1.0, gaussian_tv_pinsker + 2 * rejected_prior_mass_bound)
    rng = np.random.default_rng(seed)
    errors = []
    energy_residual = 0.0
    largest_initial = 0.0
    for a in (-gain, gain):
        x = rng.normal(0, state_std, size=(trials, n))
        energies = np.sum(x * x, axis=1)
        bad = energies > E0
        while np.any(bad):
            x[bad] = rng.normal(0, state_std, size=(int(bad.sum()), n))
            energies = np.sum(x * x, axis=1)
            bad = energies > E0
        largest_initial = max(largest_initial, float(energies.max()))
        # Scattering r=-a, g=sqrt(1-a^2), input alpha each window.
        y = a * ALPHA + g * x
        new_states = -a * x + g * ALPHA
        residual = np.sum(new_states * new_states, axis=1) + np.sum(y * y, axis=1) - energies - n * ALPHA * ALPHA
        energy_residual = max(energy_residual, float(np.max(np.abs(residual))))
        classified_positive = np.sum(y, axis=1) >= 0
        errors.append(float(np.mean(classified_positive if a < 0 else ~classified_positive)))
    return {
        "horizon_and_delay": n,
        "candidate_gains": [-gain, gain],
        "gain_separation": separation,
        "initial_state_prior": "N(0,E0/(4N) I) conditioned on squared norm <=E0",
        "every_actual_initial_state_has_energy_at_most": E0,
        "unconditioned_Gaussian_adaptive_KL_upper_bound": 2 * separation**2 * ALPHA**2 * n**2 / (g*g*E0),
        "removed_prior_mass_Chernoff_upper_bound": rejected_prior_mass_bound,
        "adaptive_full_analog_transcript_TV_upper_bound_after_truncation": truncated_tv_bound,
        "unavoidable_average_gain_estimation_failure_for_radius_less_than_half_separation": (1 - truncated_tv_bound) / 2,
        "unavoidable_control_radius_threshold_for_b_and_lambda": gain * B / (gain * gain + LAM),
        "numerical_full_analog_LRT_trials_per_instance": trials,
        "numerical_LRT_average_error": sum(errors) / 2,
        "unconditioned_Gaussian_LRT_exact_average_error": 0.5 * (1 - math.erf(separation * ALPHA * n / (g * math.sqrt(2 * E0)))),
        "largest_initial_energy_in_numerical_samples": largest_initial,
        "maximum_passive_energy_identity_residual": energy_residual,
        "scope": "forward-only one-port N-window observations, bounded |u|<=alpha, no access to internal delay states or reverse port, no resets; arbitrary adaptive algorithms and all digitizations are covered by the analytic lower bound",
    }


def exact_deterministic_indistinguishable_pair(n=64):
    """Two actual finite passive delay-line states, same exact zero transcript.

    Constant full-amplitude input is a concrete deterministic policy. For an
    arbitrary deterministic adaptive policy, substitute its commands along the
    all-zero observation path; the same initial-state construction and budget
    bound apply. Private fresh random signs are expressly outside this result.
    """
    c = math.sqrt(E0 / (E0 + n * ALPHA * ALPHA))
    g = math.sqrt(1 - c * c)
    instances = []
    for a in (-c, c):
        u = np.full(n, ALPHA)
        x = -a * u / g
        y = a * u + g * x
        new = -a * x + g * u
        instances.append({
            "gain": a,
            "delay": n,
            "every_initial_delay_coordinate": float(x[0]),
            "initial_state_energy": float(x @ x),
            "max_absolute_output": float(np.max(np.abs(y))),
            "final_state_energy": float(new @ new),
            "optimal_ridge_command": a * B / (a*a + LAM),
            "passive_identity_absolute_error": abs(float(new @ new + y @ y - x @ x - u @ u)),
        })
    return {
        "horizon": n,
        "instances": instances,
        "common_command_each_window": ALPHA,
        "common_analog_transcript": "zero in every window (exact algebra)",
        "unavoidable_deterministic_gain_radius": c,
        "unavoidable_deterministic_command_radius": c * B / (c*c + LAM),
        "scope": "no resets, forward-only one-port observations, deterministic policies; for a general deterministic policy preload x_t=-a*u_t(zero history)/g; initial energy is at most E0. Does not cover private fresh random signs or reverse-port access.",
    }


def main():
    main_result = one_run(262144, 1 / math.sqrt(2), 1, 7, detailed=True)
    fixtures = [
        ("short_memory", 1 / math.sqrt(2), 1),
        ("long_delay", 0.7, 257),
        ("near_frozen_observable_mode", 0.999999, 97),
    ]
    repeats = []
    for name, r, delay in fixtures:
        rows = [one_run(65536, r, delay, seed) for seed in range(8)]
        repeats.append({
            "fixture": name, "runs": len(rows), "windows_per_run": 65536,
            "sigma_delta_max_audited_error": max(x["sigma_delta"]["audited_gain_error"] for x in rows),
            "sigma_delta_gain_radius": rows[0]["sigma_delta"]["certified_gain_radius"],
            "certification_misses_observed": sum(x["sigma_delta"]["audited_gain_error"] > x["sigma_delta"]["certified_gain_radius"] for x in rows),
            "overload_encounters_observed": sum(x["sigma_delta"]["overload_encounters"] for x in rows),
            "memoryless_adc_mean_bias_audit_only": float(np.mean([x["fixed_range_257_level_memoryless_adc"]["estimate"] + r for x in rows])),
            "ordinary_wide_adc_max_audited_error": max(x["ordinary_LTI_wide_range_257_level_adc"]["audited_gain_error"] for x in rows),
        })
    output = {
        "model_and_scope": "Mathematical scalar forward-response identification with passive predictable additive memory, pre-ADC sign multiplication and sigma-delta analog state. No hardware/practical advantage/priority claim.",
        "parameters": {"alpha": ALPHA, "feedback": FEEDBACK, "E0": E0, "delta": DELTA, "known_gain_bound": A_MAX, "b": B, "lambda": LAM, "command_radius": U_MAX},
        "main_matched_experiment": main_result,
        "other_passive_fixtures": repeats,
        "stored_energy_release_discriminator": release_instance(),
        "passive_initial_energy_lower_bound": passive_initial_energy_lower_bound(),
        "exact_deterministic_indistinguishable_pair": exact_deterministic_indistinguishable_pair(),
        "exhaustive_algebra_check": exhaustive_last_crossing_check(),
        "warning": "Finite numerical runs test implementation and discriminate mechanisms; the stated probability theorem comes from the accompanying proof, not empirical coverage.",
    }
    destination = OUT / "PRE_ADC_ACCUMULATION_RESULTS.json"
    destination.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({
        "result_path": str(destination),
        "main_sigma_delta": main_result["sigma_delta"],
        "main_memoryless": main_result["fixed_range_257_level_memoryless_adc"],
        "ordinary_wide_adc": main_result["ordinary_LTI_wide_range_257_level_adc"],
        "prefixes": main_result["prefixes"],
        "other_fixtures": repeats,
        "passive_initial_energy_lower_bound": output["passive_initial_energy_lower_bound"],
        "exact_deterministic_indistinguishable_pair": output["exact_deterministic_indistinguishable_pair"],
        "algebra": output["exhaustive_algebra_check"],
    }, indent=2))


if __name__ == "__main__":
    main()
