#!/usr/bin/env python3
"""Recompute reported concentration changes and SI regional means; no mass closure assumed."""
from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
R = 8.31446261815324  # J mol^-1 K^-1
F = 96485.33212  # C mol^-1
M_FE = 55.845  # g mol^-1
M_SN = 118.710  # g mol^-1


def number(value: str | None) -> float | None:
    if value is None or not value.strip():
        return None
    return float(value)


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def apparent_removal_pct(before: float | None, after: float | None) -> float | None:
    if before is None or after is None or before == 0:
        return None
    return 100.0 * (before - after) / before


def main() -> None:
    regional = read_csv("ambiru2026-s4-regions.csv")
    preprint = read_csv("ambiru2026-preprint-table1.csv")
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in regional:
        groups[row["run"]].append(row)
    preprint_by_run = {row["run"]: row for row in preprint}
    expected_runs = {str(run) for run in range(1, 17)}
    if len(regional) != 48 or len(preprint) != 16 or len(preprint_by_run) != 16 or set(groups) != expected_runs or set(preprint_by_run) != expected_runs:
        raise ValueError("Expected source transcriptions to cover runs 1 through 16 exactly")
    for run, group in groups.items():
        if len(group) != 3 or {row["region"] for row in group} != {"upper", "middle", "lower"}:
            raise ValueError(f"Run {run} must have exactly upper/middle/lower SI rows")
    for run in ("11", "15", "16"):
        group = sorted(groups[run], key=lambda row: ("upper", "middle", "lower").index(row["region"]))
        sn_values = [row["sn_after_wt_pct"] for row in group]
        expected_sn = {
            "11": ["0.020", "0.004", "0.005"],
            "15": ["0.010", "0.015", "0.047"],
            "16": ["0.009", "0.080", "0.073"],
        }[run]
        if sn_values != expected_sn:
            raise ValueError(f"Run {run} SI Sn values do not match the audited Table S4 transcription")

    results: dict[str, object] = {
        "input_validation": {
            "si_regional_rows": len(regional),
            "si_runs": len(groups),
            "si_regions_per_run": 3,
            "preprint_table1_rows": len(preprint),
            "pinned_si_sn_transcription_wt_pct": {
                "run_11_upper_middle_lower": [0.020, 0.004, 0.005],
                "run_15_upper_middle_lower": [0.010, 0.015, 0.047],
                "run_16_upper_middle_lower": [0.009, 0.080, 0.073],
            },
        },
        "provenance": {
            "regional_source": "Ambiru et al. 2026 published SI Table S4, manually transcribed; caption says Table 1 values are arithmetic means of the three regional assays.",
            "comparison_source": "Author preprint Table 1 as indexed in the ResearchSquare PDF search result; direct PDF route returned 403. It is not represented here as the inaccessible final article table.",
            "units": "wt% concentrations; concentration changes are not element-inventory mass balances.",
        },
        "regional_table1_reconciliation": [],
        "comparisons_of_interest": [],
        "thermochemistry": {},
        "conditional_faraday_equivalents": {},
        "process_baseline": {
            "source": "Paeng and Azimi 2025 ACS Supporting Information, Table S1-S4; 2024 USD assumptions.",
            "cases_per_si_one_tonne_basis": [
                {"case": 1, "feed_molten_steel_kg": 959.20, "reductant_or_desulfurizer_kg": 40.80, "flux_remaining_kg": 1440.00, "new_flux_kg": 480.00, "supply_feS2_or_fe2o3_kg": 96.00, "electricity_kwh": 117.66, "combined_steel_output_kg": 1017.80, "flux_residue_kg": 480.00, "co_g_kg": 78.20, "opex_usd_per_t": 137.64},
                {"case": 2, "feed_molten_steel_kg": 951.80, "reductant_or_desulfurizer_kg": 48.20, "flux_remaining_kg": 1819.90, "new_flux_kg": 296.27, "supply_feS2_or_fe2o3_kg": 105.81, "electricity_kwh": 53.95, "combined_steel_output_kg": 1001.62, "flux_residue_kg": 296.27, "co_g_kg": 104.19, "opex_usd_per_t": 121.27},
                {"case": 3, "feed_molten_steel_kg": 1001.62, "reductant_or_desulfurizer_kg": 56.00, "flux_remaining_kg": 0.00, "new_flux_kg": 0.00, "supply_feS2_or_fe2o3_kg": 0.00, "electricity_kwh": 0.00, "combined_steel_output_kg": 994.74, "flux_residue_kg": 62.88, "co_g_kg": 0.00, "opex_usd_per_t": 41.72},
                {"case": 4, "feed_molten_steel_kg": 994.74, "reductant_or_desulfurizer_kg": 0.00, "flux_remaining_kg": 1940.00, "new_flux_kg": 60.00, "supply_feS2_or_fe2o3_kg": 210.00, "electricity_kwh": 408.08, "combined_steel_output_kg": 1117.75, "flux_residue_kg": 60.00, "co_g_kg": 53.91, "opex_usd_per_t": -56.61},
            ],
            "material_cost_assumptions_usd_per_unit": {
                "scrap_steel_per_t": 313,
                "calcium_aluminate_flux_per_t": 200,
                "pyrite_FeS2_per_t": 250,
                "iron_ore_Fe2O3_per_t": 104,
                "coal_per_t": 132,
                "CaC2_per_t": 650,
                "N2_per_Nm3": 3,
                "ZrB2_per_g": 0.13,
                "water_per_t": 0.69,
                "waste_disposal_per_t": 24,
            },
            "capital_cost_usd_per_t_capacity": {
                "electrorefining_cell": 1584.33,
                "desulfurization": 96.88,
                "EAF": 278.52,
                "continuous_casting": 273.30,
                "hot_strip_mill": 246.53,
            },
            "levelized_hrc_cost_usd_per_t": {"0.43_wt_pct_Cu_scrap": 941.73, "0.21_wt_pct_Cu_scrap": 783.24},
            "unknowns": ["The SI labels four cases but the main-text definitions are not reconstructed from the SI; case ids are preserved as printed.", "The TEA is a model of a Cu/C process, not measured process data for the 2026 Sn/FeS batch screen."]
        },
    }

    analytes = [
        ("Cu", "cu_before_wt_pct", "cu_after_wt_pct"),
        ("Sn", "sn_before_wt_pct", "sn_after_wt_pct"),
        ("Ni", "ni_before_wt_pct", "ni_after_wt_pct"),
        ("Cr", "cr_before_wt_pct", "cr_after_wt_pct"),
    ]
    for run, group in groups.items():
        for element, before_key, after_key in analytes:
            before_values = [row[before_key] for row in group if row[before_key].strip()]
            after_values = [row[after_key] for row in group if row[after_key].strip()]
            if after_values and len(after_values) != 3:
                raise ValueError(f"Run {run} {element} assay must have all three regional values")
            if before_values and len(set(before_values)) != 1:
                raise ValueError(f"Run {run} {element} initial assay differs across regional rows")
    for run in sorted(groups, key=int):
        group = groups[run]
        p = preprint_by_run[run]
        row_out: dict[str, object] = {
            "run": int(run),
            "atmosphere": group[0]["atmosphere"],
            "potential": group[0]["potential"],
            "charge_C": number(group[0]["charge_C"]),
            "regional_measurement_count": len(group),
            "analytes": {},
        }
        for element, before_key, after_key in analytes:
            values = [number(r[after_key]) for r in group]
            values = [v for v in values if v is not None]
            before = number(p[f"{element.lower()}_before_wt_pct"])
            preprint_after = number(p[f"{element.lower()}_after_wt_pct"])
            regional_mean = mean(values)
            if values or before is not None or preprint_after is not None:
                diff = None if regional_mean is None or preprint_after is None else regional_mean - preprint_after
                row_out["analytes"][element] = {
                    "preprint_initial_wt_pct": before,
                    "preprint_table1_after_wt_pct": preprint_after,
                    "si_region_values_wt_pct": values,
                    "si_region_count": len(values),
                    "si_region_mean_wt_pct": regional_mean,
                    "si_region_min_wt_pct": min(values) if values else None,
                    "si_region_max_wt_pct": max(values) if values else None,
                    "preprint_apparent_concentration_removal_pct": apparent_removal_pct(before, preprint_after),
                    "si_mean_apparent_concentration_removal_pct": apparent_removal_pct(before, regional_mean),
                    "mean_minus_preprint_table1_wt_pct": diff,
                    "constant_1000kg_basis_change_kg_t_equivalent": None if before is None or regional_mean is None else (before - regional_mean) * 10.0,
                }
        results["regional_table1_reconciliation"].append(row_out)

    for run in ("7", "9", "11"):
        row = next(x for x in results["regional_table1_reconciliation"] if x["run"] == int(run))
        results["comparisons_of_interest"].append(row)

    temperature = 1873.0
    dg_form = {"SnS_g_kJ_per_mol": -61.338, "FeS_l_kJ_per_mol": -55.124, "Cu2S_l_kJ_per_mol": -71.212, "Ni3S2_l_kJ_per_mol": -116.081, "CrS_s_kJ_per_mol": -96.723}
    reactions = {
        "Sn_exchange": dg_form["SnS_g_kJ_per_mol"] - dg_form["FeS_l_kJ_per_mol"],
        "Cu_exchange_per_Cu2S": dg_form["Cu2S_l_kJ_per_mol"] - dg_form["FeS_l_kJ_per_mol"],
        "Ni_exchange_per_Ni3S2": dg_form["Ni3S2_l_kJ_per_mol"] - 2 * dg_form["FeS_l_kJ_per_mol"],
        "Cr_exchange_per_CrS": dg_form["CrS_s_kJ_per_mol"] - dg_form["FeS_l_kJ_per_mol"],
    }
    results["thermochemistry"] = {
        "temperature_K": temperature,
        "source_standard_formation_gibbs_kJ_per_mol_product": dg_form,
        "exchange_reaction_deltaG0_kJ_per_reaction_extent": reactions,
        "standard_state_quotient_at_equilibrium_K": {k: math.exp(-dg * 1000.0 / (R * temperature)) for k, dg in reactions.items()},
        "caveat": "Standard-state comparison only. Activities, phases/speciation (including listed SnS gas standard), slag/metal partition, and kinetic barriers are not solved.",
    }

    results["conditional_faraday_equivalents"] = {
        "formula": "m = M*|Q|/(n F), conditional on all signed net charge being a single n-electron metal oxidation/reduction; this is not measured metal loss or full-cell energy.",
        "Fe_as_Fe2plus_g": {str(q): M_FE * abs(q) / (2 * F) for q in (19, 110, 844, 12455)},
        "Sn_as_Sn2plus_g": {str(q): M_SN * abs(q) / (2 * F) for q in (19, 110, 844, 12455)},
        "known_lab_basis": {"initial_alloy_g": 30.0, "slag_g_approx": 60.0, "metal_to_slag_mass_ratio": 0.5, "temperature_K": 1873.0, "pre_equilibration_s": 7200, "electrolysis_s": 3600, "gas_flow_L_min": 2.0},
        "sn_inventory_caveat": "At 30 g initial metal, 0.199 wt% Sn is 0.0597 g initially. Final metal mass is not reported, so a concentration decrement cannot be converted into an exact Sn mass transfer.",
    }

    out = ROOT / "results.json"
    out.write_text(json.dumps(results, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(out)
    print("Sn Table1/SI regional means:")
    for row in results["regional_table1_reconciliation"]:
        sn = row["analytes"].get("Sn")
        if sn:
            print(row["run"], row["potential"], sn["preprint_table1_after_wt_pct"], sn["si_region_mean_wt_pct"], sn["preprint_apparent_concentration_removal_pct"], sn["si_mean_apparent_concentration_removal_pct"])


if __name__ == "__main__":
    main()
