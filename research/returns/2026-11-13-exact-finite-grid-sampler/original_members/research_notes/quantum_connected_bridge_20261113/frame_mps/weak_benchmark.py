import numpy as np,time,json
from pathlib import Path
from mps_sampler import safe_sample as rare
from weak_unravelling import safe_sample as weak
OUT=Path(__file__).parent;rows=[]
def grid(w):
 p=[]
 for a in[0,1]:p.append([(y*w+x,y*w+x+1) for y in range(w) for x in range(a,w-1,2)])
 for a in[0,1]:p.append([(y*w+x,(y+1)*w+x) for y in range(a,w-1,2) for x in range(w)])
 return[p[t%4] for t in range(100)]
for w,base in [(4,40000),(16,41000)]:
 fails=0
 for mode in['rare','weak']:
  for seed in range(base,base+3):
   cpu=time.process_time();wall=time.perf_counter()
   try:
    if mode=='rare':_,s=rare(w*w,grid(w),.03,.05,np.random.default_rng(seed),chi=64,error_budget=1e-4,physical=True,mpo=True,early=True,compact=True,per_gate_budget=True,strict=True,max_cpu=10,max_wall=30)
    else:_,s=weak(w*w,grid(w),.03,.05,np.random.default_rng(seed),chi=64,error_budget=1e-4,max_cpu=10,max_wall=30)
   except Exception as e:s=dict(aborted=True,reason='numerical_or_implementation_error',error=repr(e))
   s.update(cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall,width=w,mode=mode,seed=seed);rows.append(s);fails+=int(mode=='weak' and s['aborted']);(OUT/'weak_results.json').write_text(json.dumps(rows,indent=2));print(s,flush=True)
 if w==4 and fails>=2:
  (OUT/'weak_stop.json').write_text(json.dumps(dict(reason='predeclared weak pilot failure',failures=fails,trials=3)));break
