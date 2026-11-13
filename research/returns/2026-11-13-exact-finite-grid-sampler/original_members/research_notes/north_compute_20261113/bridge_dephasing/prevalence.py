"""Unfiltered fixed-seed actual category records; multigraph bridges/cores statistics."""
import sys,time,json,statistics
from pathlib import Path
from collections import deque
import numpy as np
sys.path.insert(0,str(Path('research_notes/north_compute_20261113/affine_sampler').resolve()))
from resource_probe import layers
from mps_sampler import plan
from check import bridge_indices

def stats(n,events):
 current=list(range(n));vertices=n;edges=[];ids=[]
 for t,(u,v,kind) in enumerate(events):
  if kind=='Q':edges.append((current[u],current[v]));ids.append(t)
  elif kind=='R':
   current[u]=vertices;current[v]=vertices+1;vertices+=2
 adj=[[] for _ in range(vertices)]
 for i,(u,v) in enumerate(edges):adj[u].append((v,i));adj[v].append((u,i))
 bridge=bridge_indices(n,events);nonbridge={i for i,t in enumerate(ids) if t not in bridge}
 def components(allowed):
  seen=set();result=[]
  for i in allowed:
   u,v=edges[i]
   if u in seen:continue
   stack=[u];seen.add(u);vs=0;es=set()
   while stack:
    x=stack.pop();vs+=1
    for y,e in adj[x]:
     if e not in allowed:continue
     es.add(e)
     if y not in seen:seen.add(y);stack.append(y)
   result.append((vs,len(es),len(es)-vs+1))
  return result
 allcomponents=components(set(range(len(edges))));blocks=components(nonbridge)
 deg=[len(a) for a in adj];keep=set(range(len(edges)));queue=deque(i for i,d in enumerate(deg) if d<=1)
 while queue:
  u=queue.popleft()
  for v,e in adj[u]:
   if e not in keep:continue
   keep.remove(e);deg[u]-=1;deg[v]-=1
   if deg[v]==1:queue.append(v)
 return dict(Q_occurrences=len(edges),bridge_Q=len(bridge),nonbridge_Q=len(nonbridge),two_core_Q=len(keep),cycle_rank=sum(x[2] for x in allcomponents),nonbridge_cycle_rank=sum(x[2] for x in blocks),largest_nonbridge_block_vertices=max([x[0] for x in blocks],default=0),largest_nonbridge_block_Q=max([x[1] for x in blocks],default=0),largest_nonbridge_block_cycle_rank=max([x[2] for x in blocks],default=0),cyclic_blocks=len(blocks))

rows=[];start=time.time()
for width in [16,32]:
 for eps in [.02,.05]:
  vals=[]
  for seed in range(100):
   begin=time.perf_counter();records,*_=plan(width*width,layers(width,100),.03,eps,np.random.default_rng(39200+seed));pt=time.perf_counter()-begin
   events=[(u,v,'R' if reset else 'Q' if rare else 'D') for ev,_,_,_ in records for (u,v),reset,rare,cand in ev]
   begin=time.perf_counter();a=stats(width*width,events);a['bridge_preprocessing_seconds']=time.perf_counter()-begin;a['category_sampling_seconds']=pt;a['seed']=39200+seed;vals.append(a)
  summary={k+'_mean':statistics.mean(v[k] for v in vals) for k in vals[0] if k!='seed'}
  summary['bridge_fraction_of_all_sampled_Q']=sum(v['bridge_Q'] for v in vals)/sum(v['Q_occurrences'] for v in vals)
  rows.append(dict(n=width*width,T=100,r=.03,epsilon=eps,trials=100,summary=summary,raw=vals));print(width,eps,summary,flush=True)
out={'rows':rows,'seconds':time.time()-start,'scope':'Unfiltered independently seeded actual category records. Graph preprocessing only. Cyclic blocks NOT independent quantum states: D may couple their phases. No full sampler runtime/scaling claim.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
