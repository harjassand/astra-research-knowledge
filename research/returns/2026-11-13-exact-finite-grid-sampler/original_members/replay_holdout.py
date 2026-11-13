from pathlib import Path
import sys,json,time
D=Path(__file__).resolve().parent/'research_notes/north_compute_20261113/affine_sampler';sys.path.insert(0,str(D))
from frozen_component_v1 import sample,grid_layers
rows=[json.loads(x) for x in (D/'holdout_v1_raw.jsonl').read_text().splitlines()];layers=grid_layers(32,32,100);start=time.perf_counter()
for j,row in enumerate(rows):
 out,s=sample(1024,layers,seed=int(row['seed']),cap=4096,bitcap=20000)
 assert str(out)==row['output'] and s['aborted']==row['aborted'],j
 if (j+1)%100==0:print(j+1,'passed',flush=True)
print('All recorded draws reproduced in',time.perf_counter()-start,'seconds')
