"""Two-site diagnostic only: absorbing-overflow finite-state projection.
Matrix-exponential result is floating point, not interval certified. The analytic
FSP bound is hit_mass <= exact_hit_probability <= hit_mass + overflow_mass.
"""
import json,sys,time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import expm_multiply
from kinetics import C1,C2,C3,C4,D
cap=int(sys.argv[1]) if len(sys.argv)>1 else 100
T=float(sys.argv[2]) if len(sys.argv)>2 else 1.
t0=time.perf_counter(); ids={}
for a in range(cap+1):
 for b in range(cap+1):
  if max(a,b)>15: ids[a,b]=len(ids)
B=len(ids);O=B+1;n=O+1
rr=[];cc=[];vv=[]
for x,i in ids.items():
 total=0.
 transitions=[]
 for j in range(2):
  a=x[j];y=list(x);y[j]+=1
  transitions.append((tuple(y),C1*a*(a-1)+C3))
  if a:
   y=list(x);y[j]-=1
   transitions.append((tuple(y),C2*a*(a-1)*(a-2)+C4*a))
  if a:
   y=list(x);y[j]-=1;y[1-j]+=1
   transitions.append((tuple(y),D*a))
 for y,r in transitions:
  if max(y)>cap: dest=O
  elif max(y)<=15:dest=B
  else:dest=ids[y]
  rr.append(dest);cc.append(i);vv.append(r);total+=r
 rr.append(i);cc.append(i);vv.append(-total)
A=coo_matrix((vv,(rr,cc)),shape=(n,n)).tocsr()
p0=np.zeros(n);p0[ids[50,50]]=1
build=time.perf_counter()-t0; t1=time.perf_counter()
p=expm_multiply(A*T,p0,traceA=T*sum(A.diagonal()))
res=dict(cap=cap,T=T,n=n,nnz=A.nnz,hit_mass=float(p[B]),overflow_mass=float(p[O]),
 mass_sum=float(p.sum()),min_mass=float(p.min()),build_seconds=build,
 expm_seconds=time.perf_counter()-t1)
open(f'fsp_cap{cap}_T{T}.json','w').write(json.dumps(res,indent=2));print(json.dumps(res),flush=True)
