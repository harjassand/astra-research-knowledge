"""Finite native-PVBS shifted-kernel checks with fixed random exchange phases."""
import numpy as np, json
from pathlib import Path
from functools import reduce
rng=np.random.default_rng(246031)
results=[]
for lambdas in [[.5,2.],[.5,.5],[.5,.5,2.],[.5,.5,.5],[.25,.5,2.]]:
 s=len(lambdas);d=s+1;lam=np.r_[1,lambdas];h=np.zeros((d*d,d*d),complex)
 for i in range(d):
  for j in range(i+1,d):
   th=rng.uniform(-np.pi,np.pi);v=np.zeros(d*d,complex);v[i*d+j]=1;v[j*d+i]=-np.exp(1j*th)*lam[j]/lam[i];v/=np.linalg.norm(v);h+=np.outer(v,v.conj())
 for i in range(1,d):h[i*d+i,i*d+i]=1
 y=np.r_[0,np.array(lambdas)**2/(1+np.array(lambdas)**2)-.5];Y=np.diag(y)
 hp=h-np.kron(Y,np.eye(d))+np.kron(np.eye(d),Y)
 r=max(lambdas.count(x) for x in set(lambdas));k=r+1
 H=np.zeros((d**k,d**k),complex)
 for i in range(k-1):H+=np.kron(np.eye(d**i),np.kron(hp,np.eye(d**(k-i-2))))
 ev=np.linalg.eigvalsh(H)
 rec={'lambdas':lambdas,'k':k,'two_site_min_eigenvalue':float(np.linalg.eigvalsh(hp)[0]),'block_ground_dimension_at_1e-9':int(np.count_nonzero(abs(ev)<1e-9)),'block_c':float(ev[1])}
 assert rec['block_ground_dimension_at_1e-9']==1 and rec['block_c']>0
 results.append(rec)
print(json.dumps(results,indent=2))
(Path(__file__).resolve().parent/'native_pvbs_coboundary_results.json').write_text(json.dumps(results,indent=2)+'\n')
