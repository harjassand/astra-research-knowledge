from fractions import Fraction as F
from pathlib import Path
import json, hashlib

p=Path(__file__).with_name('AUTOMATIC_VALIDATED_ROW_FAST_PATH.md')
cases=0
for d in range(2,129):
    J=(4*d*d-1).bit_length()
    ks=[F(1,2**(j+2)) for j in range(J+1)]
    assert F(1,32*d*d)<ks[-1]<=F(1,16*d*d)
    for j,k in enumerate(ks):
        assert sum(1/q for q in ks[:j+1])<2/k
        for balance in [k,min(F(1,4),k*F(3,2))]:
            jj=next(i for i,z in enumerate(ks) if z<=balance)
            assert ks[jj]>=balance/2
            cases+=1
    assert F(1,1024*(J+1))+F(2,8192*(J+1))<F(1,512)
assert F(1,512)+F(1,4096)+F(1,512)==F(17,4096)
assert 2*F(17,4096)+F(1,2)<1
out={'status':'PASS author exact composition arithmetic; load-bearing candidate modules remain pending',
    'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'dimension_cases':127,
    'instance_balance_cases':cases,'source_calls':0,'sampled_trial_outcomes':0,
    'scope':'Exact finite schedule, geometric bill, balance-index and error arithmetic only. No empirical acquisition or independent receipt.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
