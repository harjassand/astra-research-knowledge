from fractions import Fraction as F
from math import factorial
from pathlib import Path
from flint import arb,ctx
import json,time,random
from displaced_evaluator import log_H,asarb
rows=[]
# Small-degree integral branch made applicable by large displacement.
for n in [1,2,3,20,101]:
 a,c=F(1,3),F(100)
 exact=sum((F(1,factorial(q)*factorial(n-2*q))*(a/2)**q*c**(n-2*q) for q in range(n//2+1)),F(0))
 start=time.perf_counter();value,meta=log_H(n,a,c,30,force_integral=True)
 with ctx.workprec(400):
  truth=asarb(exact).log()
  assert value.overlaps(truth)
  assert value.rad()<arb(2)**(-31)
  rows.append({'n':n,'a':str(a),'c':str(c),'p':30,'seconds':time.perf_counter()-start,'actual_log_radius':str(value.rad()),'method':meta['method'],'exact_rational_check':True})
# Large orders and tiny odd displacement test no subtractive parity cancellation.
for n,a,c,p in [(4000,F(1,3),F(1,7),20),(4001,F(1,3),F(1,10**40),20),(10**20,F(1,3),F(1,7),30),(10**20+1,F(1,3),F(1,10**80),30),(10**50,F(1,100),F(10**20),30),(10**100+1,F(1,10**100),F(1,10**200),50)]:
 start=time.perf_counter();value,meta=log_H(n,a,c,p)
 with ctx.workprec(meta['working_bits']):
  assert value.rad()<arb(2)**(-p-1)
  rows.append({'n':str(n),'a':str(a),'c':str(c),'p':p,'seconds':time.perf_counter()-start,'actual_log_radius':str(value.rad()),'log_H_digits':value.str(160),'metadata':meta})
# Direct finite positive coefficient sum independently checks modest large orders.
for n,a,c in [(4000,F(1,3),F(1,7)),(4001,F(1,3),F(1,10**40))]:
 value,_=log_H(n,a,c,20)
 with ctx.workprec(300):
  total=arb(0);aa,cc=asarb(a),asarb(c)
  for q in range(n//2+1):
   total+=(q*(aa/2).log()+(n-2*q)*cc.log()-arb(q+1).lgamma()-arb(n-2*q+1).lgamma()).exp()
  assert value.overlaps(total.log())
rows.append({'direct_sum_large_order_checks':2})
Path(__file__).with_name('displaced_evaluator_results.json').write_text(json.dumps({'status':'internally tested supplemental evaluator; frozen v2 untouched','rows':rows},indent=2))
print('passed',len(rows),'records')
