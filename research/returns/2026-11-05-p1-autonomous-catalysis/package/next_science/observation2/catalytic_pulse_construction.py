"""Conditional pulse/gate checks, not a causal fit to the catalyst."""
from pathlib import Path
import json
import numpy as np
from scipy.special import expi
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parent
KB=8.617333262e-5
TAU=4.1e-8
pulses=[]
for T in [298.,300.,353.]:
 c=.192/(KB*T)
 shape=expi(c)-.5772156649015329-np.log(c)
 for pref in [2.3e9,1e13]:
  k0=pref*np.exp(-.375/(KB*T)); k1=pref*np.exp(-.183/(KB*T))
  A=k0*TAU*shape; p=-np.expm1(-A)
  pulses.append(dict(T=T,prefactor=pref,cold=k0,hot=k1,rectangle=k1*TAU,
      excess_action=A,extra_probability_upper=p,
      ready_targets_for_gain3point3_if_true_branching=(1-1/3.3)/p))
gates=[]
for T in [298.,300.,353.]:
 b=1/TAU; a=b*np.exp(-.126/(KB*T))
 k0=2.3e9*np.exp(-.375/(KB*T)); k1=2.3e9*np.exp(-.183/(KB*T))
 K=np.array([[k0+a,-a],[-b,k1+b]])
 start=np.array([b,a])/(a+b)
 time=float(start@np.linalg.solve(K,np.ones(2)))
 closed=(b*k1+a*k0+(a+b)**2)/((a+b)*(k0*k1+k0*b+a*k1))
 assert abs(time-closed)<1e-12*max(time,closed)
 gates.append(dict(T=T,p_excited=float(start[1]),up=a,down=b,
     cold=k0,hot=k1,mean_time=time,gain=1/(k0*time),
     fast_gain=(b*k0+a*k1)/((a+b)*k0)))
F,B0,B=3.3,66.1,60.2
elasticity=(B0/B-1)/(F-1)
x=brentq(lambda x:x/np.expm1(x)-elasticity,.01,20)
restricted=dict(scope='Illustrative common-range slope only; actual S16 gain is U-shaped and this does not fit its full range. Positive offspring reduction is not generally a whole-cycle model.',
 F=F,R=1-1/F,elasticity=elasticity,required_action=x,
 tau_for_action=TAU*x/pulses[0]['excess_action'],B_unsaturated=B0/F)
result=dict(scope='Voltage reference, thermal free energy, pulse shape and active-site mapping unacquired. Conditional calculations only.',
 pulses=pulses,thermal_gate=gates,restricted_slope=restricted,
 normalization=dict(uptake_base=.079,uptake_modified=.04175,
 TOF_gain=F,current_gain=F*.04175/.079,
 static_barrier_eV=KB*298*np.log(F)))
(ROOT/'catalytic_pulse_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
