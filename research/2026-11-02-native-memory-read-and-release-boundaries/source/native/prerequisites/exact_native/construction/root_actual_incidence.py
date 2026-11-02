"""Read actual deterministic family fixture; no geometric inference from counts."""
from pathlib import Path
import runpy,collections,json,os
p=Path(os.environ.get('ASTRA_HOST_FIXTURE','producer-workspace/actual_host_quotient_deterministic_test.py'))
d=runpy.run_path(str(p));r=[]
for X,Z,n in d['levels']:
 r.append({'n':n,'X_incidence':dict(collections.Counter(sum((s>>q)&1 for s in X) for q in range(n))),'Z_incidence':dict(collections.Counter(sum((s>>q)&1 for s in Z) for q in range(n)))})
print(json.dumps(r,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n')
