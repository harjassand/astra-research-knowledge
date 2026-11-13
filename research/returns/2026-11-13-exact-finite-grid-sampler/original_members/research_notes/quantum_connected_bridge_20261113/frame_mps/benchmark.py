import numpy as np,json,time
from mps_sampler import sample
from pathlib import Path
OUT=Path(__file__).parent

def grid(h,w,d):
 phases=[]
 for parity in [0,1]:phases.append([(y*w+x,y*w+x+1) for y in range(h) for x in range(parity,w-1,2)])
 for parity in [0,1]:phases.append([(y*w+x,(y+1)*w+x) for y in range(parity,h-1,2) for x in range(w)])
 return [phases[t%4] for t in range(d)]
rows=[]
def run(h,w,d,eps,chi,tol,trials,physical=False,validate=False):
 vals=[]
 for seed in range(trials):
  _,s=sample(h*w,grid(h,w,d),.03,eps,np.random.default_rng(20261113+seed),chi=chi,tol=tol,physical=physical,validate=validate)
  vals.append(s)
 row=dict(h=h,w=w,d=d,eps=eps,chi=chi,tol=tol,trials=trials,physical=physical,validate=validate,means={k:float(np.mean([s[k] for s in vals])) for k in vals[0]},maxima={k:float(max(s[k] for s in vals)) for k in vals[0]},raw=vals);rows.append(row);(OUT/'results.json').write_text(json.dumps(rows,indent=2));print({k:v for k,v in row.items() if k not in ['raw']},flush=True)
for physical in [False,True]:run(2,4,100,.02,None,1e-12,20,physical,True)
for chi in [2,4,8]:run(2,4,100,.02,chi,1e-12,20,False,True)
for physical in [False,True]:run(4,4,100,.02,16,1e-12,10,physical)
for chi in [8,32]:run(4,4,100,.02,chi,1e-12,10)
run(4,4,100,.02,None,1e-9,5)
for chi in [16,32]:run(4,6,100,.02,chi,1e-12,5)
