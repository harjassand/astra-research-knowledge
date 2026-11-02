import os;os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,json,math,itertools
import numpy as np
from scipy.linalg import block_diag
from schur_channel import *
from search_symmetric import cartesian_flags
rng=np.random.default_rng(20261102);out={'status':'independent full tensor and finite-difference validation, float64','cases':[]}
for n,B in [(1,2),(2,2),(3,2),(4,2),(2,4),(3,4)]:
 if B==4:w,ps,info=cartesian_flags(1/math.e+1e-5,2)
 else:w=np.array([.4,.6]);ps=np.array([[.84,.08,.03,.05],[.5,.2,.2,.1]])
 A=rng.normal(size=(2,n+1));A/=np.linalg.norm(A)
 eng=SchurChannel(n,w,ps);val,g=eng.coherent(A,True);direct,tr=direct_coherent(n,w,ps,A)
 eps=1e-6;gn=np.empty_like(A)
 for i in range(A.size):
  ep=np.zeros_like(A);ep.ravel()[i]=eps;gn.ravel()[i]=(eng.coherent(A+ep)-eng.coherent(A-ep))/(2*eps)
 item=dict(n=n,B=B,schur=val,direct=direct,error=val-direct,gradient_max_error=np.max(abs(g-gn)),trace=eng.coherent(A,diagnostics=True)['trace'],blocks=len(eng.meta))
 if n==2 and B==4:
  U=dicke_isometry(n);psi=(A@U.T).ravel();Y=np.outer(psi,psi);bys=[];bxs=[]
  for flags in itertools.product(range(B),repeat=n):
   Z=Y;prob=1.
   for i,a in enumerate(flags):Z=apply_qubit_channel(Z,ps[a],i,n,2);prob*=w[a]
   X=np.einsum('aman->mn',Z.reshape(2,2**n,2,2**n));bys.append(prob*Z);bxs.append(prob*X)
  FY=block_diag(*bys);FX=block_diag(*bxs)
  item.update(full_flag_B_entropy=entropy(FX),full_flag_RB_entropy=entropy(FY),full_flag_ic=entropy(FX)-entropy(FY),full_flag_dimensions=[len(FX),len(FY)])
 out['cases'].append(item)
assert max(abs(c['error']) for c in out['cases'])<1e-12
assert max(abs(c['gradient_max_error']) for c in out['cases'])<1e-7
for n in [6,8,12]:
 w=np.array([.45,.55]);ps=np.array([[.9,.03,.02,.05],[.5,.2,.2,.1]])
 eng=SchurChannel(n,w,ps)
 A=rng.normal(size=(1,n+1));A/=np.linalg.norm(A)
 out.setdefault('pure_checks',[]).append(dict(n=n,ic=eng.coherent(A),trace=eng.coherent(A,diagnostics=True)['trace']))
print(json.dumps(out,indent=2))
