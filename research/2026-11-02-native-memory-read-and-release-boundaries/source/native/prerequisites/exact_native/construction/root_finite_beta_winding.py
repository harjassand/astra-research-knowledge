"""Finite-beta leading winding formula, isolated K-cycle. Numerical check only."""
import numpy as np,json,math
from scipy.special import logsumexp,gammainc
out=[]
for K in [3,4,7]:
 for B in [1.,3.,10.]:
  rs=[.12,.08,.05] if K==7 else [.03,.02,.01]
  row=[]
  target=gammainc(K-1,B)/(1+(K-1)*math.exp(-B))
  for r in rs:
   fs=[]
   for s in [-1,1]:
    H=np.diag([0.]+[1.]*(K-1))
    for j in range(K):
     h=-r*(s if j==K-1 else 1)
     H[j,(j+1)%K]+=h;H[(j+1)%K,j]+=h
    ev=np.linalg.eigvalsh(H);fs.append(-logsumexp(-B*ev)/B)
   J=(fs[0]-fs[1])/2
   row.append({'r':r,'ratio_to_zero_temperature_leading':J/(2*r**K),'finite_beta_leading':target})
  out.append({'K':K,'B':B,'checks':row})
print(json.dumps(out,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(out,indent=2)+'\n')
