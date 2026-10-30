"""Verify all finite graph data needed by the sharp-exponent policy."""
import itertools,json,random
from pathlib import Path

def build(n,Q,E):
 if any(i==0 and j!=0 for i,j in E):return None
 done={0};rank={0:0};history=[];level=0
 while len(done)<n:
  initial={i for i in range(n) if i not in done and any(u==i and v in done for u,v in Q)}
  elig=set(initial);parent={};d={i:0 for i in range(n) if i not in done|initial}
  while True:
   bad={i for i in elig if any(u==i and v not in done|elig for u,v in E)}
   if not bad:break
   for i in bad:
    j=next(v for u,v in sorted(E) if u==i and v not in done|elig)
    parent[i]=j;d[i]=1+d[j]
   elig-=bad
  if not elig:return None
  history.append((parent,d));level+=1
  for i in elig:rank[i]=level
  done|=elig
 danger={i for i in range(n) if any(u==i and rank[v]<=rank[i]-2 for u,v in Q)}
 parents={i:history[rank[i]-2][0][i] for i in danger}
 dist={i:(history[rank[i]-2][1][i] if i in danger else 0) for i in range(n)}
 for i,j in parents.items():
  assert (i,j) in E and rank[i]==rank[j] and dist[i]==1+dist[j]
 assert all(dist[i]==0 for i in set(range(n))-danger)
 assert all(0<=v<=n for v in dist.values())
 assert all(rank[v]>=rank[u]-1 for u,v in Q if u not in danger)
 return dict(ranks=rank,L=max(rank.values()),dangerous=sorted(danger),parents=parents,distance=dist)

count=0;maxL=0
for n in [2,3]:
 edges=[(i,j) for i in range(n) for j in range(n) if i!=j]
 for qb in range(1<<len(edges)):
  Q={e for j,e in enumerate(edges) if qb>>j&1}
  for eb in range(1<<len(edges)):
   E={e for j,e in enumerate(edges) if eb>>j&1};r=build(n,Q,E)
   if r:count+=1;maxL=max(maxL,r['L'])
rng=random.Random(20261030);random_valid=0
for _ in range(2000):
 n=rng.randint(4,8);edges=[(i,j) for i in range(n) for j in range(n) if i!=j]
 Q={e for e in edges if rng.random()<.3};E={e for e in edges if e[0]!=0 and rng.random()<.12}
 r=build(n,Q,E)
 if r:random_valid+=1;maxL=max(maxL,r['L'])
example=build(6,{(1,0),(2,0),(3,1),(4,0),(5,3)},{(2,3),(4,5)})
assert example['L']==3 and example['parents']=={2:3,4:5}
out=dict(exhaustive_graph_pairs=4112,exhaustive_valid_policies=count,random_graphs=2000,
 random_valid_policies=random_valid,max_rank_checked=maxL,three_level_example=example,
 scope='Exact graph policy checks; analytic probability bounds are proved separately.')
print(json.dumps(out,indent=2));Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
