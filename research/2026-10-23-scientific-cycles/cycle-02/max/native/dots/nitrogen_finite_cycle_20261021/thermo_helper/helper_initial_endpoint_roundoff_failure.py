"""Explicit continuous-NASA model variant with variable-pressure ideal-gas kinetics.
Internal energy includes formation energy. e: J/kg; U=rho*e: J/m3 gas.
No model validation, cycle, pressure closure or universal integration guarantee.
"""
from pathlib import Path
import importlib.util,hashlib,json
import numpy as np
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parents[1]/'nitrogen_regenerator_20261021/vector_kernel/kernel.py'
_spec=importlib.util.spec_from_file_location('_pinned_source_kernel',BASE)
_mod=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_mod)

class ThermoKernel(_mod.Kernel):
 def __init__(self,cache_dir=ROOT,verify=True):
  m=json.loads((Path(cache_dir)/'manifest.json').read_text())
  if verify and hashlib.sha256(BASE.read_bytes()).hexdigest()!=m['base_kernel_sha256']:raise ValueError('Immutable base kernel source hash mismatch')
  super().__init__(cache_dir,verify)
  self.pmin,self.pmax=m['pressure_domain_Pa']
 def _state(self,T,Y,P,strict):
  # Reuse shape, composition and T checks without changing standard reference P0.
  tt,yy,_,diag=super()._state(T,Y,self.P0,strict)
  pp=np.broadcast_to(np.asarray(P,dtype=float),tt.shape)
  if not np.isfinite(pp).all() or np.any((pp<self.pmin)|(pp>self.pmax)):
   raise ValueError(f'Pressure outside explicit {self.pmin}–{self.pmax} Pa domain')
  return tt,yy,pp,diag
 def evaluate(self,T,Y,P=101325.,strict=False,return_rates=False):
  r=super().evaluate(T,Y,P,strict,return_rates)
  Rmix=self.R*np.sum(r['Y']/self.W[:,None],axis=0)
  r['Rmix']=Rmix;r['cv']=r['cp']-Rmix
  r['e_species']=r['h_species']-self.R*r['T']/self.W[:,None]
  r['internal_energy']=np.sum(r['Y']*r['e_species'],axis=0)
  if np.any(r['cv']<=0):raise FloatingPointError('Nonpositive cv')
  return r
 def temperature_from_internal_energy(self,e,Y,T_guess=None,strict=False,trial_clamp=False,atol=1e-6,rtol=2e-13,max_iter=80):
  if (not np.isscalar(atol) or not np.isscalar(rtol) or not np.isfinite(atol) or not np.isfinite(rtol) or min(atol,rtol)<0):raise ValueError('Tolerances must be finite nonnegative scalars')
  if isinstance(max_iter,(bool,np.bool_)) or not isinstance(max_iter,(int,np.integer)) or max_iter<1:raise ValueError('max_iter must be a positive integer')
  if strict and trial_clamp:raise ValueError('Strict accepted states cannot clamp energy')
  e=np.asarray(e,dtype=float)
  if e.ndim>1 or not e.size or not np.isfinite(e).all():raise ValueError('Energy must be finite nonempty scalar/1D')
  e=np.atleast_1d(e);yy=np.asarray(Y,dtype=float);n=max(e.size,yy.shape[1] if yy.ndim==2 else 1);e=np.broadcast_to(e,(n,))
  _,Y,_,diag=self._state(np.full(n,300.),Y,self.P0,strict)
  Rmix=self.R*np.sum(Y/self.W[:,None],axis=0)
  def thermo(T):
   cp,h,_=self.thermochemistry(T);cv=np.sum(Y*cp*self.R/self.W[:,None],axis=0)-Rmix
   ee=np.sum(Y*h*(self.R*T)/self.W[:,None],axis=0)-Rmix*T
   if np.any(cv<=0):raise FloatingPointError('Nonpositive cv in inversion')
   return ee,cv
  lo=np.full(n,200.);hi=np.full(n,3500.);elo,_=thermo(lo);ehi,_=thermo(hi)
  domtol=32*np.finfo(float).eps*np.maximum(1,np.abs(e));outside=(e<elo-domtol)|(e>ehi+domtol)
  if np.any(outside) and not trial_clamp:raise ValueError('Energy outside200–3500K domain; explicit nonstrict trial_clamp needed')
  target=np.clip(e,elo,ehi);tol=atol+rtol*np.maximum(1,np.abs(e))
  if not np.isfinite(tol).all():raise ValueError('Residual tolerance overflow')
  if T_guess is None:T=lo+(hi-lo)*(target-elo)/(ehi-elo)
  else:
   T=np.broadcast_to(np.asarray(T_guess,dtype=float),(n,)).copy()
   if not np.isfinite(T).all():raise ValueError('Nonfinite temperature guess')
   T=np.clip(T,lo,hi)
  done=np.zeros(n,dtype=bool);iterations=np.zeros(n,dtype=int)
  for _ in range(max_iter):
   ee,cv=thermo(T);res=ee-target;iterations[~done]+=1;done|=abs(res)<=tol
   if done.all():break
   lo=np.where((res<0)&~done,T,lo);hi=np.where((res>=0)&~done,T,hi)
   trial=T-res/cv;safe=np.isfinite(trial)&(trial>lo)&(trial<hi);trial=np.where(safe,trial,.5*(lo+hi));T=np.where(done,T,trial)
  else:raise RuntimeError('Internal energy inversion failed tolerance; no state returned')
  diag.update(energy_clamped=outside,energy_target_original=e,energy_target_effective=target,energy_residual_original_J_kg=res+target-e,energy_residual_effective_J_kg=res,energy_iterations=iterations)
  return {'T':T,'Y':Y,'diagnostics':diag}
 def evaluate_ey(self,e,Y,P=101325.,T_guess=None,strict=False,trial_clamp=False,return_rates=False):
  a=self.temperature_from_internal_energy(e,Y,T_guess,strict,trial_clamp)
  r=self.evaluate(a['T'],a['Y'],P,strict=True,return_rates=return_rates);r['diagnostics'].update(a['diagnostics']);return r
 def evaluate_rho_u(self,rho,U,Y,T_guess=None,strict=False,trial_clamp=False,return_rates=False):
  rho,U=np.broadcast_arrays(np.atleast_1d(np.asarray(rho,dtype=float)),np.atleast_1d(np.asarray(U,dtype=float)))
  if rho.ndim!=1 or not rho.size or not np.isfinite(rho).all() or np.any(rho<=0) or not np.isfinite(U).all():raise ValueError('rho must be positive finite; U finite; scalar/1D arrays')
  a=self.temperature_from_internal_energy(U/rho,Y,T_guess,strict,trial_clamp)
  P=rho*self.R*np.sum(a['Y']/self.W[:,None],axis=0)*a['T']
  r=self.evaluate(a['T'],a['Y'],P,strict=True,return_rates=return_rates);r['pressure']=P;r['diagnostics'].update(a['diagnostics']);return r
