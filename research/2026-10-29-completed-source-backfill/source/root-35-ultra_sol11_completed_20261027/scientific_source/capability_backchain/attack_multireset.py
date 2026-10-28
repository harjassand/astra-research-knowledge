"""Actual finite multireset entropy/curvature attack; diagnostics, not proof.

Qutrit physical A, reference B tensor C. Source is P_OmegaAB tensor I_C
plus I_A tensor [aI+bP_Phi0+cP_Phi1]. Both Phi have full Schmidt rank;
their rational projectors use real cyclic shift rather than complex phases.
"""
import numpy as np
from pathlib import Path
import json,time
HERE=Path(__file__).resolve().parent;OUT=HERE/'outputs';OUT.mkdir(exist_ok=True)
def trace_a(X):return np.einsum('ibic->bc',X.reshape(3,9,3,9))
def N(X):return (np.kron(np.eye(3),trace_a(X))-X.reshape(3,9,3,9).transpose(2,1,0,3).reshape(27,27))/2
def E(X):return np.kron(np.eye(3)/3,trace_a(X))
om=np.eye(3).reshape(-1);main=np.kron(np.outer(om,om),np.eye(3))
v=[]
for k in range(3):
 x=np.zeros((3,3))
 for i in range(3):x[i,(i+k)%3]=1/np.sqrt(3)
 v.append(x.ravel())
P=[np.outer(x,x) for x in v];D=np.kron(np.eye(3),P[0]-P[1])
assert np.allclose(N(main),N(main).T) and np.allclose(N(main)@N(main),N(main))
def entropy_f(X):
 x=np.linalg.eigvalsh(X);assert min(x)>-1e-9
 x=x[x>1e-14];return float(x@np.log(x))
def deficit(a,b,c):
 Y=a*np.eye(9)+b*P[0]+c*P[1];X=main+np.kron(np.eye(3),Y)
 return entropy_f(X)+entropy_f(E(X))-2*entropy_f(N(X))
def bkm(X,D):
 x,U=np.linalg.eigh(X);assert min(x)>0
 d=U.T@D@U
 l=np.log(x);dx=x[:,None]-x[None,:];dl=l[:,None]-l[None,:]
 close=np.abs(dx)<1e-7*np.maximum(x[:,None],x[None,:])
 q=np.empty_like(dx);np.divide(dl,dx,out=q,where=~close)
 q[close]=2/(x[:,None]+x[None,:])[close]
 return float(np.sum(d*d*q))
def curvature(a,b,c):
 Y=a*np.eye(9)+b*P[0]+c*P[1];X=main+np.kron(np.eye(3),Y)
 return bkm(X,D)+bkm(E(X),D)-2*bkm(N(X),D)
if __name__=='__main__':
 start=time.perf_counter();rng=np.random.default_rng(842781)
 rows=[]
 for _ in range(600):
  a,total=10**rng.uniform(-3,3,2);p=rng.uniform(.005,.995);b=total*p;c=total*(1-p)
  delta=deficit(a,b,c);curv=curvature(a,b,c)
  rows.append({'a':float(a),'b':float(b),'c':float(c),'deficit':delta,'fixed_total_split_curvature':curv})
 fixed=[]
 for a in [0,.001,.1,1,10]:
  for t in [.001,.1,1,10,100]:
   vals=[deficit(a,t*p,t*(1-p)) for p in [0,.1,.25,.5,.75,.9,1]]
   fixed.append({'a':a,'total':t,'deficits':vals})
 result={'scope':'finite numerical attack, no universal/physical claim','parameter_source':'supplied rational matrix family',
  'samples':rows,'fixed_total_controls':fixed,'min_curvature':min(rows,key=lambda z:z['fixed_total_split_curvature']),
  'max_curvature':max(rows,key=lambda z:z['fixed_total_split_curvature']),
  'minimum_normalized_deficit':min(rows,key=lambda z:z['deficit']/(9+27*z['a']+3*z['b']+3*z['c'])),
  'elapsed_seconds':time.perf_counter()-start}
 (OUT/'MULTIRESET_DIAGNOSTIC.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['samples','fixed_total_controls']},indent=2))
