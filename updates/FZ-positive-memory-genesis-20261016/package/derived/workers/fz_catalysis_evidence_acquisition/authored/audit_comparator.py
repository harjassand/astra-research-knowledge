#!/usr/bin/env python3
"""Reconcile condition-specific Wang Chem2026 statements, not raw data replication."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "external_excluded_from_publication"
PINS = {
    "Chem2026_candidate_mmc1.pdf": "6cf02fe35f7d972b91a28b8fe763c2b08290d94b93edc754a233921a276103c1",
    "Chem2026_candidate_mmc2.pdf": "7ff94ced84217f2be124c35d571275728bb05851358076bf0a26100084a8a365",
}
for name, digest in PINS.items():
    assert hashlib.sha256((EXT / name).read_bytes()).hexdigest() == digest

# Explicit standard-volume scenario, not an experimentally verified flow reference.
R_L_atm = 0.082057366080960
standard_T_K = 273.15
total_gas_L = 2 * 200 * 60 / 1000
reported_consumed_mol = 5.36e-3
crude_feed_A_mol = total_gas_L * .005 / (R_L_atm * standard_T_K)
caption_pure_feed_A_mol = total_gas_L * .35 / (R_L_atm * standard_T_K)
result = {
    "doi": "10.1016/j.chempr.2026.103063",
    "source_sha256": PINS,
    "source_versions": {"online_publication": "2026-05-05", "issue": "Chem12,103063,2026-10-08", "pdf_metadata_created": "2026-10-07"},
    "main_Fig3G_200h_condition": {
        "catalyst": "Cu nanowire arrays", "DMF_electrolyte_volume_mL": 250,
        "supporting_electrolyte": "0.1M Bu4NBF4", "default_DMF_to_water_volume_ratio": 20,
        "C2H2_fraction": .005, "C2H4_fraction": .20, "Ar_fraction": .795,
        "flow_sccm": 2, "current_mA": 15, "current_density_mA_cm2": 1},
    "separate_main_Fig3E_S29_high_throughput_condition": {"flow_sccm": 100, "configuration": "two electrolytic cells", "residual_acetylene_ppm_reported": 3, "status": "not established as 200h at100sccm"},
    "separate_energy_conditions_reported": [
        {"supporting_electrolyte_M": .1, "current_mA": 5, "cell_V_approx": 2.5, "kWh_per_kg_newly_generated_C2H4": 8.51},
        {"supporting_electrolyte_M": 1, "cell_V_approx": 1.7, "kWh_per_kg_newly_generated_C2H4": 5.80}],
    "SI31_condition_reconciliation": {
        "source": "79-page SI PDF, physical page50, FigS31 and note",
        "caption": {"DMF_mL": 70, "C2H2_fraction": .35, "flow_sccm": 2, "current_mA": 100},
        "plot_DMF_mL_approx": 237,
        "note_A_consumed_mmol": 5.36,
        "note_water_loss_mL_approx": .1,
        "explicit_standard_volume_scenario_T_K": standard_T_K,
        "A_feed_mmol_0p5percent2sccm200h": crude_feed_A_mol * 1000,
        "A_feed_mmol_35percent2sccm200h": caption_pure_feed_A_mol * 1000,
        "caption_feed_to_note_consumption_ratio": caption_pure_feed_A_mol / reported_consumed_mol,
        "feed_fraction_ratio_independent_of_standard_T": .35/.005,
        "status": "caption, plot and note condition identity unresolved, not repaired by substitution"},
    "assay_status": {
        "authors_reported_replicates": 3,
        "GC_FID_and_TCD": True,
        "SI10_calibration_curve_plots": "acquired, displayedR2=.999",
        "SI11_SI12_chromatogram_and_GCMS_plots": "acquired as PDF figures",
        "raw_instrument_exports": "not acquired",
        "near_ppm_LOQ_validation": "not established from acquired records"},
    "decision": "essential-output comparator; no matched superiority, complete-cost parity or independent physical validation claimed"
}
assert .99 < crude_feed_A_mol/reported_consumed_mol < 1.01
assert 69 < caption_pure_feed_A_mol/reported_consumed_mol < 71
(ROOT/"authored"/"comparator_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"crude_feed_mmol":crude_feed_A_mol*1000,"SI_caption_feed_mmol":caption_pure_feed_A_mol*1000,"ratio_to_SI_consumption":caption_pure_feed_A_mol/reported_consumed_mol}))
