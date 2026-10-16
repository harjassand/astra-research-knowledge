"""Independent statistical diagnostic, not proof of rare-event accuracy."""
import time,json,numpy as np
from kinetics import evolve,grid_edges,splitting
start=time.perf_counter();n=65536
out=evolve(np.full((n,2),50,np.int64),np.zeros(n),grid_edges(1,2),.2,15,60401,-1)
x,t,hit,jumps,peak=out
result={'ssa':{'particles':n,'hits':int(hit.sum()),'p':float(hit.mean()),'events':int(jumps.sum()),'seconds':time.perf_counter()-start,'max_count':int(peak.max())}}
start=time.perf_counter(); reps=[]
for seed in range(4901,4917):
 reps.append(splitting(rows=1,cols=2,particles=128,seed=seed,deadline=.2,levels=tuple(range(47,14,-2))))
ps=np.array([r['estimate'] for r in reps])
result['splitting']={'replicates':reps,'p_mean':float(ps.mean()),'standard_error':float(ps.std(ddof=1)/len(ps)**.5),'events':sum(r['total_events'] for r in reps),'seconds':time.perf_counter()-start}
json.dump(result,open('sampler_validation.json','w'),indent=2)
print(json.dumps({**result['ssa'],'split_mean':ps.mean(),'split_se':ps.std(ddof=1)/4,'split_seconds':result['splitting']['seconds']}))
