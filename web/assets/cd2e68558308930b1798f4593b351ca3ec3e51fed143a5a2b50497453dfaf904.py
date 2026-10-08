#!/usr/bin/env python3
"""Cross-paper dimensional audit of a moving-frame Fog surface-pool model.

This is a conditional model check, not an inference that the slow FCS component
is receptor-bound or that its length equals the downstream MyoII length.
Lengths use the linear front-frame equation

    D b'' + v_rel b' - k b = 0,

whose decaying solution b ~ exp(-x/lambda) has

    lambda = 2 D / (v_rel + sqrt(v_rel**2 + 4 D k)).

The k=0 limit lambda=D/v_rel is a maximum range for k>=0 in this model.
"Reported +/-" values are used only as interval endpoints; they mix source
reports of SEM and SD and are not confidence intervals.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path


# Primary-source reported means; conversions are explicit.
V_UM_PER_MIN = 2.2  # 2019 Nature: 2.2 +/- 0.2 um/min, about one row / 3 min
V_ERR_UM_PER_MIN = 0.2
D_FREE_UM2_PER_S = 55.0  # 2026 Nature Communications, Fog::YFP, extracellular
D_SLOW_UM2_PER_S = 1.6  # 2026 Nature Communications, slow apical Fog::YFP pool
D_SLOW_ERR_UM2_PER_S = 0.2
OBSERVED_ZONE_UM = 70.0  # 2026 Fogslow profile bins extend to 70 um

# 2026 Nature Communications MyoII exponential lengths (um).
MYOII_LENGTHS = {
    "WT": (3.18, 0.29),
    "two_extra_fog_copies": (5.26, 0.58),
    "gprk2_RNAi": (5.48, 0.58),
}


def clearance_rate_for_length(D: float, v_um_min: float, length: float) -> float:
    """Invert the moving-frame characteristic equation; k in s^-1."""
    v = v_um_min / 60.0
    return D / length**2 - v / length


def moving_length(D: float, v_um_min: float, k_s: float) -> float:
    """Positive decay length for D>0, v>=0, k>=0."""
    v = v_um_min / 60.0
    return 2.0 * D / (v + math.sqrt(v * v + 4.0 * D * k_s))


def corner_interval(fn, values):
    out = [fn(*corner) for corner in itertools.product(*[(m - e, m + e) for m, e in values])]
    return [min(out), max(out)]


def main() -> None:
    v = V_UM_PER_MIN
    v_s = v / 60.0
    lmax_free = D_FREE_UM2_PER_S / v_s
    lmax_slow = D_SLOW_UM2_PER_S / v_s

    results = {
        "status": "conditional dimensional/model audit; no biological parameter identified",
        "units": {"length": "um", "velocity": "um/s", "diffusivity": "um^2/s", "clearance": "s^-1"},
        "inputs": {
            "front_speed_um_per_min": {"mean": V_UM_PER_MIN, "reported_error": V_ERR_UM_PER_MIN, "source_note": "2019 Nature; reported as one cell row per ~3 min"},
            "Fog_fast_D_um2_per_s": D_FREE_UM2_PER_S,
            "Fog_slow_D_um2_per_s": {"mean": D_SLOW_UM2_PER_S, "reported_error": D_SLOW_ERR_UM2_PER_S, "source_note": "2026 Nature Communications; slow apical pool is interpreted as membrane-associated, not proven receptor-bound"},
            "MyoII_length_um": {k: {"mean": m, "reported_error": e} for k, (m, e) in MYOII_LENGTHS.items()},
        },
        "moving_frame_zero_clearance_range": {
            "free_Fog_um": lmax_free,
            "slow_surface_pool_um": lmax_slow,
            "slow_pool_corner_interval_um": corner_interval(
                lambda D, vv: D / (vv / 60.0),
                [(D_SLOW_UM2_PER_S, D_SLOW_ERR_UM2_PER_S), (V_UM_PER_MIN, V_ERR_UM_PER_MIN)],
            ),
            "interpretation": "For this linear moving-frame model and nonnegative clearance, the excess-field decay length cannot exceed D/v_rel.",
        },
        "front_vs_diffusion_time_over_70um": {
            "front_sweep_time_s": OBSERVED_ZONE_UM / v_s,
            "free_Fog_diffusion_time_L2_over_2D_s": OBSERVED_ZONE_UM**2 / (2.0 * D_FREE_UM2_PER_S),
            "slow_pool_diffusion_time_L2_over_2D_s": OBSERVED_ZONE_UM**2 / (2.0 * D_SLOW_UM2_PER_S),
            "free_Fog_Peclet_vL_over_D": v_s * OBSERVED_ZONE_UM / D_FREE_UM2_PER_S,
            "slow_pool_Peclet_vL_over_D": v_s * OBSERVED_ZONE_UM / D_SLOW_UM2_PER_S,
            "warning": "Uses cross-paper v as a proxy for v_rel and FCS D values; exact same-condition material-frame quantities must be acquired.",
        },
        "effective_clearance_if_MyoII_length_equals_bound_pool_length": {},
        "cell_local_wave_timed_competitor": {},
        "falsification_thresholds": {},
    }

    kvals = {}
    for condition, (length, err) in MYOII_LENGTHS.items():
        k_slow = clearance_rate_for_length(D_SLOW_UM2_PER_S, v, length)
        k_free = clearance_rate_for_length(D_FREE_UM2_PER_S, v, length)
        kslow_range = corner_interval(
            clearance_rate_for_length,
            [(D_SLOW_UM2_PER_S, D_SLOW_ERR_UM2_PER_S), (V_UM_PER_MIN, V_ERR_UM_PER_MIN), (length, err)],
        )
        kfree_range = corner_interval(
            clearance_rate_for_length,
            [(D_FREE_UM2_PER_S, 0.0), (V_UM_PER_MIN, V_ERR_UM_PER_MIN), (length, err)],
        )
        kvals[condition] = k_slow
        results["effective_clearance_if_MyoII_length_equals_bound_pool_length"][condition] = {
            "slow_pool_k_mean_s^-1": k_slow,
            "slow_pool_k_corner_interval_s^-1": kslow_range,
            "slow_pool_mean_lifetime_s_if_first_order": 1.0 / k_slow if k_slow > 0 else None,
            "free_pool_k_mean_s^-1": k_free,
            "free_pool_k_corner_interval_s^-1": kfree_range,
            "note": "This inversion is invalid unless MyoII length is proportional to the same transported ligand field; the 2026 paper measures integrin cofactor effects that can break that assumption.",
        }
        results["cell_local_wave_timed_competitor"][condition] = {
            "tau_s_for_lambda_equals_v_times_tau": length / v_s,
            "note": "A per-cell exponential response indexed by contact/activation time creates the same moving-frame exponential length, without lateral ligand transport; this is a comparator, not an identified biology.",
        }

    results["effective_clearance_if_MyoII_length_equals_bound_pool_length"]["WT_to_gprk2_RNAi_slow_pool_k_ratio"] = (
        kvals["WT"] / kvals["gprk2_RNAi"] if kvals["gprk2_RNAi"] > 0 else None
    )
    max_v_for_extent = D_SLOW_UM2_PER_S / 70.0 * 60.0
    results["falsification_thresholds"] = {
        "largest_extent_without_clearance_or_local_gain_at_current_v_um": lmax_slow,
        "relative_front_speed_needed_for_70um_extent_at_zero_clearance_um_per_min": max_v_for_extent,
        "condition": "If same-condition cell-relative speed exceeds this threshold and an excess Fogslow profile is verified over 70 um, the passive bound-pool model cannot explain that extent without local gain, a broader source/contact gate, or a different effective diffusivity.",
    }

    out = Path(__file__).with_name("front_length_audit.json")
    out.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
