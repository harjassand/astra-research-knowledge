"""Actual Example6.8 polygon lists, not incidence invented from coincident coordinates.
Boundary edges excluded; degree2 interior pairs and inherited OP/PQ/QR seam retained.
"""
import json,itertools
from collections import defaultdict
examples={
 'doubled_T_left':[
 ('upper',['O','R','Q','P']),('upper',['R','A0','A1','Q']),
 ('right',['O','P','D0']),('right',['P','Q','C1','C0','D0']),
 ('lower',['O','P','D1','B1','B0']),('lower',['P','Q','D1'])],
 'refinement_right':[
 ('upper',['O','A0','A1','P']),('upper',['P','A1','R','Q']),
 ('right',['O','P','C0']),('right',['P','Q','C1','C0']),('right',['C1','Q','R','C3','C2']),
 ('lower',['O','P','B1','B0']),('lower',['P','Q','B2','B1']),('lower',['Q','B4','B3','B2']),('lower',['Q','R','B5','B4'])]}
reports=[]
for name,faces in examples.items():
 incidence=defaultdict(list)
 for i,(region,poly) in enumerate(faces):
  for a,b in zip(poly,poly[1:]+poly[:1]):incidence[tuple(sorted((a,b)))].append(i)
 regions=['upper','right','lower']
 masks=[sum(1<<i for i,(r,p) in enumerate(faces) if r==t) for t in regions]
 def compress(x):return sum(((x&m).bit_count()%2)<<j for j,m in enumerate(masks))
 pairs=[];seams=[]
 for edge,fs in incidence.items():
  if len(fs)==2:
   assert faces[fs[0]][0]==faces[fs[1]][0]
   pairs.append(sum(1<<i for i in fs))
  elif len(fs)==3:
   assert set(faces[i][0] for i in fs)==set(regions)
   seams.append((edge,fs))
  else:assert len(fs)==1
 assert len(pairs)==len(faces)-3
 for color,F in [('blue',[0,7]),('red',[0,3,5,6])]:
  g=list(pairs)
  for edge,fs in seams:
   ordered=[next(i for i in fs if faces[i][0]==r) for r in regions]
   for f in F[1:]:g.append(sum((1<<ordered[j]) for j in range(3) if f>>j&1))
  span={0}
  for v in g:span|={x^v for x in list(span)}
  for x in range(1<<len(faces)):
   target=min((compress(x)^f for f in F),key=lambda y:(y.bit_count(),y))
   actual=min((x^v).bit_count() for v in span)
   assert actual==target.bit_count()
  reports.append(dict(example=name,color=color,faces=len(faces),interior_pair_edges=len(pairs),inherited_seams=[e for e,fs in seams],relative_rank=(len(span).bit_length()-1),tested_syndromes=1<<len(faces),exact_cost_preserved=True))
print(json.dumps(reports,indent=2))
