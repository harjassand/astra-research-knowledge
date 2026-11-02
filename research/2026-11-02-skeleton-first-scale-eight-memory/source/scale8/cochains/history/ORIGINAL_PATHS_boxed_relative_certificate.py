"""Actual Figure20 parent-ID book completion, relative external port boundary.
Checks both inherited seam codes; abstract polygons from source, no coordinate gluing.
"""
import sys,json
from collections import defaultdict
sys.path.insert(0,'producer-workspace/explicit_memory_witness_20261102')
from sheaf_incidence_compiler import nullspace,echelon,solve
examples=json.load(open('producer-workspace/example_6_8_polygon_data.json'))
out=[]
expanded={}
for name,raw in examples.items():
 for mask in range(1,8):
  selected={r for j,r in enumerate(["upper","right","lower"]) if mask>>j&1}
  expanded[(name,mask)]=[(r,p) for r,p in raw if r in selected]
for (name,mask),raw in expanded.items():
 seam=set('OPQ' if name=='doubled_T_left' else 'OPQR')
 faces=[[v if v in seam else r+':'+v for v in p] for r,p in raw]
 E=defaultdict(list);VF=defaultdict(set);VE=defaultdict(set)
 for j,p in enumerate(faces):
  for v in p:VF[v].add(j)
  for a,b in zip(p,p[1:]+p[:1]):
   e=tuple(sorted((a,b)));E[e].append(j);VE[a].add(e);VE[b].add(e)
 seam_edges={tuple(sorted(e)) for e in zip(list('OPQ' if name=='doubled_T_left' else 'OPQR'),list('PQ' if name=='doubled_T_left' else 'PQR'))}; outer={e for e,fs in E.items() if len(fs)==1 and e not in seam_edges}; boundaryV={v for e in outer for v in e}
 for color in ['blue','red']:
  data={};D1=[]
  for e,fs in sorted(E.items()):
   d=len(fs);basis=[(1<<d)-1] if d==2 or color=='blue' else [1|(1<<j) for j in range(1,d)]
   # Outer edge code immaterial to relative complex; choose full singleton.
   if e in outer:basis=[1]
   start=len(D1) if e not in outer else None
   data[e]=(fs,basis,start,echelon(basis))
   if e not in outer:
    D1 += [sum(1<<fs[j] for j in range(d) if u>>j&1) for u in basis]
  D0=[]
  for v,fs0 in sorted(VF.items()):
   if v in boundaryV:continue
   fs=sorted(fs0);pos={f:j for j,f in enumerate(fs)};rows=[]
   for e in VE[v]:
    ef,b,_,_=data[e]
    rows += [sum(1<<pos[ef[j]] for j in range(len(ef)) if u>>j&1) for u in nullspace(b,len(ef))]
   for u in nullspace(rows,len(fs)):
    col=0
    for e in VE[v]:
     ef,b,start,solver=data[e]
     assert start is not None
     restrict=sum(((u>>pos[f])&1)<<j for j,f in enumerate(ef))
     col ^=solve(solver,restrict)<<start
    D0.append(col)
  r0=len(echelon(D0));r1=len(echelon(D1));h=[len(D0)-r0,len(D1)-r0-r1,len(faces)-r1]
  assert h[:2]==[0,0]
  degree=mask.bit_count()
  assert h[2]==(degree-1 if color=='blue' else 1)
  out.append(dict(name=name,page_mask=mask,seam=color,dims=[len(D0),len(D1),len(faces)],ranks=[r0,r1],H=h,outer_edges=sorted(outer),relative_vertices=sorted(set(VF)-boundaryV)))
print(json.dumps(out,indent=2))
