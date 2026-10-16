"""Numerical stress test, not proof: three Z3 frames, fully overlapping noncommuting terms."""
import itertools, json
import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(20261015)
G=list(itertools.product(range(3),repeat=3)); n=4
subsets=[S for k in range(1,4) for S in itertools.combinations(range(3),k)]
def hermitian():
 A=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n)); A=(A+A.conj().T)/2
 return A/np.linalg.norm(A,2)
worst=0.; count=0
for trial in range(12):
 dt=np.array([.11,.17,.23,.29])
 H0=[2*hermitian() for _ in dt]
 V=np.zeros((4,3,3,n,n),complex)
 for t in range(4):
  for i in range(3):
   for g in range(3): V[t,i,g]=(.3+.1*i)*hermitian()
 actions=np.array([sum(dt[t]*max(np.linalg.norm(V[t,i,g],2) for g in range(3)) for t in range(4)) for i in range(3)])
 U={}
 for g in G:
  W=np.eye(n,dtype=complex)
  for t in range(4): W=expm(-1j*dt[t]*(H0[t]+sum(V[t,i,g[i]] for i in range(3))))@W
  U[g]=W
 F={chi:sum(np.exp(-2j*np.pi*sum(chi[i]*g[i] for i in range(3))/3)*U[g] for g in G)/27 for chi in G}
 complete=sum(K.conj().T@K for K in F.values())
 assert np.linalg.norm(complete-np.eye(n),2)<1e-12
 for S in subsets:
  effect=sum(K.conj().T@K for chi,K in F.items() if all(chi[i]!=0 for i in S))
  budget=float(np.prod(actions[list(S)]**2))
  ratio=float(np.linalg.eigvalsh(effect)[-1]/budget)
  worst=max(worst,ratio); count+=1
  assert np.linalg.eigvalsh(budget*np.eye(n)-effect)[0]>=-1e-12
print(json.dumps({'PASS':True,'subset_effect_checks':count,'group':'Z3^3','segments':4,'dimension':n,'worst_effect_to_bound_ratio':worst,'note':'Numerical stress test only; analytic proof is independent.'}))
