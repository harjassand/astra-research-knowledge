import numpy as np,random,json
rng=np.random.default_rng(8675309)
for n in range(4,31):
 best=0
 for it in range(10000):
  x=rng.random((n,n));A=np.zeros((n,n),int)
  for i in range(n):
   for j in range(i):
    if x[i,j]<.4:A[i,j]=1
    elif x[i,j]<.8:A[j,i]=1
  d=A.sum(1)
  if min(d)==0:continue
  M=A.T/d-np.eye(n);M[-1,:]=1;b=np.zeros(n);b[-1]=1
  try:p=np.linalg.solve(M,b)
  except:continue
  if min(p)<1e-8:continue
  B=(A@A>0)&(A==0);np.fill_diagonal(B,False);s=B.sum(1);v=p@(s-d)
  if v<best-1e-8:
   best=v;print(n,it,best,'s',s,'d',d,flush=True)
   json.dump({'n':n,'v':float(v),'A':A.tolist(),'p':p.tolist(),'s':s.tolist(),'d':d.tolist()},open('independent_programme/deep_theory_20261010/audit/general_counterexample.json','w'),indent=2)
   raise SystemExit
 print('done',n,flush=True)
