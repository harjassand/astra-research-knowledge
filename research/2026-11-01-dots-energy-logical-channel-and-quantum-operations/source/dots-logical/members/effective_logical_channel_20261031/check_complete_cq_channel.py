#!/usr/bin/env python3
"""Double-precision diagnostic, not certified arithmetic or diamond SDP.
For a classical input source, the induced complete channel difference is a direct
sum of label-conditioned differences. Its diamond norm is the maximum over labels.
Unnormalized Choi trace norm bounds each diamond norm from above; half that norm
is a maximally-entangled-input lower bound. No stationary preparation assumption.
"""
import json, math
import numpy as np
from scipy.linalg import expm
X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex);I=np.eye(2)
def comm(H):return np.kron(I,H)-np.kron(H.T,I)
def choi(S):
 J=np.zeros((4,4),complex)
 for a in range(2):
  for b in range(2):
   E=np.zeros((2,2));E[a,b]=1
   J[2*a:2*a+2,2*b:2*b+2]=(S@E.reshape(4,order='F')).reshape((2,2),order='F')
 return (J+J.conj().T)/2
rows=[]
for n in [1,2,3,4]:
 D=2**n;q=21/20
 spins=np.array([[1-2*((x>>i)&1) for i in range(n)] for x in range(D)])
 w=np.array([q**sum(s[i]==s[i+1] for i in range(n-1)) for s in spins]);pi=w/w.sum()
 Q=np.zeros((D,D))
 for x in range(D):
  for i in range(n):
   y=x^(1<<i);r=w[y]/(w[x]+w[y]);Q[y,x]+=r;Q[x,x]-=r
 z=spins[:,0];r=np.linalg.solve(-Q.T+np.ones((D,1))*pi[None,:],z);c=float(pi@(z*r))
 Le=-1j*comm(X)-c*comm(Z)@comm(Z)
 U=expm(-1j*np.pi/4*X);C=np.kron(U.conj(),U)
 gamma=2*np.linalg.norm(U.conj().T@Z@U-Z,2)
 k=.95;b=1;d=2
 for lam in [10,100,10000,1000000]:
  A=np.kron(lam*Q,np.eye(4)).astype(complex)
  for x in range(D):A[4*x:4*x+4,4*x:4*x+4]+=-1j*comm(X+math.sqrt(lam)*z[x]*Z)
  E=expm(A*.5);Ee=expm(Le*.5)
  for control in [False,True]:
   full=E@ (np.kron(np.eye(D),C) if control else np.eye(4*D)) @E
   eff=Ee@(C if control else np.eye(4))@Ee
   red=full.reshape(D,4,D,4).sum(axis=0)
   norms=[];cp=[];tp=[]
   for x in range(D):
    S=red[:,x,:];J=choi(S);dif=choi(S-eff)
    norms.append(float(np.abs(np.linalg.eigvalsh(dif)).sum()))
    cp.append(float(np.linalg.eigvalsh(J).min()))
    tp.append(float(np.linalg.norm(np.array([1,0,0,1])@S-np.array([1,0,0,1]))))
   g=gamma if control else 0
   bound=min(2,(4*b/k+2*d/k+16*b**3/k**2+g/k)/math.sqrt(lam)+(8*b*b/k**2+8*b*d/k**2+16*b**4/k**3+4*b*g/k**2)/lam)
   upper=min(2,max(norms));lower=max(norms)/2
   assert lower<=bound+1e-7
   rows.append(dict(n=n,rate=lam,control=control,choi_diamond_lower=lower,choi_diamond_upper=upper,theorem_upper=bound,min_channel_choi_eigenvalue=min(cp),max_trace_defect=max(tp),integrated_covariance=c))
out=dict(scope=__doc__,arithmetic='SciPy double precision, not certified. Choi bounds are mathematical bounds but computed values are diagnostic.',rows=rows)
from pathlib import Path
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(cases=len(rows),max_trace_defect=max(r['max_trace_defect'] for r in rows),min_choi=min(r['min_channel_choi_eigenvalue'] for r in rows),last_rows=rows[-4:]),indent=2))
