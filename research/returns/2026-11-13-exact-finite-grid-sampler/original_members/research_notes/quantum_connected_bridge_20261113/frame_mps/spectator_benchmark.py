import numpy as np,json,time
from pathlib import Path
from mps_sampler import safe_sample
from segment_cycle_counts import grid
OUT=Path(__file__).parent;rows=[]
for spectator in[False,True]:
 for seed in range(70000,70005):
  cpu=time.process_time();wall=time.perf_counter()
  try:_,s=safe_sample(1024,grid(32,100),.03,.05,np.random.default_rng(seed),chi=64,strict=True,physical=True,ordering='spectral',mpo=True,error_budget=1e-4,early=True,compact=True,per_gate_budget=True,spectator=spectator,max_cpu=10,max_wall=30)
  except Exception as e:s=dict(aborted=True,reason='numerical_or_implementation_error',error=repr(e))
  s.update(cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall,spectator=spectator,seed=seed);rows.append(s);(OUT/'spectator_results.json').write_text(json.dumps(rows,indent=2));print(s,flush=True)
