import numpy as np,json
from mps_sampler import sample
from pathlib import Path

def grid(h,w,d):
 p=[]
 for a in [0,1]:p.append([(y*w+x,y*w+x+1) for y in range(h) for x in range(a,w-1,2)])
 for a in [0,1]:p.append([(y*w+x,(y+1)*w+x) for y in range(a,h-1,2) for x in range(w)])
 return [p[t%4] for t in range(d)]
rows=[]
for h,w,chi,trials,physical,validate in [(2,4,None,100,False,True),(2,4,None,100,True,True),(8,8,32,10,False,False),(8,8,32,10,True,False),(8,8,64,10,False,False),(16,16,32,3,False,False)]:
 vals=[]
 for seed in range(trials):
  _,s=sample(h*w,grid(h,w,100),.03,.02,np.random.default_rng(777+seed),chi=chi,tol=1e-10,physical=physical,validate=validate);vals.append(s)
 row=dict(h=h,w=w,chi=chi,trials=trials,physical=physical,means={k:float(np.mean([s[k] for s in vals])) for k in vals[0]},maxima={k:float(max(s[k] for s in vals)) for k in vals[0]},raw=vals);rows.append(row);Path(__file__).with_name('scaling_results.json').write_text(json.dumps(rows,indent=2));print({k:v for k,v in row.items() if k!='raw'},flush=True)
