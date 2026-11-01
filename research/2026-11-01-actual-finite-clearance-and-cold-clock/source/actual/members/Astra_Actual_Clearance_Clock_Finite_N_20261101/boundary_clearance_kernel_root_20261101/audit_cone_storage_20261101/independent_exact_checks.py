#!/usr/bin/env python3
"""Independent literal marks and exact algebra; no author-code imports."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
EXPECTED={
 "CONE_WEIGHTED_CLOCK_DERIVATIVES.md":"2293739c573815ba5cfcf721ed020a71fbb24047f95d348a50f4fbd005ea6847",
 "HISTORY_SOURCE_STORAGE_V1_221a66ea.md":"221a66ea00b3bcfa8179def2e43cbe0310b0705090aa23e8f4c9cb413a0cac50",
 "UNWEIGHTED_SOURCE_STORAGE.md":"13af680297269e41d9b02e6cc09a43e9b65781493391484002841bf712643700",
}
hashes={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in EXPECTED}
assert hashes==EXPECTED,(hashes,EXPECTED)
A,B,C,D,E=s.symbols('A B C D E', integer=True, nonnegative=True)
rates=[1,A,A*(A-1),A*C,A*(A-1),A*D,A*(A-1),A*E,A*E,2*C*D,C*D,A*B]
# Coordinates A,B,C,D,E; enter literal directed reactions independently.
deltas=[(1,0,0,0,0),(-1,0,0,0,0),(-1,0,1,0,0),(1,0,-1,0,0),
        (-1,0,0,1,0),(1,0,0,-1,0),(-1,0,0,0,1),(1,0,0,0,-1),
        (-1,0,1,1,-1),(1,0,-1,-1,1),(1,1,-1,-1,0),(-1,-1,1,1,0)]
marks=[h[0]-2*h[4] for h in deltas]
assert marks==[1,-1,-1,1,-1,1,-3,3,1,-1,1,-1]
assert max(map(abs,marks))==3
assert [sum(h) for h in deltas]==[1,-1]+[0]*10
drift=s.expand(sum(r*m for r,m in zip(rates,marks)))
bracket=s.expand(sum(r*m*m for r,m in zip(rates,marks)))
expected_drift=1+4*A-5*A*A+A*(C+D-B+4*E)-C*D
expected_bracket=1+A+11*A*(A-1)+A*(C+D)+10*A*E+3*C*D+A*B
assert s.expand(drift-expected_drift)==0
assert s.expand(bracket-expected_bracket)==0
K=B/2-C-D-4*E
drift_slack=5*A*(A-1)+A+A*K
bracket_slack=A*(11*(B-A)+K+6*(B/8-E)+7*B/4+10)
assert s.expand((1-A*B/2-C*D)-drift-drift_slack)==0
assert s.expand((1+15*A*B+3*C*D)-bracket-bracket_slack)==0
assert s.expand((1+30*(A*B/2+C*D))-(1+15*A*B+3*C*D)-27*C*D)==0
g,e,z,l,J,Kll=s.symbols('g e z l J Kll', positive=True)
kle=g**-3+s.Rational(9,14)*g**-4+s.Rational(3,14)*g**-6
kee=s.Rational(3,10)*g**-3+(s.Rational(3,2)+1/(2*g*g))*kle
constants={
 "bl":s.Rational(1,5)*g**-3,
 "be":s.Rational(1,2)*g**-2,
 "bll":s.Rational(3,7)*g**-4,
 "ble":kle,"bee":kee,
}
padded={k:s.simplify(v.subs(g,s.Rational(1,2))) for k,v in constants.items()}
assert padded=={'bl':s.Rational(8,5),'be':s.Integer(2),'bll':s.Rational(48,7),'ble':s.Integer(32),'bee':s.Rational(572,5)}
assert s.integrate((g*z*z)**-3,(z,e,s.oo))==1/(5*g**3*e**5)
assert s.integrate(3*(g*z*z)**-4,(z,e,s.oo))==3/(7*g**4*e**7)
# Differentiate b_e=3e/2-alpha*J using exact formal chain rules.
alpha=s.Rational(3,2)*e+1/(2*l*l)
bl=J-1
ble=J/l**3-alpha*Kll
be=s.Rational(3,2)*e-alpha*J
formal_l=s.diff(be,l)+s.diff(be,J)*Kll
formal_e=s.diff(be,e)+s.diff(be,J)*ble
assert s.simplify(formal_l-ble)==0
assert s.simplify(formal_e-(-s.Rational(3,2)*bl-alpha*ble))==0
S,d=s.symbols('S d',positive=True)
assert s.simplify(S*S/(2*(d+61*S))-S/124-S*(S-d)/(124*(d+61*S)))==0

# Finite enabled-jump sanity checks supplement exact polynomial certificates.
states=0; targets=0
for b in range(1,25):
 for a in range(b+1):
  for ee in range(b//8+1):
   for cc in range(b//2-4*ee+1):
    for dd in range(b//2-4*ee-cc+1):
     states+=1
     rs=[1,a,a*(a-1),a*cc,a*(a-1),a*dd,a*(a-1),a*ee,a*ee,2*cc*dd,cc*dd,a*b]
     em=max(1,ee)
     x=(a,b,cc,dd,ee)
     gw=sum(r*m for r,m in zip(rs,marks))
     qw=sum(r*m*m for r,m in zip(rs,marks))
     assert F(gw)<=1-F(a*b,2)-cc*dd
     assert qw<=1+15*a*b+3*cc*dd
     for rate,h,mark in zip(rs,deltas,marks):
      if rate<=0: continue
      y=tuple(xx+hh for xx,hh in zip(x,h))
      assert min(y)>=0
      assert y[4]<=em+1
      assert y[0]+2*(em+1-y[4])>=0
      assert (y[0]-2*y[4])-(a-2*ee)==mark
      targets+=1

result={
 "scope":"exact cone algebra and stopped storage identities; no admission or clearance",
 "source_sha256":hashes,
 "padded_cone_constants":{k:str(v) for k,v in padded.items()},
 "storage_marks":marks,
 "storage_drift":str(drift),"storage_bracket":str(bracket),
 "drift_nonnegative_slack":str(drift_slack),
 "bracket_nonnegative_slack":str(bracket_slack),
 "checked_integer_domain_states":states,"checked_enabled_targets":targets,
 "asymptotic_original_status":"requires additional W0+d scaling; exact theorem passes",
 "repaired_status":"PASS with fixed/conditionally bounded initial storage and stated S0=Theta(nu N) hypothesis",
 "history":"Initial hash check rejected concurrent parent repair; original and complete repair diff were inspected, both exact versions now bound.",
 "small_initial_storage_counterexample":{"W0":2,"d":1,"Qbar":6,"x":3,"tail_exponent":"9/368"},
 "all_assertions_passed":True,
}
(HERE/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
