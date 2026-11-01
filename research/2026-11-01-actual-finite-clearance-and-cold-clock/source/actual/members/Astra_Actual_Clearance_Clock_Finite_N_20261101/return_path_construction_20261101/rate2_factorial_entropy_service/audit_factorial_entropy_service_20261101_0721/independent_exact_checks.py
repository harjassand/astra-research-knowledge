#!/usr/bin/env python3
"""Independent exact diagnostics. Ordinary proof is in MATHEMATICAL_REVIEW.md.

No author code is imported; no numerical square-root/log sampling is used.
The finite integer checks are supplemental, not a proof of a uniform theorem.
"""
import hashlib
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent
checks = 0
def check(condition, label):
    global checks
    assert bool(condition), label
    checks += 1
def zero(expression, label):
    check(sp.simplify(expression) == 0, label)
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

freeze = json.loads((ROOT/'inputs/AUTHOR_FREEZE.json').read_text())
for name, meta in freeze['files'].items():
    check(digest(ROOT/'inputs'/name) == meta['sha256'], ('snapshot hash', name))
    check((ROOT/'inputs'/name).stat().st_size == meta['bytes'], ('snapshot bytes',name))
    check(digest(SOURCE/name) == meta['sha256'], ('source unchanged',name))
check(digest(ROOT/'inputs/FACTORIAL_ENTROPY_OUTPUT_SERVICE.md') ==
      'bc5e25aacdeddf99d5e01a4429bd83dfad5b547a86b653cad0a1fcf161522bd9', 'requested source')
harmonic = SOURCE.parent/'rate2_explicit_macro_removal/EXPLICIT_HARMONIC_PERSISTENCE_AND_REMOVAL.md'
check(digest(harmonic) == freeze['source_dependencies']['accepted_harmonic_source'], 'harmonic source')

A,B,C,D,E = x = sp.symbols('A B C D E', nonnegative=True, integer=True)
rt = sp.sqrt(7)
s = (rt-1)/2
t = 2-s
alpha = sp.Rational(2,9)
q = (alpha,alpha*s*s,alpha*s,alpha*s,alpha*t)
# Independently entered literal ten actual binary channels.
aa,ac,ad,ae,cd,ab = [(2,0,0,0,0),(1,0,1,0,0),(1,0,0,1,0),
                    (1,0,0,0,1),(0,0,1,1,0),(1,1,0,0,0)]
actual = [(aa,ac,1),(ac,aa,1),(aa,ad,1),(ad,aa,1),(aa,ae,1),
          (ae,aa,1),(ae,cd,1),(cd,ae,2),(cd,ab,1),(ab,cd,1)]
competitor = [(aa,ac,s),(ac,aa,1),(aa,ad,s),(ad,aa,1),(aa,ae,1),
              (ae,aa,1),(ae,cd,1),(cd,ae,2),(cd,ab,1),(ab,cd,1),(aa,cd,1-s)]
def mon(values,y):
    return math.prod(a**n for a,n in zip(values,y))
def falling(values,y):
    return math.prod(math.prod(a-j for j in range(n)) for a,n in zip(values,y))
zero(sum(q)-1,'q sum')
zero(2*s*s+2*s-3,'quadratic identity')
check(0<s<1,'s range')
check(q[1]>sp.Rational(1,7),'q minimum lower bound')
check(all(q[1]<=v<=q[4] for v in q),'q min/max')
check(t/(s*s)<2,'q ratio')
for y in [aa,ac,ad,ae,cd,ab]:
    zero(sum(k*mon(q,u) for u,v,k in competitor if u==y)-
         sum(k*mon(q,u) for u,v,k in competitor if v==y), ('complex balance',y))
for i in range(5):
    zero(sum(k*falling(x,y)*(z[i]-y[i]) for y,z,k in actual)-
         sum(k*falling(x,y)*(z[i]-y[i]) for y,z,k in competitor), ('drift equivalence',i))

expected_shift = [A-C-1,2*A,A-D-1,2*A,A-E-1,2*A,C+D+1,A+E+1,A+B+1,C+D+1,C+D+1]
expected_weight = [1,s,1,s,1/t,t,t/(s*s),2*s*s/t,1,1,(1-s)/(s*s)]
envelope = [sp.Integer(0)]*6
rows = []
for j,(y,z,k) in enumerate(competitor):
    target = tuple(a+v-u for a,u,v in zip(x,y,z))
    shift = sp.expand(falling(target,z)-falling(x,z))
    weight = sp.simplify(k*mon(q,y)/mon(q,z))
    zero(shift-expected_shift[j],('shift',j))
    zero(weight-expected_weight[j],('weight',j))
    for i,var in enumerate(x): envelope[i] += weight*abs(shift.coeff(var))
    envelope[5] += weight*abs(shift.subs(dict.fromkeys(x,0)))
    rows.append({'edge':f'{y}->{z}','shift':str(shift),'weight':str(weight)})
for value,wanted in zip(envelope,[8+rt,1,4,4,2,8]):
    zero(value-wanted,'absolute-shift envelope')
check(8+rt<sp.Rational(32,3),'shift scalar bound')
incident = sum(k*mon(q,y) for y,z,k in competitor if y==aa or z==aa)
zero(incident-2*(s+2)*alpha**2,'AA incident flux')
check(s+14<15,'falling/shift remainder')
check(32+sp.Rational(1,9)+sp.Rational(18,32)<33,'full drift constant')

# Formal separable potential: all non-A terms cancel in the comparator difference.
g = [sp.Function('g'+str(i)) for i in range(5)]
def increment(y,z):
    return sum(g[i](x[i]+z[i]-y[i])-g[i](x[i]) for i in range(5))
diff = sum(k*falling(x,y)*increment(y,z) for y,z,k in actual)-sum(k*falling(x,y)*increment(y,z) for y,z,k in competitor)
zero(diff-(1-s)*A*(A-1)*(2*g[0](A-1)-g[0](A-2)-g[0](A)), 'separable comparison identity')

# Coercivity: reciprocal coefficients and the exact path Cauchy remainder.
for a,b,c in [(aa,ac,2*s),(aa,ad,2*s),(aa,ae,3-s),(ae,cd,5-3*s),(cd,ab,2*s*s)]:
    zero(sum(k*mon(q,y)/alpha**2 for y,z,k in competitor if (y,z) in [(a,b),(b,a)])-c,'reciprocal edge')
u,v,w=sp.symbols('u v w', real=True)
zero(6*u*u+5*v*v+3*w*w-(u*u+(u+v)**2+(u+v+w)**2)-
     (2*(u-v)**2+(u-w)**2+(v-w)**2),'path remainder SOS')
for value,lower in [(2*s,sp.Rational(1,3)),(3-s,2),(5-3*s,sp.Rational(5,3)),(2*s*s,1)]:
    check(value>=lower,'coercivity edge lower bound')
zero(1/(6*(1+alpha))-sp.Rational(3,22),'weighted Cauchy coefficient')
check(s<=sp.Rational(5,6),'small-A s bound')
check(sp.Rational(6,5)-sp.Rational(484,5)*sp.Rational(1,1000)>=1,'small-A coercivity margin')
check(44*sp.Rational(1,1000)**2<2*alpha,'small-A output range')
zero(1/(3*alpha**2)-sp.Rational(27,4),'small-A coercivity coefficient')
check(sp.Rational(27,4)>=6,'coercivity six')

# Actual total intensity: a nonnegative-coefficient polynomial certificate.
S=sum(x)
qall=1+A+sum(k*falling(x,y) for y,z,k in actual)
remainder=sp.Poly(sp.expand(3*S*S+1-qall),*x)
check(all(c>=0 for _,c in remainder.terms()),'global rate coefficientwise bound')

# Exact finite count-boundary factorial identities and enabled targets.
states=enabled=disabled=0
for total in range(11):
  for a in range(total+1):
   for b in range(total-a+1):
    for c in range(total-a-b+1):
     for d in range(total-a-b-c+1):
      state=(a,b,c,d,total-a-b-c-d)
      subst=dict(zip(x,state)); states+=1
      check((max(a-1,0))**2<=a*(a-1)<=a*a,'integer falling-root enclosure')
      for j,(y,z,k) in enumerate(competitor):
        source=falling(state,y)
        if not source:
            disabled+=1
            continue
        enabled+=1
        target=tuple(a+v-u for a,u,v in zip(state,y,z))
        check(min(target)>=0,'enabled target nonnegative')
        target_factor=falling(target,z)
        check(target_factor>0,'target factorial positive')
        check(target_factor-falling(state,z)==int(expected_shift[j].subs(subst)),('finite shift',j))
        factorial_ratio=math.prod(F(math.factorial(a),math.factorial(b)) for a,b in zip(target,state))
        check(F(target_factor,source)==factorial_ratio,'exact zero-safe factorial ratio')

def exp_lower(z,n=200):
    term=F(1); total=term
    for j in range(1,n+1):
        term*=z/F(j); total+=term
    return total
check(exp_lower(F(12,5),12)>F(35,4),'initial entropy log bound')
check(exp_lower(F(3),8)>F(585,64),'port positive log bound')
check(exp_lower(F(1),2)>2,'port death e lower bound')
for h,b,wanted in [(5,F(1,2),324480),(8,F(1),823296)]:
    gap=F(h,6)-b
    check(gap>0,'occupation gap')
    check(F(128*h*(4+33*h),3)/(gap*gap)==wanted,'occupation constant')
    xcoeff=F(3,2)*F(1,64)*gap*gap/F(h)
    check(xcoeff==F(1,1920 if h==5 else 3072),'exponential x coefficient')
check((F(1,10)-100*F(1,10**6))*2000>=2,'harmonic storage gap')
check(F(2000)*F(1,2)>=1000,'harmonic lower strip endpoint')
check(F(2000)/(F(1,10**6))>=200000,'harmonic N threshold')
check(F(1,10**6)/8<=F(1,1000),'received floor permitted')
check(F(17,16)+F(1,16)-F(3,4)==F(3,8),'T5 death containment')
check(F(5,4)+F(1,16)-F(3,4)==F(9,16)<F(3,4),'T8 death containment')
check(F(1,32)-F(2,3)*F(1,16)==-F(1,96),'immigration exponent')
check(F(1,2)*F(1,4)**2/F(2)==F(1,64),'T5 lower-tail exponent')
check(F(1)*F(1,4)**2/F(2)==F(1,32),'T8 lower-tail exponent')
examples=[]
for N,ell,lower in [(10**19,46,23),(10**20,48,2200)]:
    check(exp_lower(F(ell))>6*N,'certified log upper')
    X=F(N*N,10**12*1920)-169*N
    check(X>0,'positive entropy tail threshold')
    exponent=X*X/(F(104*5*N*N*ell*ell)+F(4,3)*ell*X)
    check(exponent>lower,'certified exponent')
    examples.append({'N':str(N),'log_upper':ell,'certified_exponent_lower':lower,'exact_exponent_at_log_upper':str(exponent)})
check(F(324480,1)/(F(1,10**12)*10**20)==F(32448,10**7),'polynomial example')
def other_T5_error_upper(N):
    # e^x >= x^6/6! for persistence, e^x >= x for each port tail.
    X=F(N,10**9)
    return F(160*N*N*math.factorial(6),1)/(X**6)+F(64,N)+F(96,N)
check(1-F(32448,10**7)-other_T5_error_upper(10**20)>F(996755,10**6),
      'stated success decimal including every other error')
check(1/exp_lower(F(23))+other_T5_error_upper(10**19)<F(11,10**11),
      'N=1e19 complete failure less than 1.1e-10')

report={'status':'PASS exact supplemental diagnostics; ordinary proof independently reviewed',
        'source_sha256':digest(SOURCE/'FACTORIAL_ENTROPY_OUTPUT_SERVICE.md'),
        'harmonic_dependency_sha256':digest(harmonic),'assertions':checks,
        'finite_count_states':states,'enabled_competitor_marks':enabled,'disabled_competitor_marks':disabled,
        'shift_rows':rows,'rate_envelope_remainder':str(remainder.as_expr()),
        'exact_exponential_examples':examples,
        'additional_certified_T5_N1e19_total_failure_upper':'1.1e-10',
        'scope':'No finite diagnostic substitutes for the uniform proof, optional stopping, or same-event join.'}
(ROOT/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
