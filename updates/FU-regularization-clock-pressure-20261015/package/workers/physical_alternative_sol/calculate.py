#!/usr/bin/env python3
"""Source-number arithmetic only; this is not a new device simulation.

Run from any directory. All physical inputs are reported in Sawant et al.,
Adv. Optical Mater. (2025), DOI 10.1002/adom.202500775, sections 2 and 3.
No efficiency, lifetime, or material property is fitted or assumed.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def transmission(loss_db):
    return 10.0 ** (-loss_db / 10.0)

inputs = {
    "source": "https://doi.org/10.1002/adom.202500775",
    "phase_patch_length_um": 1.5,
    "phase_change_deg": 55.0,
    "table_phase_slope_deg_per_um": 37.0,
    "crystalline_propagation_loss_db_per_um": 5.7,
    "write_energy_j": 100e-12,
    "erase_energy_j": 7.4e-9,
    "write_pulse_s": 400e-12,
    "erase_pulse_s": 1.2e-6,
    "endurance_cycle_period_s": 50e-6,
}
results = {"inputs": inputs}
alpha = inputs["crystalline_propagation_loss_db_per_um"]
length = inputs["phase_patch_length_um"]
slope = inputs["phase_change_deg"] / length
cycle_j = inputs["write_energy_j"] + inputs["erase_energy_j"]
results["observed_geometry_arithmetic"] = {
    "phase_slope_from_patch_deg_per_um": slope,
    "active_crystalline_propagation_loss_db": alpha * length,
    "active_crystalline_propagation_transmission": transmission(alpha * length),
    "complete_cycle_optical_energy_j": cycle_j,
    "erase_fraction_of_complete_cycle_energy": inputs["erase_energy_j"] / cycle_j,
    "erase_to_write_energy_ratio": inputs["erase_energy_j"] / inputs["write_energy_j"],
    "complete_cycle_average_optical_power_at_reported_rate_w": cycle_j / inputs["endurance_cycle_period_s"],
    "nominal_energy_for_1e9_cycles_j": cycle_j * 1e9,
    "nominal_time_for_1e9_cycles_hours": 1e9 * inputs["endurance_cycle_period_s"] / 3600,
}
results["conditional_fixed_geometry_extrapolation"] = {}
for name, beta in [("from_measured_patch", slope), ("from_rounded_table_slope", inputs["table_phase_slope_deg_per_um"])]:
    lpi = 180 / beta
    losspi = alpha * lpi
    results["conditional_fixed_geometry_extrapolation"][name] = {
        "phase_slope_deg_per_um": beta,
        "pi_length_um": lpi,
        "crystalline_pi_loss_db": losspi,
        "crystalline_pi_transmission": transmission(losspi),
        "input_photon_multiplier_for_equal_detected_photons": 1 / transmission(losspi),
        "maximum_phase_deg_under_1db_crystalline_propagation_loss": beta / alpha,
        "maximum_phase_deg_under_3db_crystalline_propagation_loss": 3 * beta / alpha,
    }
results["scope"] = {
    "established": "Arithmetic on source-reported values and a conditional constant-slope extension of its fixed geometry.",
    "not_established": [
        "A measured pi phase shifter", "A new physical effect", "A universal phase-loss bound",
        "A high-endurance low-loss directional coupler using these pulses",
        "Long dark retention", "Wall-plug energy", "Network throughput advantage",
        "Independent experimental replication", "Astra mission achievement"
    ],
    "extrapolation_premise": "The measured phase and crystalline propagation-loss slopes persist when the same cross section is lengthened. No claim beyond this premise is made.",
    "boundary": "The 5.7 dB/um value is absolute crystalline propagation loss. It must not be identified with another paper's crystalline-minus-amorphous excess loss.",
}
out = ROOT / "calculations.json"
out.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
