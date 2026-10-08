#!/usr/bin/env python3
"""Finite three-state reach-avoid counterexample and robust dose rule.

All numbers below are synthetic model inputs. The script independently checks
the deterministic population-balance solution against RK4, and evaluates a
finite-sample, assay-noise-aware, founder-balanced two-arm decision rule.
It is not biological data or validation.
"""
from __future__ import annotations

import json
import math
from typing import Iterable


def phi(rate: float, time: float) -> float:
    """Integral_0^time exp(-rate*s) ds, stable at rate zero."""
    if abs(rate) < 1e-12:
        return time
    return -math.expm1(-rate * time) / rate


def founder_reach_probability(lam: float, mu: float, time: float) -> float:
    """P(source -> target by time before avoidance) for a single founder."""
    if lam < 0 or mu < 0 or time < 0:
        raise ValueError("rates and time must be nonnegative")
    return lam * phi(lam + mu, time)


def continuum_counts(
    lam: float,
    mu: float,
    g_source: float,
    g_target: float,
    g_avoid: float,
    time: float,
) -> tuple[float, float, float]:
    """Solve the exact three-state deterministic population-balance model.

    Source cells switch to target/avoid with hazards lam/mu. State i has net
    growth rate g_i. Returns source, target, avoid abundance from one source.
    """
    k = lam + mu
    n_source = math.exp((g_source - k) * time)
    d_target = g_target - g_source + k
    d_avoid = g_avoid - g_source + k
    n_target = lam * math.exp(g_target * time) * phi(d_target, time)
    n_avoid = mu * math.exp(g_avoid * time) * phi(d_avoid, time)
    return n_source, n_target, n_avoid


def target_fraction(counts: Iterable[float]) -> float:
    source, target, avoid = counts
    total = source + target + avoid
    return target / total if total else 0.0


def rk4_counts(
    lam: float,
    mu: float,
    g_source: float,
    g_target: float,
    g_avoid: float,
    time: float,
    steps: int = 30000,
) -> tuple[float, float, float]:
    """Independent numerical integration of the population-balance ODE."""
    k = lam + mu
    h = time / steps

    def rhs(y: tuple[float, float, float]) -> tuple[float, float, float]:
        s, r, a = y
        return (
            (g_source - k) * s,
            lam * s + g_target * r,
            mu * s + g_avoid * a,
        )

    y = (1.0, 0.0, 0.0)
    for _ in range(steps):
        k1 = rhs(y)
        y2 = tuple(y[i] + 0.5 * h * k1[i] for i in range(3))
        k2 = rhs(y2)
        y3 = tuple(y[i] + 0.5 * h * k2[i] for i in range(3))
        k3 = rhs(y3)
        y4 = tuple(y[i] + h * k3[i] for i in range(3))
        k4 = rhs(y4)
        y = tuple(
            y[i] + (h / 6.0) * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
            for i in range(3)
        )
    return y


def solve_target_growth_for_fraction(
    lam: float,
    mu: float,
    g_source: float,
    g_avoid: float,
    time: float,
    desired_fraction: float,
    lower: float = -20.0,
    upper: float = 10.0,
) -> float:
    """Bisection for g_target matching one observed bulk fraction."""

    def residual(g_target: float) -> float:
        counts = continuum_counts(
            lam, mu, g_source, g_target, g_avoid, time
        )
        return target_fraction(counts) - desired_fraction

    f_lower, f_upper = residual(lower), residual(upper)
    if f_lower * f_upper > 0:
        raise ValueError("target growth root is not bracketed")
    for _ in range(100):
        middle = 0.5 * (lower + upper)
        f_middle = residual(middle)
        if f_lower * f_middle <= 0:
            upper, f_upper = middle, f_middle
        else:
            lower, f_lower = middle, f_middle
    return 0.5 * (lower + upper)


def assay_observation_probability(
    reach_probability: float, sensitivity: float, specificity: float
) -> float:
    return (1.0 - specificity) + (
        sensitivity + specificity - 1.0
    ) * reach_probability


def hoeffding_radius(n: int, alpha_per_arm: float) -> float:
    return math.sqrt(math.log(2.0 / alpha_per_arm) / (2.0 * n))


def robust_latent_probability_interval(
    observed_mean: float,
    observation_radius: float,
    sensitivity_interval: tuple[float, float],
    specificity_interval: tuple[float, float],
) -> tuple[float, float]:
    """Invert binary assay under rectangular sensitivity/specificity bounds."""
    q_low = max(0.0, observed_mean - observation_radius)
    q_high = min(1.0, observed_mean + observation_radius)
    s_low, s_high = sensitivity_interval
    c_low, c_high = specificity_interval
    gamma_p_lower = s_high + c_low - 1.0
    gamma_p_upper = s_low + c_high - 1.0
    if gamma_p_lower <= 0 or gamma_p_upper <= 0:
        return 0.0, 1.0
    # In the interior range 1-c_high < q <= q_high < s_low, p decreases
    # in s and increases in c. Outside it, abstain rather than extrapolate.
    if q_low <= 1.0 - c_high or q_high >= s_low:
        return 0.0, 1.0
    p_low = (q_low + c_low - 1.0) / gamma_p_lower
    p_high = (q_high + c_high - 1.0) / gamma_p_upper
    return max(0.0, min(1.0, p_low)), max(0.0, min(1.0, p_high))


def robust_fixed_dose_decision(
    n: int,
    baseline_positive_count: int,
    dose_positive_count: int,
    sensitivity_interval: tuple[float, float],
    specificity_interval: tuple[float, float],
    familywise_alpha: float,
    intervention_cost_probability_units: float,
    actuation_worst_case_probability_debit: float,
) -> dict[str, float | int | bool | str]:
    """Two-arm Hoeffding controller with simultaneous confidence intervals."""
    # Split one familywise error budget across two endpoint arms, two
    # assay-calibration proportions, and the actuation certificate.
    per_arm_alpha = familywise_alpha / 5.0
    radius = hoeffding_radius(n, per_arm_alpha)
    base_mean = baseline_positive_count / n
    dose_mean = dose_positive_count / n
    base_interval = robust_latent_probability_interval(
        base_mean, radius, sensitivity_interval, specificity_interval
    )
    dose_interval = robust_latent_probability_interval(
        dose_mean, radius, sensitivity_interval, specificity_interval
    )
    raw_lower_gain = dose_interval[0] - base_interval[1]
    net_lower_gain = (
        raw_lower_gain
        - intervention_cost_probability_units
        - actuation_worst_case_probability_debit
    )
    return {
        "n_founder_lineages_per_arm": n,
        "baseline_positive_count": baseline_positive_count,
        "dose_positive_count": dose_positive_count,
        "assay_positive_mean_baseline": base_mean,
        "assay_positive_mean_dose": dose_mean,
        "simultaneous_assay_mean_radius": radius,
        "baseline_reach_probability_interval": list(base_interval),
        "dose_reach_probability_interval": list(dose_interval),
        "lower_bound_reach_probability_gain": raw_lower_gain,
        "intervention_cost_probability_units": intervention_cost_probability_units,
        "actuation_worst_case_probability_debit": actuation_worst_case_probability_debit,
        "net_lower_bound_gain": net_lower_gain,
        "apply_fixed_dose": net_lower_gain > 0.0,
        "decision": "APPLY" if net_lower_gain > 0.0 else "NO-GO / collect more data",
    }


def main() -> None:
    # Exact population-balance counterexample: founder reach probability is 0.1,
    # but target-state growth makes target cells a majority by t=3.
    p = {
        "lambda_source_to_target": 0.1,
        "mu_source_to_avoid": 0.9,
        "g_source": 0.0,
        "g_target": 1.0,
        "g_avoid": 0.0,
        "horizon": 3.0,
    }
    counts = continuum_counts(
        p["lambda_source_to_target"],
        p["mu_source_to_avoid"],
        p["g_source"],
        p["g_target"],
        p["g_avoid"],
        p["horizon"],
    )
    numeric = rk4_counts(
        p["lambda_source_to_target"],
        p["mu_source_to_avoid"],
        p["g_source"],
        p["g_target"],
        p["g_avoid"],
        p["horizon"],
    )
    bulk_fraction = target_fraction(counts)

    # A second parameter set with the opposite founder fate probability but
    # exactly the same one-time bulk target fraction.
    lambda_2, mu_2 = 0.9, 0.1
    g_target_2 = solve_target_growth_for_fraction(
        lambda_2, mu_2, 0.0, 0.0, p["horizon"], bulk_fraction
    )
    second_counts = continuum_counts(
        lambda_2, mu_2, 0.0, g_target_2, 0.0, p["horizon"]
    )
    second_bulk_fraction = target_fraction(second_counts)

    # Finite trial decision. A hidden binary reach label has calibrated assay
    # intervals; founders contribute equally so descendants do not size-bias it.
    alpha = 0.05
    sensitivity_interval = (0.88, 0.92)
    specificity_interval = (0.93, 0.97)
    calibration_radius = 0.02
    raw_calibration_per_class = math.ceil(
        math.log(2.0 / (alpha / 5.0)) / (2.0 * calibration_radius**2)
    )
    # Round to a multiple of 20 so synthetic calibration means 0.90 and 0.95
    # are represented by integer success counts without rounding the interval.
    calibration_per_class = 20 * math.ceil(raw_calibration_per_class / 20)
    arms = []
    for n, y_base, y_dose in ((500, 110, 196), (3000, 660, 1176)):
        result = robust_fixed_dose_decision(
            n=n,
            baseline_positive_count=y_base,
            dose_positive_count=y_dose,
            sensitivity_interval=sensitivity_interval,
            specificity_interval=specificity_interval,
            familywise_alpha=alpha,
            intervention_cost_probability_units=0.05,
            actuation_worst_case_probability_debit=0.02,
        )
        result["endpoint_assays"] = 2 * n
        result["assay_calibration_cells_two_classes"] = 2 * calibration_per_class
        result["total_observation_units_including_calibration"] = (
            2 * n + 2 * calibration_per_class
        )
        arms.append(result)

    output = {
        "status": "synthetic finite model arithmetic; not biological validation",
        "population_balance_model": p,
        "single_founder_reach_probability_by_horizon": founder_reach_probability(
            p["lambda_source_to_target"],
            p["mu_source_to_avoid"],
            p["horizon"],
        ),
        "continuum_population_abundances_source_target_avoid": counts,
        "rk4_independent_abundance_check": numeric,
        "maximum_closed_form_vs_rk4_absolute_error": max(
            abs(a - b) for a, b in zip(counts, numeric)
        ),
        "endpoint_bulk_target_fraction": bulk_fraction,
        "second_nonidentifiable_model": {
            "lambda_source_to_target": lambda_2,
            "mu_source_to_avoid": mu_2,
            "g_source": 0.0,
            "g_target_solved": g_target_2,
            "g_avoid": 0.0,
            "single_founder_conditional_reach_probability": lambda_2
            / (lambda_2 + mu_2),
            "continuum_abundances_source_target_avoid": second_counts,
            "endpoint_bulk_target_fraction": second_bulk_fraction,
        },
        "decision_rule_assumptions": {
            "founder_lineages_per_arm_are_independently_randomized": True,
            "each_founder_has_equal_analysis_weight": True,
            "endpoint_assay_sensitivity_interval": sensitivity_interval,
            "endpoint_assay_specificity_interval": specificity_interval,
            "familywise_confidence": 1.0 - alpha,
            "simultaneous_error_budget_components": 5,
            "calibration_radius": calibration_radius,
            "calibration_per_class_required_by_Hoeffding": calibration_per_class,
            "synthetic_gold_target_calibration_positives": round(
                0.90 * calibration_per_class
            ),
            "synthetic_gold_non_target_calibration_negatives": round(
                0.95 * calibration_per_class
            ),
            "realized_calibration_confidence_radius": hoeffding_radius(
                calibration_per_class, alpha / 5.0
            ),
            "dose_cost_probability_units": 0.05,
            "99_percent_actuation_debit_probability_units": 0.02,
            "growth_bias_control": "one vote per founder; no descendant-count weighting",
        },
        "finite_decisions": arms,
    }
    # The close fractions are computed through two independent numerical paths.
    assert output["maximum_closed_form_vs_rk4_absolute_error"] < 1e-8
    assert abs(bulk_fraction - second_bulk_fraction) < 1e-12
    assert arms[0]["apply_fixed_dose"] is False
    assert arms[1]["apply_fixed_dose"] is True
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
