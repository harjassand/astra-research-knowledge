#!/usr/bin/env python3
"""Finite arithmetic example for a controlled double-well metastability model.

This computes the exact stationary points/barrier heights for
V_q(x)=(x^2-1)^2/4-q*x and evaluates the Eyring--Kramers approximation.
It also evaluates the first-order timing-susceptibility kernel on the
uncontrolled uphill instanton and a confidence-adjusted L2 pulse budget.

The output is a model calculation, not biological data or a validation of
the Kramers approximation at the chosen numerical noise level.
"""

from __future__ import annotations

import json
import math
from pulse_policy import design_matched_pulse


def potential(x: float, q: float) -> float:
    return 0.25 * (x * x - 1.0) ** 2 - q * x


def potential_second(x: float) -> float:
    return 3.0 * x * x - 1.0


def bisect_root(f, a: float, b: float, iterations: int = 100) -> float:
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("root not bracketed")
    for _ in range(iterations):
        m = (a + b) / 2.0
        fm = f(m)
        if fa * fm <= 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return (a + b) / 2.0


def critical_points(q: float) -> tuple[float, float, float]:
    # V'_q(x)=x^3-x-q. Three roots exist for q below the positive spinodal.
    f = lambda x: x**3 - x - q
    c = 1.0 / math.sqrt(3.0)
    left = bisect_root(f, -1.5, -c)
    saddle = bisect_root(f, -c, c)
    right = bisect_root(f, c, 1.5)
    return left, saddle, right


def barrier_and_prefactor(q: float, epsilon: float) -> dict[str, float]:
    left, saddle, right = critical_points(q)
    barrier = potential(saddle, q) - potential(left, q)
    prefactor = math.sqrt(potential_second(left) * abs(potential_second(saddle))) / (2.0 * math.pi)
    rate = prefactor * math.exp(-barrier / epsilon)
    return {
        "dose": q,
        "source_minimum": left,
        "saddle": saddle,
        "target_minimum": right,
        "barrier": barrier,
        "prefactor": prefactor,
        "kramers_rate": rate,
        "kramers_mean_wait": 1.0 / rate,
    }


def trapezoid(values: list[float], step: float) -> float:
    if len(values) < 2:
        return 0.0
    return step * (0.5 * values[0] + sum(values[1:-1]) + 0.5 * values[-1])


def main() -> None:
    epsilon = 0.05
    dose_grid = [0.0, 0.025, 0.05, 0.075, 0.10]
    dose_rows = [barrier_and_prefactor(q, epsilon) for q in dose_grid]

    # Uncontrolled uphill instanton x(t)=-1/sqrt(1+exp(2t));
    # kappa(t)=V'(x(t)) for a unit additive drift control.
    horizon = 8.0
    bins = 401
    step = 2.0 * horizon / (bins - 1)
    times = [-horizon + j * step for j in range(bins)]
    kappa = []
    for t in times:
        y = 1.0 / (1.0 + math.exp(2.0 * t))
        x = -math.sqrt(y)
        kappa.append(x**3 - x)
    norm2 = trapezoid([v * v for v in kappa], step)
    norm = math.sqrt(norm2)

    implemented_policy = design_matched_pulse(
        times,
        kappa,
        observation_sigma=0.05,
        observations_per_bin=58,
        observation_alpha=0.025,
        dose_energy=0.01,
        required_action_decrease=0.05,
        actuator_gain_sigma=0.05,
        actuator_z=1.959963984540054,
        timing_jitter_sigma=0.20,
        endpoint_sensitivity=0.90,
        endpoint_specificity=0.95,
        endpoint_delta=0.05,
    )

    # A transparent synthetic acquisition/control-noise budget.
    # Each time-bin kernel estimate is sub-Gaussian with sigma=0.05 per cell.
    # Simultaneous error <= delta with probability 1-alpha_obs.
    sigma_obs = 0.05
    delta_kappa = 0.03
    alpha_obs = 0.025
    observations_per_bin = math.ceil(
        2.0 * sigma_obs**2 / delta_kappa**2 * math.log(2.0 * bins / alpha_obs)
    )
    kappa_lower = [max(v - delta_kappa, 0.0) for v in kappa]
    lower_norm = math.sqrt(trapezoid([v * v for v in kappa_lower], step))

    # Sustained-dose Kramers calculation: find the constant concentration that
    # gives a 1/2 transition probability by T=100.
    target_probability = 0.5
    pulse_horizon = 100.0
    base = barrier_and_prefactor(0.0, epsilon)
    target_rate = -math.log(1.0 - target_probability) / pulse_horizon
    low, high = 0.0, 0.20
    for _ in range(100):
        q = (low + high) / 2.0
        if barrier_and_prefactor(q, epsilon)["kramers_rate"] < target_rate:
            low = q
        else:
            high = q
    q_half = (low + high) / 2.0

    # Separate finite-horizon action-kernel example. A path-matched pulse is
    # compared with a uniform pulse over the same 16-unit window, both at the
    # same L2 control energy, for a local first-order action decrease R=0.05.
    required_action_decrease = 0.05
    window = 2.0 * horizon
    integral_lower = trapezoid(kappa_lower, step)
    matched_nominal_energy = (required_action_decrease / norm) ** 2
    uniform_nominal_energy = (
        required_action_decrease * math.sqrt(window) / trapezoid(kappa, step)
    ) ** 2

    # Independent multiplicative actuator gain error eta~N(0,sigma_act^2).
    # A one-sided normal confidence bound multiplies the nominal action gain by
    # (1-z*sigma_act). The same measured kernel lower bound is used throughout.
    sigma_act = 0.05
    alpha_control = 0.025
    z_one_sided = 1.959963984540054
    actuator_gain_lcb = 1.0 - z_one_sided * sigma_act
    # Analytic for this double well: integral (d kappa/dt)^2 dt = 1/2,
    # integral kappa^2 dt = 1/4. Small Gaussian timing jitter loses the fraction
    # sigma_t^2 * ||kappa'||^2/(2||kappa||^2) to second order.
    timing_jitter_sd = 0.20
    kappa_derivative_norm2 = 0.5
    timing_gain_factor = 1.0 - timing_jitter_sd**2 * kappa_derivative_norm2 / (2.0 * norm2)
    # Use the pulse-policy implementation's timing factor, estimated directly
    # from the lower-confidence kernel. The analytic raw-kernel timing factor
    # above is reported separately and is not mixed with this lower-kernel norm.
    matched_robust_energy = implemented_policy[
        "required_energy_after_amplitude_lcb_and_mean_timing_adjustment"
    ]
    uniform_robust_energy = (
        required_action_decrease * math.sqrt(window)
        / (integral_lower * actuator_gain_lcb)
    ) ** 2

    # Endpoint assay cost: sensitivity .90, specificity .95, 5-point precision.
    sensitivity, specificity = 0.90, 0.95
    endpoint_margin = sensitivity + specificity - 1.0
    endpoint_delta = 0.05
    alpha_endpoint = 0.05
    endpoint_cells = math.ceil(
        math.log(2.0 / alpha_endpoint)
        / (2.0 * endpoint_margin**2 * endpoint_delta**2)
    )

    result = {
        "status": "finite model calculation; not biological validation",
        "potential": "V_q(x)=(x^2-1)^2/4-q*x",
        "noise_scale_epsilon": epsilon,
        "constant_dose_rows": dose_rows,
        "constant_dose_for_half_commitment_by_horizon": {
            "dose": q_half,
            "barrier": barrier_and_prefactor(q_half, epsilon)["barrier"],
            "kramers_rate": barrier_and_prefactor(q_half, epsilon)["kramers_rate"],
            "predicted_commitment_probability": 1.0 - math.exp(-pulse_horizon * barrier_and_prefactor(q_half, epsilon)["kramers_rate"]),
            "horizon": pulse_horizon,
        },
        "uncontrolled_instanton_l2_susceptibility_norm": norm,
        "analytic_uncontrolled_norm": 0.5,
        "simultaneous_kernel_lower_norm": lower_norm,
        "kernel_observations_per_time_bin": observations_per_bin,
        "total_kernel_reads": observations_per_bin * bins,
        "observation_confidence": 1.0 - alpha_obs,
        "actuator_relative_gain_sigma": sigma_act,
        "actuator_confidence": 1.0 - alpha_control,
        "timing_jitter_sd": timing_jitter_sd,
        "analytic_kappa_derivative_norm2": kappa_derivative_norm2,
        "analytic_uncontrolled_small_jitter_action_gain_factor": timing_gain_factor,
        "first_order_path_matched_pulse": {
            "target_action_decrease": required_action_decrease,
            "window": window,
            "uniform_kernel_integral": trapezoid(kappa, step),
            "lower_confidence_kernel_integral": integral_lower,
            "nominal_l2_energy_path_matched": matched_nominal_energy,
            "nominal_l2_energy_uniform_same_window": uniform_nominal_energy,
            "lower_kernel_pulse_policy_energy_after_gain_and_mean_timing_debits": matched_robust_energy,
            "amplitude_lcb_only_uniform_lower_kernel_energy_no_timing_debit": uniform_robust_energy,
            "timing_correction_status": "second-order expected-gain approximation, not a high-confidence lower bound",
        },
        "endpoint_assay": {
            "sensitivity": sensitivity,
            "specificity": specificity,
            "probability_precision": endpoint_delta,
            "confidence": 1.0 - alpha_endpoint,
            "independent_cells_required": endpoint_cells,
        },
        "implemented_policy_summary": {
            "lineage_observations": implemented_policy["lineage_observations"],
            "lower_kernel_l2_norm": implemented_policy["lower_kernel_l2_norm"],
            "action_decrease_at_requested_energy": implemented_policy["nominal_action_decrease_at_requested_energy"],
            "adjusted_action_decrease": implemented_policy["action_decrease_after_amplitude_lcb_and_mean_timing_adjustment"],
            "required_energy_for_action_decrease": implemented_policy["required_energy_after_amplitude_lcb_and_mean_timing_adjustment"],
            "endpoint_cells_for_precision": implemented_policy["endpoint_cells_for_precision"],
        },
        "warning": "Kramers and first-order action approximations require small noise, a unique nondegenerate escape path, and weak control; the chosen values only illustrate the arithmetic. Timing-jitter correction is an expected-gain approximation, not a confidence guarantee.",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
