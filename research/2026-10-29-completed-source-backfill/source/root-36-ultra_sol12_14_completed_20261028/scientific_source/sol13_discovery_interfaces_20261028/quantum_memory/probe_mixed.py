"""Direct matrix-weight diagnostic, including mixed memory weights."""
from probe_memory import OUT,U,flog
import numpy as np
from scipy.optimize import minimize
import json,time
S=np.einsum('ai,bi->iab',U,U.conj())
def unpack(z,r):
 n=9*r*r;return z[:n].reshape(9,r,r)+1j*z[n:].reshape(9,r,r)
def objective(z,r):
 t=unpack(z,r);normal=np.sum(abs(t)**2);aa=np.einsum('iab,icb->iac',t,t.conj())/normal
 c=aa.sum(axis=0);m=np.einsum('iab,icd->acbd',S,aa).reshape(3*r,3*r)
 fc,lc=flog(c);fm,lm=flog(m);values=[];grads=[];lm=lm.reshape(3,r,3,r)
 for si,ai in zip(S,aa):
  fi,li=flog(ai);values.append(fi)
  adj=np.einsum('ab,biaj->ij',si,lm)
  grads.append(li+lc-2*adj)
 value=sum(values)+fc-2*fm;grads=np.array(grads)
 alpha=np.real(sum(np.trace(g@a) for g,a in zip(grads,aa)))
 gt=2*np.einsum('iab,ibc->iac',grads-alpha*np.eye(r),t)/normal
 return float(value),np.r_[gt.real.ravel(),gt.imag.ravel()]
def run():
 start=time.perf_counter();rng=np.random.default_rng(2026102801);records=[];best=(1,None,None)
 for r in [2,3,4]:
  for seed in range(12):
   t=rng.normal(size=(9,r,r))+1j*rng.normal(size=(9,r,r));t/=np.linalg.norm(t);z=np.r_[t.real.ravel(),t.imag.ravel()]
   if seed==0:
    v=rng.normal(size=z.size);e=1e-6;fd=(objective(z+e*v,r)[0]-objective(z-e*v,r)[0])/(2*e);_,gg=objective(z,r);assert abs(fd-gg@v)<1e-6
   opt=minimize(objective,z,args=(r,),jac=True,method='L-BFGS-B',options={'maxiter':400,'ftol':1e-12,'gtol':1e-8})
   val,_=objective(opt.x,r);records.append({'r':r,'seed':seed,'value':val,'iterations':opt.nit,'optimizer_success':bool(opt.success)})
   if val<best[0]:best=(val,r,opt.x.copy())
   if val<-1e-5:break
  if best[0]<-1e-5:break
 np.savez(OUT/'MIXED_PROBE_BEST.npz',rank=best[1],T=unpack(best[2],best[1]))
 result={'scope':'diagnostic only; direct PSD matrix weights A_i=T_iT_i*/trace','best_value':best[0],'best_memory_dimension':best[1],'runs':records,'seconds':time.perf_counter()-start}
 (OUT/'MIXED_PROBE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='runs'},indent=2))
if __name__=='__main__':run()
