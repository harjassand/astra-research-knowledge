#!/usr/bin/env python3
"""Reproduce conditional GaAs selective-melting arithmetic.

This is a room-temperature, equal-molar, impulsive thermal-dose model. It does
not identify the 2% optical carrier modulation reported by Fraser et al. with
heat-deposition contrast. There is no phase-selective melt, retained polarity,
or process-cost measurement in this calculation.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

T_REF_K = 298.15
T_M_K = 1514.0
L_FUSION_J_MOL = 106_720.0


def heat_content_relative_to_298(t_k: float) -> float:
    """GaAs(s) Shomate fit, J/mol relative to 298.15 K, valid 800--1514 K.

    Yamaguchi, Itagaki & Yazawa (1989), Table 1, GaAs(s):
    H_T = a*T + b*T**2 + c/T + d, with a=47.3, b=3.99e-3,
    c=2.40e5, d=-1.53e4.
    """
    if not math.isfinite(t_k) or not 800.0 <= t_k <= T_M_K:
        raise ValueError("Published solid fit is valid only on 800--1514 K")
    return 47.3 * t_k + 3.99e-3 * t_k**2 + 2.40e5 / t_k - 1.53e4


def sensible_heat_to_melting(t0_k: float) -> float:
    if t0_k == T_REF_K:
        h0 = 0.0
    else:
        h0 = heat_content_relative_to_298(t0_k)
    return heat_content_relative_to_298(T_M_K) - h0


def contrast_threshold(h_sensible: float, latent: float) -> float:
    return latent / (2.0 * h_sensible + latent)


def molten_fraction_supremum(c: float, h_sensible: float,
                               latent: float) -> float:
    if not math.isfinite(c) or not 0.0 <= c < 1.0:
        raise ValueError("C must be finite and in [0, 1)")
    return min(1.0, 2.0 * c * h_sensible / ((1.0 - c) * latent))


def window(h_sensible: float, latent: float, c: float) -> tuple[float, float]:
    """Open Q interval: full melt hot, protected patch below melt onset."""
    return (h_sensible + latent) / (1.0 + c), h_sensible / (1.0 - c)


def main() -> None:
    rows = []
    for t0 in (T_REF_K, 800.0, 1000.0, 1200.0, 1400.0, 1500.0):
        hs = sensible_heat_to_melting(t0)
        c_star = contrast_threshold(hs, L_FUSION_J_MOL)
        c_below = 0.5 * c_star
        c_above = 0.5 * (1.0 + c_star)
        low_below, high_below = window(hs, L_FUSION_J_MOL, c_below)
        low_above, high_above = window(hs, L_FUSION_J_MOL, c_above)
        assert not low_below < high_below
        assert low_above < high_above
        rows.append({
            "initial_temperature_K": t0,
            "sensible_enthalpy_to_melting_J_per_mol": hs,
            "complete_melt_thermal_contrast_strictly_above": c_star,
            "dose_window_at_half_threshold": {
                "lower_deposited_Qhot_J_per_mol": low_below,
                "upper_deposited_Qprotected_J_per_mol": high_below,
                "nonempty": low_below < high_below,
            },
            "dose_window_at_midpoint_to_one": {
                "contrast": c_above,
                "lower_deposited_Qhot_J_per_mol": low_above,
                "upper_deposited_Qprotected_J_per_mol": high_above,
                "nonempty": low_above < high_above,
            },
        })

    h_room = sensible_heat_to_melting(T_REF_K)
    c_room = contrast_threshold(h_room, L_FUSION_J_MOL)
    apb_before = 0.10
    apb_after = 0.014
    result = {
        "status": "conditional model arithmetic only; no physical validation",
        "thermochemical_source": {
            "citation": "Yamaguchi, Itagaki and Yazawa (1989), DOI 10.2320/jinstmet1952.53.8_764",
            "fit_range_K": [800.0, 1514.0],
            "T_ref_K": T_REF_K,
            "T_m_K": T_M_K,
            "L_fusion_J_per_mol": L_FUSION_J_MOL,
            "source_reported_uncertainty_Tm_K": 1.0,
            "source_reported_uncertainty_L_fusion_J_per_mol": 200.0,
            "source_reported_heat_content_fit_error_J_per_mol": 100.0,
        },
        "room_temperature_selective_complete_melt": {
            "H_sensible_J_per_mol": h_room,
            "contrast_CQ_strictly_greater_than": c_room,
            "minimum_hot_to_cold_deposited_energy_ratio_at_threshold": (1.0 + c_room) / (1.0 - c_room),
            "dose_window_lower_deposited_Qhot_J_per_mol_at_threshold": (h_room + L_FUSION_J_MOL) / (1.0 + c_room),
            "dose_window_upper_deposited_Qprotected_J_per_mol_at_threshold": h_room / (1.0 - c_room),
        },
        "hypothetical_heat_contrast_examples_not_measurements": [
            {
                "assumed_CQ": c,
                "molten_fraction_supremum_before_protected_patch_reaches_Tm": molten_fraction_supremum(c, h_room, L_FUSION_J_MOL),
            }
            for c in (0.02, 0.064, 0.14)
        ],
        "temperature_sensitivity": rows,
        "Barrett_2019_matched_surface_APB_comparator": {
            "as_grown_line_density_per_um": apb_before,
            "after_650C_7_5min_furnace_line_density_per_um": apb_after,
            "fractional_line_density_reduction": 1.0 - apb_after / apb_before,
            "fold_reduction": apb_before / apb_after,
            "retained_phase_selected_displacement_measured": False,
        },
        "not_measured_or_not_inferred": [
            "phase-dependent deposited thermal energy contrast C_Q in any processing regime",
            "phase-selected APB migration or polarity reversal in GaAs",
            "a retained structural state after laser drive removal",
            "incident threshold for a capped GaAs-on-Si 400 nm film",
            "whole-wafer uniformity, yield, wall-plug energy, ramp/cool time, or cost",
            "any identification of Fraser's carrier modulation with heat contrast",
        ],
        "excluded_regimes": [
            "nonthermal carrier-driven structural transition",
            "sustained heating with heat loss",
            "boundary-local bond rearrangement",
            "partial melting and seeded regrowth",
            "laser ablation, As loss, or composition change",
        ],
    }
    out = Path(__file__).resolve().with_name("results.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
