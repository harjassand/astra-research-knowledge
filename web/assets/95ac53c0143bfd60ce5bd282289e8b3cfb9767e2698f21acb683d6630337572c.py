#!/usr/bin/env python3
"""Reproduce the branching clone-safety witness and finite-data design arithmetic.

This is a conditional model calculator, not a biological fit. The model is a
linear birth-death process of safe cells S: S->2S at rate b, S->0 at rate d,
and S->U at rate q. U is a persistent, nonproliferating harmful lineage mark.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


def no_harm_probability(b: float, d: float, q: float, t: float) -> float:
    """P(no U has appeared by t), using the Riccati PGF equation's roots."""
    if min(b, d, q, t) < 0 or b <= 0:
        raise ValueError("require b>0 and d,q,t >= 0")
    if q == 0 or t == 0:
        return 1.0
    disc = math.sqrt((b + d + q) ** 2 - 4 * b * d)
    r_minus = (b + d + q - disc) / (2 * b)
    r_plus = (b + d + q + disc) / (2 * b)
    c = (1 - r_minus) / (1 - r_plus)
    y = c * math.exp(-disc * t)
    return (r_minus - y * r_plus) / (1 - y)


def harm_probability(b: float, d: float, q: float, t: float) -> float:
    return 1.0 - no_harm_probability(b, d, q, t)


def expected_counts(b: float, d: float, q: float, t: float) -> tuple[float, float]:
    """Return E[S_t], E[U_t] for U persistent/nonbranching."""
    r = b - d - q
    safe = math.exp(r * t)
    if abs(r) < 1e-14:
        unsafe = q * t
    else:
        unsafe = q * math.expm1(r * t) / r
    return safe, unsafe


def pgf_no_target_no_harm(b: float, d: float, a: float, q: float,
                          t: float, x: float) -> float:
    """E[x**R_t * 1{U_t=0}] from one S founder.

    Backward equation: F'=bF^2-(b+d+a+q)F+d+a*x, F(0)=1.
    A closed Riccati solution is used except at removable singularities, where
    a high-accuracy RK4 calculation supplies an independent stable limit.
    """
    if min(b, d, a, q, t) < 0 or b <= 0 or not 0 <= x <= 1:
        raise ValueError("require b>0, d,a,q,t >= 0 and x in [0,1]")
    if q == 0 and x == 1:
        return 1.0
    K = b + d + a + q
    c0 = d + a * x
    disc_sq = K * K - 4 * b * c0
    if disc_sq <= 1e-26:
        return rk4_riccati(b, K, c0, t)
    disc = math.sqrt(disc_sq)
    r_minus = (K - disc) / (2 * b)
    r_plus = (K + disc) / (2 * b)
    den = 1 - r_plus
    if abs(den) < 1e-12:
        return rk4_riccati(b, K, c0, t)
    c = (1 - r_minus) / den
    y = c * math.exp(-disc * t)
    return (r_minus - y * r_plus) / (1 - y)


def rk4_riccati(b: float, K: float, c0: float, t: float,
                steps: int = 40000) -> float:
    dt = t / steps

    def f(z: float) -> float:
        return b * z * z - K * z + c0

    z = 1.0
    for _ in range(steps):
        k1 = f(z)
        k2 = f(z + dt * k1 / 2)
        k3 = f(z + dt * k2 / 2)
        k4 = f(z + dt * k3)
        z += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return z


def expected_three_counts(b: float, d: float, a: float, q: float,
                          t: float) -> tuple[float, float, float]:
    """Return (E[S_t], E[R_t], E[U_t]) for target/harm absorbing marks."""
    r = b - d - a - q
    safe = math.exp(r * t)
    integrated_safe = t if abs(r) < 1e-14 else math.expm1(r * t) / r
    return safe, a * integrated_safe, q * integrated_safe


def endpoint_moment_rate_inverse(mean_s: float, mean_r: float, mean_u: float,
                                 var_s: float, t: float) -> dict[str, float]:
    """Population-moment inverse for one founder-resolved terminal census.

    Assumes S->2S at b, S->0 at d, S->R at a, S->U at q, with R,U
    persistent and nonbranching. The moments are unconditional over all seeded
    founders, including zero-descendant clones.
    """
    if t <= 0 or mean_s <= 0 or min(mean_r, mean_u, var_s) < 0:
        raise ValueError("invalid endpoint moments")
    r = math.log(mean_s) / t
    if abs(r) < 1e-10:
        a = mean_r / t
        q = mean_u / t
        birth_plus_removal = var_s / t
    else:
        a = r * mean_r / (mean_s - 1)
        q = r * mean_u / (mean_s - 1)
        birth_plus_removal = var_s * r / (mean_s * (mean_s - 1))
    b = (birth_plus_removal + r) / 2
    total_removal = (birth_plus_removal - r) / 2
    d = total_removal - a - q
    return {"b": b, "d": d, "a": a, "q": q,
            "net_mean_growth_r": r,
            "birth_plus_effective_removal": birth_plus_removal}


def target_safe_probability(b: float, d: float, a: float, q: float,
                            t: float) -> float:
    """P(R_t>0 and U_t=0) from one S founder."""
    return pgf_no_target_no_harm(b, d, a, q, t, 1.0) - pgf_no_target_no_harm(
        b, d, a, q, t, 0.0
    )


def rk4_target_safe_probability(b: float, d: float, a: float, q: float,
                                 t: float) -> float:
    """Independent numerical integration of both PGF boundary equations."""
    K = b + d + a + q
    h1 = rk4_riccati(b, K, d + a, t)
    h0 = rk4_riccati(b, K, d, t)
    return h1 - h0


def extinction_probability(b: float, d: float, t: float) -> float:
    """P(S_t=0) for an ordinary linear birth-death process (q=0)."""
    if min(b, d, t) < 0 or b <= 0:
        raise ValueError("require b>0 and d,t >= 0")
    if t == 0 or d == 0:
        return 0.0
    r = b - d
    if abs(r) < 1e-14:
        return b * t / (1 + b * t)
    return d * (-math.expm1(-r * t)) / (b - d * math.exp(-r * t))


def rk4_no_harm(b: float, d: float, q: float, t: float, steps: int = 20000) -> float:
    """Independent RK4 check of F'=bF^2-(b+d+q)F+d, F(0)=1."""
    dt = t / steps

    def f(x: float) -> float:
        return b * x * x - (b + d + q) * x + d

    x = 1.0
    for _ in range(steps):
        k1 = f(x)
        k2 = f(x + dt * k1 / 2)
        k3 = f(x + dt * k2 / 2)
        k4 = f(x + dt * k3)
        x += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return x


def founder_sample_size(m_actions: int, alpha: float, half_width: float) -> int:
    """Hoeffding n/action for simultaneous intervals on target and harm means.

    There are 2*m Bernoulli means and each two-sided Hoeffding interval has
    half-width sqrt(log(4*m/alpha)/(2n)); Bonferroni gives total error <= alpha.
    """
    if m_actions < 1 or not 0 < alpha < 1 or not 0 < half_width < 1:
        raise ValueError("invalid sample-design inputs")
    return math.ceil(math.log(4 * m_actions / alpha) / (2 * half_width**2))


def counting_process_radius(rate_max: float, exposure_max: float,
                            n_hazards: int, family_alpha: float) -> float:
    """Freedman radius for simultaneous event-count/compensator deviations.

    For cause j with count C_j and predictable at-risk exposure A_j <= Amax,
    intensity lambda_j Y_j and 0<=lambda_j<=rate_max, this returns beta such
    that P(|C_j-lambda_j*A_j|>beta for some j) <= family_alpha, using the
    unit-jump Freedman bound and a union bound over n_hazards.
    """
    if rate_max < 0 or exposure_max < 0 or n_hazards < 1 or not 0 < family_alpha < 1:
        raise ValueError("invalid confidence-bound inputs")
    x = math.log(2 * n_hazards / family_alpha)
    v = rate_max * exposure_max
    return math.sqrt(2 * v * x) + (2.0 / 3.0) * x


def hazard_interval(count: int, exposure: float, radius: float,
                    rate_max: float) -> tuple[float, float]:
    """Simultaneous CI induced by |C-lambda*A|<=radius."""
    if count < 0 or exposure < 0 or radius < 0 or rate_max < 0:
        raise ValueError("invalid interval inputs")
    if exposure == 0:
        return 0.0, rate_max
    return max(0.0, count - radius) / exposure, min(rate_max, (count + radius) / exposure)


def robust_harm_upper(b_hi: float, d_lo: float, q_hi: float, t: float) -> float:
    """Worst endpoint of a rectangular rate set, by pathwise monotonicity."""
    return harm_probability(b_hi, d_lo, q_hi, t)


def main() -> None:
    T, q = 1.0, 0.5
    models = {
        "low_turnover": (1.0, 0.5),
        "high_turnover": (10.5, 10.0),
    }
    rows = {}
    for label, (b, d) in models.items():
        s, u = expected_counts(b, d, q, T)
        F = no_harm_probability(b, d, q, T)
        rk = rk4_no_harm(b, d, q, T)
        rows[label] = {
            "birth_rate": b,
            "death_rate": d,
            "net_growth": b - d,
            "q_switch": q,
            "mean_safe_at_T": s,
            "mean_harmful_at_T": u,
            "mean_total_at_T": s + u,
            "P_any_harm_by_T": 1 - F,
            "P_no_harm_by_T": F,
            "q0_extinction_probability_by_T": extinction_probability(b, d, T),
            "RK4_absolute_error": abs(F - rk),
        }

    max_mean_gap = 0.0
    for k in range(101):
        t = k * T / 100
        a = expected_counts(*models["low_turnover"], q, t)
        b = expected_counts(*models["high_turnover"], q, t)
        max_mean_gap = max(max_mean_gap, abs(a[0] - b[0]), abs(a[1] - b[1]))

    # Two fixed actions. Their complete expected-count trajectories are equal
    # between the two branching worlds, but their clone-level rankings reverse.
    actions = {"A": (0.1, 0.0), "B": (0.2, 0.3)}
    decision_rows = {}
    decision_mean_gap = 0.0
    for action, (a_rate, q_rate) in actions.items():
        decision_rows[action] = {}
        for world, (b_rate, d_rate) in models.items():
            counts = expected_three_counts(b_rate, d_rate, a_rate, q_rate, T)
            mean_s, mean_r, mean_u = counts
            effective_r = b_rate - d_rate - a_rate - q_rate
            if abs(effective_r) < 1e-14:
                var_s = (b_rate + d_rate + a_rate + q_rate) * T
            else:
                var_s = ((b_rate + d_rate + a_rate + q_rate) / effective_r
                         * mean_s * (mean_s - 1))
            decision_rows[action][world] = {
                "a_target": a_rate,
                "q_harm": q_rate,
                "mean_S_R_U_at_T": counts,
                "variance_S_at_T": var_s,
                "moment_inverse_reconstruction": endpoint_moment_rate_inverse(
                    mean_s, mean_r, mean_u, var_s, T
                ),
                "P_target_and_no_harm": target_safe_probability(
                    b_rate, d_rate, a_rate, q_rate, T
                ),
                "target_safe_RK4_absolute_error": abs(
                    target_safe_probability(b_rate, d_rate, a_rate, q_rate, T)
                    - rk4_target_safe_probability(b_rate, d_rate, a_rate, q_rate, T)
                ),
            }
        low_counts = decision_rows[action]["low_turnover"]["mean_S_R_U_at_T"]
        high_counts = decision_rows[action]["high_turnover"]["mean_S_R_U_at_T"]
        decision_mean_gap = max(
            decision_mean_gap,
            *(abs(x - y) for x, y in zip(low_counts, high_counts)),
        )

    pA_low = decision_rows["A"]["low_turnover"]["P_target_and_no_harm"]
    pB_low = decision_rows["B"]["low_turnover"]["P_target_and_no_harm"]
    pA_high = decision_rows["A"]["high_turnover"]["P_target_and_no_harm"]
    pB_high = decision_rows["B"]["high_turnover"]["P_target_and_no_harm"]
    gap_low = pB_low - pA_low
    gap_high = pA_high - pB_high
    decision_gap = min(gap_low, gap_high)

    out = {
        "model": "S->2S at b; S->0 at d; S->U at q; U persists without branching",
        "horizon": T,
        "mean_trajectory_max_abs_gap_on_101_point_grid": max_mean_gap,
        "models": rows,
        "decision_reversal": {
            "horizon": T,
            "worlds_share_b_minus_d": 0.5,
            "actions": decision_rows,
            "mean_count_curve_max_abs_gap": decision_mean_gap,
            "world_low_best_action": "B" if gap_low > 0 else "A",
            "world_high_best_action": "A" if gap_high > 0 else "B",
            "gap_low": gap_low,
            "gap_high": gap_high,
            "worst_regret_of_action_B": gap_high,
            "minimax_randomized_policy_B_probability": gap_low / (gap_low + gap_high),
            "minimax_randomized_regret": gap_low * gap_high / (gap_low + gap_high),
            "per_action_pair_founder_n_for_error_le_0_05": math.ceil(
                math.log(1 / 0.05) / decision_gap**2
            ),
            "sample_claim": "Hoeffding bound exp(-n*gap^2) for the sign of the difference of two independent n-founder Bernoulli sample means",
        },
        "two_action_founder_sample_size_per_action": {
            "alpha": 0.05,
            "half_width": 0.05,
            "n": founder_sample_size(2, 0.05, 0.05),
            "calibrated_claim": "95% simultaneous Hoeffding coverage for target and harm rates across two fixed actions, assuming independent randomized founders and complete founder-level outcomes",
        },
        "example_capped_event_count_radius": {
            "rate_upper_bound": 12.0,
            "at_risk_cell_time_budget": 200.0,
            "number_of_hazards": 6,
            "family_alpha": 0.05,
            "radius": counting_process_radius(12.0, 200.0, 6, 0.05),
            "warning": "the radius is large at this illustrative exposure budget; the design must increase independent at-risk cell-time or return UNKNOWN",
        },
    }
    target = Path(__file__).with_name("branching_safety_controller_results.json")
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
