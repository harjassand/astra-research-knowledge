import json,numpy as np,time
from pathlib import Path
from mps_sampler import safe_sample

def grid(h,w,d):
 p=[]
 for a in [0,1]:p.append([(y*w+x,y*w+x+1) for y in range(h) for x in range(a,w-1,2)])
 for a in [0,1]:p.append([(y*w+x,(y+1)*w+x) for y in range(a,h-1,2) for x in range(w)])
 return [p[t%4] for t in range(d)]
rows=[]
for order,phys in [('spectral',False),('spectral',True)]:
 vals=[]
 for seed in range(5):
  _,s=safe_sample(256,grid(16,16,100),.03,.02,np.random.default_rng(9000+seed),chi=256,tol=1e-12,strict=True,physical=phys,ordering=order);vals.append(s)
 row=dict(order=order,physical=phys,aborts=sum(s['aborted'] for s in vals),mean_seconds=float(np.mean([s['seconds'] for s in vals])),raw=vals);rows.append(row);Path(__file__).with_name('ordering256_results.json').write_text(json.dumps(rows,indent=2));print({k:v for k,v in row.items() if k!='raw'},flush=True)
