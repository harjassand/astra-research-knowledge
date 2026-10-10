#!/usr/bin/env python3
"""Reproduce conditional Faraday and energy bounds for the Sweetman et al. claim.

All reported inputs are transcribed from the primary 2024 paper (see SOURCES.md).
This script does not process raw observations; source XLSX files could not be
downloaded in this environment. It computes what water electrolysis would
require if the paper's reported net O2 flux were real and entirely Faradaic.
"""

from __future__ import annotations

import json

F = 96485.33212  # C mol-1, Faraday constant
SECONDS_PER_DAY = 86400.0
CHAMBER_FOOTPRINT_M2 = 484e-4  # 484 cm2, from Methods
E_REV_V = 1.23  # reversible water-splitting voltage, source paper
E_OPERATING_V = 1.23 + 0.37  # source paper's stated seawater overpotential
E_REPORTED_MAX_V = 0.95  # maximum nodule surface potential reported in text

# Paper-reported DOP range, mmol O2 m-2 d-1, normalized to chamber footprint.
flux_mmol_m2_day = (1.7, 18.0)

rows = []
for flux_mmol_m2_day_i in flux_mmol_m2_day:
    mol_o2_m2_s = flux_mmol_m2_day_i * 1e-3 / SECONDS_PER_DAY
    current_density_A_m2 = 4.0 * F * mol_o2_m2_s
    min_power_density_W_m2 = current_density_A_m2 * E_REV_V
    operating_power_density_W_m2 = current_density_A_m2 * E_OPERATING_V
    chamber_current_A = current_density_A_m2 * CHAMBER_FOOTPRINT_M2
    rows.append(
        {
            "reported_O2_flux_mmol_m2_day": flux_mmol_m2_day_i,
            "Faradaic_current_density_mA_m2": current_density_A_m2 * 1e3,
            "minimum_power_density_mW_m2_at_1p23V": min_power_density_W_m2 * 1e3,
            "power_density_mW_m2_at_1p60V": operating_power_density_W_m2 * 1e3,
            "current_per_484cm2_chamber_mA": chamber_current_A * 1e3,
        }
    )

result = {
    "inputs": {
        "Faraday_constant_C_mol": F,
        "O2_flux_range_mmol_m2_day": list(flux_mmol_m2_day),
        "chamber_footprint_m2": CHAMBER_FOOTPRINT_M2,
        "reversible_voltage_V": E_REV_V,
        "stated_operating_voltage_V": E_OPERATING_V,
        "reported_maximum_nodule_probe_potential_V": E_REPORTED_MAX_V,
    },
    "per_mole_O2": {
        "required_charge_C_mol": 4.0 * F,
        "minimum_work_kJ_mol_at_1p23V": 4.0 * F * E_REV_V / 1000.0,
        "work_kJ_mol_at_0p95V": 4.0 * F * E_REPORTED_MAX_V / 1000.0,
        "work_kJ_mol_at_1p60V": 4.0 * F * E_OPERATING_V / 1000.0,
        "fraction_of_reversible_minimum_available_at_0p95V": E_REPORTED_MAX_V / E_REV_V,
    },
    "flux_requirements": rows,
    "interpretation": (
        "Conditional lower bounds for water electrolysis only. The measured nodule "
        "potentials are open-circuit probe differences, not a demonstrated loaded "
        "cell voltage or charge budget; no conclusion about the O2 observation or "
        "an alternative mechanism follows from this calculation alone."
    ),
}

print(json.dumps(result, indent=2, sort_keys=True))
