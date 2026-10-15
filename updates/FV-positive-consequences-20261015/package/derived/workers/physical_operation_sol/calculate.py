"""Transparent arithmetic on acquired source values, with source locators and boundaries."""
from pathlib import Path
import hashlib, json, math, statistics

B=Path(__file__).resolve().parent
f4=json.loads((B/'sources/heat_fig4.cells.json').read_text())
f5=json.loads((B/'sources/heat_fig5.cells.json').read_text())
drive=json.loads((B/'sources/drive_data.cells.json').read_text())
result={'status':'NO_NEW_PHYSICAL_OPERATION_ACQUIRED','actual_experiments_performed_here':False}
result['film_source_data_checks']={
 'source':'heat_fig4.xlsx Fig4d A3:E5; heat_fig5.xlsx Fig5d C2:D10',
 'joule_cooling_unit_COP_counter_heating':f4['Fig4d']['D5'],
 'joule_thermal_actuator_efficiency':f4['Fig4d']['D4'],
 'joule_full_thermal_COP':f4['Fig4d']['D3'],
 'factorized_COP':f4['Fig4d']['D5']*f4['Fig4d']['D4'],
 'external_source_temperature_C_mean':statistics.mean(f5['Fig5d'][f'D{i}'] for i in range(2,5)),
 'external_free_span_K_mean':statistics.mean(f5['Fig5d'][f'D{i}'] for i in range(5,8)),
 'external_SCP_W_per_g_mean':statistics.mean(f5['Fig5d'][f'D{i}'] for i in range(8,11)),
 'warning':'Specific power is per 0.630 mg active refrigerant, not total apparatus; free-span and zero-lift cooling are different operating points.'}

film=[]
for name,q0,qf,delta,cop0,cop_narrow in [
 ('Joule-heated',2.79e-3,1.25e-3,1.0,6.69e-4,2.18e-2),
 ('External-source',2.09e-3,1.27e-3,0.5,3.17e-4,5.60e-3)]:
    p=q0/cop0; p_narrow=q0/cop_narrow
    film.append({'configuration':name,'source':'heat_si.pdf PDF pp.30-32, SI Tables 3-4; Note 2 PDF pp.4-6',
       'Qc_zero_lift_W':q0,'Qc_finite_cold_drop_W':qf,'finite_cold_drop_K':delta,
       'COP_zero_lift_with_auxiliary_actuators':cop0,
       'derived_accounted_input_W':p,
       'derived_heater_input_W':p_narrow,
       'derived_auxiliary_actuator_input_W':p-p_narrow,
       'derived_auxiliary_fraction':1-p_narrow/p,
       'estimated_finite_lift_COP_if_same_drive_power':qf/p,
       'boundary_warning':'Source auxiliary integral covers loading/unloading intervals only; values are not independently metered complete wall-plug performance. Finite-lift COP is an explicitly constant-input estimate, not a reported COP.'})
result['film_accounted_power']=film

d=drive['Figure 6']; rows=[]
for i in range(3,12):
    if 'P'+str(i) not in d: continue
    load=d['Q'+str(i)]; unload=d['S'+str(i)]; win=d['W'+str(i)]
    eta=(load-win)/unload
    rows.append({'source_range':f'Figure 6!P{i}:AD{i}','frequency_Hz':d['P'+str(i)],
       'load_J':load,'unload_J':unload,'shaft_input_J':win,
       'recomputed_recovery_percent':100*eta,'source_recovery_percent':d['AC'+str(i)]})
result['four_disc_spring_recovery']=rows
result['drive_warning']='These are disc-spring tests, not coupled refrigeration tests; no thermal COP is inferred.'

result['cycle_duration_arithmetic']={
 'source':'kw_si.pdf PDF p.17, 950 MPa, 3.5 Hz cycle tests',
 'five_hundred_thousand_cycles_hours':500000/3.5/3600,
 'two_million_cycles_days':2000000/3.5/86400,
 'warning':'Functional fatigue was observed; duration conversion does not establish lifetime.'}
Tc,T0,Ts=295.1,295.6,403.2
result['three_reservoir_bound']={
 'assumptions':'Restored periodic state; heat from source Ts>T0; cold load Tc<T0; other work/consumables separately charged',
 'Tc_K':Tc,'T0_K':T0,'Ts_K':Ts,
 'ideal_heat_driven_COP_upper_bound':Tc/(T0-Tc)*(1-T0/Ts),
 'identity':'Qc*(T0/Tc-1) <= Qs*(1-T0/Ts) + W_electric + exergy_other',
 'negative':'With no above-ambient heat source, no work/consumable input and restored state, positive below-ambient cooling is impossible.'}
result['salt_finite_rate_falsifier']={
 'assumptions':'Isothermal restricted model, approximately constant partial dissolution enthalpy, full work/other-state corrections retained separately',
 'identity':'Qc = Delta_h_diss*n_retained - W_contact - E_other_cold',
 'necessary':'n_retained/n_gross > (sigma*v_s + E_other_cold/n_gross)/Delta_h_diss',
 'also_required':'c_exported > c_eq(T_h,sigma_low) for warm regrowth in the specified cycle',
 'numbers_assigned':False,
 'unacquired':'Same-NH4SCN loaded-contact dissolution, precipitation survival, warm regeneration, damage and work responses.'}

assert abs(result['film_source_data_checks']['factorized_COP']-f4['Fig4d']['D3'])<0.0001
assert all(abs(x['recomputed_recovery_percent']-x['source_recovery_percent'])<0.15 for x in rows)
assert film[0]['derived_auxiliary_fraction']>0.9 and film[1]['derived_auxiliary_fraction']>0.9
(B/'calculation_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'film_accounted_power':film,'recovery_verified_rows':len(rows)},indent=2))
