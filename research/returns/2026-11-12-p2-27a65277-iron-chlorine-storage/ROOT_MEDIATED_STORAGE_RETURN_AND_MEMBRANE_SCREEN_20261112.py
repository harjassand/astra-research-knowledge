"""Conditional engineering screens; no fitted cell or complete-device simulation."""

import json
import math
from pathlib import Path

F = 96485.33212
R = 8.314462618
temperature_K = 298.15
hold_s = 144 * 3600
discharge_s = 100 * 3600
air_oxygen_pressure_Pa = 0.21 * 101325
barrer_SI = 3.35e-16

# A supplied-iron fuel cell's external discharge is two electrons per Fe;
# Faradaic return of its terminal Fe(III) oxide requires three per Fe.
# This scope excludes a changed discharge reaction or another paid return route.
power_and_other_factor = 0.97**2 * 0.99 * 0.98
return_cycle = {
    "discharge_electrons_per_Fe": 2,
    "Faradaic_return_electrons_per_Fe": 3,
    "ideal_external_charge_ratio": 2 / 3,
    "introduced_DC_discharge_mean_V": 0.75,
    "introduced_power_conversion_each": 0.97,
    "introduced_hold_retention": 0.99,
    "introduced_auxiliary_factor": 0.98,
    "mean_return_voltage_ceiling_for_65pct_AC_RTE_V":
        power_and_other_factor * (2 / 3) * 0.75 / 0.65,
    "scope": "No actual charging voltage, electrode or full return cycle is supplied.",
}

# An ideal one-electron mediator with reversible Nernst activities must span
# the chemical driving margins for both reaction directions. Activities are
# treated as ideal fractions only for this hypothetical symmetric example.
mediator_windows = []
for electrons in (1, 2):
    for epsilon in (0.1, 0.05, 0.01, 0.001):
        mediator_windows.append({
            "electrons": electrons,
            "minor_state_fraction": epsilon,
            "symmetric_potential_window_V":
                2 * R * temperature_K / (electrons * F)
                * math.log((1 - epsilon) / epsilon),
        })

# Static homogeneous separator: f = 4 F P dp thold/(l j tdis),
# Vohm = j l/kappa. Thus f*Vohm = K. These parameters must belong
# to the same actual membrane state; no measured material is assumed.
separator_screens = []
for permeability_barrer in (1, 10, 100):
    for conductivity_S_m in (0.01, 0.1):
        permeability = permeability_barrer * barrer_SI
        K = (4 * F * permeability * air_oxygen_pressure_Pa
             / conductivity_S_m * hold_s / discharge_s)
        mean_discharge_V = 0.9
        j_A_m2 = 100
        optimum_V = math.sqrt(K * mean_discharge_V)
        separator_screens.append({
            "hypothetical_oxygen_permeability_Barrer": permeability_barrer,
            "hypothetical_useful_ion_conductivity_S_m": conductivity_S_m,
            "K_hold_fraction_times_Vdrop_V": K,
            "hold_loss_at_25mV_membrane_drop": K / 0.025,
            "minimum_first_order_hold_plus_voltage_loss":
                2 * math.sqrt(K / mean_discharge_V),
            "optimum_membrane_drop_V": optimum_V,
            "optimum_thickness_at_100A_m2_m":
                optimum_V * conductivity_S_m / j_A_m2,
        })

# Example reference inventory: 10 MWh delivered AC at 0.9 V mean DC and
# 97% output conversion. This reference is not pre-inflated for hold loss.
reference_charge_C = 10_000 * 3_600_000 / (0.97 * 0.9)
oxygen_mol_at_one_percent = 0.01 * reference_charge_C / (4 * F)
oxygen_hold = {
    "reference_delivered_AC_MWh": 10,
    "reference_discharge_charge_C": reference_charge_C,
    "four_electron_parasitic_oxygen_mol_at_1pct_loss": oxygen_mol_at_one_percent,
    "equivalent_ideal_ambient_air_headspace_m3":
        oxygen_mol_at_one_percent * R * temperature_K / air_oxygen_pressure_Pa,
    "scope": "Four-electron electrical-equivalent loss model, not every iron phase path.",
}

result = {
    "status": "CONDITIONAL_ANALYTIC_SCREEN_NOT_A_DEVICE_SIMULATION",
    "constants": {
        "F_C_mol": F, "R_J_mol_K": R,
        "T_K": temperature_K, "hold_s": hold_s,
        "discharge_s": discharge_s, "oxygen_dp_Pa": air_oxygen_pressure_Pa,
        "Barrer_in_mol_m_per_m2_s_Pa": barrer_SI,
    },
    "source_specific_return_cycle": return_cycle,
    "ideal_mediator_windows": mediator_windows,
    "hypothetical_separator_screens": separator_screens,
    "reference_oxygen_inventory": oxygen_hold,
}
output = Path(__file__).with_suffix(".json")
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"output": str(output), "return_cycle": return_cycle,
                  "separator_examples": separator_screens,
                  "oxygen_inventory": oxygen_hold}, indent=2))
