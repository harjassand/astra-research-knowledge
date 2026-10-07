#!/usr/bin/env python3
"""Bounded transcription checks for explicit EB reference balancing."""
from pathlib import Path
import numpy as np,json
root=Path(__file__).resolve().parent
rng=np.random.default_rng(6050103)

def density(d):
 z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));s=z@z.conj().T
 return s/np.trace(s)

def povm(d,r):
 Z=[density(d) for _ in range(r)];S=sum(Z);lam,U=np.linalg.eigh(S)
 inv=(U*(lam**-.5))@U.conj().T
 return [inv@z@inv for z in Z]

def contract(d):
 z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));z=(z+z.conj().T)/2
 return z/max(1,np.linalg.norm(z,2))

fixtures=[]
for d in range(2,7):
 for r in [d,2*d]:
  M=povm(d,r);rho=[density(d) for _ in range(r)]
  E=lambda A:sum(np.trace(m@A)*p for m,p in zip(M,rho))
  Es=lambda A:sum(np.trace(p@A)*m for m,p in zip(M,rho))
  S=E(np.eye(d));lam,U=np.linalg.eigh(S)
  f=np.minimum(1,lam**-.5);F=(U*f)@U.conj().T
  Delta=np.eye(d)-F@S@F;Delta=(Delta+Delta.conj().T)/2
  D=np.eye(d)-Es(F@F);D=(D+D.conj().T)/2
  t=float(np.trace(Delta).real/d)
  delta=float(np.linalg.svd(S-np.eye(d),compute_uv=False).sum()/d)
  Ebal=lambda A:F@E(A)@F+np.trace(D@A)*Delta/(d*t)
  assert np.linalg.eigvalsh(D).min()>-1e-10 and np.linalg.eigvalsh(Delta).min()>-1e-10
  assert abs(t-delta/2)<1e-10
  uerr=float(np.linalg.norm(Ebal(np.eye(d))-np.eye(d),'fro'))
  assert uerr<1e-9
  maxerr=0.;maxterr=0.
  for _ in range(40):
   A=contract(d);maxerr=max(maxerr,float(np.linalg.svd(E(A)-Ebal(A),compute_uv=False).sum()/d))
   maxterr=max(maxterr,float(abs(np.trace(Ebal(A))-np.trace(A))))
  bound=2*np.sqrt(t)+t
  assert maxerr<bound+1e-9 and maxterr<1e-8
  fixtures.append({'d':d,'POVM_outcomes':r,'delta':delta,'t':t,'bound':float(bound),'sample_max_normalized_L1_change':maxerr,'unital_error':uerr,'sample_trace_error':maxterr})
(root/'eb_balancing_checks.json').write_text(json.dumps({'seed':6050103,'fixtures':fixtures,'scope':'Floating finite diagnostics only. Positivity, EB, reference fixation and uniform norm estimates follow from the written proof.'},indent=2)+'\n')
print(json.dumps({'fixtures':len(fixtures),'max_unital_error':max(x['unital_error'] for x in fixtures),'max_trace_error':max(x['sample_trace_error'] for x in fixtures)},indent=2))
