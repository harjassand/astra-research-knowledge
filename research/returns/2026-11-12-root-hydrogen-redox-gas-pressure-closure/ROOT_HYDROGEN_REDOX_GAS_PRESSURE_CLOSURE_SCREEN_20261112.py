"""ROOT conditional carrier/gas/pressure accounting, not material or device data."""
import json
import math
from pathlib import Path

F = 96485.33212
R = 8.314462618
M_H2 = 0.00201588
M_NIOH2 = 0.09270808
T = 298.15
N_H2 = 1 / M_H2
ACTIVE = 2 * M_NIOH2 / M_H2
U = 0.1
TRANSFER = ACTIVE / U  # kg active carrier cycled per kg gross cathodic H2
# Import the earlier numerical AC screen ONLY as a paid gross-generator input.
# The downstream 2F carrier inventory does not construct its parasitic reactions.
CELL_AC = 2 * F / M_H2 / 3600 * 1.50 / 1000 / 0.995 / 0.96
TARGET = 45


def evaluate(name, residual_oxidized_fraction, oxygen_mol_L,
             return_oxygen_head_L_kg, lost_H2_head_L_kg,
             H2_loss_pressure_bar, pressure_recovery, heat_kWh,
             cleaning_kWh, stripping_kWh):
    # Every numeric transport/material parameter below is INTRODUCED.
    liquid_L = TRANSFER * 1.0
    solid_volume_m3 = TRANSFER / 4000.0
    pumped_m3 = liquid_L / 1000 + solid_volume_m3
    pressure_work = pumped_m3 * 29e5 / 3_600_000
    pump_AC = pressure_work / 0.60
    recovered = pressure_work * pressure_recovery
    net_pressure = pump_AC - recovered
    dissolved_O2 = liquid_L * oxygen_mol_L
    returned_gas_O2 = TRANSFER * return_oxygen_head_L_kg / 1000 * 1e5 / (R*T)
    O2_to_deoxo = dissolved_O2 + returned_gas_O2
    H2_consumed_redox = N_H2 * residual_oxidized_fraction / U
    H2_consumed_deoxo = 2 * O2_to_deoxo
    H2_lost_head = (TRANSFER * lost_H2_head_L_kg / 1000
                    * H2_loss_pressure_bar * 1e5 / (R*T))
    accepted = N_H2 - H2_consumed_redox - H2_consumed_deoxo - H2_lost_head
    y = accepted / N_H2
    assert y > 0
    # Solid state after electrochemical charge u, before H2 contact residual f.
    # All carried oxygen is consumed by H2; exported O2 excludes that oxygen.
    n_carrier = TRANSFER / M_NIOH2
    O2_released_thermal = n_carrier * (U-residual_oxidized_fraction) / 4
    exported_O2 = O2_released_thermal - O2_to_deoxo
    # Material conservation: accepted + lost H2 == twice exported O2.
    balance_residual = accepted + H2_lost_head - 2 * exported_O2
    assert abs(balance_residual) < 1e-10
    gross_energy = CELL_AC + net_pressure + heat_kWh + cleaning_kWh + stripping_kWh
    return {
        "name": name,
        "introduced_residual_oxidized_fraction_of_total_carrier": residual_oxidized_fraction,
        "introduced_dissolved_O2_mol_L": oxygen_mol_L,
        "introduced_return_pure_O2_head_L_kg_active_at_1bar": return_oxygen_head_L_kg,
        "introduced_unrecovered_H2_head_L_kg_active": lost_H2_head_L_kg,
        "introduced_H2_loss_pressure_bar": H2_loss_pressure_bar,
        "introduced_effective_pressure_energy_recovery": pressure_recovery,
        "introduced_heat_cleaning_stripping_kWh_per_gross_kg": [heat_kWh, cleaning_kWh, stripping_kWh],
        "dissolved_O2_mol_per_gross_kg": dissolved_O2,
        "gas_O2_mol_per_gross_kg": returned_gas_O2,
        "gross_H2_fraction_consumed_redox": H2_consumed_redox/N_H2,
        "gross_H2_fraction_consumed_deoxo": H2_consumed_deoxo/N_H2,
        "gross_H2_fraction_lost_head": H2_lost_head/N_H2,
        "net_accepted_H2_fraction": y,
        "ideal_pressure_transfer_kWh_per_gross_kg": pressure_work,
        "pump_AC_kWh_per_gross_kg": pump_AC,
        "physically_returned_pressure_energy_kWh_per_gross_kg": recovered,
        "net_pressure_kWh_per_gross_kg": net_pressure,
        "total_kWh_per_accepted_kg": gross_energy/y,
        "gross_kg_for_cold_run_4point167kg_accepted": 4.167/y,
        "baseline_charge_side_reactions_and_terminal_map_not_established": True,
        "stoichiometric_H2_minus_2O2_balance_residual_mol": balance_residual,
        "max_extra_gross_kWh_before_45target": TARGET*y-gross_energy,
    }


cases = [
    evaluate("unrecovered_30bar_heads_no_pressure_recovery", .001, .001, .1, .1, 30, 0, 1, .3, 0),
    evaluate("flooded_gas_sides_liquid_O2_remains", .001, .001, 0, 0, 30, .9, 1, .3, 0),
    evaluate("favorable_unqualified_flooded_stripped_low_residual", .0001, .000001, 0, .001, 30, .9, 1, .3, .1),
]

thresholds = {
    "ppm_O2_requirement": 5,
    "O2_mol_per_kg_H2_if_no_cleanup": N_H2*5e-6/(1-5e-6),
    "O2_mol_L_if_1L_liquid_per_kg_active_no_other_contamination":
        N_H2*5e-6/(1-5e-6)/TRANSFER,
    "fraction_H2_lost_for_0point1L_kg_active_30bar_head":
        TRANSFER*.1/1000*30e5/(R*T)/N_H2,
    "fraction_H2_lost_same_head_after_unqualified_recovery_to_1bar":
        TRANSFER*.1/1000*1e5/(R*T)/N_H2,
    "zero_aux_max_total_H2_loss_fraction_from_cell_AC_alone": 1-CELL_AC/TARGET,
    "zero_aux_max_residual_oxidized_fraction_if_only_loss": U*(1-CELL_AC/TARGET),
}

renewal = []
for u in (1.0, .1):
    for lifetime_cycles in (10000, 100000, 1000000):
        renewal.append({
            "introduced_utilization": u,
            "introduced_prepared_active_material_USD_kg": 100,
            "introduced_qualified_cycles": lifetime_cycles,
            "material_only_USD_per_gross_kg_H2": ACTIVE/u*100/lifetime_cycles,
            "operating_hours_at_introduced_200s_complete_cycle": lifetime_cycles*200/3600,
        })

result = {
    "status": "CONDITIONAL_COUPLED_ACCOUNTING_NOT_A_HYDROGEN_INVENTION",
    "boundary": "One kg gross cathodic H2, disjoint downstream redox/deoxo/head losses; final useful kg denominator.",
    "constants_not_recovered_thermochemical_data": {"F": F, "R": R, "M_H2_kg_mol": M_H2,
                                                    "M_NiOH2_kg_mol": M_NIOH2, "ideal_gas_T_K": T},
    "active_kg_cycled_per_gross_kg_H2_at_full_utilization": ACTIVE,
    "introduced_utilization": U,
    "active_kg_cycled_per_gross_kg_H2": TRANSFER,
    "introduced_paid_generator_AC_allowance_kWh_per_gross_kg": CELL_AC,
    "shared_introduced_pressure_assumptions": {
        "liquid_L_per_kg_active": 1, "solid_density_kg_m3": 4000,
        "delta_p_bar": 29, "pump_AC_efficiency": .60,
        "no_extra_compressor_added_to_pressurized_cell": True,
    },
    "cases": cases,
    "thresholds": thresholds,
    "material_renewal_screens": renewal,
    "introduced_200s_loop_active_inventory_kg_at_1grosskg_day": TRANSFER*200/86400,
    "ten_gram_specimen_gross_H2_mg_per_10pct_cycle": .01/M_NIOH2*U/2*M_H2*1e6,
    "limits": [
        "No measured O2 solubility, residual phase, gas holdup, density, efficiency, life or price is supplied.",
        "All gas carrying volume is explicitly unrecovered; equalization can change it but pays buffers/recompression.",
        "Recovery is credited only as returned useful work in the hypothetical coupled ledger, never potential alone.",
        "No dry-vacuum stripping of hot aqueous carrier is assumed; water evaporation/condensation remains unmodeled.",
        "Deoxo product loss is charged, while catalyst kinetics/exotherm/drying/life are not established by a utility allowance.",
        "A returning residual state must actually contact and react with H2 for the redox loss scenario to apply.",
        "If measured net charge yield already includes these losses, applying them again would double count.",
        "The AC baseline is a paid input allowance, not a simultaneous charge/side-reaction/pressure-voltage construction.",
        "No source, artifact, physical test, purchase, new worker or new allocation was executed by this model.",
    ],
}
path = Path(__file__).with_suffix('.json')
path.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
