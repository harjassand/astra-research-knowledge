"""Independent accounting screens, not a fitted ore or concrete process."""
import json
import math
from pathlib import Path

F = 96485.33212
M_FE = .055845
M_O = .015999
M_H2 = .00201588
M_CAO = .0560774
M_CO2 = .0440095
crf = .08*(1.08**20)/(1.08**20-1)

# Diagnostics of the returned ledger, not universal ironmaking bounds.
ore = {
    "returned_complete_USD_t": 2038,
    "returned_purchased_MWh_t": 5.894,
    "returned_joint_favorable_USD_t": 1423,
    "if_initial_capital_and_all_renewals_free_USD_t": 2038-449.2-919.6,
    "if_initial_capital_renewals_and_all_energy_free_USD_t": 2038-449.2-919.6-237.2,
    "if_all_energy_free_other_lines_unchanged_USD_t": 2038-237.2,
    "noncell_MWh_t_from_return": 5.894-3.950,
    "max_V_div_FE_at_4MWh_with_unchanged_noncell_and_95pct_rectifier":
        (4-(5.894-3.950))*.95/1.43978,
}

# Independent alternative: magnetizing upgrade, rather than making Fe metal.
feed_Fe = 1000*.5966
recovered_Fe = feed_Fe*.95
concentrate = recovered_Fe/.69
magnetite_Fe_fraction = 3*M_FE/(3*M_FE+4*M_O)
hematite_Fe_fraction = 2*M_FE/(2*M_FE+3*M_O)
mag = {
    "introduced_feed_Fe_kg_t": feed_Fe,
    "introduced_95pct_Fe_recovery_69pct_grade_concentrate_kg_tfeed": concentrate,
    "allowed_nonmagnetite_mass_if_all_recovered_Fe_is_magnetite_kg":
        concentrate-recovered_Fe/magnetite_Fe_fraction,
    "allowed_nonhematite_mass_if_all_recovered_Fe_is_hematite_kg":
        concentrate-recovered_Fe/hematite_Fe_fraction,
    "P_rejection_needed_at_introduced_0point03pct_product_P":
        1-concentrate*.0003/.667,
    "if_P_uniform_in_retained_Fe_max_P_rejection_at_95pct_Fe_recovery": .05,
    "hematite_to_magnetite_charge_Ah_tfeed_ideal": (feed_Fe/M_FE)*(F/3)/3600,
    "introduced_1point5V_90pct_FE_95pct_rectifier_kWh_tfeed":
        (feed_Fe/M_FE)*(F/3)/3600*1.5/.9/.95/1000,
    "introduced_H2_to_magnetite_kg_tfeed_stoichiometric": (feed_Fe/M_FE)/6*M_H2,
    "introduced_52kWh_kg_H2_plus_gross_480C_sensible_kWh_tfeed":
        (feed_Fe/M_FE)/6*M_H2*52+1000*.8*(480-25)/3600,
}

# Conservation of original paste and original aggregate; origin is not Ca assay.
liberation = []
for paste_fraction in (.15,.20,.25,.30):
    paste = 1000*paste_fraction
    aggregate = 1000-paste
    paste_recovered = .90*paste
    allowed_aggregate_loss = .05*aggregate
    min_paste_purity_for_95pct_aggregate_recovery = (
        paste_recovered/(paste_recovered+allowed_aggregate_loss))
    for purity in (.85,.90,.95):
        paste_product = paste_recovered/purity
        aggregate_to_paste = paste_product-paste_recovered
        agg_product_agg = aggregate-aggregate_to_paste
        residual_paste = paste-paste_recovered
        agg_product = agg_product_agg+residual_paste
        assert abs(paste_product+agg_product-1000)<1e-10
        drying=[]
        for cake_solids in (.75,.90):
            cake_water=paste_product*(1/cake_solids-1)
            delivered_water=paste_product*(1/.98-1)
            evaporated=max(0,cake_water-delivered_water)
            drying.append({"introduced_filter_cake_solids":cake_solids,
                           "water_to_evaporate_kg_tfeed":evaporated,
                           "introduced_2260kJ_kg_latent_only_kWh_tfeed":evaporated*2260/3600})
        liberation.append({
            "introduced_paste_fraction":paste_fraction,
            "introduced_paste_recovery":.90,"introduced_paste_product_purity":purity,
            "paste_product_dry_kg_tfeed":paste_product,
            "original_aggregate_recovery":agg_product_agg/aggregate,
            "original_aggregate_purity_in_aggregate_product":agg_product_agg/agg_product,
            "min_paste_purity_for_95pct_aggregate_recovery":min_paste_purity_for_95pct_aggregate_recovery,
            "drying_screens":drying,
        })

throughput=100000/3600  # kg/s; INTRODUCED100t/h
sample_kg=.14
shots_per_chunk=10
pulse_J=84
shots_s=throughput/sample_kg*shots_per_chunk
pulse_kWh_t=shots_per_chunk*pulse_J/sample_kg/3600
pulse = {
    "introduced_chunk_mass_kg":sample_kg,"introduced_J_per_shot":pulse_J,
    "introduced_shots_per_chunk":shots_per_chunk,
    "capacitor_energy_kWh_t":pulse_kWh_t,
    "shots_s_at_100tph_if_independent_chunks":shots_s,
    "capacitor_power_kW":shots_s*pulse_J/1000,
    "introduced_80pct_charger_wall_power_kW":shots_s*pulse_J/1000/.8,
    "parallel_modules_needed_at_introduced_100Hz_per_module":math.ceil(shots_s/100),
    "introduced_100USD_wear_pair_material_only_USD_t_at_1million_shots":
        1000/sample_kg*shots_per_chunk*100/1e6,
    "introduced_100USD_wear_pair_material_only_USD_t_at_10million_shots":
        1000/sample_kg*shots_per_chunk*100/1e7,
}

thermal = {
    "introduced_20pct_paste_cp1kJkgK_selective_100K_heat_kWh_t":200*1*100/3600,
    "introduced_whole_concrete_cp1_500K_gross_heat_kWh_t":1000*1*500/3600,
    "introduced_thermal_mismatch_stress_MPa_E30GPa_dalpha3ppmK_dT50K":30e9*3e-6*50/1e6,
    "all_values_unmeasured_no_fracture_or_dielectric_law":True,
}

# An oxide correction diagnostic: contaminating quartz requires fresh calcium.
ca_per_silica=3*M_CAO/.0600843
extra_CaO=10*ca_per_silica
cement = {
    "introduced_extra_quartz_kg_per_t_product":10,
    "CaO_for_C3S_ratio_only_kg":extra_CaO,
    "limestone_process_CO2_for_that_CaO_kg":extra_CaO*M_CO2/M_CAO,
    "limits":"Simple 3CaO:SiO2 stoichiometry, not clinker phase equilibrium, source data, or a full kiln model.",
}

annual_feed=100*8760*.9
finance={
    "introduced_100tph_90pct_annual_tfeed":annual_feed,
    "introduced_50kWh_t_at_40USD_MWh_electricity_USD_t":2,
    "introduced_20USD_t_ceiling_minus_6haul_4other_2power_USD_t_for_capital_service":8,
    "max_capital_at_20y8pct_and_introduced_3pct_cap_maintenance_USD":8*annual_feed/(crf+.03),
    "same_ceiling_at_60pct_utilization_USD":8*100*8760*.6/(crf+.03),
}

result={"status":"INTRODUCED_CONSERVATION_AND_RESOURCE_SCREENS_NOT_A_WORKING_INVENTION",
        "ore_ledger_diagnostics":ore,"magnetizing_upgrade_alternative":mag,
        "concrete_liberation_cases":liberation,"pulse_throughput_and_wear":pulse,
        "thermal_surrogates":thermal,"contamination_calcium_diagnostic":cement,
        "full_processing_cost_screen":finance,
        "limits":["No source/SI/artifact recovery or producer code executed.",
                  "No liberation, phase selectivity, lifetime, wall efficiency, price or industrial rate was measured.",
                  "A crack or lower crushing strength is not original-paste purity or aggregate acceptance.",
                  "A staged classify-and-retreat mechanism must pay real classification, water, drying, controls and waste.",
                  "No recovered-paste market, free heat, disposal credit, carbonation credit or future physical execution is supplied."]}
p=Path(__file__).with_suffix('.json')
p.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
