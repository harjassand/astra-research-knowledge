"""Actual canonical optical gate plus FE-isolation transition integrals.
All energies normalized by ONE-bank area A; a pairhalfcycle contains two
faces that each make a full low/high/low roundtrip, hence four flips total.
T343K/Vfe fixed transition reference, NOT a favorable efficiency assumption.
"""
from pathlib import Path
import json
import numpy as np
from scipy.integrate import quad
from gate_stack import *
ROOT=Path(__file__).resolve().parent
T=343.;dt=20e-6
L=face(MUL,T,23.);H=face(MUH,T,23.)
def wf(m,vf):
 z=face(m,T,vf)
 return z['Vg']*(z['Cq']+CGAP+CI*z['Vg_mu'])
W=quad(lambda m:wf(m,23.),MUL,MUH,epsabs=1e-12)[0]
Q=H['Qg']-L['Qg'];dv=H['Vg']-L['Vg']
mudot=(MUH-MUL)/dt
j2=quad(lambda m:((face(m,T,23.)['Cq']+CGAP+CI*face(m,T,23.)['Vg_mu'])*mudot)**2/mudot,MUL,MUH,epsabs=1e-8)[0]
# Gate dielectric's exact resistive-step dissipation sum, bothdirections.
loss_up=H['Vg']*Q-W;loss_down=W-L['Vg']*Q
out=dict(scope=__doc__,dt_flip_s=dt,temperature_reference_K=T,Vg_low=L['Vg'],Vg_high=H['Vg'],
 deltaQg_C_m2=Q,delta_Qisolation_C_m2=CI*dv,
 recoverable_gate_input_J_m2_per_upflip=W,
 recoverable_gate_input_pair_halfcycle_J_m2=2*W,
 recoverable_gate_output_pair_halfcycle_J_m2=2*W,
 absolute_processed_gate_energy_pair_halfcycle_J_m2=4*W,
 hard_step_loss_up_J_m2=loss_up,hard_step_loss_down_J_m2=loss_down,
 hard_step_pair_halfcycle_loss_J_m2=2*(loss_up+loss_down),
 isolation_only_hard_step_loss_per_flip_J_m2=.5*CI*dv*dv,
 integral_gate_current_squared_one_flip_A2s_m4=j2,
 integral_gate_current_squared_pair_halfcycle_A2s_m4=4*j2,
 peak_flip_gate_current_A_m2=max((face(m,T,23.)['Cq']+CGAP+CI*face(m,T,23.)['Vg_mu'])*mudot for m in np.linspace(MUL,MUH,201)),
 fe_bias_cross_absolute_processed_pair_halfcycle_J_m2=2*CI*dv*(23.+.1),
 conditional_one_minus_loss_over_absolute_processed_energy_to_fit_0p0267J_margin=1-.02673822068938191/(4*W),
 conditional_gate_RA_ohm_m2_to_fit_0p0267J_margin=.02673822068938191/(4*j2),
 caution='Conditional0.0267J is root provisional shape0 withisolationmass favorableotherlosses halfcycle margin only. New coupled electrical trajectory MUSTrecompute it. These are transitionprocessedenergies,notnetwork oractualrecoveryefficiency; includesneitherFE/SiCisolationdielectriclossnorcontrollers/switch/bufferreset.')
(ROOT/'flip_budget.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
