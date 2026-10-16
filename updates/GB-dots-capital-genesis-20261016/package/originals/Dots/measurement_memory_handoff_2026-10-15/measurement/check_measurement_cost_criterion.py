"""Exact rational checks of the conservative measurement-cost optimizer; no device data."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json

def optimizer(c,d):
 assert c>=0 and d>0
 r=c/d;m=max(1,isqrt(r.numerator//r.denominator))
 if m*(m+1)<r:m+=1
 return [m,m+1] if r==m*(m+1) else [m]
def objective(M,c,d):return d*(M+1)+c/M

def cap_optimizer(a,C,d):
 assert a>=0 and C>=0 and d>0
 tail=max(1,a.numerator//a.denominator+1)
 unc=optimizer(C*a,d);candidates={1,tail,*[max(tail,m) for m in unc]}
 values={m:d*(m+1)+C*min(F(1),a/m) for m in candidates};best=min(values.values())
 return sorted(m for m,v in values.items() if v==best)
checks=0;capchecks=0
for cp in range(31):
 for cq in [1,3]:
  for dp in range(1,11):
   for dq in [1,5]:
    c,d=F(cp,cq),F(dp,dq);opt=optimizer(c,d);values=[objective(m,c,d) for m in range(1,201)];best=min(values);actual=[m for m in range(1,201) if values[m-1]==best]
    assert opt==actual,(c,d,opt,actual)
    assert (min(values)<objective(1,c,d))==(c>2*d)
    for threshold in [F(0),F(1),F(7,3),objective(opt[0],c,d),objective(opt[0],c,d)-F(1,100)]:
     for M in range(1,21):assert (objective(M,c,d)<=threshold)==(d*M*M+(d-threshold)*M+c<=0)
    checks+=1
for ap in range(41):
 for aq in [1,3]:
  for C in [F(1,10),F(1),F(7)]:
   for d in [F(1,10),F(1),F(3)]:
    a=F(ap,aq);opt=cap_optimizer(a,C,d);vals=[d*(m+1)+C*min(F(1),a/m) for m in range(1,201)];best=min(vals);actual=[m for m in range(1,201) if vals[m-1]==best]
    assert opt==actual,(a,C,d,opt,actual);capchecks+=1
examples=[]
for c,d in [(F(1),F(1)),(F(2),F(1)),(F(3),F(1)),(F(6),F(1)),(F(100),F(1))]:
 opt=optimizer(c,d);examples.append({'c':str(c),'d':str(d),'optimal_M':opt,'baseline':str(objective(1,c,d)),'optimal_cost':str(objective(opt[0],c,d))})
r={'status':'PASS','uncapped_exact_rational_cases':checks,'capped_exact_rational_cases':capchecks,'brute_force_integer_range':[1,200],'examples_dimensionless_algebra_only':examples,'device_inputs_used':False,'actual_physical_error_monotonicity_asserted':False}
Path(__file__).with_name('measurement_cost_criterion_check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
