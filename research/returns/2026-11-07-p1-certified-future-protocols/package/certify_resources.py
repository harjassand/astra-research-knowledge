from pathlib import Path
from fractions import Fraction as Q
import json
from exact import encode,require

P=Path(__file__).resolve().parent/'results'
read=lambda n:json.loads((P/n).read_text())
e=read('EXECUTION.json');a=read('ACQUISITION.json')['certificate'];v=read('VERIFICATION.json')
c=Q(e['certified_true_target_signed_output_at_every_acknowledgement'])
M=Q(a['uniform_output_derivative_bound']);decay=Q(a['a']);h=Q(2);D=e['deadline_ticks']
Rstart=Q(a['initial_error'])+Q(a['deployment_actuation_error'])
require(c/M<h)
per_event=decay*c**3/(3*M)
lower=e['completed_requests']*per_event-Rstart**2/2
require(lower>0)
current_native=read('NATIVE_TOTAL_COST.json')
old=[read(n) for n in ['DEVELOPMENT_ZERO_LEAD_RUN.json','DEVELOPMENT_PHASE_RUN.json','DEVELOPMENT_ADC_RUN.json']]
all_native=[z['NATIVE_TOTAL_COST.json'] for z in old]+[current_native]
totals={k:sum(int(z[k]) for z in all_native) for k in ['advance_calls','state_coordinate_updates','scalar_reads','exponential_enclosures','state_integer_multiplications']}
out={
 'status':'PASS','event_magnitude_c':c,'event_integration_duration':c/M,
 'post_relaxation_source_norm_upper':Rstart,'net_source_work_per_event_lower_before_initial_energy':per_event,
 'executed_prefix_net_source_work_lower':lower,
 'executed_deployment_absolute_source_work_upper':Q(e['source_absolute_supply_bound']),
 'liminf_net_source_power_lower_for_infinite_backlog':per_event/(D*h),
 'deployment_command_squared_effort':Q(v['deployment_command_squared_effort']),
 'acquisition_command_squared_effort':Q(6),
 'deployment_force_cap':Q(2),'deployment_force_slew_cap':Q(32),
 'source_time_all_acquisition_and_deployment':Q(current_native['time']),
 'development_native_executions':len(all_native),
 'development_totals_including_final_execution':totals,
 'development_scope':'four native software runs; previous three explicitly retained as development records, no physical experiments',
 'work_units':'declared power-conjugate port units; no watts/joules conversion supplied',
 'additional_hardware_cost':'integrate the supplied driver envelope and add actual reader/clock/computation/communication/preparation energies',
 'extra_scalar_rational_operations_upper':100,
 'extra_rational_bit_length_upper':1024,
 'extra_source_queries':0,
 'scope':'mathematical source-work and digital-work certificate, not a hardware efficiency measurement'
}
(P/'RESOURCE_CERTIFICATE.json').write_text(json.dumps(encode(out),indent=2,sort_keys=True)+'\n')
print(json.dumps({k:float(x) if isinstance(x,Q) else x for k,x in out.items() if k in ['executed_prefix_net_source_work_lower','liminf_net_source_power_lower_for_infinite_backlog','post_relaxation_source_norm_upper','development_native_executions','development_totals_including_final_execution']},indent=2))
