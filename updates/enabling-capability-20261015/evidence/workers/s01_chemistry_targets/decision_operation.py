#!/usr/bin/env python3
"""Reproducible decision/units countermodels using exact rational arithmetic.

These are conditional mathematical operations and source-contract diagnostics.
They do not fit a predictor, obtain mixture truth, or repair source labels.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent


def rational(x):
    return {"exact": str(x), "decimal": float(x)}


def utility_gap(a, b, lam):
    return a[0]-b[0]-lam*(a[1]-b[1])


def main():
    # Exact source-decimal arithmetic, kept separate from protobuf float32 values.
    n_ord_umol = F("0.04")
    reagent_dose_ul = F("0.2")
    reaction_ul = 5*reagent_dose_ul
    c_ord_M = n_ord_umol/reaction_ul  # umol/uL is mol/L.
    c_si_M = F("0.2")
    quench_ul, aliquot_ul, analytical_solvent_ul = F(3), F("0.5"), F(30)
    quench_dilution = (reaction_ul+quench_ul)/reaction_ul
    analytical_dilution = (analytical_solvent_ul+aliquot_ul)/aliquot_ul
    total_dilution = quench_dilution*analytical_dilution
    code_max_mM = F("0.2")/4/30*1000
    # IS response normalization removes a shared post-quench dilution factor.
    n_caffeine_workup_umol = F("0.0667")*3
    n_caffeine_analysis_umol = F("0.0067")*3
    # SI wording includes an unspecified aliquot of a mixed calibration sample.
    # The following concentration is CONDITIONAL on the complete 20uL caffeine
    # stock aliquot reaching the final 1000uL. The product/IS ratio below does
    # not require this assumption because any shared aliquot factor cancels.
    caffeine_calibration_mM_if_full_aliquot = F("0.085")*20/1000*1000
    standard_product_to_caffeine_ratio = [F("0.0679")*v/(F("0.085")*20) for v in [5,10,15,20,25]]
    units = {
        "status": "UNRESOLVED_SOURCE_UNIT_CONTRACT; NO_LABEL_RESCALING",
        "ORD_limiting_amount_umol_source_decimal": rational(n_ord_umol),
        "reaction_volume_ul_from_five_carriers": rational(reaction_ul),
        "ORD_implied_feed_concentration_M": rational(c_ord_M),
        "SI_stated_reaction_concentration_M": rational(c_si_M),
        "quench_dilution_factor": rational(quench_dilution),
        "analytical_dilution_factor_including_aliquot_volume": rational(analytical_dilution),
        "total_physical_dilution_factor": rational(total_dilution),
        "analytical_product_mM_at_100percent_using_ORD_amount": rational(c_ord_M/total_dilution*1000),
        "analytical_product_mM_at_100percent_using_SI_concentration": rational(c_si_M/total_dilution*1000),
        "code_default_max_yield_commented_mM": rational(code_max_mM),
        "code_error_to_fractional_yield_radius_multiplier": rational(1/code_max_mM),
        "code_error_to_percentage_point_radius_multiplier": rational(100/code_max_mM),
        "caffeine_workup_amount_umol": rational(n_caffeine_workup_umol),
        "caffeine_analysis_details_amount_umol": rational(n_caffeine_analysis_umol),
        "caffeine_workup_vs_analysis_concentration_ratio": rational(n_caffeine_workup_umol/n_caffeine_analysis_umol),
        "calibration_caffeine_mM_conditional_on_full_stock_aliquot": rational(caffeine_calibration_mM_if_full_aliquot),
        "standard_product_to_caffeine_ratios_independent_of_shared_dilution": [rational(x) for x in standard_product_to_caffeine_ratio],
        "calibration_equivalent_product_mM_at_100percent_SI_feed_conditional_full_aliquot": rational(caffeine_calibration_mM_if_full_aliquot*(c_si_M*reaction_ul)/n_caffeine_workup_umol),
        "calibration_equivalent_product_mM_at_100percent_ORD_feed_conditional_full_aliquot": rational(caffeine_calibration_mM_if_full_aliquot*n_ord_umol/n_caffeine_workup_umol),
        "interpretation": [
            "The source deconvolution estimates live in the numerical scale of external wavelength calibration ext_coef files, which were not acquired.",
            "Figure S13 plots product/internal-standard concentration ratios. Shared dilution cancels in those ratios; 61-versus-30 dilution alone does not establish erroneous yields.",
            "Original calibration files and exact run arguments are required to reconcile code's max_yield with ORD amounts and the SI protocol.",
            "Code normalizes DP/SP points by max_yield while leaving error_DP/error_SP unchanged. The proper unit conversion follows the actual calibration scale and exact runtime max_yield.",
            "No inferred rescaling or source-data correction is made here."
        ]
    }
    # Actual point-label ranking reversal; native float32 source values are exact
    # rationals once decoded. This establishes a label-level decision difference.
    selected = (F(52.630210876464844), F(47.21154022216797))
    target_best = (F(99.15884399414062), F(0))
    runner_up_target = F(99.15573120117188)
    assert sum(selected) > sum(target_best)
    assert target_best[0] > selected[0] and target_best[1] < selected[1]
    radius = (target_best[0]-runner_up_target)/2
    # Positive target bleed can reverse an observed target order while leaving
    # the same measured vector under two admissible calibration hypotheses.
    # Use an abstract physically admissible example, explicitly not assay data.
    obs_a, obs_b = (F(42),F(20)), (F(40),F(10))
    alpha = F(1,2)
    true_a = (obs_a[0]-alpha*obs_a[1],obs_a[1])
    true_b = (obs_b[0]-alpha*obs_b[1],obs_b[1])
    assert obs_a[0] > obs_b[0] and true_a[0] < true_b[0]
    assert all(x >= 0 for x in true_a+true_b) and sum(true_a)<=100 and sum(true_b)<=100
    example = {
        "actual_ORD_label_ranking_reversal": {
            "combined_label_argmax_T_S": [rational(x) for x in selected],
            "target_label_argmax_T_S": [rational(x) for x in target_best],
            "combined_argmax_is_strictly_Pareto_dominated": True,
            "target_argmax_vs_runner_up_equal_absolute_error_radius_pct_points": rational(radius),
            "scope": "Producer labels only; no independent composition, no achieved uncertainty bound."
        },
        "abstract_cross_talk_countermodel_not_data": {
            "observed_A": [rational(x) for x in obs_a],
            "observed_B": [rational(x) for x in obs_b],
            "hypothesis_1_identity_calibration_target_prefers": "A",
            "hypothesis_2_observed_T_equals_true_T_plus_alpha_true_S": rational(alpha),
            "hypothesis_2_true_A": [rational(x) for x in true_a],
            "hypothesis_2_true_B": [rational(x) for x in true_b],
            "hypothesis_2_target_prefers": "B",
            "meaning": "Separate positive gains preserve Pareto order, but unknown cross-talk does not. This shows an information gate, not evidence the acquired assay has this cross-talk."
        },
        "conditional_robust_pairwise_decision": {
            "utility": "U=T-lambda*S, lambda>=0",
            "observed_gap": "dT-lambda*dS",
            "uncertainty_contract": "Every T and S observation has absolute error <=eps in percentage points; a control mean retains <=eps under arbitrary dependence.",
            "sharp_worst_case_gap_interval": "[dT-lambda*dS-2eps(1+lambda), dT-lambda*dS+2eps(1+lambda)]",
            "strict_preference_certificate": "dT-lambda*dS>2eps(1+lambda)",
            "sharp_pairwise_error_radius": "abs(dT-lambda*dS)/(2(1+lambda))",
            "achieved_eps": "UNKNOWN"
        },
        "conditional_common_affine_calibration": {
            "transform": "T'=aT+b, S'=cS+d with shared a,c>0",
            "pareto_order": "invariant",
            "penalty_reparameterization": "lambda'=a*lambda/c",
            "does_not_cover": ["per-well or per-batch gains", "cross-talk", "unmeasured censoring limits", "unknown product structure"]
        }
    }
    (BASE/"UNIT_AUDIT.json").write_text(json.dumps(units,indent=2)+"\n")
    (BASE/"DECISION_OPERATION.json").write_text(json.dumps(example,indent=2)+"\n")
    print(json.dumps({"ORD_implied_feed_M":float(c_ord_M),"physical_dilution":float(total_dilution),"code_default_mM":float(code_max_mM),"reported_error_to_yield_pp_multiplier_if_default_scale":float(100/code_max_mM),"unique_target_winner_epsilon_radius_pp":float(radius),"countermodel_verified":True},indent=2))


if __name__=="__main__":
    main()
