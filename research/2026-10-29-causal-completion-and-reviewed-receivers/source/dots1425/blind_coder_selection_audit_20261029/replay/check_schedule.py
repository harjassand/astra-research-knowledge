from fractions import Fraction as F
from math import comb,ceil
import json
from pathlib import Path
rows=[]
for eps in [F(1,2),F(1,4),F(3,4)]:
 for delta in [F(1,4),F(1,16)]:
  for j in range(3):
   L=(j+1)**2; dj=delta/F(2**(j+1)*L)
   b=0
   while F(1,2**b)>dj:b+=1
   m=ceil(32*b/eps); cutoff=(3*eps*m/4).__floor__()
   assert cutoff==24*b
   good=eps/4
   # Exact independent binomial upper tail using recurrence.
   term=(1-good)**m; reject=F(0)
   for x in range(m+1):
    if x>cutoff:reject+=term
    if x<m:term*=F(m-x,x+1)*good/(1-good)
   assert reject<=dj**8
   # Worst allowed seed-quality mixture: 1/4 always rejected,3/4 good.
   fail=F(1,4)+F(3,4)*reject
   assert fail<F(1,2)
   rows.append(dict(epsilon=str(eps),delta=str(delta),stage=j,b=b,m=m,threshold=cutoff,good_reject=float(reject),stage_fail_bound=float(fail**L)))
tails=[]
for js in [0,1,3,8]:
 for p in [1,4,12]:
  exact=F(0); exponent=0
  for s in range(25):
   exact+=F(2**(p*s),2**exponent)
   exponent+=(js+s+1)**2
  tails.append(dict(first_good_stage=js,cost_exponent=p,normalized_first25_cost=float(exact)))
# One-seed/stage counterexample: success1/2, stage cost4^j => summands2^j diverge.
assert all(F(1,2**j)*4**j==2**j for j in range(10))
out={'scope':'exact schedule and good-seed binomial tests; no physical learner executed','schedule_cases':rows,'tail_cases':tails,'one_seed_counterexample':'reach probability2^-j times stage cost4^j =2^j'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS',len(rows),'exact binomial cases;',len(tails),'tail fixtures')
