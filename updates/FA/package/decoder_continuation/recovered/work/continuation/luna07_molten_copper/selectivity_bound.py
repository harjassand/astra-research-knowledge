#!/usr/bin/env python3
"""Reproduce the monovalent common-bath Ag/Cu selectivity bound.

Inputs are the inherited 1273 K Ag-shuttle compositions and the source-reported
infinite-dilution Cu activity coefficient in liquid Ag. This is a thermodynamic
screen for Cu+/Ag+ in a homogeneous shared electrolyte, not a kinetic model or
an electrolysis experiment.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

M_CU_G_MOL = 63.546
M_AG_G_MOL = 107.8682
GAMMA_CU_IN_AG_1273K = 3.76
R_GAS_J_MOL_K = 8.31446261815324
FARADAY_C_MOL = 96485.33212
TEMPERATURE_K = 1273.0
# JANAF tabulates ΔfG° for metastable Cu(l) relative to stable Cu(s) as
# 1.523 kJ/mol at 1200 K and 0.561 kJ/mol at 1300 K. Linear interpolation
# supplies a documented, approximate solid/liquid standard-state correction.
CU_LIQUID_MINUS_SOLID_G_1200_J_MOL = 1523.0
CU_LIQUID_MINUS_SOLID_G_1300_J_MOL = 561.0
CU_LIQUID_MINUS_SOLID_G_1273_J_MOL = (
    CU_LIQUID_MINUS_SOLID_G_1200_J_MOL
    + (TEMPERATURE_K - 1200.0)
    / 100.0
    * (CU_LIQUID_MINUS_SOLID_G_1300_J_MOL - CU_LIQUID_MINUS_SOLID_G_1200_J_MOL)
)


def mole_fraction_cu_from_mass_fraction(w_cu: float) -> float:
    n_cu = w_cu / M_CU_G_MOL
    n_ag = (1.0 - w_cu) / M_AG_G_MOL
    return n_cu / (n_cu + n_ag)


def case(label: str, w_cu: float) -> dict[str, float | str | bool]:
    x_cu = mole_fraction_cu_from_mass_fraction(w_cu)
    a_cu_liquid_standard = GAMMA_CU_IN_AG_1273K * x_cu
    # Ito et al.'s alloy activity is relative to pure liquid Cu. At 1273 K
    # cathodic Cu is stable as a solid. Convert the alloy activity to the
    # common pure-solid standard with JANAF ΔG°(Cu(l)-Cu(s)).
    a_cu_solid_standard = a_cu_liquid_standard * math.exp(
        CU_LIQUID_MINUS_SOLID_G_1273_J_MOL
        / (R_GAS_J_MOL_K * TEMPERATURE_K)
    )
    # Ag is the solvent at <0.4 mass% Cu. The numeric ratio uses a_Ag ~= 1;
    # exact general result is in terms of measured a_Ag/a_Cu.
    a_ag_approx = 1.0
    activity_ratio = a_ag_approx / a_cu_solid_standard
    v_thermal = R_GAS_J_MOL_K * TEMPERATURE_K / FARADAY_C_MOL
    return {
        "label": label,
        "cu_mass_fraction": w_cu,
        "cu_mole_fraction": x_cu,
        "cu_activity_relative_to_pure_liquid": a_cu_liquid_standard,
        "cu_activity_relative_to_stable_pure_solid": a_cu_solid_standard,
        "ag_activity_approximation": a_ag_approx,
        "anode_to_cathode_R_threshold_gap_factor": activity_ratio,
        "nernst_scale_activity_ratio_gap_V": v_thermal * math.log(activity_ratio),
        "selective_window_nonoverlap_if_shared_bath": activity_ratio > 1.0,
    }


def main() -> None:
    results = {
        "scope": "Cu(I)/Ag(I), one homogeneous shared molten electrolyte; alloy anode and pure-metal Cu cathode compared against pure-Ag deposition; all activities dimensionless in same-melt standard states",
        "temperature_K": TEMPERATURE_K,
        "thermal_voltage_V": R_GAS_J_MOL_K * TEMPERATURE_K / FARADAY_C_MOL,
        "source_input_gamma_Cu_in_liquid_Ag": GAMMA_CU_IN_AG_1273K,
        "source_input_gamma_status": "reported-derived infinite-dilution coefficient; not a measurement of electrostripping",
        "Cu_standard_state_correction": {
            "source": "NIST-JANAF Cu(l) table",
            "interpolation_inputs": {"1200_K_delta_G_fusion_J_per_mol": CU_LIQUID_MINUS_SOLID_G_1200_J_MOL, "1300_K_delta_G_fusion_J_per_mol": CU_LIQUID_MINUS_SOLID_G_1300_J_MOL},
            "delta_G_fusion_interpolated_at_1273_K_J_per_mol": CU_LIQUID_MINUS_SOLID_G_1273_J_MOL,
            "method": "linear interpolation of tabulated ΔfG°(Cu(l)) values relative to stable Cu(s); approximate",
        },
        "silver_activity_assumption": "a_Ag approximately 1 in Ag-rich dilute liquid; exact theorem uses a_Ag/a_Cu and needs no numeric approximation",
        "cases": [
            case("lean_regenerated_shuttle", 0.00040908983712882667),
            case("loaded_shuttle_at_regenerator_interface", 0.0037255675322499476),
            case("0.30_mass_percent_Cu", 0.003),
            case("0.40_mass_percent_Cu", 0.004),
        ],
        "symbolic_bounds": {
            "delta_E0_definition": "E0_Ag(I)/Ag(l) - E0_Cu(I)/Cu(s) in the same electrolyte/reference at 1273 K",
            "R_definition": "a_Ag_plus/a_Cu_plus in the homogeneous electrolyte",
            "anode_selective_Cu_dissolution": "R > (a_Ag_alloy/a_Cu_alloy)*exp(-F*delta_E0/(Rgas*T))",
            "cathode_Cu_deposition_before_Ag": "R < exp(-F*delta_E0/(Rgas*T))",
            "ratio_of_lower_anode_bound_to_upper_cathode_bound": "a_Ag_alloy/a_Cu_alloy",
            "nonoverlap_condition": "a_Ag_alloy/a_Cu_alloy > 1",
            "independent_of_delta_E0": True,
        },
        "interpretation": "Thermodynamic non-overlap under stated assumptions. Kinetic Ag suppression, alternative salt speciation/valence, or a divided cell is not excluded and has no qualifying measured Ag-shuttle dataset in this review.",
        "receipt_status": "internally computed arithmetic; inputs are source-derived or inherited scenario values; not experimental validation",
    }
    out = Path(__file__).with_name("bound_results.json")
    out.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
