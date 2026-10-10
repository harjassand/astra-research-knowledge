from itertools import combinations
from check_folds import sunflower
import json

rows=[tuple(map(int,s)) for s in '001 002 020 030 100 113 211 212 223 233 300 313'.split()]
assert not any(sunflower(t) for t in combinations(rows,3))

def valid(sub):
    return len(set(sub))==len(sub) and not any(sunflower(t) for t in combinations(sub,3))

report=[]
for i in range(3):
    pr=[r[:i]+r[i+1:] for r in rows]
    witness=next(ids for ids in combinations(range(12),4) if valid([pr[j] for j in ids]))
    assert not any(valid([pr[j] for j in ids]) for ids in combinations(range(12),5))
    report.append({'coordinate':i,'maximum_safe_retained':4,'retained_original_indices':witness,
                   'all_five_row_subsets_rejected':True})
print(json.dumps({'sunflower_free':True,'size':12,'rank':3,'erasure':report},indent=2))
