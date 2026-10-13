#!/usr/bin/env python3
"""Small exact-formula arithmetic for the defensive-mixture bound.

No trajectories are simulated.  The input p_scale is a planning scale inherited
from the reported estimate, not a newly certified target value.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


P_SCALE = 4.304224792713203e-10
DELTA = 0.05
REL_TOL = 0.10
DT = 0.0005
HORIZON = 2.0
TOTAL_FORCE_BUDGET = 20_838_768
ACQUISITION_FORCE_POINTS = 19_400_000
OBSERVED_GUIDE_FORCE_POINTS = 1_438_768
N_STEPS_MAX = round(HORIZON / DT)


def bernstein_ci_at_mean(x: float, n: int, epsilon: float,
                         delta: float = DELTA) -> tuple[float, float]:
    """Two-sided Bernstein CI for mean of iid Y in [0,1/epsilon].

    Uses Var(Y) <= E[Y^2] <= E[Y]/epsilon.  The displayed x is the observed
    sample mean; this function does not generate observations.
    """
    if n <= 0 or not (0.0 < epsilon <= 1.0) or not (0.0 < delta < 1.0):
        raise ValueError("require n>0, 0<epsilon<=1, and 0<delta<1")
    M = 1.0 / epsilon
    L = math.log(2.0 / delta)  # two tails, delta/2 each
    a = 2.0 * M * L / n
    c = math.sqrt(a)
    b = 2.0 * M * L / (3.0 * n)

    # Invert x >= mu - sqrt(a*mu) - b for an upper endpoint.
    upper = ((c + math.sqrt(c*c + 4.0*(x+b))) / 2.0) ** 2
    # Invert x <= mu + sqrt(a*mu) + b for a lower endpoint.
    if x <= b:
        lower = 0.0
    else:
        lower = ((math.sqrt(c*c + 4.0*(x-b)) - c) / 2.0) ** 2
    return lower, upper


def bernstein_n_required(p: float = P_SCALE, rel_tol: float = REL_TOL,
                         epsilon: float = 1.0,
                         delta: float = DELTA) -> int:
    """Sufficient n for the two-sided Bernstein radius <= rel_tol*p.

    Put t=epsilon*n*p and s=sqrt(2L/t); the relative radius is
    s+s^2/3.  Solve this quadratic for s, then round n upwards.
    """
    L = math.log(2.0 / delta)
    s = (math.sqrt(9.0 + 12.0*rel_tol) - 3.0) / 2.0
    t = 2.0*L/(s*s)
    return math.ceil(t/(epsilon*p))


def main() -> None:
    n_after_acquisition_worst = (
        TOTAL_FORCE_BUDGET - ACQUISITION_FORCE_POINTS
    ) // N_STEPS_MAX
    n_total_worst = TOTAL_FORCE_BUDGET // N_STEPS_MAX
    n_req_eps1 = bernstein_n_required()
    effective_count_required = n_req_eps1*P_SCALE
    coupling_lower_bound_paths = math.ceil((1.0-2.0*DELTA)/(3.0*REL_TOL*P_SCALE))
    L = math.log(2.0/DELTA)
    doob_sample_cases = []
    for n in (359, 10_000):
        variance_ratio_cap = n / effective_count_required
        log_envelope_cap = 0.5*math.log(variance_ratio_cap) if variance_ratio_cap >= 1.0 else None
        doob_sample_cases.append({
            "n": n,
            "maximum_R_for_Bernstein_10pct_95pct": variance_ratio_cap,
            "maximum_log_path_envelope_h_if_R_equals_exp_2h": log_envelope_cap,
            "maximum_uniform_log_residual_per_step_over_4000_steps": (
                log_envelope_cap/N_STEPS_MAX if log_envelope_cap is not None else None
            ),
        })
    finite_example_epsilon = 0.1
    finite_example_qc_event = 0.5
    finite_example_event_scale_C = 1.0/((1.0-finite_example_epsilon)*finite_example_qc_event)
    finite_example_relative_radius = (
        math.sqrt(2.0*finite_example_event_scale_C*L/10_000)
        + 2.0*finite_example_event_scale_C*L/(3.0*10_000)
    )
    table = []
    for n, label in [
        (n_after_acquisition_worst, "remaining budget after 19.4M acquisition; 4000-step cap"),
        (n_total_worst, "entire budget, no acquisition; 4000-step cap"),
        (10_000, "same count as inherited guided paths; hypothetical Q-mixture data"),
        (OBSERVED_GUIDE_FORCE_POINTS, "optimistic one iid sample per remaining force point (impossible accounting)") ,
        (TOTAL_FORCE_BUDGET, "optimistic one iid sample per total force point (impossible accounting)"),
    ]:
        for eps in (1.0, 0.1, 0.01):
            lo, hi = bernstein_ci_at_mean(P_SCALE, n, eps)
            table.append({
                "case": label,
                "n": n,
                "epsilon": eps,
                "illustrative_observed_mean": P_SCALE,
                "lower": lo,
                "upper": hi,
                "upper_over_p_scale": hi/P_SCALE,
                "empirical_bernstein_range_term_scale": (
                    7.0*(1.0/eps)*math.log(2.0/DELTA)/(3.0*max(1, n-1))
                ),
            })

    # The global-mixture M=1/epsilon bound is best at epsilon=1.  A stepwise
    # mixture compounds M across at most N_STEPS_MAX transitions.
    result = {
        "status": "ARITHMETIC_ONLY_NO_SIMULATION",
        "p_scale_not_certified_truth": P_SCALE,
        "delta": DELTA,
        "relative_tolerance": REL_TOL,
        "dt": DT,
        "horizon": HORIZON,
        "maximum_euler_steps_per_stopped_path": N_STEPS_MAX,
        "total_force_budget": TOTAL_FORCE_BUDGET,
        "acquisition_force_points": ACQUISITION_FORCE_POINTS,
        "remaining_force_points_after_acquisition": TOTAL_FORCE_BUDGET-ACQUISITION_FORCE_POINTS,
        "worst_case_paths_from_remaining_budget": n_after_acquisition_worst,
        "worst_case_paths_from_total_budget_without_acquisition": n_total_worst,
        "two_sided_bernstein_sufficient_paths_at_epsilon_1": n_req_eps1,
        "two_sided_bernstein_sufficient_force_points_at_4000_per_path": n_req_eps1*N_STEPS_MAX,
        "two_sided_bernstein_force_factor_over_budget_at_4000_per_path": (n_req_eps1*N_STEPS_MAX)/TOTAL_FORCE_BUDGET,
        "epsilon_scaled_effective_sample_requirement": "n*epsilon*p_scale >= " + str(effective_count_required),
        "distribution_free_rare_spike_coupling_lower_bound_paths_at_epsilon_1": coupling_lower_bound_paths,
        "distribution_free_rare_spike_coupling_lower_bound_over_total_force_budget": coupling_lower_bound_paths/TOTAL_FORCE_BUDGET,
        "illustrative_intervals_if_observed_mean_equals_p_scale": table,
        "stepwise_global_weight_bound_epsilon_0_1": "10^4000",
        "stepwise_log10_bound_epsilon_0_1": N_STEPS_MAX,
        "stepwise_epsilon_min_for_global_weight_cap_2": 2.0**(-1.0/N_STEPS_MAX),
        "stepwise_epsilon_min_for_global_weight_cap_10": 10.0**(-1.0/N_STEPS_MAX),
        "control_energy_H_max": 80.0**2*HORIZON,
        "gaussian_second_moment_log10_bound_for_Qc": (80.0**2*HORIZON/2.0)/math.log(10.0),
        "control_energy_log_weight_cutoff_for_0p1p_tail_bias": (
            (80.0**2*HORIZON)/4.0
            + math.sqrt((80.0**2*HORIZON)*math.log(1.0/(0.1*P_SCALE)))
        ),
        "control_energy_log10_weight_cutoff_for_0p1p_tail_bias": (
            (80.0**2*HORIZON)/4.0
            + math.sqrt((80.0**2*HORIZON)*math.log(1.0/(0.1*P_SCALE)))
        )/math.log(10.0),
        "ideal_physical_event_count_at_total_force_budget_if_one_force_point_per_sample": TOTAL_FORCE_BUDGET*P_SCALE,
        "physical_no_hit_probability_at_worst_case_5209_paths": (1.0-P_SCALE)**n_total_worst,
        "physical_no_hit_probability_at_359_paths": (1.0-P_SCALE)**n_after_acquisition_worst,
        "physical_zero_hit_95pct_exact_upper_at_359_paths": -math.expm1(math.log(DELTA)/n_after_acquisition_worst),
        "physical_zero_hit_95pct_exact_upper_at_5209_paths": -math.expm1(math.log(DELTA)/n_total_worst),
        "doob_residual_envelope_requirements": doob_sample_cases,
        "doob_deterministic_10pct_relative_enclosure_total_log_residual": math.log1p(REL_TOL),
        "doob_deterministic_10pct_relative_enclosure_per_step_over_4000_steps": math.log1p(REL_TOL)/N_STEPS_MAX,
        "finite_two_atom_event_envelope_example": {
            "target_P_event_mass": "p",
            "controlled_Qc_event_mass": finite_example_qc_event,
            "epsilon": finite_example_epsilon,
            "global_defensive_weight_bound": 1.0/finite_example_epsilon,
            "event_scaled_weight_bound_Y_over_p": finite_example_event_scale_C,
            "two_sided_Bernstein_relative_radius_at_n_10000": finite_example_relative_radius,
            "interpretation": "If an event-specific likelihood envelope Y<=C*p is proved, the range/variance certificate can be useful; the Gaussian controller has no such proved envelope.",
        },
    }
    out = Path(__file__).with_name("certificate_arithmetic.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
