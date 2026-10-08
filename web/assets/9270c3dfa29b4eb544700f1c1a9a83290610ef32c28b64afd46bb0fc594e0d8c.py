"""Exact small witness exercising an accepted volume exchange.
The warm start satisfies the proved theta floor, but is deliberately not
the greedy output. This checks the exchange module, not the whole theorem.
"""
from fractions import Fraction as F
from pathlib import Path
import json

C=[2,3,3,2];a=4;d=1
norm=sum(x*x for x in C)
P=[[F(x*y,norm) for y in C] for x in C]
H=1+3*d*(a-d);theta=F(1,2*a);nu=F(1,100)
zeta=min(F(1,4),theta/(100*d*2**d),F(1,12*H),nu/(128*H**2))
Q=[[P[i][j]+(zeta if i==j else 0) for j in range(a)] for i in range(a)]
volumes=[sum((Q[i][j]**2 for i in range(a)),F(0)) for j in range(a)]
selected=0;assert volumes[selected]>=theta
moves=[]
while True:
    replacement=next((j for j in range(a) if volumes[j]>2*volumes[selected]),None)
    if replacement is None:break
    moves.append({"from":selected,"to":replacement,
                  "ratio":str(volumes[replacement]/volumes[selected])})
    selected=replacement
assert len(moves)==1
assert all(v<=2*volumes[selected] for v in volumes)
true_ratios=[P[j][j]/P[selected][selected] for j in range(a)]
assert max(true_ratios)<=3 and P[selected][selected]>=F(1,H)
payload={"status":"FINITE-EVIDENCE: exact accepted exchange module",
         "theta_floor_satisfied":True,"warm_start_column":0,
         "accepted_moves":moves,"selected_column":selected,
         "true_Gram_minimum":str(P[selected][selected]),
         "public_lower":str(F(1,H)),"checks_passed":True,
         "limit":"Warm start is not the full greedy algorithm output"}
Path(__file__).with_name("exchange_witness.json").write_text(json.dumps(payload,indent=2)+"\n")
print(json.dumps(payload,indent=2))
