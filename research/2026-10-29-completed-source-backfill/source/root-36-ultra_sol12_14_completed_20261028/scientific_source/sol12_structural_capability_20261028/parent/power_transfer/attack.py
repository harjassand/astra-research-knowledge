"""Bounded constructive screen of an entropy-generating trace-power route.
Floating proposals only. Negative values would require rational certification.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
os.environ.setdefault('OMP_NUM_THREADS','1')
import json,time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
OUT=Path(__file__).resolve().parent
def E(x,d):
 r=np.einsum('iaib->ab',x.reshape(3,d,3,d))
 return np.kron(np.eye(3)/3,r)
def N(x,d):return (3*E(x,d)-x.reshape(3,d,3,d).transpose(2,1,0,3).reshape(3*d,3*d))/2
def tracepower(x,p,derivative=False):
 lam,u=np.linalg.eigh((x+x.T)/2);lam=np.maximum(lam,0)
 if derivative:return (u*(p*lam**(p-1)))@u.T
 return float(np.sum(lam**p))
def objective(v,d,p):
 n=3*d;g=v.reshape(n,n);z=g@g.T;t=np.trace(z);x=z/t;tau=E(x,d);y=N(x,d)
 f=tracepower(x,p)+tracepower(tau,p)-2*tracepower(y,p)
 h=tracepower(x,p,True)+E(tracepower(tau,p,True),d)-2*N(tracepower(y,p,True),d)
 grad=2*(h-np.sum(h*x)*np.eye(n))@g/t
 return f,grad.ravel()
def entropy(x):
 lam=np.linalg.eigvalsh((x+x.T)/2);lam=lam[lam>1e-14]
 return float(np.sum(lam*np.log(lam)))
def main():
 start=time.perf_counter();rng=np.random.default_rng(920311);rows=[];best=None
 for d in [2,3,4]:
  n=3*d
  for p in [1.05,1.25,1.5,1.75]:
   for seed in range(3):
    g=rng.normal(size=(n,n))
    result=minimize(objective,g.ravel(),args=(d,p),jac=True,method='L-BFGS-B',options={'maxiter':350,'ftol':1e-14,'gtol':1e-9})
    z=result.x.reshape(n,n);x=z@z.T;x/=np.trace(x);tau=E(x,d);y=N(x,d)
    row={'reference_dimension':d,'p':p,'seed':seed,'score':float(result.fun),'iterations':int(result.nit),'evaluations':int(result.nfev),'numeric_Delta':entropy(x)+entropy(tau)-2*entropy(y),'status':str(result.message)}
    rows.append(row)
    if best is None or row['score']<best['row']['score']:best={'row':row,'G':z.tolist(),'rho':x.tolist()}
    if row['score'] < -1e-8:print(json.dumps({'negative_proposal':row}),flush=True)
 out={'status':'BOUNDED_NUMERIC_TRACE_POWER_SCREEN','rows':rows,'best_proposal':best,'seconds_including_proposals':time.perf_counter()-start,'scope':'36 deterministic real-matrix starts, dimension≤12. No global inequality proof, certified sign, or method advantage. Trace-power positivity for p down to1 would imply entropy target; finite p tests do not.'}
 (OUT/'SCREEN.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':out['status'],'minimum_score':min(r['score'] for r in rows),'seconds':out['seconds_including_proposals']},indent=2))
if __name__=='__main__':main()
