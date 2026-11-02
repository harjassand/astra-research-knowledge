"""Exact small native resonant-clock Gibbs diagnostic. No code/lifetime claim."""
from pathlib import Path
import json
import numpy as np
from scipy.linalg import eigh
I=np.eye(2);X=np.array([[0.,1.],[1.,0.]]);Z=np.diag([1.,-1.]);D=np.eye(4)
P=[[np.kron(X,I),np.kron(I,X),D],[np.kron(Z,I),np.kron(I,Z),D]]
S=[P[0][0]@P[0][1],P[1][0]@P[1][1]]
K=3;t=1.;eta=.05;g=eta*t/K;J=2*g*g/(t*K)
H=np.zeros((36,36));U=np.zeros_like(H)
for q in range(K):
 for r in range(K):
  k=(q*K+r)*4;H[k:k+4,k:k+4]+=2*t*((q!=0)+(r!=0))*D
  u=D.copy()
  for a,n in enumerate([q,r]):
   for j in range(n):u=u@P[a][j]
  U[k:k+4,k:k+4]=u
  for a,n in enumerate([q,r]):
   c=[q,r];c[a]=(n+1)%K;l=(c[0]*K+c[1])*4
   h=g if n in [0,K-1] else t
   H[l:l+4,k:k+4]-=h*P[a][n];H[k:k+4,l:l+4]-=h*P[a][n]
clock=np.zeros((3,3));clock[0,1]=clock[1,0]=1
V=np.kron(np.eye(9),np.kron(X,I)+.7*np.kron(Z,I))+.3*np.kron(np.kron(clock,np.eye(3)),D)
V/=np.linalg.norm(V,2)
checks=[U@np.kron(np.eye(9),s)@U.T for s in S]
rows=[]
for alpha in [0.,.001,.01]:
 ev,vs=eigh(H+alpha*J*V)
 for B in [1.,5.,20.,100.]:
  beta=B/J;weights=np.exp(-beta*(ev-ev[0]));weights/=weights.sum();rho=(vs*weights)@vs.T
  probs=[float(np.trace(rho@(np.eye(36)-s)/2)) for s in checks]
  assert abs(np.trace(rho)-1)<1e-12 and min(probs)>-1e-12
  rows.append(dict(v_over_J=alpha,beta_J=B,beta_v=alpha*B,syndrome_defect_probabilities=probs,smallest_gap=float(ev[1]-ev[0])))
result=dict(scope='Two data qubits, two 3-level clocks, full36-dimensional Gibbs state; no protected logical qubit and no asymptotic claim.',K=K,t=t,g=g,J=J,rows=rows)
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
