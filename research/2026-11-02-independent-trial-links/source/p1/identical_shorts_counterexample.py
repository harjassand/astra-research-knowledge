#!/usr/bin/env python3
"""Two 3-mode physical laws with IDENTICAL four short assays and opposite long decisions."""
import json
from fractions import Fraction as F
p=[F(1,10),F(1,2),F(9,10)]
w=[F(1,3)]*3
b=[F(9,10),F(3,20),F(1,2)]
a_minus=[F(1,10),F(17,20),F(2,5)]
a_plus=[F(3,10),F(9,20),F(3,5)]
def moment(vec,n):return sum(wj*pj**n*vj for wj,pj,vj in zip(w,p,vec))
for k in (0,1):
 assert moment(a_minus,k)==moment(a_plus,k)
 assert moment(b,k)==moment(b,k)
d0=moment(a_minus,0)-moment(b,0)
d1=moment(a_minus,1)-moment(b,1)
assert d0<0<d1
lm=(moment(a_minus,74)-moment(b,74)); lp=(moment(a_plus,74)-moment(b,74))
assert lm<0<lp
assert all(F(0)<=v<=F(1) for v in a_minus+a_plus+b)
r={'modes':3,'baseline_p':[str(t) for t in p],'weights':[str(t) for t in w],
    'model_neg_A':[str(t) for t in a_minus],'model_pos_A':[str(t) for t in a_plus], 'B_shared':[str(t) for t in b],
    'identical_A0':str(moment(a_minus,0)), 'identical_A1':str(moment(a_minus,1)),
    'identical_B0':str(moment(b,0)), 'identical_B1':str(moment(b,1)),
    'd0':str(d0),'d1':str(d1),
    'L75_A_minus_B_model_neg':float(lm), 'L75_A_minus_B_model_pos':float(lp),
    'long_decision_neg':'B','long_decision_pos':'A',
    'truth':'Even exactly known four short assays do not determine long intervention preference with 3 persistent modes.'}
with open('producer-workspace/identical_shorts_counterexample_results.json','w') as f:json.dump(r,f,indent=2)
print(json.dumps(r,indent=2))
