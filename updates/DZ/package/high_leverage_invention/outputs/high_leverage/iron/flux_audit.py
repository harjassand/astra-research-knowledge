#!/usr/bin/env python3
"""Conditional arithmetic for a driven solid-iron export membrane.

This is not a calibrated physical simulation or an experimental result.
The free-alpha-Fe diffusivity is source-reported; its transfer to dirty ore,
confined Fe, and an electromigration interface remains unestablished.
"""
import json
import math
from pathlib import Path

R = 8.31446261815324
F = 96485.33212
NA = 6.02214076e23
kB = R / NA
M_FE = 0.055845
M_O = 0.015999
M_H2 = 0.00201588
RHO_FE = 7874.0  # Illustrative bulk density, kg/m3.


def audit(*, temperature=1163.0, radius=30e-9, length=30e-9,
          porosity=0.2, mobile_thickness=0.3e-9, metal_thickness=3e-9,
          conductivity=1e6, zstar=10.0, delta_mu=100.0,
          target_kg_m2_h=10.0, gamma=1.0, contact_ra=1e-12):
    ds = 10.0 * math.exp(-228000.0 / (R * temperature))
    vm = M_FE / RHO_FE
    omega = vm / NA
    surface_moles = mobile_thickness / vm
    perimeter_per_area = 2.0 * porosity / radius
    metal_area_fraction = porosity*((1.0+metal_thickness/radius)**2-1.0)
    mobility = perimeter_per_area * ds * surface_moles / (R * temperature)
    passive_mol_m2_s = mobility * delta_mu / length
    passive_kg_m2_h = passive_mol_m2_s * M_FE * 3600.0

    target_mol_m2_s = target_kg_m2_h / (M_FE * 3600.0)
    field = target_mol_m2_s / (mobility * abs(zstar) * F)
    active_voltage = field * length
    current_density_metal = conductivity * field
    current_density_projected = metal_area_fraction * current_density_metal
    joule_w_m2 = conductivity * metal_area_fraction * field**2 * length
    contact_w_m2 = current_density_projected**2 * contact_ra
    specific_joule_mwh_t = joule_w_m2 / target_kg_m2_h / 1000.0
    specific_contact_mwh_t = contact_w_m2 / target_kg_m2_h / 1000.0
    shell_kg_m2 = RHO_FE * metal_area_fraction * length
    shell_depletion_s = shell_kg_m2 / (target_kg_m2_h / 3600.0)
    em_work_mol = abs(zstar) * F * active_voltage
    blech_stress_pa = em_work_mol / vm

    surface_atoms = surface_moles * NA
    mullins_b = ds * surface_atoms * omega**2 * gamma / (kB * temperature)
    # Planar linear smoothing scale, not a film-dewetting lifetime.
    smoothing_100nm_s = (100e-9)**4 / ((2*math.pi)**4 * mullins_b)
    return {
        "inputs": {
            "temperature_K": temperature,
            "channel_radius_m": radius,
            "channel_length_m": length,
            "open_fraction": porosity,
            "mobile_layer_m": mobile_thickness,
            "conducting_Fe_shell_m": metal_thickness,
            "conductivity_S_m_assumed": conductivity,
            "Zstar_assumed": zstar,
            "chemical_drop_J_mol_assumed": delta_mu,
            "target_kg_Fe_m2_h": target_kg_m2_h,
            "gamma_J_m2_assumed": gamma,
            "contact_resistance_ohm_m2_assumed": contact_ra,
        },
        "free_Fe_Ds_m2_s_source_law": ds,
        "transport_coefficients_transfer_status": "UNKNOWN",
        "surface_moles_m2": surface_moles,
        "metal_cross_section_fraction_exact_annulus": metal_area_fraction,
        "metal_cross_section_fraction_thin_shell_approx":
            perimeter_per_area * metal_thickness,
        "passive_kg_Fe_m2_h_conditional": passive_kg_m2_h,
        "required_field_V_m_conditional": field,
        "active_layer_voltage_V": active_voltage,
        "metal_current_A_m2_conditional": current_density_metal,
        "projected_current_A_m2_conditional": current_density_projected,
        "active_layer_joule_W_m2": joule_w_m2,
        "active_layer_MWh_t_Fe": specific_joule_mwh_t,
        "contact_W_m2": contact_w_m2,
        "contact_MWh_t_Fe": specific_contact_mwh_t,
        "contact_RA_for_equal_contact_and_active_loss_ohm_m2":
            joule_w_m2 / current_density_projected**2,
        "initial_Fe_shell_kg_m2": shell_kg_m2,
        "shell_inventory_depletion_s_without_ore_admission": shell_depletion_s,
        "required_Fe_moles_s_m2": target_mol_m2_s,
        "electrons_per_exported_Fe_atom_conditional":
            current_density_projected / (F * target_mol_m2_s),
        "EM_work_J_mol": em_work_mol,
        "stress_difference_that_exactly_cancels_EM_Pa": blech_stress_pa,
        "mullins_B_m4_s_conditional": mullins_b,
        "100nm_planar_linear_smoothing_s_not_dewetting_lifetime":
            smoothing_100nm_s,
    }


def material_basis(fe_grade=0.45, export_recovery=0.94,
                   metallization=0.97, product_fe_kg=1000.0):
    hematite_fe_fraction = 2*M_FE/(2*M_FE+3*M_O)
    feed_fe = product_fe_kg/export_recovery
    ore = feed_fe/fe_grade
    gangue = ore - feed_fe/hematite_fe_fraction
    hydrogen_min = product_fe_kg*3*M_H2/(2*M_FE)
    hydrogen_for_metallization = hydrogen_min*metallization/export_recovery
    return {
        "status": "Illustrative hematite_plus_inert_gangue_basis_not_real_ore_assay",
        "Fe_grade": fe_grade,
        "export_recovery": export_recovery,
        "metallization": metallization,
        "exported_Fe_kg": product_fe_kg,
        "ore_feed_kg": ore,
        "feed_Fe_kg": feed_fe,
        "gangue_kg": gangue,
        "metallized_but_not_exported_Fe_kg": feed_fe*metallization-product_fe_kg,
        "unmetallized_Fe_kg": feed_fe*(1-metallization),
        "H2_kg_stoichiometric_floor_if_only_exported_Fe_is_reduced": hydrogen_min,
        "H2_kg_for_declared_metallization_before_gas_heat_losses":
            hydrogen_for_metallization,
        "gangue_heat_890_to_1600_C_plus_400kJ_kg_fusion_MWh_t_Fe":
            gangue*(710.0+400.0)/3.6e6,
        "ore_sensible_heat_25_to_890_C_at_0p8kJ_kgK_MWh_t_Fe":
            ore*0.8*865.0/3.6e6,
        "heat_values_status": "Assumed_constant_heat_capacities_and_fusion_not_process_predictions",
    }


if __name__ == "__main__":
    base = audit()
    assert 0 < base["free_Fe_Ds_m2_s_source_law"] < 1e-8
    assert abs(base["metal_cross_section_fraction_exact_annulus"]-0.042)<1e-12
    assert base["shell_inventory_depletion_s_without_ore_admission"] < 0.01
    cases = []
    for size_nm in (30, 100, 1000):
        cases.append(audit(radius=size_nm*1e-9, length=size_nm*1e-9))
    result = {
        "claim_status": "Conditional arithmetic; no device, ore export, or novelty established",
        "base": base,
        "same_radius_and_length_cases": cases,
        "material_basis": material_basis(),
        "coefficient_sensitivity": [
            audit(zstar=zstar) for zstar in (1.0, 10.0, 100.0)
        ],
    }
    target = Path(__file__).with_name("flux_audit.json")
    target.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"wrote": str(target.resolve()), "base": base,
                      "material_basis": result["material_basis"]}, indent=2))
