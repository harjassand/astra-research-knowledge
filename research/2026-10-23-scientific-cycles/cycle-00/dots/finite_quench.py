"""Replace imposed 1e8K/s front-end with finite gas-film,300K ideal cooling wall.
Same fully-developed-laminar lumped mean model as recuperator. External coolant
flow/material/power and radial hot tails unresolved. Boundary guard is mandatory.
"""
import time,json,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import counterflow as cf
from quench_screen import P
ROOT=Path(__file__).resolve().parent
QUENCH_D=.001;G=1.;last={}
def finite_cool(g,Y,Ta,Tb,beta,rtol=1e-8):
 global last
 W=g.molecular_weights;ns=g.n_species;g.transport_model='mixture-averaged';g.TPY=Ta,P,Y;hi=g.enthalpy_mass
 def rhs(x,s):
  g.TPY=s[ns],P,s[:ns];h=3.66*g.thermal_conductivity/QUENCH_D;q=4*h/QUENCH_D/G*(s[ns]-300);dy=g.net_production_rates*W/G
  return np.r_[dy,(-q-np.dot(g.partial_molar_enthalpies/W,dy))/g.cp_mass,32*g.viscosity*G/(g.density*QUENCH_D**2),g.density/G]
 def stop(x,s):return s[ns]-Tb
 stop.terminal=True;stop.direction=-1
 sol=solve_ivp(rhs,[0,.3],np.r_[Y,Ta,0.,0.],method='BDF',rtol=rtol,atol=1e-12,events=stop,max_step=.0001)
 if not sol.success or len(sol.t_events[0])!=1:raise RuntimeError('finite quench did not reach handover')
 y=sol.y[:ns,-1];g.TPY=Tb,P,y;last={'diameter_m':QUENCH_D,'length_m':float(sol.t[-1]),'residence_s':float(sol.y[-1,-1]),'pressure_drop_Pa':float(sol.y[-2,-1]),'rejected_heat_J_kg':hi-g.enthalpy_mass,'outlet_O_massfraction':float(g['O'].Y[0]),'min_Y':float(sol.y[:ns].min()),'mass_error':float(abs(sol.y[:ns].sum(0)-1).max())};return y,last
if __name__=='__main__':
 t=time.monotonic();rows=[];cf.cool=finite_cool
 for D in [.001,.0005,.0001]:
  QUENCH_D=D
  for Tq in [1800.,2400.]:
   try:
    r=cf.run(Tq=Tq,L=.02);r['front_quench']=last.copy();r['accepted_boundary']=abs(r['cold_inlet_residual_K'])<1e-3 and abs(r['heat_balance_residual_J_kg'])<1e-6*r['gross_J_kg'];rows.append(r);print(D,Tq,r['net_gas_heat_MJ_mol'],r['accepted_boundary'],last,flush=True)
   except Exception as e:rows.append({'D':D,'Tq':Tq,'error':repr(e)})
 (ROOT/'results/finite_quench.json').write_text(json.dumps({'rows':rows,'wall_s':time.monotonic()-t,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2)+'\n')
