import numpy as np,json,time
from scipy.stats import beta
from pathlib import Path
from mps_sampler import safe_sample
OUT=Path(__file__).parent

def grid(h,w,d):
 p=[]
 for a in [0,1]:p.append([(y*w+x,y*w+x+1) for y in range(h) for x in range(a,w-1,2)])
 for a in [0,1]:p.append([(y*w+x,(y+1)*w+x) for y in range(a,h-1,2) for x in range(w)])
 return [p[t%4] for t in range(d)]
rows=[];summary=[]
for width,eps in [(32,.02),(32,.05)]:
 regcpu=0
 for physical in [False,True]:
  vals=[]
  for seed in range(20000 if eps==.02 else 22000,20005 if eps==.02 else 22005):
   cpu=time.process_time();wall=time.perf_counter()
   try:
    _,s=safe_sample(width*width,grid(width,width,100),.03,eps,np.random.default_rng(seed),chi=64,strict=True,physical=physical,ordering='spectral',mpo=True,error_budget=1e-4,early=True,max_cpu=10,max_wall=30,compact=True)
   except Exception as e:s=dict(aborted=True,reason='numerical_or_implementation_error',error=repr(e))
   s.update(cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall,width=width,epsilon=eps,physical=physical,seed=seed);rows.append(s);vals.append(s);regcpu+=s['cpu_seconds'];(OUT/'compact_results.json').write_text(json.dumps(rows,indent=2));print(s,flush=True)
  k=sum(v['aborted'] for v in vals);n=len(vals);upper=float(beta.ppf(1-.01,k+1,n-k)) if k<n else 1.
  summary.append(dict(width=width,epsilon=eps,physical=physical,failures=k,trials=n,simultaneous95_upper_abort=upper,mean_cpu=float(np.mean([v['cpu_seconds'] for v in vals])),mean_wall=float(np.mean([v['wall_seconds'] for v in vals]))));(OUT/'compact_summary.json').write_text(json.dumps(summary,indent=2))
 if regcpu>=100:
  (OUT/'compact_stop.json').write_text(json.dumps(dict(after_width=width,after_epsilon=eps,reason='aggregate CPU guard',cpu=regcpu)));break
