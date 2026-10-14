"""Reproduce small arithmetic derivations from the cited primary reports.

Source values are transcribed in this file; outputs are arithmetic only and do
not model carrier generation, dislocation kinetics, or reaction probabilities.
"""

import json
from pathlib import Path

H = 6.62607015e-34  # J s, exact SI value
C = 299_792_458  # m s^-1, exact SI value
LAMBDA_M = 365e-9

# Fonseca Montenegro et al., Fig. 2 / Methods VI.3, 365 nm incident power
# density. Convert mW cm^-2 to W m^-2 (factor 10), then to photons cm^-2 s^-1.
power_mw_cm2 = [0.07, 0.09, 0.29, 0.67]
photon_flux = {
    f"{p:g}_mW_cm-2": {
        "incident_power_W_m-2": p * 10,
        "incident_photons_cm-2_s-1": (p * 10) * LAMBDA_M / (H * C) / 1e4,
    }
    for p in power_mw_cm2
}

# Appendix VIII.2 reports dark-to-light glide reductions for Zn-core and
# S-core TD populations in two film thicknesses. The ratio-change calculation
# is (Zn reduction)/(S reduction); it is not a reaction-probability estimate.
mobility_reductions = {
    "20_nm_film": {"Zn_core_dark_to_light_reduction": 100, "S_core_dark_to_light_reduction": 5},
    "25_nm_film": {"Zn_core_dark_to_light_reduction": 10, "S_core_dark_to_light_reduction": 2},
}
for values in mobility_reductions.values():
    values["Zn_to_S_mobility_ratio_change_factor"] = (
        values["Zn_core_dark_to_light_reduction"]
        / values["S_core_dark_to_light_reduction"]
    )

# Main text gives line densities at N_Al=4e17 and 4e19 cm^-3.
low = {"Zn_core_um-1": 9.1, "S_core_um-1": 5.3}
high = {"Zn_core_um-1": 0.9, "S_core_um-1": 5.0}
doping = {
    "N_Al_low_cm-3": 4e17,
    "N_Al_high_cm-3": 4e19,
    "low_doping_line_density_um-1": low,
    "high_doping_line_density_um-1": high,
    "Zn_core_density_reduction_factor": low["Zn_core_um-1"] / high["Zn_core_um-1"],
    "S_core_density_ratio_low_to_high": low["S_core_um-1"] / high["S_core_um-1"],
    "Zn_to_S_density_ratio_low": low["Zn_core_um-1"] / low["S_core_um-1"],
    "Zn_to_S_density_ratio_high": high["Zn_core_um-1"] / high["S_core_um-1"],
}
doping["change_in_Zn_to_S_density_ratio_factor"] = (
    doping["Zn_to_S_density_ratio_low"] / doping["Zn_to_S_density_ratio_high"]
)

out = {
    "status": "derived_arithmetic_only",
    "source": {
        "paper": "Fonseca Montenegro et al., Phys. Rev. Materials 10, 025003 (2026)",
        "doi": "10.1103/c2hc-lyp2",
        "accessed_version": "arXiv:2506.07908v2 (2025-10-27)",
        "figures_sections": ["Fig. 2", "Fig. 4", "Appendix VIII.2", "Methods VI.3"],
    },
    "optical_incident_photon_flux": {
        "wavelength_nm": 365,
        "exposure_duration_reported": False,
        "absorbed_fraction_or_carrier_density_reported_for_this_measurement": False,
        "values": photon_flux,
    },
    "dark_light_relative_mobility_selectivity": mobility_reductions,
    "growth_doping_line_density_comparison": doping,
    "limits": [
        "Incident photon flux is not absorbed carrier flux or dose.",
        "The relative mobility factors are derived from reported fold reductions, not reaction rates.",
        "Doping densities are growth-integrated line-density observations, not post-growth repair yields.",
    ],
}

Path(__file__).with_name("DERIVATIONS.json").write_text(
    json.dumps(out, indent=2) + "\n", encoding="utf-8"
)
