"""Native arithmetic/first-law checks, no reproduction of author process simulation."""
from pathlib import Path
from fractions import Fraction as F
import json,math,hashlib,time,resource
start=time.perf_counter();p=Path(__file__).parent;i=json.loads((p/'inputs.json').read_text())
src=p.parent/'capture_evidence/pilot.txt';assert hashlib.sha256(src.read_bytes()).hexdigest()==i['primary_text_sha256']
f=lambda n:F(i[n]); n=f('acid_100pct_kg')*1000/f('acid_molar_mass_g_mol');duration=f('operating_hours')*3600
Ea=f('absorbed_kW')*1000*duration;Eg=f('generator_input_kW')*1000*duration
Q=f('reported_heat_fraction')*f('absorbed_kW')*1000;T0=f('ambient_K_assumption');Tw=f('water_tank_K');cp=f('water_cp_J_kg_K_assumption');m=f('tank_water_kg_assumption')
Cw=cp*f('water_flow_kg_min_assumption')/60;Tout=Tw+Q/Cw
eta=1-T0/Tw;eta_hot=1-T0/Tout
Bstream=float(Cw)*float(Tout-Tw-T0*F(str(math.log(float(Tout/Tw)))))
stored=m*cp*(Tw-T0)
Pabs=f('ambient_Pa_assumption')+f('chamber_gauge_psi')*f('psi_Pa');V=math.pi*float(f('oxidizer_diameter_m')/2)**2*float(f('oxidizer_height_m'))
qstd=f('loop_flow_SLPM')/60000;qact=qstd*f('chamber_K_assumption')/f('SLPM_reference_K_assumption')*f('ambient_Pa_assumption')/Pabs
rate=n/duration;Nsl=rate*f('SL_molar_L_assumption')*60;air=f('air_makeup_SLPM');psa=f('PSA_makeup_SLPM');fresh=air+psa
# Restricted dry steady complete-acid closure, no NOx in purge, no inventory drift.
purge=fresh-F(7,4)*Nsl;O2out=air*f('air_O2_fraction_assumption')+psa*f('PSA_O2_fraction')-F(5,4)*Nsl
capture0=f('capture_original');capture1=f('capture_proposed');survival=[]
for s in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
 c=lambda e:e/(1-s*(1-e))
 ratio=c(capture0)/c(capture1)
 survival.append({'survival':float(s),'product_per_fresh_fixedN_original':float(c(capture0)),'product_per_fresh_fixedN_upgraded':float(c(capture1)),'SEC_upgraded_over_original':float(ratio),'nominal_5p3_scaled_MJ_mol':float(f('reported_plasma_SEC_MJ_mol')*ratio)})
assert survival[-1]['SEC_upgraded_over_original']==1
out={'scope':i['notes'],'batch':{'HNO3_equivalent_mol':float(n),'formation_rate_mol_s':float(rate),'absorbed_energy_MJ':float(Ea/10**6),'generator_input_energy_MJ':float(Eg/10**6),'absorbed_SEC_MJ_mol':float(Ea/n/10**6),'generator_only_SEC_MJ_mol':float(Eg/n/10**6),'rounded_5p3_generator_conversion_MJ_mol':float(f('reported_plasma_SEC_MJ_mol')*f('generator_input_kW')/f('absorbed_kW')),'gas_balance_equivalent_mol':float(Ea/10**6/f('reported_gas_balance_SEC_MJ_mol')),'implied_solution_density_kg_L':float(f('acid_100pct_kg')/f('acid_mass_fraction')/f('acid_solution_L'))},'heat_port':{'conditional_recovered_power_W':float(Q),'Carnot_at_60C':float(eta),'hottest_water_if_tank_is_return_K':float(Tout),'Carnot_at_conditional_hottest_water':float(eta_hot),'water_stream_incremental_exergy_upper_W':Bstream,'isothermal_60C_work_upper_W':float(Q*eta),'tank_sensible_storage_MJ_from_25C':float(stored/10**6),'time_to_fill_tank_storage_h_at30kW':float(stored/Q/3600),'conditional_batch_heat_MJ':float(Q*duration/10**6),'conditional_heat_beyond_tank_storage_MJ':float((Q*duration-stored)/10**6),'claim_scope':'Heat grade of demonstrated water port only; not upstream hot gas or avoided heater input. Duty not proved batch-integrated.'},'residence_interpretation':{'geometry_volume_m3':V,'pressure_absolute_Pa':float(Pabs),'standard_flow_m3_s':float(qstd),'conditional_in_vessel_flow_m3_s':float(qact),'volume_over_standard_flow_s':V/float(qstd),'conditional_corrected_residence_s':V/float(qact),'scope':'Requires stated loop SLPM actually crossing vessel, reference and T assumptions; not measured residence time.'},'dry_nominal_makeup_consistency':{'captured_N_standard_L_min_equivalent':float(Nsl),'purge_standard_L_min_required':float(purge),'O2_purge_fraction_implied':float(O2out/purge),'scope':'Conditional nominal descriptor consistency test; not actual purge measurement. Unpaired approximate flows, NOx/water purge and changing inventory prevent complete balance.'},'closed_loop_survival':survival,'elapsed_s':time.perf_counter()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(p/'result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
