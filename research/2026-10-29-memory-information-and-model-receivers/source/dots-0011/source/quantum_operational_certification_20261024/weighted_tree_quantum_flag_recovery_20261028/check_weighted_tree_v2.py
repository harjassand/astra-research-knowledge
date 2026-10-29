#!/usr/bin/env python3
import numpy as np,json,itertools
from pathlib import Path
rng=np.random.default_rng(202610282324)
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);P=[I,X,Y,Z]
def tn(A):return float(np.sum(abs(np.linalg.eigvalsh((A+A.conj().T)/2))))
def state():
 v=rng.normal(size=3);v=v/np.linalg.norm(v)*rng.choice([1.,rng.random()]);return (I+sum(v[i]*P[i+1] for i in range(3)))/2
edges=[(0,1),(0,2),(1,3)];words=list(itertools.product(range(4),repeat=4));largest=0.;cases=[]
for test in range(200):
 pi=rng.dirichlet(np.ones(4));T=[]
 for _ in edges:
  t=rng.dirichlet(np.ones(4),size=4)
  if test%3==0:t[:,3]=0;t/=t.sum(axis=1)[:,None]
  T.append(t)
 tau=[state() for _ in range(4)];sigma=[pi[a]*tau[a] for a in range(4)]
 prob=[]
 for x in words:prob.append(pi[x[0]]*np.prod([t[x[i],x[j]] for (i,j),t in zip(edges,T)]))
 J=[np.zeros((4,4)) for _ in edges]
 for x,p in zip(words,prob):
  for z,(i,j) in enumerate(edges):J[z][x[i],x[j]]+=p
 A=[]
 for a in range(4):
  raw=sigma[a]+sum(rng.normal(scale=.005)*p for p in P)
  val,U=np.linalg.eigh(raw);A.append((U*np.maximum(val,0))@U.conj().T)
 if test==0:A=[np.zeros((2,2),complex) for _ in range(4)]
 B=[np.maximum(j+rng.normal(scale=.003,size=(4,4)),0) for j in J]
 if test%4==0:B[0][1]=0
 Zsum=sum(np.trace(a).real for a in A)
 if Zsum==0:root=[I/8 for _ in range(4)]
 else:root=[a/Zsum for a in A]
 Q=[]
 for b in B:
  q=np.zeros((4,4))
  for a in range(4):q[a]=b[a]/b[a].sum() if b[a].sum()>0 else np.ones(4)/4
  Q.append(q)
 actual=0
 for x,p in zip(words,prob):
  coef=np.prod([q[x[i],x[j]] for (i,j),q in zip(edges,Q)])
  actual+=tn(p*tau[x[0]]-coef*root[x[0]])/2
 rooterr=sum(tn(a-s) for a,s in zip(A,sigma));edgeerr=sum(np.sum(abs(b-j)) for b,j in zip(B,J));bound=rooterr+edgeerr
 assert actual<=bound+1e-12
 largest=max(largest,actual/bound)
 cases.append({'actual_cq_TV':actual,'bound':bound,'zero_root':bool(Zsum==0),'zero_fitted_row':test%4==0})
out={'tests':len(cases),'all_passed':True,'max_actual_over_bound':largest,'tree_edges':edges,'source_flags':'random rank1 or mixed, noncommuting','cases':cases}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='cases'})
