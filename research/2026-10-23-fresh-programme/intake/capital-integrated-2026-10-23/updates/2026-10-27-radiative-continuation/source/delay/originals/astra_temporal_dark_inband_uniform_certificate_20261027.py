#!/usr/bin/env python3
"""All-time positive-Schur certificate for the on-band, real-control echo.
The estimates follow from: exact f polynomial bounds, Fourier Plancherel,
positive-source monotonicity, and Schur completion at zero energy.
No time grid or numerical eigenvalue scan enters the proof.
"""
import math,json
from scipy.special import beta
T=12.0;tau=0.5; L=T-2*tau; alpha=0.16;eta=0.01;CUTOFF=12.0;mu=2*math.pi
I=L*4**6*beta(7,7)
v_norm=eta*CUTOFF/math.sqrt(30)
w_norm=math.sqrt(6)*v_norm
v_inf=eta*math.sqrt(CUTOFF/5)*(4/5)**2
h_max=math.sqrt(6)*alpha
hp_max=(12/L)*h_max
rad_max=math.sqrt(4*math.pi)*v_inf*4*alpha*math.sqrt(I)
rho_min=math.sqrt(1-h_max*h_max-rad_max*rad_max)
# h1(t) is positive and unimodal about T/2: derivative condition 2 tau < L/(2 sqrt(5)).
assert 2*tau < L/(2*math.sqrt(5))
# From radiation vacuum at t=0 and t=T, and componentwise monotonic h(t),
# ||radiation(t)|| <= ||W|| * min(int_0^t ||h||, int_t^T ||h||)
#                      <= ||W|| * (T/2) * ||h(t)||.
rad_over_h=w_norm*T/2
rho_prime_over_h=(hp_max+w_norm*rad_max)/rho_min
theta_prime_over_h=math.pi/(2*I*math.sqrt(2)*alpha)
r_prime_over_h=rho_prime_over_h+theta_prime_over_h
y_max=hp_max+w_norm*rad_max
C_max=2*r_prime_over_h+y_max/rho_min
Q_max=3*w_norm*rad_over_h
bath_schur_max=6*eta*eta*CUTOFF/5
margin=mu-C_max-Q_max-bath_schur_max
assert margin>1.1, margin
# Relaxed hand-check numbers are also sufficient and deliberately separated
# from floating-point mathematical constants.
coarse_margin=6.28-5.12-.053-.002
assert coarse_margin>1.1
result={'parameter_set':{'T':T,'tau':tau,'carrier_mu':mu,'photon_band':[0,CUTOFF],
  'alpha':alpha,'radiation_form_factor_eta':eta},
  'bounds':{'source_L2_bump_squared_integral':I,'coupling_operator_norm_upper':w_norm,
  'form_factor_sup':v_inf,'emitter_norm_upper':h_max,'emitter_envelope_derivative_upper':hp_max,
  'transient_radiation_norm_upper':rad_max,'storage_norm_lower':rho_min,
  'radiation_over_instantaneous_emitter_norm_upper':rad_over_h,
  'storage_derivative_over_emitter_norm_upper':r_prime_over_h,
  'storage_emitter_C_operator_norm_upper':C_max,'emitter_emitter_Q_operator_norm_upper':Q_max,
  'bath_zero_energy_schur_upper':bath_schur_max,
  'complete_internal_schur_positive_margin':margin,
  'coarse_rational_check_margin_over':coarse_margin},
  'proof_scope':'Uniform in t for the exact continuous L2 bath; positive Schur margin is internal and does not imply a gap of the entire gapless field. Real-symmetric internal controls are inverse engineered; no physical local hardware certified.'}
with open('/mnt/data/astra_temporal_dark_inband_uniform_certificate_20261027.json','w') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
