"""Exact finite graph rejection witnesses; no raw-network stability verdict."""
import itertools,json
from pathlib import Path

def rank_or_witness(n,root,Q,E):
 leave=next(((i,j) for i,j in E if i==root and j!=root),None)
 if leave:return dict(status='FAST_TARGET_DEPARTURE',edge=leave)
 done={root};rank={root:0};level=0
 while len(done)<n:
  initial={i for i in range(n) if i not in done and any(u==i and v in done for u,v in Q)}
  elig=set(initial);parent={};distance={i:0 for i in range(n) if i not in done|initial}
  while True:
   bad={i for i in elig if any(u==i and v not in done|elig for u,v in E)}
   if not bad:break
   for i in bad:
    j=next(v for u,v in sorted(E) if u==i and v not in done|elig)
    parent[i]=j;distance[i]=1+distance[j]
   elig-=bad
  if not elig:
   return dict(status='FAST_RESET_OBSTRUCTION',processed=sorted(done),entry_types=sorted(initial),
               safe_types=sorted(set(range(n))-done-initial),parent=parent,distance=distance)
  level+=1
  for i in elig:rank[i]=level
  done|=elig
 return dict(status='RANK',ranks=rank)

def verify(n,Q,E,w):
 if w['status']=='FAST_TARGET_DEPARTURE':return tuple(w['edge']) in E and w['edge'][0]==0 and w['edge'][1]!=0
 if w['status']=='RANK':
  r=w['ranks'];return r[0]==0 and all(r[i]>0 and any(u==i and r[v]<r[i] for u,v in Q) for i in range(1,n)) and all(r[j]<=r[i] for i,j in E)
 S=set(w['processed']);T=set(w['entry_types']);Z=set(w['safe_types']);d=w['distance'];parent=w['parent']
 assert 0 in S and S|T|Z==set(range(n)) and not(S&T or S&Z or T&Z)
 assert all(not any(u==i and v in S for u,v in Q) for i in Z)
 assert all((i,parent[i]) in E and parent[i] not in S and d[i]==1+d[parent[i]] for i in T)
 assert all(d[i]==0 for i in Z) and all(0<=x<=n for x in d.values())
 return True

n=3;edges=[(i,j) for i in range(n) for j in range(n) if i!=j]
counts={}
for qb in range(1<<len(edges)):
 Q={e for j,e in enumerate(edges) if qb>>j&1}
 for eb in range(1<<len(edges)):
  E={e for j,e in enumerate(edges) if eb>>j&1};w=rank_or_witness(n,0,Q,E)
  assert verify(n,Q,E,w);counts[w['status']]=counts.get(w['status'],0)+1
example=rank_or_witness(3,0,{(2,1),(1,0)},{(1,2)})
out=dict(graph_pairs_checked=sum(counts.values()),counts=counts,example=example,
 scope='Checks graph certificates only; analytic finite-K occupation proof is separate.')
print(json.dumps(out,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
