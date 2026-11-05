#!/usr/bin/env python3
"""Join exact digital receipt, finite release, finite ADC, and drive tolerance."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
physical=json.loads((P/'physical_bridge_results.json').read_text())
compiler=json.loads((P.parent/'independent'/'passive_compiler_results.json').read_text())
adc=json.loads((P/'finite_digitization_results.json').read_text())
raw=(P/'physical_bridge_results.json').read_bytes()
assert compiler['source_sha256']==hashlib.sha256(raw).hexdigest()
j=compiler['physical_join']
mu=Q(j['mu_exact']);B=Q(str(physical['declared_B']))
xi=Q(1,100000);tau=Q(str(physical['finite_control']['finite_release_time']))
delta=Q(j['physical_initial_coordinate_error_exact'])+xi*tau
gamma=Q(j['initial_force_error_with_encoding_exact'])+B*xi*tau
residual=Q(j['numerical_residual_exact'])
speed=Q(j['actual_numerical_path_speed_exact'])
kernel=Q(j['kernel_L1_exact'])
bound=max(delta,(kernel*speed+gamma+residual+xi)/mu)
G=Q(str(physical['hidden_force_envelope']))
F=Q(str(physical['deployment']['force_amplitude_bound']))+xi
k=Q(str(physical['finite_control']['stiffness']))
vp=lambda z:z+Q(3,20)*z**3
Wrel=F+vp(delta)+G+2*B*delta+k*delta
Gafter=G+B*delta
Xdep=max(delta,(Gafter+F)/mu)
Wdep=F+vp(Xdep)+Gafter+2*B*Xdep
reaction=F+max(Wrel,Wdep)
travel=F*(1+tau)
release_work=k*delta**2/2
out={
 'status':'complete conditional finite-operation certificate',
 'physical_source_receipt_sha256':compiler['source_sha256'],
 'emitted_path_sha256':compiler['output_sha256'],
 'drive_delivery_error_allowance_exact':str(xi),
 'release_time_exact':str(tau),
 'post_release_initial_coordinate_bound_exact':str(delta),
 'old_force_error_including_encoding_and_release_drive_error_exact':str(gamma),
 'kernel_L1_bound_exact':str(kernel),'decoded_speed_exact':str(speed),
 'decoded_residual_exact':str(residual),'mu_exact':str(mu),
 'final_uniform_trajectory_bound_exact':str(bound),
 'final_uniform_trajectory_bound':float(bound),
 'joint_valid_event_probability_at_least':adc['joint_valid_output_probability_lower_bound'],
 'confidence_scope':'Conditional on the declared passive physical class, mass/energy/convexity bounds, calibrated control and metrology inequalities, and reliable finite classical arithmetic.',
 'physical_resources':{
   'switchable_stiffness_required_for_free_deployment':True,
   'moving_viscous_support_required_for_additive_drive':True,
   'support_speed_cap_including_error':float(Q(str(physical['deployment']['force_amplitude_bound']))+xi),
   'support_travel_cap_including_error':float((Q(str(physical['deployment']['force_amplitude_bound']))+xi)*(1+tau)),
   'finite_release_stiffness_slew_bound':physical['finite_control']['release_stiffness_slew_bound'],
   'release_position_speed_bound':float(Wrel),
   'deployment_position_speed_bound':float(Wdep),
   'local_support_reaction_force_bound':float(reaction),
   'absolute_support_work_bound':float(reaction*travel),
   'absolute_stiffness_release_work_bound':float(release_work),
   'stiffness_release_peak_parameter_power_bound':float(Q(15,8)*release_work/tau),
   'calibration_contract':'Drive error includes residual released-trap force, support-motion error, and any drag-calibration contribution during deployment. Acquisition calibration errors must separately meet the recorded deterministic report and initialization allowances.',
   'frontend_force_range_contract':'The force transducer must remain linear over the declared global force cap or have a certified clearing response; the finite ADC receipt prices the metered hold windows.'},
 'execution_scope':{
  'physical_plant':'floating simulation, not laboratory or interval-validated ODE',
  'raw_sensor_record':'finite counts and digitization costs charged; fine bins aggregated, not individually materialized',
  'learned_model':'finite rational positive model independently verified',
  'digital_predictor':'actual rational path independently verified from saved knots',
  'drive_error':'robust allowance, not a sampled perturbed drive'},
 'preservation':'No earlier accepted result is weakened or generalized by this construction.'
}
(P/'complete_operation_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'complete_bound':float(bound),'joint_event':adc['joint_valid_output_probability_lower_bound'],
                  'source_hash':compiler['source_sha256'],'path_hash':compiler['output_sha256']},indent=2))
