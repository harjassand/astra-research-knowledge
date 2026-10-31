#!/usr/bin/env python3
import numpy as np,json
q=21/20;t=(q-1)/(q+1)
def small(n):
 M=-np.eye(n)
 if n>1:
  M[0,1]=M[-1,-2]=t
  a=(q*q-1)/(2*(q*q+1))
  for i in range(1,n-1):M[i,i-1]=M[i,i+1]=a
 C=np.array([[t**abs(i-j) for j in range(n)] for i in range(n)])
 return M,C,-np.linalg.solve(M,C)
rows=[]
for n in [1,2,3,4,6]:
 M,C,D=small(n);N=1<<n
 spins=np.array([[1-2*((x>>i)&1) for i in range(n)] for x in range(N)])
 w=np.array([q**sum(spins[x,i]==spins[x,i+1] for i in range(n-1)) for x in range(N)])
 pi=w/w.sum();Q=np.zeros((N,N))
 for x in range(N):
  for i in range(n):
   y=x^(1<<i);rate=w[y]/(w[x]+w[y]);Q[y,x]+=rate;Q[x,x]-=rate
 W=np.linalg.solve(-Q.T+np.ones((N,1))*pi.reshape(1,N),spins)
 DF=W.T@(pi[:,None]*spins)
 e1=float(np.linalg.norm(Q.T@spins-spins@M.T));e2=float(np.linalg.norm(D-DF))
 assert max(e1,e2)<1e-12
 rows.append(dict(n=n,closure_residual=e1,integrated_covariance_residual=e2,D00=float(D[0,0])))
M,C,D=small(128)
out={'scope':'Finite classical covariance checks, not a finite-rate retained-channel or quantum circuit simulation','small_cases':rows,'n128':{'M_condition':float(np.linalg.cond(M)),'D_norm':float(np.linalg.norm(D,2)),'D00':float(D[0,0])}}
open('native_energy_refinement_20261031/magnetization_covariance_checks.json','w').write(json.dumps(out,indent=2)+'\n')
print(out)
