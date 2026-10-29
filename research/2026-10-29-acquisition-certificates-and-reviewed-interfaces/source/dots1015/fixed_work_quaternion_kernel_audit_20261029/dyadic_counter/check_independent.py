from pathlib import Path
from fractions import Fraction as F
import importlib.util,random,json
p=Path('producer-workspace/dyadic_gap_counter.py')
s=importlib.util.spec_from_file_location('counter',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
rng=random.Random(291029);checks=0
for b in [0,1,7,39,64]:
 for cap in [F(0),F(2),F(340050),F(1,2**b)]:
  c=m.Counter(b,cap);true=F(0)
  for j in range(100):
   e=cap*F(rng.randrange(10001),10000);v=c.add(e);true+=e
   assert e<=v<=e+F(1,2**b) and 0<=v<=cap
   assert true<=F(c.units,c.den)<=true+F(c.calls,c.den)
   assert c.units<=c.calls*c.cap_units
   checks+=1
result={'independent_exact_checks':checks,'scope':'Arithmetic upper counters only; no physical or empirical expectation inference.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
