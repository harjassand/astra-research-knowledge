"""All-pairs packet metric on the actual four glued-cross stars of one hashtag.
Checks XOR-atom optimum equals occupied-vertex matching optimum for all4096 patterns.
"""
from itertools import combinations
from collections import deque,Counter
from functools import lru_cache
import json
pairs=set()
for x in [1,2]:
 for y in [1,2]:
  N=(x-1)*3+y;S=N-1;E=6+(y-1)*3+x;W=E-1
  for i,j in combinations([N,S,E,W],2):pairs.add((min(i,j),max(i,j)))
adj={i:set() for i in range(12)}
for i,j in pairs:adj[i].add(j);adj[j].add(i)
atoms=[1<<i for i in range(12)]+[(1<<i)|(1<<j) for i,j in pairs]
dist={0:0};queue=deque([0])
while queue:
 s=queue.popleft()
 for a in atoms:
  t=s^a
  if t not in dist:dist[t]=dist[s]+1;queue.append(t)
@lru_cache(None)
def matching(s):
 if not s:return 0
 i=(s&-s).bit_length()-1;t=s^(1<<i)
 return min([1+matching(t)]+[1+matching(t^(1<<j)) for j in adj[i] if t>>j&1])
for s in range(4096):
 assert matching(s)==dist[s]
 assert s.bit_count()/2<=dist[s]<=s.bit_count()
print(json.dumps(dict(vertices=12,pair_atoms=len(pairs),max_degree=max(map(len,adj.values())),tested_patterns=4096,all_passed=True,distance_histogram=dict(Counter(dist.values())),pairs=sorted(pairs)),indent=2))
