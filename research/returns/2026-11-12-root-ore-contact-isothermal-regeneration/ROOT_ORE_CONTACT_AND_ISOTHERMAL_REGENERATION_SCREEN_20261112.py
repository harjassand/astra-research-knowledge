"""ROOT analytic contracts, not a device simulation or measured parameter fit.

No producer code or archive is imported. Standard-library arithmetic only.
All assumed dimensions, prices, transport constants and lifetimes below are
explicit sensitivity inputs, never inferred jointly from separate experiments.
"""
import json
import math

F = 96485.33212  # C/mol; declared standard Faraday constant
M_FE = 55.845   # g/mol, declared stoichiometric mass
M_H2 = 2.01588 # g/mol, declared stoichiometric mass; no NIST thermochemistry
M_NIOH = 92.707 # g/mol, declared stoichiometric mass
Q_FE = 3 * F * 1000 / M_FE / 3600  # Ah per kg Fe(III)-derived metal
Q_H2 = 2 * F * 1000 / M_H2 / 3600


def iron_screen():
    # These ledger figures come from the complete AVAILABLE DEC9C2C6 return.
    # They are a conditional engineering model, not independent plant data.
    old_cost = 684.0
    old_rectified_cell = 4.709 # MWh/t, numerically kWh/kg
    all_other_energy = 5.592 - old_rectified_cell
    electrical_efficiency = 0.95 # INTRODUCED, close to old ledger convention
    target_cell = 4 - all_other_energy
    max_v_over_fe = target_cell * electrical_efficiency / (Q_FE / 1000)
    favorable_cell = (Q_FE / 1000) * 1.7 / (0.90 * electrical_efficiency)
    waived_chemical_and_waste = 32.2 + 28.5 + 3.9 + 45.8
    # Simultaneous free waivers are a diagnostic, NOT an implementable scenario.
    extreme_waiver_cost = (old_cost - waived_chemical_and_waste
                          - 40 * (old_rectified_cell - favorable_cell))
    ore_fe = 0.5966
    recovery = 0.90
    product_fe = 0.97
    feed_p = 0.000667
    product_limit_p = 0.0005
    min_p_rejection = 1 - ((ore_fe * recovery / product_fe)
                           * product_limit_p / feed_p)

    # Uniform-film Fick surrogate. 2.3 mM is the paper's predicted solubility,
    # not an actual available electroactive concentration on this ore.
    concentration = 2.3 # mol/m3 = 2.3 mM
    diffusion = 1e-9   # m2/s, INTRODUCED hypothetical
    film = 100e-6     # m, INTRODUCED hypothetical
    j_dissolved = 3 * F * diffusion * concentration / film
    film_for_1000 = 3 * F * diffusion * concentration / 1000

    # Product-seeded cathode SURROGATE: geometric area is not connected area.
    rho_fe = 7870.0
    radius = 0.5e-3
    area_per_kg = 3 / (rho_fe * radius)
    kg_per_hour = 100000 * 1000 / 8760 # on-stream nameplate production
    mean_fe = 0.90
    wetted_current_density = 1000.0
    current = kg_per_hour * Q_FE / mean_fe
    connected_area = current / wetted_current_density
    granular_cases = []
    for chi in [1.0, 0.3, 0.1]:
        mass = connected_area / (area_per_kg * chi)
        granular_cases.append({
            'electrically_accessible_fraction_assumed': chi,
            'required_total_granule_geometric_area_m2': connected_area / chi,
            'iron_seed_inventory_t': mass / 1000,
            'seed_inventory_hours_of_product': mass / kg_per_hour,
        })

    # Hypothetical poison film on 5-micron-radius ore particles; no observation
    # that all actual gangue is such a film, or that abrasion selectively removes it.
    ore_kg_per_kg_fe = 1 / (ore_fe * recovery)
    rho_ore = 5200.0
    ore_radius = 5e-6
    ore_surface = 3 * ore_kg_per_kg_fe / (rho_ore * ore_radius)
    film_thickness = 2e-9
    film_density = 2500.0
    poison_mass = ore_surface * film_thickness * film_density
    gamma = 1.0 # J/m2 INTRODUCED surface-work scale, not a milling quote
    surface_work = ore_surface * gamma / 3.6e6
    # theta_dot = k_form*(1-theta) - k_strip*theta
    live_target = 0.90
    strip_over_form = live_target / (1 - live_target)
    return {
        'FeIII_charge_Ah_per_kg': Q_FE,
        'old_model_noncell_declared_energy_MWh_per_t': all_other_energy,
        'max_voltage_over_FE_at_4MWh_per_t_with_old_other_loads': max_v_over_fe,
        'Vmax_if_FE_0p66': max_v_over_fe * 0.66,
        'Vmax_if_FE_0p90': max_v_over_fe * 0.90,
        'introduced_1p7V_0p90FE_cell_MWh_per_t': favorable_cell,
        'same_other_loads_total_MWh_per_t': favorable_cell + all_other_energy,
        'unphysical_free_chemical_waste_waiver_cost_USD_per_t': extreme_waiver_cost,
        'remaining_saving_to_450_even_after_free_waivers_USD_per_t': extreme_waiver_cost-450,
        'minimum_P_rejection_fraction_given_declared_feed_product': min_p_rejection,
        'dissolved_film_surrogate': {
            'assumed_D_m2_per_s': diffusion,
            'predicted_not_measured_C_mol_per_m3': concentration,
            'assumed_film_m': film,
            'j_A_per_m2': j_dissolved,
            'film_m_for_1000A_per_m2': film_for_1000,
        },
        'granular_contact_surrogate': {
            'assumed_radius_m': radius,
            'geometric_area_m2_per_kg': area_per_kg,
            'nameplate_product_kg_per_h': kg_per_hour,
            'required_total_current_MA': current / 1e6,
            'required_connected_area_m2': connected_area,
            'cases': granular_cases,
        },
        'selective_surface_renewal_hypothesis': {
            'ore_radius_m': ore_radius,
            'assumed_ore_density_kg_per_m3': rho_ore,
            'surface_m2_per_kg_accepted_Fe': ore_surface,
            'assumed_2nm_film_kg_per_kg_Fe': poison_mass,
            'introduced_surface_work_kWh_per_kg_Fe': surface_work,
            'k_strip_over_k_form_for_90pct_live_area': strip_over_form,
            'warning': 'No measured film, selective removal, rate, wear, power or phase closure is supplied.',
        },
    }


def hydrogen_screen():
    # Whole-cycle reversible mediator energy cancels at the same restored state.
    # This is not an efficiency claim for the HELD E-TAC source.
    net_fe = 0.995
    eta_rectifier = 0.96
    r = 8.314462618
    temperature = 298.15
    compressor_eta = 0.65
    compression = (1000 / M_H2) * r * temperature * math.log(30) / 3.6e6 / compressor_eta
    aux = 0.5 # kWh/kg INTRODUCED placeholder; not an achieved auxiliary budget
    voltage_budget = (45 - compression - aux) * 1000 * net_fe * eta_rectifier / Q_H2
    source_2p12_screen = Q_H2 * 2.12 / 1000 / net_fe / eta_rectifier + compression + aux
    redox_mass_per_h2 = 2 * M_NIOH / M_H2
    # Two interchangeable equal cassettes, one charges while the other discharges.
    # tau is one half-cycle residence; one full cassette cycle takes 2*tau.
    cassette_cases = []
    for tau_h in [0.5, 6.0]:
        for usable in [0.2, 0.5]:
            mass = 2 * redox_mass_per_h2 * (1 / 24) * tau_h / usable / net_fe
            full_cycles_per_year = (8760 * 0.9) / (2 * tau_h)
            cassette_cases.append({
                'tau_half_cycle_h': tau_h,
                'usable_fraction_assumed': usable,
                'pair_active_NiOH_kg_per_kgH2_per_day': mass,
                'full_cycles_per_calendar_year_at_90pct': full_cycles_per_year,
                '5000_cycle_life_years_not_measured': 5000 / full_cycles_per_year,
            })
    replacements = []
    for cycles in [5000, 50000]:
        replacements.append({
            'assumed_full_cycles': cycles,
            'assumed_usable_fraction': 0.2,
            'assumed_delivered_active_cost_USD_per_kg': 10,
            'active_material_only_renewal_USD_per_kgH2': redox_mass_per_h2 * 10 / (0.2 * cycles * net_fe),
        })
    # Pure O2 headspace carryover per swap, before any cleanup; dissolved O2,
    # bubbles, adsorption, leaks and pressure differences are NOT included.
    ideal_molar_volume = r * temperature / 101325 # m3/mol at 1 atm
    gas_cases = []
    for tau_h in [0.5, 6.0]:
        h2_moles_per_batch = (1 / 24) * tau_h * 1000 / M_H2
        allowable_o2_moles = (5e-6 / (1 - 5e-6)) * h2_moles_per_batch
        gas_cases.append({
            'tau_h': tau_h,
            'max_unremoved_pure_O2_carryover_mL_at_1atm': allowable_o2_moles * ideal_molar_volume * 1e6,
        })
    return {
        'H2_charge_Ah_per_kg': Q_H2,
        'assumed_net_FE': net_fe,
        'assumed_rectifier_efficiency': eta_rectifier,
        'introduced_ideal_1to30bar_compression_kWh_per_kg': compression,
        'introduced_other_aux_kWh_per_kg': aux,
        'max_whole_cycle_equivalent_cell_voltage_for_45kWh_per_kg': voltage_budget,
        'remaining_HER_OER_ohmic_V_if_Erev_1p23_and_mediator_loss_0p12': voltage_budget - 1.23 - 0.12,
        'source_2p12V_transferred_into_declared_full_boundary_kWh_per_kg': source_2p12_screen,
        'redox_active_NiOH_kg_per_kgH2_at_full_use': redox_mass_per_h2,
        'cassette_cases': cassette_cases,
        'active_replacement_cases': replacements,
        'gas_carryover_cases': gas_cases,
        'warning': 'Not an achievable joint operating point, complete plant model, supplier quote or life qualification.',
    }


if __name__ == '__main__':
    out = {'iron': iron_screen(), 'hydrogen': hydrogen_screen()}
    # Arithmetic identities validate these calculations, not physical assumptions.
    assert abs(Q_FE - 1439.7787) < 0.001
    assert abs((Q_FE/1000)*3.2/0.84 - 5.4848712) < 0.00001
    assert out['iron']['granular_contact_surrogate']['cases'][2]['iron_seed_inventory_t'] > 200
    assert out['hydrogen']['max_whole_cycle_equivalent_cell_voltage_for_45kWh_per_kg'] < 1.54
    print(json.dumps(out, indent=2, sort_keys=True))
