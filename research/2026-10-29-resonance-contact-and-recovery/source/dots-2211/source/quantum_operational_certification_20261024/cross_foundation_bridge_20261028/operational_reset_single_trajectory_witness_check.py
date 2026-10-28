from fractions import Fraction as F
import json
from pathlib import Path
count=0
for q in [F(1,10),F(1,4),F(1,2),F(3,4),F(9,10)]:
 for N in range(1,9):
  total=F(0)
  for mask in range(1<<N):
   ys=[(mask>>k)&1 for k in range(N)];prob=F(1)
   for y in ys:prob*=q if y else 1-q
   total+=prob
   for x0 in [0,1]:
    xs=[x0]
    for y in ys:xs.append(xs[-1]^y)
    assert all((xs[k+1]^xs[k])==ys[k] for k in range(N))
   count+=1
  assert total==1
r={'status':'PASS_EXACT_TRAJECTORY_IDENTITY','q_values':5,'max_N':8,'flip_sequences_checked':count,'source_draws':0,'scope':'Exact physical transition identity, not an empirical run or verification of source-class membership.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
