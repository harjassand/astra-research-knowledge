import numpy as np,json
from numpy.random import default_rng
rng=default_rng(10100522)
def stats(A):
 n=A.shape[0];r=A.sum(1)[0];P=A/r
 M=P.T-np.eye(n);M[-1,:]=1;b=np.zeros(n);b[-1]=1
 try:pi=np.linalg.solve(M,b)
 except np.linalg.LinAlgError:return None
 if pi.min()<1e-9:return None
 B=(A@A>0)&(A==0);np.fill_diagonal(B,False);d2=B.sum(1); din=A.sum(0)
 return pi,d2,din
best={};fail=[]
for n,r in [(9,2),(13,3),(17,4),(21,5),(25,6),(31,7),(37,9),(41,10),(51,12)]:
 A=np.zeros((n,n),dtype=np.int64)
 for i in range(n):A[i,(i+np.arange(1,r+1))%n]=1
 nacc=0;mn=9.;mnmax=999
 for it in range(80000):
  u=rng.integers(n);old=rng.choice(np.flatnonzero(A[u]));v=rng.integers(n)
  if u==v or A[u,v] or A[v,u] or np.dot(A[v],A[:,u]):continue
  A[u,old]=0;A[u,v]=1;nacc+=1
  if nacc%10:continue
  out=stats(A)
  if out is None:A[u,old]=1;A[u,v]=0;continue
  pi,d2,din=out; val=float(pi@d2/r); top=np.flatnonzero(pi>=max(pi)-1e-10); topval=int(d2[top].max())
  mn=min(mn,val);mnmax=min(mnmax,topval)
  if val<1-1e-9 or topval<r:
   row={'n':n,'r':r,'weighted_ratio':val,'maxpi_d2':topval,'pi':pi.tolist(),'d2':d2.tolist(),'din':din.tolist(),'A':A.tolist(),'iteration':it}
   fail.append(row);print('FAIL',n,r,val,topval,'weighted_din',float(pi@din),flush=True)
   if val<1-1e-9:break
 print('DONE',n,r,'accepted',nacc,'minweighted',mn,'minmaxpi',mnmax,flush=True)
 best[str((n,r))]={'accepted':nacc,'minweighted':mn,'minmaxpi':mnmax}
 if len(fail)>100:break
json.dump({'best':best,'failures':fail},open('independent_programme/deep_theory_20261010/stationary_probe.json','w'),indent=2)
