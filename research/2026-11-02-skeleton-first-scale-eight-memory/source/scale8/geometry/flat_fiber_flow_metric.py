"""Exact flat fiber quotient metric on 1024 boundary classes via a 30-edge flow graph."""
import json,contextlib,io
from collections import deque,Counter
with contextlib.redirect_stdout(io.StringIO()):
 from flat_fiber_boundary_projection import basis
 from flat_parent_face_fiber_test import D1,rank
# Projection of each physical face-syndrome bit into the dual-cycle coordinates.
ports=[sum(((row>>f)&1)<<j for j,row in enumerate(basis)) for f in range(30)]
# Coordinate0 is A; coordinates1..9 are region vertices. Root0 is omitted.
assert all(x.bit_count() in [1,2] for x in ports)
dist={0:0};rep={0:0};queue=deque([0])
while queue:
 x=queue.popleft()
 for f,p in enumerate(ports):
  y=x^p
  if y not in dist:
   dist[y]=dist[x]+1;rep[y]=rep[x]^(1<<f);queue.append(y)
assert len(dist)==1024 and dist[1]==2
assert rank(D1)==20 # 30 edges -11 vertices +1; full cycle span
for q,s in rep.items():
 check=0
 for f,p in enumerate(ports):
  if s>>f&1:check^=p
 assert check==q and s.bit_count()==dist[q]
print(json.dumps(dict(scope=__doc__,graph_vertices=11,physical_syndrome_edges=30,cycle_rank=20,classes=1024,distance_histogram=dict(Counter(dist.values())),coarse_A_only_distance=dist[1],ports=ports,minimum_sections=[dict(charge=q,weight=dist[q],representative=rep[q]) for q in range(1024)]),indent=2))
