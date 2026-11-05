"""Floating gate: forbid clean two-edge nongeodesic triangle segments.
This necessary MWPM condition retains every selected residual witness.
No sampling/convergence certificate is asserted by this diagnostic program.
"""
import json,time,numpy as np
from pathlib import Path
from scipy.sparse import csr_matrix
from tilted_pilot import CircuitModel

def run(shots=10000):
 start=time.perf_counter();root=Path(__file__).parent;G=json.loads((root/'d13_r13_p1_1000_graph.json').read_text());m=CircuitModel(G);p=np.array([e['p_float'] for e in G['errors']]);cost=np.array(G['costs']);w=np.stack([(1-p)*2.**(-cost),p*2.**cost],axis=1)
 directed=[]
 for i,(u,v) in enumerate(m.edges):directed.extend([(u,v,i),(v,u,i)])
 sid={(u,v):i for i,(u,v,e) in enumerate(directed)};shortcut={(min(u,v),max(u,v)):cost[e] for e,(u,v) in enumerate(m.edges)}
 states=[(u,v,e,bit) for u,v,e in directed for bit in range(2)];nxt=[];row=[];col=[];vals=[];blocked=0
 for i,(u,v,e,oldbit) in enumerate(states):
  ns=[]
  if v in m.checkid:
   for z,f in m.adj[v]:
    if z==u:continue
    short=shortcut.get((min(u,z),max(u,z)),10**9)<cost[e]+cost[f]
    for bit in range(2):
     if oldbit==bit==0 and short:blocked+=1;continue
     j=2*sid[v,z]+bit;ns.append(j);row.append(i);col.append(j);vals.append(w[f,bit])
  nxt.append(ns)
 T=csr_matrix((vals,(row,col)),shape=(len(states),len(states)));h=[np.array([float(v in m.right) for u,v,e,bit in states])];M=150
 for l in range(1,M):h.append(T@h[-1])
 starts=[2*sid[u,m.adj[u][0][0]]+bit for u in m.left for bit in range(2)];sw0=np.array([w[states[i][2],states[i][3]] for i in starts]);lw=np.array([float(sw0@x[starts]) for x in h]);Z=float(lw.sum());setup=time.perf_counter()-start
 rng=np.random.default_rng(2026110514);counts={x:0 for x in ['nonsimple','negative_score','tilt_reject','not_failure','other_witness','accepted']};ts=time.perf_counter()
 for _ in range(shots):
  L=1+int(rng.choice(M,p=lw/Z));sw=sw0*h[L-1][starts];s=starts[int(rng.choice(len(starts),p=sw/sw.sum()))];u,v,e,bit=states[s];vertices=[u,v];path=[e];bits=[bit]
  for rem in range(L-1,0,-1):
   ns=nxt[s];ww=np.array([w[states[j][2],states[j][3]]*h[rem-1][j] for j in ns]);s=ns[int(rng.choice(len(ns),p=ww/ww.sum()))];u,v,e,bit=states[s];vertices.append(v);path.append(e);bits.append(bit)
  if len(set(vertices))!=len(vertices):counts['nonsimple']+=1;continue
  score=int(np.sum(cost[path]*(2*np.array(bits)-1)))
  if score<0:counts['negative_score']+=1;continue
  if rng.random()>=2.**(-score):counts['tilt_reject']+=1;continue
  errors=(rng.random(len(p))<p).astype(np.uint8);errors[path]=bits
  witness=m.witness(errors)
  if witness is None:counts['not_failure']+=1;continue
  if witness!=tuple(path):counts['other_witness']+=1;continue
  counts['accepted']+=1
 out={'scope':'floating geodesic witness feasibility pilot only; no certified rate','shots':shots,'counts':counts,'blocked_clean_triangle_transitions':blocked,'Z_float':Z,'normalizer_reduction_vs_unrestricted':.00021008319110677544/Z,'mean_path_length':float(np.dot(lw,np.arange(1,M+1))/Z),'point_estimate_diagnostic':Z*counts['accepted']/shots,'setup_seconds':setup,'sampling_seconds':time.perf_counter()-ts,'total_seconds':time.perf_counter()-start}
 (root/'geodesic_tilted_pilot_d13.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
