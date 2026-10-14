#!/usr/bin/env python3
"""Reproduce report scales; every nonconstant input is source-derived or labeled."""
from __future__ import annotations

import json
import math
from pathlib import Path

OUT = Path(__file__).with_name("calculation_results.json")

# Lizée et al. Fig. 4(f): visual estimates from the plotted trace only.
# The graph spans about 0..3.5 s and about ten cycles; current extrema are
# approximately +6.5 and -3.0 nA, and the red position trace is about +/-6 um.
f_hz = 10.0 / 3.5
position_amplitude_um = 6.0
current_peak_amplitude_na = (6.5 - (-3.0)) / 2.0
drop_diameter_um = 10.0
v_peak_um_s = 2.0 * math.pi * f_hz * position_amplitude_um
sigma_visual_na_s_um2 = current_peak_amplitude_na / (drop_diameter_um * v_peak_um_s)

# Equilibrium Johnson-current-noise floors for reported 300 K samples with
# reported 300 ohm--2 kohm resistance. The 1-Hz bandwidth is explicitly chosen
# only to express a spectral-density scale as RMS; actual noise/SNR is unknown.
k_B = 1.380649e-23  # J/K, exact SI constant
temperature_K = 300.0  # room-temperature illustrative input, not a measured value
resistances_ohm = [300.0, 2000.0]
johnson_sample_conductance_S = [1.0 / max(resistances_ohm), 1.0 / min(resistances_ohm)]
johnson_A_sqrtHz = [math.sqrt(4.0 * k_B * temperature_K / r) for r in resistances_ohm]
johnson_only_snr_1Hz = [
    current_peak_amplitude_na * 1e-9 / x for x in johnson_A_sqrtHz
]

# Coquinot et al. PNAS 121 (2024), model-only one-CNT estimate:
# 40 pA short-circuit at 1 bar, R_int ~= 13 Gohm, Z ~= 11.
pressure_Pa = 1.0e5
current_short_A = 40.0e-12
resistance_internal_ohm = 13.0e9
conductance_S = 1.0 / resistance_internal_ohm
cross_coefficient_A_Pa = current_short_A / pressure_Pa
figure_of_merit_Z = 11.0
# From the reported linear two-port matrix and Z=C^2/(L G-C^2):
permeance_m3_s_Pa = (
    cross_coefficient_A_Pa**2 / conductance_S
    * (1.0 + 1.0 / figure_of_merit_Z)
)
flow_short_m3_s = permeance_m3_s_Pa * pressure_Pa
voltage_open_V = current_short_A / conductance_S
electric_power_max_W = current_short_A**2 * resistance_internal_ohm / 4.0
efficiency_at_max_power = figure_of_merit_Z / (2.0 * (figure_of_merit_Z + 2.0))
hydraulic_power_at_max_power_W = electric_power_max_W / efficiency_at_max_power
hydraulic_power_at_short_W = flow_short_m3_s * pressure_Pa
johnson_model_A_sqrtHz = math.sqrt(4.0 * k_B * temperature_K / resistance_internal_ohm)

result = {
    "source_scopes": {
        "lizee_visual": "Approximate digitization from Fig. 4(f), not a tabulated measurement or pressure coefficient.",
        "johnson": "Equilibrium resistor floor at an illustrative 300 K; 1 Hz bandwidth; not measured device/amplifier noise.",
        "coquinot": "Published theoretical model estimates only; no experimental CNT wet-generator measurement. Rounded source values propagate rounding."
    },
    "lizee_fig4f_visual_estimate": {
        "frequency_hz": f_hz,
        "position_amplitude_um": position_amplitude_um,
        "current_peak_amplitude_na": current_peak_amplitude_na,
        "drop_diameter_um": drop_diameter_um,
        "peak_speed_um_s": v_peak_um_s,
        "sigma_ef_visual_na_s_um2": sigma_visual_na_s_um2,
        "note": "Current trace is asymmetric and has an offset; neither this value nor sigma_ef is the channel transport coefficient C_he."
    },
    "lizée_reported_resistance_johnson_floor": {
        "temperature_K_illustrative": temperature_K,
        "resistance_ohm_order": resistances_ohm,
        "inverse_two_terminal_conductance_S_order": johnson_sample_conductance_S,
        "current_noise_A_sqrtHz_order": johnson_A_sqrtHz,
        "current_noise_pA_sqrtHz_order": [x * 1e12 for x in johnson_A_sqrtHz],
        "visual_current_amplitude_over_1Hz_johnson_floor_only": johnson_only_snr_1Hz,
        "actual_SNR": "UNKNOWN"
    },
    "coquinot_single_CNT_model_only": {
        "pressure_Pa": pressure_Pa,
        "short_circuit_current_A": current_short_A,
        "C_he_A_per_Pa": cross_coefficient_A_Pa,
        "internal_resistance_ohm": resistance_internal_ohm,
        "G_S": conductance_S,
        "open_circuit_voltage_V": voltage_open_V,
        "Z": figure_of_merit_Z,
        "derived_model_permeance_m3_per_s_per_Pa": permeance_m3_s_Pa,
        "derived_model_short_circuit_flow_m3_per_s": flow_short_m3_s,
        "derived_model_short_circuit_flow_fL_per_s": flow_short_m3_s * 1e18,
        "derived_model_hydraulic_power_short_circuit_W": hydraulic_power_at_short_W,
        "matched_load_power_max_W": electric_power_max_W,
        "efficiency_at_matched_load_max_power": efficiency_at_max_power,
        "hydraulic_power_at_matched_load_max_power_W": hydraulic_power_at_max_power_W,
        "johnson_current_noise_A_sqrtHz_300K": johnson_model_A_sqrtHz,
        "actual_experimental_K_C_G": "UNKNOWN"
    }
}

OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
