"""ROOT conditional transport/current balances; no measured membrane or reactor.

Only standard-library arithmetic. No external sources, producer execution,
hardware action, simulation of a qualified material, or incumbent price claim.
"""

import json
import math
from pathlib import Path

F = 96485.33212
M = 0.0340147  # kg/mol H2O2, retained stoichiometric convention
Q_KWH_PER_V_KG = 2 * F / M / 3_600_000


def transport_case(permeability, conductivity, loss=0.02, current_density=2000):
    # Introduced density 1000 kg/m3 and 3 wt%; neutral Fick + uniform Ohm.
    concentration = 30 / M
    f = 0.9
    k = 2 * F * permeability * concentration / (conductivity * f)
    thickness = 2 * F * permeability * concentration / (loss * current_density * f)
    voltage = current_density * thickness / conductivity
    v_other = 2.2  # introduced voltage excluding THIS separator's Ohmic drop
    rectifier = 0.96
    aux = 0.30
    optimum_loss = 1 / (math.sqrt(1 + v_other / k) + 1)
    optimum_voltage = k / optimum_loss
    energy = Q_KWH_PER_V_KG * (v_other + voltage) / (rectifier * f * (1 - loss)) + aux
    minimum_energy = Q_KWH_PER_V_KG / (rectifier * f) * (
        math.sqrt(v_other + k) + math.sqrt(k)
    ) ** 2 + aux
    optimum_energy = Q_KWH_PER_V_KG * (v_other + optimum_voltage) / (
        rectifier * f * (1 - optimum_loss)
    ) + aux
    assert math.isclose(minimum_energy, optimum_energy, rel_tol=1e-12)
    assert math.isclose(loss * voltage, k, rel_tol=1e-12)
    return {
        "permeability_m2_s": permeability,
        "conductivity_S_m": conductivity,
        "j_A_m2": current_density,
        "introduced_loss_fraction": loss,
        "thickness_m_for_loss": thickness,
        "separator_voltage_V": voltage,
        "loss_times_voltage_V": k,
        "kWh_kg_at_introduced_loss": energy,
        "energy_optimum_loss_fraction": optimum_loss,
        "energy_optimum_separator_voltage_V": optimum_voltage,
        "energy_minimum_kWh_kg_in_this_family": minimum_energy,
    }


def two_compartment(conductance, anode_decay, cathode_decay):
    # Concentration equations in mol/m3; flows/conductance in m3/s.
    # Gross sources are defined independently of the modeled destruction.
    i = 2000
    source_a, source_c = i * 0.8 / (2 * F), i * 0.9 / (2 * F)
    target = 30 / M
    flow_a, flow_c = source_a / target, source_c / target
    volume_a = volume_c = 0.001  # introduced 1-L compartment each
    aa = flow_a + anode_decay * volume_a + conductance
    cc = flow_c + cathode_decay * volume_c + conductance
    determinant = aa * cc - conductance**2
    ca = (source_a * cc + conductance * source_c) / determinant
    c_c = (source_c * aa + conductance * source_a) / determinant
    outlet = flow_a * ca + flow_c * c_c
    destruction = anode_decay * volume_a * ca + cathode_decay * volume_c * c_c
    source = source_a + source_c
    assert math.isclose(source, outlet + destruction, rel_tol=1e-12)
    return {
        "introduced_conductance_m3_s": conductance,
        "introduced_anode_decay_s_1": anode_decay,
        "introduced_cathode_decay_s_1": cathode_decay,
        "anode_concentration_mol_m3": ca,
        "cathode_concentration_mol_m3": c_c,
        "mixed_outlet_wt_fraction_at_introduced_density": outlet / (flow_a + flow_c) * M / 1000,
        "net_collected_fraction_of_gross_source": outlet / source,
        "destroyed_fraction": destruction / source,
        "signed_cathode_to_anode_transfer_mol_s": conductance * (c_c - ca),
        "total_balance_residual_mol_s": source - outlet - destruction,
    }


def main():
    concentration = 30 / M
    eta, f, loss, j = 0.96, 0.9, 0.02, 2000
    q_eq = 2 / (M * f * (1 - loss))  # mol electron equivalents per accepted kg
    volume_l = 1 / 0.03  # introduced solution density 1 kg/L
    gates_g_per_kg = {
        "total_other_nonwater_dissolved_mass": 1000 * (1 / 0.999 - 1),
        "chloride": volume_l * 0.001,
        "Na_plus_K_combined": volume_l * 0.010,
        "TOC_as_carbon": volume_l * 0.010,
        "Fe_Cu_Mn_combined": volume_l * 0.000010,
    }
    area = (1000 / 86400 / M) * 2 * F / (f * (1 - loss) * j)
    chloride_moles = gates_g_per_kg["chloride"] / 35.45
    same_stock_salt_moles = gates_g_per_kg["total_other_nonwater_dissolved_mass"] / 58.44
    target_voltage_budget = (5 - 0.30) * eta * f / Q_KWH_PER_V_KG
    k_max = (target_voltage_budget - 2.2) ** 2 / (4 * target_voltage_budget)
    result = {
        "scope": "Conditional arithmetic only; no qualified material, full reactor, purity assay or achieved advantage.",
        "constants_and_introduced_inputs": {
            "F_C_mol": F, "M_kg_mol": M,
            "solution_density_kg_L_INTRODUCED": 1,
            "bulk_H2O2_concentration_mol_m3": concentration,
            "cathodic_Faradaic_yield_INTRODUCED": f,
            "rectifier_efficiency_INTRODUCED": eta,
            "auxiliary_kWh_kg_INTRODUCED": 0.30,
            "other_voltage_excluding_modeled_separator_V_INTRODUCED": 2.2,
            "transport_loss_illustration_NOT_human_gate": loss,
        },
        "purity_and_charge": {
            "solution_L_kg_active": volume_l,
            "mol_electron_equivalents_kg_active": q_eq,
            "allowed_g_kg_active": gates_g_per_kg,
            "chloride_mol_per_mol_electron_equivalent_ceiling": chloride_moles / q_eq,
            "NaCl_equivalent_ceiling_from_total_mass_only": same_stock_salt_moles / q_eq,
            "area_m2_for_1t_active_day_at_introduced_j": area,
            "combined_Fe_Cu_Mn_allowed_mg_m2_day_at_that_scale": gates_g_per_kg["Fe_Cu_Mn_combined"] * 1000 * 1000 / area,
            "chloride_allowed_flux_mol_m2_s": chloride_moles * (1000 / 86400) / area,
        },
        "family_energy_target_boundary": {
            "available_voltage_function_budget_V": target_voltage_budget,
            "max_loss_times_separator_voltage_V_after_optimizing_loss": k_max,
            "max_P_over_kappa_m3_S_s": k_max * f / (2 * F * concentration),
            "limitations": "Only neutral passive loss into a perfect destructive sink plus Ohmic same-layer conduction; excludes alternative geometries, matched product concentrations and active transport. Other voltage/auxiliaries held introduced and fixed, not a thermodynamic bound on peroxide.",
        },
        "transport_grid": [transport_case(p, k) for p in [1e-14, 1e-13, 1e-12, 1e-11, 1e-10] for k in [0.1, 1, 10]],
        "current_density_similarity": [transport_case(1e-11, 1, current_density=x) for x in [1000, 2000, 5000]],
        "two_product_compartments": [two_compartment(g, d, 0) for d in [0, 0.1] for g in [0, 1e-6, 1e-4]],
        "nonclaims": [
            "No measured permeability/conductivity, neutral-speciation fraction or constant-property validity supplied.",
            "Transport-loss illustration is separate from the issued 98% 24-hour stored-product requirement.",
            "A chloride-to-charge quotient is a stock/flux diagnostic, not an electrochemical salt-leak theorem.",
            "Internal crossover cancels from whole inventory; only actual destruction/rejection loses product.",
            "Do not subtract modeled product destruction again from an FE already measured as net recovered product.",
            "The two-compartment favorable no-decay case does not supply compatible paired electrodes or pure-product hardware.",
        ],
    }
    # Analytic consistency checks for the physical bookkeeping, not material tests.
    no_decay = result["two_product_compartments"][:3]
    assert all(math.isclose(x["net_collected_fraction_of_gross_source"], 1, rel_tol=1e-12) for x in no_decay)
    ks = [x["loss_times_voltage_V"] for x in result["current_density_similarity"]]
    assert max(ks) - min(ks) < 1e-12
    path = Path(__file__).with_suffix('.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ["purity_and_charge", "family_energy_target_boundary", "current_density_similarity", "two_product_compartments"]}, indent=2))


if __name__ == '__main__':
    main()
