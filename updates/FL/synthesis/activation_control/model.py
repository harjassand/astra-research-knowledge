#!/usr/bin/env python3
"""Reproducible ideal-cycle ledger for reaction-conditioned product-state work extraction.

This is an algebraic scenario calculator, not a chemical kinetics or device model.
All constants and boundaries are stated in REPORT.md and READ_LEDGER.md.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

OUT = Path(__file__).with_name("results.json")

# Standard thermochemical inputs from NIST-JANAF, at 298.15 K and 0.1 MPa.
H_CO = -110.527        # kJ/mol
H_CO2 = -393.522       # kJ/mol
G_CO = -137.163        # kJ/mol
G_CO2 = -394.389       # kJ/mol
S_CO = 197.653         # J/(mol K)
S_CO2 = 213.795        # J/(mol K)
S_O2 = 205.147         # J/(mol K)

T_K = 298.15
R_J_MOL_K = 8.31446261815324
KJ_PER_EV_MOLECULE = 96.48533212331002
KWH_PER_KJ = 1.0 / 3600.0
M_CO_KG_MOL = 0.0280104
E_LOAD_EV = 6.14
P_CO_BAR = 14.0         # 13 barg, treated as 14 bar absolute
P_O2_BAR = 1.0          # standard-state product activity for conservative screen
SOEC_KWH_KG = 3.2      # ISPT modeled system electricity, excess-steam assumption


def cycle_work_per_product_ev(
    *,
    p: float,
    s: float,
    loss: float,
    eta_load: float,
    recover_survivor: float,
    recover_product: float,
    recover_loss_residual: float,
    residual_fraction_after_loss: float,
    overhead_ev_per_attempt: float,
    conditioning_ev_per_product: float,
    delta_product_ev: float,
    activation_ev: float = E_LOAD_EV,
) -> float:
    """Expected wall-to-wall net work per useful product for the 3-branch model.

    `recover_*` are fractions of the corresponding non-equilibrium work potential
    delivered back to the same cyclic work bus after source/receiver round-trip loss.
    `overhead_ev_per_attempt` includes auxiliary actuators, readout, feedback
    reset, and controls not already deducted in the net return fractions;
    conditioning is charged per saleable product.
    """
    if p <= 0 or eta_load <= 0:
        return math.inf
    if abs(p + s + loss - 1.0) > 1e-12:
        raise ValueError("branch probabilities must sum to one")
    if activation_ev < delta_product_ev:
        raise ValueError("paid auxiliary work is required when activation is below product free energy")
    residual_product = activation_ev - delta_product_ev
    numerator = (
        activation_ev / eta_load
        + overhead_ev_per_attempt
        - s * recover_survivor * activation_ev
        - p * recover_product * residual_product
        - loss * recover_loss_residual * residual_fraction_after_loss * activation_ev
    )
    return numerator / p + conditioning_ev_per_product


def main() -> None:
    delta_h_kj_mol = H_CO - H_CO2
    delta_g_standard_kj_mol = G_CO - G_CO2
    delta_s_j_mol_k = S_CO + 0.5 * S_O2 - S_CO2
    q_rev_kj_mol = T_K * delta_s_j_mol_k / 1000.0
    compression_kj_mol = R_J_MOL_K * T_K * math.log(P_CO_BAR) / 1000.0
    delta_g_target_kj_mol = delta_g_standard_kj_mol + compression_kj_mol
    delta_g_target_ev = delta_g_target_kj_mol / KJ_PER_EV_MOLECULE
    product_free_energy_potential_ev = E_LOAD_EV - delta_g_target_ev
    delta_h_target_kj_mol = delta_h_kj_mol + compression_kj_mol

    baseline_kj_mol = SOEC_KWH_KG * M_CO_KG_MOL / KWH_PER_KJ
    baseline_ev = baseline_kj_mol / KJ_PER_EV_MOLECULE
    budget_kj_mol = baseline_kj_mol - delta_g_target_kj_mol
    budget_ev = budget_kj_mol / KJ_PER_EV_MOLECULE
    ideal_kwh_kg = delta_g_target_kj_mol * KWH_PER_KJ / M_CO_KG_MOL
    budget_kwh_kg = budget_kj_mol * KWH_PER_KJ / M_CO_KG_MOL
    enthalpy_kwh_kg = delta_h_target_kj_mol * KWH_PER_KJ / M_CO_KG_MOL

    # Independent one-loss-at-a-time thresholds. Combined losses must share the
    # single budget in REPORT.md and therefore be stricter.
    loss_ratio_max = budget_ev / E_LOAD_EV
    eta_load_min = E_LOAD_EV / (E_LOAD_EV + budget_ev)
    recover_product_min = 1.0 - budget_ev / product_free_energy_potential_ev
    p_if_only_full_attrition = 1.0 / (1.0 + loss_ratio_max)

    # Exact source-restricted survivor model for a=1/2, perfect survivor return.
    a = 0.5
    restricted_survivor_floor_ev = E_LOAD_EV / a

    scenarios = {
        # Loss-free case: every nonproduct event is an unchanged survivor, so
        # the source model has a=1 even though only half of attempts react.
        "loss_free_ideal_product_state_recovery": cycle_work_per_product_ev(
            p=0.5, s=0.5, loss=0.0, eta_load=1.0,
            recover_survivor=1.0, recover_product=1.0,
            recover_loss_residual=0.0, residual_fraction_after_loss=0.0,
            overhead_ev_per_attempt=0.0, conditioning_ev_per_product=0.0,
            delta_product_ev=delta_g_target_ev,
        ),
        # Matched a=1/2 comparison: p=a(1-s)=0.25, s=0.5, loss=0.25.
        # The extra operation recovers product excess, but the loss branch is
        # deliberately left unrecovered. It saves exactly R_P vs E/a.
        "a_half_product_state_recovery": cycle_work_per_product_ev(
            p=0.25, s=0.5, loss=0.25, eta_load=1.0,
            recover_survivor=1.0, recover_product=1.0,
            recover_loss_residual=0.0, residual_fraction_after_loss=0.0,
            overhead_ev_per_attempt=0.0, conditioning_ev_per_product=0.0,
            delta_product_ev=delta_g_target_ev,
        ),
        "full_loss_5pct_probability": cycle_work_per_product_ev(
            p=0.95, s=0.0, loss=0.05, eta_load=1.0,
            recover_survivor=1.0, recover_product=1.0,
            recover_loss_residual=0.0, residual_fraction_after_loss=0.0,
            overhead_ev_per_attempt=0.0, conditioning_ev_per_product=0.0,
            delta_product_ev=delta_g_target_ev,
        ),
        "product_return_80pct": cycle_work_per_product_ev(
            p=1.0, s=0.0, loss=0.0, eta_load=1.0,
            recover_survivor=1.0, recover_product=0.80,
            recover_loss_residual=0.0, residual_fraction_after_loss=0.0,
            overhead_ev_per_attempt=0.0, conditioning_ev_per_product=0.0,
            delta_product_ev=delta_g_target_ev,
        ),
        "load_efficiency_90pct": cycle_work_per_product_ev(
            p=1.0, s=0.0, loss=0.0, eta_load=0.90,
            recover_survivor=1.0, recover_product=1.0,
            recover_loss_residual=0.0, residual_fraction_after_loss=0.0,
            overhead_ev_per_attempt=0.0, conditioning_ev_per_product=0.0,
            delta_product_ev=delta_g_target_ev,
        ),
    }

    kbt_ev = 8.617333262145e-5 * T_K
    data = {
        "status": "idealized model arithmetic only; not a measured device or kinetic prediction",
        "thermochemistry": {
            "temperature_K": T_K,
            "standard_pressure_MPa": 0.1,
            "reaction": "CO2(g) -> CO(g) + 0.5 O2(g)",
            "delta_H_kJ_per_mol_CO": delta_h_kj_mol,
            "delta_G_standard_kJ_per_mol_CO": delta_g_standard_kj_mol,
            "delta_S_J_per_mol_K": delta_s_j_mol_k,
            "T_delta_S_kJ_per_mol_CO": q_rev_kj_mol,
            "CO_pressure_bar_absolute": P_CO_BAR,
            "O2_activity_pressure_bar": P_O2_BAR,
            "ideal_CO_compression_kJ_per_mol": compression_kj_mol,
            "delta_G_at_target_kJ_per_mol_CO": delta_g_target_kj_mol,
            "delta_G_at_target_eV_per_CO": delta_g_target_ev,
            "delta_H_plus_ideal_compression_kJ_per_mol_CO": delta_h_target_kj_mol,
            "delta_H_plus_ideal_compression_eV_per_CO": delta_h_target_kj_mol / KJ_PER_EV_MOLECULE,
            "heat_is_recorded_separately_from_work": True,
        },
        "activation_model": {
            "loaded_free_energy_eV_per_addressed_CO2": E_LOAD_EV,
            "ideal_product_non_equilibrium_free_energy_eV_per_CO": product_free_energy_potential_ev,
            "source_restricted_survivor_floor_for_a_half_eV_per_CO": restricted_survivor_floor_ev,
            "loss_free_ideal_state_recovery_net_work_eV_per_CO": scenarios["loss_free_ideal_product_state_recovery"],
            "a_half_extended_net_work_eV_per_CO": scenarios["a_half_product_state_recovery"],
            "a_half_source_restricted_floor_eV_per_CO": restricted_survivor_floor_ev,
        },
        "comparator": {
            "ISPT_modeled_system_electricity_kWh_per_kg_CO": SOEC_KWH_KG,
            "ISPT_standard_CO_molar_mass_kg_per_mol": M_CO_KG_MOL,
            "ISPT_energy_kJ_per_mol_CO": baseline_kj_mol,
            "ISPT_energy_eV_per_CO": baseline_ev,
            "ideal_reversible_target_floor_kWh_per_kg_CO": ideal_kwh_kg,
            "conditional_extra_cost_budget_kWh_per_kg_CO": budget_kwh_kg,
            "conditional_extra_cost_budget_eV_per_CO": budget_ev,
            "no_heat_credit_enthalpy_screen_kWh_per_kg_CO": enthalpy_kwh_kg,
            "no_heat_credit_budget_kWh_per_kg_CO": SOEC_KWH_KG - enthalpy_kwh_kg,
        },
        "independent_thresholds_one_at_a_time": {
            "maximum_full_attrition_probability_over_product_probability": loss_ratio_max,
            "minimum_product_return_fraction": recover_product_min,
            "minimum_wall_to_molecule_loading_efficiency": eta_load_min,
            "minimum_product_probability_if_all_nonproducts_are_full_losses": p_if_only_full_attrition,
            "combined_terms_must_fit_one_budget": True,
        },
        "examples_eV_per_CO": scenarios,
        "feedback_memory_examples": {
            "kBT_eV_at_298_15K": kbt_ev,
            "one_bit_erasure_eV": kbt_ev * math.log(2.0),
            "three_outcome_record_erasure_eV": kbt_ev * math.log(3.0),
            "scope": "Landauer reset floor only for explicit classical record; actuator and measurement costs are additional",
        },
        "cascade_energy_ceiling": {
            "maximum_integer_CO_outputs_per_6_14eV_activation_at_target_deltaG": math.floor(E_LOAD_EV / delta_g_target_ev),
            "not_a_kinetic_or_physical_yield_claim": True,
        },
        "topsoe_stack_crosscheck": {
            "reported_electricity_kWh_per_Nm3_CO": 3.44,
            "reported_CO_tonnes_per_30000_Nm3": 35.5,
            "derived_stack_only_kWh_per_kg_CO": 3.44 / (35.5 * 1000.0 / 30000.0),
            "scope": "derived from reported volume and mass; stack-level, not matched purified-product system energy",
        },
        "limitations": [
            "No joint CO2 reaction, survivor, attrition, or product-state distribution is measured.",
            "No product ergotropy or net work returned to the wall-side bus is measured.",
            "Product conditioning, oxygen-side stream, cooling, laser wall efficiency, and throughput remain unacquired.",
            "The 6.14 eV state is an observed high-J tail; it is not an ensemble mean or an established productive state.",
        ],
    }
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
