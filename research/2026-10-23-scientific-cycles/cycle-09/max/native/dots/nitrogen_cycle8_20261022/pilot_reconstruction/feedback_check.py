"""Exact finite feedback countermodels with identical baseline observations.
These are logical source-response models, NOT fitted plasma kinetics.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time,resource
start=time.perf_counter();e0=F(65,100);e1=F(9,10);A0=F(1);rows=[]
for gain in [F(0),F(1),F(3,2)]:
 intercept=A0*(1-gain*(1-e0));assert intercept>0
 A=lambda e:intercept/(1-gain*(1-e))
 q=lambda e:e*A(e)
 assert A(e0)==A0
 assert gain*(1-e0)<1 and gain*(1-e1)<1
 derivative=A(e0)*(1-gain)/(1-(1-e0)*gain)
 # Exact finite difference sign matches derivative; baseline identical.
 rows.append({'post_torch_source_map':'f(R)=intercept+gain*R','intercept':str(intercept),'gain':str(gain),'baseline_A':str(A(e0)),'baseline_return':str((1-e0)*A(e0)),'baseline_product':str(q(e0)),'upgraded_A':str(A(e1)),'upgraded_return':str((1-e1)*A(e1)),'upgraded_product':str(q(e1)),'SEC_ratio_fixed_total_power':str(q(e0)/q(e1)),'local_dq_depsilon':str(derivative)})
assert rows[0]['baseline_product']==rows[1]['baseline_product']==rows[2]['baseline_product']=='13/20'
assert F(rows[0]['SEC_ratio_fixed_total_power'])<1
assert F(rows[1]['SEC_ratio_fixed_total_power'])==1
assert F(rows[2]['SEC_ratio_fixed_total_power'])>1
# Fixed fresh production + survival recurrence, explicit loss/inventory conservation.
finite=[]
for survival in [F(0),F(1,2),F(1)]:
 for e in [e0,e1]:
  S=F(1);inventory=F(0);captured=F(0);destroyed=F(0)
  for j in range(12):
   destroyed+=(1-survival)*inventory
   A=S+survival*inventory
   captured+=e*A;inventory=(1-e)*A
  assert 12*S==captured+destroyed+inventory
  finite.append({'survival':str(survival),'capture':str(e),'new_fixed_N':'12','captured':str(captured),'destroyed_or_lost':str(destroyed),'final_unreset_inventory':str(inventory)})
out={'scope':'No physical source gain inferred. Demonstrates non-identification and inventory accounting.','source_response_countermodels':rows,'finite_12_pass_balances':finite,'elapsed_s':time.perf_counter()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
p=Path(__file__).parent;(p/'feedback_result.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
