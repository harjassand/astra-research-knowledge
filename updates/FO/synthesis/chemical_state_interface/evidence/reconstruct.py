"""Small arithmetic reconstruction from the cited source-reported values.

This checks unit conversions and ratios only. It is not a kinetic model, source
validation, or experimental replication.
"""

import json
from pathlib import Path


HOMOGENIZATION_S = 72_000
HOMOGENIZATION_SPACE_VELOCITY_MOL_PER_MOL_H_PER_KS = 100
INITIAL_MTO_S = 1_800
HE_PURGE_S = 600
BASE_POOL_RATIO = 0.6
MANIPULATED_POOL_RATIOS = [1.0, 1.4]
BASE_SELECTIVITY_RATIO = 1.8
MANIPULATED_SELECTIVITY_RATIOS = [2.5, 5.6]

PULSE_C_UMOL = 7.6
PULSE_DELAY_COUNT = 225
PULSE_INTERVAL_MIN = [3.75, 1.25]
PRE_SWITCH_13C_PULSE_COUNT = 5

result = {
    "scope": "arithmetic from source-reported protocol values only",
    "hwang_hsapO34": {
        "pool_homogenization_duration_s": HOMOGENIZATION_S,
        "pool_homogenization_duration_h": HOMOGENIZATION_S / 3600,
        "pool_homogenization_cumulative_feed_mol_meoh_per_mol_H": (
            HOMOGENIZATION_SPACE_VELOCITY_MOL_PER_MOL_H_PER_KS * HOMOGENIZATION_S / 1000
        ),
        "initial_MTO_stage_duration_s": INITIAL_MTO_S,
        "initial_MTO_stage_feed_mol_meoh_per_mol_H": (
            HOMOGENIZATION_SPACE_VELOCITY_MOL_PER_MOL_H_PER_KS * INITIAL_MTO_S / 1000
        ),
        "He_purge_duration_s": HE_PURGE_S,
        "documented_initial_conditioning_and_purge_s": INITIAL_MTO_S + HOMOGENIZATION_S + HE_PURGE_S,
        "documented_initial_conditioning_and_purge_h": (INITIAL_MTO_S + HOMOGENIZATION_S + HE_PURGE_S) / 3600,
        "initial_plus_conditioning_MeOH_feed_mol_per_mol_H": (
            HOMOGENIZATION_SPACE_VELOCITY_MOL_PER_MOL_H_PER_KS * (INITIAL_MTO_S + HOMOGENIZATION_S) / 1000
        ),
        "absolute_pool_homogenization_feed_moles": None,
        "pool_ratio_baseline": BASE_POOL_RATIO,
        "pool_ratio_manipulated": MANIPULATED_POOL_RATIOS,
        "pool_ratio_fold_vs_baseline": [x / BASE_POOL_RATIO for x in MANIPULATED_POOL_RATIOS],
        "C3_to_C2_selectivity_baseline": BASE_SELECTIVITY_RATIO,
        "C3_to_C2_selectivity_manipulated": MANIPULATED_SELECTIVITY_RATIOS,
        "C3_to_C2_fold_vs_baseline": [x / BASE_SELECTIVITY_RATIO for x in MANIPULATED_SELECTIVITY_RATIOS],
    },
    "liu_acs_hzsm5_scan": {
        "assumption": "one 7.6 umol-C pulse at each of 225 scanned delays",
        "pulses_per_scanned_curve": PULSE_DELAY_COUNT,
        "carbon_dose_umol_per_scanned_curve": PULSE_C_UMOL * PULSE_DELAY_COUNT,
        "carbon_dose_mmol_per_scanned_curve": PULSE_C_UMOL * PULSE_DELAY_COUNT / 1000,
        "elapsed_h_by_pulse_interval": {
            str(interval): interval * PULSE_DELAY_COUNT / 60
            for interval in PULSE_INTERVAL_MIN
        },
        "five_pre_switch_13C_pulses_umolC": PULSE_C_UMOL * PRE_SWITCH_13C_PULSE_COUNT,
        "full_switch_campaign_total_dose": None,
    },
}

out = Path(__file__).with_name("reconstruction.json")
out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
