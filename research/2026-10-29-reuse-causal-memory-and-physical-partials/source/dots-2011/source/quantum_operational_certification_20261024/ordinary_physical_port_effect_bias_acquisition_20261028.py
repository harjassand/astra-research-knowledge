#!/usr/bin/env python3
"""Exact positive-effect/negative-map error-record witness and physical signed moments."""
import itertools,json,hashlib
from pathlib import Path
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
R=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
assert R.H*R==I
P0=s.diag(1,0);P1=s.diag(0,1)
def k(*a):
 out=s.ones(1,1)
 for x in a:out=s.kronecker_product(out,x)
 return out
def mm(a,b):
 z=s.zeros(2);z[a,b]=1;return z
rows=[];entries=0
for p in [s.Rational(1,100),s.Rational(1,4),s.Rational(49,100)]:
 for a,b in itertools.product(range(2),repeat=2):
  om=mm(a,b);F0=(1-p)*k(om,P0);F1=p*k(om,P1);T=F0+F1
  for sigma,chi in [(I,1),(X,1),(Z,-1)]:
   actual=k(R*(sigma/2)*R.H,F0)+k(R*X*(sigma/2)*X*R.H,F1)
   H=F0+chi*F1;target=k(R*sigma*R.H/2,H)
   assert actual==target;entries+=64
   red=s.zeros(2)
   for x,y in itertools.product(range(2),repeat=2):red[x,y]=sum(actual[4*x+j,4*y+j] for j in range(4))
   assert red==R*sigma*R.H*s.trace(om)*(1-p+chi*p)/2;entries+=4
 # One positive memory input suffices to disprove map positivity/CP domination.
 om=P0;F0=(1-p)*k(om,P0);F1=p*k(om,P1);H=F0-F1;T=F0+F1
 assert H[1,1]==-p and (F0-(1-p)*T)[1,1]==-p*(1-p)
 rows.append({'p':str(p),'X_effect_bias':'1','Z_effect_bias':str(1-2*p),'signed_map_negative_entry':str(-p),'good_minus_scaled_total_negative_entry':str(-p*(1-p))})
# Explicit arbitrary error-dependent TP updates preserve effects but not map order.
K=[s.diag(s.Rational(3,5),s.Rational(4,5)),s.Matrix([[0,s.Rational(3,5)],[s.Rational(4,5),0]])]
assert sum((A.H*A for A in K),s.zeros(2))==I
ps=[s.Rational(1,10),s.Rational(2,5)];U=[X,s.Matrix([[1,0],[0,s.I]])]
Ebad=sum((p*A.H*A for p,A in zip(ps,K)),s.zeros(2));Aeff=I-2*Ebad
assert all(x>=0 for x in Aeff.diagonal())
assert all(s.Rational(2,5)-x>=0 for x in Ebad.diagonal())
# Construct the adjoint effects directly from tagged Kraus columns, including f-dependent U.
effects=[]
for f in [0,1]:
 e=s.zeros(2)
 for p,A,B in zip(ps,K,U):
  weight=(p if f else 1-p);J=(B if f else I)*A
  e+=weight*J.H*J
 effects.append(e)
assert effects[1]==Ebad and effects[0]+effects[1]==I
assert Aeff==s.diag(s.Rational(52,125),s.Rational(73,125))
out={'status':'PASS_EFFECT_ONLY_PHYSICAL_ACQUISITION_WITH_RETAINED_ERROR_RECORD',
 'source_outcomes':0,'rng_draws':0,'full_and_reduced_signed_memory_entries':entries,
 'tagged_error_cases':rows,'error_dependent_TP_memory_update_effect':str(Aeff),
 'scope':'exact hypothesis-separation and conditional-moment fixtures; finite learner is justified by the manuscript hypothesis audit, not sampled here',
 'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_suffix('.md')]}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
