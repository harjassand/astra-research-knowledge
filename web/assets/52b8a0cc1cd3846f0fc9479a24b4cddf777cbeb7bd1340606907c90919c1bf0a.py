#!/usr/bin/env python3
"""Finite checks and resource arithmetic for endpoint force-order spectroscopy.

This is a mathematical simulator, not an analysis of experimental records.
It uses exact scalar affine propagators for a two-state CTMC and piecewise
constant ramp surrogates.  The tests check the stated algebra and expose the
cost of estimating a rate from three endpoint order contrasts.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Affine:
    """Occupancy map x -> a*x+b for x=P(state 1)."""

    a: float
    b: float


def compose(after: Affine, before: Affine) -> Affine:
    """Return after o before."""
    return Affine(after.a * before.a, after.a * before.b + after.b)


def segment(k01: float, k10: float, duration: float) -> Affine:
    """Two-state CTMC propagation for rates 0->1 and 1->0."""
    lam = k01 + k10
    if lam == 0:
        return Affine(1.0, 0.0)
    pi1 = k01 / lam
    a = math.exp(-lam * duration)
    return Affine(a, pi1 * (1.0 - a))


def sequence(segments: Iterable[tuple[float, float, float]]) -> Affine:
    """Compose a time-ordered list of constant-rate segments."""
    out = Affine(1.0, 0.0)
    for k01, k10, duration in segments:
        out = compose(segment(k01, k10, duration), out)
    return out


def loop(pre: Affine, post: Affine, k01: float, k10: float,
         plateau: float) -> Affine:
    """Baseline->force ramp, plateau, return ramp."""
    return compose(post, compose(segment(k01, k10, plateau), pre))


def contrast(a: Affine, b: Affine, x0: float) -> float:
    """AB minus BA occupancy, where a,b are force-loop maps."""
    ab = compose(b, a)
    ba = compose(a, b)
    return (ab.a * x0 + ab.b) - (ba.a * x0 + ba.b)


def endpoint_order_contrast(a: Affine, b: Affine, x0: float,
                            read_gap: float = 1.0) -> float:
    """Expected scalar read contrast; read_gap is E[Y|1]-E[Y|0]."""
    return read_gap * contrast(a, b, x0)


def rate_from_ratio(ratio: float, spacing: float) -> float:
    if not (0.0 < ratio < 1.0 and spacing > 0.0):
        raise ValueError("ratio must lie in (0,1), and spacing must be positive")
    return -math.log(ratio) / spacing


def two_arm_n(gap: float, alpha: float = 0.05) -> int:
    """Per-arm n for a Hoeffding threshold test at gap >= gap.

    Pair independent [0,1] outcomes across arms. Each difference lies in
    [-1,1], so Hoeffding gives P(|Dhat-D|>=eps)<=2 exp(-n eps^2/2).
    Thresholding at gap/2 bounds both errors by alpha.
    """
    if gap <= 0:
        raise ValueError("gap must be positive")
    return math.ceil(8.0 * math.log(2.0 / alpha) / (gap * gap))


def contrast_precision_n(eps_d: float, alpha: float = 0.05) -> int:
    """Per-arm n at each of three durations for simultaneous |Dhat-D|<=eps_d.

    Pair independent [0,1] outcomes across arms. Hoeffding gives
    2 exp(-n eps_d^2/2) per contrast; union bound over three durations gives
    6 exp(-n eps_d^2/2).
    """
    if eps_d <= 0:
        raise ValueError("eps_d must be positive")
    return math.ceil(2.0 * math.log(6.0 / alpha) / (eps_d * eps_d))


def optimal_dwell_split(lam_a: float, lam_b: float,
                        total_dwell: float) -> tuple[float, float]:
    """Maximize the two-state AB/BA gap for fixed total force-on dwell.

    With no ramps, |Delta x|=|pi_B-pi_A|*(1-exp(-lam_a*s_a))
    *(1-exp(-lam_b*s_b)), s_a+s_b=total_dwell.  The log objective is
    strictly concave, and its unique interior optimum equates the two
    marginal log gains.  Fixed ramps add the same wall-time overhead to all
    splits, but generally change the optimum and must then be measured/fitted.
    """
    if lam_a <= 0 or lam_b <= 0 or total_dwell <= 0:
        raise ValueError("rates and total dwell must be positive")
    if abs(lam_a - lam_b) < 1e-14 * max(lam_a, lam_b):
        return total_dwell / 2.0, total_dwell / 2.0

    def marginal(lam: float, s: float) -> float:
        # Stable near zero: lam/(expm1(lam*s)).
        return lam / math.expm1(lam * s)

    lo, hi = 0.0, total_dwell
    for _ in range(100):
        sa = (lo + hi) / 2.0
        sb = total_dwell - sa
        # The difference decreases strictly as sa increases.
        if marginal(lam_a, sa) > marginal(lam_b, sb):
            lo = sa
        else:
            hi = sa
    sa = (lo + hi) / 2.0
    return sa, total_dwell - sa


def no_ramp_order_gap(lam_a: float, lam_b: float, pi_gap: float,
                      s_a: float, s_b: float) -> float:
    return (abs(pi_gap) * (1.0 - math.exp(-lam_a * s_a))
            * (1.0 - math.exp(-lam_b * s_b)))


def rate_interval(d1_hat: float, d2_hat: float, eps_d: float,
                  tau: float) -> tuple[float, float]:
    """Conservative rate interval when each D_j error is at most eps_d.

    d1=D(tau)-D(0), d2=D(2tau)-D(tau), so each adjacent difference has
    error at most 2 eps_d.  The interval is returned only when its ratio is
    positive and below one.
    """
    # The two adjacent differences share the unknown common curvature sign.
    # Orient by d1 only after both estimates have a common, separated sign.
    if d1_hat < 0.0 and d2_hat < 0.0:
        d1_hat, d2_hat = -d1_hat, -d2_hat
    elif d1_hat <= 0.0 or d2_hat <= 0.0:
        raise ValueError("adjacent differences do not have a resolved common sign")
    lo_den = d1_hat - 2.0 * eps_d
    if lo_den <= 0:
        raise ValueError("first difference is not separated from zero")
    r_lo = (d2_hat - 2.0 * eps_d) / (d1_hat + 2.0 * eps_d)
    r_hi = (d2_hat + 2.0 * eps_d) / lo_den
    if not (0.0 < r_lo <= r_hi < 1.0):
        raise ValueError("ratio confidence interval leaves (0,1)")
    return rate_from_ratio(r_hi, tau), rate_from_ratio(r_lo, tau)


def main() -> None:
    # Heterogeneous, direction-asymmetric ramp surrogates.  They are fixed
    # loop-specific maps, so only the plateau duration varies within a loop.
    pre_a = sequence([(1.2, 3.0, 0.035), (2.0, 1.5, 0.025)])
    post_a = sequence([(2.4, 1.0, 0.030), (1.4, 2.2, 0.020)])
    pre_b = sequence([(2.8, 1.2, 0.030), (1.5, 2.5, 0.020)])
    post_b = sequence([(1.1, 2.7, 0.025), (2.3, 1.4, 0.030)])
    k01_a, k10_a = 4.1, 2.4
    k01_b, k10_b = 1.3, 4.7
    lam_a = k01_a + k10_a
    tau = math.log(1.5) / lam_a  # places exp(-lambda_A*tau) at 2/3
    t_b = 3.0 / (k01_b + k10_b)
    read_gap = 0.35
    x0 = 0.137

    D = []
    for n in range(3):
        a = loop(pre_a, post_a, k01_a, k10_a, n * tau)
        b = loop(pre_b, post_b, k01_b, k10_b, t_b)
        D.append(endpoint_order_contrast(a, b, x0, read_gap))
    d1, d2 = D[1] - D[0], D[2] - D[1]
    ratio = d2 / d1
    expected_ratio = math.exp(-lam_a * tau)
    assert abs(ratio - expected_ratio) < 1e-12

    # Check initial-state invariance over boundary and interior occupancies.
    gaps_by_initial_state = []
    for x in [0.0, 0.137, 0.5, 1.0]:
        a = loop(pre_a, post_a, k01_a, k10_a, tau)
        b = loop(pre_b, post_b, k01_b, k10_b, t_b)
        gaps_by_initial_state.append(endpoint_order_contrast(a, b, x, read_gap))
    assert max(gaps_by_initial_state) - min(gaps_by_initial_state) < 1e-14

    # Three-class mixture: common curvature sign makes ratio a convex mean
    # of exp(-lambda*tau), even though it is not a population mean rate.
    mix = [(0.25, 0.7, 1.0), (0.50, 1.0, 1.0), (0.25, 1.4, 1.0)]
    mix_d1 = sum(w * c * math.exp(-lam * tau) *
                 (math.exp(-lam * tau) - 1.0) for w, lam, c in mix)
    mix_d2 = sum(w * c * math.exp(-2.0 * lam * tau) *
                 (math.exp(-lam * tau) - 1.0) for w, lam, c in mix)
    mix_ratio = mix_d2 / mix_d1
    mix_r_range = (math.exp(-max(z[1] for z in mix) * tau),
                   math.exp(-min(z[1] for z in mix) * tau))
    assert mix_r_range[0] <= mix_ratio <= mix_r_range[1]

    # Opposite curvature signs can put the ratio outside every component rate.
    signed_mix = [(1.0, 0.22314355131420976), (-0.30, 0.916290731874155)]
    signed_d1 = sum(c * (math.exp(-lam * tau) - 1.0)
                    for c, lam in signed_mix)
    signed_d2 = sum(c * math.exp(-lam * tau) *
                    (math.exp(-lam * tau) - 1.0)
                    for c, lam in signed_mix)
    signed_ratio = signed_d2 / signed_d1
    assert not (math.exp(-max(z[1] for z in signed_mix) * tau) <= signed_ratio <=
                math.exp(-min(z[1] for z in signed_mix) * tau))

    # Hohng-derived planning illustration, explicitly not an observed rate or
    # measured assay output: equilibrium-shift model plus a separate published
    # HJ FRET-state separation from MAESTRO.
    kbt_pn_nm = 4.114
    dx_nm = 4.4
    delta_force_pn = 1.7
    delta_pi = 0.5 * math.tanh(delta_force_pn * dx_nm / (2.0 * kbt_pn_nm))
    activation = (1.0 - math.exp(-3.0)) ** 2
    order_gaps = {}
    order_n = {}
    for zeta in [1.0, 0.35, 0.1]:
        g = zeta * delta_pi * activation
        order_gaps[str(zeta)] = g
        order_n[str(zeta)] = two_arm_n(g)

    # Three-duration rate-estimation illustration: one common amplitude
    # multiplies D(s)=C(1-exp(-lambda_A s)), and the d1,d2 curvature is small.
    zeta = 0.35
    delta_pi_rate = 0.36
    b_activation = 1.0 - math.exp(-3.0)
    C = zeta * delta_pi_rate * b_activation
    r = 2.0 / 3.0
    rate_d1 = C * (1.0 - r)
    rate_d2 = C * r * (1.0 - r)
    eps_d = 4.0e-4
    n_rate = contrast_precision_n(eps_d)
    lam_tau = math.log(1.5)
    lam_ci = rate_interval(rate_d1, rate_d2, eps_d, lam_tau)
    assert lam_ci[0] < 1.0 < lam_ci[1]
    assert rate_interval(-rate_d1, -rate_d2, eps_d, lam_tau) == lam_ci

    # The unique split must satisfy equal marginal log gains.
    sa_test, sb_test = optimal_dwell_split(0.5, 2.0, 2.0)
    assert abs(0.5 / math.expm1(0.5 * sa_test)
               - 2.0 / math.expm1(2.0 * sb_test)) < 1e-12

    # Equal-information baseline for order detection: under an equal total
    # plateau budget, optimize the split to minimize the distribution-free
    # Hoeffding molecule count.  This is optimal only in the stated no-ramp,
    # two-state, contiguous-AB/BA schedule family.  Actual measured ramps can
    # shift the optimum and must be included before comparing protocols.
    total_dwell = 2.0
    pi_gap_control = 0.6
    control_scenarios = {}
    for la, lb in [(1.0, 1.0), (0.5, 2.0), (2.0, 0.5)]:
        sa_opt, sb_opt = optimal_dwell_split(la, lb, total_dwell)
        g_opt = no_ramp_order_gap(la, lb, pi_gap_control, sa_opt, sb_opt)
        g_equal = no_ramp_order_gap(la, lb, pi_gap_control,
                                    total_dwell / 2.0, total_dwell / 2.0)
        assert g_opt + 1e-14 >= g_equal
        control_scenarios[f"lambdaA={la},lambdaB={lb}"] = {
            "lambdaA_per_s": la,
            "lambdaB_per_s": lb,
            "fixed_total_plateau_dwell_s": total_dwell,
            "optimized_sA_sB_s": [sa_opt, sb_opt],
            "equal_split_sA_sB_s": [total_dwell / 2.0, total_dwell / 2.0],
            "optimized_gap_at_abs_delta_pi_0.6": g_opt,
            "equal_split_gap_at_abs_delta_pi_0.6": g_equal,
            "optimized_over_equal_gap": g_opt / g_equal,
            "n_per_arm_95pct_Hoeffding": two_arm_n(g_opt),
            "equal_split_n_per_arm_95pct_Hoeffding": two_arm_n(g_equal),
        }

    results = {
        "classification": "finite mathematical check and conditional planning arithmetic; no experimental data",
        "ramp_loop_check": {
            "lambda_A_per_s": lam_a,
            "tau_s": tau,
            "expected_ratio_exp_minus_lambda_tau": expected_ratio,
            "observed_ratio_from_three_ramp_aware_contrasts": ratio,
            "absolute_ratio_error": abs(ratio - expected_ratio),
            "order_contrast_by_initial_occupancy": gaps_by_initial_state,
            "max_initial_occupancy_spread": max(gaps_by_initial_state) - min(gaps_by_initial_state),
            "contrasts_D0_D1_D2": D,
        },
        "heterogeneous_rate_mix_common_sign": {
            "component_rates_per_s": [z[1] for z in mix],
            "contrast_weighted_exp_rate_ratio": mix_ratio,
            "component_exp_rate_interval": list(mix_r_range),
            "ratio_is_inside_component_interval": mix_r_range[0] <= mix_ratio <= mix_r_range[1],
            "note": "The effective rate is contrast-weighted, not the population mean.",
        },
        "heterogeneous_rate_mix_opposite_sign_counterexample": {
            "component_rates_per_s": [z[1] for z in signed_mix],
            "curvature_coefficients": [z[0] for z in signed_mix],
            "ratio": signed_ratio,
            "component_exp_rate_interval": [
                math.exp(-max(z[1] for z in signed_mix) * tau),
                math.exp(-min(z[1] for z in signed_mix) * tau),
            ],
            "ratio_outside_interval": not (
                math.exp(-max(z[1] for z in signed_mix) * tau) <= signed_ratio <=
                math.exp(-min(z[1] for z in signed_mix) * tau)
            ),
        },
        "conditional_hj_order_test": {
            "Dxeq_nm_source_reported_mean": dx_nm,
            "force_increment_pn_illustrative": delta_force_pn,
            "equilibrium_population_shift_from_logistic_model": delta_pi,
            "activation_if_each_plateau_is_3_over_its_lambda": activation,
        "bounded_scalar_read_gap_scenarios": order_gaps,
        "note": "zeta here is a bounded-statistic mean gap, not total variation; the .35 HJ scale is reported as approximate FRET-state levels in a different setup and is not a calibrated read-channel parameter",
            "per_arm_n_for_95pct_two_sided_Hoeffding_test": order_n,
            "status": "inferred planning scales; source does not report these exact forces, rates, photon records, or endpoint sample costs",
        },
        "conditional_three_duration_rate_estimation": {
            "read_gap": zeta,
            "population_shift": delta_pi_rate,
            "B_activation": b_activation,
            "common_amplitude_C": C,
            "lambda_A_tau": lam_tau,
            "D1_minus_D0": rate_d1,
            "D2_minus_D1": rate_d2,
            "per_arm_n_for_simultaneous_contrast_error_4e-4": n_rate,
            "total_arms": 6,
            "total_endpoint_records": 6 * n_rate,
            "lambda_A_CI_over_lambda_A": list(lam_ci),
            "status": "distribution-free endpoint bound; shows rate inversion is sample-expensive at this contrast scale",
        },
        "matched_plateau_budget_optimal_control": {
            "scope": "No-ramp two-state model, contiguous AB versus BA, fixed total plateau dwell; ramp overhead fixed and excluded from split optimization.",
            "criterion": "Maximize absolute endpoint order gap, equivalently minimize the stated distribution-free Hoeffding molecule bound for bounded endpoint reads.",
            "optimality_equation": "lambdaA/(exp(lambdaA*sA)-1) = lambdaB/(exp(lambdaB*sB)-1), sA+sB=T",
            "scenarios": control_scenarios,
            "limitation": "This is not a photon-likelihood/Fisher-optimal protocol and not globally optimal over arbitrary waveforms. Empirical ramp maps, background, and brightness must be included in the matched full-likelihood comparison.",
        },
    }
    out = Path(__file__).with_name("protocol_cost.json")
    out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
