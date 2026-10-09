#!/usr/bin/env python3
"""Verify fixed one-record EB output and exact entropy identity on finite states."""
from pathlib import Path
import json, math
import numpy as np
ROOT=Path(__file__).resolve().parent
rng=np.random.default_rng(2707)
dims=[2,2,2]
def partial(x,dims,keep):
 ds=list(dims); a=x.reshape(ds+ds)
 for i in sorted(set(range(len(ds)))-set(keep),reverse=True):
  a=np.trace(a,axis1=i,axis2=i+len(ds)); ds.pop(i)
 return a.reshape(math.prod(ds),math.prod(ds))
def entropy(x):
 es=np.linalg.eigvalsh((x+x.conj().T)/2); es=es[es>1e-12]
 return float(-np.dot(es,np.log(es)))
def dephase_last(x,ds):
 a=x.reshape(ds+ds); out=np.zeros_like(a)
 for c in range(ds[-1]):
  ind=[slice(None)]*(2*len(ds));ind[len(ds)-1]=c;ind[-1]=c
  out[tuple(ind)]=a[tuple(ind)]
 return out.reshape(x.shape)
def relative(x,y):
 ey,vy=np.linalg.eigh((y+y.conj().T)/2)
 good=ey>1e-12; support=vy[:,good]@vy[:,good].conj().T
 assert np.linalg.norm(x-support@x@support)<1e-9
 logy=(vy[:,good]*np.log(ey[good]))@vy[:,good].conj().T
 return float(-entropy(x)-np.trace(x@logy).real)
def eb_output(rho):
 k=partial(rho,dims,[1,2]); ac=partial(rho,dims,[0,2])
 out=np.zeros((8,8),complex)
 for c in range(2):
  bc=k.reshape(2,2,2,2)[:,c,:,c]; p=np.trace(bc).real
  beta=bc/p if p>1e-12 else np.eye(2)/2
  xa=ac.reshape(2,2,2,2)[:,c,:,c]
  label=np.zeros((2,2));label[c,c]=1
  out+=np.kron(np.kron(xa,beta),label)
 return out
states=[]
up=np.array([1,0]);plus=np.array([1,1])/math.sqrt(2)
psi=math.sqrt(.4)*np.kron(np.kron(up,up),up)+math.sqrt(.6)*np.kron(np.kron([0,1],plus),[0,1])
pure=np.outer(psi,psi.conj());kap=partial(pure,dims,[1,2])
for mix in [1,.3]:
 rho=mix*pure+(1-mix)*np.kron(np.eye(2)/2,kap)
 states.append(("CQ_NOT_CC_COHERENT_EXTENSION",rho))
for i in range(8):
 z=rng.normal(size=(8,8))+1j*rng.normal(size=(8,8))
 rho=z@z.conj().T;rho/=np.trace(rho)
 states.append(("ARBITRARY_KAPPA",rho))
rows=[]
for kind,rho in states:
 kap=partial(rho,dims,[1,2]);a=partial(rho,dims,[0]);b=partial(rho,dims,[1]);c=partial(rho,dims,[2])
 ab=partial(rho,dims,[0,1]);ac=partial(rho,dims,[0,2])
 rp=dephase_last(rho,dims);kp=dephase_last(kap,[2,2])
 acp=dephase_last(ac,[2,2]);cp=dephase_last(c,[2])
 db=entropy(ab)+entropy(kap)-entropy(b)-entropy(rho)
 dc=entropy(ac)+entropy(kap)-entropy(c)-entropy(rho)
 U=entropy(rp)-entropy(rho);V=entropy(acp)-entropy(ac)
 Q=entropy(kp)-entropy(kap);qC=entropy(cp)-entropy(c)
 out=eb_output(rho);D=relative(rho,out)
 error=abs(D-(dc+V+Q-qC))
 ma=np.linalg.norm(partial(out,dims,[0])-a)
 mk=np.linalg.norm(partial(out,dims,[1,2])-kp)
 assert error<1e-10
 assert ma<1e-10 and mk<1e-10
 assert D<=db+dc+2*Q-qC+1e-10
 assert V<=U+1e-10
 if kind.startswith("CQ"):
  assert np.linalg.norm(kap-kp)<1e-10
  assert D<=db+dc+1e-10
  beta0=kap.reshape(2,2,2,2)[:,0,:,0]/.4
  beta1=kap.reshape(2,2,2,2)[:,1,:,1]/.6
  assert np.linalg.norm(beta0@beta1-beta1@beta0)>.1
 rows.append({"family":kind,"delta_B":db,"delta_C":dc,
              "direct_relative_entropy_to_EC_output":D,
              "partial_coherence_kappa":Q,
              "identity_error":error,"exact_A_error":ma,
              "raw_dephased_BC_error":mk,
              "original_BC_error":float(np.linalg.norm(partial(out,dims,[1,2])-kap))})
out={"status":"PASS","scope":"10 finite direct matrix diagnostics only, not general proof or formal certification; arbitrary-kappa raw output verified as DEPHASED marginal.","results":rows}
(ROOT/"ONE_RECORD_DIAGNOSTICS.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"status":"PASS","cases":len(rows),"max_identity_error":max(r["identity_error"] for r in rows)}))

