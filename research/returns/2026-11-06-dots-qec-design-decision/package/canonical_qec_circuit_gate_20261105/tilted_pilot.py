"""Floating pilot of the tilted canonical proposal; no confidence claim."""
import sys,json,time,numpy as np
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'canonical_qec_witness_20261105'))
from sampler import Model,pymatching
from scipy.sparse import csr_matrix
class CircuitModel(Model):
 def __init__(self,G):
  self.edges=[tuple(x) for x in G['edges']];nd=G['internal_vertices'];n=max(max(e) for e in self.edges)+1
  self.left=G['left'];self.right=set(G['right']);self.checks=list(range(nd));self.checkid={v:v for v in self.checks};self.adj=[[] for _ in range(n)];self.cut=[];self.edge_checks=[];self.m=pymatching.Matching()
  left=set(self.left)
  for i,(u,v) in enumerate(self.edges):
   self.adj[u].append((v,i));self.adj[v].append((u,i));ends=[z for z in (u,v) if z<nd];self.edge_checks.append(ends)
   if u in left or v in left:self.cut.append(i)
   if len(ends)==2:self.m.add_edge(*ends,fault_ids={i},weight=G['costs'][i])
   else:self.m.add_boundary_edge(ends[0],fault_ids={i},weight=G['costs'][i])
  for a in self.adj:a.sort(key=lambda x:x[1])
 def witness(self,e):
  # Same selector, but the certificate checks weighted rather than unweighted cost.
  from collections import deque
  c=self.decode(e);r=e^c
  if int(r[self.cut].sum())%2==0:return None
  parents={v:None for v in self.left};q=deque(self.left);last=None
  while q:
   u=q.popleft()
   if u in self.right:last=u;break
   for v,edge in self.adj[u]:
    if r[edge] and v not in parents:parents[v]=(u,edge);q.append(v)
  assert last is not None
  path=[]
  while parents[last] is not None:last,edge=parents[last];path.append(edge)
  return tuple(path[::-1])

def run(shots=10000):
 start=time.perf_counter();root=Path(__file__).parent;G=json.loads((root/'d13_r13_p1_1000_graph.json').read_text());m=CircuitModel(G);p=np.array([e['p_float'] for e in G['errors']]);c=np.array(G['costs']);g=(1-p)*2.**(-c)+p*2.**c;qtilt=p*2.**c/g
 states=[]
 for i,(u,v) in enumerate(m.edges):states.extend([(u,v,i),(v,u,i)])
 sid={(u,v):i for i,(u,v,e) in enumerate(states)};nxt=[];rows=[];cols=[];vals=[]
 for i,(u,v,e) in enumerate(states):
  ns=[sid[v,w] for w,f in m.adj[v] if w!=u] if v in m.checkid else [];nxt.append(ns)
  for j in ns:rows.append(i);cols.append(j);vals.append(g[states[j][2]])
 T=csr_matrix((vals,(rows,cols)),shape=(len(states),len(states)));h=[np.array([float(v in m.right) for u,v,e in states])];M=150
 for l in range(1,M):h.append(T@h[-1])
 starts=[sid[u,m.adj[u][0][0]] for u in m.left];startg=np.array([g[states[i][2]] for i in starts]);lw=np.array([float(startg@x[starts]) for x in h]);Z=float(lw.sum());setup=time.perf_counter()-start
 rng=np.random.default_rng(2026110513);counts={x:0 for x in ['nonsimple','not_failure','other_witness','tilt_reject','accepted']};ts=time.perf_counter()
 for _ in range(shots):
  L=1+int(rng.choice(M,p=lw/Z));sw=startg*h[L-1][starts];s=starts[int(rng.choice(len(starts),p=sw/sw.sum()))];u,v,edge=states[s];vertices=[u,v];path=[edge]
  for rem in range(L-1,0,-1):
   ns=nxt[s];ww=np.array([g[states[j][2]]*h[rem-1][j] for j in ns]);s=ns[int(rng.choice(len(ns),p=ww/ww.sum()))];u,v,edge=states[s];vertices.append(v);path.append(edge)
  if len(set(vertices))!=len(vertices):counts['nonsimple']+=1;continue
  e=(rng.random(len(p))<p).astype(np.uint8);e[path]=(rng.random(len(path))<qtilt[path])
  witness=m.witness(e)
  if witness is None:counts['not_failure']+=1;continue
  if witness!=tuple(path):counts['other_witness']+=1;continue
  score=int(np.sum(c[path]*(2*e[path].astype(int)-1)));assert score>=0
  if rng.random()>=2.**(-score):counts['tilt_reject']+=1;continue
  counts['accepted']+=1
 out={'scope':'floating feasibility pilot only; no certified rate or confidence claim','shots':shots,'counts':counts,'Z_float':Z,'point_estimate_diagnostic':Z*counts['accepted']/shots,'setup_seconds':setup,'sampling_seconds':time.perf_counter()-ts,'total_seconds':time.perf_counter()-start}
 (root/'tilted_pilot_d13.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
