"""Complete reduced first red-step seed: direct parent-face parity cochain projection.
Source-compatible declared flat-cylinder realization; not the full recursive atlas.
"""
import json,contextlib,io
with contextlib.redirect_stdout(io.StringIO()):
 from flat_parent_face_fiber_test import faces,inc
from sheaf_incidence_compiler import compile_sheaf,nullspace,echelon
colors={}
for e,fs in inc.items():
 if len(fs)==2:continue
 a,b=e
 if a[1]==b[1] and a[1] in [0,3]:color='blue'
 elif a[0]==b[0] and a[0] in [0,3]:color='red'
 else:color='red'
 colors[e]=color
r=compile_sheaf(faces,colors,True)
P1=[]
for e,fs in sorted(inc.items()):
 d=len(fs);c=colors.get(e,'degree2');dim=1 if c in ['blue','degree2'] else d-1
 a,b=e
 image=(1 if a[1]==0 else 2) if a[1]==b[1] and a[1] in [0,3] else 0
 P1.extend([image]*dim)
assert len(P1)==r['C1']
def apply(cols,s):
 o=0
 for j,c in enumerate(cols):
  if s>>j&1:o^=c
 return o
for g,p in zip(r['D1'],P1):assert g.bit_count()%2==p.bit_count()%2
for c in r['D0']:assert apply(P1,c)==0
# Kernel of D1 represented as a row system over qubit coordinates.
rows=[sum(((g>>f)&1)<<j for j,g in enumerate(r['D1'])) for f in range(r['C2'])]
cycles=nullspace(rows,r['C1']);images=[apply(P1,c) for c in cycles]
assert all(p in [0,3] for p in images) and 3 in images
assert r['k']==1
print(json.dumps(dict(scope=__doc__,C0=r['C0'],C1=r['C1'],C2=r['C2'],rank_delta0=r['rank_delta0'],rank_delta1=r['rank_delta1'],k=r['k'],P1=P1,P2='total parity of30 fine faces',P0='zero (seed C0=0)',cochain_identities_passed=True,logical_projection_rank=1),indent=2))
