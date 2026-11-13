from pathlib import Path
import json,hashlib,sys
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
for p,h in json.loads((ROOT/'MANIFEST.json').read_text()).items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
D=ROOT/'research_notes/north_compute_20261113/affine_sampler'
summary=json.loads((D/'holdout_v1_result.json').read_text());rows=[json.loads(x) for x in (D/'holdout_v1_raw.jsonl').read_text().splitlines()]
assert len(rows)==1000 and sum(x['aborted'] for x in rows)==0
assert len({x['seed'] for x in rows})==1000 and [x['index'] for x in rows]==list(range(1000))
for p,h in summary['protocol']['source_sha256'].items():
 rel=p[p.index('research_notes/'):];assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h
u=F(summary['abort_99pct_upper']);assert u==F(919,200000)
assert (1-u)**1000 <= F(1,100) # exact rational, no floating confidence arithmetic
sys.path.insert(0,str(D));from frozen_component_v1 import sample,grid_layers
layers=grid_layers(32,32,100)
for row in rows[:3]:
 out,s=sample(1024,layers,seed=int(row['seed']),cap=4096,bitcap=20000)
 assert str(out)==row['output'] and s['aborted']==row['aborted']
print('Manifest, frozen hashes, 1000 records, exact confidence inequality and three deterministic replays passed.')
