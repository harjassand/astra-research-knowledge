#!/usr/bin/env python3
"""Conditional continuum accounting for a valved Kelvin pump.

This is a calculator, not a validated molecular or device simulation. Every
surface state and transport assumption is explicit. Only stdlib is required.
Run from any directory; results are written beside this file.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R = 8.314462618
F = 96485.33212
NA = 6.02214076e23
M = 0.01801528
RHO = 997.0
VM = M / RHO
GAMMA = 0.072
EPS0 = 8.8541878128e-12
CP_AIR = 1006.0
RHO_AIR = 1.184
LATENT = 2.44e6
J_PER_KWH = 3.6e6


def psat(tc: float) -> float:
    """Buck approximation in Pa, sufficient only for this conditional ledger."""
    return 611.21 * math.exp((18.678 - tc / 234.5) * tc / (257.14 + tc))


def chemical_pressure(h: float, tk: float) -> float:
    return R * tk / VM * math.log(1.0 / h)


def vapor_density(h: float, tc: float) -> float:
    return h * psat(tc) * M / (R * (tc + 273.15))


def capillary_drive(r: float, theta: float) -> float:
    return 2.0 * GAMMA * math.cos(math.radians(theta)) / r


def case(r_nm=0.7, theta_a=45.0, theta_b=100.0, dt_k=3.0,
         extraction=0.2, sites_nm2=1.0, excess_voltage=0.05,
         cycle_s=60.0, hold_fraction=0.5, c_delta=0.1,
         c_dry=0.02, charge_eff=0.95, recovery_eff=0.95,
         leakage_power_w_m2=0.0):
    tc = 25.0
    tk = tc + 273.15
    ts = tk + dt_k
    h_in = 0.6
    h_out = h_in * (1.0 - extraction)
    h_local_worst = h_out * psat(tc) / psat(tc + dt_k)
    r = r_nm * 1e-9
    gamma_a = GAMMA * math.cos(math.radians(theta_a))
    gamma_b = GAMMA * math.cos(math.radians(theta_b))
    delta_gamma = gamma_a - gamma_b
    area_per_kg = 2.0 / (RHO * r)
    w_surface = area_per_kg * delta_gamma
    pchem = chemical_pressure(h_local_worst, ts)
    vapor_removed = vapor_density(h_in, tc) - vapor_density(h_out, tc)
    air_m3_kg = 1.0 / vapor_removed
    source_fan = 100.0 * air_m3_kg / 0.55
    # Electrical work also reaches the heat sink. Iteration closes this load
    # for each selected electrical implementation, without latent-heat reuse.
    heat_air_per_j = 1.0 / (RHO_AIR * CP_AIR * dt_k)
    heat_fan_fraction = 50.0 / 0.55 * heat_air_per_j
    n_e_mol_kg = area_per_kg * sites_nm2 * 1e18 / NA
    redox_excess = n_e_mol_kg * F * excess_voltage
    voltage_hi = math.sqrt(2.0 * delta_gamma / c_delta)
    # Four ideal electrical strokes, low voltage = 0. Negative means returned.
    charge_dry = 0.5 * c_dry * voltage_hi**2 * area_per_kg
    fill_held = c_delta * voltage_hi**2 * area_per_kg
    discharge_wet = -0.5 * (c_dry + c_delta) * voltage_hi**2 * area_per_kg
    signed_ideal = charge_dry + fill_held + discharge_wet
    electronics_actual = (charge_dry + fill_held) / charge_eff + discharge_wet * recovery_eff
    leakage = leakage_power_w_m2 * cycle_s * hold_fraction * area_per_kg
    redox_core = w_surface + redox_excess + leakage
    capacitor_core = electronics_actual + leakage
    # E_total = core + sourcefan + heatfan_fraction*(latent + E_total).
    redox_total = (redox_core + source_fan + heat_fan_fraction * LATENT) / (1.0 - heat_fan_fraction)
    capacitor_total = (capacitor_core + source_fan + heat_fan_fraction * LATENT) / (1.0 - heat_fan_fraction)
    e_per_water = n_e_mol_kg / (1.0 / M)
    counterions_mol_l = 2.0 * c_delta * voltage_hi / (F * r) / 1000.0
    rate_kg_m2_h = 1.0
    inventory_kg_m2 = rate_kg_m2_h * cycle_s / 3600.0
    active_area_m2_m2 = inventory_kg_m2 * area_per_kg
    coating_kg_m2 = active_area_m2_m2 * 0.5e-9 * 1500.0
    return {
        "r_nm": r_nm, "theta_a_deg": theta_a, "theta_b_deg": theta_b,
        "surface_overtemperature_k": dt_k, "air_water_extraction_fraction": extraction,
        "local_worst_RH": h_local_worst,
        "chemical_pressure_MPa": pchem / 1e6,
        "capture_drive_MPa": 2.0 * gamma_a / r / 1e6,
        "capture_margin_MPa": (2.0 * gamma_a / r - pchem) / 1e6,
        "ejection_pressure_MPa": -2.0 * gamma_b / r / 1e6,
        "surface_contrast_mJ_m2": delta_gamma * 1000.0,
        "surface_work_kWh_kg": w_surface / J_PER_KWH,
        "source_air_m3_kg": air_m3_kg,
        "source_fan_kWh_kg": source_fan / J_PER_KWH,
        "latent_heat_kWh_kg": LATENT / J_PER_KWH,
        "heat_rejection_air_m3_kg_latent_only": LATENT * heat_air_per_j,
        "heat_rejection_fan_kWh_kg_latent_only": heat_fan_fraction * LATENT / J_PER_KWH,
        "redox_sites_nm2": sites_nm2,
        "redox_excess_voltage_V": excess_voltage,
        "electrons_per_water": e_per_water,
        "redox_excess_kWh_kg": redox_excess / J_PER_KWH,
        "capacitor_voltage_hi_V": voltage_hi,
        "capacitor_charge_dry_kWh_kg": charge_dry / J_PER_KWH,
        "capacitor_fill_held_kWh_kg": fill_held / J_PER_KWH,
        "capacitor_discharge_wet_kWh_kg": discharge_wet / J_PER_KWH,
        "capacitor_signed_ideal_kWh_kg": signed_ideal / J_PER_KWH,
        "capacitor_conversion_loss_kWh_kg": (electronics_actual - signed_ideal) / J_PER_KWH,
        "capacitor_min_counterion_inventory_mol_L": counterions_mol_l,
        "leakage_kWh_kg": leakage / J_PER_KWH,
        "conditional_redox_all_in_kWh_kg": redox_total / J_PER_KWH,
        "conditional_capacitor_all_in_kWh_kg": capacitor_total / J_PER_KWH,
        "cycle_s": cycle_s,
        "active_area_m2_per_m2_footprint": active_area_m2_m2,
        "conditional_0p5nm_coating_kg_m2_footprint": coating_kg_m2,
        "capture_pass_continuum_only": 2.0 * gamma_a / r > pchem,
        "all_surface_and_transport_values_status": "ASSUMED_NOT_DEMONSTRATED",
    }


def main():
    nominal = case()
    sweep = [case(r_nm=r, dt_k=dt, sites_nm2=s, excess_voltage=v)
             for r in [0.5, 0.7, 1.0, 2.0]
             for dt in [1.0, 3.0, 5.0]
             for s, v in [(1.0, 0.05), (3.0, 0.1)]]
    baseline_pressure = chemical_pressure(0.6, 298.15)
    fields = {}
    for name, eps, sigma in [("normal_confined", 2.0, None),
                             ("in_plane_confined", 1030.0, 3.0)]:
        field = math.sqrt(2.0 * baseline_pressure / (EPS0 * (eps - 1.0)))
        fields[name] = {"assumed_linear_relative_epsilon": eps,
                        "field_V_m": field, "field_GV_m": field / 1e9}
        if sigma is not None:
            power = sigma * field**2
            fields[name].update({"reported_conductivity_S_m": sigma,
                                "joule_power_W_m3": power,
                                "dwell_limit_s_for_0p1kWh_kg": 0.1 * J_PER_KWH * RHO / power})
    leak_budget = 0.005 * J_PER_KWH
    measured_planar_power = 10e-6 / 1e-4  # 10 microW/cm2, not assigned as steady leakage.
    gates = {
        "ambient_RH_0p6_chemical_pressure_MPa": baseline_pressure / 1e6,
        "ambient_reversible_work_kWh_kg": baseline_pressure / RHO / J_PER_KWH,
        "minimum_delta_gamma_mJ_m2_r_1nm_theta_off_90": baseline_pressure * 1e-9 / 2 * 1000,
        "gold_effective_r_68nm_RH_threshold_theta_30": math.exp(-2 * GAMMA * math.cos(math.radians(30)) * VM / (68e-9 * R * 298.15)),
        "gold_theta_off_70_pressure_to_empty_if_r_1nm_MPa": capillary_drive(1e-9, 70) / 1e6,
        "hydrophobic_vapor_guard_r_2nm_theta_150_entry_MPa": -capillary_drive(2e-9, 150) / 1e6,
        "hydrophobic_outlet_r_100nm_theta_120_entry_MPa": -capillary_drive(100e-9, 120) / 1e6,
        "nominal_leak_budget_hold_s_at_0p1W_m2": leak_budget / (nominal["surface_work_kWh_kg"] * J_PER_KWH / (nominal["surface_contrast_mJ_m2"] / 1000) * measured_planar_power),
        "planar_reported_power_W_m2_not_proven_steady_leakage": measured_planar_power,
        "uniform_fill_transport_not_established": True,
        "molecular_Kelvin_extrapolation_not_validated": True,
    }
    # Internal consistency checks are calculator checks, never physical validation.
    assert abs(nominal["surface_work_kWh_kg"] - nominal["capacitor_signed_ideal_kWh_kg"]) < 1e-12
    assert baseline_pressure > 0
    assert gates["hydrophobic_outlet_r_100nm_theta_120_entry_MPa"] < nominal["ejection_pressure_MPa"] < gates["hydrophobic_vapor_guard_r_2nm_theta_150_entry_MPa"]
    result = {"status": "CONDITIONAL_ARCHITECTURE_NO_MATERIAL_DEMONSTRATION",
              "nominal": nominal, "bulk_field_counterexample": fields, "gates": gates,
              "assumptions": {
                  "gamma_N_m": GAMMA, "rho_water_kg_m3": RHO,
                  "capture_air_25C_RH": 0.6, "source_fan_Pa": 100,
                  "heat_rejection_fan_Pa": 50, "fan_efficiency": 0.55,
                  "latent_J_kg": LATENT,
                  "capital_and_ionic_separation_energy": "UNPRICED_NOT_ZERO",
                  "unspecified_device_loss": "NOT_INCLUDED_NOT_ZERO"}}
    (ROOT / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    with (ROOT / "sweep.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(sweep[0]))
        writer.writeheader()
        writer.writerows(sweep)
    print(json.dumps({"nominal": nominal, "gates": gates, "fields": fields}, indent=2))


if __name__ == "__main__":
    main()
