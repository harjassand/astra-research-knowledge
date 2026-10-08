#!/usr/bin/env python3
"""Recompute descriptive Fig. 5p rescue quantities from the official source data.

Raw replicate values are transcribed from MOESM11_ESM.xlsx, worksheet "Figure 5",
section "Fig. 5p". This script intentionally uses only the Python standard library.
It does not recompute or reinterpret the paper's inferential tests.
"""
import json
import math
from pathlib import Path

RAW = {
    "control": [5090507, 4984949, 5184033, 5051615],
    "clodronate": [2372806, 2428438, 2020320, 2135245],
    "clodronate_plus_CXCL16": [2825187, 2585301, 2660136, 2759337],
    "clodronate_plus_CXCL10": [3049799, 2950718, 2467810, 2959881],
    "clodronate_plus_CXCL16_CXCL10": [3071035, 3367325, 3052521, 3219973],
    "clodronate_plus_IGF1": [4341047, 4180586, 4233750, 4115784],
    "clodronate_plus_CCL2": [4476359, 4413795, 4315991, 4567152],
    "clodronate_plus_IGF1_CCL2": [5162374, 5018172, 5275341, 5163110],
    "clodronate_plus_all_four": [4968874, 4996545, 5150520, 4971834],
}


def summary(xs):
    mean = sum(xs) / len(xs)
    sd = math.sqrt(sum((x - mean) ** 2 for x in xs) / (len(xs) - 1))
    return {"n": len(xs), "mean": mean, "sd": sd, "sem": sd / math.sqrt(len(xs))}


summaries = {key: summary(vals) for key, vals in RAW.items()}
baseline = summaries["clodronate"]["mean"]
control = summaries["control"]["mean"]
denominator = control - baseline
for key, row in summaries.items():
    row["ratio_to_control_mean"] = row["mean"] / control
    row["fraction_of_control_minus_clodronate_gap"] = (row["mean"] - baseline) / denominator


def fractional_response(key):
    return summaries[key]["fraction_of_control_minus_clodronate_gap"]


def bliss_independent_ceiling(single_a, single_b):
    """Bliss independent-action benchmark on normalized marker-gap recovery."""
    a, b = fractional_response(single_a), fractional_response(single_b)
    return 1 - (1 - a) * (1 - b)


pair_igf_ccl = fractional_response("clodronate_plus_IGF1_CCL2")
pair_cxcl = fractional_response("clodronate_plus_CXCL16_CXCL10")
bliss_igf_ccl = bliss_independent_ceiling("clodronate_plus_IGF1", "clodronate_plus_CCL2")
bliss_cxcl = bliss_independent_ceiling("clodronate_plus_CXCL16", "clodronate_plus_CXCL10")

out = {
    "source": {
        "article_doi": "10.1038/s41467-026-72331-w",
        "supplement": "41467_2026_72331_MOESM11_ESM.xlsx",
        "worksheet": "Figure 5",
        "section": "Fig. 5p",
        "analysis": "descriptive group means; no inferential tests recomputed",
    },
    "groups": summaries,
    "derived": {
        "control_minus_clodronate_mean_gap": denominator,
        "combo_minus_clodronate_mean": summaries["clodronate_plus_IGF1_CCL2"]["mean"] - baseline,
        "combo_minus_IGF1_only_mean": summaries["clodronate_plus_IGF1_CCL2"]["mean"] - summaries["clodronate_plus_IGF1"]["mean"],
        "combo_minus_CCL2_only_mean": summaries["clodronate_plus_IGF1_CCL2"]["mean"] - summaries["clodronate_plus_CCL2"]["mean"],
        "combo_minus_all_four_mean": summaries["clodronate_plus_IGF1_CCL2"]["mean"] - summaries["clodronate_plus_all_four"]["mean"],
    },
    "fractional_rescue_interaction_bounds": {
        "definition": "e=(mean MFI minus clodronate mean)/(control mean minus clodronate mean); Bliss=1-(1-eA)(1-eB)",
        "conditional_assumptions": [
            "each single-agent fractional response is nondecreasing with dose",
            "fractional marker-gap recovery is treated as a bounded effect scale",
            "Bliss independent-action is the null model, not a biological law",
        ],
        "IGF1_plus_CCL2": {
            "single_agent_full_dose_effects": {
                "IGF1_5ng": fractional_response("clodronate_plus_IGF1"),
                "CCL2_100ng": fractional_response("clodronate_plus_CCL2"),
            },
            "full_dose_Bliss_upper_bound_for_half_dose_pair": bliss_igf_ccl,
            "observed_half_dose_pair_effect_uncapped": pair_igf_ccl,
            "observed_half_dose_pair_effect_capped_at_control": min(1, pair_igf_ccl),
            "observed_minus_Bliss_surplus_uncapped": pair_igf_ccl - bliss_igf_ccl,
            "observed_minus_Bliss_surplus_capped": min(1, pair_igf_ccl) - bliss_igf_ccl,
            "pair_dose_each_factor": {"IGF1_ng": 2.5, "CCL2_ng": 50},
        },
        "CXCL16_plus_CXCL10": {
            "single_agent_full_dose_effects": {
                "CXCL16_100ng": fractional_response("clodronate_plus_CXCL16"),
                "CXCL10_100ng": fractional_response("clodronate_plus_CXCL10"),
            },
            "full_dose_Bliss_upper_bound_for_half_dose_pair": bliss_cxcl,
            "observed_half_dose_pair_effect": pair_cxcl,
            "observed_minus_Bliss_surplus": pair_cxcl - bliss_cxcl,
            "pair_dose_each_factor_ng": 50,
        },
    },
}
path = Path(__file__).resolve().parents[1] / "proofs" / "rescue_quantification.json"
path.write_text(json.dumps(out, indent=2) + "\n")
print(path)
print(json.dumps(out["derived"], indent=2))
