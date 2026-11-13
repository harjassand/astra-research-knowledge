import json,numpy as np
from pathlib import Path
from mps_sampler import safe_sample

def grid(h,w,d):
 p=[]
 for a in [0,1]:p.append([(y*w+x,y*w+x+1) for y in range(h) for x in range(a,w-1,2)])
 for a in [0,1]:p.append([(y*w+x,(y+1)*w+x) for y in range(a,h-1,2) for x in range(w)])
 return [p[t%4] for t in range(d)]
rows=[]
for h,w,chi,trials,phys in [(8,8,128,30,False),(8,8,128,30,True),(16,16,128,5,False)]:
 vals=[]
 for seed in range(trials):
  _,s=safe_sample(h*w,grid(h,w,100),.03,.02,np.random.default_rng(9000+seed),chi=chi,tol=1e-11,strict=True,physical=phys);vals.append(s)
 row=dict(h=h,w=w,chi=chi,trials=trials,physical=phys,aborts=sum(s['aborted'] for s in vals),mean_seconds=float(np.mean([s['seconds'] for s in vals])),max_error=max(s['path_error_sum'] for s in vals),raw=vals);rows.append(row);Path(__file__).with_name('strict128_results.json').write_text(json.dumps(rows,indent=2));print({k:v for k,v in row.items() if k!='raw'},flush=True)
