#!/usr/bin/env python3
"""Four-port inclusive scattering with two ordinary reciprocal waveguide directions
and TWO independent radiation-loss continua. Equal spectral weights kappa*x^2.
The real Kramers-Kronig correction is INCLUDED and center retuned.
Off-center rows are grid diagnostics, not interval-certified loss tolerances.
The center lower bound is analytic and optimal for a tuned parity resonance.
"""
import numpy as np, json, sys
from numpy.linalg import norm
from math import sqrt,pi,cos,log
from astra_reciprocal_parity_design_probe_20261026 import params
from astra_reciprocal_full_scattering_search_20261026 import Bp

tau=1.1;gamma=1.;E0=1.5;chi=1800.0
P=params(str(tau),str(gamma))
cs=np.array([[1,1],[1,-1]],float)/sqrt(2)
B0=lambda e:2+2*e+e*e*log((2-e)/e)
def S4(e,kappa,shift=0.):
    # Two emitter parities and two positive harmonic side modes.
    # Retune the bare epsilon_p by +kappa*A(E0), accounting for radiation PV at E0.
    bare=np.diag([p['bare']+kappa*B0(E0) for p in P])
    M=cs@bare@cs.T
    N=cs@np.diag([sqrt(p['r']) for p in P]); Om=np.diag([p['Omega'] for p in P])
    H=np.block([[M,N],[N.T,Om]])
    VP=sqrt(gamma)*e/sqrt(2)*np.array([[1,1],[np.exp(1j*tau*e),np.exp(-1j*tau*e)]])
    VL=sqrt(kappa)*e*np.eye(2)
    W2=np.column_stack((VP,VL))
    W=np.zeros((4,4),complex);W[:2,:]=W2
    D=e*np.eye(4,dtype=complex)-H
    D[:2,:2]+=cs@np.diag([Bp(e,tau,p['p']) for p in P])@cs.T
    D[:2,:2]+=(kappa*B0(e)-shift)*np.eye(2)+1j*pi*W2@W2.conj().T
    return np.eye(4)-2j*pi*W.conj().T@np.linalg.solve(D,W)

values=[]
energies=np.linspace(1.452,1.548,301)
for kap in [0,1e-7,3e-7,1e-6,2e-6,3e-6,5e-6,1e-5,2e-5,3e-5]:
   center=0; sel=unsel=0; rad=unit=0
   for e in energies:
      S=S4(e,kap)
      Sun=S4(e,kap,chi)
      sel=max(sel, float(norm(S[:,0]-[-1,0,0,0])))
      unsel=max(unsel,float(norm(Sun[:,0]-[1,0,0,0])))
      rad=max(rad,float(norm(S[2:,0])))
      unit=max(unit,float(norm(S.conj().T@S-np.eye(4),ord=2)))
   S=S4(E0,kap);center=float(norm(S[:,0]-[-1,0,0,0]))
   c=abs(cos(tau*E0))
   worst_opt_center=float(2*np.sqrt(kap/(gamma*(1-c)+kap))) if kap else 0.0
   assert unit<1e-11
   values.append(dict(relative_independent_radiative_density=kap/gamma,center_right_input_error=center,
                       max_selected_right_input_error_grid=sel,max_unselected_right_input_error_grid=unsel,
                       max_selected_radiative_loss_amplitude_grid=rad,max_s_unitarity_residual=unit,
                       center_worst_parity_lower_bound_for_any_real_detuning=worst_opt_center))
error_target=0.01
sharp_kappa_over_gamma=(error_target**2/(4-error_target**2))*(1-abs(cos(tau*E0)))
out={'model':'Finite-band reciprocal two-emitter Fano gate plus independent emission continuum for each emitter, all four output ports included',
     'center':E0,'strict_center_condition_relative_kappa_over_gamma_for_full_photon_operator_norm_below_1pct':sharp_kappa_over_gamma,
     'loss_grid_diagnostics':values,
     'exact_center_identity':'On each parity channel with desired radiative halfwidth a=pi*gamma*E^2*(1+p*cos(tau*E)) and independent emission halfwidth ell=pi*kappa*E^2, optimal real tuning at q=0 gives complete-photon-output error 2*sqrt(ell/(a+ell)). No loss conditioning. All physical outputs present.',
     'scope':'Strict necessary independent-radiation bound for selected center and all incident photon channel superpositions. Grid rows are diagnostics only and include the causal real bath Lamb shift with center retuning. Does not model 3D radiation cross-correlations, dephasing or finite-time extraction.'}
with open('/mnt/data/astra_reciprocal_independent_loss_results_20261026.json','w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
