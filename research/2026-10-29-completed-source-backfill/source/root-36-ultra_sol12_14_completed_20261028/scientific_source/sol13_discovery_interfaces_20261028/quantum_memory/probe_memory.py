"""Bounded falsification probe for the actual matrix-weight SIC target."""
from pathlib import Path
import json,time
import numpy as np
from scipy.optimize import minimize
OUT=Path(__file__).resolve().parent/'outputs';OUT.mkdir(exist_ok=True)
w=np.exp(2j*np.pi/3);U=np.zeros((3,9),complex)
for a in range(3):
 for b in range(3):U[(a+1)%3,3*a+b]=1/np.sqrt(2);U[(a+2)%3,3*a+b]=-w**(-b)/np.sqrt(2)
G=U.conj().T@U
def flog(a):
 ev,V=np.linalg.eigh((a+a.conj().T)/2);positive=ev>1e-13
 return np.sum(ev[positive]*np.log(ev[positive])),(V[:,positive]*np.log(ev[positive]))@V[:,positive].conj().T
def target_t(t,gradient=False):
 tr=np.sum(abs(t)**2);rho=t@t.conj().T/tr;p=np.real(np.diag(rho));out=G*rho
 fi,li=flog(rho);fo,lo=flog(out);fd=np.sum(p*np.log(p));value=fi+fd-2*fo
 if not gradient:return float(value)
 A=li+np.diag(np.log(p))-2*G.conj()*lo;A=(A+A.conj().T)/2
 grad=2*(A@t-np.real(np.trace(A@rho))*t)/tr
 return float(value),grad
def unpack(z,r):return z[:9*r].reshape(9,r)+1j*z[9*r:].reshape(9,r)
def objective(z,r):
 val,grad=target_t(unpack(z,r),True)
 return val,np.r_[grad.real.ravel(),grad.imag.ravel()]
def run():
 start=time.perf_counter();rng=np.random.default_rng(20261028);controls={}
 controls['A_i_S_i_over9']=target_t(U.conj().T/3)
 controls['A_i_transpose_S_i_over9']=target_t(U.T/3)
 controls['orthogonal_A_i']=target_t(np.eye(9)/3)
 assert abs(controls['A_i_S_i_over9']-np.log(4/3))<1e-12
 assert abs(controls['A_i_transpose_S_i_over9']-(8*np.log(2)/3-np.log(3)))<1e-12
 t=rng.normal(size=(9,2))+1j*rng.normal(size=(9,2));z=np.r_[t.real.ravel(),t.imag.ravel()]
 v=rng.normal(size=z.size);eps=1e-6;fd=(objective(z+eps*v,2)[0]-objective(z-eps*v,2)[0])/(2*eps)
 _,grad=objective(z,2);assert abs(fd-grad@v)<1e-7
 records=[];best=(1,None,None)
 for r in [2,3,4,9]:
  for seed in range(16):
   t=rng.normal(size=(9,r))+1j*rng.normal(size=(9,r));t/=np.linalg.norm(t)
   z=np.r_[t.real.ravel(),t.imag.ravel()]
   opt=minimize(objective,z,args=(r,),jac=True,method='L-BFGS-B',options={'maxiter':400,'ftol':1e-12,'gtol':1e-8})
   value=target_t(unpack(opt.x,r));records.append({'rank':r,'seed':seed,'value':value,'iterations':opt.nit,'optimizer_success':bool(opt.success)})
   if value<best[0]:best=(value,r,opt.x.copy())
   if value<-1e-5:break
  if best[0]<-1e-5:break
 np.savez(OUT/'MEMORY_PROBE_BEST.npz',rank=best[1],T=unpack(best[2],best[1]),G=G)
 result={'scope':'diagnostic only; rank-one memory weights via Gram Schur map','controls':controls,'gradient_fd_error':float(abs(fd-grad@v)),'best_value':best[0],'best_rank':best[1],'runs':records,'seconds':time.perf_counter()-start}
 (OUT/'MEMORY_PROBE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='runs'},indent=2))
if __name__=='__main__':run()
