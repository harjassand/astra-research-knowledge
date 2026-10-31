#!/usr/bin/env python3
"""Diagnostic of native merged-source diagonal-algebra restriction.
Full quantum system output agrees with output after source dephasing, including
initial source-system entanglement. Double arithmetic, not certified simulation.
"""
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
rng=np.random.default_rng(814)
X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex)
def super_comm(H):
 d=len(H);return -1j*(np.kron(np.eye(d),H)-np.kron(H.T,np.eye(d)))
def dissipator(L):
 d=len(L);H=L.conj().T@L
 return np.kron(L.conj(),L)-.5*(np.kron(np.eye(d),H)+np.kron(H.T,np.eye(d)))
def reduced(rho,D):return np.einsum('aiaj->ij',rho.reshape(D,2,D,2))
rows=[]
for n in [1,2,3]:
 D=2**n;q=21/20
 w=np.array([q**sum(((x>>i)&1)==((x>>(i+1))&1) for i in range(n-1)) for x in range(D)])
 Q=np.zeros((D,D));Ls=[]
 for i in range(n):
  L0=np.zeros((D,D));L1=np.zeros((D,D))
  for x in range(D):
   if (x>>i)&1:continue
   y=x^(1<<i);r0=w[y]/(w[x]+w[y]);r1=1-r0
   # L0=|1><v|; L1=-|0><v| on each fixed-neighbor sector.
   L0[y,x]=math.sqrt(r0);L0[y,y]=-math.sqrt(r1)
   L1[x,x]=-math.sqrt(r0);L1[x,y]=math.sqrt(r1)
   Q[y,x]+=r0;Q[x,x]-=r0;Q[x,y]+=r1;Q[y,y]-=r1
  Ls.extend([L0,L1])
 G=sum(dissipator(L) for L in Ls)
 err=0
 for k in range(D):
  o=np.zeros(D);o[k]=1
  out=(G.conj().T@np.diag(o).reshape(-1,order='F')).reshape((D,D),order='F')
  err=max(err,float(np.linalg.norm(out-np.diag(Q.T@o))))
 for lam in [100,10000]:
  H=np.kron(np.eye(D),X)+math.sqrt(lam)*np.kron(np.diag([1-2*(x&1) for x in range(D)]),Z)
  L=super_comm(H)+lam*sum(dissipator(np.kron(l,I)) for l in Ls for I in [np.eye(2)])
  E=expm(L)
  out_error=0
  for trial in range(4):
   psi=rng.normal(size=2*D)+1j*rng.normal(size=2*D);psi/=np.linalg.norm(psi)
   rho=np.outer(psi,psi.conj());deph=np.zeros_like(rho)
   for x in range(D):deph[2*x:2*x+2,2*x:2*x+2]=rho[2*x:2*x+2,2*x:2*x+2]
   a=(E@rho.reshape(-1,order='F')).reshape((2*D,2*D),order='F')
   b=(E@deph.reshape(-1,order='F')).reshape((2*D,2*D),order='F')
   out_error=max(out_error,float(np.linalg.norm(reduced(a,D)-reduced(b,D),ord='nuc')))
  rows.append(dict(n=n,rate=lam,diagonal_adjoint_residual=err,max_system_output_difference=out_error))
out=dict(scope=__doc__,rows=rows)
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
