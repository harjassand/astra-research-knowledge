"""Same-author end-to-end receipt, mutation, scope, and computation-budget tests."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
import json,hashlib,sys
import multiface as M
import receive_certificate as R
root=Path(__file__).resolve().parent;raw=M.fixture();p=M.construct(raw);c=M.encode(p)
assert R.receive(raw,c)
mutations=0
for key,val in [('Nstar',0),('t','2'),('P',0),('status','INDEPENDENT_WHOLE_PASS')]:
 bad=deepcopy(c);bad[key]=val;assert not R.receive(raw,bad);mutations+=1
try:R.evaluate_expression(p['CF_expression'],max_power_bits=10000)
except M.BudgetRefusal:refused=True
else:raise AssertionError('enormous finite head expanded despite bit budget')
assert R.evaluate_expression({'op':'mul','args':[F(2,3),{'op':'pow','base':F(3,2),'exponent':4}]},max_power_bits=100)==F(27,8)
assert p['t']>1 and p['eps']<=1 and 'SMALL_T' in p['status']
# Existing admitted backbone rejects this structural fixture: every hub has arms,
# so no amplification-only detour can be separated off.
sys.path.insert(0,str(root.parent/'stochastic_arm_backbone_recovery_20261101'))
import arm_backbone as Old
try:Old.recognize(raw)
except Old.G.Unsupported as exc:old_reason=str(exc)
else:raise AssertionError('claimed strict raw extension not observed')
# Ordinary complex balance is also ruled out in this fixture: every active A+i
# has the same unit outgoing rates and receives total reverse rate E except i=1,
# which receives E+1; the common hub/2A amplification equations and the other
# satellite equations need a separate actual algebraic test, not a claim here.
(root/'fixture_certificate.json').write_text(json.dumps(c,indent=2,sort_keys=True)+'\n')
result=dict(status='PASS_SAME_AUTHOR_CANONICAL_RECEIVING_NOT_INDEPENDENT',mutation_rejections=mutations,power_budget_refusal=refused,old_backbone_rejection=old_reason,faces=len(p['faces']),mask_count=p['mask_count'],Nstar_bits=p['Nstar'].bit_length(),max_scalar_bits=max(abs(v.numerator).bit_length()+v.denominator.bit_length() if isinstance(v,F) else abs(v).bit_length() for v in p.values() if isinstance(v,(int,F))),certificate_bytes=(root/'fixture_certificate.json').stat().st_size,bindings={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['THEOREM_PENDING.md','multiface.py','receive_certificate.py','check_receiving.py','fixture_certificate.json']})
(root/'receiving_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
