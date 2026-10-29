"""Actual rank-four antisymmetric Kraus contraction for a mixed qubit encoder.
Known measurement outcomes are all computational wedge basis subsets; no V-dependent control.
"""
import itertools,numpy as np,json
from pathlib import Path
rng=np.random.default_rng(202610291154);Y=np.array([[0,-1j],[1j,0]])
Y3=np.kron(np.kron(Y,Y),Y)
e0=np.zeros((8,2));e0[2,0]=1/np.sqrt(2);e0[4,0]=-1/np.sqrt(2);e0[3,1]=1/np.sqrt(2);e0[5,1]=-1/np.sqrt(2)
e1=np.zeros((8,2));e1[1,0]=np.sqrt(2/3);e1[2,0]=e1[4,0]=-np.sqrt(1/6);e1[3,1]=e1[5,1]=np.sqrt(1/6);e1[6,1]=-np.sqrt(2/3)
E=[e0,e1];assert np.linalg.norm(np.column_stack(E).conj().T@np.column_stack(E)-np.eye(4))<1e-12
rows=[]
for D in [4,5,7]:
 for lam in [[.5,.5],[.3,.7],[.01,.99]]:
  A=rng.normal(size=(D,4))+1j*rng.normal(size=(D,4));V=np.linalg.qr(A)[0]
  effect=np.zeros((2,2),complex);residual=0;leak=0;decoded=[]
  for subset in itertools.combinations(range(D),4):
   for junk in itertools.product(range(2),repeat=4):
    M=np.zeros((8,2),complex)
    factor=np.sqrt(np.prod([lam[a] for a in junk])/(8*24))
    for idx,xs in enumerate(itertools.product(range(2),repeat=3)):
     for l in range(2):
      cols=[2*x+a for x,a in zip(xs,junk[:3])]+[2*l+junk[3]]
      if len(set(cols))==4:M[idx,l]=factor*np.linalg.det(V[np.ix_(subset,cols)])
    effect+=M.conj().T@M;MY=Y3@M
    leak=max(leak,float(np.linalg.norm(MY-sum(e@e.conj().T@MY for e in E))))
    for e in E:
     K=e.conj().T@MY;alpha=np.trace(K)/2;residual=max(residual,float(np.linalg.norm(K-alpha*np.eye(2))));decoded.append(K)
  target=(lam[0]*lam[1])**2/16
  err=np.linalg.norm(effect-target*np.eye(2));assert err<1e-12 and residual<1e-12 and leak<1e-12
  rows.append(dict(D=D,junk_spectrum=lam,success=target,effect_residual=float(err),decoded_scalar_identity_residual=residual,spin_three_halves_leak=leak))
res=dict(scope='Dense actual exterior-instrument contraction plus fixed Y and spin1/2 decoder for qubit logical input, rank2 junk, outputD4,5,7. Diagnostic not general theorem/hardware.',rows=rows)
Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
