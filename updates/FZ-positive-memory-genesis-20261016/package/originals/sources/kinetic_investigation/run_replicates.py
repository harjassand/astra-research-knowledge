import json,time,sys
from pathlib import Path
from kinetics import splitting,evolve,grid_edges
import numpy as np
seeds=[8017+1009*j for j in range(12)]
a=int(sys.argv[1]); b=int(sys.argv[2])
for j in range(a,b):
 t0=time.perf_counter()
 result=splitting(particles=256,seed=seeds[j],levels=tuple(range(47,14,-2)))
 result['wall_seconds']=time.perf_counter()-t0
 path=Path(f'split_rep_{j:02}.json');path.write_text(json.dumps(result,indent=2))
 print(j,result['estimate'],result['total_events'],result['wall_seconds'],flush=True)
