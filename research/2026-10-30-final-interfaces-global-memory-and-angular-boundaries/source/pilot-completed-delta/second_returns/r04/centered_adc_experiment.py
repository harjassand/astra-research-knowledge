#!/usr/bin/env python3
"""Local follow-up: synchronous analog reference before a bounded ADC.

Reads the first-tranche local physical simulation. Writes only phase2 results.
The centered estimator is ordinary scalar interval identification; the new
resource is a calibrated signed analog reference before the clipping element.
"""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import sys

import numpy as np

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FIRST = HERE.parent / "passive_service_experiment.py"
spec = importlib.util.spec_from_file_location("first_service", FIRST)
first = importlib.util.module_from_spec(spec)
spec.loader.exec_module(first)


def block_constants(n, energy_bound, width, eta, reference_gain_error, levels, failure):
    r = 1.0
    rho = reference_gain_error
    qmax = width/2 + rho
    margin = r - qmax*eta
    if margin <= 0:
        raise ValueError("Residual command must leave a positive ADC margin")
    delta = 2*r/(levels-1)
    hbound = 2*energy_bound + 4*n*eta*eta
    beta = hbound/(n*margin*margin)
    x = math.log(2/failure)
    nu = (math.sqrt(2*(hbound+n*delta*delta/4)*x)/(n*eta)
          + 2*(r+qmax*eta)*x/(3*n*eta))
    threshold = width*(1-2*beta)/4
    return {"old_energy_bound": hbound, "attenuation_loss_bound": beta,
            "martingale_radius": nu, "reference_gain_error_bound": rho,
            "total_score_error": nu+rho,
            "half_width_progress_threshold": threshold,
            "positive_progress": beta < 0.5 and nu+rho <= threshold}


def choose_block(energy_bound, width, eta, rho, levels, failure):
    lo, hi = 1, 1
    while not block_constants(hi, energy_bound, width, eta, rho, levels, failure)["positive_progress"]:
        hi *= 2
        if hi > 2**48:
            raise ValueError("Requested precision exceeds the fixed reference contract")
    while lo < hi:
        mid = (lo+hi)//2
        if block_constants(mid, energy_bound, width, eta, rho, levels, failure)["positive_progress"]:
            hi = mid
        else:
            lo = mid+1
    return lo, block_constants(lo, energy_bound, width, eta, rho, levels, failure)


def planned_blocks(gain_radius, eta, levels=2, failure=0.01, energy0=64.0):
    stages = math.ceil(math.log2(1/gain_radius))
    # The signed-reference calibration error is charged, not set to zero.
    rho = gain_radius/32
    energy = energy0
    blocks = []
    for k in range(stages):
        width = 2**(1-k)
        n, constants = choose_block(energy, width, eta, rho, levels, failure/stages)
        blocks.append({"stage": k+1, "interval_width_before": width,
            "initial_stored_energy_bound": energy, "physical_windows": n,
            "failure_allocation": failure/stages, "constants": constants})
        energy += n*eta*eta  # Known conservative bound; no true state used.
    return blocks, rho


def candidate_ci(score, width, beta, error, old_interval):
    low, high = old_interval
    center = (low+high)/2
    kappa = 1-beta
    zl, zh = score-error, score+error
    sl = zl/kappa if zl < 0 else zl
    sh = zh/kappa if zh > 0 else zh
    ci = (max(low, center+sl), min(high, center+sh))
    if ci[0] > ci[1] or ci[1]-ci[0] > width/2 + 1e-12:
        return old_interval, False
    # Pad to exactly width/2. This makes all future budgets deterministic.
    newlow = max(low, min((ci[0]+ci[1])/2-width/4, high-width/2))
    new = (newlow, newlow+width/2)
    assert new[0]-1e-12 <= ci[0] <= ci[1] <= new[1]+1e-12
    return new, True


def simulate_centered(a, delay, eta=0.075, gain_radius=0.0625, levels=2, seed=1):
    energy0, dark = 64.0, 9.0
    plan, rho = planned_blocks(gain_radius, eta, levels, energy0=energy0)
    rng = np.random.default_rng(seed)
    initial = rng.normal(size=delay)
    initial *= math.sqrt((energy0-dark)/float(initial@initial))
    plant = first.LosslessDelay(a, initial, dark)
    interval = (-1.0, 1.0)
    stages, reads, saturated = [], 0, 0
    reference_squared_sum = 0.0
    total_reference_gain_error_max = 0.0
    for stage in plan:
        old = interval
        width = old[1]-old[0]
        center = (old[0]+old[1])/2
        # Reserve half the gain-error budget for unknown analog calibration.
        # The controller knows the digital DAC code, not the actual leakage.
        step = rho
        nominal_code = max(-1.0, min(1.0, round(center/step)*step))
        calibration_leakage = (-1.0 if seed % 2 else 1.0)*rho/4
        realized_center = nominal_code+calibration_leakage
        reference_error = realized_center-center
        total_reference_gain_error_max = max(total_reference_gain_error_max, abs(reference_error))
        assert abs(reference_error) <= rho+1e-12
        n = stage["physical_windows"]
        signs = rng.choice([-1.0, 1.0], size=n)
        coins = rng.random(n)
        total, warnings = 0.0, 0
        for sign, coin in zip(signs, coins):
            u = eta*float(sign)
            y, _ = plant.step(u)
            reference = realized_center*u
            q, warning = first.adc(y-reference, float(coin), levels=levels)
            total += float(sign)*q
            warnings += warning
            reference_squared_sum += reference*reference
        score = total/(n*eta)
        const = stage["constants"]
        interval, progress = candidate_ci(score, width, const["attenuation_loss_bound"],
            const["total_score_error"], old)
        reads += n
        saturated += warnings
        stages.append({**stage, "commanded_candidate": center,
            "known_nominal_reference_gain_code": nominal_code,
            "realized_reference_candidate_for_audit_only": realized_center,
            "unknown_reference_calibration_leakage_for_audit_only": calibration_leakage,
            "signed_centered_score": score, "retained_saturated_reads": warnings,
            "gain_interval_after": list(interval), "half_width_progress": progress,
            "gain_coverage_for_audit_only": interval[0] <= a <= interval[1]})
        if not progress:
            break
    task = first.task_interval(interval)
    actual_u = first.optimal_command(a)
    return {
        "true_gain_for_audit_only": a, "delay_windows": delay,
        "ADC_levels": levels, "ADC_full_scale": 1.0,
        "probe_amplitude": eta, "requested_gain_radius": gain_radius,
        "per_task_failure_probability": 0.01,
        "calendar_and_physical_windows": reads, "scalar_ADC_reads": reads,
        "saturated_reads_all_retained": saturated, "resets": 0,
        "zero_input_waits": 0, "stages": stages,
        "controller_final_gain_interval": list(interval),
        "controller_gain_radius": (interval[1]-interval[0])/2,
        "controller_task_certificate": task,
        "actual_command_error_for_audit_only": abs(task["returned_command"]-actual_u),
        "task_coverage_for_audit_only": abs(task["returned_command"]-actual_u) <= task["certified_distance_radius"]+1e-12,
        "reference_gain_error_bound": rho,
        "reference_gain_error_observed_for_audit_only": total_reference_gain_error_max,
        "reference_analog_full_span": 2*eta,
        "reference_required_span_including_error": 2*eta*(1+rho),
        "reference_analog_step": rho*eta,
        "reference_levels_including_endpoints": math.ceil(2/rho)+1,
        "reference_squared_sample_sum_not_joules": reference_squared_sum,
        "reference_sign_modulations": reads,
        "reference_candidate_changes": len(stages),
        "reference_resource_note": "Reference energy requires physical impedance, timing and electronics-work calibration. Its squared sample sum is not a complete apparatus-energy bill.",
        "passive_resource_audit": plant.summary(),
    }


def fixed_adc_budget(epsilon, levels, eta_grid):
    # Strong public-constants optimization of the first-return certificate,
    # not an information-theoretic lower bound for all fixed-ADC methods.
    etas = eta_grid
    e0, failure, r = 64.0, 0.01, 1.0
    x = math.log(2/failure)
    delta = 2*r/(levels-1)
    def evaluate(n):
        h = 2*e0+4*n*etas*etas
        beta = h/n/(r-etas)**2
        noise = np.sqrt(2*(h+n*delta*delta/4)*x)/(n*etas)+2*(r+etas)*x/(3*n*etas)
        j = int(np.argmin(beta+noise))
        return float((beta+noise)[j]), float(etas[j])
    lo, hi = 1, 1
    while evaluate(hi)[0] > epsilon:
        hi *= 2
    while lo < hi:
        mid = (lo+hi)//2
        if evaluate(mid)[0] <= epsilon:
            hi = mid
        else:
            lo = mid+1
    radius, amplitude = evaluate(lo)
    return {"method": "First-return ordinary fixed-ADC signed regression certificate, optimized amplitude grid",
        "ADC_levels": levels, "target_gain_radius": epsilon,
        "physical_windows_and_scalar_reads": lo, "probe_amplitude": amplitude,
        "incident_energy": lo*amplitude*amplitude, "gain_radius_bound": radius,
        "known_reference_operation": False,
        "comparison_scope": "Comparison between sufficient certificates; no lower bound on the strongest ordinary fixed-ADC estimator."}


def sparse_fixed_adc_pareto(epsilon=.0625, levels=2):
    """Ordinary sparse alternatives, with both count tails charged.

    These are analytic budget plans, not additional physical simulations.
    Minimize expected reads on a public grid for each calendar horizon.
    """
    p, amplitude = np.meshgrid(np.geomspace(.0001,.95,70), np.linspace(.02,.7,100))
    p, amplitude = p.ravel(), amplitude.ravel()
    failure, energy0, r = .01, 64., 1.
    z = math.log(4/failure)  # Two count tails share failure/2.
    x = math.log(4/failure)  # Two martingale tails share failure/2.
    delta = 2*r/(levels-1)
    plans = []
    for n in [2000000,4000000,8000000]:
        mean = n*p
        spread = np.sqrt(2*mean*z)+2*z/3
        cap = np.minimum(n,np.ceil(mean+spread))
        lower = np.maximum(1,np.floor(mean-spread))
        h = 2*energy0+4*cap*amplitude*amplitude
        beta = p*h/(lower*(r-amplitude)**2)
        nu = (np.sqrt(2*p*(h+n*delta*delta/4)*x)+2*(r+2*amplitude)*x/3)/(lower*amplitude)
        score = beta+nu
        admissible = (score <= epsilon) & (mean > spread+1)
        indices = np.flatnonzero(admissible)
        if not len(indices):
            continue
        j = indices[int(np.argmin(mean[indices]))]
        plans.append({"method":"Ordinary active-index sparse signed regression with the original fixed ADC",
            "physical_windows":n,"ADC_levels":levels,"target_gain_radius":epsilon,
            "activity_probability":float(p[j]),"probe_amplitude":float(amplitude[j]),
            "expected_ADC_reads":float(mean[j]),"ADC_read_count_lower":int(lower[j]),
            "ADC_read_count_upper":int(cap[j]),
            "expected_incident_energy":float(mean[j]*amplitude[j]**2),
            "gain_radius_bound_on_joint_count_and_martingale_event":float(score[j]),
            "failure_probability":failure,"extra_analog_reference":False,
            "execution_scope":"Computed resource/certificate plan, not an executed source trajectory."})
    return plans


def failed_attacks():
    a, center, eta, h, r = 0.6, 0.6, 0.125, 2.0, 1.0
    digital = sum(s*(np.clip(h+s*a*eta, -r, r)-center*s*eta)/eta for s in [-1., 1.])/2
    analog = sum(s*np.clip(h+s*(a-center)*eta, -r, r)/eta for s in [-1., 1.])/2
    wrong_candidate_analog = sum(s*np.clip(h+s*a*eta, -r, r)/eta for s in [-1., 1.])/2
    return {"gain": a, "candidate_equal_to_gain": center, "old_field": h,
        "probe_amplitude": eta, "digital_residual_expected_score_at_true_gain": float(digital),
        "analog_residual_expected_score_at_true_gain": float(analog),
        "analog_expected_score_at_wrong_candidate_zero": float(wrong_candidate_analog),
        "interpretation": "Digital subtraction cannot remove clipping bias; analog zero score alone cannot distinguish a correct candidate from a saturated uninformative memory field."}


def reference_calibration_twins(horizon=256, rho=0.02):
    rng = np.random.default_rng(9821)
    gains = [-rho, rho]  # Static reciprocal passive attenuators, no memory.
    reference_errors = [-rho, rho]
    records = [[], []]
    raw_max_difference = 0.0
    previous = 0.0
    for _ in range(horizon):
        u = .7*math.tanh(float(rng.normal()))
        candidate = math.tanh(previous)
        coin = float(rng.random())
        raws = []
        for j in range(2):
            y = gains[j]*u
            raws.append(y)
            centered = y-(candidate+reference_errors[j])*u
            q, warning = first.adc(centered, coin)
            records[j].append([q, warning])
        previous = records[0][-1][0]
        raw_max_difference = max(raw_max_difference, abs(raws[0]-raws[1]))
    radius = .4*rho/(rho*rho+.5)
    return {"physical_windows_replayed": horizon, "passive_state_dimension_per_instance": 0,
        "initial_stored_energy": 0.0, "physical_gains": [-rho, rho],
        "unknown_coherent_reference_gain_errors": reference_errors,
        "identical_centered_ADC_values_and_flags": records[0] == records[1],
        "raw_unprovided_signal_max_difference": raw_max_difference,
        "opposite_task_optima": [-radius, radius], "unavoidable_command_radius": radius,
        "indistinguishability_horizon": "All finite or infinite interrogation sequences under the stated centered-only observation contract, not just the numerical replay.",
        "oracle_scope": "Centered-only receiver with unknown input-coherent reference leakage. A separately calibrated reference-bypass channel or leakage measurement is an additional operation and removes this exact equivalence."}


def confidence_set_geometry_checks():
    rng = np.random.default_rng(888)
    worst = 0.0
    for _ in range(100000):
        width = float(rng.uniform(.001, 2))
        left = float(rng.uniform(-1, 1-width))
        interval = (left, left+width)
        a = float(rng.uniform(*interval))
        beta = float(rng.uniform(0, .49))
        error = float(rng.uniform(0, width*(1-2*beta)/4))
        tau = float(rng.uniform(1-beta, 1))
        score = (a-sum(interval)/2)*tau+float(rng.uniform(-error, error))
        ci, progress = candidate_ci(score, width, beta, error, interval)
        assert progress and ci[0]-1e-12 <= a <= ci[1]+1e-12
        worst = max(worst, (ci[1]-ci[0])/width)
    return {"random_geometric_confidence_checks": 100000,
        "largest_returned_width_fraction": worst}


def analytic_deadline_checks():
    rng = np.random.default_rng(42991)
    worst_fraction = 0.0
    for _ in range(1000):
        stages = int(rng.integers(1,13))
        epsilon = 2.0**(-stages)
        rho = epsilon/32
        eta = float(np.exp(rng.uniform(math.log(.005),math.log(.125))))
        failure = float(10**rng.uniform(-8,-1))
        energy0 = float(10**rng.uniform(-4,4))
        x = math.log(2*stages/failure)
        n1 = math.ceil(max(128*energy0,1024*x/(eta*eta),1))
        energy = energy0
        total = 0
        for k in range(stages):
            n = 4**k*n1
            constants = block_constants(n,energy,2.0**(1-k),eta,rho,2,failure/stages)
            assert constants["positive_progress"]
            worst_fraction = max(worst_fraction,constants["total_score_error"]/constants["half_width_progress_threshold"])
            total += n
            energy += n*eta*eta
        assert total < 4*n1/(3*epsilon*epsilon)
    return {"random_analytic_budget_parameter_checks":1000,
        "largest_score_error_over_allowed_progress_threshold":worst_fraction,
        "scope":"Numerical validation of the closed analytic budget over varied parameters, not executed physical windows."}


def main():
    grid = np.geomspace(.0001, .49, 20000)
    comparisons = [fixed_adc_budget(e, levels, grid)
        for levels in [2,257] for e in [.125,.0625,.03125,.015625]]
    # Main gains span near-zero, a moderate positive value, negative gain and a
    # long delay. Exactly the same four gain values as in the first tranche.
    cases = [(0.01,1), (.3,1), (-.6,127), (.95,32768)]
    runs = [simulate_centered(a,d,seed=300+i) for i,(a,d) in enumerate(cases)]
    plans = []
    for levels in [2,257]:
        for target in [.125,.0625,.03125,.015625]:
            blocks, rho = planned_blocks(target,.075,levels)
            n = sum(b["physical_windows"] for b in blocks)
            plans.append({"ADC_levels":levels, "target_gain_radius":target,
                "physical_windows_and_scalar_reads":n,"probe_amplitude":.075,
                "incident_energy":n*.075**2,"reference_gain_error_bound":rho,
                "reference_DAC_levels":math.ceil(2/rho)+1,
                "reference_analog_step":rho*.075})
    result = {"changed_mechanism": "Subtract a calibrated signed candidate response before the clipping element; use ordinary interval identification with passivity-charged sensitivity.",
        "failed_attacks":failed_attacks(),
        "centered_reference_main_runs":runs,
        "fixed_ADC_certificate_comparators":comparisons,
        "ordinary_sparse_fixed_ADC_resource_tradeoffs":sparse_fixed_adc_pareto(),
        "centered_reference_deterministic_budget_curves":plans,
        "reference_calibration_indistinguishable_twins":reference_calibration_twins(),
        "confidence_set_geometry":confidence_set_geometry_checks(),
        "analytic_deadline_checks":analytic_deadline_checks(),
        "scope": "No claim of a separation from ordinary methods with the same analog-reference operation; the estimator itself is ordinary interval identification. No optimality claim for the original fixed-ADC oracle. Mathematical normalized scattering model only."}
    target = HERE/"CENTERED_RESULTS.json"
    target.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"results":str(target),
        "main_window_counts":[r["calendar_and_physical_windows"] for r in runs],
        "main_gain_radii":[r["controller_gain_radius"] for r in runs],
        "main_task_radii":[r["controller_task_certificate"]["certified_distance_radius"] for r in runs],
        "all_main_coverage":all(r["task_coverage_for_audit_only"] for r in runs),
        "all_stages_progressed":all(s["half_width_progress"] for r in runs for s in r["stages"]),
        "reference_twins_identical":result["reference_calibration_indistinguishable_twins"]["identical_centered_ADC_values_and_flags"]},indent=2))


if __name__ == "__main__":
    main()
