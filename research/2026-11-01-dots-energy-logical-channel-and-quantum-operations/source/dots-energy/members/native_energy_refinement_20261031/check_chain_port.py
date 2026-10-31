#!/usr/bin/env python3
"""Finite classical matrix diagnostics for the acquired port; no quantum backend."""
import numpy as np,json,math
rng=np.random.default_rng(20261031)
rows=[]
for n in range(1,9):
 for rep in range(5):
  t=rng.uniform(-1/41,1/41,n-1)
  if rep==0:t[:]=0
  ss=np.sqrt(1-t*t);R=np.zeros((n,n));R[0,0]=1
  for i in range(1,n):R[:,i]=t[i-1]*R[:,i-1];R[i,i]=ss[i-1]
  S=np.diag(t,1);D=np.diag(np.r_[1,ss]);N=np.eye(n);power=np.eye(n)
  for j in range(1,n):power=power@S;N+=power
  W=np.zeros((1<<(n-1),n));V=np.zeros_like(W);W[0,0]=1
  for i in range(n):
   for x in range(1<<i):
    v=1
    for k in range(i):v*=ss[k] if (x>>k)&1 else t[k]
    V[x,i]=v
  for j in range(1,n):
   for x in range(1<<(j-1)):
    v=1
    for k in range(j-1):v*=ss[k] if (x>>k)&1 else t[k]
    W[x+(1<<(j-1)),j]=v
  err=max(np.linalg.norm(W.T@W-np.eye(n)),np.linalg.norm(W@R-V),np.linalg.norm(R-D@N))
  assert err<1e-12
  assert np.linalg.norm(R,2)<=40/39+1e-12
  # Highest occupied bond recovers every nonzero W column component.
  for j in range(n):
   for x in np.flatnonzero(abs(W[:,j])>1e-15):assert int(x).bit_length()==j
  rows.append(dict(n=n,rep=rep,identity_residual=float(err),R_norm=float(np.linalg.norm(R,2))))
# Polynomial-size R diagnostic, no exponential source basis.
n=128;t=rng.uniform(-1/41,1/41,n-1);ss=np.sqrt(1-t*t);R=np.zeros((n,n));R[0,0]=1
for i in range(1,n):R[:,i]=t[i-1]*R[:,i-1];R[i,i]=ss[i-1]
L=9;S=np.diag(t,1);D=np.diag(np.r_[1,ss]);partial=np.eye(n);power=np.eye(n)
for j in range(1,L+1):power=power@S;partial+=power
trunc=float(np.linalg.norm(R-D@partial,2));bound=(1/40)**(L+1)/(1-1/40)
assert trunc<=bound+1e-15
out={'scope':'Finite matrix/marker diagnostics only; analytical frame/LCU proof is authoritative','small_cases':rows,'n128':{'R_norm':float(np.linalg.norm(R,2)),'Neumann_L':L,'truncation_residual':trunc,'analytic_tail_bound':bound}}
open('native_energy_refinement_20261031/chain_port_checks.json','w').write(json.dumps(out,indent=2)+'\n')
print('passed',len(rows),'small cases; n128',out['n128'])
