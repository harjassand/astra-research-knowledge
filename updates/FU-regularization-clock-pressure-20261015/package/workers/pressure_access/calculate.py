"""Conditional arithmetic for the pressure-write audit; no material prediction.

Run with Python 3.10+. Inputs are proposed geometry or explicitly cited constants.
No stress strength, activation energy, critical-current law, COP or yield is fitted.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
MU0 = 4 * math.pi * 1e-7
KB = 1.380649e-23


def calculate():
    width, thickness, length = 60e-6, 20e-6, 50e-6
    current_density = 1000 * 1e6  # A/mm^2 -> A/m^2
    criterion = 1e-6 / 1e-2  # microvolt/cm -> V/m
    area = width * thickness
    current = current_density * area
    voltage = criterion * length
    power = current * voltage
    radius_cm, moment_over_field = 42.5e-4, 1.9e-8
    fraction = math.pi * moment_over_field / radius_cm**3
    t_hot = 300
    volumes = [(diagonal**2 / 2) * 20e-6 for diagonal in [80e-6, 100e-6, 120e-6]]
    hold_hours = (725-25)/200 + 1 + (860-725)/300 + 3 + (860-600)/1 + (600-25)/200
    outputs = {
        "status": "CONDITIONAL_ARITHMETIC_ONLY_NO_PHYSICAL_MEASUREMENT",
        "proposed_bridge": {
            "width_m": width, "thickness_m": thickness, "voltage_spacing_m": length,
            "area_m2": area, "J_A_per_m2": current_density, "E_V_per_m": criterion,
            "current_A": current, "voltage_V": voltage,
            "resistance_ohm": voltage/current, "segment_electrical_loss_W": power,
            "segment_power_density_W_per_m3": current_density*criterion,
            "current_ratio_to_source_0p2mA": current/0.0002,
            "current_ratio_to_source_50mA": current/0.05,
            "infinite_sheet_B_face_T": MU0*current_density*thickness/2,
            "sheet_approximation_scope": "Uniform infinite sheet; not rectangular-edge field prediction",
            "Lorentz_force_N_at_0p1T_over_voltage_segment": current*0.1*length,
            "contacts_parametric_only": [
                {"one_contact_R_ohm": resistance,
                 "one_contact_loss_W": current**2*resistance,
                 "ratio_to_segment_criterion_loss": current**2*resistance/power}
                for resistance in [1e-6, 1e-3]
            ],
        },
        "source_shielding_formula_replay": {
            "formula": "pi * (|M|/H) / r_cm**3",
            "inputs": {"M_over_H_emu_per_Oe": moment_over_field, "r_cm": radius_cm},
            "estimate": fraction,
            "scope": "70 K geometry-dependent estimate; not enhanced-temperature phase fraction",
            "radius_sensitivity_not_measurement_error_bar": [
                {"r_multiplier": mult, "fraction": fraction/mult**3}
                for mult in [0.90, 0.95, 1.00, 1.05, 1.10]
            ],
        },
        "source_square_volume_replay": [
            {"diagonal_um": diagonal, "volume_m3": volume,
             "volume_nL": volume/1e-12, "copies_per_cm3_only_volume_ratio": 1e-6/volume}
            for diagonal, volume in zip([80, 100, 120], volumes)
        ],
        "force_requirement": {"pressure_Pa": 1e10, "area_m2": 1e-4, "force_N": 1e6,
                              "scope": "Force only. Compression energy requires measured loading path."},
        "Carnot_minimum_work_per_heat_at_300K": {
            str(cold): (t_hot-cold)/cold for cold in [4.2, 20, 77, 100, 133, 140, 151]
        },
        "ideal_refrigerator_work_ratio_77K_to_140K_same_heat": ((300-77)/77)/((300-140)/140),
        "growth_schedule_arithmetic": {
            "assumed_room_temperature_C_for_ramp_arithmetic": 25,
            "pre_postanneal_hours": hold_hours,
            "including_5_day_postanneal_hours": hold_hours + 120,
            "including_10_day_postanneal_hours": hold_hours + 240,
            "scope": "Source schedule only; excludes setup, gas handling, quench, yield and qualification.",
        },
        "Johnson_noise_at_140K_parametric_not_instrument_spec": [
            {"source_resistance_ohm": resistance,
             "V_per_sqrt_Hz": math.sqrt(4*KB*140*resistance)}
            for resistance in [1, 100]
        ],
        "averaging_example_not_acquired_noise": {
            "assumed_independent_pair_sigma_V": 50e-9,
            "target_5_sigma_total_V": 5e-9,
            "N_pairs": math.ceil((5*50e-9/5e-9)**2),
            "scope": "Illustrative only; no bias/drift removal and no acquired noise assumption.",
        },
        "binomial_zero_failures_one_sided_95_percent": {
            "n_59_upper_failure_probability": 1-0.05**(1/59),
            "n_299_upper_failure_probability": 1-0.05**(1/299),
            "scope": "Independent same-protocol trials only; no service-life extrapolation.",
        },
        "unacquired_material_inputs": [
            "same-state extracted I-V(T,B,orientation,t)", "enhanced-phase connected geometry",
            "residual-pressure requirement p_star", "complement mean hydrostatic tension bound S",
            "storage variable and relaxation kinetics", "contact heat and thermal conductance",
            "actual refrigerator COP", "qualified preparation yield", "service lifetime",
            "loading deformation trajectory", "engineering current density with package",
        ],
    }
    assert math.isclose(current, 1.2)
    assert math.isclose(voltage, 5e-9)
    assert math.isclose(power, 6e-9)
    assert 0.77 < fraction < 0.79
    assert math.isclose(volumes[1]/1e-12, 0.1)
    assert math.isclose(1e-6/volumes[1], 10_000_000)
    return outputs


if __name__ == "__main__":
    result = calculate()
    destination = HERE / "calculations.json"
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(destination)
