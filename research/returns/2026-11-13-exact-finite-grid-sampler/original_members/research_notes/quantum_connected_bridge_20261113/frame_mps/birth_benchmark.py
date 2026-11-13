import numpy as np,json,time
from scipy.stats import beta
from pathlib import Path
from mps_sampler import safe_sample
OUT=Path(__file__).parent
p=[];w=32
for a in [0,1]:p.append([(y*w+x,y*w+x+1) for y in range(w) for x in range(a,w-1,2)])
for a in [0,1]:p.append([(y*w+x,(y+1)*w+x) for y in range(a,w-1,2) for x in range(w)])
layers=[p[t%4] for t in range(100)];rows=[];summary=[]
for physical in [False,True]:
 for birth in [False,True]:
  vals=[]
  for seed in range(30000,30003):
   cpu=time.process_time();wall=time.perf_counter()
   try:_,s=safe_sample(1024,layers,.03,.05,np.random.default_rng(seed),chi=64,strict=True,physical=physical,ordering='spectral',mpo=True,error_budget=1e-4,early=True,compact=True,birth_order=birth,per_gate_budget=True,max_cpu=10,max_wall=30)
   except Exception as e:s=dict(aborted=True,reason='numerical_or_implementation_error',error=repr(e))
   s.update(cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall,physical=physical,birth_order=birth,seed=seed);rows.append(s);vals.append(s);(OUT/'birth_results.json').write_text(json.dumps(rows,indent=2));print(s,flush=True)
  k=sum(s['aborted'] for s in vals);upper=float(beta.ppf(.99,k+1,3-k)) if k<3 else 1.
  summary.append(dict(physical=physical,birth_order=birth,failures=k,trials=3,upper_abort99=upper,mean_cpu=float(np.mean([s['cpu_seconds'] for s in vals]))));(OUT/'birth_summary.json').write_text(json.dumps(summary,indent=2))
