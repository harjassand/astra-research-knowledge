#!/usr/bin/env python3
"""Arithmetic screening of proposed oxidative covalent isotope fractionation.

No new experiment, fitted kinetic rate, raw-workbook reanalysis, or validated
separator is represented here. Targets are design tests, not measured outcomes.

Reported operating coverage and electrolyte concentration:
Soong et al., Nature Communications 16, 10741 (2025).
https://doi.org/10.1038/s41467-025-65771-3

The reported coverage is not a proved material capacity ceiling. All per-area
projections below assume that coverage; scaling and accessible area are unknown.
"""
from __future__ import annotations
import json
import math
import sys
from pathlib import Path

NA = 6.02214076e23                  # mol^-1
FARADAY = 96485.33212               # C mol^-1
M_D_KG_MOL = 2.01410177812e-3      # kg per mole of D atoms
KB_EV_K = 8.617333262145e-5
COVERAGE_ATOMS_M2 = 1e18           # reported approximate operating coverage

def check_fraction(x: float, name: str) -> None:
    if not math.isfinite(x) or not 0 < x < 1:
        raise ValueError(f"{name} must be finite and strictly between 0 and 1")

def odds(fraction: float) -> float:
    check_fraction(fraction, "fraction")
    return fraction / (1 - fraction)

def enrichment(initial_fraction: float, final_fraction: float) -> float:
    return odds(final_fraction) / odds(initial_fraction)

def rate_ratio_required(a: float, d_recovery: float) -> float:
    if not math.isfinite(a) or a < 1:
        raise ValueError("Enrichment must be finite and at least one")
    check_fraction(d_recovery, "D recovery")
    return 1 + math.log(a) / (-math.log(d_recovery))

def recovery_at_constant_ratio(a: float, ratio: float) -> float:
    if a < 1 or ratio <= 1:
        raise ValueError("Require enrichment >= 1 and rate ratio > 1")
    return math.exp(-math.log(a) / (ratio - 1))

def main() -> dict:
    ns = COVERAGE_ATOMS_M2 / NA
    designs = []
    for initial_d in (0.5, 0.1, 0.05, 0.00015):
        final_d, recovery = 0.95, 0.5
        a = enrichment(initial_d, final_d)
        ratio = rate_ratio_required(a, recovery)
        s_h = recovery / a
        reproduced_final = (initial_d * recovery /
                            (initial_d * recovery + (1-initial_d) * s_h))
        assert math.isclose(reproduced_final, final_d, rel_tol=1e-12)
        assert math.isclose(recovery_at_constant_ratio(a, ratio),
                            recovery, rel_tol=1e-12)
        designs.append({
            "status": "chosen test, not observation",
            "initial_surface_D_atom_fraction": initial_d,
            "final_surface_D_atom_fraction": final_d,
            "D_surface_recovery": recovery,
            "odds_enrichment": a,
            "required_hazard_ratio_bound": ratio,
            "H_surface_recovery": s_h,
            "D_recovery_if_constant_hazard_ratio_is_6":
                recovery_at_constant_ratio(a, 6),
        })

    # Optimistic inventory-only collection illustration: start fully D-loaded;
    # collect 50%; assume no H on surface and only acid contributes carrier H.
    area_m2 = 1e-4
    n_d_mol = ns * area_m2 * 0.5
    purity = 0.95
    carrier_h_budget_mol = n_d_mol * (1 - purity) / purity
    collector_acid_mol_l = 0.18
    v_max_l = carrier_h_budget_mol / collector_acid_mol_l

    # Illustrative productivity: 10% surface D, 50% D recovery, one COMPLETE
    # cycle/s. Neither complete cycle rate nor recovery is experimentally known.
    initial_d, recovery, hz = 0.1, 0.5, 1.0
    output_kg_per_m2_cycle = ns * M_D_KG_MOL * initial_d * recovery
    energy_factor = 1.0 / output_kg_per_m2_cycle / 3.6e6

    result = {
        "status": "unvalidated physical proposal; arithmetic screening only",
        "measurements_not_acquired": {
            "mixed_isotope_stripping_hazards": None,
            "loading_partition_coefficient": None,
            "product_collection_yield_and_purity": None,
            "complete_cycle_time_seconds": None,
            "net_cycle_energy_J_m2": None,
            "separator_endurance_cycles": None,
        },
        "input_reported_operating_coverage_atoms_m2": COVERAGE_ATOMS_M2,
        "coverage_is_not_a_fundamental_upper_bound": True,
        "operating_inventory": {
            "mol_atoms_m2": ns,
            "D_microgram_m2_if_fully_D_loaded": ns*M_D_KG_MOL*1e9,
            "one_electron_charge_C_m2": ns*FARADAY,
        },
        "chosen_selectivity_tests": designs,
        "illustrative_productivity": {
            "assumed_initial_surface_D_fraction": initial_d,
            "assumed_D_recovery": recovery,
            "assumed_complete_cycle_frequency_Hz": hz,
            "D_g_day_m2": output_kg_per_m2_cycle*hz*86400*1000,
            "kWh_per_kg_D_per_J_m2_of_net_cycle_energy": energy_factor,
            "not_an_experimental_performance_prediction": True,
        },
        "collector_inventory_test": {
            "assumed_surface_area_cm2": 1,
            "assumed_initial_surface_D_fraction": 1,
            "assumed_D_collection_recovery": 0.5,
            "target_product_D_atom_fraction": purity,
            "D_mol_collected": n_d_mol,
            "collector_H_concentration_mol_l": collector_acid_mol_l,
            "maximum_collector_volume_pL": v_max_l*1e12,
            "equivalent_uniform_layer_thickness_nm":
                v_max_l*1e-3/area_m2*1e9,
            "scope": "simple liquid collector with equilibrating carrier H only",
            "excludes_unmeasured_aprotic_or_gas_collection_architectures": True,
        },
        "zero_point_energy_caution": {
            "energy_difference_eV": 0.045,
            "temperature_K": 298.15,
            "boltzmann_factor": math.exp(0.045/(KB_EV_K*298.15)),
            "this_is_NOT_a_measured_rate_or_separation_factor": True,
        },
        "cycling_arithmetic": {
            "one_million_cycles_at_1_Hz_days": 1e6/86400,
            "cycles_in_365_days_at_1_Hz": 365*86400,
            "scope": "arithmetic, not a lifetime prediction",
        },
    }
    return result

if __name__ == "__main__":
    result = main()
    text = json.dumps(result, indent=2, allow_nan=False)
    if len(sys.argv) > 2:
        raise SystemExit("Usage: python screening.py [output.json]")
    if len(sys.argv) == 2:
        Path(sys.argv[1]).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
