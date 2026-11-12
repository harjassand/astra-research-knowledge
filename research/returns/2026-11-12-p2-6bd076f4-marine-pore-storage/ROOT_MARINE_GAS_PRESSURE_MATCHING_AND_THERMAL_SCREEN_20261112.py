"""ROOT conditional screens for marine pore storage and pressure-matched gas storage.
Not a complete plant simulation. No producer code or archive is imported.
All efficiencies, prices, transfer coefficients and lives are declared assumptions.
"""
import json
import math

rho_w = 1025.0
g = 9.80665
p0 = 101325.0
depth = 600.0
T0 = 293.15
Rair = 287.0
p_high = p0 + rho_w*g*depth
ratio = p_high/p0
e_water = (p_high-p0)/3.6e6
e_air = p_high*math.log(ratio)/3.6e6

def screens():
    useful_kwh = 100000.0
    # INTRODUCED .85 full expansion-to-AC and .90 usable-volume fraction.
    # Neither is inferred from a component experiment.
    eta_out = 0.85
    usable = 0.90
    V = useful_kwh/(e_air*eta_out*usable)
    rho_air = p_high/(Rair*T0)
    # INTRODUCED ballast density; actual material/anchorage not constructed.
    rho_ballast = 2750.0
    ballast_kg = (rho_w-rho_air)*V/(1-rho_w/rho_ballast)
    rock_cost = 20.0 # USD/t INTRODUCED delivered/placed allowance, not quote
    ballast_cost = ballast_kg/1000*rock_cost
    # Ideal spheres are just an area and pressure-gradient diagnostic.
    bag_radius = 10.0
    bag_count_equiv = V/(4*math.pi*bag_radius**3/3)
    bag_area = 3*V/bag_radius
    gradient = (rho_w-rho_air)*g*2*bag_radius
    hoop_resultant = gradient*bag_radius/2 # thin spherical surrogate N/m
    converter_product = 0.93**2 * 0.90**2 * 0.97**2
    retained_needed = 0.65/converter_product
    cycle_days = 344/24
    max_lambda = -math.log(retained_needed)/cycle_days
    throttling_eff = math.log(ratio)/(ratio-1)
    water_per_heat = 1e6/(4180*5) # kg/s for 1MW and INTRODUCED5K rise
    U = 500.0 # W/m2/K INTRODUCED joint overall coefficient
    dT = 5.0
    HX_area = 1e6/(U*dT)
    rho_rock = 2750.0
    e_water_out = e_water*0.90
    porosity_min = 1/(1+15*1000*e_water_out/(rho_rock*rock_cost))
    # From the complete AVAILABLE marine return, conditional model figures.
    old_mass_t = 575051.0
    old_capex = 32.469e6
    old_total = old_capex/useful_kwh
    target_capex = 15*useful_kwh
    cycles_year = 8760*0.9/344
    crf = 0.08/(1-(1.08)**(-20))
    output_year_mwh = cycles_year*100
    all_service_budget = ((125-20/0.65)*output_year_mwh-target_capex*crf)
    return {
      'declared_depth_m':depth,
      'absolute_storage_pressure_bar':p_high/1e5,
      'pressure_ratio_to_atmosphere':ratio,
      'ideal_pressure_flow_work_kWh_per_m3':e_water,
      'ideal_isothermal_gas_flow_exergy_kWh_per_storage_m3':e_air,
      'warning_flow_work':'Gas flow exergy already includes the pressure-displacement operation; do not add another p*dV output credit.',
      'gas_capacity_and_anchor_surrogate':{
        'assumed_full_output_conversion':eta_out,'assumed_usable_fraction':usable,
        'storage_volume_m3':V,'ideal_gas_density_kg_per_m3':rho_air,
        'assumed_ballast_density_kg_per_m3':rho_ballast,
        'ballast_t':ballast_kg/1000,
        'assumed_delivered_placed_rock_USD_per_t':rock_cost,
        'ballast_only_USD_per_useful_kWh':ballast_cost/useful_kwh,
        '10m_radius_spherical_bag_equivalents':bag_count_equiv,
        'ideal_sphere_total_area_m2':bag_area,
        'full_height_hydrostatic_differential_Pa':gradient,
        'spherical_membrane_resultant_N_per_m_surrogate':hoop_resultant,
      },
      'whole_cycle_hypothetical_factors':{
        'gas_comp':0.93,'gas_exp':0.93,'hydraulic_charge':0.90,
        'hydraulic_generation':0.90,'electrical_each_way':0.97,
        'product_before_retention_auxiliaries':converter_product,
        'minimum_retention_for_65pct_if_all_other_aux_zero':retained_needed,
        'max_continuous_mass_loss_per_day_if_full_344h_exposed':max_lambda,
        'warning':'Gas factors are hypothetical over the WHOLE1bar-to-storage cycle. A7-to210bar single-shot result does not establish them.',
      },
      'pressure_matching':{
        'fixed_high_pressure_supply_ideal_comp_eff_over_FULL_stroke':throttling_eff,
        'fixed_high_pressure_input_over_isothermal_minimum':1/throttling_eff,
        'assumption':'One atmospheric-case piston, zero deadvolume, compression plus high-pressure ejection, constant high-pressure hydraulic supply and no pressure-energy recovery.',
      },
      'thermal_1MW_surrogate':{
        'assumed_total_U_W_per_m2K':U,'assumed_deltaT_K':dT,
        'heat_exchange_area_m2':HX_area,
        'liquid_flow_kg_per_s_at_5K':water_per_heat,
        'heat_exchanged_each_100h_MWh':100,
        'warning':'An isothermal machine exchanges roughly its gas-work power as heat. The ambient heat source/sink, finite approach and circulation are not free.',
      },
      'old_pore_design_diagnostics':{
        'conditional_core_t':old_mass_t,
        'conditional_capital_USD_per_useful_kWh':old_total,
        'entire_target_capital_USD_per_core_t_if_all_else_free':target_capex/old_mass_t,
        'ideal_min_porosity_to_fit_rock_cost_alone_600m':porosity_min,
        'assumption':'Hypothetical uniform pore bed, full useful void,90pctoutput; excludes barrier, heels, access, installation and machinery. Not a universal structural bound.',
      },
      'finance':{
        'cycles_per_year':cycles_year,'CRF_20y_8pct':crf,
        'all_annual_service_replacement_removal_budget_USD_at_target_and_20charging':all_service_budget,
        'remaining_after_2pct_routine_maintenance_USD_per_year':all_service_budget-0.02*target_capex,
      },
    }

if __name__ == '__main__':
    x=screens()
    assert e_air > 4*e_water
    assert 0 < x['pressure_matching']['fixed_high_pressure_supply_ideal_comp_eff_over_FULL_stroke'] < 0.08
    assert abs(x['finance']['cycles_per_year']-22.9186046512)<1e-8
    print(json.dumps(x,indent=2,sort_keys=True))
