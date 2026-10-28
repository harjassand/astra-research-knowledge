#!/usr/bin/env python3
"""Exact rational midpoint/future-memory lower-bound fixtures; no draws."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
import sympy as S
X=S.Matrix([[0,1],[1,0]]);Z=S.diag(1,-1);I=S.eye(2)
def Q(x):return S.Rational(x.numerator,x.denominator)
fixtures=[];matrix_checks=0
for r in [F(1,100),F(1,40),F(1,20),F(1,16)]:
 c=(1-r*r)/(1+r*r);s=2*r/(1+r*r);tau2=4*s*s;p=(2*c*s)**2
 assert c*c+s*s==1 and tau2<=F(1,16)
 assert p==tau2*(1-tau2/4) and p<F(1,2)
 for sign in [-1,1]:
  V=Q(c)*I-S.I*sign*Q(s)*Z
  W=Q(c*c-s*s)*I-S.I*sign*Q(2*c*s)*Z
  A=V*X*V.conjugate().T;B=W*X*W.conjugate().T
  assert S.simplify(V*V.conjugate().T-I)==S.zeros(2)
  assert S.simplify(W*W.conjugate().T-I)==S.zeros(2)
  assert S.simplify((A-X)**2-Q(tau2)*I)==S.zeros(2)
  assert S.simplify((A-B)**2-Q(tau2)*I)==S.zeros(2)
  assert S.simplify(W*Z*W.conjugate().T-Z)==S.zeros(2)
  matrix_checks+=5
 for q in [1,2,4,8,16,32,128]:
  ws=[(1-p)**(q-k)*p**k for k in range(q+1)]
  assert max(ws)==(1-p)**q
  assert sum(F(comb(q,k))*ws[k] for k in range(q+1))==1
  floor=1-(1-p)**q
  assert floor>=1-(1-tau2/4)**q
  fixtures.append({'q':q,'stereographic_r':str(r),'tau_squared':str(tau2),'p':str(p),'lower_float':float(floor)})
result={'status':'PASS exact rational midpoint floor','source_draws':0,'rng_draws':0,'exact_matrix_identities':matrix_checks,'finite_q_fixtures':len(fixtures),'fixtures':fixtures}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='fixtures'},indent=2))
