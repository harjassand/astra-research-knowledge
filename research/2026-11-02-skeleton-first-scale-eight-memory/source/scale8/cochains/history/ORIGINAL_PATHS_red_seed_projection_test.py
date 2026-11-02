"""Direct red projection on complete abstract first-step flat seed fixture.
No raw recursive source atlas or metric-preserving coordinate embedding is asserted.
"""
import sys,io,contextlib,json
sys.path.insert(0,'producer-workspace/explicit_memory_witness_20261102')
with contextlib.redirect_stdout(io.StringIO()):
 from flat_parent_face_fiber_test import faces,inc
from sheaf_incidence_compiler import compile_sheaf,nullspace,echelon
colors={};P1=[]
for e,fs in sorted(inc.items()):
 a,b=e; d=len(fs)
 if a[1]==b[1] and a[1] in [0,3]: color='blue';old=1 if a[1]==0 else 2
 elif a[0]==b[0] and a[0] in [0,3]:color='red';old=0
 else:color='degree2' if d==2 else 'red';old=0
 colors[e]=color
 basis=[(1<<d)-1] if color in ['blue','degree2'] else [1|(1<<j) for j in range(1,d)]
 for u in basis:P1.append(old if u.bit_count()%2 else 0)
r=compile_sheaf(faces,colors,True)
def act(cols,v):
 y=0
 for j,c in enumerate(cols):
  if v>>j&1:y^=c
 return y
assert len(P1)==r['C1']
assert all(c.bit_count()%2==p.bit_count()%2 for c,p in zip(r['D1'],P1))
assert all(act(P1,c)==0 for c in r['D0'])
rows=[sum(1<<j for j,c in enumerate(r['D1']) if c>>f&1) for f in range(r['C2'])]
cycles=nullspace(rows,r['C1']);images=[act(P1,c) for c in cycles]
assert all(p in [0,3] for p in images)
assert 3 in images and r['k']==1
out=dict(scope=__doc__,dimensions=[r[k] for k in ['C0','C1','C2']],ranks=[r['rank_delta0'],r['rank_delta1']],H0=r['C0']-r['rank_delta0'],H1=r['k'],H2=r['C2']-r['rank_delta1'],P2='total parity of all 30 faces',P1=P1,cochain_degree0=True,cochain_degree1=True,H1_map_surjective=True,H1_map_isomorphism=True)
print(json.dumps(out,indent=2))
