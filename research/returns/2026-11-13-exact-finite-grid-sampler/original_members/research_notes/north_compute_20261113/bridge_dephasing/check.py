"""Exact circuit-output bridge-Q dephasing test. Multigraph edge IDs retained."""
import numpy as np,sympy as s,json,itertools,sys
from pathlib import Path

def bridge_indices(n,events):
 current=list(range(n));vertices=n;graph=[[] for _ in range(n)];event_edge={};edge_event=[]
 for t,(u,v,kind) in enumerate(events):
  if kind=='Q':
   a,b=current[u],current[v];eid=len(edge_event);edge_event.append(t);graph[a].append((b,eid));graph[b].append((a,eid));event_edge[t]=eid
  elif kind=='R':
   for w in (u,v):current[w]=vertices;vertices+=1;graph.append([])
 timer=0;tin=[-1]*vertices;low=[-1]*vertices;bridges=set()
 def dfs(v,parentedge=-1):
  nonlocal timer
  tin[v]=low[v]=timer;timer+=1
  for w,e in graph[v]:
   if e==parentedge:continue
   if tin[w]!=-1:low[v]=min(low[v],tin[w])
   else:
    dfs(w,e);low[v]=min(low[v],low[w])
    if low[w]>tin[v]:bridges.add(edge_event[e])
 for v in range(vertices):
  if tin[v]==-1:dfs(v)
 return bridges

def exact(n,events,dephase):
 N=1<<n;rho=s.zeros(N);rho[0,0]=1
 for t,(u,v,kind) in enumerate(events):
  mask=(1<<u)|(1<<v);D=s.diag(*[(3+(4 if ((x>>u)&1)==((x>>v)&1) else -4)*s.I)/5 for x in range(N)]);XX=s.zeros(N)
  for x in range(N):XX[x^mask,x]=1
  rho=D*rho*D.conjugate().T
  if kind=='Q':
   if t in dephase:rho=s.Rational(144,169)*rho+s.Rational(25,169)*XX*rho*XX
   else:
    Q=(12*s.eye(N)-5*s.I*XX)/13;rho=Q*rho*Q.conjugate().T
  elif kind=='R':
   reset=s.zeros(N);rest=[x for x in range(N) if not x&mask];shifts=[0,1<<u,1<<v,mask]
   for x in rest:
    for y in rest:
     tr=sum(rho[x+b,y+b] for b in shifts)/4
     for b in shifts:reset[x+b,y+b]=tr
   rho=reset
  rho=rho.applyfunc(s.expand)
 return [rho[x,x] for x in range(N)]

if __name__=='__main__':
 cases=[[(0,1,'Q'),(1,2,'Q'),(0,2,'D'),(0,1,'Q'),(1,2,'R')],[(0,1,'Q'),(1,2,'Q'),(0,2,'D')],[(0,1,'Q'),(0,1,'Q')],[(0,1,'Q'),(0,1,'R'),(0,1,'Q')]]
 out=[]
 for events in cases:
  bridges=bridge_indices(3,events);a=exact(3,events,set());b=exact(3,events,bridges);assert a==b
  allq={i for i,e in enumerate(events) if e[2]=='Q'};all_dephased=exact(3,events,allq)
  out.append(dict(events=events,bridge_event_indices=sorted(bridges),exact_full_output_equality=True,all_Q_dephasing_also_equal=(a==all_dephased),all_Q_dephasing_TV=str(sum(abs(x-y) for x,y in zip(a,all_dephased))/2)))
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
