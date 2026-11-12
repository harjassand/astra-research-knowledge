"""ROOT conditional analytic contracts; not a simulated or qualified iron device.

All geometry, bulk density, conductivity/access, pressure, recovery and price
examples are introduced hypotheses. Literature thin-film loading and plasma
numbers retain the precise boundaries described in the companion note.
Standard library only. No producer code or linked artifacts are used.
"""
import json
import math

F = 96485.33212
M_FE = 55.845e-3  # kg/mol, numerical stoichiometric convention
M_O = 15.999e-3
M_N = 14.0067e-3
AH_FE3_PER_KG = 3 * F / (3600 * M_FE)


def harvest_contract(fe_fraction, silica_alumina, recovery):
    """Favorable all-metal Fe product; other gangue/oxygen omitted, not gifted."""
    ore_kg_per_1000kg_metal = 1000 / (fe_fraction * recovery)
    incoming_si_al = ore_kg_per_1000kg_metal * silica_alumina
    allowed_product_mass = 1000 / 0.97
    non_fe_allowance = allowed_product_mass - 1000
    p_in = ore_kg_per_1000kg_metal * 0.000667
    p_out_max = allowed_product_mass * 0.0005
    return {
        "ore_kg_per_t_metal": ore_kg_per_1000kg_metal,
        "silica_alumina_in_kg_per_t_metal": incoming_si_al,
        "all_nonFe_allowance_kg_per_t_metal": non_fe_allowance,
        "minimum_silica_alumina_rejection_fraction": 1 - non_fe_allowance / incoming_si_al,
        "minimum_net_P_rejection_fraction": 1 - p_out_max / p_in,
        "scope": "optimistic composition screen; other gangue, unmetalized Fe and salts tighten it",
    }


def contact_packet(thickness_m=1e-4, bulk_density=2800, fe=0.5966,
                   recovery=0.9, faradaic_efficiency=0.9, current_A_m2=1000):
    ore = thickness_m * bulk_density
    metal = ore * fe * recovery
    charge = metal * AH_FE3_PER_KG / faradaic_efficiency
    active_h = charge / current_A_m2
    annual_hours = 8760 * 0.9
    t_per_h = 100000 / 8760  # nameplate; output and hours both multiplied by .9
    current = t_per_h * 1000 * AH_FE3_PER_KG / faradaic_efficiency
    area = current / current_A_m2
    # Introduced work surrogate: 5 MPa applied through 20 um at 50% efficiency.
    pressure = 5e6
    stroke = 2e-5
    efficiency_mech = 0.5
    work_J_per_m2 = pressure * stroke / efficiency_mech
    work_kWh_per_t_metal = work_J_per_m2 / metal * 1000 / 3.6e6
    return {
        "introduced_thickness_um": thickness_m * 1e6,
        "introduced_bulk_density_kg_m3": bulk_density,
        "ore_kg_m2_per_packet": ore,
        "credited_metal_kg_m2_per_packet": metal,
        "required_charge_Ah_m2": charge,
        "electrolysis_min_per_packet": active_h * 60,
        "annual_electrolysis_only_packets_per_station": annual_hours / active_h,
        "industrial_total_current_MA": current / 1e6,
        "actually_connected_area_m2": area,
        "introduced_pressure_MPa": pressure / 1e6,
        "force_MN_per_m2": pressure / 1e6,
        "introduced_stroke_um": stroke * 1e6,
        "introduced_reseat_work_kWh_per_t_metal": work_kWh_per_t_metal,
        "scope": "no contact/kinetics/downtime/frame/fatigue/wash performance supplied",
    }


def thin_film_gap():
    oxide_kg_m2 = 43e-6 * 1e4 / 1000  # 43 ug/cm2 converted to kg/m2
    fe_mass_fraction = 2 * M_FE / (2 * M_FE + 3 * M_O)
    metal_kg_m2 = oxide_kg_m2 * fe_mass_fraction
    all_reduction_Ah_m2 = AH_FE3_PER_KG * metal_kg_m2
    return {
        "reported_oxide_loading_kg_m2": oxide_kg_m2,
        "theoretical_full_metal_kg_m2": metal_kg_m2,
        "theoretical_full_reduction_Ah_m2": all_reduction_Ah_m2,
        "introduced_100um_packet_to_thinfilm_oxide_mass_ratio": 0.28 / oxide_kg_m2,
        "scope": "not a current-efficiency measurement, ore rate or scaling law",
    }


def volume_screen():
    # Introduced room-state density surrogates, not a measured stress law.
    rho_oxide, rho_metal = 5260.0, 7870.0
    ratio = (2 * M_FE / rho_metal) / ((2 * M_FE + 3 * M_O) / rho_oxide)
    return {"introduced_solid_volume_ratio": ratio,
            "introduced_unconstrained_linear_ratio": ratio ** (1 / 3),
            "scope": "shrinkage does not prove cracks, connected pores or retained electrical contact"}


def equipment_life(packet):
    area = packet["actually_connected_area_m2"]
    annual_t = 90000
    hours = 8760 * 0.9
    replacement_usd_m2 = 100.0
    return [{"introduced_part_life_h": life,
             "replacement_only_USD_t": area / annual_t * replacement_usd_m2 * hours / life}
            for life in [100, 1000, hours]]


def economic_screens():
    # Published rounded candidate ledger is retained; these are algebraic waivers.
    base = 787.0
    cell_power = 3.504
    return {
        "unchanged_sulfate_ledger_free_initialcapital_and_routine_maintenance_USD_t": base - 145 - 21,
        "unchanged_sulfate_ledger_also_free_all_cell_electricity_USD_t": base - 145 - 21 - cell_power * 40,
        "scope": "not an all-process lower bound; chemical/flow architecture may change",
        "introduced_direct_noncell_MWh_t": 0.65,
        "introduced_rectifier_efficiency": 0.95,
        "maximum_direct_cell_V_div_FE_under_4MWh_t": (4 - 0.65) * 0.95 / (AH_FE3_PER_KG / 1000),
    }


def plasma_boundary():
    # Troia2025 main Sections2--3: 3.2 MJ/mol fixed NOx, injected-power boundary.
    # The conversion is explicitly conditional on one N atom per reported NOx
    # equivalent; it does not independently inspect the rendered dimer equation.
    e = 3.2 / (3.6 * M_N)
    return {"reported_injected_energy_MJ_per_mol_NOx": 3.2,
            "conditional_oneN_equivalent_kWh_kgN": e,
            "conditional_oneN_equivalent_USD_kgN_at_40MWh": e * 0.04,
            "conditional_oneN_equivalent_USD_kgN_at_20MWh": e * 0.02,
            "scope": "NOx-equivalent convention conditional; not useful nitrate, wall AC, full plant or a universal plasma bound"}


packet = contact_packet()
out = {
    "kind": "ROOT independently derived conditional analytic contracts",
    "device_or_material_validation": False,
    "ah_per_kg_Fe_from_FeIII": AH_FE3_PER_KG,
    "ideal_selective_harvest": harvest_contract(0.5966, 0.126, 0.9),
    "thin_film_to_packet_gap": thin_film_gap(),
    "conditional_packet": packet,
    "conditional_volume_change": volume_screen(),
    "conditional_part_replacements": equipment_life(packet),
    "cohort_retention_examples": [
        {"number_of_required_reseatings": n,
         "minimum_retention_each_for_90pct_final": 0.9 ** (1 / n)}
        for n in [12, 40, 100]
    ],
    "economic_waivers": economic_screens(),
    "different_operation_plasma_boundary": plasma_boundary(),
    "symbolic_reversible_identity": {
        "definitions": "a=FeIII/II potential; b=FeII/0; c=OER, SAME consistent material activities",
        "split_work_per_F": "2*(a-b)+3*(c-a)=3*c-a-2*b",
        "direct_work_per_F": "3*(c-(a+2*b)/3)=3*c-a-2*b",
        "scope": "no numeric electrode potentials supplied; paid mixing/state return required",
    },
}
assert math.isclose(AH_FE3_PER_KG, 1439.78, rel_tol=1e-5)
assert math.isclose(packet["actually_connected_area_m2"] * 1000,
                    packet["industrial_total_current_MA"] * 1e6)
assert 0 < out["ideal_selective_harvest"]["minimum_silica_alumina_rejection_fraction"] < 1
print(json.dumps(out, indent=2, sort_keys=True))
