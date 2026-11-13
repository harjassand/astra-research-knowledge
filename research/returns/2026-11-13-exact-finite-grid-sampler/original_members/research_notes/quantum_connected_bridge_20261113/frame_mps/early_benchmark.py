import json,numpy as np,time
from pathlib import Path
from mps_sampler import safe_sample

def grid(h,w,d):
 p=[]
 for a in [0,1]:p.append([(y*w+x,y*w+x+1) for y in range(h) for x in range(a,w-1,2)])
 for a in [0,1]:p.append([(y*w+x,(y+1)*w+x) for y in range(a,h-1,2) for x in range(w)])
 return [p[t%4] for t in range(d)]
rows=[]
for phys in [False,True]:
 for seed in range(10):
  cpu=time.process_time();_,s=safe_sample(256,grid(16,16,100),.03,.02,np.random.default_rng(14000+seed),chi=128,strict=True,physical=phys,ordering='minla',mpo=True,error_budget=1e-4,early=True);s['cpu_seconds']=time.process_time()-cpu;s['physical']=phys;s['seed']=14000+seed;rows.append(s);Path(__file__).with_name('early_results.json').write_text(json.dumps(rows,indent=2));print(phys,seed,s['aborted'],s['seconds'],s.get('max_bond'),flush=True)
