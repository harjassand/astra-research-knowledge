from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json
import random
import time

from paired_exact import Q, canonical, mat, brute_weights, gram_weight
from support_radius import acquire_support_radius, acquired_radius_count

start = time.perf_counter()
receipts = []
for n,k,h,seed in [(4,2,3,103),(6,3,4,107),(8,4,5,109)]:
    # Every square Cauchy subminor is nonzero. Exactly the k-subsets of H
    # support the top canonical law, so mandatory core is empty and radius1.
    Fmat = mat([[F(1,i+j+1) if i<h else F(0)
                for j in range(n)] for i in range(n)])
    V = canonical(Fmat)
    weights = brute_weights(V,k)
    support = [set(S) for S,w in weights.items() if w]
    core = sorted(set.intersection(*support))
    a = acquire_support_radius(V,k,F(1,10000),random.Random(seed))
    assert a['status'] == 'POSITIVE'
    witness = set(a['witness'])
    true_radius = max(len(S-witness) for S in support)
    true_diameter = max(len(S-T) for S in support for T in support)
    assert true_radius == a['radius'] == 1
    assert core == [] and true_diameter == 1
    assert len(support) == len(list(combinations(range(h),k)))
    receipts.append({'n':n,'k':k,'active_rows':h,'positive_support_count':len(support),
        'mandatory_core':core,'true_radius':true_radius,'true_diameter':true_diameter,
        'partition':sum(weights.values(),F(0)), 'acquired':a})

upper = mat([[int(i<j) for j in range(6)] for i in range(6)])
unique = acquired_radius_count(canonical(upper),3,F(1,4),F(1,1000),0,random.Random(113))
assert unique['value'] == 1 and unique['acquisition']['radius'] == 0
assert unique['samples'] == 0

small = mat([[F(1,i+j+1) if i<3 else F(0) for j in range(4)] for i in range(4)])
Vsmall = canonical(small)
count = acquired_radius_count(Vsmall,2,F(3,4),F(1,2),1,random.Random(127))
exact = sum(brute_weights(Vsmall,2).values(),F(0))
assert abs(count['value']/exact-1) <= F(3,4)

class AllZeroBits:
    # One specified possible grid outcome, not a source of uniform randomness.
    def getrandbits(self,bits):
        return 0

cancel = mat([[1,0,1,0,1,0],[0,1,0,1,0,-1]])
underestimate = acquire_support_radius(cancel,1,F(1,10),AllZeroBits())
assert sum(brute_weights(cancel,1).values(),F(0)) == 3
assert underestimate['witness'] == [0] and underestimate['radius'] == 0
# True radius is1, but x1=x2 outside the center cancels the leading polynomial.
# This outcome has positive probability under ideal independent grid draws.
# It demonstrates why the acquired radius is a confidence result, not exact.

result = {'status':'PASS','acquisitions':receipts,'unique_support_exact_count':unique,
          'implemented_small_radius_FPRAS_run':count,'run_exact_partition':exact,
          'explicit_possible_underestimation_outcome':{
              'true_radius':1,'reported':underestimate,
              'note':'all grid entries1 is a specified possible outcome, not an iid diagnostic; confidence failure must remain charged'},
          'elapsed_seconds':time.perf_counter()-start,
          'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'limitations':'finite exact support diagnostics and one seeded FPRAS execution; probability/asymptotic claims require the proof'}
(Path(__file__).parent/'radius_checks.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
print(json.dumps({'status':'PASS','elapsed_seconds':result['elapsed_seconds'],
                  'radii':[x['acquired']['radius'] for x in receipts],
                  'count_samples':count['estimate']['sign_samples']},indent=2))
