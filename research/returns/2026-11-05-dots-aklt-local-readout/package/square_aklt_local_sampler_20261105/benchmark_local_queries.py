from pathlib import Path
from collections import Counter
import time,json
from local_perfect_sampler import LocalPerfectLoopSampler

# Exact pathwise translation check under identical random streams.
a=LocalPerfectLoopSampler([(0,0)],seed=723);b=LocalPerfectLoopSampler([(10**9,-10**9)],seed=723)
for _ in range(100):
 x,s=a.sample();y,t=b.sample();shifted=[tuple((u-10**9,v+10**9) for u,v in p) for p in y]
 assert x==shifted and s==t
cases=[('one_vertex',[(0,0)],2000),('adjacent_pair',[(0,0),(1,0)],2000),
 ('distant_pair',[(0,0),(10**6,10**6)],2000),('eight_vertex_line',[(i,0) for i in range(8)],500),
 ('eight_by_eight',[(i,j) for i in range(8) for j in range(8)],100)]
results=[]
for name,K,n in cases:
 s=LocalPerfectLoopSampler(K,seed=20261105+len(K));start=time.monotonic();work=Counter();hist=Counter();maxclan=0;times=[]
 for k in range(n):
  t=time.monotonic();loops,stats=s.sample();times.append(time.monotonic()-t);work.update(stats);hist[len(loops)]+=1;maxclan=max(maxclan,stats['clan_size'])
  if(k+1)%max(1,n//5)==0:print(name,k+1,'elapsed',time.monotonic()-start,flush=True)
 r={'case':name,'query_vertices':len(K),'samples':n,'elapsed_seconds':time.monotonic()-start,'mean_seconds':sum(times)/n,
 'maximum_seconds':max(times),'mean_target_loops':sum(k*v for k,v in hist.items())/n,
 'mean_work':{k:v/n for k,v in work.items()},'max_clan':maxclan,'physical_volume':'infinite square lattice',
 'scope':'Wall-time diagnostics, not a guaranteed latency. Every stochastic and geometric cutoff is absent.'}
 results.append(r);print(json.dumps(r),flush=True)
 (Path(__file__).parent/'local_query_benchmarks.json').write_text(json.dumps({'translation_check_draws':100,'results':results},indent=2)+'\n')
