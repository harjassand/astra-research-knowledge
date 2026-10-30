"""Numerical search on actual general three-wave periodic gradients.

Spatial vectors and all three output polarizations vary freely. Exact
triad moment formulae remove all discretization and FFT aliasing. These
numerical searches certify neither universal safety nor a separation.
Any negative candidate needs rational field and global ROC replay.
"""
from pathlib import Path
from fractions import Fraction as R
from math import factorial
from itertools import product,combinations
import json,sys,time
import numpy as np
from scipy.optimize import minimize
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'work'));import heat_model as h
start=time.perf_counter();F4=np.zeros((4,)*4);C3=np.zeros((4,)*3)
for shape,P in ((F4,h.F),(C3,h.C)):
 n=shape.ndim
 for ids in product(range(4),repeat=n):
  pw=tuple(ids.count(i) for i in range(4));shape[ids]=float(P.get(pw,0))*np.prod([factorial(q) for q in pw])/factorial(n)
NU=1859.
def evaluate(x,full=False):
 kv=x[:4].reshape(2,2);uv=x[4:].reshape(3,2);kv=kv/np.sqrt(np.sum(kv*kv));uv=uv/np.sqrt(np.sum(uv*uv));freq=np.vstack((kv,kv[0]+kv[1]));rr=np.einsum('si,sj->sij',uv,freq).reshape(3,4)
 HR=12*np.einsum('ijkl,sk,sl->sij',F4,rr,rr);H=np.sum(HR,axis=0)/2;fr=np.einsum('ijkl,si,sj,sk,sl->s',F4,rr,rr,rr,rr);f=3*np.sum(fr)/8+sum(np.einsum('i,ij,j',rr[j],HR[i],rr[j]) for i,j in combinations(range(3),2))/8
 v=6*np.einsum('ijkl,j,k,l->i',F4,*rr);c=1.5*np.einsum('ijk,i,j,k',C3,*rr);w=1.5*np.einsum('ijk,sj,sk->i',C3,rr,rr);s=np.sum(rr*rr)/2;hv=np.linalg.solve(H,v);hw=np.linalg.solve(H,w);a=2*f-v@hv;b=2*NU*s-w@hw;r=c-v@hw;ratio=r*r/(a*b)
 if full:return {'ratio':float(np.real(ratio)),'a':float(np.real(a)),'b':float(np.real(b)),'r':float(np.real(r)),'f':float(np.real(f)),'H_condition':float(np.linalg.cond(H)),'spatial_vectors':np.real(kv).tolist(),'output_vectors':np.real(uv).tolist(),'ray_directions':np.real(rr).tolist(),'spatial_determinant':float(np.real(np.linalg.det(kv)))}
 return ratio
def fun(x):
 try:
  v=float(np.real(evaluate(x)))
  return -v if np.isfinite(v) else 1e6
 except np.linalg.LinAlgError:return 1e6
def jac(x):
 dx=1e-20;out=[]
 for i in range(len(x)):
  xx=x.astype(complex);xx[i]+=1j*dx
  try:out.append(-float(np.imag(evaluate(xx)))/dx)
  except np.linalg.LinAlgError:out.append(0.)
 return np.array(out)
rng=np.random.default_rng(20261031);best=[];runs=[]
qc=json.loads((root/'outputs/quadratic_boundary/certificate.json').read_text());ur=np.array(list(map(R,qc['lower_rank_one_output'])),float);nr=np.array(list(map(R,qc['lower_rank_one_spatial'])),float);nr/=np.linalg.norm(nr);ur/=np.linalg.norm(ur);per=np.array([-nr[1],nr[0]])
starts=[rng.normal(size=10) for _ in range(64)]
for eps in (.01,.05,.2,.5,1.):
 for j in range(4):
  kv=np.vstack((nr, rng.uniform(.3,1.7)*nr+eps*per));uv=np.vstack((ur+.2*rng.normal(size=2),ur+.2*rng.normal(size=2),eps*rng.normal(size=2)));starts.append(np.concatenate((kv.ravel(),uv.ravel())))
for i,x in enumerate(starts):
 result=minimize(fun,x,jac=jac,method='BFGS',options={'gtol':1e-8,'maxiter':350});d=evaluate(result.x,True);d.update({'run':i,'parameters':result.x.tolist(),'iterations':result.nit,'success':bool(result.success)});runs.append(d)
 if d['a']>0 and d['b']>0 and d['H_condition']<1e12:
  best.append(d);best.sort(key=lambda q:q['ratio'],reverse=True);best=best[:12]
 if i%8==0:print(json.dumps({'completed':i+1,'total':len(starts),'best_ratio':best[0]['ratio'] if best else None,'seconds':time.perf_counter()-start}),flush=True)
 out={'scope':'Finite numerical search of general actual three-wave fields. No all-fields or all-triads theorem. Any ratio >1 needs exact verification and fresh global ROC admission.','nu':NU,'best':best,'runs':runs,'seconds':time.perf_counter()-start};(root/'work/general_triad_search.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'completed':len(runs),'best':best[0] if best else None,'seconds':time.perf_counter()-start}),flush=True)
