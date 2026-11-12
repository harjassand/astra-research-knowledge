#!/usr/bin/env python3
"""ROOT independent conditional diagnostics, not producer execution or physical data."""
import json,math
from pathlib import Path
F=96485.33212; R=8.314462618; T=298.15
M_N=.0140067; M_AS=.13213952; M_acid=.098079; M_base=.039997
def crf(r,n): return r/(1-(1+r)**-n)
def suppression(pe): return pe/math.expm1(pe) if pe else 1.
o={}
o["peroxide_fixed_displayed_ledger"]={
 "reference_USD_kg":2.078,"favorable_bulk":.836,"required_30pct_advantage":.7*.836,
 "remaining_water_storage_delivery_labor_QA":.465,"operating_power":.220,"other_service":.022,
 "remaining_blocks_with_reactor_capital_and_all_listed_wear_free":.465+.220+.022,
 "remaining_after_electricity_also_free":.465+.022,
 "free_hardware_remaining_gap":(.465+.220+.022)-.7*.836,
 "cell_assembly_capital_headroom_fraction":1e6/921000-1,
 "warning":"Rounded displayed blocks; water/storage capital may remain in its own block. Fixed-ledger screens, not all-peroxide lower bounds."}
o["campaign"]={"process_kWh_per_accepted_kg":27.054/4.23378,
 "with_first_qualification":31.554/4.23378,
 "output_margin_kg":4.23378-4.167,"relative_output_margin":4.23378/4.167-1,
 "first_prep_including_25p5kWh":(31.554+25.5)/4.23378,
 "decay_98pct_retention_ceiling_h_inv":-math.log(.98)/24}
u=5.02e-6; L=.002; D=7e-10; pe=u*L/D
rows=[]
for a in [0,.001,.01,.05,.10]:
 # Same column diffusivity, same boundary concentrations and geometric length.
 # A zero-flow area fraction leaves alpha of the unprotected diffusive flux.
 # All flow redistributed to remaining area keeps total volume flow fixed.
 ratio=a+(1-a)*suppression(pe/(1-a))
 rows.append({"stagnant_area_fraction":a,"total_volume_flow_held_fixed":True,
 "backflux_relative_to_no_flow":ratio,
 "factor_relative_to_homogeneous":ratio/suppression(pe)})
o["introduced_parallel_flow_defects"]={"Pe":pe,"uniform_suppression":suppression(pe),"rows":rows,
 "warning":"Independent nonreacting parallel-column surrogate; no cast-resin map or common electric-current solution. An area-average Peclet number does not certify local protection."}
o["introduced_adsorption_reset"]=[]
for tau in [1,3,6,12]:
 o["introduced_adsorption_reset"].append({"tau_h":tau,"initial_bound_mg":452,"after_6h_mg":452*math.exp(-6/tau),
 "warning":"No measured isotherm or desorption law. Producer reset tolerance is not an added human qualification rule."})
charge=F/(M_N*3600)
o["nitrogen_stoichiometry"]={"ideal_one_charge_Ah_kgN":charge,
 "kWh_kgN_per_volt_at_ideal_one_charge_transport":charge/1000,
 "pure_H2SO4_kg_per_kgN_AS":M_acid/(2*M_N),
 "dry_AS_kg_per_kgN":M_AS/(2*M_N),
 "pure_NaOH_kg_per_kgN_if_one_base_equiv":M_base/M_N,
 "5wtpct_N_product_kg_per_kgN":20,
 "stoichiometric_acid_cost_at_introduced_0p12_USD_kg":M_acid/(2*M_N)*.12,
 "one_base_equiv_cost_at_introduced_0p5_USD_kg":M_base/M_N*.5}
o["introduced_proton_swing_work"]=[]
for dpH in [1,2.5,4]:
 o["introduced_proton_swing_work"].append({"delta_pH":dpH,
 "reversible_voltage_V":R*T/F*math.log(10)*dpH,
 "reversible_kWh_kgN_per_proton_equiv":R*T*math.log(10)*dpH/M_N/3.6e6,
 "warning":"Ideal reversible proton work only; not the full free energy of NH4 separation, acid manufacture, buffering, stripping or salt restoration."})
o["nitrogen_electrotransport_introduced"]=[]
for V in [.3,.6,1,1.5,2]:
 for ce in [.5,.8,.95]:
  o["nitrogen_electrotransport_introduced"].append({"terminal_V":V,"effective_N_charge_efficiency":ce,
  "rectifier_efficiency":.95,"auxiliary_kWh_kgN":.5,
  "purchased_kWh_kgN":charge/1000*V/(ce*.95)+.5})
o["introduced_feed_and_alkalinity"]=[]
for N_g_L in [.7,1,1.5]:
 for alk_g_CaCO3_L in [2,3.5,5]:
  # CaCO3 equivalent mass 50.043 g/eq.
  n=N_g_L/14.0067; alk=alk_g_CaCO3_L/50.043
  o["introduced_feed_and_alkalinity"].append({"TAN_gN_L":N_g_L,"alk_gCaCO3_L":alk_g_CaCO3_L,
   "equiv_alkalinity_per_TAN":alk/n,
   "feed_m3_per_kg_recoveredN_at_90pct":1/(N_g_L*.9),
   "warning":"Alkalinity is not freely available OH. Real inorganic-carbon/pH/other-ion speciation and acid/base outlet states must close."})
o["introduced_NH3_fraction"]=[]
for pH in [7.5,8,9,9.5,10]:
 o["introduced_NH3_fraction"].append({"pH":pH,"ideal_25C_pKa":9.25,"free_fraction":1/(1+10**(9.25-pH))})
# Product water: 5 wt% N gives 20kg product/kgN. Pure AS carries 4.717kg dry matter.
acid50=M_acid/(2*M_N)/.5; dryAS=M_AS/(2*M_N)
o["introduced_capture_water_budget"]={
 "water_in_50wtpct_acid_kg_kgN":acid50*.5,
 "water_allowed_in_5wtpctN_AS_kg_kgN":20-dryAS,
 "remaining_vapor_plus_makeup_water_allowance":20-dryAS-acid50*.5,
 "warning":"No nitrate/organic nitrogen counted; no measured water-vapor/membrane-wetting map supplied."}
annual=1000*365*.9
capital=1e6*crf(.08,20)/annual; power=3*.08
acid=M_acid/(2*M_N)*.12
o["introduced_industrial_cost"]={
 "accepted_kgN_year":annual,"capital_1M_USD_kgN":capital,
 "3kWh_kgN_power_at_80":power,"stoich_acid_at_0p12":acid,
 "730_loaded_labor_h_at_60_USDh_per_kgN":730*60/annual,
 "remaining_to_2_USD_kgN_before_base_and_other_items":2-capital-power-acid-730*60/annual,
 "warning":"Includes neither a quotation nor a supplied mechanism, pretreatment life, chemical minimization or disposal credit."}
o["status"]="CONDITIONAL_ACCOUNTING_AND_TRANSPORT_SCREENS_NOT_AN_INVENTION"
assert abs(charge/1000-1.913426)<.001
assert all(x["backflux_relative_to_no_flow"]>=suppression(pe) for x in rows)
Path(__file__).with_suffix(".json").write_text(json.dumps(o,indent=2)+"\n")
print(json.dumps(o,indent=2))
