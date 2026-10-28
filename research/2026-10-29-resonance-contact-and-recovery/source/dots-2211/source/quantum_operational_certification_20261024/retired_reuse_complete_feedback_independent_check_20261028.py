#!/usr/bin/env python3
"""Independent coherent-memory/controller reuse tests and fixed-workload constants."""
from pathlib import Path
import numpy as np,json
rng=np.random.default_rng(2820262026);I=np.eye(2);Z=np.diag([1.,-1.]);bell=np.array([1,0,0,1],complex)/np.sqrt(2)
# registers P,M,R; initial P-R Bell pair and coherent M state.
m=np.array([1,1j])/np.sqrt(2);psi=np.einsum('pr,m->pmr',bell.reshape(2,2),m).reshape(8);initial=np.outer(psi,psi.conj())
def unitary(d):
 x=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));q,r=np.linalg.qr(x);return q
rows=[]
for J in [1,2,3,5,8]:
 native=[unitary(4) for _ in range(J)]
 def run(t):
  out=initial.copy();R=np.kron(np.diag(np.exp(1j*t*np.array([1,-1])/2)),np.eye(4))
  for j,U in enumerate(native):
   Q=np.kron(U,I);out=Q@out@Q.conj().T;out=R@out@R.conj().T
   # A fixed nonunitary memory operation retains coherent feedback and is independent of t.
   if j%2:
    M=np.kron(np.kron(I,Z),I);out=.87*out+.13*M@out@M
  return out
 ref=run(0)
 for t in [.001,.02,.2,.9,np.pi]:
  actual=(run(t)+run(-t))/2;dist=np.abs(np.linalg.eigvalsh(actual-ref)).sum()/2
  bound=min(1,J*J*t*t/4);sinebound=min(1,np.pi**2*J*J*np.sin(t/2)**2/4)
  assert dist<=bound+1e-12 and dist<=sinebound+1e-12
  rows.append({'J':J,'t':t,'complete_PM_reference_distance':float(dist),'Taylor_bound':bound,'sine_bound':sinebound})
# Independent qubit-Choi projector formulation of arbitrary decoder inequality.
checks=0;minslack=1.;constant_cases=0
for N in [1,3,17,256,4096]:
 for J in [1,2,7,32]:
  d=1/(4*max(J,np.sqrt(N)));target=(1/(8*np.pi**2))*min(1,J*J/N)
  overlaplower=(1-np.sqrt(N)*np.sin(2*d))*(1-abs(np.cos(2*J*d)))/2
  assert overlaplower>=target-1e-14;constant_cases+=1
  targets=[]
  for sign in [1,-1]:
   U=np.diag(np.exp(1j*sign*J*d*np.array([1,-1])));v=np.kron(U,I)@bell;targets.append(np.outer(v,v.conj()))
  assert abs(np.linalg.eigvalsh(targets[0]+targets[1])[-1]-(1+abs(np.cos(2*J*d))))<1e-12
  for k in range(24):
   q=unitary(8)[:,:2];Ks=[q[2*l:2*l+2] for l in range(4)];choi=sum(np.outer(np.kron(K,I)@bell,(np.kron(K,I)@bell).conj()) for K in Ks)
   es=[1-np.trace(choi*T).real for T in targets];slack=sum(es)-(1-abs(np.cos(2*J*d)))
   assert slack>=-1e-12;minslack=min(minslack,slack);checks+=1
out={'status':'PASS_COMPLETE_COHERENT_FEEDBACK_REUSE_AND_ARBITRARY_DECODER_LOWER_FIXTURES','complete_feedback_cases':rows,'general_CPTP_Choi_checks':checks,'minimum_decoder_slack':float(minslack),'minimax_constant_cases':constant_cases,'source_draws':0,'scope':'Floating matrix stress checks with full retained source memory/reference and nonunitary feedback; analytic proof supplies general complete norm bound. Not acquired data.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='complete_feedback_cases'},indent=2))
