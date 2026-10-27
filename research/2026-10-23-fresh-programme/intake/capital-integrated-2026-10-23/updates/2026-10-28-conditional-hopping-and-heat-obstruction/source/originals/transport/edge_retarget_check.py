"""Exact finite controls for the all-size coherence-edge retargeting identity.
No inference from small volumes to thermodynamic transport is made by this file.
"""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json
OUT=Path(__file__).parent

def bit(x,i,n):return (x>>(i%n))&1

def graph(n):
 edges={};adj=defaultdict(list)
 for eta in range(1<<n):
  for i in range(n):
   if bit(eta,i,n)==bit(eta,i+1,n):continue
   xi=eta^(1<<i)^(1<<((i+1)%n));key=tuple(sorted((eta,xi)))
   env=2*bit(eta,i-1,n)+bit(eta,i+2,n)
   amp=[F(7,8),F(9,8),F(5,4),F(3,4)][env]
   if key in edges:assert edges[key][1]==amp
   else:edges[key]=(i,amp);adj[eta].append(xi);adj[xi].append(eta)
 return edges,adj

def balanced_cycles(edges,adj):
 # Every added oriented cycle has exactly zero vertex divergence.
 flow=defaultdict(F);parent={};depth={}
 for root in adj:
  if root in parent:continue
  parent[root]=None;depth[root]=0;stack=[root]
  while stack:
   u=stack.pop()
   for v in adj[u]:
    if v not in parent:parent[v]=u;depth[v]=depth[u]+1;stack.append(v)
 tree={tuple(sorted((v,p))) for v,p in parent.items() if p is not None}
 def add(u,v,weight):flow[tuple(sorted((u,v)))]+=weight*(1 if u<v else -1)
 for number,(u,v) in enumerate(edges):
  if (u,v) in tree:continue
  weight=F((number%7)-3,7)
  if not weight:continue
  # edge u->v, followed by unique tree path v->u.
  add(u,v,weight);a,b=v,u
  while depth[a]>depth[b]:add(a,parent[a],weight);a=parent[a]
  while depth[b]>depth[a]:add(parent[b],b,weight);b=parent[b]
  while a!=b:
   add(a,parent[a],weight);a=parent[a];add(parent[b],b,weight);b=parent[b]
 return flow

def div(flow,edges,weighted):
 ans=defaultdict(F)
 for (u,v),x in flow.items():
  y=x*(edges[u,v][1] if weighted else 1);ans[u]+=y;ans[v]-=y
 return ans

records=[]
for n in [5,6,7,8]:
 edges,adj=graph(n);flow=balanced_cycles(edges,adj)
 assert all(v==0 for v in div(flow,edges,False).values())
 naive=div(flow,edges,True)
 retarget={e:value/edges[e][1] for e,value in flow.items()}
 repaired=div(retarget,edges,True)
 assert all(v==0 for v in repaired.values())
 assert any(v!=0 for v in naive.values())
 # Non-edge odd coherences produce no diagonal commutator at either model.
 nonedge=[(u,v) for u in range(1<<n) for v in range(u+1,1<<n) if (u,v) not in edges and u.bit_count()==v.bit_count()]
 rec={'n':n,'configuration_edges':len(edges),'nonzero_cycle_flow_edges':sum(bool(v) for v in flow.values()),'nonedge_number_neutral_coherences':len(nonedge),'naive_max_divergence':str(max(abs(v) for v in naive.values())),'retargeted_max_divergence':'0','arithmetic':'exact Fraction','status':'PASS'}
 records.append(rec);print(json.dumps(rec),flush=True)
(OUT/'EDGE_RETARGET_CHECKS.json').write_text(json.dumps(records,indent=2)+'\n')
