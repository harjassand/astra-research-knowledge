"""Diagnostic conditional relative-entropy ratio; no proof is inferred."""
from probe_mixed import OUT,S,unpack,flog
from scipy.optimize import minimize
import numpy as np
import json,time
def objective(z,r):
 t=unpack(z,r);normal=np.sum(abs(t)**2);aa=np.einsum('iab,icb->iac',t,t.conj())/normal
 c=aa.sum(axis=0);m=np.einsum('iab,icd->acbd',S,aa).reshape(3*r,3*r)
 fc,lc=flog(c);fm,lm=flog(m);lm=lm.reshape(3,r,3,r);fis=[];lis=[];adjs=[]
 for si,ai in zip(S,aa):
  fi,li=flog(ai);fis.append(fi);lis.append(li);adjs.append(np.einsum('ab,biaj->ij',si,lm))
 din=sum(fis)-fc+np.log(9);dout=fm-fc+np.log(3)
 if din<1e-9:return 0,np.zeros_like(z)
 ratio=dout/din;grads=-np.array([ad-lc-ratio*(li-lc) for li,ad in zip(lis,adjs)])/din
 alpha=np.real(sum(np.trace(g@a) for g,a in zip(grads,aa)))
 gt=2*np.einsum('iab,ibc->iac',grads-alpha*np.eye(r),t)/normal
 return -float(ratio),np.r_[gt.real.ravel(),gt.imag.ravel()]
def run():
 start=time.perf_counter();rng=np.random.default_rng(2026102802);records=[];best=(0,None,None)
 for r in [2,3,4]:
  for seed in range(16):
   t=rng.normal(size=(9,r,r))+1j*rng.normal(size=(9,r,r));t*=np.exp(rng.normal(size=(9,1,1))*(seed%3));t/=np.linalg.norm(t);z=np.r_[t.real.ravel(),t.imag.ravel()]
   if seed==0:
    v=rng.normal(size=z.size);e=1e-6;fd=(objective(z+e*v,r)[0]-objective(z-e*v,r)[0])/(2*e);_,gg=objective(z,r);assert abs(fd-gg@v)<1e-6
   opt=minimize(objective,z,args=(r,),jac=True,method='L-BFGS-B',options={'maxiter':500,'ftol':1e-12,'gtol':1e-8})
   val,_=objective(opt.x,r);ratio=-val;records.append({'r':r,'seed':seed,'ratio':ratio,'iterations':opt.nit,'optimizer_success':bool(opt.success)})
   if ratio>best[0]:best=(ratio,r,opt.x.copy())
   if ratio>.50001:break
  if best[0]>.50001:break
 np.savez(OUT/'RATIO_PROBE_BEST.npz',rank=best[1],T=unpack(best[2],best[1]))
 result={'scope':'diagnostic only; conditional uniform-baseline ratio with reference term subtracted','best_ratio':best[0],'best_memory_dimension':best[1],'runs':records,'seconds':time.perf_counter()-start}
 (OUT/'RATIO_PROBE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='runs'},indent=2))
if __name__=='__main__':run()
