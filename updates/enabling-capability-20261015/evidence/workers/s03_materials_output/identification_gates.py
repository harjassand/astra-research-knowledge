"""Exact logical/calibration gates using measured values as fixed observations.

The alternate models below are countermodels, not fabricated experimental output
or a successful physical simulation. They show what cannot be identified without
an additional measurement or assumption.
"""
from pathlib import Path
import json
import numpy as np
from scipy.io import loadmat

BASE=Path(__file__).resolve().parent
d=loadmat(BASE/'data/FeCoNi_benchmark_dataset_220501a.mat')
hc=d['Coer'].ravel();theta=d['Kerr'].ravel()
ir_h=np.argsort(hc)[::-1];ir_k=np.argsort(theta)[::-1]
top,second=ir_k[:2]

# theta_i = k_i * m_i. m here is an uncalibrated magnetic quantity. A global
# reference can remove an instrument factor, but not material-dependent k_i.
gain_a=np.ones(len(theta));gain_b=gain_a.copy();gain_b[top]=1.1
magnetic_a=theta/gain_a;magnetic_b=theta/gain_b
assert np.array_equal(magnetic_a*gain_a,theta)
assert np.allclose(magnetic_b*gain_b,theta,rtol=0,atol=1e-16)
assert np.argmax(magnetic_a)!=np.argmax(magnetic_b)

epsilon=.001
max_h=float(hc.max())
ranking_radius=float((hc[ir_h[0]]-hc[ir_h[1]])/2)
# If every source value is within delta of truth, selecting the observed maximum
# gives (max_source-delta)/(max_source+delta) as the worst relative guarantee.
relative_certificate_radius=epsilon*max_h/(2-epsilon)

out={
 'scope':'logical_nonidentifiability_and_calibration_countermodels_not_new_physical_measurements',
 'coercivity_observed_max_mT':max_h,
 'coercivity_top_two_rows_1based':(ir_h[:2]+1).tolist(),
 'coercivity_top_two_gap_mT':float(hc[ir_h[0]]-hc[ir_h[1]]),
 'per_specimen_symmetric_error_radius_to_tie_top_two_mT':ranking_radius,
 'required_uniform_absolute_error_bound_for_99_9percent_relative_certificate_mT':relative_certificate_radius,
 'calibration_error_bound_acquired':None,
 'qualification':'A common positive affine calibration preserves ranking. The gap bound concerns specimen-specific error; no such error magnitude is asserted.',
 'kerr_gain_countermodel':{
  'equation':'theta_i = k_i * m_i; instrument common gain could be factored into k_i',
  'observed_top_two_rows_1based':[int(top)+1,int(second)+1],
  'observed_rotations_mrad':[float(theta[top]),float(theta[second])],
  'minimum_relative_gain_ratio_that_can_invert_top_two':float(theta[top]/theta[second]),
  'constructed_gain_change_for_top_row':1.1,
  'model_A_target_max_row_1based':int(np.argmax(magnetic_a))+1,
  'model_B_target_max_row_1based':int(np.argmax(magnetic_b))+1,
  'same_all_observed_kerr_values':True,
  'same_composition_and_XRD_inputs':True,
  'interpretation':'Unknown material-dependent optical coefficient prevents treating maximum Kerr as maximum saturation magnetization. Models are algebraic witnesses; physical realizability of particular gains has not been measured.',
  'resolving_interface':'Specimen-specific magneto-optical coefficient or independent calibrated VSM/SQUID magnetometry at the chosen geometry and temperature.'},
 'preparation_transfer_countermodel':{
  'available_preparation_support':'single prepared source library; no treatment index or repeated preparation is in acquired data',
  'model_A':'F_A(c,z,p)=F_0(c,z)',
  'model_B':'F_B(c,z,p)=F_0(c,z)+p*psi(c,z)',
  'observed_preparation':'p=0',
  'same_all_source_observations':True,
  'unobserved_preparation_difference':'At p=1, arbitrary nonzero psi can change the optimum while preserving every observed value at p=0.',
  'smoothness':'For finitely many distinct compositions, disjoint smooth bump functions can specify arbitrary finite psi values. Smoothness alone does not resolve the ambiguity.',
  'qualification':'This is an unrestricted-model identifiability statement, not proof that every psi is physically realizable. A physical structural sufficiency law could exclude it, but such a law is not independently validated by these data.',
  'resolving_interface':'Repeated matched compositions under independently varied preparation, co-registered XRD and raw magnetic loops, with blinded refabrication and an equally informed baseline.'}
}
(BASE/'IDENTIFICATION_GATES.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
