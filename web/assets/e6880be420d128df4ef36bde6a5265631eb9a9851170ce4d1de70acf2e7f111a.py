#!/usr/bin/env python3
"""Finite diagnostics for the projection-and-deficit EB construction."""
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
rng=np.random.default_rng(6050102)

def unitary(d):
 z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));q,r=np.linalg.qr(z)
 return q@np.diag(np.exp(-1j*np.angle(np.diag(r))))

def apply_both(X,F,d):
 Y=np.zeros_like(X)
 for i in range(d):
  for j in range(d):
   inds_i=[b*d+i for b in range(d)];inds_j=[b*d+j for b in range(d)]
   Y[np.ix_(inds_i,inds_j)]=F(X[np.ix_(inds_i,inds_j)])
 Z=np.zeros_like(X)
 for i in range(d):
  for j in range(d):Z[i*d:(i+1)*d,j*d:(j+1)*d]=F(Y[i*d:(i+1)*d,j*d:(j+1)*d])
 return Z

fixtures=[]
for d in range(2,5):
 for a in [.001,.03,.3,.8]:
  P=[np.diag(np.eye(d)[i]) for i in range(d)]
  K=[np.sqrt(1-a)*p for p in P]+[np.sqrt(a)*unitary(d)]
  M=[k.conj().T@k for k in K]
  def psi(x):return sum(np.trace(m@x)*m/np.trace(m) for m in M)
  def L(x):return sum(k@x@k.conj().T for k in K)
  def Cd(x):return (sum(k.conj().T@x@k for k in K)+psi(x))/2
  def Phi(x):return Cd((L(x)+psi(x))/2)
  def B(x):
   raw=sum((np.kron(k@x@k.conj().T,m/np.trace(m))+np.kron(m/np.trace(m),k@x@k.conj().T))/2 for k,m in zip(K,M))
   return apply_both(raw,Cd,d)
  omega=np.zeros((d**3,d**3),complex)
  Jphi=np.zeros((d*d,d*d),complex)
  for i in range(d):
   for j in range(d):
    e=np.zeros((d,d),complex);e[i,j]=1
    omega+=np.kron(e,B(e))/d
    Jphi+=np.kron(e,Phi(e))/d
  ui=[]
  for i in range(d):
   inds=[i*d*d+b*d+i for b in range(d)]
   ui.append(d*omega[np.ix_(inds,inds)])
  defects=np.array([1-np.trace(u).real for u in ui])
  delta=np.eye(d)/d-sum(ui)/d
  eta=float(np.trace(delta).real)
  Ri=[u+f*delta/eta for u,f in zip(ui,defects)]
  Jep=sum(np.kron(p,r) for p,r in zip(P,Ri))/d
  choi_error=float(np.linalg.svd(Jphi-Jep,compute_uv=False).sum())
  bound=2*np.sqrt(max(eta,0))+eta
  output_error=float(np.linalg.norm(sum(Ri)-np.eye(d),'fro'))
  trace_error=max(abs(np.trace(r)-1) for r in Ri)
  minprep=float(min(np.linalg.eigvalsh((r+r.conj().T)/2).min() for r in Ri))
  minomega=float(np.linalg.eigvalsh((omega+omega.conj().T)/2).min())
  assert minomega>-1e-10 and minprep>-1e-10
  assert output_error<1e-9 and trace_error<1e-9 and choi_error<=bound+1e-9
  # Matching projection removes every R off-diagonal block after C trace.
  mask=np.array([r==c for r in range(d) for b in range(d) for c in range(d)])
  success=omega*mask[:,None]*mask[None,:]
  traced=np.zeros((d*d,d*d),complex)
  for c in range(d):
   inds=[r*d*d+b*d+c for r in range(d) for b in range(d)]
   traced+=success[np.ix_(inds,inds)]
  cq=sum(np.kron(p,u) for p,u in zip(P,ui))/d
  cq_error=float(np.linalg.norm(traced-cq,'fro'))
  assert cq_error<1e-10
  fixtures.append({'d':d,'a':a,'eta':eta,'normalized_choi_trace_error':choi_error,'proved_bound':bound,'sigma_preservation_error':output_error,'preparation_trace_error':float(trace_error),'minimum_preparation_eigenvalue':minprep,'minimum_broadcaster_choi_eigenvalue':minomega,'projection_CQ_identity_error':cq_error})
result={'seed':6050102,'fixtures':fixtures,'scope':'Only finite floating diagnostics. Full claim rests on the written projection-and-deficit derivation; no universal anchor acquisition or optimal EB distance computation is supplied.'}
(ROOT/'broadcast_anchor_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'fixtures':len(fixtures),'max_sigma_preservation_error':max(f['sigma_preservation_error'] for f in fixtures),'max_preparation_trace_error':max(f['preparation_trace_error'] for f in fixtures),'max_projection_CQ_identity_error':max(f['projection_CQ_identity_error'] for f in fixtures),'minimum_preparation_eigenvalue':min(f['minimum_preparation_eigenvalue'] for f in fixtures)},indent=2))
