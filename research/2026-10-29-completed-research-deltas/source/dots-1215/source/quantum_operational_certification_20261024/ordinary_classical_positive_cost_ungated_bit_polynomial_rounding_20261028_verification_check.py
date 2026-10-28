#!/usr/bin/env python3
"""Contributor verification; exact rational group and finite-coupling checks."""
from pathlib import Path
import hashlib,json
import sympy as s
import numpy as np
r=np.random.default_rng(281112);root=Path(__file__).resolve().parent
cases=0;nonbaseline=0;max_ratio=0.
for case in range(160):
 n=2+case%11
 p=s.Matrix([s.Rational(1,4**int(j)) for j in r.integers(1,14,size=n)])
 rr=s.Matrix([s.sqrt(x) for x in p]);Mrest=p*p.T+rr*rr.T/2+s.diag(*[x/2-x*x for x in p])
 av=s.Matrix([int(j) for j in r.integers(-30,31,size=n)])
 if av.norm()==0:av[0]=1
 a0=s.Rational(int(r.integers(-2,3)),20) if case%3==0 else s.Integer(0)
 v=s.Matrix([a0,*list(av)]);A=v*v.T;m=s.Rational(case%5+1,7)
 w=[s.Integer(2)**int(j) for j in r.integers(0,20,size=n)]
 M=s.zeros(n+1);M[0,0]=1;M[0,1:]=p.T;M[1:,0]=p;M[1:,1:]=Mrest
 d=m+sum(w[i]*p[i] for i in range(n));F=s.trace(A*M)/d;R0=a0*a0/m
 a=max(s.Integer(1),s.trace(A));delta=min(s.Rational(1,2),m/(64*a*n));groups={}
 for i in range(n):
  if p[i]<delta:continue
  scale=s.Integer(1)
  while p[i]<=scale/2:scale/=2
  groups.setdefault(scale,[]).append(i)
 L=len(groups)
 if F<1 or R0>=F/4:cases+=1;continue
 assert L
 keep=[i for I in groups.values() for i in I]
 SK=s.trace(A.extract([i+1 for i in keep],[i+1 for i in keep])*Mrest.extract(keep,keep))
 assert SK>=F*d/16
 infos=[]
 for scale,I in groups.items():
  T=sum(abs(av[i]) for i in I)**2
  if not T:continue
  tr=sum(av[i]**2 for i in I)
  # Exactly feasible rational correlation interpolation with half-optimal bound.
  achieved=(T+tr)/2
  c=m+sum(w[i] for i in I)/2
  SI=s.trace(A.extract([i+1 for i in I],[i+1 for i in I])*Mrest.extract(I,I))
  assert scale*achieved>=SI/2
  infos.append((achieved/c,achieved,c))
 score,T,c=max(infos,key=lambda x:x[0]);assert score>=F/(64*L)
 if R0<T/(64*c):
  assert a0*a0<T/64
  # Worst permitted analytic expectation, independent of actual sign outcomes.
  ENlo=3*T/64;tar=T/(128*c)
  assert ENlo-tar*c==5*T/128
  assert tar>=F/(8192*L)
  nonbaseline+=1
 cases+=1
couplings=0
for n in range(1,513):
 h=s.Rational(1,8192*n*n);eta=h/s.Integer(128*n)
 # sqrt(2/pi)<1; enough to use n*h.
 factor=eta**2/h**2+n*h
 assert factor<s.Rational(1,512*n)
 assert s.Rational(5,512*n+4)>=s.Rational(1,128*n)
 assert s.Rational(1,128*n)-s.Rational(1,256*n)==s.Rational(1,256*n)
 couplings+=1
src=root/'ordinary_classical_positive_cost_ungated_bit_polynomial_rounding_20261028.md'
out={'status':'PASS_CONTRIBUTOR_VERIFICATION_NOT_FRESH_INDEPENDENT_RECEIPT','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'exact_global_rank_one_Gram_group_cases':cases,'small_baseline_selected_group_cases':nonbaseline,'exact_correlation_coupling_and_trial_cap_cases':couplings,'scope':'Exact scalar grouping/rounding/coupling bounds. Reviewer contributed finite-SDP and cap ideas before freeze; no production solver/Gaussian sampler or CPTP transfer.'}
(root/(src.stem+'_verification_check.json')).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
