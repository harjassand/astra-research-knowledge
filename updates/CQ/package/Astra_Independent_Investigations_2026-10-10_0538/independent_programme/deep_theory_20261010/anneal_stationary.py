import numpy as np,json,time
from numpy.random import default_rng
rng=default_rng(10100531)
def getstat(A):
 n=len(A);r=int(A.sum(1)[0]);M=A.T.astype(float)/r-np.eye(n);M[-1]=1;b=np.zeros(n);b[-1]=1
 try:pi=np.linalg.solve(M,b)
 except np.linalg.LinAlgError:return None
 if pi.min()<1e-11:return None
 B=(A@A>0)&(A==0);np.fill_diagonal(B,False);s=B.sum(1);return float(pi@s/r),pi,s
results=[];start=time.time()
for n,r in [(13,3),(17,4),(25,6),(21,5),(29,7),(37,9),(21,4),(31,6),(41,8),(31,5),(41,6)]:
 A=np.zeros((n,n),dtype=np.int64)
 for i in range(n):A[i,(i+np.arange(1,r+1))%n]=1
 cur=getstat(A);best=(cur[0],A.copy(),cur[1],cur[2]);ac=0
 for it in range(200000):
  u=rng.integers(n);v=rng.integers(n)
  if u==v or A[u,v] or A[v,u] or A[v]@A[:,u]:continue
  old=rng.choice(np.flatnonzero(A[u]));A[u,old]=0;A[u,v]=1
  new=getstat(A)
  temp=[.015,.008,.004,.001,.00001][min(4,(it%100000)//20000)]
  if new is None or (new[0]>cur[0] and rng.random()>np.exp((cur[0]-new[0])/temp)):
   A[u,old]=1;A[u,v]=0;continue
  cur=new;ac+=1
  if cur[0]<best[0]-1e-12:
   best=(cur[0],A.copy(),cur[1],cur[2]); print('IMPROVE',n,r,it,best[0],flush=True)
  if cur[0]<.99999:break
 row={'n':n,'r':r,'value':best[0],'A':best[1].tolist(),'pi':best[2].tolist(),'second':best[3].tolist(),'accepted':ac}
 results.append(row);json.dump(results,open('independent_programme/deep_theory_20261010/stationary_anneal.json','w'),indent=2)
 print('DONE',n,r,'best',best[0],'accepted',ac,'seconds',time.time()-start,flush=True)
 if best[0]<.99999:break
