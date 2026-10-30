"""Exact exhaustive finite criterion check; no CTMC recurrence simulation."""
from itertools import product
import json
def find(n,Q,E):
 if any(i==0 and j!=0 for i,j in E):return None
 ranks={0:0};level=1
 while len(ranks)<n:
  C={i for i in range(1,n) if i not in ranks and any((i,j) in Q for j in ranks)}
  while True:
   bad={i for i in C if any(j not in ranks and j not in C for k,j in E if k==i)}
   if not bad:break
   C-=bad
  if not C:return None
  ranks.update({i:level for i in C});level+=1
 return ranks
def valid(n,Q,E,r):
 return all(r[j]<=r[i] for i,j in E) and all(any((i,j) in Q and r[j]<r[i] for j in range(n)) for i in range(1,n))
n=3;edges=[(i,j) for i in range(n) for j in range(n) if i!=j];cases=0;accepted=0
for qb in range(1<<len(edges)):
 Q={e for k,e in enumerate(edges) if qb>>k&1}
 for eb in range(1<<len(edges)):
  E={e for k,e in enumerate(edges) if eb>>k&1}
  r=find(n,Q,E)
  exists=any(valid(n,Q,E,{0:0,1:a,2:b}) for a,b in product(range(1,n),repeat=2))
  assert (r is not None)==exists,(Q,E,r,exists)
  if r is not None:assert valid(n,Q,E,r);accepted+=1
  cases+=1
# Genuine non-a excess: 2->1, 1->0 baseline; extra 2->1 allowed.
Q={(2,1),(1,0)};E={(2,1)};example=find(3,Q,E)
assert example=={0:0,1:1,2:2}
print(json.dumps({'all_directed_graph_pairs_3_types':cases,'accepted':accepted,'criterion_complete_on_exhaustion':True,'non_a_excess_example':example,'scope':'finite rank-criterion algebra only; actual generator and global transfer separate'},indent=2))
