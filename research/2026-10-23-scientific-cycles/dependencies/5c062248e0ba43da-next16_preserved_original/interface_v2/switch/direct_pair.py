"""Nominal device/circuit screen, not a successful engine or universal bound.
One common-source pair of GS66516T GaN FETs plus exchange inductor.
All J2 and loss margins are inputs to be refreshed from the full engine.
"""
from pathlib import Path
import json,math
import numpy as np
from scipy.optimize import least_squares,brentq
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parent
source='https://www.infineon.com/assets/row/public/documents/24/49/infineon-gs66516t-datasheet-en.pdf'
V400=400.;Q400=134e-9;E400=17e-6;C400=126e-12
# Positive, decreasing capacitance interpolation. Anchors are datasheet typicals.
# The exponential is an explicitly declared model, not vendor SPICE.
def ce(p,v):
 ci,ca,vs=np.exp(p);return ci+ca*np.exp(-v/vs)
def qe(p,v):
 ci,ca,vs=np.exp(p);return ci*v+ca*vs*(-np.expm1(-v/vs))
def ee(p,v):
 ci,ca,vs=np.exp(p);x=v/vs;return .5*ci*v*v+ca*vs*vs*(1-(1+x)*np.exp(-x))
r=least_squares(lambda p:np.array([ce(p,V400)/C400-1,qe(p,V400)/Q400-1,ee(p,V400)/E400-1]),np.log([118e-12,1e-9,83.]),xtol=1e-13,ftol=1e-13,gtol=1e-13)
p=r.x
m=14;dv=22.9;vin=m*dv;ton=.001;toff=.003;J=18000.;margin=.02674;LA=1.19709e-6
Qg=14.2e-9;vg=6.;ig=320e-6
Gdyn=2*Qg*vg;Gbias=2*ig*vg*ton
C=float(ce(p,vin));Q=float(qe(p,vin));E=float(ee(p,vin))
cases=[]
for rnlabel,Ron in [('25C_typ_favorable',.025),('25C_max_not_warm_guarantee',.032),('65C_typ_graph_approx',.036),('150C_typ',.065)]:
 for comm,Ec in [('one_Eoss_CONDITIONAL_RECOVERY_OF_OFF_COMMMUTATION',E),('settled_passive_OFF_then_hard_ON',vin*Q)]:
  for ilabel,ileak in [('zero_only_diagnostic',0.),('25C_typ650V_used_only_sensitivity',4e-6),('25C_max650V_used_only_sensitivity',100e-6)]:
   b=Ec+Gdyn+Gbias+vin*ileak*toff;a=2*Ron*J/m**2
   Aopt=math.sqrt(b/a);minloss=2*math.sqrt(a*b)
   Rextra=margin*margin*m*m/(4*J*b)-2*Ron
   cases.append(dict(Ron_scope=rnlabel,Ron_each_ohm=Ron,commutation=comm,leakage_scope=ilabel,leakage_A=ileak,A_bank_opt_m2=Aopt,minimum_switch_gate_leak_J_per_pair_half_m2=minloss,max_other_series_R_ohm_after_area_optimization=Rextra,remaining_margin_J_per_pair_half_m2=margin-minloss,one_off_interval_energy_J=b))
# The OFF capacitance rings with the same physical exchange L, not a separate
# freely chosen compensator. Bank C is orders larger; frozen-bank limit is used.
A=.002;L=LA*m*m/A
vpk=brentq(lambda v:ee(p,v)-vin*qe(p,v),650.,2000.)
def rhs(t,y):
 v,i=y;return [i/ce(p,max(0.,v)),(vin-v-.072*i)/L]
def cross(t,y):return y[0]-650
cross.terminal=True;cross.direction=1
s=solve_ivp(rhs,[0,.001],[0.,0.],events=cross,rtol=1e-9,atol=[1e-8,1e-10],max_step=1e-7)
ring=dict(bank_area_m2=A,L_H=L,series_resistance_ohm=.072,voltage_cross_650_time_s=float(s.t_events[0][0]),current_at650_A=float(s.y_events[0][0,1]),lossless_turning_voltage_V=float(vpk),model_Q650_C=float(qe(p,650.)),model_E650_J=float(ee(p,650.)),energy_condition='Eoss(vpk)=Vin*Qoss(vpk); positive decreasingC makesvpk>2Vin. Fixedbankapproximationonly; noavalanchemodelorclaimofsurvivalabove650V')
out=dict(scope=__doc__,source=source,source_revision='210727',anchors=dict(Coss400_F=C400,Qoss400_C=Q400,Eoss400_J=E400,Ron25C_typ_ohm=.025,Ron25C_max_ohm=.032,Ron150C_typ_ohm=.065,Qg400V_6V_C=Qg,gate_bias6V25C_A=ig,leak650V25C_typ_A=4e-6,leak650V25C_max_A=100e-6,leak650V150C_typ_A=800e-6),declared_capacitance_model=dict(form='C(v)=Cinf+Cexp*exp(-v/Vscale)',Cinf_F=float(np.exp(p[0])),Cexp_F=float(np.exp(p[1])),Vscale_V=float(np.exp(p[2])),anchor_relative_residual=r.fun.tolist(),scope='Nominal interpolation ofvendor typicals;notguaranteeddevicebounds. Visually consistentwithFigs7/8.'),inputs=dict(series_patches_each_bank=m,local_Vdifference=dv,terminal_Vdifference=vin,swap_on_s=ton,thermal_hold_off_s=toff,J2dt_A2_s_m4=J,fullengine_available_margin_J_per_pair_half_m2=margin),at_actual_voltage=dict(Coss_F=C,Qoss_C=Q,Eoss_J=E,passive_OFF_settling_loss_J=vin*Q-E,hard_ON_loss_J=E,total_settled_commutation_J=vin*Q,gatecharge_loss_J=Gdyn,gatebias_loss_J=Gbias),cases=cases,unclamped_OFF_ring=ring,exact_joint_requirement='[(2Ron+Rcoil+Rwire)*J/m^2]*A + [Ecomm+2QgVg+2IgVg*ton+integral_VIoff_dt+Edriver_control+Ebuffer]/A + LFE < recomputed engine margin, with thermal changes re-integrated; maxRvalues give allremaining budget toseriesR andzerootherloss, thereforealternativesnotjointallowances')
# Fixed geometry: these allowances must be shared, never independently spent.
Af=.0018;warmRon=.036;half=ton+toff
fixed=[]
for rext in [0.,.005,.01,.02]:
 for ileak in [0.,4e-6,1e-5,1e-4]:
  base=E+Gdyn+Gbias+vin*ileak*toff
  ec=(2*warmRon+rext)*Af*Af/m**2*J
  fixed.append(dict(A_bank_m2=Af,other_series_R_ohm=rext,OFF_leak_current_A=ileak,gate_bias_current_A=ig,Ron_each_ohm=warmRon,commutation='one_Eoss_only_CONDITIONAL_ON_ACTUAL_OFF_ENERGY_RECOVERY',max_controller_plus_unallocated_buffer_FE_loss_power_W=(margin*Af-ec-base)/half,zero_other_losses_beyond_entries=True))
out['fixed_geometry_joint_budget']=fixed
out['one_coherent_requirement_example']=dict(A_bank_m2=Af,Rother=.01,Pcontrol=.0005,Ioff_max_A=(margin*Af-(2*warmRon+.01)*Af*Af/m**2*J-(E+Gdyn+Gbias)-.0005*half)/(vin*toff),scope='Jointrequirementonly;FE/bufferlosszeroandOFFcommutationrecoveryotherwiseideal. ActualwarmRon,Ig,Ioffunqualified.')
(ROOT/'direct_pair.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
for x in cases:
 if x['Ron_scope']=='65C_typ_graph_approx':print(x)
