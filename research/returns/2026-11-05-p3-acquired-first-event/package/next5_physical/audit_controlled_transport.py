"""Audits for the controlled equilibrium transport construction.

The analytic proof is in CONTROLLED_TRANSPORT.md. This program checks its
identities and evaluates a finite-slew, two-endpoint diagnostic. Gaussian
draws are synthetic statistics, not physical or full SDE executions.
"""
from pathlib import Path
import json
import math
import time

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent
mp.mp.dps = 80


def spectral(a, mobility):
    a, mobility = mp.mpf(a), mp.mpf(mobility)
    lam = a / (mobility - 1)
    disc = mp.sqrt((1 - lam) ** 2 + 4 * lam * a)
    rp = (1 + lam + disc) / (2 * (1 - a))
    # Product identity avoids subtracting nearly equal numbers.
    rm = lam / ((1 - a) * rp)
    wm = (rp - 1) / (rp - rm)
    return lam, [(1 - wm, rp), (wm, rm)]


def one_mode_pulse(rate, amplitude, ramp, total):
    """Exactly integrated affine-input segments, evaluated at 80 digits."""
    r, u, h, T = map(mp.mpf, (rate, amplitude, ramp, total))
    z = mp.mpf(0)
    displacement = mp.mpf(0)
    work = mp.mpf(0)
    segments = [(h, mp.mpf(0), u / h),
                (T - 2 * h, u, mp.mpf(0)),
                (h, u, -u / h)]
    for length, start, slope in segments:
        er = mp.exp(-r * length)
        i0 = -mp.expm1(-r * length) / r
        i1 = (-mp.expm1(-r * length) - r * length * er) / r**2
        aa = z - start / r + slope / r**2
        bb = start / r - slope / r**2
        dd = slope / r
        integral = aa * i0 + bb * length + dd * length**2 / 2
        t_integral = aa * i1 + bb * length**2 / 2 + dd * length**3 / 3
        displacement += integral
        work += start * integral + slope * t_integral
        z = aa * er + bb + dd * length
    variance = 2 * (T / r + mp.expm1(-r * T) / r**2)
    return displacement, work, variance, z


def pulse(modes, amplitude, ramp, total):
    vals = [mp.mpf(0)] * 4
    for weight, rate in modes:
        item = one_mode_pulse(rate, amplitude, ramp, total)
        vals = [x + weight * y for x, y in zip(vals, item)]
    return vals


def symbolic_checks():
    rho, lam = sp.symbols("rho lam", positive=True)
    S = sp.Matrix([[1, rho], [rho, 1]])
    Q = sp.diag(1, lam)
    A = Q * S.inv()
    e = sp.Matrix([1, 0])
    c = S * e
    M = S.inv()
    G = M * Q * M
    assert sp.simplify(A * S + S * A.T - 2 * Q) == sp.zeros(2)
    assert sp.simplify(S * G * S - Q) == sp.zeros(2)
    assert sp.simplify((e.T * A.inv() * S * e)[0] - 1 - rho**2 / lam) == 0
    ctr = sp.simplify(sp.Matrix.hstack(c, A * c).det())
    obs = sp.simplify(sp.Matrix.vstack(e.T, e.T * A).det())
    tr = sp.simplify(sp.trace(Q * (S.inv() - 2 * sp.eye(2) + S)))
    assert ctr == -rho
    assert sp.simplify(obs + rho / (1 - rho**2)) == 0
    assert sp.simplify(tr - (1 + lam) * rho**2 / (1 - rho**2)) == 0
    return {"lyapunov": True, "physical_force_noise_realization": True,
            "transport": str(1 + rho**2 / lam),
            "controllability_determinant": str(ctr),
            "observability_determinant": str(obs),
            "stationary_Girsanov_integrand": str(tr)}


def inequality_checks():
    maximum_kernel_ratio = 0.0
    maximum_weight_ratio = 0.0
    minimum_correlation_ratio = math.inf
    cases = 0
    for aval in [1e-8, 1e-6, 1e-4, .01, .1, .25]:
        rho = math.sqrt(aval)
        for mobility in [2, 3, 10, 1000, 1e8]:
            lam, modes = spectral(str(aval), str(mobility))
            lam = float(lam)
            S = np.array([[1., rho], [rho, 1.]])
            Q = np.diag([1., lam])
            A = Q @ np.linalg.inv(S)
            BB = np.diag([1., math.sqrt(lam)]) @ (np.linalg.inv(S) - np.eye(2))
            c = S[:, 0]
            for t in [0., .01, .1, 1., 4., 20., 100., 1 / max(lam, 1e-300)]:
                val = np.linalg.norm(BB @ expm(-A * t) @ c)
                maximum_kernel_ratio = max(maximum_kernel_ratio, val / (2 * aval))
                assert val <= 2 * aval * (1 + 2e-6)
                cases += 1
            wm = float(modes[1][0])
            maximum_weight_ratio = max(maximum_weight_ratio, wm / (2 * aval))
            assert aval * (1 - 1e-9) <= wm <= 2 * aval * (1 + 1e-9)
            # The lower correlation bound needs 4<=t<=1/(2a).
            if 4 <= 1 / (2 * aval):
                for t in np.linspace(4., min(1000., 1 / (2 * aval)), 17):
                    tt = mp.mpf(float(t))
                    cc = sum(w * mp.exp(-r * tt) for w, r in modes)
                    gap = cc - mp.exp(-tt)
                    ratio = float(gap / mp.mpf(str(aval)))
                    minimum_correlation_ratio = min(minimum_correlation_ratio, ratio)
                    assert ratio >= .25 - 1e-10
    return {"kernel_cases": cases, "max_kernel_over_2a": maximum_kernel_ratio,
            "max_slow_weight_over_2a": maximum_weight_ratio,
            "min_correlation_difference_over_a_in_claimed_range":
                minimum_correlation_ratio}


def main():
    began = time.perf_counter()
    a, M = mp.mpf("0.0001"), mp.mpf(1000)
    U, h, T = mp.mpf(10), mp.mpf(1), mp.mpf(800)
    lam, modes = spectral(a, M)
    base = pulse([(mp.mpf(1), mp.mpf(1))], U, h, T)
    alt = pulse(modes, U, h, T)
    m0, work0, v0, j0 = base
    m1, work1, v1, j1 = alt
    gap = m1 - m0
    threshold = (m0 + m1) / 2
    sigma = mp.mpf(".25")  # standard deviation of each endpoint readout
    adc_step = mp.mpf(".01")
    force_error = mp.mpf(".0001")
    timing_radius = mp.mpf(".0001")  # each gate/time error is within this window
    timing_displacement_allowance = mp.mpf(1)
    meter_total_bias = mp.mpf(".01")
    threshold_error = mp.mpf("1e-8")
    # Two independent meter noises appear in the difference.
    varmax = max(v0, v1) + 2 * sigma**2
    mean_force_error = force_error * max(v0, v1) / 2
    bounded_error = (mean_force_error + adc_step + meter_total_bias
                     + timing_displacement_allowance + threshold_error)
    # Handles both endpoint windows: at the first, the force is zero, and
    # at the final window the current mean is bounded by U[1+2a(T+radius)].
    timing_failure = (2 * timing_radius * (2 + (U + force_error) * (1 + 2 * a * (T + 2 * timing_radius)))
                      / timing_displacement_allowance)
    separation = gap / 2 - bounded_error
    chernoff = mp.exp(-separation**2 / (2 * varmax))
    display_range = mp.mpf(12000)
    satmargin = display_range - max(abs(m0), abs(m1)) - mean_force_error - 2 - meter_total_bias - adc_step
    saturation_failure = 4 * mp.exp(-satmargin**2 / (2 * varmax))
    total_error_bound = timing_failure + chernoff + saturation_failure
    assert total_error_bound < mp.mpf(".01")
    # This is a diagnostic evaluation, not a certified interval calculation.
    nominal_err0 = mp.erfc((threshold - m0) / mp.sqrt(2 * (v0 + 2 * sigma**2))) / 2
    nominal_err1 = mp.erfc((m1 - threshold) / mp.sqrt(2 * (v1 + 2 * sigma**2))) / 2
    seed = 2026110505
    rng = np.random.default_rng(seed)
    n = 100_000
    samples0 = rng.normal(float(m0), math.sqrt(float(v0 + 2 * sigma**2)), n)
    samples1 = rng.normal(float(m1), math.sqrt(float(v1 + 2 * sigma**2)), n)
    samples0 = np.round(samples0 / float(adc_step)) * float(adc_step)
    samples1 = np.round(samples1 / float(adc_step)) * float(adc_step)
    errors0 = int(np.count_nonzero(samples0 > float(threshold)))
    errors1 = int(np.count_nonzero(samples1 <= float(threshold)))
    inclusive_time = T + 4 * timing_radius + mp.mpf('.02')
    klpassive = -mp.log(1 - a) / 2 + inclusive_time * (1 + lam) * a / (4 * (1 - a))
    passive_tv_upper = mp.sqrt(klpassive / 2)
    effort = U**2 * (T - 4 * h / 3)
    actual_effort_bound = effort + 2 * force_error * U * (T - h) + force_error**2 * T
    controlled_kl_bound = a * (1 + T) + a**2 * effort * T**2
    conservative_T = (mp.mpf(131072) * mp.log(100) / (U**2 * a**2))**(mp.mpf(1) / 3)
    expected_absolute_work_upper = (max(work0, work1) + force_error * max(m0, m1)
                                    + force_error * (U + force_error) * max(v0, v1) / 2
                                    + U * (T - h) + force_error * T)
    battery_capacity_sufficient = mp.mpf("100000000")
    battery_abort_budget = expected_absolute_work_upper / battery_capacity_sufficient

    # An example at the same budgets that remains hidden but has much larger K.
    a_hidden, M_hidden = mp.mpf("1e-10"), mp.mpf("1e9")
    hidden_kl = a_hidden * (1 + inclusive_time) + a_hidden**2 * actual_effort_bound * inclusive_time**2
    result = {
        "status": "analytic_identities_and_diagnostic_checks_passed",
        "symbolic": symbolic_checks(),
        "inequality_diagnostics": inequality_checks(),
        "model": {"a": str(a), "rho": str(mp.sqrt(a)), "lambda": str(lam),
                  "true_transport": str(M), "reference_transport": "1",
                  "rates": [str(r) for w, r in modes],
                  "weights": [str(w) for w, r in modes],
                  "slow_relaxation_time": str(1 / modes[1][1])},
        "protocol": {"pulse_duration": str(T), "peak_force": str(U),
                     "ramp_duration": str(h), "maximum_nominal_slew": str(U / h),
                     "actual_slew_contract": "10.001",
                     "squared_force_effort": str(effort),
                     "actual_effort_upper_with_force_error": str(actual_effort_bound),
                     "two_endpoint_readouts": True,
                     "per_readout_gaussian_sigma": str(sigma),
                     "adc_step": str(adc_step), "relative_readout_range": str(display_range),
                     "bits_per_endpoint": math.ceil(math.log2(2 * float(display_range / adc_step) + 1)),
                     "gate_width_and_timing_envelope": str(timing_radius),
                     "force_calibration_envelope": str(force_error),
                     "total_meter_bias_envelope": str(meter_total_bias),
                     "readout_service_each": ".01",
                     "conservative_wall_time": "800.0204",
                     "native_stationary_preparation": "Supplied equilibrium velocity source with initial position in a unit interval about its fiducial; not physically executed or free to create.",
                     "actuator_clock_tick": ".000005",
                     "actuator_clock_counter_bits": 28,
                     "actuator_clock_ticks": 160000000,
                     "actuator_clock_total_phase_error_envelope": ".000005",
                     "clock_condition": "A calibrated total phase bound is supplied; a bit counter alone does not establish this bound."},
        "pulse_reference": {"mean_displacement": str(m0), "variance_displacement": str(v0),
                            "mean_work": str(work0), "work_variance": str(2 * work0),
                            "terminal_mean_current": str(j0)},
        "pulse_alternative": {"mean_displacement": str(m1), "variance_displacement": str(v1),
                              "mean_work": str(work1), "work_variance": str(2 * work1),
                              "terminal_mean_current": str(j1)},
        "decision": {"mean_separation": str(gap), "threshold": str(threshold),
                     "nominal_error_reference": str(nominal_err0),
                     "nominal_error_alternative": str(nominal_err1),
                     "bounded_displacement_error": str(bounded_error),
                     "timing_failure_bound": str(timing_failure),
                     "gaussian_chernoff_bound": str(chernoff),
                     "saturation_failure_bound": str(saturation_failure),
                     "combined_error_bound_numerically_evaluated": str(total_error_bound),
                     "conservative_theorem_duration_for_1_percent_error": str(conservative_T)},
        "work_reserve": {
            "expected_absolute_mechanical_work_upper": str(expected_absolute_work_upper),
            "battery_abort_probability_budget": str(battery_abort_budget),
            "sufficient_absolute_work_reserve": str(battery_capacity_sufficient),
            "limitation": "Conservative Markov bound; acquisition and controller electronics are additional."},
        "passive_comparison": {"continuous_current_observation_duration": str(inclusive_time),
                               "full_path_kl_upper": str(klpassive),
                               "record_tv_upper": str(passive_tv_upper),
                               "minimum_possible_max_testing_error_lower": str((1 - passive_tv_upper) / 2)},
        "controlled_information_bound": str(controlled_kl_bound),
        "undetectable_at_same_budget": {
            "inclusive_time_budget": str(inclusive_time),
            "actual_force_effort_upper": str(actual_effort_bound),
            "a": str(a_hidden), "transport": str(M_hidden),
            "lambda": str(a_hidden / (M_hidden - 1)),
            "all_adaptive_force_protocol_kl_upper": str(hidden_kl),
            "all_record_tv_upper": str(mp.sqrt(hidden_kl / 2))},
        "synthetic_execution": {
            "seed": seed, "draws_per_hypothesis": n,
            "reference_errors": errors0, "alternative_errors": errors1,
            "reference_error_fraction": errors0 / n, "alternative_error_fraction": errors1 / n,
            "what_was_generated": "One-dimensional exact-model Gaussian displacement plus combined endpoint Gaussian noise; the subtracted statistic is quantized once. Separate endpoint ADCs are bounded in the certificate, not simulated. No physical trials or full SDE histories."},
        "limitations": [
            "The analytic theorem is primary; mpmath values and random draws are numerical diagnostics.",
            "The finite pulse tests the specified pair; it is not a uniform upper estimator of transport.",
            "Known hypothesis models determine the threshold. Actual model identity is unknown.",
            "Native equilibrium velocity initialization is supplied. Generic preparation may pay inverse slow rate.",
            "Finite detector and force specifications are assumed calibrated; no instrument factory was built.",
            "A microscopic finite bath implementation and electronics energy are not modeled.",
            "No historical firstness claim against the system-identification literature."],
    }
    result["execution_seconds"] = time.perf_counter() - began
    (ROOT / "audit_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "T": float(T), "mean_separation": float(gap),
        "error_bound": float(total_error_bound),
        "nominal_errors": [float(nominal_err0), float(nominal_err1)],
        "empirical_errors": [errors0 / n, errors1 / n],
        "passive_testing_error_lower": float((1 - passive_tv_upper) / 2),
        "hidden_alternative_TV_upper": float(mp.sqrt(hidden_kl / 2)),
        "mean_work_max": float(max(work0, work1)),
        "seconds": result["execution_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
