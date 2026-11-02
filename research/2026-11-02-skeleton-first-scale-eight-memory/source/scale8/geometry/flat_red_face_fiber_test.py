"""Direct red/parity relative face-fiber test using actual strong-sheaf vertex stalks.
Same topological compacted flat two-rib cellulation as blue fiber; boundary edges excluded.
"""
import contextlib,io,json
with contextlib.redirect_stdout(io.StringIO()):
 from flat_parent_face_fiber_test import faces,inc,edges,vertices
from sheaf_incidence_compiler import nullspace,echelon,solve
D1=[];ed={}
for e in edges:
 fs=inc[e];d=len(fs);local=[1|(1<<j) for j in range(1,d)]
 start=len(D1)
 for x in local:D1.append(sum(1<<fs[j] for j in range(d) if x>>j&1))
 ed[e]=(fs,local,start,echelon(local))
D0=[];stalk_dimensions=[]
for v in vertices:
 ves=[e for e in edges if v in e];vfs=sorted(set(f for e in ves for f in inc[e]));idx={f:j for j,f in enumerate(vfs)}
 constraints=[]
 for e in ves:
  fs,local,start,solver=ed[e]
  for h in nullspace(local,len(fs)):
   constraints.append(sum(1<<idx[fs[j]] for j in range(len(fs)) if h>>j&1))
 stalk=nullspace(constraints,len(vfs));stalk_dimensions.append(len(stalk))
 for u in stalk:
  c=0
  for e in ves:
   fs,local,start,solver=ed[e]
   restriction=sum(((u>>idx[f])&1)<<j for j,f in enumerate(fs))
   c^=solve(solver,restriction)<<start
  image=0
  for j,d in enumerate(D1):
   if c>>j&1:image^=d
  assert image==0
  D0.append(c)
r0,r1=len(echelon(D0)),len(echelon(D1))
result=dict(scope=__doc__,C0=len(D0),C1=len(D1),C2=len(faces),vertex_stalk_dimensions=stalk_dimensions,rankD0=r0,rankD1=r1,H0=len(D0)-r0,H1=len(D1)-r0-r1,H2=len(faces)-r1,metachecks=nullspace(D1,len(faces)),D0=D0,D1=D1)
assert (result['H0'],result['H1'],result['H2'])==(1,0,1)
assert result['metachecks']==[(1<<30)-1]
print(json.dumps(result,indent=2))
