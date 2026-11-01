from itertools import product
from collections import deque
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

def check(name,n,edges):
 incident=[[j for j,e in enumerate(edges) if v in e] for v in range(n)]
 phases=[]
 for v in range(n):
  d=len(incident[v]);phases.append([('C',j) for j in range(d+1)]+[('W',0)]+[('K',j) for j in range(d+1)]+[('A',0)])
 domains=phases+[tuple([-1]+list(e)) for e in edges]
 states=list(product(*domains));index={s:i for i,s in enumerate(states)}
 def locallegal(s,v):
  typ,j=s[v]; own=[s[n+e]==v for e in incident[v]]
  if typ=='C':return not any(own[:j])
  if typ=='W':return not any(own)
  if typ=='K':return all(own[:j]) and not any(own[j:])
  return all(own)
 def successors(s):
  for v in range(n):
   typ,j=s[v];d=len(incident[v]);t=list(s)
   if typ=='C':
    if j==d:t[v]=('W',0)
    else:
     e=incident[v][j]
     if t[n+e]==v:t[n+e]=-1
     t[v]=('C',j+1)
   elif typ=='W':t[v]=('K',0)
   elif typ=='K':
    if j==d:t[v]=('A',0)
    else:
     e=incident[v][j]
     if t[n+e] in (-1,v):t[n+e]=v;t[v]=('K',j+1)
     else:t[v]=('C',0)
   else:t[v]=('C',0) # STRUCTURAL native completion, not quantum timing model.
   yield v,tuple(t)
 rows=[];cols=[];legal=[];violations=0
 for i,s in enumerate(states):
  good=[locallegal(s,v) for v in range(n)];legal.append(all(good))
  for actor,t in successors(s):
   for v in range(n):
    assert not good[v] or locallegal(t,v),(name,s,actor,t,v)
   rows.append(i);cols.append(index[t])
  if all(good):
   for u,v in edges:assert not(s[u][0]=='A' and s[v][0]=='A')
 graph=csr_matrix((np.ones(len(rows),dtype=np.int8),(rows,cols)),shape=(len(states),)*2)
 ns,lab=connected_components(graph,directed=True,connection='strong')
 closed=np.ones(ns,dtype=bool)
 for u,v in zip(rows,cols):
  if lab[u]!=lab[v]:closed[lab[u]]=False
 badclosed=[i for i,s in enumerate(states) if closed[lab[i]] and not legal[i]]
 assert not badclosed,(name,'bad closed SCC',states[badclosed[0]])
 # Reverse BFS: every arbitrary state can reach the legal invariant set.
 reverse=graph.transpose().tocsr();dist=[-1]*len(states);queue=deque()
 for i,good in enumerate(legal):
  if good:dist[i]=0;queue.append(i)
 while queue:
  x=queue.popleft()
  for y in reverse.indices[reverse.indptr[x]:reverse.indptr[x+1]]:
   if dist[y]<0:dist[y]=dist[x]+1;queue.append(y)
 assert min(dist)>=0
 print(f'{name}: states={len(states)}, transitions={len(rows)}, SCCs={ns}, closed_SCCs={sum(closed)}, legal_states={sum(legal)}, max_shortest_repair={max(dist)}; PASS')
for item in [('isolated',1,[]),('edge',2,[(0,1)]),('path3',3,[(0,1),(1,2)]),('triangle',3,[(0,1),(1,2),(2,0)]),('star4',4,[(0,1),(0,2),(0,3)])]:check(*item)
print('All initial phases and lock values enumerated. ACTIVE completion is an enabled structural edge only; no quantum performance rate inferred.')
