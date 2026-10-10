import numpy as np,json
from pathlib import Path
rng=np.random.default_rng(171010)
for n in range(4,15):
 for trial in range(20000):
  A=np.zeros((n,n),dtype=int)
  for i in range(n):
   for j in range(i):
    z=rng.integers(3)
    if z==1:A[i,j]=1
    if z==2:A[j,i]=1
  d=A.sum(1)
  if min(d)==0:continue
  reach=A+np.eye(n,dtype=int)
  for _ in range(n):reach=((reach@reach)>0).astype(int)
  if not reach.all():continue
  P=A/d[:,None]
  B=P.T-np.eye(n);B[-1,:]=1;b=np.zeros(n);b[-1]=1
  pi=np.linalg.solve(B,b)
  sec=((A@A)>0)&(A==0)&(~np.eye(n,dtype=bool));s=sec.sum(1)
  diff=float(pi@(s-d))
  if diff < -1e-8:
   out={'n':n,'trial':trial,'A':A.tolist(),'degree':d.tolist(),'second':s.tolist(),'pi':pi.tolist(),'difference':diff,'triangles_trace':int(np.trace(A@A@A))}
   Path('independent_programme/root_stationary_neighborhood_20261010/found.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));raise SystemExit
 print(n,'passed',flush=True)
