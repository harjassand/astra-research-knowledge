from pathlib import Path
import json
H=Path(__file__).parent;Q=H.parent
j=json.loads((H/'oracle_and_endpoint_fit_v1.json').read_text());out=[]
for r in j['endpoint_fit_pilots']:
 label=r['source_label']
 if label=='original_ideal_idle':tau=None
 else:tau=json.loads((Q/'clocked_flagged_storage_20261028'/f'{label}.json').read_text())['timing']['total_EC_time']+2
 out.append({'source_label':label,'T':r['T'],'additional_endpoint_native_exposures':r['actual_total_native_exposures'],'prior_selected_inverse_minimum_fit_exposures':20480,'prior_actual_full_pilot_calibration_exposures':102400,'prior_actual_full_pilot_total_exposures':2068480,'standalone_equal_total_acquisition_budget':False,'aggregate_extra_channel_time_reference_units':None if tau is None else tau*r['actual_total_native_exposures'],'ideal_five_site_parallel_extra_time_reference_units':None if tau is None else tau*r['actual_total_native_exposures']/5,'prep_readout_and_final_pulse_time':'additional uncharged interface','original_ideal_idle_clock':'not specified' if tau is None else 'declared clocked model'})
(H/'endpoint_clock_costs_v1.json').write_text(json.dumps(out,indent=2)+'\n')
