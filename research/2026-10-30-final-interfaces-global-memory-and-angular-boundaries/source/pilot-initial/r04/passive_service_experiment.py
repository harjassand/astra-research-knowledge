#!/usr/bin/env python3
"""Finite-service identification and an explicit passive saturation obstruction.

All source dynamics are simulated.  No physical apparatus is operated.
Only RESULTS.json in this script's directory is written.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


class LosslessDelay:
    """A fixed real reciprocal one-port lossless scattering realization.

    y = a*u + c*x[head]; x[head] <- c*u - a*x[head]; head <- head+1.
    The overwrite plus rotation is an orthogonal state/input map.
    """

    def __init__(self, a, initial, dark_energy=0.0):
        if abs(a) >= 1:
            raise ValueError("Require |a| < 1")
        self.a = float(a)
        self.c = math.sqrt(1.0 - a*a)
        self.x = np.asarray(initial, dtype=float).copy()
        self.head = 0
        self.dark_energy = float(dark_energy)
        self.energy0 = float(self.x @ self.x) + self.dark_energy
        self.energy = self.energy0
        self.input_energy = 0.0
        self.output_energy = 0.0
        self.old_energy = 0.0
        self.max_balance_error = 0.0

    def step(self, u):
        old = float(self.x[self.head])
        h = self.c*old
        y = self.a*u + h
        new = self.c*u - self.a*old
        self.x[self.head] = new
        self.head = (self.head + 1) % self.x.size
        self.energy += new*new - old*old
        self.input_energy += u*u
        self.output_energy += y*y
        self.old_energy += h*h
        balance = self.energy + self.output_energy - self.energy0 - self.input_energy
        self.max_balance_error = max(self.max_balance_error, abs(balance))
        return y, h

    def summary(self):
        return {
            "state_dimension": int(self.x.size),
            "initial_energy": self.energy0,
            "final_energy": self.energy,
            "unchanged_dark_energy": self.dark_energy,
            "incident_energy": self.input_energy,
            "output_energy": self.output_energy,
            "old_field_energy": self.old_energy,
            "max_energy_balance_error": self.max_balance_error,
            "energy_recomputed_error": abs(self.energy - float(self.x @ self.x) - self.dark_energy),
        }


def adc(y, coin, full_scale=1.0, levels=257):
    """Clip then unbiased stochastic rounding; coin is fresh conditional on y.

    This supplies the exact conditional contract in the theorem.
    A physical implementation would require its own calibration evidence.
    """
    r = full_scale
    delta = 2*r/(levels - 1)
    z = max(-r, min(r, y))
    position = (z + r)/delta
    left = min(levels - 1, max(0, int(math.floor(position))))
    fraction = position - left
    index = min(levels - 1, left + int(coin < fraction))
    return -r + index*delta, bool(abs(y) > r)


def dense_constants(n, eta, energy0, failure=0.01, full_scale=1.0, levels=257):
    """Deterministic finite-horizon bounds, not fitted to the simulated source."""
    if not (0 < eta < full_scale):
        raise ValueError("Need 0 < eta < ADC full scale")
    delta = 2*full_scale/(levels-1)
    x = math.log(2/failure)
    k = 2*energy0 + 4*n*eta*eta
    beta = k/(n*(full_scale-eta)**2)
    noise = (
        math.sqrt(2*(k + n*delta*delta/4)*x)/(n*eta)
        + 2*(full_scale + eta)*x/(3*n*eta)
    )
    return {"H_bound": k, "attenuation_loss_bound": beta, "martingale_radius": noise,
            "additive_gain_radius": beta+noise}


def select_eta(n, energy0, failure, full_scale=1.0, max_command=0.7):
    # Design uses only declared resource limits, not true gain, state or errors.
    candidates = np.geomspace(0.001*full_scale, min(0.7*full_scale, max_command), 20000)
    values = [dense_constants(n, float(e), energy0, failure, full_scale)["additive_gain_radius"]
              for e in candidates]
    return float(candidates[int(np.argmin(values))])


def gain_interval(estimate, noise, beta):
    """Invert estimate = a*tau + martingale noise, tau in [1-beta,1]."""
    lo = estimate - noise
    hi = estimate + noise
    tau = max(0.0, 1.0-beta)
    if tau > 0:
        lower = lo/tau if lo < 0 else lo
        upper = hi/tau if hi > 0 else hi
    else:
        lower = -1.0 if lo <= 0 else lo
        upper = 1.0 if hi >= 0 else hi
    lower, upper = max(-1.0, lower), min(1.0, upper)
    if lower > upper:  # Confidence event failed or physical contract invalid.
        return (-1.0, 1.0)
    return (lower, upper)


def optimal_command(a, b=0.4, regularizer=0.5):
    return a*b/(a*a + regularizer)


def task_interval(gain_ci, b=0.4, regularizer=0.5):
    lo, hi = gain_ci
    candidates = [lo, hi]
    for stationary in [-math.sqrt(regularizer), math.sqrt(regularizer)]:
        if lo <= stationary <= hi:
            candidates.append(stationary)
    vals = [optimal_command(a, b, regularizer) for a in candidates]
    low, high = min(vals), max(vals)
    return {"interval": [low, high], "returned_command": (low+high)/2,
            "certified_distance_radius": (high-low)/2}


def simulate_dense(a, delay, n, eta, seed, energy0=64.0, dark_energy=9.0):
    rng = np.random.default_rng(seed)
    initial = rng.normal(size=delay)
    initial *= math.sqrt((energy0-dark_energy)/float(initial@initial))
    plant = LosslessDelay(a, initial, dark_energy)
    signs = rng.choice([-1.0, 1.0], size=n)
    rounding_coins = rng.random(n)
    correlation = 0.0
    warnings = 0
    for s, coin in zip(signs, rounding_coins):
        y, _ = plant.step(eta*float(s))
        q, warning = adc(y, float(coin))
        warnings += warning
        correlation += float(s)*q
    estimate = correlation/(n*eta)
    constants = dense_constants(n, eta, energy0)
    ci = gain_interval(estimate, constants["martingale_radius"], constants["attenuation_loss_bound"])
    task = task_interval(ci)
    true_u = optimal_command(a)
    return {
        "true_gain_for_audit_only": a, "delay_windows": delay,
        "calendar_windows": n, "physical_windows": n, "active_windows": n,
        "scalar_ADC_reads": n, "ADC_levels": 257, "ADC_full_scale": 1.0,
        "probe_amplitude": eta, "zero_input_waits": 0, "resets": 0,
        "recorded_saturated_reads_all_retained": warnings,
        "signed_correlation_estimate": estimate, "constants": constants,
        "controller_gain_interval": list(ci), "controller_task_certificate": task,
        "true_optimal_command_for_audit_only": true_u,
        "actual_distance_for_audit_only": abs(task["returned_command"]-true_u),
        "gain_coverage": ci[0] <= a <= ci[1],
        "task_coverage": abs(task["returned_command"]-true_u) <= task["certified_distance_radius"] + 1e-12,
        "passive_resource_audit": plant.summary(),
    }


def sparse_constants(n, m, p, amplitude, energy0, failure=0.01, r=1.0, levels=257):
    # Split failure equally between the input-count bound and Freedman.
    # With probability >=1-failure/2, M <= cap.  On that event V <= vcap.
    z = math.log(2/failure)
    cap = min(n, int(math.ceil(n*p + math.sqrt(2*n*p*z) + 2*z/3)))
    k = 2*energy0 + 4*cap*amplitude*amplitude
    x = math.log(4/failure)
    delta = 2*r/(levels-1)
    if m == 0 or m > cap:
        return {"active_count_cap": cap, "count_cap_respected": m <= cap,
                "attenuation_loss_bound": 1.0, "martingale_radius": 2.0}
    beta = p*k/(m*(r-amplitude)**2)
    noise = (math.sqrt(2*p*(k+n*delta*delta/4)*x)
             + 2*(r+2*amplitude)*x/3)/(m*amplitude)
    return {"active_count_cap": cap, "count_cap_respected": True,
            "H_bound_on_count_event": k, "attenuation_loss_bound": beta,
            "martingale_radius": noise}


def simulate_sparse(a, delay, n, eta, amplitude, seed, energy0=64.0, dark_energy=9.0):
    rng = np.random.default_rng(seed)
    initial = rng.normal(size=delay)
    initial *= math.sqrt((energy0-dark_energy)/float(initial@initial))
    plant = LosslessDelay(a, initial, dark_energy)
    p = (eta/amplitude)**2  # Equal expected incident energy to dense design.
    activities = rng.random(n) < p
    signs = rng.choice([-1.0, 1.0], size=n)
    rounding_coins = rng.random(n)
    correlation, warnings, active = 0.0, 0, 0
    for on, s, coin in zip(activities, signs, rounding_coins):
        y, _ = plant.step(amplitude*float(s) if on else 0.0)
        if on:
            active += 1
            q, warning = adc(y, float(coin))
            warnings += warning
            correlation += float(s)*q
    estimate = correlation/(active*amplitude) if active else 0.0
    constants = sparse_constants(n, active, p, amplitude, energy0)
    if active == 0 or not constants["count_cap_respected"]:
        ci = (-1.0, 1.0)
    else:
        ci = gain_interval(estimate, constants["martingale_radius"], constants["attenuation_loss_bound"])
    task = task_interval(ci)
    true_u = optimal_command(a)
    return {
        "ordinary_comparator": "active-index signed regression, sparse randomized probes",
        "true_gain_for_audit_only": a, "delay_windows": delay,
        "calendar_windows": n, "physical_windows": n, "active_windows": active,
        "scalar_ADC_reads": active, "ADC_levels": 257, "ADC_full_scale": 1.0,
        "activity_probability": p, "probe_amplitude": amplitude,
        "expected_incident_energy": n*p*amplitude*amplitude,
        "zero_input_waits": n-active, "resets": 0,
        "recorded_saturated_reads_all_retained": warnings,
        "signed_correlation_estimate": estimate, "constants": constants,
        "controller_gain_interval": list(ci), "controller_task_certificate": task,
        "true_optimal_command_for_audit_only": true_u,
        "actual_distance_for_audit_only": abs(task["returned_command"]-true_u),
        "gain_coverage": ci[0] <= a <= ci[1],
        "task_coverage": abs(task["returned_command"]-true_u) <= task["certified_distance_radius"]+1e-12,
        "passive_resource_audit": plant.summary(),
    }


def saturated_twins(horizon=1024, max_command=0.7, r=1.0, regularizer=0.5, b=0.4):
    magnitude = math.sqrt(regularizer)
    c = math.sqrt(1-magnitude*magnitude)
    old_field = r + magnitude*max_command + 0.01
    initial = np.full(horizon, old_field/c)
    plus = LosslessDelay(magnitude, initial)
    minus = LosslessDelay(-magnitude, initial)
    rng = np.random.default_rng(1042026)
    transcript_plus, transcript_minus = [], []
    raw_difference, minimum_margin = 0.0, float("inf")
    # The proof covers every adaptive bounded policy.  This policy is a replay
    # check with both random excitation and deterministic response feedback.
    previous = 0.0
    for k in range(horizon):
        u = max_command*math.tanh(rng.normal() + 0.2*previous + (-1)**k)
        coin = float(rng.random())
        yp, _ = plus.step(u)
        ym, _ = minus.step(u)
        qp, wp = adc(yp, coin, r)
        qm, wm = adc(ym, coin, r)
        transcript_plus.append([qp, wp])
        transcript_minus.append([qm, wm])
        previous = qp
        raw_difference = max(raw_difference, abs(yp-ym))
        minimum_margin = min(minimum_margin, yp-r, ym-r)
    r0 = b/(2*math.sqrt(regularizer))
    return {
        "physical_windows": horizon, "state_dimension_per_instance": horizon,
        "max_command": max_command, "ADC_full_scale": r,
        "gains": [-magnitude, magnitude], "old_field_per_window": old_field,
        "required_initial_energy": horizon*old_field*old_field/(1-magnitude*magnitude),
        "identical_ADC_values_and_warning_flags": transcript_plus == transcript_minus,
        "minimum_true_saturation_margin": minimum_margin,
        "max_raw_readout_difference": raw_difference,
        "opposite_optimal_commands": [-r0, r0],
        "deterministic_minimax_command_radius": r0,
        "confidence_claim": "For any honest 1-delta radius certificate on both instances, P(radius < r0) <= 2 delta.",
        "plus_resource_audit": plus.summary(), "minus_resource_audit": minus.summary(),
    }


def secant_checks():
    rng = np.random.default_rng(44)
    largest_error = 0.0
    worst_bias_excess = 0.0
    for _ in range(100000):
        a = float(rng.uniform(-1, 1))
        eta = float(rng.uniform(0.001, 0.9))
        h = float(rng.normal()*4)
        secant = (np.clip(h+a*eta, -1, 1)-np.clip(h-a*eta, -1, 1))/(2*eta)
        # The sign-symmetry identity and attenuation are what make the new
        # certificate valid even though no hypothetical second read is made.
        tau = secant/a if abs(a) > 1e-12 else 0.0
        largest_error = max(largest_error, max(0.0, -tau, tau-1))
        bound = abs(a)*float(abs(h) > 1-eta)
        worst_bias_excess = max(worst_bias_excess, abs(secant-a)-bound)
    return {"random_scalar_secant_checks": 100000, "max_attenuation_violation": largest_error,
            "max_energy_charge_bias_violation": worst_bias_excess}


def main():
    n, energy0, failure = 16384, 64.0, 0.01
    eta = select_eta(n, energy0, failure)
    cases = [(0.01, 1), (0.3, 1), (-0.6, 127), (0.95, 32768)]
    dense = [simulate_dense(a, delay, n, eta, 1000+i) for i, (a, delay) in enumerate(cases)]
    sparse = [simulate_sparse(a, delay, n, eta, 0.25, 1000+i) for i, (a, delay) in enumerate(cases)]
    # Modest executable calibration check, not an empirical substitute for proof.
    repetitions = [simulate_dense(0.3, 7, 4096, select_eta(4096, energy0, failure), 20000+i)
                   for i in range(128)]
    result = {
        "model_scope": "Fixed contractive scalar incremental response, one persistent passive scattering specimen, no bath, known E0, calibrated conditional stochastic-rounding ADC.",
        "failure_probability_per_primary_task": failure,
        "zero_experiment_command_radius": 0.4/(2*math.sqrt(0.5)),
        "first_failed_attack_saturated_twins": saturated_twins(),
        "changed_mechanism_design": {"physical_windows": n, "energy0_bound": energy0,
            "probe_amplitude_chosen_without_source_knowledge": eta,
            "dense_expected_and_actual_incident_energy": n*eta*eta},
        "dense_ordinary_signed_regression": dense,
        "matched_expected_energy_sparse_ordinary_comparator": sparse,
        "secant_identity_numerical_check": secant_checks(),
        "additional_simulated_coverage": {
            "trials": len(repetitions), "physical_windows_per_trial": 4096,
            "true_gain": 0.3, "delay": 7,
            "gain_failures": sum(not z["gain_coverage"] for z in repetitions),
            "task_failures": sum(not z["task_coverage"] for z in repetitions),
            "largest_actual_error_over_reported_radius": max(
                z["actual_distance_for_audit_only"]/z["controller_task_certificate"]["certified_distance_radius"]
                for z in repetitions),
            "meaning": "Finite diagnostics only; the probability guarantee rests on the theorem and exact stated contracts.",
        },
    }
    target = Path(__file__).resolve().parent/"RESULTS.json"
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"results": str(target), "eta": eta,
        "twin_records_identical": result["first_failed_attack_saturated_twins"]["identical_ADC_values_and_warning_flags"],
        "dense_task_radii": [z["controller_task_certificate"]["certified_distance_radius"] for z in dense],
        "sparse_task_radii": [z["controller_task_certificate"]["certified_distance_radius"] for z in sparse],
        "sparse_read_counts": [z["scalar_ADC_reads"] for z in sparse],
        "all_primary_tasks_covered": all(z["task_coverage"] for z in dense+sparse),
        "coverage_diagnostic": result["additional_simulated_coverage"]}, indent=2))


if __name__ == "__main__":
    main()
