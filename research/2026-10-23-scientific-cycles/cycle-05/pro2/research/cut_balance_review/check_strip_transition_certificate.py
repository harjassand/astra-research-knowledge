#!/usr/bin/env python3
"""Independent syntax/coverage check of the new six-step transition certificate.

No producer module is imported, and no completed old recovery fixture is run.
This finite assertion is load-bearing in the all-size boundary-reset proof.
"""
from pathlib import Path
from itertools import permutations, combinations
import json
import hashlib
import time
import resource

base = Path(__file__).resolve().parents[1]
source = base / 'structure' / 'RESULT.json'
start_wall, start_cpu = time.perf_counter(), time.process_time()
data = json.loads(source.read_text())
certificate = data['transition_certificate']
states = set(permutations(range(4), 2))
required = {(s,t) for s in states for t in states}
seen = set()
for item in certificate:
    s,t = tuple(item['start']), tuple(item['end'])
    tail = tuple(item['appended'])
    assert (s,t) in required and (s,t) not in seen
    assert len(tail)==6 and all(type(a) is int and 0<=a<4 for a in tail)
    word = s+tail
    assert word[-2:]==t
    assert all(len(set(word[i:i+3]))==3 for i in range(6))
    seen.add((s,t))
assert seen==required and len(seen)==144
# Check the new gap obligation, not the old period-nine recovery experiment.
# Every actual core starts at phase 0 and has length >=18; a strict interior
# gap within its first18 vertices therefore suffices at every later length.
core = (0,1,2,0,3,1,0,2,3)*2
gaps = []
for pair in combinations(range(4),2):
    i = next(i for i in range(1,16)
             if core[i] not in pair and core[i+1] not in pair)
    gaps.append({'pair':list(pair),'strict_interior_gap':[i,i+1],
                 'gap_colors':list(core[i:i+2])})
canonical = json.dumps(certificate,sort_keys=True,separators=(',',':')).encode()
result = {
    'status':'PASS', 'transition_cases':len(seen),
    'producer_imported':False,
    'transition_certificate_canonical_sha256':hashlib.sha256(canonical).hexdigest(),
    'interior_gap_certificates':gaps,
    'body_wall_seconds':time.perf_counter()-start_wall,
    'body_cpu_seconds':time.process_time()-start_cpu,
    'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
    'scope':'Finite transition and cut-gap certificate only; no source of an all-size theorem by extrapolation.'
}
target = Path(__file__).with_name('strip_transition_result.json')
target.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
