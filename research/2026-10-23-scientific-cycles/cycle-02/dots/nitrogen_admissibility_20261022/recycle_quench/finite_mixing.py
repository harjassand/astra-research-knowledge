"""Finite-rate homogeneous entrainment, full species recycle closure.
Diagnostic of mixing-time requirement, NOT a resolved jet or admitted apparatus.
Signed Newton helper reused without modifying its positive-state chemistry.
"""
import sys,importlib.util,time,json,resource,hashlib
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
D=Path(__file__).resolve().parent;root=D.parents[1]
spec=importlib.util.spec_from_file_location('signed_recycle',root/'nitrogen_finite_cycle_20261021/signed_trial_helper/helper.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);K=mod.SignedTrialKernel()
sys.path.insert(0,str(D));import ideal_recycle as old
P=101325.;R=.85;TH=2700.;yv,heat,removal,_=old.heater(TH);fresh=old.fresh.copy()

def prop(T,Y):
 t,y,_,d=K._signed_state(T,Y,P,False);cp,hh,ss=K.thermochemistry(t);hi=hh[:,0]*K.R*T/K.W;cpi=cp[:,0]*K.R/K.W;cpv=float(Y@cpi);rho=P/(K.R*np.sum(Y/K.W)*T);C=rho*Y[:,None]/K.W[:,None]
 rate=K.signed_rates(t,C)[0][:,0];source=K.W*(K.nu@rate)
 return hi,cpv,rho,source

def enthalpy(T,Y):
 return float(Y@(K.thermochemistry(np.array([T]))[1][:,0]*K.R*T/K.W))

def pass_once(tau,yp,tol=2e-8):
 hr=enthalpy(300,yp);hh=enthalpy(TH,yv)
 def rhs(x,s):
  mass=s[:6];m=mass.sum();Y=mass/m;T=float(s[6]);hi,cp,rho,w=prop(T,Y);dm=R*yp+tau*(m/rho)*w
  dt=(R*(hr-hi@yp)-tau*(m/rho)*(hi@w))/(m*cp)
  return np.r_[dm,dt]
 a=solve_ivp(rhs,[0,1],np.r_[yv,TH],method='BDF',rtol=tol,atol=np.r_[np.full(6,1e-16),1e-5]);assert a.success,a.message
 m=a.y[:6,-1].sum();ym=a.y[:6,-1]/m;tm=float(a.y[6,-1]);Hres=m*enthalpy(tm,ym)-hh-R*hr
 def cool(u,Ysmall):
  Y=np.r_[1-Ysmall.sum(),Ysmall];T=tm-1e4*u;_,cp,rho,w=prop(T,Y);return (w/rho)[1:]
 b=solve_ivp(cool,[0,(tm-300)/1e4],ym[1:],method='BDF',rtol=tol,atol=1e-16);assert b.success,b.message
 b.y=np.vstack([1-b.y.sum(0),b.y])
 return b.y[:,-1],{'Tmix_K':tm,'mix_enthalpy_residual_J_per_kg_fresh':float(Hres),'mix_mass_residual':float(m-1-R),'minimum_Y_observed':float(min((a.y[:6]/a.y[:6].sum(0)).min(),b.y.min())),'mix_steps':len(a.t)-1,'cool_steps':len(b.t)-1},a,b

def case(tau,tol=2e-8):
 st=time.monotonic();yp=np.array(json.loads((D/'result.json').read_text())['rows'][0]['final_product_Y']);errors=[]
 for j in range(100):
  new,receipt,a,b=pass_once(tau,yp,tol);err=float(max(abs(new-yp)));errors.append(err);yp=new
  if err<1e-11:break
 else:raise RuntimeError('Return composition did not close')
 new,receipt,a,b=pass_once(tau,yp,tol);Tpre=min(receipt['Tmix_K'],1700);work=enthalpy(TH,fresh)-enthalpy(Tpre,fresh)+heat
 rejected=enthalpy(TH,yv)-enthalpy(300,yp)-(enthalpy(Tpre,fresh)-enthalpy(300,fresh))
 out={'tau_mix_s':tau,'R':R,'iterations':len(errors),'fixed_point_Y_residual':float(max(abs(new-yp))),'rtol':tol,'net_NOx_mol_kg_fresh':old.no(yp),'ideal_heater_heat_MJ_mol_NOx':work/old.no(yp)/1e6,'actual_mixer_exit_temperature_K':receipt['Tmix_K'],'fresh_preheat_upper_K':Tpre,'heater_heat_J_kg_fresh':work,'uncredited_total_heat_rejection_J_kg_fresh':rejected,'endpoint_energy_residual_J_kg':float(work-removal-(enthalpy(300,yp)-enthalpy(300,fresh))-rejected),'wall_s':time.monotonic()-st,**receipt}
 tag=str(tau).replace('.','p');np.savez_compressed(D/f'mix_tau_{tag}_trajectory.npz',progress=a.t,mass_temperature=a.y,cool_t=b.t,cool_Y=b.y,return_Y=yp)
 return out
if __name__=='__main__':
 st=time.monotonic();rows=[]
 for tau in [1e-5,1e-4,1e-3,1e-2]:
  rows.append(case(tau));print(json.dumps(rows[-1]),flush=True)
  (D/'finite_result.json').write_text(json.dumps({'scope':__doc__,'rows':rows,'wall_s':time.monotonic()-st,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'signed_helper_sha256':hashlib.sha256((root/'nitrogen_finite_cycle_20261021/signed_trial_helper/helper.py').read_bytes()).hexdigest()},indent=2))
