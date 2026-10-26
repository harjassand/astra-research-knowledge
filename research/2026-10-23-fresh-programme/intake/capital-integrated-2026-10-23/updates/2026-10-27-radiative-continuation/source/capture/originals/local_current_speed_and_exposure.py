#!/usr/bin/env python3
"""Exact universal one-port current inequality and numerical sharpness audit.
Hamiltonian h(t) = [[epsilon, v(t)^*],[v(t),h_out(t)]], ||v||<=G.
P=|a|^2. Then |Pdot| <= 2G sqrt(P(1-P)); set theta=arcsin sqrt(P),
|theta'|<=G. A full 0->1 transfer needs T>=pi/(2G) and
integral P >= pi/(4G), sharp for a two-site resonant transfer.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.integrate import quad
from scipy.optimize import brentq
OUT=Path(__file__).resolve().parent
G=.7;N=120;e,V=eigh_tridiagonal(np.ones(N),np.r_[G,.5*np.ones(N-2)])
w=V[0]**2
survival=lambda t:float(np.dot(w,np.cos((e-1)*t)))
T=brentq(survival,2.43388605,2.433886053)
I=quad(lambda t:survival(t)**2,0,T,epsabs=1e-13)[0]
Tmin=math.pi/(2*G); Imin=math.pi/(4*G)
# The positive Jacobi example nearly saturates the bound.
assert T>Tmin and I>Imin
# Exactly sharp counterexample in isolated two-level system: P=sin(G*t)^2.
Tsharp=math.pi/(2*G)
Isharp=quad(lambda t:math.sin(G*t)**2,0,Tsharp,epsabs=1e-14)[0]
assert abs(Isharp-Imin)<1e-13
# A rank-one edge current bound extends to arbitrary many output modes: ||v||<=G.
# Verify derivative inequality for a sample random 8-mode physical matrix and
# multiple externally supported initial wavefunctions (diagnostic only).
rng=np.random.default_rng(7304)
max_violation=0.
for trial in range(15):
  mat=rng.normal(size=(7,7)); h_out=(mat+mat.T)/2
  h_out+=np.eye(7)*(7+abs(np.linalg.eigvalsh(h_out).min()))
  v=rng.normal(size=7);v*=G/np.linalg.norm(v)
  h=np.zeros((8,8));h[0,0]=1;h[0,1:]=v;h[1:,0]=v;h[1:,1:]=h_out
  ev,U=np.linalg.eigh(h)
  f=rng.normal(size=8)+1j*rng.normal(size=8);f[0]=0;f/=np.linalg.norm(f)
  q=U.conj().T@f
  for t in np.linspace(0,8,101):
     state=U@(np.exp(-1j*ev*t)*q)
     p=float(abs(state[0])**2)
     pdot=float(2*np.imag(np.conj(state[0])*np.dot(v,state[1:])))
     viol=max(0,abs(pdot)-2*G*math.sqrt(max(0,p*(1-p))))
     max_violation=max(max_violation,viol)
assert max_violation<1e-12
Ud=1.;J=10.
I_direct=2*I+math.pi/Ud
I_direct_lower=math.pi/(2*G)+math.pi/Ud
I_dark_e=2*I+math.pi/(2*J)
I_dark_e_lower=math.pi/(2*G)+math.pi/(2*J)
out={'theorem':'For any one-photon one-port block Hamiltonian with ||v(t)||<=G, arcin sqrt p is G-Lipschitz; 0-to-1 transfer time>=pi/(2G) and emitter occupation integral >=pi/(4G)',
     'g_bound':G,'Jacobi_root_capture_duration':T,'universal_time_lower_bound':Tmin,'time_ratio':T/Tmin,
     'Jacobi_capture_port_occupation_integral':I,'universal_occupation_lower_bound':Imin,'occupation_ratio':I/Imin,
     'sharp_two_site_transfer_duration':Tsharp,'sharp_two_site_occupation_integral':Isharp,
     'random_multichannel_derivative_check_max_violation':max_violation,
     'direct_stage_exposure_lower_bound':I_direct_lower,'direct_stage_exposure_achieved':I_direct,
     'direct_stage_ratio_to_lower_bound':I_direct/I_direct_lower,
     'dark_storage_emitter_exposure_lower_bound_in_staged_model':I_dark_e_lower,
     'dark_storage_emitter_exposure_achieved':I_dark_e,
     'dark_storage_ratio_to_lower_bound':I_dark_e/I_dark_e_lower,
     'necessary_small_loss_markov_kappa_over_B_for_1pct_direct_upper_approx':.01**2/I_direct_lower,
     'needed_model_scope':['Single photon initially outside monitored site, finally completely on monitored site',
           'All transfer into the site flows through the bounded coupling vector v, with no direct source operation acting on that site',
           'Bounded operator norm ||v(t)||<=G; arbitrary time-dependent bath self-Hamiltonian and onsite emitter energy allowed',
           'Loss-exposure fidelity bounds are asymptotic small kappa; exact full environmental audit stored separately',
           'For an emitter-to-dark store complete staged resonant swap, its local coupling has norm <=J and each swap also saturates its own π/(4J) exposure bound']}
(OUT/'local_current_speed_exposure_results.json').write_text(json.dumps(out,indent=2))
for k in ('time_ratio','occupation_ratio','direct_stage_ratio_to_lower_bound','dark_storage_ratio_to_lower_bound'):
 print(k,out[k])
print('max random numerical current violation',max_violation)
