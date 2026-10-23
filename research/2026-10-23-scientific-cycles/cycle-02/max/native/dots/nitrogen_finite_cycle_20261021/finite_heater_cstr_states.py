"""Matched isothermal CSTR state test, not a general RTD bound or process claim.
Fixed volume/flow0.1m3s/kg and1atm. Unequal transient outflow follows isobaric EOS;
steady states have equal inlet/outlet mass. Uses fresh versus equilibrium starts.
"""
import sys,json,time,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'thermo_helper'));from helper import ThermoKernel
from validate import native_corrected
K=ThermoKernel();g=native_corrected(K);W=g.molecular_weights;g.TPX=300,101325,{'N2':.79,'O2':.21};fresh=g.Y.copy();start=time.monotonic();rows=[]
for T in [2300.,2500.,2700.]:
 g.TPY=T,101325,fresh;g.equilibrate('TP');eq=g.Y.copy()
 for tag,Y0 in [('fresh',fresh),('equilibrium',eq)]:
  def fun(t,y):
   g.TPY=T,101325,y;return ((fresh-y)/.1+g.net_production_rates*W)/g.density
  sol=solve_ivp(fun,[0,2],Y0,method='BDF',rtol=1e-10,atol=1e-18);Y=sol.y[:,-1];rate=fun(2,Y)
  r={'T_K':T,'start':tag,'success':sol.success,'NOx_mol_kg':float(np.sum(1000*Y[[4,5]]/W[[4,5]])),'max_abs_species_rate_s_inv':float(max(abs(rate))),'min_Y':float(sol.y.min()),'mass_drift':float(max(abs(sol.y.sum(0)-1))),'steps':len(sol.t)-1};rows.append(r);print(json.dumps(r),flush=True)
(R/'finite_heater_cstr_states.json').write_text(json.dumps({'scope':__doc__,'rows':rows,'wall_s':time.monotonic()-start,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope_limit':'Two initial states, not an exhaustive proof of uniqueness or stability across all states. No parameter inferred by fitting results.'},indent=2)+'\n')
