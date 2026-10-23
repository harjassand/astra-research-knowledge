"""Favorable, explicitly unqualified gas-recycle quench limit. No physical SEC claim."""
import sys,time,json,resource,hashlib
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'nitrogen_finite_cycle_20261021/thermo_helper'))
from helper import ThermoKernel
from validate import native_corrected
K=ThermoKernel();g=native_corrected(K);W=g.molecular_weights;P=101325.;g.TPX=300,P,{'N2':.79,'O2':.21};fresh=g.Y.copy();outdir=Path(__file__).resolve().parent

def h(T,Y):g.TPY=T,P,Y;return g.enthalpy_mass

def no(Y):return float(np.sum(1000*Y[[4,5]]/W[[4,5]]))

def heater(T):
 def f(v,Y):
  g.TPY=T,P,Y[:6];dy=g.net_production_rates*W;dh=float(g.partial_molar_enthalpies/W@dy)
  return np.r_[dy,max(0,dh),max(0,-dh)]
 s=solve_ivp(f,[0,.1],np.r_[fresh,0.,0.],method='BDF',rtol=2e-9,atol=np.r_[np.full(6,1e-17),1e-5,1e-5]);assert s.success
 return s.y[:6,-1],float(s.y[6,-1]),float(s.y[7,-1]),float(s.y[:6].min())

def cool(Y):
 def f(t,y):
  g.TPY=1700-1e4*t,P,y;return g.net_production_rates*W/g.density
 s=solve_ivp(f,[0,.14],Y,method='BDF',rtol=2e-9,atol=1e-17);assert s.success
 return s.y[:,-1],s

def one(T):
 yh,positive,removal,miny=heater(T);hh=h(T,yh);delta=hh-h(1700,yh);yp,_=cool(yh);yp=yp.copy();history=[]
 for it in range(100):
  rec=delta/(h(1700,yp)-h(300,yp));mix=(yh+rec*yp)/(1+rec);new,sol=cool(mix);err=float(max(abs(new-yp)));history.append(err);yp=new.copy()
  if err<1e-12:break
 else:raise RuntimeError('Recycle not closed')
 rec=delta/(h(1700,yp)-h(300,yp));mix=(yh+rec*yp)/(1+rec);yfinal,sol=cool(mix)
 # Counterflow exchanger pinch check: use hot enthalpy curve, allocate only fresh
 # feed preheat duty from300 to1700. Excess heat explicitly rejected.
 pre=h(1700,fresh)-h(300,fresh);hin=h(1700,mix);Q=np.array([(1+rec)*(hin-h(1700-1e4*t,y)) for t,y in zip(sol.t,sol.y.T)])
 gaps=[]
 for t,q in zip(sol.t,Q):
  if 0<=q<=pre:
   g.HPY=h(1700,fresh)-q,P,fresh;gaps.append(float(1700-1e4*t-g.T))
 initial_heat=h(T,fresh)-h(1700,fresh);work=initial_heat+positive
 rejected=(1+rec)*(hin-h(300,yp))-pre
 endpoint_res=work-removal-(h(300,yp)-h(300,fresh))-rejected
 once,ss=cool(yh)
 # Same heater/preheat cap gives the once-through reference same heat work.
 pumping={str(frac):rec*K.R*300*np.sum(yp/W)*np.log(1+frac) for frac in [.01,.1,.5]}
 return {'heater_K':T,'heater_v_over_mdot':.1,'quench_K':1700.,'recycle_kg_per_kg_fresh':float(rec),'fixed_point_iterations':len(history),'fixed_point_max_Y_residual':float(max(abs(yfinal-yp))),'hot_NOx_mol_kg':no(yh),'net_product_NOx_mol_per_kg_fresh':no(yp),'once_through_product_NOx_mol_kg':no(once),'heater_positive_J_kg_fresh':float(work),'heater_removal_J_kg_fresh':removal,'ideal_feed_preheat_J_kg_fresh':float(pre),'uncredited_rejected_heat_J_kg_fresh':float(rejected),'endpoint_energy_residual_J_kg':float(endpoint_res),'minimum_sampled_pinch_K':min(gaps),'heat_MJ_mol_NOx':float(work/no(yp)/1e6),'once_through_heat_MJ_mol_NOx':float(work/no(once)/1e6),'ideal_isothermal_recycle_pump_J_kg_fresh_by_pressure_ratio_increment':pumping,'minimum_heater_Y':miny,'minimum_cooler_Y':float(sol.y.min()),'final_product_Y':yp.tolist(),'iteration_residuals':history}
if __name__=='__main__':
 st=time.monotonic();rows=[]
 for T in [2700.,2900.,3100.]:rows.append(one(T));print(json.dumps(rows[-1]),flush=True)
 result={'scope':__doc__,'rows':rows,'wall_s':time.monotonic()-st,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'warnings':['Instantaneous ideal gas mixing, not proven quench hydrodynamics','Cooling trajectory and recuperator infinite-area limit are favorable assumptions','Pump columns are illustrative pressure-drop costs, not admitted pressure losses','Six-species source omits N2O and surfaces','Same final300K net gas product; no capture or fertilizer claim','Sampled pinch diagnostic is not rigorous continuum heat-exchanger proof']}
 (outdir/'result.json').write_text(json.dumps(result,indent=2))
