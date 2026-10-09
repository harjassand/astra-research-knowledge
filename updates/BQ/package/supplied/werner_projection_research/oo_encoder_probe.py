"""Exploratory SO(3)-equivariant ternary encoders. Not a proof or a distillation protocol receipt."""
from __future__ import annotations
import numpy as np
from scipy.optimize import minimize
from pathlib import Path
import json
D=3
I=np.eye(9)
F=np.eye(9).reshape(3,3,3,3).transpose(1,0,2,3).reshape(9,9)
omega=np.eye(3).reshape(9)
O=np.outer(omega,omega)
BASIS=np.stack([I,F,O])
GRAM=np.einsum('aij,bij->ab',BASIS,BASIS)
INVGRAM=np.linalg.inv(GRAM)
T=np.zeros((3,3,3,3,3)) # channel label, physical i,j,k, logical l
for i in range(3):
 for j in range(3):
  for k in range(3):
   for l in range(3):
    T[0,i,j,k,l]=(i==l)*(j==k)
    T[1,i,j,k,l]=(j==l)*(i==k)
    T[2,i,j,k,l]=(k==l)*(i==j)
T=T.reshape(3,27,3)

def encoder(w):
 W=np.einsum('a,aij->ij',w,T)
 W=W/np.sqrt(np.trace(W.conj().T@W).real/3)
 return W

def step(coeff, w):
 R=np.einsum('a,aij->ij',coeff,BASIS)
 W=encoder(w)
 V=np.kron(W,W).reshape(3,3,3,3,3,3,9).transpose(0,3,1,4,2,5,6).reshape(9,9,9,9)
 Y=V
 for ax in range(3):
  Y=np.tensordot(R,Y,axes=(1,ax))
  Y=np.moveaxis(Y,0,ax)
 X=np.einsum('abcj,abck->jk',V.conj(),Y)
 c=INVGRAM@np.einsum('aij,ji->a',BASIS,X)
 if np.max(np.abs(X-np.einsum('a,aij->ij',c,BASIS)))>1e-8:
  raise RuntimeError('Covariance residual too large')
 c=c.real
 c/=np.trace(X).real/9
 return c

def objective(v,depth):
 c=np.array([1.,-.5,0.])
 W=(v[:depth*3]+1j*v[depth*3:]).reshape(depth,3)
 if np.any(np.linalg.norm(W,axis=1)<1e-10): return 1e4
 for w in W: c=step(c,w)
 a,b,g=c
 # All possible rank-two same-plane tests: real plane if g<0, complex minimal-overlap if g>=0.
 return a+2*b+(g if g<0 else g/2)

def run(depth=2, starts=12):
 rng=np.random.default_rng(618)
 rows=[];best=None
 for i in range(starts):
  x=rng.normal(size=6*depth)
  res=minimize(lambda v:objective(v,depth),x,method='BFGS',options={'maxiter':65,'gtol':1e-7})
  row={'start':i,'value':float(res.fun),'iterations':int(res.nit),'success':bool(res.success)}
  rows.append(row)
  if best is None or res.fun<best[0]: best=(res.fun,res.x.copy())
 return {'depth':depth,'physical_copies':3**depth,'rows':rows,'minimum':float(best[0]),'best_parameters':best[1].tolist(),'status':'floating local searches in a restricted encoder family; not a universal result'}
if __name__=='__main__':
 import sys,time
 depth=int(sys.argv[1]) if len(sys.argv)>1 else 2
 starts=int(sys.argv[2]) if len(sys.argv)>2 else 8
 t=__import__('time').perf_counter()
 out=run(depth,starts)
 out['elapsed_seconds']=__import__('time').perf_counter()-t
 print(json.dumps(out,indent=2))
 (Path(__file__).parent/f'oo_encoder_depth{depth}.json').write_text(json.dumps(out,indent=2))
