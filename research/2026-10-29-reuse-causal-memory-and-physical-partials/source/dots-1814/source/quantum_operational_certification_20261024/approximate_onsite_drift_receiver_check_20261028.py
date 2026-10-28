#!/usr/bin/env python3
"""Time-ordered local-crosstalk, fixed-tube drift and record-TV fixtures. Zero draws."""
import itertools,json,math
import numpy as np
from scipy.linalg import expm
from fractions import Fraction as F
from pathlib import Path
P=[np.eye(2,dtype=complex),np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.]).astype(complex)]
def kron(xs):
 r=np.ones((1,1),complex)
 for x in xs:r=np.kron(r,x)
 return r
def at(n,i,j):return kron([P[j] if k==i else P[0] for k in range(n)])
def op(x):return float(np.linalg.norm(x,2))
def trL(W,d,g):return np.trace(W.reshape(d,g,d,g),axis1=0,axis2=2)
maxr={'time_ordered_commutator_bound':0.,'local_incident_bound':0.,'uniform_memory_bell_bound':0.,'drift_averaged_cone':0.}
fixtures=[]
for q,gq in [(1,1),(1,2),(2,1),(2,2)]:
 n=q+gq;d=2**q;g=2**gq
 vs=[expm(-.07j*(i+1)*P[2]) for i in range(q)]
 U0=kron(vs+[P[0]]*gq);hist=[]
 for h in range(6):
  segments=[];incident=np.zeros(q)
  for seg in range(3):
   H=(13+7*h+11*seg)*at(n,q,1+(seg%3)) # large bath-only term, no incident charge
   if gq>1:H+=17*at(n,q,2)@at(n,q+1,3)
   for i in range(q):
    coupling=.08+.01*((h+i+seg)%3)
    H+=coupling*at(n,i,1+(seg%3))@at(n,q,1+((seg+1)%3))
    incident[i]+=.09*coupling
   segments.append((.09,H))
  W=np.eye(d*g,dtype=complex)
  for dt,H in segments:W=expm(-1j*dt*H)@W
  U=W@U0;taus=[];boundtau=[]
  for i in range(q):
   for j in [1,3]:
    A=U0@at(n,i,j)@U0.conj().T;B=U@at(n,i,j)@U.conj().T
    tau=op(B-A);bound=sum(dt*op(H@A-A@H) for dt,H in segments)
    local=2*incident[i]
    maxr['time_ordered_commutator_bound']=max(maxr['time_ordered_commutator_bound'],tau-bound)
    maxr['local_incident_bound']=max(maxr['local_incident_bound'],bound-local)
    taus.append(tau);boundtau.append(local)
  Wextract=U0.conj().T@U;K=trL(Wextract,d,g)/d;TI=K.conj().T@K
  worst=1-np.linalg.eigvalsh(TI).min();b=sum(t*t for t in boundtau)/4
  maxr['uniform_memory_bell_bound']=max(maxr['uniform_memory_bell_bound'],worst-b)
  hist.append((U,boundtau));fixtures.append({'q':q,'gauge_qubits':gq,'history':h,'largest_exact_tau':max(taus),'largest_local_tau':max(boundtau),'worst_gauge_loss':worst,'local_uniform_upper':b})
 # Actual h-dependent encodings and positive h-dependent gauges with same fixed A.
 for i in range(q):
  for j in [1,3]:
   delta=np.zeros((d*g,d*g),complex);lambar=0.;tmax=0.
   for h,(U,bt) in enumerate(hist):
    lam=.07+.11*h;lambar+=lam/len(hist)
    gh=kron([(P[0]+(.16+.01*h)*P[1]+.12*P[2]+.05*P[3])/2]*gq)
    delta+=lam*(U@np.kron(at(q,i,j)/d,gh)@U.conj().T)/len(hist)
    tmax=max(tmax,bt[2*i+(j==3)])
   A=U0@at(n,i,j)@U0.conj().T
   radial=np.trace(A@delta).real
   maxr['drift_averaged_cone']=max(maxr['drift_averaged_cone'],lambar*(1-tmax*tmax/2)-radial)
# Exact record-distribution transfer, with arbitrary record-dependent actual future states licensed by the uniform bound.
tvfixtures=[]
for k in [1,2,3,4]:
 p=[F(1,2),F(1,3),F(1,6)];eta=F(k,100)
 physical=[p[0]-eta,p[1],p[2]+eta];tv=sum(abs(a-b) for a,b in zip(p,physical))/2
 assert tv==eta
 beta=p[2];b=F(1,20);nu=F(1,50)
 # On each good record any actual source memory is bounded by b; bad record costs one.
 risk=physical[0]*b+physical[1]*b+physical[2]
 actual=risk+nu*(1-risk)
 assert actual<=b+beta+eta+nu
 tvfixtures.append({'calibration_tv':str(tv),'physical_bad_mass':str(physical[2]),'actual_risk':str(actual),'bound':str(b+beta+eta+nu)})
assert max(maxr.values())<2e-11,maxr
result={'status':'PASS time-ordered drift and actual-record transfer checks','source_draws':0,'rng_draws':0,'time_ordered_history_fixtures':len(fixtures),'segments_per_history':3,'exact_record_transfer_fixtures':len(tvfixtures),'maximum_positive_residuals':maxr,'fixtures':fixtures,'record_transfer_fixtures':tvfixtures}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['fixtures','record_transfer_fixtures']},indent=2))
