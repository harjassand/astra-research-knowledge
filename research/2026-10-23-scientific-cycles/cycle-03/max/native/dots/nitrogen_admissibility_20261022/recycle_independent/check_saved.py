"""Read saved outputs and evaluate thermodynamic endpoints only; no chemistry integration.

The parent trajectory is not rerun. All source files are read-only.
"""
from pathlib import Path
import hashlib,json,sys
import numpy as np
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/'nitrogen_finite_cycle_20261021/thermo_helper'))
from helper import ThermoKernel
K=ThermoKernel()
source=BASE/'nitrogen_admissibility_20261022/recycle_quench/result.json'
data=json.loads(source.read_text())
fresh=np.array([.79*K.W[0],.21*K.W[1],0,0,0,0]);fresh/=fresh.sum()
W=K.W
A=np.array([[2,0,1,0,1,1],[0,2,0,1,1,2]],float)
def h(T,Y):
 _,hs,_=K.thermochemistry(np.array([float(T)]))
 return float(np.sum(np.asarray(Y)*hs[:,0]*K.R*T/W))
def n(Y):return float(1000*np.sum(np.asarray(Y)[4:6]/W[4:6]))
def atoms(Y):return A@(1000*np.asarray(Y)/W)
rows=[]
for z in data['rows']:
 T=z['heater_K'];r=z['recycle_kg_per_kg_fresh'];Y=np.asarray(z['final_product_Y']);Q=z['heater_positive_J_kg_fresh'];Qminus=z['heater_removal_J_kg_fresh'];N=n(Y);N0=z['once_through_product_NOx_mol_kg'];pre=h(1700,fresh)-h(300,fresh)
 capacity=h(1700,Y)-h(300,Y)
 # Energy-state reconstruction from the saved heater and recycle scalar ledgers.
 # This is not independent recovery of the missing hot composition.
 hhot=h(1700,fresh)+Q-Qminus
 hot_sensible_drop=r*capacity
 delta_h_product=h(300,Y)-h(300,fresh)
 Qreject=Q-Qminus-delta_h_product
 net_no_difference=N-N0
 pumping={}
 for key,w in z['ideal_isothermal_recycle_pump_J_kg_fresh_by_pressure_ratio_increment'].items():
  pumping[key]={
   'ideal_pump_J_kg_fresh':w,
   'required_NOx_for_equal_SEC_mol_kg_fresh':N0*(1+w/Q),
   'required_gain_over_observed_recycle_mol_kg_fresh':N0*(1+w/Q)-N,
   'thermal_plus_pump_SEC_MJ_mol':(Q+w)/N/1e6,
   'penalty_percent_vs_once_through':100*((Q+w)/N/(Q/N0)-1),
  }
 # From the six species only: molecular weights are <= W(NO2), hence
 # Rmix >= R/W(NO2). At constant P and T(t)=1700-1e4 t, the cooler volume
 # per unit fresh massflow is integral (1+r)*Rmix*T/P dt.
 # This deliberately weak bound needs no unsaved composition trajectory.
 integral_T_dt=.14*(1700+300)/2
 cooler_V_lower=(1+r)*K.R/max(W)/101325*integral_T_dt
 # Stronger element-constrained bound: for every allowed molecule,
 # 1 >= (number of N atoms)/2 + (number of O atoms)/4.
 # Equality is attained by an N2/NO2 mixture at this N-rich atom ratio.
 min_moles_per_kg=float(np.array([.5,.25])@atoms(fresh))
 cooler_V_element_lower=(1+r)*(K.R/1000)*min_moles_per_kg/101325*integral_T_dt
 rows.append({
  'heater_K':T,'recycle_ratio':r,'total_downstream_kg_per_kg_fresh':1+r,
  'fresh_product_mass_Y_error':float(Y.sum()-1),
  'elemental_mol_atoms_kg_fresh_residual':(atoms(Y)-atoms(fresh)).tolist(),
  'NOx_recomputed_mol_kg':N,'NOx_recompute_residual':N-z['net_product_NOx_mol_per_kg_fresh'],
  'NOx_loss_vs_once_through_mol_kg':-net_no_difference,
  'NOx_loss_vs_once_through_percent':100*(1-N/N0),
  'observed_SEC_penalty_percent_vs_once_through_no_pump':100*(N0/N-1),
  'NOx_gain_required_to_beat_once_through_no_pump_mol_kg':N0-N,
  'product_heat_capacity_integral_300_1700_J_kg':capacity,
  'hot_to_1700_enthalpy_diverted_into_recycle_J_kg_fresh':hot_sensible_drop,
  'product_formation_plus_300K_sensible_enthalpy_increase_J_kg':delta_h_product,
  'rejected_heat_recomputed_by_external_endpoint_J_kg':Qreject,
  'rejected_heat_residual_vs_saved_J_kg':Qreject-z['uncredited_rejected_heat_J_kg_fresh'],
  'fresh_preheat_recomputed_J_kg':pre,
  'fresh_preheat_residual_vs_saved_J_kg':pre-z['ideal_feed_preheat_J_kg_fresh'],
  'implied_hot_stream_enthalpy_at_1700_J_kg':hhot-hot_sensible_drop,
  'once_through_total_recovery_margin_using_recycle_endpoint_as_proxy_J_kg':hhot-hot_sensible_drop-h(300,Y)-pre,
  'cooler_mass_holdup_per_fresh_kg_s':.14*(1+r),
  'once_through_cooler_mass_holdup_per_fresh_kg_s':.14,
  'cooler_volume_lower_bound_m3_per_fresh_kg_s':cooler_V_lower,
  'element_constrained_cooler_volume_lower_bound_m3_per_fresh_kg_s':cooler_V_element_lower,
  'element_constrained_min_total_moles_per_kg':min_moles_per_kg,
  'pumping_break_even':pumping,
 })
result={
 'scope':__doc__,
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'model_species_order':K.species_names,
 'fresh_Y':fresh.tolist(),
 'rows':rows,
 'limitations':[
  'No completed chemical loop or heater/cooler ODE was rerun.',
  'Hot composition and full cooler path are absent from result.json, so an independent continuum pinch/monotone heat-removal proof is not possible from this packet.',
  'The once-through recovery-margin calculation uses the recycled product endpoint as a clearly labelled proxy, not a certification of the comparator pinch.',
  'Pressure-ratio numbers are illustrative ideal pump costs, not qualified pressure losses or efficiencies.',
 ]}
output=Path(__file__).resolve().parent/'saved_checks.json'
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
