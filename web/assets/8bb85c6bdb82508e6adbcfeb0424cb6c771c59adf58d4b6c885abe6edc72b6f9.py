from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import random
import time

from paired_exact import Q, mat
from residual_counter import mandatory_core_count, sqrt_up_to_activity

start = time.perf_counter()
Fmat = mat([[int(i<j) for j in range(4)] for i in range(4)])
Fmat[3][2] = Q(1)
acquired = mandatory_core_count(Fmat,2,F(3,4),F(1,2),1,random.Random(73))
assert acquired['status'] == 'APPROXIMATE_WITH_CONFIDENCE'
assert acquired['acquisition']['core'] == [0]
assert acquired['acquisition']['residual'] == 1
assert abs(acquired['value']/2-1) <= F(3,4)
rejected = mandatory_core_count(Fmat,2,F(3,4),F(1,2),0,random.Random(73))
assert rejected['status'] == 'UNKNOWN'

FT = mat([[0,16,16,1],[0,0,16,1],[0,0,0,1],[0,0,0,0]])
weighted_zero_residual = mandatory_core_count(FT,2,F(1,2),F(1,100),0,
    random.Random(97),[F(3,7),F(2),F(5,11),F(13)])
assert weighted_zero_residual['value'] == F(256*15,77)
assert weighted_zero_residual['residual_estimate']['sign_samples'] == 0

activity_checks = []
for lam in [F(1,2**100),F(2**100),F(3,7),F(29,11)]:
    b = sqrt_up_to_activity(lam,F(1,1000))
    assert 1 <= b*b/lam <= F(1001,1000)
    activity_checks.append({'activity':lam,'rational_sqrt':b,'relative_square':b*b/lam})

result = {'status':'PASS', 'actual_randomized_counter_run': acquired,
          'unadmitted_run':rejected,'weighted_exact_residual_zero':weighted_zero_residual,
          'activity_approximations':activity_checks,
          'elapsed_seconds':time.perf_counter()-start,
          'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'limitations':'seeded single-run diagnostic; probability guarantee is proved separately; no end-to-end TV sampler'}
(Path(__file__).parent/'counter_checks.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
print(json.dumps({'status':'PASS','elapsed_seconds':result['elapsed_seconds'],
                  'sign_samples':acquired['residual_estimate']['sign_samples']},indent=2))
