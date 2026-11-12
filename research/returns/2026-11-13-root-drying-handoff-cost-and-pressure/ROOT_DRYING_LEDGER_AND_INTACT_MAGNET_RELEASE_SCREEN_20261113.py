#!/usr/bin/env python3
"""ROOT analytic screens. Introduced parameters; no producer code or device test."""
import json, math
from pathlib import Path
R=8.314462618; mu0=4*math.pi*1e-7
def crf(r,n): return r/(1-(1+r)**(-n))
out={}
# Displayed drying ledger: do not merge industrial-handoff and laboratory preparation.
inc=30.02; target=.60*inc
out["drying_fixed_ledger"]={
 "matched_incumbent_USD_t_water":inc,"forty_percent_advantage_ceiling":target,
 "reference":48.07,"reference_process_kWh_kg":.1288,
 "optimistic_process_kWh_kg":.0778,"lab_slurry_preparation_kWh_kg":.01045,
 "optimistic_with_lab_preparation":.0778+.01045,
 "FREE_capital_finite_replacements_and_electricity_only":48.07-19.39-5.15,
 "remaining_fraction_reduction_needed":1-target/(48.07-19.39-5.15),
 "optimistic_capital_multiple_of_1M":3.260,
 "reference_cost_ratio_to_incumbent":48.07/inc,
 "hypothetical_finish_saving_USD_t_water":(2-.3)*.04*7000/(3000-128.181-.128),
 "warning":"Displayed rounded blocks, fixed other lines; not a lower bound for every dryer. Common industrial feed manufacture is outside the service-handoff target."
}
L=.004; phi=.40; mu=.15e-3; beta=2e-9; k=2.23e-16
out["cake_pressure_relaxation"]={"introduced_L_m":L,"phi":phi,"mu_Pa_s":mu,"beta_Pa_inv":beta,"k_m2":k,
 "tau_s":L*L*phi*mu*beta/k,
 "liquid_elastic_J_per_packet_at_0p7MPa":.5*beta*.073*(.7e6)**2,
 "ideal_DME_isothermal_expansion_kJ_kg_10_to_1bar":R/.04607*308.15*math.log(10)/1000,
 "warning":"Homogeneous linear liquid estimate, not two-phase nucleation, measured front propagation or reversible useful expansion."}
# A brittle component attached over its face. Geometry and every property are introduced.
a=.05; b=.025; t=.005; area=a*b; rho=7500; mass=area*t*rho
B=.6; traction=10e6; G=1000; gap=.005
Fmag=B*B*area/(2*mu0); Fface=traction*area
sigma=3*Fface*a/(2*b*t*t)
out["magnet_release_introduced_example"]={
 "length_width_thickness_m":[a,b,t],"mass_kg":mass,"bond_area_m2":area,
 "B_T":B,"adhesive_uniform_traction_Pa":traction,
 "field_attraction_uniform_gap_force_N":Fmag,
 "uniform_adhesive_force_N":Fface,
 "three_point_bending_stress_Pa_if_face_force_is_transmitted_as_central_load":sigma,
 "interface_fracture_energy_J_at_G1000":G*area,
 "magnets_per_accepted_kg_at_90pct_mass_yield":1/(mass*.9),
 "uniform_field_force_times_5mm_J":Fmag*gap,
 "warning":"Uniform gap-field and simple beam diagnostics are incompatible surrogate boundary conditions, not an actual bonded-rotor stress solution or proof of a reusable magnet."}
out["thermal_and_remagnetization_introduced"]={
 "magnet_cp_J_kgK":450,"magnet_delta_T_K":125,
 "magnet_sensible_J":mass*450*125,
 "thermal_diffusivity_m2_s":3e-6,
 "through_5mm_diffusion_time_s":t*t/3e-6,
 "through_0p2mm_adhesive_diffusion_time_s_at_alpha1e_7":(.0002)**2/1e-7,
 "ideal_4T_1L_field_store_J":4**2*.001/(2*mu0),
 "warning":"Field store is not purchased magnetizer energy. A 150C catalog use temperature is not a safe demagnetizing heat-treatment guarantee. No measured adhesive thermal kinetics, rotor temperature map or damage threshold supplied."}
# Recovery service, all external inputs and incoming assemblies paid separately as well.
annual_gross=100*250*.9
rows=[]
for yield_ in [.60,.80,.90,.95]:
 annual=annual_gross*yield_
 for workers in [1,2]:
  cap=250000*crf(.08,20)/annual
  labor=workers*40*8*250/annual
  elec=5*.08
  service=cap+labor+elec
  rows.append({"yield_of_all_contained_magnet":yield_,"workers":workers,
    "accepted_kg_year":annual,"capital_USD_kg":cap,"labor_USD_kg":labor,
    "electricity_USD_kg":elec,"remaining_to_10_USD_kg":10-service,
    "warning":"All cleaning, replacement, qualification, waste, rent, overhead, finance, downtime and feed logistics remain to be paid; no supplier quote."})
out["service_cost_introduced"]=rows
# Incoming magnet value cannot be treated as a free rescued product.
feed_rows=[]
for input_cost_per_contained_kg in [0,5,15,30]:
 for y in [.6,.9,.95]:
  feed_rows.append({"incoming_full_assembly_cost_allocated_USD_per_contained_magnet_kg":input_cost_per_contained_kg,
    "accepted_yield":y,"input_cost_USD_per_accepted_kg":input_cost_per_contained_kg/y})
out["incoming_stock_cost"]=feed_rows
# Include entire rotor with a low magnet mass fraction in any claimed thermal energy.
out["bulk_heating_introduced"]=[]
for f in [.05,.10,.25]:
 # 0.5 kJ/kgK full assembly heat capacity, 125 K rise, 50% wall->stock efficiency.
 out["bulk_heating_introduced"].append({"magnet_mass_fraction":f,
 "gross_stock_sensible_kWh_per_contained_magnet_kg":.5*125/(3600*f),
 "purchased_heat_kWh_per_accepted_kg_at_90pct_yield_50pct_heater_efficiency":.5*125/(3600*f*.9*.5)})
# An explicit piece-count and handling contract; handling need not track low fracture work.
out["handling_introduced"]=[]
for sec in [3,15,60]:
 out["handling_introduced"].append({"seconds_per_piece":sec,
 "seconds_per_accepted_kg_at_90pct_yield":sec/(mass*.9),
 "labor_USD_per_accepted_kg_at_40_USDh":sec/(mass*.9)/3600*40})
assert abs(out["drying_fixed_ledger"]["FREE_capital_finite_replacements_and_electricity_only"]-23.53)<1e-10
assert out["magnet_release_introduced_example"]["uniform_adhesive_force_N"]>out["magnet_release_introduced_example"]["field_attraction_uniform_gap_force_N"]
assert all(math.isfinite(v) for v in [sigma,Fmag,Fface,mass])
out["status"]="INTRODUCED_CONDITIONAL_DIAGNOSTICS_NOT_PHYSICAL_QUALIFICATION"
Path(__file__).with_suffix(".json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
