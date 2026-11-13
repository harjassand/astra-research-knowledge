"""Predeclared5 paired CATEGORY records perrate, exactcomponents vsstrongcompactdirectMPS.
Different Born streams; descriptivecost pilot, not accuracy or scaling certification.
"""
import sys,time,random,json,copy,statistics
from pathlib import Path
from fractions import Fraction as F
import numpy as np
import exact_component_sampler as exact
sys.path.insert(0,str(Path('research_notes/quantum_connected_bridge_20261113/frame_mps').resolve()))
import mps_sampler as mps

def makeplan(n,layers,events):
 neigh=[set() for _ in range(n)]
 for layer in layers:
  for u,v in layer:neigh[u].add(v);neigh[v].add(u)
 parent=list(range(n));site=list(range(n));cur=list(range(n));records=[];at=0
 def root(x):
  while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
  return x
 for layer in layers:
  ev=[];cuts=set();before=cur.copy()
  for u,v in layer:
   a,b,kind=events[at];at+=1;assert(u,v)==(a,b);reset=kind=='R';rare=kind=='Q';ev.append(((u,v),reset,rare,rare))
   if reset:cuts.update((u,v))
   if rare:
    ids=[cur[w] for w in({u,v}|neigh[u]|neigh[v])]
    for x in ids[1:]:parent[root(x)]=root(ids[0])
  for s in cuts:cur[s]=len(parent);parent.append(len(parent));site.append(s)
  records.append((ev,cuts,before,cur.copy()))
 roots=[root(i) for i in range(len(parent))];supports={}
 for i,s in enumerate(site):supports.setdefault(roots[i],set()).add(s)
 return records,roots,{c:sorted(s) for c,s in supports.items()},neigh

original_record=exact.Engine.record;deadline=[0.]
def capped_record(self):
 if time.process_time()>deadline[0]:raise exact.Limit('CPU20sec')
 return original_record(self)
exact.Engine.record=capped_record
rows=[];layers=exact.grid_layers(32,32,100)
for eps in [F(1,50),F(1,20)]:
 for j in range(5):
  seed=70000+j;start=time.perf_counter();cpu=time.process_time();events=exact.categories(layers,F(3,100),eps,random.Random(seed));categorywall=time.perf_counter()-start;categorycpu=time.process_time()-cpu
  start=time.perf_counter();cpu=time.process_time();deadline[0]=cpu+20
  output,a=exact.sample(1024,layers,eps=eps,seed=seed+1000,events=events,cap=4096,bitcap=20000)
  a.update(method='exact_gaussian',category_seed=seed,epsilon=str(eps),all_in_wall=time.perf_counter()-start+categorywall,all_in_cpu=time.process_time()-cpu+categorycpu,output=str(output));rows.append(a)
  def injected_plan(n,ls,r,e,rng):return makeplan(n,ls,events)
  mps.plan=injected_plan
  start=time.perf_counter();cpu=time.process_time();output,b=mps.safe_sample(1024,layers,.03,float(eps),np.random.default_rng(seed+2000),chi=128,error_budget=1e-4,strict=True,physical=True,mpo=True,early=True,compact=True,ordering='spectral',per_gate_budget=True,bridge_prune=True,max_cpu=20)
  b.update(method='compact_direct_MPS',category_seed=seed,epsilon=str(eps),all_in_wall=time.perf_counter()-start+categorywall,all_in_cpu=time.process_time()-cpu+categorycpu,output=str(output),graph_metadata='actual-category-star conservative graph, not independent auxiliary graph certificate');rows.append(b)
  Path(__file__).with_suffix('.json').write_text(json.dumps({'rows':rows,'scope':'Sameexactrationalcategoryrecords;differentBornstreams. Exactcap4096entries/20000bits vsMPSchi128/delta1e-4, bothCPU20s. All-in costs include category generation, graphpreprocessing and output. Small descriptivepilot, not reliability/scaling theorem; memorymetrics not identical.'},indent=2))
  print(str(eps),j,'exact',a['aborted'],a['all_in_cpu'],'MPS',b['aborted'],b['all_in_cpu'],flush=True)
