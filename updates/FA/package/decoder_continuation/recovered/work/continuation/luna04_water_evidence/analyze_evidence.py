#!/usr/bin/env python3
"""Reproduce unit and sensitivity comparisons for the sol04_water interface gate.

Inputs are explicitly labeled as source-reported or inherited model targets.
The CAIX conversion is a hypothetical one-ionization sensitivity, not a measured
surface rate or material bound.
"""
from __future__ import annotations
import json
import math
from pathlib import Path

OUT = Path(__file__).resolve().parent / "analysis_results.json"

# Inherited 50 um water-model operating point, not acquired material data.
ks_target = 3.3464052287581706e-4  # m/s
pco2_source_target_pa = 345.0
pco2_sink_target_pa = 10.4
ph_source_target = 5.196078890000271
ph_sink_target = 5.829408023198054
source_co2_mol_m3 = 0.08760728230459533
source_hco3_mol_m3 = 0.00645037003082904
sink_co2_mol_m3 = 0.0035477176954046706
sink_hco3_mol_m3 = 0.0013367206327524759
keq_mol_m3 = 4.72e-4
source_gross_forward_turnovers_per_site_s = 441.37695

# Hypothetical fully active CA monolayer at 25 nm^2/site.
NA = 6.02214076e23
site_footprint_m2 = 25e-18
site_density_mol_m2 = 1.0 / (site_footprint_m2 * NA)
required_specificity_M_inv_s = 1000.0 * ks_target / site_density_mol_m2

# hCA IX-c reported maximum kcat/KM and low-pH ionization, applied only as a
# one-ionization transfer sensitivity. The original assay was at high salt and
# high bicarbonate and was not a surface assay.
caix_smax_M_inv_s = 13e6
caix_smax_uncertainty_M_inv_s = 1e6
caix_low_pka = 6.6
fu_enzyme_areal_density_per_cm2 = 8.0e11

def caix_sensitivity(ph: float, smax: float) -> dict[str, float]:
    fraction = 1.0 / (1.0 + 10.0 ** (caix_low_pka - ph))
    specificity = smax * fraction
    ks = site_density_mol_m2 * specificity / 1000.0
    return {
        "pH": ph,
        "one_ionization_fraction": fraction,
        "specificity_M_inv_s_assumed": specificity,
        "hypothetical_ks_m_s": ks,
        "fraction_of_target_ks": ks / ks_target,
    }

# Fu et al. (2018) reported maximum permeance, in GPU; this is a gas-throughput
# measure under the paper's own membrane and pressure conditions, not wall ks.
gpu_to_mol_m2_s_pa = 3.34639e-10
fu_permeance_gpu = 2600.0
target_permeance_mol_m2_s_pa = 1.025e-6
target_permeance_gpu = target_permeance_mol_m2_s_pa / gpu_to_mol_m2_s_pa

# 2020 unbuffered bulk absorption assay: report gives 0.5 mg/g protein and 2 g
# solution for Figure 5; 1.5 bar initial total pressure, 30 C. It reports +76%
# initial rate at pH 10. Figure values are approximate visual reads, so not used
# as a precise rate conversion here.
protein_mg_per_g = 0.5
solution_mass_g = 2.0
protein_mg_in_assay = protein_mg_per_g * solution_mass_g

results = {
    "status": "literature does not identify a matched measured surface conductance; values below are source conversions or explicit sensitivities",
    "inherited_model_contract": {
        "ks_target_m_s": ks_target,
        "pCO2_source_target_Pa": pco2_source_target_pa,
        "pCO2_sink_target_Pa": pco2_sink_target_pa,
        "pH_source_target": ph_source_target,
        "pH_sink_target": ph_sink_target,
        "source_CO2_mol_m3": source_co2_mol_m3,
        "source_HCO3_mol_m3": source_hco3_mol_m3,
        "sink_CO2_mol_m3": sink_co2_mol_m3,
        "sink_HCO3_mol_m3": sink_hco3_mol_m3,
        "source_total_CO2_species_mM": source_co2_mol_m3 + source_hco3_mol_m3,
        "sink_total_CO2_species_mM": sink_co2_mol_m3 + sink_hco3_mol_m3,
        "keq_mol_m3": keq_mol_m3,
        "source_drive_mol_m3": source_co2_mol_m3 - (10.0 ** (-ph_source_target) * 1000.0) * source_hco3_mol_m3 / keq_mol_m3,
        "target_net_source_flux_mol_m2_s": ks_target * (source_co2_mol_m3 - (10.0 ** (-ph_source_target) * 1000.0) * source_hco3_mol_m3 / keq_mol_m3),
        "hypothetical_25nm2_monolayer_gross_forward_source_flux_mol_m2_s": site_density_mol_m2 * source_gross_forward_turnovers_per_site_s,
        "hypothetical_gross_forward_to_net_flux_ratio": (site_density_mol_m2 * source_gross_forward_turnovers_per_site_s) / (ks_target * (source_co2_mol_m3 - (10.0 ** (-ph_source_target) * 1000.0) * source_hco3_mol_m3 / keq_mol_m3)),
        "CAIX_assay_25mM_substrate_to_target_source_species_ratio": 25.0 / (source_co2_mol_m3 + source_hco3_mol_m3),
    },
    "caix_25nm2_monolayer_sensitivity_not_measurement": {
        "site_footprint_nm2": 25.0,
        "site_density_mol_m2": site_density_mol_m2,
        "required_effective_specificity_M_inv_s": required_specificity_M_inv_s,
        "measured_kcat_over_KM_max_M_inv_s": caix_smax_M_inv_s,
        "reported_uncertainty_M_inv_s": caix_smax_uncertainty_M_inv_s,
        "reported_uncertainty_note": "The article Results text says 13 +/- 1, while Table 1 says 13.0 +/- 0.1; the calculation uses the wider text range.",
        "reported_low_pKa": caix_low_pka,
        "assay_ionic_strength_M": 0.2,
        "target_background_NaCl_uM_range": [0.1, 1.0],
        "assay_ionic_strength_to_target_background_concentration_ratio": [0.2 / (1.0e-6), 0.2 / (0.1e-6)],
        "source_pH_one_ionization_sensitivity": caix_sensitivity(ph_source_target, caix_smax_M_inv_s),
        "source_pH_low_high_sensitivity": {
            "minus_one_sigma": caix_sensitivity(ph_source_target, caix_smax_M_inv_s - caix_smax_uncertainty_M_inv_s),
            "plus_one_sigma": caix_sensitivity(ph_source_target, caix_smax_M_inv_s + caix_smax_uncertainty_M_inv_s),
        },
        "sink_pH_one_ionization_sensitivity": caix_sensitivity(ph_sink_target, caix_smax_M_inv_s),
        "scope": "Hypothetical one-ionization pH transfer from an 18O equilibrium assay at 25 mM bicarbonate and ionic strength 0.2 M. It is not an immobilized-surface measurement and is not a strict upper bound for other materials or enzyme loadings.",
    },
    "caix_peak_pH_fully_active_monolayer_sensitivity_not_measurement": {
        "assumed_site_footprint_nm2": 25.0,
        "site_density_mol_m2": site_density_mol_m2,
        "reported_peak_specificity_M_inv_s": caix_smax_M_inv_s,
        "hypothetical_ks_at_peak_pH_m_s": site_density_mol_m2 * caix_smax_M_inv_s / 1000.0,
        "fraction_of_target_ks_at_peak_pH": (site_density_mol_m2 * caix_smax_M_inv_s / 1000.0) / ks_target,
        "source_total_substrate_mM": source_co2_mol_m3 + source_hco3_mol_m3,
        "caix_assay_substrate_mM": 25.0,
        "assay_to_target_source_substrate_ratio": 25.0 / (source_co2_mol_m3 + source_hco3_mol_m3),
        "scope": "Optimistic transfer of the published peak free-enzyme specificity to a hypothetical fully active 25 nm^2/site monolayer. The peak value is not at either target pH and the source assay used 25 mM substrate and 0.2 M ionic strength; this is not a measured or material-independent upper bound.",
    },
    "gas_permeance_comparison": {
        "gpu_to_mol_m2_s_pa": gpu_to_mol_m2_s_pa,
        "target_mol_m2_s_pa": target_permeance_mol_m2_s_pa,
        "target_GPU": target_permeance_gpu,
        "Fu2018_reported_max_GPU": fu_permeance_gpu,
        "Fu2018_to_target_ratio": fu_permeance_gpu / target_permeance_gpu,
        "target_shortfall_fraction_at_reported_max": 1.0 - fu_permeance_gpu / target_permeance_gpu,
        "target_source_pCO2_Pa": pco2_source_target_pa,
        "Fu2018_pH_or_temperature_sweep_pCO2_Pa": 0.48e5,
        "Fu2018_source_pressure_ratio_to_target": 0.48e5 / pco2_source_target_pa,
        "Fu2018_20pct_feed_at_0p48bar_pCO2_Pa": 0.20 * 0.48e5,
        "Fu2018_20pct_feed_source_ratio_to_target": (0.20 * 0.48e5) / pco2_source_target_pa,
        "Fu2018_reported_CA_areal_density_per_cm2": fu_enzyme_areal_density_per_cm2,
        "Fu2018_reported_CA_areal_density_mol_m2": fu_enzyme_areal_density_per_cm2 * 1.0e4 / NA,
        "Fu2018_CA_areal_density_over_hypothetical_25nm2_monolayer": (fu_enzyme_areal_density_per_cm2 * 1.0e4 / NA) / site_density_mol_m2,
        "Fu2018_reported_effective_CA_concentration_mM": 3.7,
        "scope": "2600 GPU is an integrated CO2 membrane permeance result under Fu et al.'s own membrane, gas and sink setup. It does not measure the catalytic wall law J=ks(C-HB/Keq).",
    },
    "unbuffered_bulk_assay_2020": {
        "BCA_mg_per_g_solution": protein_mg_per_g,
        "solution_mass_g": solution_mass_g,
        "total_BCA_mg_in_2g_test": protein_mg_in_assay,
        "initial_pressure_bar_abs": 1.5,
        "initial_pressure_ratio_to_target_source_pCO2": 1.5e5 / pco2_source_target_pa,
        "temperature_C": 30.0,
        "observed_unbuffered_pH10_initial_rate_increase_fraction_reported": 0.76,
        "rate_readout": "bulk headspace pressure-decay rate; no membrane area or interfacial species profile reported",
        "scope": "Free BCA in mineral water; not immobilized, not low salt, and not at target pH or gas pressure. No surface conductance can be computed from this cell rate.",
    },
    "particle_near_match_2026": {
        "particle": "uncoated polystyrene, diameter 0.08 um",
        "CO2_driven_PDMS_microchannel_mobility_m2_s": -2.9e-10,
        "Stokes_Einstein_Dp_m2_s": 5.4e-12,
        "reported_Pe": 53.0,
        "source_wall_CO2_mM": 29.5,
        "source_wall_ion_mM": 0.118,
        "scope": "Measured concentration profiles in a bare gas-permeable PDMS channel; mobility is calculated from reported particle parameters. No CA coating, wall mass closure, or particle adhesion coefficient was measured.",
    },
    "matched_surface_conductance_measured_m_s": None,
    "matched_particle_adsorption_velocity_measured_m_s": None,
}
OUT.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
