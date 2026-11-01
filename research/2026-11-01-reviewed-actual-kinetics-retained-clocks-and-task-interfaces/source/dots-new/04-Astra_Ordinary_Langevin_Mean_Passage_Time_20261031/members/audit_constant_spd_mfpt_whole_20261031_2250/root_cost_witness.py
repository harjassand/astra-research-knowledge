"""Two root calls is dimension-independent; nonsquare root BIT cost is not."""
from pathlib import Path
from fractions import Fraction as F
import json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H/'constant_spd_mfpt_20261031'))
import receive_mfpt as c
rows=[]
for m in [16,512]:
 alpha=m//4;kappa=F(3,7);P=max(192,alpha*(c.bits(kappa)+2)+128)
 r=c.Roots(P,1000000);out=r.upper(F(2,3));assert out*out>=F(2,3)
 rows.append({'fiber_dimension':m,'alpha':alpha,'precision_bits':P,'root_calls':r.calls,'largest_root_integer_bound_bits':r.max_bits})
assert rows[0]['root_calls']==rows[1]['root_calls']==1 and rows[0]['largest_root_integer_bound_bits']<rows[1]['largest_root_integer_bound_bits']
report={'status':'PASS exact counterexample to literal dimension-independent root BIT-cost wording','source_claim':'ARITHMETIC_COSTS_AND_SCOPE.md: These root costs are explicit and independent of angular dimension.','corrected_scope':'The number of root invocations is fixed at two in certify. For nonsquare arguments, scaled operands have bit size depending on P, which can grow with alpha=m/4. Budgets and output correctness remain sound.','witness':rows}
(H/'root_cost_witness.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
