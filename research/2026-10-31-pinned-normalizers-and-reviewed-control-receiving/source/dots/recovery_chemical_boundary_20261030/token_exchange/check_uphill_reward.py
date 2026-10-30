"""Exact local kernel checks; no chemical/global recurrence claim."""
from fractions import Fraction as F
import json

def invapply(a,b,c,d,u,v):
    det=a*d-b*c
    assert det>0
    return ((d*u-b*v)/det,(-c*u+a*v)/det)

cases=0
for s0 in range(1,33):
    for y0 in range(1,33):
        s,y=F(s0),F(y0)
        # Q0=[[-3,2],[1,-4]], downhill mark 3s, uphill mark2.
        a,b,c,d=3*s+3*s*y,-2*s,-s,4*s+2*y
        pu=invapply(a,b,c,d,F(0),F(2))
        uphill=y*(2*s*pu[0]+s*pu[1])
        assert uphill<=F(7,5)*y
        t=[F(2,5)/s,F(3,5)/s]
        assert a*t[0]+b*t[1]>=0
        assert c*t[0]+d*t[1]>=2
        cases+=1
# At y=1 the downhill trace rate grows linearly, while uphill is bounded.
rows=[]
for s0 in [1,10,100,1000]:
    s=F(s0); a,b,c,d=6*s,-2*s,-s,4*s+2
    pd=invapply(a,b,c,d,3*s,F(0))
    pu=invapply(a,b,c,d,F(0),F(2))
    rows.append({'s':s0,'downhill':str(2*s*pd[0]+s*pd[1]),
                 'uphill':str(2*s*pu[0]+s*pu[1])})
print(json.dumps({'exact_cases':cases,'bound_per_label':'7/5',
 'downhill_asymptotic_coefficient':'27/22',
 'uphill_limit':'10/11','examples':rows},indent=2))
