from fractions import Fraction as F
import math,json,random
from pathlib import Path
weights=[1,2,4];N=sum(weights);base=8;cap=5
# Joint mass of first successful weighted action i and first acceptance at k.
rows=[]
for k in range(1,cap+1):
 pcount=F(base-N,base)**(k-1)*F(N,base)
 for i,w in enumerate(weights):
  joint=F(base-N,base)**(k-1)*F(w,base)
  assert joint==pcount*F(w,N)
  rows.append({'count':k,'action':i,'joint':str(joint)})
fail=F(base-N,base)**cap
assert sum(F(r['joint']) for r in rows)+fail==1
rng=random.Random(295511);res=0
for _ in range(1000):
 A=10**rng.uniform(-5,5);V=A+10**rng.uniform(-5,5)
 G=(math.sqrt(V)-math.sqrt(A))**2
 r=abs((math.sqrt(G)+math.sqrt(A))**2-V)/max(1,V)
 assert r<1e-12;res=max(res,r)
out={'exact_cap_failure':str(fail),'joint_count_action_checks':rows,'inverse_threshold_cases':1000,'max_relative_threshold_residual':res,'scope':'Exact stopped-sampler independence and finite threshold algebra, not physical trajectory simulation.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print('PASS sampler independence and1000 thresholds')
