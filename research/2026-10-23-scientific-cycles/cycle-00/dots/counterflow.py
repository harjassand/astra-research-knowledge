"""Finite-film counterflow shooting calculation with coupled hot-stream chemistry.
Favorable zero wall resistance, fully developed laminar Nu=3.66 on each side;
fixed1atm chemistry, diagnosed pressure drops, frozen fresh-air cold composition.
Not a validated materials device. No externally imposed recuperator cooling ramp.
"""
import json,time,resource
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import cantera as ct
from quench_screen import gas_model,cool,T0,P
ROOT=Path(__file__).resolve().parent

def run(Tq=2100.,D=.001,G=1.,L=.1,variant='gri',rtol=1e-7,wallR=0.):
 start=time.monotonic();g=gas_model(variant);g.transport_model='mixture-averaged';c=gas_model();c.transport_model='mixture-averaged';c.TPX=T0,P,{'N2':.79,'O2':.21};feedY=c.Y.copy();h0=c.enthalpy_mass;g.TPY=3100.,P,feedY;g.equilibrate('TP');hhot=g.enthalpy_mass;Yq,_=cool(g,g.Y.copy(),3100,Tq,1e8);hq=g.enthalpy_mass;W=g.molecular_weights;ns=g.n_species;calls=0
 def integrate(Tcout,dense=False):
  nonlocal calls
  calls+=1
  def rhs(x,state):
   Y=state[:ns];Th,Tc=state[ns:ns+2];g.TPY=max(200.,Th),P,Y;c.TPY=max(200.,Tc),P,feedY
   U=1/(D/(3.66*g.thermal_conductivity)+D/(3.66*c.thermal_conductivity)+wallR);qprime=4*U/D/G*(Th-Tc)
   dY=g.net_production_rates*W/G
   dhchem=np.dot(g.partial_molar_enthalpies/W,dY)
   return np.r_[dY,(-qprime-dhchem)/g.cp_mass,-qprime/c.cp_mass,32*g.viscosity*G/(g.density*D*D),32*c.viscosity*G/(c.density*D*D)]
  def too_cold(x,y):return y[ns+1]-250
  too_cold.terminal=True;too_cold.direction=-1
  def too_hot(x,y):return 3400-max(y[ns],y[ns+1])
  too_hot.terminal=True;too_hot.direction=-1
  init=np.r_[Yq,Tq,Tcout,0.,0.];sol=solve_ivp(rhs,(0,L),init,method='BDF',rtol=rtol,atol=np.r_[np.full(ns,1e-13),1e-6,1e-6,1e-6,1e-6],events=[too_cold,too_hot],dense_output=dense,max_step=L/80)
  if not sol.success:raise RuntimeError(sol.message)
  return sol
 def mismatch(T):
  sol=integrate(T);return sol.y[ns+1,-1]-T0
 low=mismatch(300.);high=mismatch(3100.)
 if low*high>0:raise RuntimeError(('no shooting bracket',low,high))
 Tcout=brentq(mismatch,300.,3100.,xtol=1e-6);sol=integrate(Tcout,True);assert sol.t[-1]>=L*(1-1e-10)
 xx=np.linspace(0,L,401);states=sol.sol(xx);last=states[:,-1];Yout=last[:ns];Thout=last[ns];g.TPY=Thout,P,Yout;hout=g.enthalpy_mass;c.TPY=Tcout,P,feedY;qc=c.enthalpy_mass-h0
 i=[g.species_index(s) for s in ['NO','NO2']];mol=lambda Y:1000*np.sum(Y[i]/W[i]);nmol=mol(Yout);qmol=mol(Yq);initialNO=gas_model();initialNO.TPY=3100,P,feedY;initialNO.equilibrate('TP')
 energyres=(hq-hout)-qc
 gaps=states[ns]-states[ns+1]
 r={'Tq_K':Tq,'D_m':D,'mass_flux_kg_m2_s':G,'length_m':L,'variant':variant,'wall_resistance_m2K_W':wallR,'Thout_K':float(Thout),'Tc_out_K':float(Tcout),'maximum_hot_temperature_K':float(states[ns].max()),'minimum_hot_temperature_K':float(states[ns].min()),'min_gap_K':float(gaps.min()),'max_gap_K':float(gaps.max()),'retained_mol_NOx_kg':nmol,'recuperator_survival':nmol/qmol,'gross_J_kg':hhot-h0,'recovered_J_kg':qc,'net_gas_heat_MJ_mol':(hhot-h0-qc)/nmol/1e6,'pressure_drop_hot_Pa':float(last[ns+2]),'pressure_drop_cold_Pa':float(last[ns+3]),'heat_balance_residual_J_kg':energyres,'mass_drift':float(abs(states[:ns].sum(0)-1).max()),'min_Y':float(states[:ns].min()),'cold_inlet_residual_K':float(last[ns+1]-300),'shooting_calls':calls,'wall_seconds':time.monotonic()-start,'kinetic_steps':len(sol.t),'rtol':rtol,'profile':{'x_m':xx.tolist(),'Th_K':states[ns].tolist(),'Tc_K':states[ns+1].tolist(),'NOx_mol_kg':(1000*(states[i]/W[i,None]).sum(0)).tolist()}}
 return r
if __name__=='__main__':
 rows=[];start=time.monotonic()
 for Tq in [1800.,2100.,2400.]:
  for L in [.02,.1,.5]:
   try:
    r=run(Tq=Tq,L=L);rows.append(r);print(Tq,L,r['net_gas_heat_MJ_mol'],r['recuperator_survival'],r['Thout_K'],r['Tc_out_K'],r['min_gap_K'],r['pressure_drop_hot_Pa'],flush=True)
   except Exception as e:
    rows.append({'Tq_K':Tq,'length_m':L,'status':'NUMERICAL_FAILURE_NOT_PHYSICAL_EXCLUSION','error':repr(e)});print('FAILED',Tq,L,repr(e),flush=True)
   (ROOT/'results/counterflow_partial.json').write_text(json.dumps({'rows':rows},indent=2)+'\n')
 (ROOT/'results/counterflow.json').write_text(json.dumps({'rows':rows,'wall_seconds':time.monotonic()-start,'max_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2)+'\n')
