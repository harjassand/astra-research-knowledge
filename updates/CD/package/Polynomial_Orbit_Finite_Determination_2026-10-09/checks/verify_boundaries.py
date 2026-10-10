#!/usr/bin/env python3
"""Small exact checks, never substitutes for the return-stratification proof."""
from fractions import Fraction as Q
from math import factorial
import json
from pathlib import Path
import sympy as s

x,y,X,Y,u,v=s.symbols('x y X Y u v')
G=s.groebner([y-Y,x*y-X*Y],x,y,X,Y)
identity_checks=[]
for k in range(12):
    remainder=G.reduce(x**k*y-X**k*Y)[1]
    assert remainder==0
    identity_checks.append(k)

def bound(n,d,e):
    delta,t=e,1
    stages=[{'Delta':delta,'T':t}]
    for _ in range(n):
        old_delta,old_t=delta,t
        t=(old_delta+1)*old_t
        delta=old_delta**(n+2)*d**((n+1)*old_t)
        stages.append({'Delta':delta,'T':t})
    return t-1,stages

falling=[]
for degree in range(1,9):
    def P(z):
        result=Q(1)
        for j in range(degree): result*=z-j
        return result
    # F(a,b)=(a+1,P(a)), output b, initial (0,0). Dimension-collapsing.
    a,b=Q(0),Q(0)
    vals=[]
    for t in range(degree+2):
        vals.append(b)
        a,b=a+1,P(a)
    first=next(i for i,z in enumerate(vals) if z)
    B,stages=bound(2,max(1,degree),1)
    assert first==degree+1 and first<=B
    falling.append({'degree':degree,'first_nonzero_index':first,'nonzero_value':str(vals[first]),'candidate_bound':B})

# A reducible guard and a dimension-collapsing map: F(x,y)=(y,1), h=xy.
reducible=[]
for a,b in [(Q(0),Q(0)),(Q(7),Q(0)),(Q(0),Q(4))]:
    initial=[str(a),str(b)]
    vals=[]
    for t in range(5):
        vals.append(a*b)
        a,b=b,Q(1)
    first=next((i for i,z in enumerate(vals) if z),None)
    B,_=bound(2,1,2)
    assert first is None or first<=B
    reducible.append({'initial':initial,'outputs':list(map(str,vals)),'first_nonzero_index':first,'candidate_bound':B})

# Boolean binary counters demonstrate an exponential initial-zero family.
counters=[]
for n in range(1,9):
    bits=[0]*n
    outputs=[]
    for t in range(2**n):
        outputs.append(int(all(bits)))
        carry=1
        new=[]
        for b in bits:
            new.append(b+carry-2*b*carry)
            carry*=b
        bits=new
    first=next(i for i,z in enumerate(outputs) if z)
    assert first==2**n-1
    counters.append({'bits':n,'degree_bound':n,'first_nonzero_index':first})

payload={
 'scope':'Exact finite sanity checks only; no numerical verification of general theorem',
 'observation_ideal_membership_degrees':identity_checks,
 'dimension_collapsing_falling_factorial':falling,
 'reducible_guard_dimension_collapse':reducible,
 'boolean_counter_lower_examples':counters,
 'checks_passed':True,
}
p=Path(__file__).with_name('boundary_verification.json')
p.write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload,indent=2))
