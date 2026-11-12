"""ROOT own stoichiometric/cost contracts, not a material/device simulation."""
import math,json
from pathlib import Path
F=96485.33212;M=0.0340147;Mwater=.01801528;Moxygen=.0319988
Ah=2*F/(M*3600);kWhV=Ah/1000
crf=.08/(1-1.08**-20)
kg_y=1000*365*.9
h2={'reference_operating_kWh_kg':46.7198,'reference_USD_kg':6.527,'free_active_kit_USD_kg':6.527-3.204,'free_active_kit_and_initial_capital_USD_kg':6.527-3.204-1.594,'maximum_capital_for_2USD_if_kit_free_and_all_other_lines_fixed':max(0,(2-(6.527-3.204-1.594))*kg_y/crf),'allowed_average_extra_V_for_1kWh_kg_at_26_59kWh_V':1/26.59,'maximum_linear_drift_uV_h_for_1kWh_increment_over_10000_vs_initial100h':1/26.59/((10000-100)/2)*1e6,'saving_5_91kWh_at20USD_MWh_USD_kg':5.91*.02,'NPV_of_that_saving_USD':5.91*.02*kg_y/crf,'qualification':'Static displayed-ledger diagnostics, not free hardware, life or an all-H2 lower bound.'}
# Buffer for uninterrupted 1kg/day delivery through producer-defined 8h shutdown.
needed_h2=.3333333333333333
h2['ideal_30bar_25C_buffer_L_for_8h_at1kg_day']=needed_h2/.00201588*8.314462618*298.15/(30e5)*1000
h2['warning']='The producer 0.1K reset tolerance is its own model criterion, not an imposed human 0.1K gate. A small thermal reset repair does not close the main energy/cost endpoint.'

# New chemical operation, useful product stoichiometry.
product={'two_electron_Ah_kg_active':Ah,'two_electron_kWh_per_V_kg':kWhV,'H2_charge_per_kg_26590_divided_by_peroxide':26590/Ah,'water_reacted_kg_kgactive':Mwater/M,'net_O2_consumed_kg_kgactive_if_only_water_O2_H2O2':.5*Moxygen/M,'solution_mass_kg_at3pct_perkgactive':1/.03,'pure_water_input_min_kg_kgactive_for3pct':1/.03-1+Mwater/M,'gross_cathode_O2_kg_kgactive_no_anode_recycle_if_cathode_only':Moxygen/M}

cases=[]
for name,V,fc,fa,retain in [('cathode_only_A',2.4,.9,0.,.98),('cathode_only_B',2.7,.9,0.,.98),('paired_example',2.7,.9,.8,.98),('paired_lower_selectivity',3.0,.8,.4,.95)]:
 eta=.96;effective=(fc+fa)*retain
 e=kWhV*V/(eta*effective)
 current=(1000*Ah/24)/effective
 area=current/2000
 prep_cost_m2=350.;life=2000.;h_y=8760*.9
 renewal=area*prep_cost_m2*h_y/life/kg_y
 cap=1e6;capital=crf*cap/kg_y
 energy_cost=(e+.30)*.04
 cases.append({'name':name,'V':V,'gross_cathodic_yield':fc,'gross_anodic_yield':fa,'net_product_retention':retain,'rectifier_eta':eta,'stack_rectified_kWh_kgactive':e,'introduced_aux_kWh_kg':.30,'whole_introduced_kWh_kg':e+.30,'series_equivalent_current_A_for1t_day':current,'active_area_m2_at0_2A_cm2':area,'energy_USD_kg_at40':energy_cost,'capital_USD_kg_at1M':capital,'kit_renewal_USD_kg_at350USD_m2_2000h':renewal,'remaining_USD_kg_below0_8_for_all_other_labor_water_controls_waste':.8-energy_cost-capital-renewal,'scope':'All V/yields/retention/material price/life/aux/capital are introduced and jointly unqualified. Sum yields may reach2 only when actual net new peroxide from both electrodes is separately demonstrated without double counting crossover or stock.'})

# Useful concentration cannot be replaced by a lower-concentration beaker result.
conc=[]
for inlet in [.002,.01,.03,.20]:
 water_remove=max(0,1/inlet-1/.03)
 conc.append({'initial_mass_fraction':inlet,'water_to_remove_kg_perkgactive_to3pct':water_remove,'introduced_0_2kWh_kgwater_concentration_work':water_remove*.2,'qualification':'Mass balance plus introduced complete drying duty, not a suitable peroxide evaporator or thermal stability claim.'})

# Independent comparison: peroxide via on-site H2 rather than freely purchased laboratory H2.
h2_input_kg=.00201588/M
upstream={'H2_kg_perkg_H2O2_if_one_H2_per_product':h2_input_kg,'H2_operating_energy_kWh_kgactive_at_returned46_7198':h2_input_kg*46.7198,'H2_cost_USD_kgactive_at_returned6_527':h2_input_kg*6.527,'warning':'Does not establish peroxide synthesis or process viability. Paid upstream H2 may allow a different route, but no pure gas, pressure or preparation is free and return electricity needs an actual path.'}

# Lifetime/product exposure: a tracer inventory cannot become new useful peroxide.
# Introduced first-order product loss in a continuously stirred receiver at steady state.
retention=[]
for kh in [.0001,.001,.01]:
 for residence in [1.,12.,24.]:
  y=1/(1+kh*residence)
  retention.append({'introduced_loss_per_h':kh,'receiver_mean_h':residence,'steady_outlet_retention':y,'loss_fraction':1-y,'scope':'CSTR first-order surrogate only; actual decomposition depends on concentration, pH, metal contamination, light and temperature.'})

# Area, life and periodic manufacture expose the actual renewal contract.
renewals=[]
for cost in [100.,350.,1000.]:
 for life in [1000.,5000.,20000.]:
  c=next(x for x in cases if x['name']=='cathode_only_A')
  renewal=c['active_area_m2_at0_2A_cm2']*cost*(8760*.9)/life/kg_y
  renewals.append({'introduced_prepared_kit_USD_m2':cost,'introduced_life_h':life,'material_renewal_USD_kgactive':renewal,'labor_downtime_waste_not_included':True})

# Coherent complete-interval accounting example, not a fitted 100h reactor.
active_rate=.060 # kg/h net generated before receiver loss, introduced installed headroom.
t_accept=88.;gross=active_rate*t_accept
loss=gross*.02;sample=.015;retained=.040;accepted=gross-loss-sample-retained
c=next(x for x in cases if x['name']=='cathode_only_A')
energy=gross*c['stack_rectified_kWh_kgactive']+100*.015+1.0 # introduced BOP/conditioning
campaign={'hours':100,'accepted_production_h':t_accept,'introduced_rate_kgactive_h':active_rate,'gross_active_kg':gross,'product_decomposition_kg':loss,'destructive_samples_kg':sample,'end_retained_inventory_kg':retained,'accepted_kgactive':accepted,'introduced_whole_energy_kWh':energy,'introduced_whole_kWh_kgaccepted':energy/accepted,'qualification':'Stoichiometric scheduled example only. Does not supply 3pct concentration, reactor transients, accepted quality, heat, reservoir state or a build.'}
assert abs(gross-loss-sample-retained-accepted)<1e-12
assert product['net_O2_consumed_kg_kgactive_if_only_water_O2_H2O2']>0
out={'scope':'ROOT analytic contracts only; no producer execution, property-library installation, physical experiment or purchased equipment. Introduced parameters are unqualified; source claims are not synthesized into a device.','hydrogen_static_ledger':h2,'peroxide_stoichiometry':product,'electrode_cases':cases,'concentration':conc,'paid_H2_alternative':upstream,'receiver_loss':retention,'renewal_cost_cases':renewals,'complete_interval':campaign}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k]for k in ['hydrogen_static_ledger','peroxide_stoichiometry','electrode_cases','concentration','paid_H2_alternative','complete_interval']},indent=2))
