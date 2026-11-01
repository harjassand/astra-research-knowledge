#!/usr/bin/env python3
"""Independent exact full-generator and all-u finite-jump certificates."""
from pathlib import Path
import hashlib
import json
import sympy as s

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
SOURCE='ACTUAL_INVERSE_CUBIC_PROGRESS.md'
EXPECTED='d0a69858857cb54b2127fd7b79204bc9f0f2529eaae67040ba052dbd24d62719'
actual=hashlib.sha256((ROOT/SOURCE).read_bytes()).hexdigest()
assert actual==EXPECTED,(actual,EXPECTED)
A,B,C,D,E,L,Z=s.symbols('A B C D E L Z',nonnegative=True)
rates=[1,A,A*(A-1),A*C,A*(A-1),A*D,A*(A-1),A*E,A*E,2*C*D,C*D,A*B]
deltas=[(1,0,0,0,0),(-1,0,0,0,0),(-1,0,1,0,0),(1,0,-1,0,0),
        (-1,0,0,1,0),(1,0,0,-1,0),(-1,0,0,0,1),(1,0,0,0,-1),
        (-1,0,1,1,-1),(1,0,-1,-1,1),(1,1,-1,-1,0),(-1,-1,1,1,0)]
marks=[h[4]-s.Rational(h[0],2) for h in deltas]
assert marks==list(map(s.Rational,['-1/2','1/2','1/2','-1/2','1/2','-1/2','3/2','-3/2','-1/2','1/2','-1/2','1/2']))
assert max(map(abs,marks))==s.Rational(3,2)
assert [sum(h) for h in deltas]==[1,-1]+[0]*10
gu=s.expand(sum(r*h for r,h in zip(rates,marks)))
qu=s.expand(sum(r*h*h for r,h in zip(rates,marks)))
gu_expected=s.Rational(5,2)*A*A-2*A-s.Rational(1,2)+A*((B-C-D)/2-2*E)+C*D/2
qu_expected=s.Rational(1,4)+A/4+s.Rational(11,4)*A*(A-1)+A*(C+D)/4+s.Rational(5,2)*A*E+s.Rational(3,4)*C*D+A*B/4
assert s.expand(gu-gu_expected)==0
assert s.expand(qu-qu_expected)==0
assert s.expand(((L-A)**2-Z**2/4).subs({L:A+(C+D)/2,Z:C-D})-C*D)==0
assert s.Rational(9,10)**2-s.Rational(1,10)**2/4==s.Rational(323,400)
assert s.Rational(323,400)>=s.Rational(4,5)
progress_slack=s.Rational(5,2)*A*A-2*A+2*A*(B/5-E)+A*A+(C*D/8-A*L)+(C*D-4)/8
assert s.expand(gu-A*B/10-C*D/4-progress_slack.subs(L,A+(C+D)/2))==0
q_slack=(C*D-4)/16+A*(B-100)/400+(11*A/4)*(B/100-A+1)+(A/4)*(B/5-C-D)+(5*A/2)*(B/5-E)
assert s.expand(s.Rational(83,100)*A*B+s.Rational(13,16)*C*D-qu-q_slack)==0
assert s.expand(9*(A*B/10+C*D/4)-(s.Rational(83,100)*A*B+s.Rational(13,16)*C*D)-(s.Rational(7,100)*A*B+s.Rational(23,16)*C*D))==0

u,z=s.symbols('u z',positive=True)
jump_certificates=[]
for h in sorted(set(marks)):
 gap=-3*h/u**4+6*h*h/(u-s.Rational(3,2))**5-((u+h)**-3-u**-3)
 num,den=s.fraction(s.factor(s.together(gap.subs(u,100+z))))
 p=s.Poly(num,z)
 assert all(c>=0 for c in p.all_coeffs())
 # All denominator factors after u=100+z have positive coefficients.
 den_poly=s.Poly(den,z)
 assert all(c>0 for c in den_poly.all_coeffs())
 jump_certificates.append({'h':str(h),'numerator_coefficients_descending':[str(c) for c in p.all_coeffs()],
                           'positive_denominator':str(s.factor(den)),
                           'all_u_at_least_100':True})
ratio=54*u**4/(u-s.Rational(3,2))**5
assert s.simplify(s.diff(s.log(ratio),u)+(u+6)/(u*(u-s.Rational(3,2))))==0
threshold=s.factor(ratio.subs(u,100))
assert threshold<1
scalar_margin=50*197**5-27*200**5
assert scalar_margin==6195464037850>0
entrance_margin=11*99**3-10*100**3
assert entrance_margin==673289>0

# Scope counterexample: basic gates alone do not imply U>=.99E.
x={A:400,B:40000,C:3600,D:3600,E:1000}
lv=4000; uv=800; nv=48600
assert x[B]>=100 and 5*x[E]<=x[B] and 10*lv<=x[B]
assert 10*x[A]<=lv and abs(x[C]-x[D])*10<=lv and x[C]*x[D]>=4 and uv>=100
assert x[E]**2<=2*nv*lv and 100*uv<99*x[E]

result={
 'scope':'conditional actual stopped-domain time budget only; no admission, clearance, CLT or algorithm',
 'source_sha256':{SOURCE:actual},
 'status':'PASS_NO_REPAIR',
 'U_marks':[str(h) for h in marks],
 'GU':str(gu),'qU':str(qu),
 'CD_geometry_constant':'323/400',
 'progress_nonnegative_slack':str(progress_slack),
 'bracket_nonnegative_slack':str(q_slack),
 'all_u_finite_jump_certificates':jump_certificates,
 'scalar_ratio_at_100':str(threshold),'scalar_integer_margin':scalar_margin,
 'entrance_scaling_integer_margin':entrance_margin,
 'basic_gate_counterexample_U_over_E':'4/5',
 'all_assertions_passed':True,
}
(HERE/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
