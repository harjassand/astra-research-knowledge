"""Finite algebra regressions only, not proof of the hardware theorem."""
import json, itertools, numpy as np
from pathlib import Path
rng=np.random.default_rng(20261030)
d=16
bits=np.array([[(i>>j)&1 for j in range(4)] for i in range(d)])
h=[bits[:,:2].sum(1),bits[:,2:].sum(1)]
s=.71; alpha=.22; n=2
F=[np.exp(s*x) for x in h]
Z=[1+.13*np.exp(.39*x) for x in h]
w=np.array([3.7,4.1]); M=1.8
sets=[(),(0,),(1,),(0,1)]
def diag_weight(B,A,phase):
 v=np.ones(d)
 for j in B:v*=phase[j]
 for j in A:v*=Z[j]
 return v

def bound(YL,YR,phase,ww,R=(0,1)):
 subsets=[x for x in sets if set(x)<=set(R)]
 return max(float(np.dot(diag_weight(B,A,phase),np.diag(Y).real)/(np.prod(ww[list(B)])*M**len(A)))
            for B in subsets for A in subsets for Y in [YL,YR])
res={"trials":200,"soft_switch_identity_error":0.,"soft_switch_excess":0.,"cross_envelope_excess":0.,"minimum_cross_block_eigenvalue":0.,"scalar_soft_drift_excess":0.}
P=np.diag((h[0]<=1).astype(float)); Q=np.eye(d)-P
Xbit=np.zeros((d,d))
for i in range(d):Xbit[i^1,i]=1
U=Q@Xbit@P; V=P
# source H1=1 on left; the right side can have H1=0
aleg=np.exp(-s/2); bleg=1.
for _ in range(200):
 W=rng.normal(size=(2*d,2*d))+1j*rng.normal(size=(2*d,2*d))
 Y=W@W.conj().T
 YL=P@Y[:d,:d]@P; YR=P@Y[d:,d:]@P; X=P@Y[:d,d:]@P
 cin=bound(YL,YR,F,w)
 G=[1+np.exp(-alpha*n)*f for f in F]
 wn=1+np.exp(-alpha*n)*w
 cout=bound(YL,YR,G,wn)
 res['soft_switch_excess']=max(res['soft_switch_excess'],cout/cin-1)
 for B in sets:
  for A in sets:
   lhs=diag_weight(B,A,G); rhs=np.zeros(d)
   for r in range(len(B)+1):
    for C in itertools.combinations(B,r):
     rhs+=np.exp(-alpha*n*len(C))*diag_weight(C,A,F)
   res['soft_switch_identity_error']=max(res['soft_switch_identity_error'],float(np.max(abs(lhs-rhs))))
 L=(bleg/aleg)*(U@YL@U.conj().T)
 R=(aleg/bleg)*(V@YR@V.conj().T)
 C=U@X@V.conj().T
 block=np.block([[L,C],[C.conj().T,R]])
 res['minimum_cross_block_eigenvalue']=min(res['minimum_cross_block_eigenvalue'],float(np.linalg.eigvalsh(block).min()))
 co=bound(L,R,F,w,R=(1,))
 expected=aleg*bleg*w[0]*cin
 res['cross_envelope_excess']=max(res['cross_envelope_excess'],co/expected-1)
# scalar functional calculus: actual negative UF term plus bounded noise
for N in [2,4,8,16,32,64,128]:
 ss=.37; aa=.18; bb=.11; alph=.12; rhoeta=.004
 for UU in np.linspace(0,3*N,1001):
  cF=np.exp(-alph*N+ss*UU)
  lhs=(-aa*UU+rhoeta*N)*cF
  eps=aa/ss*np.exp(-(alph-ss*bb)*N-1)
  rhs=-(aa*bb-rhoeta)*N*cF+eps
  # scale to avoid spurious huge absolute cancellation errors
  res['scalar_soft_drift_excess']=max(res['scalar_soft_drift_excess'],float((lhs-rhs)/(1+abs(lhs)+abs(rhs))))
res['passed']=all(res[k]<1e-10 for k in ['soft_switch_identity_error','soft_switch_excess','cross_envelope_excess','scalar_soft_drift_excess']) and res['minimum_cross_block_eigenvalue']>-1e-9
p=Path(__file__).with_suffix('.json'); p.write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps(res,indent=2))
assert res['passed']
