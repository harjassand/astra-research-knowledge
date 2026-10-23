"""Independent reaction-order pressure formulas; naive uniform scaling must fail."""
import json
from pathlib import Path
import numpy as np
from helper import ThermoKernel
R=Path(__file__).resolve().parent;k=ThermoKernel();T=2200.;Y=np.ones(6)/6;a=k.evaluate(T,Y,101325,return_rates=True)
C=a['rho'][0]*Y/k.W;M=C.sum();A=k.A;k0=9.2e-40*A*A*T**-1.6;kinf=4.9e-16*A*T**-.4;Pr=k0*M/kinf
rows=[]
for s in [.5,.8,1.2,2.]:
 b=k.evaluate(T,Y,101325*s,return_rates=True);fallratio=s*(1+Pr)/(1+s*Pr)
 f=np.array([s*s,s*s,s*s,s*s,s*s,s*s*fallratio,s*s]);r=np.array([s**3,s**3,s*s,s*s,s**3,s*fallratio,s*s])
 fr=b['forward_rates_of_progress'][:,0]/a['forward_rates_of_progress'][:,0];rr=b['reverse_rates_of_progress'][:,0]/a['reverse_rates_of_progress'][:,0]
 rows.append({'P_ratio':s,'exact_order_max_relative_error':float(max(np.max(abs(fr/f-1)),np.max(abs(rr/r-1)))),'naive_all_rates_P_squared_max_relative_error':float(max(np.max(abs(fr/s**2-1)),np.max(abs(rr/s**2-1))))})
# Actual floating coefficient continuity residual, separately from analytic intent.
def hs(c,T):return sum(c[j]*T**j/(j+1) for j in range(5))+c[5]/T,c[0]*np.log(T)+sum(c[j]*T**j/j for j in range(1,5))+c[6]
sp=[]
for i,n in enumerate(k.species_names):
 t=k.nasa[i,0];h1,s1=hs(k.nasa[i,1:8],t);h0,s0=hs(k.nasa[i,8:15],t);sp.append({'species':n,'remaining_h_jump_J_kg':float((h1-h0)*k.R*t/k.W[i]),'remaining_s_jump_J_kg_K':float((s1-s0)*k.R/k.W[i])})
result={'pressure_tests':rows,'floating_NASA_continuity_residuals':sp,'scope':'This checks finite reaction orders/third bodies/Lindemann scaling, not a trajectory. Stored float coefficients leave tiny reported splice residuals; exact-real continuity is not claimed.'};(R/'pressure_scaling_check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
