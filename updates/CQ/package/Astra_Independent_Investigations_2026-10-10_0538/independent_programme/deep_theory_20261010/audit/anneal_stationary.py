import numpy as np, random, math, json, time
from pathlib import Path
rng=random.Random(910177)
folder=Path(__file__).parent

def stats(A):
 n=len(A);r=A[0].sum(); M=A.T.astype(float)/r-np.eye(n);M[-1,:]=1;b=np.zeros(n);b[-1]=1
 try:pi=np.linalg.solve(M,b)
 except np.linalg.LinAlgError:return None
 if pi.min()<1e-10:return None
 B=((A@A)>0)&(A==0);np.fill_diagonal(B,False);s=B.sum(1)
 return float(pi@s/r),pi,s
bestall=[];start=time.monotonic()
for triangles in [False,True]:
 for r in [3,4,5,6,8,10]:
  for n in sorted(set([3*r+1,4*r+1,6*r+1])):
   for run in range(3):
    A=np.zeros((n,n),dtype=np.int64)
    for u in range(n):A[u,[(u+j)%n for j in range(1,r+1)]]=1
    val,pi,s=stats(A);best=val;bestA=A.copy();accepted=0;tested=0
    for it in range(16000):
     u=rng.randrange(n);old=int(rng.choice(np.flatnonzero(A[u])));v=rng.randrange(n)
     if u==v or A[u,v] or A[v,u] or (not triangles and np.dot(A[v],A[:,u])):continue
     A[u,old]=0;A[u,v]=1
     out=stats(A);tested+=1
     if out is None:A[u,old]=1;A[u,v]=0;continue
     nv,np_,ns=out
     temp=.12*(1-it/16000)**2+.001
     if nv<val or rng.random()<math.exp(min(0,(val-nv)/temp)):
      val,pi,s=out;accepted+=1
      if val<best-1e-10:best=val;bestA=A.copy()
      if best<1-1e-9:
       rec={'n':n,'r':r,'triangles_allowed':triangles,'weighted_ratio':val,'pi':pi.tolist(),'s':s.tolist(),'A':A.tolist()}
       json.dump(rec,open(folder/'counterexample.json','w'),indent=2);print('FAIL',rec,flush=True);raise SystemExit
     else:A[u,old]=1;A[u,v]=0
    rec={'n':n,'r':r,'triangles_allowed':triangles,'run':run,'best':best,'tested':tested,'accepted':accepted}
    bestall.append(rec);print(rec,'seconds',time.monotonic()-start,flush=True)
    json.dump(bestall,open(folder/'anneal_results.json','w'),indent=2)
