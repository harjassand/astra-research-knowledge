#!/usr/bin/env python3
"""Exact independent physical Kraus/channel check, including unknown entangling output mixers."""
import json
from pathlib import Path
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
def kron(xs):
 r=s.ones(1,1)
 for x in xs:r=s.kronecker_product(r,x)
 return r
def rot(P,t):
 c=(1-t*t)/(1+t*t);a=2*t/(1+t*t)
 return c*s.eye(P.rows)-s.I*a*P
vs=[rot(kron([X,Y,Z]),s.Rational(1,5)),rot(kron([Z,Z,X]),s.Rational(2,9))*rot(kron([X,I,Y]),s.Rational(1,7))]
enc=s.zeros(8,2);enc[0,0]=1;enc[7,1]=1
es=[0,4,2,1];Um=s.zeros(8)
for l in range(2):
 for g,e in enumerate(es):Um[7*l^e,4*l+g]=1
errs=[kron([X if (f>>(2-k))&1 else I for k in range(3)]) for f in range(8)]
ps=[s.Rational(1,101),s.Rational(2,17),s.Rational(1,3),s.Rational(9,20)]
fixtures=[];entries=0
for vi,V in enumerate(vs):
 assert V.H*V==s.eye(8)
 U=V*Um;assert U.H*U==s.eye(8)
 BX=U*s.kronecker_product(X,s.eye(4))*U.H;BZ=U*s.kronecker_product(Z,s.eye(4))*U.H
 assert s.simplify(BX*BZ+BZ*BX)==s.zeros(8)
 assert s.simplify(BX*BX)==s.eye(8) and s.simplify(BZ*BZ)==s.eye(8)
 for p in ps:
  wf=[p**f.bit_count()*(1-p)**(3-f.bit_count()) for f in range(8)]
  GI=s.diag(*[wf[e] for e in es]);GX=s.diag(*[wf[7^e] for e in es]);G=GI+GX
  kap=1-2*p;r=p*(1-p)/2;gamma=kap*r;loss=3*p*p-2*p*p*p
  assert min(G.diagonal())/2==r and min((GI-GX).diagonal())/2==gamma
  assert all(v>=0 for v in (GI-GX-kap*G).diagonal())
  assert all(v>=0 for v in (GI-GX).diagonal())
  assert s.trace(GX)==loss and s.trace(GI)==1-loss
  # Independent physical Kraus expression on all coherent logical matrix units.
  for a in range(2):
   for b in range(2):
    E=s.zeros(2);E[a,b]=1
    physical=s.zeros(8)
    encoded=enc*E*enc.H
    for f in range(8):physical+=wf[f]*(errs[f]*encoded*errs[f].H)
    physical=V*physical*V.H
    model=U*(s.kronecker_product(E,GI)+s.kronecker_product(X*E*X,GX))*U.H
    assert physical==model
    entries+=64
    decoded=U.H*physical*U
    reduced=s.zeros(2)
    for l in range(2):
     for m in range(2):reduced[l,m]=sum(decoded[4*l+g,4*m+g] for g in range(4))
    assert s.simplify(reduced-((1-loss)*E+loss*X*E*X))==s.zeros(2)
  # Known class upper p<=49/100 supplies coarse kappa0=1/50, not actual p.
  k0=s.Rational(1,50);assert k0<=kap
  assert all(v>=0 for v in (GI-GX-k0*G).diagonal())
  fixtures.append({'mixer':vi,'p':str(p),'actual_margin':str(kap),'supplied_class_margin':str(k0),'patch_floor':str(r),'signed_gap':str(gamma),'oracle_loss':str(loss)})
out={'status':'PASS exact coherent physical-noise witness with entangling mixers','source_draws':0,'rng_draws':0,'nontrivial_exact_rational_output_mixers':len(vs),'physical_channel_cases':len(fixtures),'full_coherent_output_entries_checked':entries,'decoded_logical_matrix_unit_cases':4*len(fixtures),'fixtures':fixtures}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='fixtures'},indent=2))
