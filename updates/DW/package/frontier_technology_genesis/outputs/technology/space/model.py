#!/usr/bin/env python3
"""Conditional first-order foil-cell space radiator model.

No device, CFD, lifetime, manufacturing, or novelty validation is claimed.
Every unmeasured geometric/material value is an input, not a fit to a device.
Area is always deployed projected footprint; two emitting faces are explicit.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

SIGMA = 5.670374419e-8


def rectangle_dp(mu, length, volume_flow, width, height):
    """Fully developed laminar rectangle; 0 < h/w <= 1.

    First aspect-ratio correction. This deliberately uses full-length flow,
    overestimating an artery that collects condensate progressively.
    """
    assert 0 < height <= width
    return (12 * mu * length * volume_flow /
            (width * height**3 * (1 - 0.63 * height / width)))


def evaluate():
    p = {
        "status": "UNBUILT_CONDITIONAL_POINT_DESIGN",
        "footprint_m2": 100.0,
        "cell_pitch_m": 0.01,
        "cell_length_m": 0.5,
        "source_K": 360.0,
        "emitter_K": 350.0,
        "effective_sink_K": 200.0,
        "emissivity_assumed": 0.85,
        "unobstructed_geometry_factor_assumed": 0.90,
        "solar_absorptivity_assumed": 0.90,
        "solar_flux_W_m2": 1361.0,
        "sun_grazing_angle_deg": 5.0,
        "water_surface_tension_N_m_approx": 0.0633,
        "water_density_kg_m3_approx": 974.0,
        "water_viscosity_Pa_s_approx": 0.000365,
        "water_latent_heat_J_kg_approx": 2.315e6,
        "water_sat_pressure_Pa_approx": 41680.0,
        "water_vapor_R_J_kg_K": 461.52,
        "water_vapor_viscosity_Pa_s_approx": 1.15e-5,
        "capillary_pore_radius_m_assumed": 20e-6,
        "contact_angle_deg_assumed": 15.0,
        "arteries_per_cell": 2,
        "artery_width_m": 0.0004,
        "artery_height_m": 0.0003,
        "fine_wick_thickness_m": 50e-6,
        "fine_wick_solid_fraction_assumed": 0.30,
        "fine_wick_permeability_m2_required": 1e-13,
        "foil_thickness_m": 25e-6,
        "titanium_density_kg_m3": 4500.0,
        "inflated_wall_curvature_radius_m_assumed": 0.004,
        "vapor_cross_section_m2_assumed": 9.4e-6,
        "vapor_height_m_assumed": 0.002,
        "lunar_gravity_m_s2": 1.62,
    }
    T, Ts = p["emitter_K"], p["effective_sink_K"]
    gross = (2 * p["emissivity_assumed"] * SIGMA * (T**4 - Ts**4) *
             p["unobstructed_geometry_factor_assumed"])
    sun = (p["solar_absorptivity_assumed"] * p["solar_flux_W_m2"] *
           math.sin(math.radians(p["sun_grazing_angle_deg"])))
    q = gross - sun
    a_cell = p["cell_pitch_m"] * p["cell_length_m"]
    q_cell = q * a_cell
    mdot = q_cell / p["water_latent_heat_J_kg_approx"]
    vdot = mdot / p["water_density_kg_m3_approx"]
    artery = rectangle_dp(
        p["water_viscosity_Pa_s_approx"], p["cell_length_m"],
        vdot / p["arteries_per_cell"], p["artery_width_m"],
        p["artery_height_m"])
    # Conservative lateral return: all cell condensate traverses half pitch.
    wick_A = p["fine_wick_thickness_m"] * p["cell_length_m"]
    local_wick = (p["water_viscosity_Pa_s_approx"] *
                  (p["cell_pitch_m"] / 2) * vdot /
                  (p["fine_wick_permeability_m2_required"] * wick_A))
    cap = (2 * p["water_surface_tension_N_m_approx"] *
           math.cos(math.radians(p["contact_angle_deg_assumed"])) /
           p["capillary_pore_radius_m_assumed"])
    vapor_rho = p["water_sat_pressure_Pa_approx"] / (
        p["water_vapor_R_J_kg_K"] * T)
    vapor_speed = mdot / (vapor_rho * p["vapor_cross_section_m2_assumed"])
    vapor_dp_approx = (12 * p["water_vapor_viscosity_Pa_s_approx"] *
                       p["cell_length_m"] * vapor_speed /
                       p["vapor_height_m_assumed"]**2)
    head_moon = (p["water_density_kg_m3_approx"] *
                 p["lunar_gravity_m_s2"] * p["cell_length_m"])
    head_earth = p["water_density_kg_m3_approx"] * 9.81 * p["cell_length_m"]
    rho_ti = p["titanium_density_kg_m3"]
    wall_mass = 2 * p["foil_thickness_m"] * rho_ti
    fine_wick_mass = (p["fine_wick_thickness_m"] *
                      p["fine_wick_solid_fraction_assumed"] * rho_ti)
    artery_equiv_ti = (2 * 2 * (p["artery_width_m"] + p["artery_height_m"]) *
                       10e-6 / p["cell_pitch_m"])
    artery_mass = artery_equiv_ti * rho_ti
    wick_water = (p["fine_wick_thickness_m"] *
                  (1 - p["fine_wick_solid_fraction_assumed"]) *
                  p["water_density_kg_m3_approx"])
    artery_water = (p["arteries_per_cell"] * p["artery_width_m"] *
                    p["artery_height_m"] / p["cell_pitch_m"] *
                    p["water_density_kg_m3_approx"])
    mass = {
        "two_titanium_walls": wall_mass,
        "fine_wick": fine_wick_mass,
        "artery_formed_foil_allowance": artery_mass,
        "wick_and_artery_water": wick_water + artery_water,
        "emissive_coating_assumed": 0.10,
        "local_coolant_spines_wall_and_fluid_assumed": 0.16,
        "main_supply_return_wall_and_fluid_assumed": 0.215,
        "pump_accumulator_fittings_assumed": 0.10,
        "deployment_and_frame_assumed": 0.25,
        "primary_rail_armor_assumed": 0.10,
        "electrical_and_pointing_reserve_assumed": 0.10,
    }
    nominal_mass = sum(mass.values())
    reserve_mass = nominal_mass * 1.25
    redundant_extra = 0.55
    # This is a sensitivity only: 2016 module 380 W / 0.523 kg at
    # 400 K inlet; design coolant-to-fin-root drop 19.1 K, sink 250 K.
    # Temperature/geometry/transport differences prevent this from proving
    # superiority. Baseline excludes pump, deployment and attitude systems.
    baseline_W_kg = 380 / 0.523
    normalized_baseline_W_kg = baseline_W_kg * (
        (T**4 - Ts**4) / ((400 - 19.1)**4 - 250**4))
    sensitivities = []
    for emit, angle, geo, redundant in [
        (350, 5, 0.90, False), (350, 5, 0.80, False),
        (340, 5, 0.90, False), (350, 15, 0.90, False),
        (350, 5, 0.90, True),
    ]:
        net = (2 * p["emissivity_assumed"] * SIGMA *
               (emit**4 - Ts**4) * geo -
               p["solar_absorptivity_assumed"] * p["solar_flux_W_m2"] *
               math.sin(math.radians(angle)))
        density = reserve_mass + (redundant_extra if redundant else 0)
        sensitivities.append({"emitter_K": emit, "sun_angle_deg": angle,
                              "view_factor": geo, "dual_primary_loop": redundant,
                              "net_W_m2_footprint": net,
                              "installed_kg_m2_footprint": density,
                              "net_W_kg_installed": net / density})
    # 100 kW, single-phase main loop, 10 K temperature drop.
    load = 100000.0
    main_mdot = load / (4180 * 10)
    pump = 60000 * main_mdot / (p["water_density_kg_m3_approx"] * 0.5)
    results = {
        "inputs": p,
        "calculated": {
            "gross_two_sided_W_m2_footprint": gross,
            "absorbed_sun_W_m2_footprint": sun,
            "net_W_m2_footprint": q,
            "cells_per_m2": 1 / a_cell,
            "power_per_cell_W": q_cell,
            "cell_water_flow_kg_s": mdot,
            "capillary_pressure_Pa": cap,
            "return_artery_pressure_drop_upper_bound_Pa": artery,
            "fine_wick_lateral_drop_conservative_Pa": local_wick,
            "vapor_speed_m_s": vapor_speed,
            "vapor_drop_approx_Pa": vapor_dp_approx,
            "gravity_head_Moon_Pa": head_moon,
            "gravity_head_Earth_Pa": head_earth,
            "capillary_ratio_microgravity": cap / (artery + local_wick + vapor_dp_approx),
            "capillary_ratio_Moon_full_adverse_tilt": cap / (
                artery + local_wick + vapor_dp_approx + head_moon),
            "capillary_ratio_Earth_full_adverse_tilt": cap / (
                artery + local_wick + vapor_dp_approx + head_earth),
            "nominal_membrane_hoop_stress_MPa": (
                p["water_sat_pressure_Pa_approx"] *
                p["inflated_wall_curvature_radius_m_assumed"] /
                p["foil_thickness_m"] / 1e6),
            "nominal_installed_mass_kg_m2": nominal_mass,
            "installed_mass_with_25pct_reserve_kg_m2": reserve_mass,
            "installed_mass_dual_primary_loop_kg_m2": reserve_mass + redundant_extra,
            "net_specific_power_with_reserve_W_kg": q / reserve_mass,
            "measured_2016_module_W_kg_at_other_conditions": baseline_W_kg,
            "radiation_only_scaled_baseline_W_kg_not_a_measurement": normalized_baseline_W_kg,
            "conditional_ratio_to_scaled_module_only_baseline": q / reserve_mass / normalized_baseline_W_kg,
            "main_loop_mass_flow_kg_s_at_100kW": main_mdot,
            "pump_W_at_60kPa_and_50pct_efficiency": pump,
            "seam_length_m_per_m2_approx": 105.0,
            "seam_hours_at_100m2_10mm_s_approx": 105 * 100 / 0.01 / 3600,
            "sealed_cells_at_100m2": 100 / a_cell,
            "fractional_heat_loss_if_five_single_cells_lost_per_m2": 5 * a_cell,
            "total_water_loss_kg_if_five_single_cells_lost_per_m2": (
                5 * a_cell * (wick_water + artery_water)),
        },
        "mass_budget_kg_per_m2_footprint": mass,
        "sensitivity_cases": sensitivities,
        "limits": [
            "Thermal contacts, two-scale wick fabrication and stable priming are assumed, not demonstrated.",
            "25 percent mass reserve is not evidence of an engineered deployment frame or armor adequacy.",
            "Two-face cold view and near-edge-on Sun are mission constraints.",
            "Punctures only remain local if they miss common coolant rails and do not unzip seams.",
            "Freeze restart, space environmental lifetime and 20000-cell production yield are unverified.",
            "Radiation-only baseline scaling is a screening sensitivity, not a matched experimental comparison.",
            "Sealed cell, arterial wick, foil radiator, local puncture loss and distributed loads are known principles.",
        ],
    }
    return results


if __name__ == "__main__":
    result = evaluate()
    dest = Path(__file__).with_name("model_results.json")
    dest.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["calculated"], indent=2))
    print(f"Saved conditional model to {dest}")
