from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import api,multiface as M
root=Path(__file__).resolve().parent;raw=M.fixture();q=api.qualitative(raw)
assert q['independent_sets_enumerated']==0
refusal=api.construct(raw,max_masks=0)
assert refusal['status']=='QUANTITATIVE_MASK_BUDGET_REFUSAL' and not refusal['stability_refuted']
assert refusal['qualitative']==q
bad=0
for budget in [True,-1,F(2),1.5,'32']:
 try:api.construct(raw,max_masks=budget)
 except ValueError:bad+=1
 else:raise AssertionError('budget-domain rejection')
p=M.construct(raw)
assert api.pointwise_profile(p,0)==M.profile(p,0)
try:api.pointwise_profile(p,100,max_power_bits=1)
except M.BudgetRefusal:pass
else:raise AssertionError('bit budget')
result=dict(status='PASS_SAME_AUTHOR_API_SCOPE_AND_BUDGET_TESTS',invalid_budget_rejections=bad,qualitative_scan_enumerated_sets=0,quantitative_refusal_retains_qualitative=True,bindings={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['api.py','check_api.py']})
(root/'api_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
