import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
from pathlib import Path
from itertools import combinations
from math import comb,sqrt
from fractions import Fraction as F
import numpy as np
import json,time
st=time.monotonic()
def falling(n,l):
 q=1
 for i in range(l):q*=n-i
 return q
def run(d,s):
 N=2*s;a=list(combinations(range(d),N));b=list(combinations(range(d),s));D=len(a);Q=len(b);ids={x:i for i,x in enumerate(a)}
 V=np.zeros((Q*Q,D))
 for i,k in enumerate(b):
  for j,l in enumerate(b):
   if set(k)&set(l):continue
   sign=(-1)**sum(x>y for x in k for y in l)
   V[i*Q+j,ids[tuple(sorted(k+l))]]=sign/sqrt(comb(N,s))
 ks=[V.reshape(Q,Q,D)[:,j,:] for j in range(Q)]
 def T(x):return sum(k@x@k.T for k in ks)
 def R(x):return Q/D*sum(k.T@x@k for k in ks)
 def phi(x):return R(T(x))
 matrix=np.zeros((D*D,D*D))
 for i in range(D):
  for j in range(D):
   z=np.zeros((D,D));z[i,j]=1;matrix[:,i*D+j]=phi(z).reshape(-1)
 exp=[]
 for l in range(min(N,d-N)+1):
  m=comb(d,l)**2-(comb(d,l-1)**2 if l else 0)
  lam=F(falling(s,l)*falling(d-N,l),falling(N,l)*falling(d-s,l)) if l<=s else F(0)
  exp +=[float(lam)]*m
 lam1=F(s*(d-N),N*(d-s))
 c=1/(1-lam1)
 replace=np.outer(np.eye(D).reshape(-1),np.eye(D).reshape(-1))/D
 eig=np.linalg.eigvalsh((matrix+matrix.T)/2)
 rec={'d':d,'s':s,'N':N,'D_N':D,'D_s':Q,'lambda1':str(lam1),'replacement_constant':str(c),
 'isometry_residual':float(np.max(abs(V.T@V-np.eye(D)))),
 'reference_T_residual':float(np.max(abs(T(np.eye(D)/D)-np.eye(Q)/Q))),
 'reference_Phi_residual':float(np.max(abs(phi(np.eye(D)/D)-np.eye(D)/D))),
 'symmetry_residual':float(np.max(abs(matrix-matrix.T))),
 'spectrum_residual':float(np.max(abs(eig-np.sort(exp)))),
 'Dirichlet_min_eig':float(np.linalg.eigvalsh(float(c)*(np.eye(D*D)-matrix)-(np.eye(D*D)-replace)).min())}
 assert all(v<1e-10 for k,v in rec.items() if 'residual' in k),rec
 assert rec['Dirichlet_min_eig']>-1e-10
 return rec
rec=[run(d,s) for d,s in [(3,1),(4,1),(5,1),(5,2),(6,2)]]
result={'status':'PASS_DIAGNOSTIC_ONLY','fixtures':rec,'wall_seconds':time.monotonic()-st,'scope':'Finite transcription of exterior spectral proof; no asymptotic extrapolation or counterexample.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
