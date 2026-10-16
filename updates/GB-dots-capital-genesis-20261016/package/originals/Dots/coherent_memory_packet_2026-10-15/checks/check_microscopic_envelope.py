from itertools import combinations
import json
# Index 0 center; 1..4 predecessors; 5..8 successors; 9..14 opposite corners.
pairs=list(combinations(range(4),2))
edges=[(0,1+i) for i in range(4)]+[(0,5+i) for i in range(4)]
for k,(i,j) in enumerate(pairs): edges += [(5+i,9+k),(5+j,9+k)]
endpoints=[(1<<a)|(1<<b) for a,b in edges]
support=[0]*(1<<20)
for m in range(1,1<<20):
 bit=m&-m; support[m]=support[m^bit]|endpoints[bit.bit_length()-1]
def env(s):
 out=s
 if not(s&30): out &= ~1
 for k,(i,j) in enumerate(pairs):
  if s&1 and s&(1<<(5+i)) and s&(1<<(5+j)): out|=1<<(9+k)
 return out
def correction(m):
 incoming=m&15; outgoing=(m>>4)&15
 if incoming or outgoing.bit_count()%2 or not outgoing:return 0
 dirs=[i for i in range(4) if outgoing&(1<<i)]
 toggle=0
 for i,j in zip(dirs[::2],dirs[1::2]):
  k=pairs.index((i,j)); toggle^=(1<<(4+i))|(1<<(4+j))|(1<<(8+2*k))|(1<<(9+2*k))
 return toggle
counts={'active':0,'inactive_incoming':0,'inactive_empty':0}
for m in range(1<<20):
 if (m&255).bit_count()%2:continue
 t=correction(m)
 counts['active' if t else 'inactive_incoming' if m&15 else 'inactive_empty']+=1
 assert support[m^t]&~env(support[m])==0,(m,support[m],t)
# Exhaustively check all comparable adjacent Boolean configurations; this implies monotonicity.
mono=0
for s in range(1<<15):
 for i in range(15):
  if not s&(1<<i):
   assert env(s)&~env(s|(1<<i))==0
   mono+=1
# Every unit-face boundary toggles only its four corner vertices, regardless of edge cancellation.
faults=0
for k,(i,j) in enumerate(pairs):
 t=(1<<(4+i))|(1<<(4+j))|(1<<(8+2*k))|(1<<(9+2*k))
 corners=1|(1<<(5+i))|(1<<(5+j))|(1<<(9+k))
 for m in range(1<<20):
  assert support[m^t]&~(support[m]|corners)==0
  faults+=1
report={'correction_configurations':sum(counts.values()),'correction_cases':counts,'monotonicity_cover_pairs':mono,'face_fault_configurations':faults,'failures':0,'note':'All 20 edge bits around the six positive plaquettes enumerated; parity enforced only at center, thus a superset of globally realizable cycles. External edges cannot change the center and can only add occupied vertices at sites never erased.'}
print(json.dumps(report,indent=2))
