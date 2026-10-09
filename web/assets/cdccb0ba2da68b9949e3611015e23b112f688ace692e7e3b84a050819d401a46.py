import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from completion import CompletionSampler
from sampler import enumerate_target
from instances import diffusion_gram
import numpy as np,time,json
from pathlib import Path
rows=[]
for mode in ['local','irregular','cycle']:
 for beta in [100.,10000.]:
  n=12; G,meta=diffusion_gram(n,314,mode)
  X=np.sqrt(beta)*np.array(meta['feature_matrix']).T
  start=time.perf_counter(); obj=CompletionSampler(X,np.repeat(np.arange(n),2))
  prep=time.perf_counter()-start
  start=time.perf_counter(); samples,diag=obj.sample(2000,51,max_trials=12000000)
  secs=time.perf_counter()-start
  ids=((samples%2)*(1<<np.arange(n))).sum(axis=1)
  p,z,logs=enumerate_target(G,beta)
  hist=np.bincount(ids,minlength=len(p))/len(ids)
  exact_acc=float(np.exp(z-n*np.log(2)-obj.log_dpp_normalizer))
  row=dict(mode=mode,beta=beta,preprocess_seconds=prep,seconds=secs,
        exact_acceptance=exact_acc,tv=float(.5*np.abs(hist-p).sum()),**diag)
  rows.append(row); print(row,flush=True)
Path('results/completion_pilot.json').write_text(json.dumps(rows,indent=2))
