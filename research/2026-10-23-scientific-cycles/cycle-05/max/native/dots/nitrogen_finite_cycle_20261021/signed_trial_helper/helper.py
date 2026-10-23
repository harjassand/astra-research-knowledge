"""Newton-trial signed continuation; NOT an accepted-state positivity policy."""
from pathlib import Path
import importlib.util, hashlib
import numpy as np
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/'thermo_helper/helper.py'
SOURCE_SHA256='5753a5fec7dc209a202be6ca1ba6c24a48c06cd070fb1f199886361db08af29b'
sp=importlib.util.spec_from_file_location('_continuous_thermo',SOURCE)
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
class SignedTrialKernel(m.ThermoKernel):
 def __init__(self,cache_dir=SOURCE.parent,verify=True):
  if verify and hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA256:raise ValueError('Thermo source changed')
  super().__init__(cache_dir,verify)
  bounds=[]
  for row in self.nasa:
   vals=[]
   for a,l,h in [(row[8:15],200.,1000.),(row[1:8],1000.,3500.)]:
    rr=np.polynomial.polynomial.polyroots(np.arange(1,5)*a[1:5])
    ts=[l,h]+[r.real for r in rr if abs(r.imag)<1e-8 and l<r.real<h]
    vals.extend(np.polynomial.polynomial.polyval(ts,a[:5])-1)
   bounds.append([min(vals),max(vals)])
  self.cv_bounds=np.array(bounds)*self.R/self.W[:,None]
 def _signed_state(self,T,Y,P,strict):
  T=np.atleast_1d(np.asarray(T,float));Y=np.asarray(Y,float)
  if Y.ndim==1:Y=Y[:,None]
  if T.ndim!=1 or Y.ndim!=2 or Y.shape[0]!=6:raise ValueError('Invalid species-first shape')
  n=max(T.size,Y.shape[1]);T=np.broadcast_to(T,(n,));Y=np.broadcast_to(Y,(6,n))
  if not np.isfinite(Y).all() or not np.isfinite(T).all():raise ValueError('Nonfinite trial')
  neg=-np.minimum(Y,0).sum(axis=0)
  if np.any(neg>1e-3) or (strict and np.any(neg>0)):raise ValueError('Negative trial mass exceeds allowance (strict allows none)')
  if np.any(abs(Y.sum(axis=0)-1)>1e-12):raise ValueError('Signed Y must sum to one; no renormalization')
  if np.any((T<200)|(T>3500)):raise ValueError('Temperature outside domain')
  lower=(np.maximum(Y,0)*self.cv_bounds[:,0,None]+np.minimum(Y,0)*self.cv_bounds[:,1,None]).sum(axis=0)
  if np.any(lower<=0) or np.any((Y/self.W[:,None]).sum(axis=0)<=0):raise ValueError('Nonmonotone signed thermo or Rmix')
  return T,Y,P,dict(raw_min_Y=Y.min(axis=0),raw_sum_Y=Y.sum(axis=0),negative_input=neg>0,negative_mass_fraction=neg,normalization_max_change=np.zeros(n),signed_cv_global_lower_bound_J_kg_K=lower,trial_only_signed_extension=neg>0)
 def signed_rates(self,T,C):
  T=np.atleast_1d(T);C=np.asarray(C);cp,h,s=self.thermochemistry(T)
  lk=-self.nu.T@(h-s)+self.delta_nu[:,None]*np.log(self.P0/(self.R*T))
  A=self.A;lt=np.log(T)
  k=np.stack([np.log(5e-14*A)-113200/T+np.log(-np.expm1(-3354/T)),np.log(3.7e-14*A)-59380/T+np.log(-np.expm1(-2238/T)),np.log(3e-16*A)-38000/T,np.log(9.7e-21*A)+1.01*lt-3120/T,np.log(2.4e-15*A)-74700/T,np.log(4.9e-16*A)-.4*lt,np.log(5.5e-18*A)+188/T])
  third=self.third_body_efficiencies@C
  if np.any(third<=0):raise ValueError('Nonpositive signed third-body concentration')
  k[0]+=np.log(third[0]);k[1]+=np.log(third[1]);k[4]+=np.log(third[2])
  pr=np.log(9.2e-40*A*A)-1.6*lt+np.log(third[2])-k[5];k[5]-=np.logaddexp(0,-pr)
  # Exact integer monomial structure, represented with signed log magnitudes.
  # This retains expm1 cancellation without changing any negative concentration.
  with np.errstate(divide='ignore'):lc=np.log(abs(C))
  lm_f=np.stack([lc[0],lc[1],lc[0]+lc[3],lc[1]+lc[2],lc[4],lc[4]+lc[3],lc[5]+lc[3]])
  lm_r=np.stack([2*lc[2],2*lc[3],lc[4]+lc[2],lc[4]+lc[3],lc[2]+lc[3],lc[5],lc[4]+lc[1]])
  sg=np.sign(C)
  sf=np.stack([sg[0],sg[1],sg[0]*sg[3],sg[1]*sg[2],sg[4],sg[4]*sg[3],sg[5]*sg[3]])
  sr=np.stack([sg[2]**2,sg[3]**2,sg[4]*sg[2],sg[4]*sg[3],sg[2]*sg[3],sg[5],sg[4]*sg[1]])
  lf=k+lm_f;lr=k-lk+lm_r;f=sf*np.exp(lf);r=sr*np.exp(lr);net=f-r
  same=(sf==sr)&(sf!=0);pos=same&(lf>lr);neg=same&(lf<lr);equal=same&(lf==lr)
  net[pos]=sf[pos]*np.exp(lf[pos])*(-np.expm1(lr[pos]-lf[pos]));net[neg]=-sf[neg]*np.exp(lr[neg])*(-np.expm1(lf[neg]-lr[neg]));net[equal]=0
  return net,f,r,lk
 def temperature_from_internal_energy(self,e,Y,T_guess=None,strict=False,trial_clamp=False,atol=1e-6,rtol=2e-13,max_iter=80):
  if (not np.isscalar(atol) or not np.isscalar(rtol) or not np.isfinite(atol) or not np.isfinite(rtol) or min(atol,rtol)<0):raise ValueError('Tolerances must be finite nonnegative scalars')
  if isinstance(max_iter,(bool,np.bool_)) or not isinstance(max_iter,(int,np.integer)) or max_iter<1:raise ValueError('max_iter must be a positive integer')
  if strict and trial_clamp:raise ValueError('Strict accepted states cannot clamp energy')
  e=np.asarray(e,dtype=float)
  if e.ndim>1 or not e.size or not np.isfinite(e).all():raise ValueError('Energy must be finite nonempty scalar/1D')
  e=np.atleast_1d(e);yy=np.asarray(Y,dtype=float);n=max(e.size,yy.shape[1] if yy.ndim==2 else 1);e=np.broadcast_to(e,(n,))
  _,Y,_,diag=self._signed_state(np.full(n,300.),Y,self.P0,strict)
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
  T=np.clip(T,lo,hi)
  done=np.zeros(n,dtype=bool);iterations=np.zeros(n,dtype=int)
  for _ in range(max_iter):
   ee,cv=thermo(T);res=ee-target;iterations[~done]+=1;done|=abs(res)<=tol
   if done.all():break
   lo=np.where((res<0)&~done,T,lo);hi=np.where((res>=0)&~done,T,hi)
   trial=T-res/cv;safe=np.isfinite(trial)&(trial>lo)&(trial<hi);trial=np.where(safe,trial,.5*(lo+hi));T=np.where(done,T,trial)
  else:raise RuntimeError('Internal energy inversion failed tolerance; no state returned')
  diag={key:value for key,value in diag.items() if not key.startswith('pressure_')}
  diag.update(energy_clamped=outside,energy_target_original=e,energy_target_effective=target,energy_residual_original_J_kg=res+target-e,energy_residual_effective_J_kg=res,energy_iterations=iterations)
  return {'T':T,'Y':Y,'diagnostics':diag}
 def evaluate_rho_u(self,rho,U,Y,T_guess=None,strict=False,trial_clamp=False,return_rates=False):
  rho,U=np.broadcast_arrays(np.atleast_1d(np.asarray(rho,float)),np.atleast_1d(np.asarray(U,float)))
  if rho.ndim!=1 or not rho.size or not np.isfinite(rho).all() or np.any(rho<=0) or not np.isfinite(U).all():raise ValueError('Invalid conservative rho/U')
  a=self.temperature_from_internal_energy(U/rho,Y,T_guess,strict,trial_clamp)
  T,Y=a['T'],a['Y'];rho=np.broadcast_to(rho,T.shape);U=np.broadcast_to(U,T.shape)
  Rmix=self.R*np.sum(Y/self.W[:,None],axis=0);P=rho*Rmix*T
  # Inherited evaluator provides ONLY transport; all thermo/rate fields replaced.
  yp=np.maximum(Y,0);yp/=yp.sum(axis=0)
  r=super().evaluate(T,yp,P,strict=True,return_rates=False)
  diag=r['diagnostics'];diag.update(a['diagnostics']);diag.update(transport_clipped_mixture=np.any(Y<0,axis=0),transport_composition_max_change=np.max(abs(yp-Y),axis=0),pressure_eos_Pa=P)
  cpR,h,s=self.thermochemistry(T);hs=h*self.R*T/self.W[:,None];cps=cpR*self.R/self.W[:,None];es=hs-self.R*T/self.W[:,None]
  net,f,rev,lk=self.signed_rates(T,rho*Y/self.W[:,None])
  e=(Y*es).sum(axis=0);cp=(Y*cps).sum(axis=0)
  r.update(T=T,Y=Y,X=(Y/self.W[:,None])/(Y/self.W[:,None]).sum(axis=0),rho=rho,rho_input=rho,pressure=P,Rmix=Rmix,cp=cp,cv=cp-Rmix,h_species=hs,e_species=es,enthalpy=(Y*hs).sum(axis=0),internal_energy=e,internal_energy_density_input=U,conservative_energy_residual_J_m3=rho*e-U,mass_production=(self.nu@net)*self.W[:,None],diagnostics=diag)
  if return_rates:r.update(net_rates_of_progress=net,forward_rates_of_progress=f,reverse_rates_of_progress=rev,log_Kc=lk,cp_species=cps,h_RT=h,s_R=s)
  if any(not np.isfinite(v).all() for v in r.values() if isinstance(v,np.ndarray)):raise FloatingPointError('Nonfinite signed evaluator result')
  return r
