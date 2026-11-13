import numpy as np,json
from pathlib import Path
from mps_sampler import sample
rows=[]
for physical in [False,True]:
 for eps in [.02,.1]:
  for seed in range(30):
   _,s=sample(8,[[(0,1),(2,3),(4,5),(6,7)],[(0,4),(1,5),(2,6),(3,7)],[(1,2),(5,6)],[]]*25,.03,eps,np.random.default_rng(seed),error_budget=1e-7,validate=True,ordering='spectral',mpo=True,combined_frame=not physical,physical=physical,combined_physical=physical)
   rows.append(dict(physical=physical,eps=eps,seed=seed,**s))
Path(__file__).with_name('combined_validation.json').write_text(json.dumps(rows,indent=2));print(len(rows),max(s['conditional_TV'] for s in rows),max(s['born_error'] for s in rows))
