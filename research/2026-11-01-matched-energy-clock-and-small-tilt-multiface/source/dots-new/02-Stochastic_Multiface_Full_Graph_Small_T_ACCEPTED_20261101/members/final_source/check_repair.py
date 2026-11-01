"""Exact regressions for independent audit's two code findings."""
from fractions import Fraction as F
from pathlib import Path
from random import Random
from copy import deepcopy
import json,hashlib,sys
import multiface as M,api,receive_certificate as R
root=Path(__file__).resolve().parent;guard_before=sys.get_int_max_str_digits();raw=M.fixture(2,((0,1),));huge=F(1<<20000)
raw_big=[(u,v,huge if sum(u)==0 else k) for u,v,k in raw]
qual=api.qualitative(raw_big);assert qual['independent_sets_enumerated']==0
p=M.construct(raw_big);c=M.encode(p);blob=json.dumps(c,sort_keys=True);back=json.loads(blob)
assert R.receive(raw_big,back)
assert R.evaluate_expression(M.encode(huge))==huge
assert R.evaluate_expression(M.encode(1<<20000))==1<<20000
try:R.evaluate_expression(back['CF_expression'],max_power_bits=10)
except M.BudgetRefusal:pass
else:raise AssertionError('tagged power exponent failed budget refusal')
assert sys.get_int_max_str_digits()==guard_before
for bad_budget in [True,-1,F(2),1.5]:
 for action in [lambda:M.construct(raw,max_masks=bad_budget),lambda:M.profile(p,0,max_power=bad_budget),lambda:R.evaluate_expression(F(1),max_power_bits=bad_budget)]:
  try:action()
  except ValueError:pass
  else:raise AssertionError('low-level budget domain')
base=R.certificate(raw)
type_mutations=0
for path,badval in [(('raw','A'),False),(('raw','m'),float(base['raw']['m'])),(('M',),float(base['M']))]:
 bad=deepcopy(base);dest=bad
 for key in path[:-1]:dest=dest[key]
 dest[path[-1]]=badval
 assert not R.receive(raw,bad);type_mutations+=1
rng=Random(123);permutations=0
for _ in range(20):
 rows=list(raw);rng.shuffle(rows);assert R.certificate(rows)==base;permutations+=1
assert R.certificate(list(reversed(raw)))==base
split=[row for u,v,k in raw for row in [(u,v,k/2),(u,v,k/2)]]
assert R.certificate(split)==base
assert M.recognize(raw)['raw_sha256']==M.recognize(list(reversed(raw)))['raw_sha256']
assert M.recognize(raw)['normalized_reaction_sha256']==M.recognize(raw)['raw_sha256']
assert M.input_list_sha256(raw)!=M.input_list_sha256(list(reversed(raw)))
assert M.input_list_sha256(raw)!=M.input_list_sha256(split)
assert api.qualitative(raw)['input_list_sha256']!=api.qualitative(list(reversed(raw)))['input_list_sha256']
result=dict(status='PASS_SAME_AUTHOR_ADDITIVE_REPAIR_REGRESSIONS',large_rate_bits=huge.numerator.bit_length(),large_input_qualitative=True,large_certificate_json_bytes=len(blob.encode()),raw_permutations=permutations+1,exact_type_mutation_rejections=type_mutations,split_duplicate_invariance=True,decimal_guard_unchanged=True,ordered_input_identity_separate_from_normalized=True,bindings={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['THEOREM_PENDING.md','multiface.py','api.py','receive_certificate.py','check_repair.py']})
(root/'repair_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
