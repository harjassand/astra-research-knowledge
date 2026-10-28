"""Independent numerical QR, perturbation and physical receiver stress checks.
These are not substitutes for the manuscript's dimension-uniform proof.
"""
import numpy as np
import json
from pathlib import Path
rng=np.random.default_rng(442089)
trials=0; max_raw=0.;max_polar=0.;max_qr=0.;max_action=0.;counts={}
for d in [3,4,5,8,16]:
 for t in range(60):
  A=rng.normal(size=(d,2))+1j*rng.normal(size=(d,2))
  V=np.linalg.qr(A)[0]
  s=rng.uniform(.02,1.)
  C=s*np.outer(V[:,0],V[:,1].conj())
  E=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
  E*=s*rng.uniform(.0001,.19)/np.linalg.norm(E,2)
  eta=np.linalg.norm(E,2)
  left,sing,right=np.linalg.svd(C+E)
  a=sing[0]
  assert a>4*eta
  W=np.column_stack((left[:,0],right.conj().T[:,0]))
  theta=np.vdot(V,W);theta/=abs(theta)
  pL,_,pR=np.linalg.svd(W,full_matrices=False); VH=pL@pR
  raw=np.linalg.norm(W-theta*V,'fro')/(2*eta/a)
  polar=np.linalg.norm(VH-theta*V,2)/(4*eta/a)
  assert raw<1+1e-10 and polar<1+1e-10
  max_raw=max(max_raw,raw);max_polar=max(max_polar,polar)
  # Independently implement complex two-level QR; no dense completion oracle.
  B=VH.copy();U=np.eye(d,dtype=complex);count=0
  for col in [0,1]:
   for row in range(d-1,col,-1):
    x,y=B[col,col],B[row,col]
    r=np.sqrt(abs(x)**2+abs(y)**2)
    if r==0:continue
    G=np.eye(d,dtype=complex)
    G[col,col]=x.conj()/r;G[col,row]=y.conj()/r
    G[row,col]=-y/r;G[row,row]=x/r
    B=G@B;U=G@U;count+=1
  target=np.eye(d,dtype=complex)[:,:2]
  qr=np.linalg.norm(U@VH-target,2)
  assert qr<2e-13 and count<=2*d-3
  assert np.linalg.norm(U@U.conj().T-np.eye(d),2)<2e-13
  max_qr=max(max_qr,qr);counts[str(d)]=max(counts.get(str(d),0),count)
  # Arbitrary complex input matrices: compressed/reset expression equals QR protocol.
  X=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
  F=np.eye(d)-VH@VH.conj().T
  out=VH.conj().T@X@VH
  out[1,1]+=np.trace(F@X)
  trans=U@X@U.conj().T
  got=trans[:2,:2].copy();got[1,1]+=np.trace(trans[2:,2:])
  action=np.linalg.norm(out-got,2)
  assert action<2e-12
  max_action=max(max_action,action);trials+=1
out={'seed':442089,'trials':trials,'dimensions':[3,4,5,8,16],'maximum_raw_distance_over_bound':max_raw,'maximum_polar_distance_over_bound':max_polar,'maximum_QR_isometry_residual':max_qr,'maximum_channel_action_residual':max_action,'maximum_two_level_counts':counts,'status':'independent numerical stress checks passed; not a universal proof or hardware benchmark'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
