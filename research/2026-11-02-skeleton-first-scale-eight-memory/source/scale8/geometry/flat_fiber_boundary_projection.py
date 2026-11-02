"""Explicit dual cycles and boundary-port projection for flat parent-face fiber.
Formal single-face boundary ports must be restricted/combined using actual old-edge F.
"""
import json,contextlib,io
with contextlib.redirect_stdout(io.StringIO()):
 from flat_parent_face_fiber_test import faces,inc,edges,D1,rank,boundary_edge
A=(1<<9)-1
cycles=[]
for x in range(3):
 for y in range(3):
  j=3*x+y;v=(1<<j)|(1<<(9+j))
  if x>0:v^=1<<(18+(x-1)*3+y)
  if x<2:v^=1<<(18+x*3+y)
  if y>0:v^=1<<(24+(y-1)*3+x)
  if y<2:v^=1<<(24+y*3+x)
  cycles.append(v)
basis=[A]+cycles
assert rank(basis)==10
assert all((v&c).bit_count()%2==0 for v in basis for c in D1)
assert sum([],[])==[] # no-op; keep no hidden numerical dependencies
s=0
for v in cycles:s^=v
assert s==((1<<18)-1)
ports=[]
for edge,fs in sorted(inc.items()):
 if not boundary_edge(edge):continue
 assert len(fs)==1
 f=fs[0];v=1<<f
 proj=sum(((row&v).bit_count()%2)<<j for j,row in enumerate(basis))
 assert not (proj>>(1+4)&1) # central region never meets a boundary port
 a,b=edge
 if a[2]==b[2]:
  j=f%9
  expected=(1<<(1+j))|((1<<0) if f<9 else 0)
  kind='A-sheet' if f<9 else 'B-sheet'
 else:
  supported=[j for j,c in enumerate(cycles) if c>>f&1]
  assert len(supported)==2
  expected=sum(1<<(1+j) for j in supported);kind='rib-endpoint'
 assert proj==expected
 ports.append(dict(edge=edge,face=f,kind=kind,quotient_projection=proj))
assert rank([p['quotient_projection'] for p in ports])==9
# Actual first seed permits only inherited blue y-boundary ports.
seed=[p['quotient_projection'] for p in ports if p['edge'][0][1]==p['edge'][1][1] and p['edge'][0][1] in [0,3]]
assert rank(seed)==7
print(json.dumps(dict(basis_order=['whole_A']+[f'region_{x}_{y}' for x in range(3) for y in range(3)],dual_basis=basis,central_cube_index=5,all_formal_boundary_rank=9,actual_seed_boundary_rank=7,ports=ports),indent=2))
