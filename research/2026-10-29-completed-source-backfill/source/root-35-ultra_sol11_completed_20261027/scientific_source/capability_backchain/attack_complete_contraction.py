"""Constructive full-state variational attack on qutrit conditional SDPI.

Uses exact analytic gradients of the ordinary matrix-log objective, rather
than treating random samples as a universal bound. Output proposals are
finite floating diagnostics, retained for later exact/interval refinement.
"""
import numpy as np
from scipy.optimize import minimize
from pathlib import Path
import json,time
HERE=Path(__file__).resolve().parent;OUT=HERE/'outputs';OUT.mkdir(exist_ok=True)
def trace_a(X,r):return np.einsum('ibic->bc',X.reshape(3,r,3,r))
def N(X,r):return (np.kron(np.eye(3),trace_a(X,r))-X.reshape(3,r,3,r).transpose(2,1,0,3).reshape(3*r,3*r))/2
def E(X,r):return np.kron(np.eye(3)/3,trace_a(X,r))
def flog(X):
 x,U=np.linalg.eigh(X);assert x.min()>0
 logs=np.log(x)
 return float(x@logs),(U*logs)@U.conj().T
def unpack(x,d,k):return x[:d*k].reshape(d,k)+1j*x[d*k:].reshape(d,k)
def pack(A):return np.concatenate([A.real.ravel(),A.imag.ravel()])
def evaluate(x,r,k,eps=1e-11,gradient=True):
 d=3*r;A=unpack(x,d,k);X=A@A.conj().T+eps*np.eye(d);t=float(np.trace(X).real);rho=X/t
 sigma=E(rho,r);tau=N(rho,r)
 fr,lr=flog(rho);fs,ls=flog(sigma);fn,ln=flog(tau)
 den=fr-fs;num=fn-fs
 if den<1e-12:return 0.,np.zeros_like(x)
 R=num/den
 Gu=N(ln,r)-E(ls,r);Gv=lr-E(ls,r)
 G=(Gu*den-num*Gv)/den**2
 grad=(2/t)*(G-np.trace(G@rho).real*np.eye(d))@A
 return -R,-pack(grad)
if __name__=='__main__':
 start=time.perf_counter();rng=np.random.default_rng(770415);rows=[];best=None;checks=[]
 for r in [2,3,4,6]:
  d=3*r
  for k in sorted({1,2,3,4,min(6,d),d}):
   for rep in range(4):
    A=rng.normal(size=(d,k))+1j*rng.normal(size=(d,k));A/=np.linalg.norm(A)
    if rep==0 and k==1:
     A[:]=0
     for j in range(min(3,r)):A[j*r+j,0]=1/np.sqrt(min(3,r))
    x=pack(A)
    if k==3 and rep==1:
     direction=rng.normal(size=len(x));direction/=np.linalg.norm(direction);h=1e-6
     f,g=evaluate(x,r,k);fd=(evaluate(x+h*direction,r,k)[0]-evaluate(x-h*direction,r,k)[0])/(2*h)
     checks.append({'r':r,'analytic':float(g@direction),'finite_difference':float(fd),'absolute_error':float(abs(g@direction-fd))})
    result=minimize(evaluate,x,args=(r,k),jac=True,method='L-BFGS-B',options={'maxiter':500,'ftol':1e-13,'gtol':2e-8,'maxls':40})
    row={'reference_dimension':r,'factor_rank':k,'repeat':rep,'ratio':float(-result.fun),
     'iterations':result.nit,'function_evaluations':result.nfev,'optimizer_success':bool(result.success),'message':str(result.message)}
    rows.append(row)
    if best is None or row['ratio']>best['ratio']:
     best=dict(row);best['factor_real']=unpack(result.x,d,k).real.tolist();best['factor_imag']=unpack(result.x,d,k).imag.tolist()
    if row['ratio']>.500001:print('VIOLATION_PROPOSAL',json.dumps(row),flush=True)
  print('DONE_REF',r,max(q['ratio'] for q in rows if q['reference_dimension']==r),flush=True)
 result={'status':'FINITE_VARIATIONAL_ATTACK; no universal theorem or certified counterexample',
  'objective':'D((W3 tensor id)rho || E rho)/D(rho || E rho)',
  'input':'all complex factor entries varied; rho=(AA*+eps I)/trace, eps=1e-11',
  'gradient_checks':checks,'runs':rows,'best':best,'elapsed_seconds':time.perf_counter()-start}
 (OUT/'COMPLETE_CONTRACTION_ATTACK.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['runs','best']}|{'best':{k:v for k,v in best.items() if not k.startswith('factor_')}},indent=2))
