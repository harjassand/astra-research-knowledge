"""Fully specified local completion of Fig20 as cellwise subdivisions of a three-page book.
Parent face IDs forbid all extra identifications at internal edges. This verifies
that completion, not an assertion that source prose supplied its full incidence.
"""
import json,contextlib,io,runpy
from collections import defaultdict
from pathlib import Path
p=Path(__file__).parent
examples=json.loads((p/'example_6_8_polygon_data.json').read_text())
reports=[]
for name,faces in examples.items():
 pages={}
 for region in ['upper','right','lower']:
  polys=[poly for r,poly in faces if r==region]
  inc=defaultdict(list);vertices=set()
  for j,poly in enumerate(polys):
   vertices.update(poly)
   for a,b in zip(poly,poly[1:]+poly[:1]):inc[tuple(sorted((a,b)))].append(j)
  assert all(len(v) in [1,2] for v in inc.values())
  internal=[e for e,f in inc.items() if len(f)==2]
  boundary=[e for e,f in inc.items() if len(f)==1]
  assert len(internal)==len(polys)-1
  # Dual graph is a tree, hence inductive disk gluing along one full edge.
  seen={0}
  while True:
   new=seen|{j for fs in inc.values() if len(fs)==2 and any(i in seen for i in fs) for j in fs}
   if new==seen:break
   seen=new
  assert len(seen)==len(polys)
  bd=defaultdict(list)
  for a,b in boundary:bd[a].append(b);bd[b].append(a)
  assert all(len(x)==2 for x in bd.values())
  cycle=['O'];prev=None;cur='O'
  while True:
   nxt=next(v for v in sorted(bd[cur]) if v!=prev)
   if nxt=='O':break
   cycle.append(nxt);prev,cur=cur,nxt
   assert len(cycle)<=len(bd)
  assert len(cycle)==len(bd)
  assert len(vertices)-len(inc)+len(polys)==1
  pages[region]=dict(parent_boundary=cycle,internal_edges=internal,faces=len(polys),vertices=len(vertices),edges=len(inc),euler_characteristic=1,dual_tree=True)
 # Distinct pages are glued only along the designated old seam, with namespaced
 # off-seam vertices; all other geometric coincidences remain disjoint.
 seam={'O','P','Q'} if name=='doubled_T_left' else {'O','P','Q','R'}
 # Explicit old parent-boundary incidences for this local book:
 seam_edges={tuple(sorted(e)) for e in zip(['O','P','Q','R'] if len(seam)==4 else ['O','P','Q'],['P','Q','R'] if len(seam)==4 else ['P','Q'])}
 for reg,d in pages.items():
  assert not (set(map(tuple,d['internal_edges']))&seam_edges)
 reports.append(dict(realization=name,pages=pages,glued_parent_seam=sorted(seam_edges),all_internal_edges_degree2_by_parent_ids=True,physical_global_family_claim=False))
print(json.dumps(reports,indent=2))
