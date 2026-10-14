#!/usr/bin/env python3
"""Reproducible scale and ergotropy calculations for the FL molecular audit.

Uses only Python's standard library. Literature values are inputs, not refit
parameters. The collision/unloading calculation is an explicit toy model.
"""

import json
import math
from pathlib import Path

K_B = 1.380649e-23                 # J K^-1, exact SI value
EV_J = 1.602176634e-19             # J, exact SI value
N_A = 6.02214076e23                # mol^-1, exact SI value
H = 6.62607015e-34                 # J s, exact SI value
C = 299792458.0                    # m s^-1, exact SI value
TORR_PA = 101325.0 / 760.0
T_K = 300.0


def passive_rotor_energy_in_units_B(J: int) -> float:
    """Passive energy for a uniform mixture over the (2J+1) m states.

    Rigid-rotor levels are E_j/B = j(j+1) with degeneracy 2j+1.
    The passive rearrangement sorts the 2J+1 equal nonzero eigenvalues into
    the lowest 2J+1 rotor states. This idealized model omits nuclear-spin,
    electronic, and field-selection restrictions.
    """
    slots = 2 * J + 1
    remaining = slots
    energy = 0
    for j in range(J + 1):
        degeneracy = 2 * j + 1
        filled = min(remaining, degeneracy)
        energy += filled * j * (j + 1)
        remaining -= filled
        if remaining == 0:
            break
    assert remaining == 0
    return energy / slots


def ideal_linear_deceleration_return(z: float) -> float:
    """Fraction of initial rotor energy returned under a toy loss hazard.

    Assumes L(t)=L0(1-t/td), E(t)=E0(1-t/td)^2 and a constant hazard
    lambda_loss=z/td that destroys all still-unextracted rotor energy.
    It is not a measured CO2 extraction efficiency.
    """
    if z == 0:
        return 1.0
    return 2.0 * (z - 1.0 + math.exp(-z)) / (z * z)


def net_activation_energy_per_product(r: float, p_productive: float) -> float:
    """E_net/E for one activation attempt, with survivor return r.

    Products consume one E; unsuccessful survivors retain E until return.
    Assumes no other loss, loading work, unloading time, or product recovery.
    """
    if not 0.0 <= r <= 1.0 or not 0.0 < p_productive <= 1.0:
        raise ValueError("r must be in [0,1], p must be in (0,1]")
    s = 1.0 - p_productive
    return (1.0 - r * s) / p_productive


def main() -> None:
    n_co2_380 = (380.0 * TORR_PA) / (K_B * T_K)
    n_co2_50 = (50.0 * TORR_PA) / (K_B * T_K)
    n_h2_sio = 7.0e6 * 1.0e6       # cm^-3 -> m^-3
    p_h2_pa = n_h2_sio * K_B * T_K
    tau_co2_s = 500e-12 / 3.0
    k_react_sio = 0.18 / 60.0
    k_unpumped_sio = 0.05 / 60.0

    e_co2_ev = 6.14
    e_co2_j = e_co2_ev * EV_J
    molar_activation_j_mol = e_co2_j * N_A
    co_kg_mol = 28.0101e-3
    activation_kwh_kg = molar_activation_j_mol / co_kg_mol / 3.6e6

    # Approximate one high-J CO2 delta-J=2 gap with the low-J B constant;
    # actual high-J shifts require centrifugal-distortion constants.
    B_co2_cm = 0.390
    delta_j = B_co2_cm * (364 * 365 - 362 * 363)
    carrier_cm_790nm = 1.0e7 / 790.0

    # Theoretical state-space rearrangement example, normalized by E_J.
    passive = {}
    for J in (57, 170):
        e_initial_over_B = J * (J + 1)
        e_passive_over_B = passive_rotor_energy_in_units_B(J)
        passive[str(J)] = {
            "initial_E_over_B": e_initial_over_B,
            "passive_E_over_B_uniform_m": e_passive_over_B,
            "passive_fraction_of_initial": e_passive_over_B / e_initial_over_B,
            "ergotropy_fraction_uniform_m": 1.0 - e_passive_over_B / e_initial_over_B,
            "assumptions": "rigid rotor; all m states accessible; same electronic/nuclear-spin block",
        }

    unload = {}
    for td_ps in (1, 5, 10, 20, 50, 100, 167):
        z = td_ps / (tau_co2_s * 1e12)
        unload[str(td_ps)] = {
            "collision_exposure_z": z,
            "ideal_return_if_each_collision_erases_remaining_work": ideal_linear_deceleration_return(z),
            "no_collision_probability": math.exp(-z),
        }

    sio_cycles = {}
    for t_s in (1.0, 10.0, 60.0, 300.0):
        p = 1.0 - math.exp(-k_react_sio * t_s)
        s = 1.0 - p
        sio_cycles[str(int(t_s))] = {
            "product_probability": p,
            "survivor_fraction": s,
            "throughput_per_ion_per_s_if_unload_time_zero": p / t_s,
            "activation_E_per_product_at_r_0.99": net_activation_energy_per_product(0.99, p),
            "activation_E_per_product_at_r_0.9999": net_activation_energy_per_product(0.9999, p),
        }

    d2 = {
        "J0_to_J2_rotational_shift_cm-1": 179.0,
        "pump_carrier_wavenumber_cm-1_at_1064nm": 1.0e7 / 1064.0,
        "single_photon_fraction_from_molecular_shift": 179.0 / (1.0e7 / 1064.0),
        "observed_anti-Stokes_power_W": 60e-6,
        "reported_pump_output_power_W": 17.5e-3,
        "anti-Stokes_to_pump_power_ratio": 60e-6 / 17.5e-3,
        "condition": "77 K D2, 10 Torr; this ratio is not an energy-recovery efficiency",
    }

    # Externally triggered coherent two-photon emission in p-H2. The reported
    # photon count is an estimate at the target; output energy below is derived
    # from that count and wavelength, not a separate calorimetric measurement.
    h2_density = 60e3 / (K_B * 78.0)
    h2_partner_photons = 6.0e11
    h2_partner_lambda_m = 5.048e-6
    h2_partner_energy_j = h2_partner_photons * H * C / h2_partner_lambda_m
    h2_trigger_energy_j = 150e-6
    h2_pump_each_j = 5e-3
    h2_rep_rate_hz = 10.0
    h2 = {
        "condition": "para-H2 at 78 K and 60 kPa; coherent Raman preparation plus externally triggered emission",
        "number_density_cm-3_ideal_gas": h2_density / 1e6,
        "reported_vibrational_gap_cm-1": 4161.0,
        "reported_coherence_estimate": 0.04,
        "reported_maximum_coherence": 0.5,
        "reported_partner_wavelength_um": h2_partner_lambda_m * 1e6,
        "reported_partner_photons_per_pulse_at_target": h2_partner_photons,
        "derived_partner_channel_energy_J_per_pulse": h2_partner_energy_j,
        "reported_partner_to_trigger_energy_ratio_approx": 1e-4,
        "derived_partner_energy_ratio_from_photon_count": h2_partner_energy_j / h2_trigger_energy_j,
        "reported_external_trigger_J_per_pulse": h2_trigger_energy_j,
        "reported_drive_energy_each_J_per_pulse": h2_pump_each_j,
        "rep_rate_Hz": h2_rep_rate_hz,
        "derived_partner_channel_average_power_W": h2_partner_energy_j * h2_rep_rate_hz,
        "derived_two_visible_driver_average_power_W": 2 * h2_pump_each_j * h2_rep_rate_hz,
        "reported_first_anti-Stokes_to_partner_intensity_ratio_approx": 50.0,
        "status": "coherent emitted channel; not total optical balance, net work recovery, or chemistry-compatible cycle",
    }

    out = {
        "status": "derived estimates; no lab measurement reproduced",
        "gas_state_assumption": {"temperature_K": T_K, "ideal_gas": True},
        "co2_380Torr": {
            "number_density_m-3": n_co2_380,
            "number_density_cm-3": n_co2_380 / 1e6,
            "mean_collision_time_s_inferred_from_500ps_per_3_collisions": tau_co2_s,
            "collision_rate_s-1": 1.0 / tau_co2_s,
            "J364_tail_energy_eV_per_molecule": e_co2_ev,
            "molar_energy_kJ_mol": molar_activation_j_mol / 1000.0,
            "activation_energy_kWh_per_kg_CO_if_one_J364_activation_per_CO": activation_kwh_kg,
            "delta_J_364_to_362_cm-1_rigid_B_approx": delta_j,
            "790nm_carrier_wavenumber_cm-1": carrier_cm_790nm,
            "one_step_Raman_gap_fraction_of_790nm_carrier": delta_j / carrier_cm_790nm,
            "pulse_energy_at_sample_J": [0.004, 0.007],
            "amplifier_repetition_rate_Hz": 10,
            "actual_molecular_energy_transfer_efficiency": None,
            "number_of_excited_molecules_per_shot": None,
        },
        "co2_50Torr_number_density_cm-3": n_co2_50 / 1e6,
        "sio_plus_h2": {
            "H2_density_cm-3_reported": n_h2_sio / 1e6,
            "equivalent_ideal_gas_pressure_Pa_at_300K": p_h2_pa,
            "equivalent_pressure_Torr_at_300K": p_h2_pa / TORR_PA,
            "density_ratio_CO2_380Torr_to_H2_in_ion_trap": n_co2_380 / n_h2_sio,
            "pumped_reaction_rate_min-1_reported": 0.18,
            "pumped_reaction_rate_s-1": k_react_sio,
            "pumped_mean_reaction_time_s": 1.0 / k_react_sio,
            "unpumped_reaction_rate_min-1_reported": 0.05,
            "observed_rate_enhancement": k_react_sio / k_unpumped_sio,
            "activation_scale_eV_from_100_kBT_quoted_at_300K": 100.0 * K_B * T_K / EV_J,
            "optical_work_input_and_optical_recovery_measured": False,
        },
        "passive_state_examples": passive,
        "toy_rotor_unloading": {
            "loss_hazard_assumed_equal_to_CO2_collision_rate_s-1": 1.0 / tau_co2_s,
            "by_unload_duration_ps": unload,
            "formula": "r=2*(z-1+exp(-z))/z^2; z=lambda_loss*t_d",
            "warning": "each collision erasing all remaining recoverable work is an adverse toy assumption, not measured physics",
        },
        "sio_reaction_waiting_cycle": {
            "by_reaction_hold_time_s": sio_cycles,
            "formula": "p=1-exp(-k_r*t); E_net_per_product/E=(1-r*(1-p))/p",
            "excludes": ["loading work", "laser holding power", "unloading duration", "other losses", "product-side energy recovery"],
        },
        "cavity_D2_primary_paper": d2,
        "coherent_pH2_emission_primary_paper": h2,
    }
    path = Path(__file__).with_name("CALCULATIONS.json")
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
