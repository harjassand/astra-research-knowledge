"""Exact finite checks and conservative asymptotic acceptance bounds."""
from fractions import Fraction as F
from math import comb
from decimal import Decimal, localcontext
from pathlib import Path
import json

def tail(n,p,m):
    return sum((F(comb(n,k))*p**k*(1-p)**(n-k) for k in range(m,n+1)),F(0))
checks=0
for p in [F(1,10000),F(1,1000),F(1,200),F(1,10),F(1,3)]:
    for m in range(1,21):
        zmin=F(comb(2*m,m))*p**m
        upper=(1-p)**(m+1)/(1-2*p)
        exact_tail=tail(2*m,p,m)
        assert exact_tail/zmin <= upper
        # The actual deterministic repetition tie fails on half of the equal-weight errors.
        pf=exact_tail-F(1,2)*comb(2*m,m)*(p*(1-p))**m
        monotone_z=sum((F(comb(2*m,k))*p**k for k in range(m,2*m+1)),F(0))
        assert pf/monotone_z <= upper
        checks+=1
rows=[]
with localcontext() as ctx:
    ctx.prec=70
    for ps in ['0.0001','0.001','0.005']:
        p=Decimal(ps)
        for m in [100,1000,10000]:
            u=(1-p)**(m+1)/(1-2*p)
            rows.append({'p':ps,'line_edges':2*m,'acceptance_upper_decimal':str(min(u,Decimal(1)))})
result={'scope':'cover-specific upper bound, not an impossibility result for repetition decoding or rare-event estimation','exact_finite_checks':checks,'formula':'(1-p)^(m+1)/(1-2p)','rows':rows}
Path(__file__).with_name('repetition_limit_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
