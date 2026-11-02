#!/usr/bin/env python3
"""Exact links of vertices INSIDE the declared T/glued/free boxes.
Uses source Example 6.8 polygons and only the ordinary sheet collars specified
by the doubled-T/rib interpretation. This is not a global coordinate generator.
Robust cost upper-bounds every choice of physical basis in each edge stalk.
"""
from pathlib import Path
from collections import defaultdict
import json,itertools
ROOT=Path(__file__).resolve().parent
DATA=Path(__file__).resolve().parents[2]/'prerequisites'/'source_fixture'/'example_6_8_polygon_data.json'
examples=json.loads(DATA.read_text())
COLORS=('blue','red')
def rank(cols):
 piv={}
 for a in cols:
  while a:
   b=a.bit_length()-1
   if b in piv:a^=piv[b]
   else:piv[b]=a;break
 return len(piv)
def kernel(rows,n):
 return [a for a in range(1<<n) if all((a&r).bit_count()%2==0 for r in rows)]
def calculate(edges,colors):
 nodes=sorted(set(sum(([a,b] for a,b in edges),[])))
 inc={v:[i for i,e in enumerate(edges) if v in e] for v in nodes}
 rows=[]
 for v,ids in inc.items():
  c=colors.get(v,'degree2' if len(ids)==2 else None)
  if c is None:raise ValueError((v,len(ids),edges,colors))
  if c in ('blue','degree2'):
   rows += [(1<<ids[0])|(1<<i) for i in ids[1:]]
  elif c=='red':rows.append(sum(1<<i for i in ids))
  else:raise ValueError(c)
 C=kernel(rows,len(edges));dim=(len(C)).bit_length()-1
 def cost(a):
  total=0
  for v,ids in inc.items():
   active=sum((a>>j)&1 for j in ids)
   if not active:continue
   c=colors.get(v,'degree2')
   if c in ('blue','degree2'):total+=1
   else:total+=len(ids)-1 # arbitrary GL basis upper bound (safe even Par4)
  return total
 chosen=[]
 for a in sorted(C[1:],key=lambda a:(cost(a),a)):
  if rank(chosen+[a])>len(chosen):chosen.append(a)
  if len(chosen)==dim:break
 assert len(chosen)==dim
 return {'link_nodes':nodes,'link_edges':edges,'node_face_degrees':{v:len(inc[v]) for v in nodes},'node_colors':colors,'rank':dim,'robust_generator_costs':[cost(a) for a in chosen],'max_robust_weight':max([cost(a) for a in chosen],default=0),'face_basis_vectors':chosen,'number_qubits_incident':sum((1 if colors.get(v,'degree2') in ('blue','degree2') else len(ids)-1) for v,ids in inc.items())}
def t_link(chart,pages,v,old,new):
 faces=[(p,poly) for p,poly in examples[chart] if p in pages]
 edges=[]
 for p,poly in faces:
  if v in poly:
   j=poly.index(v);edges.append((poly[(j-1)%len(poly)],poly[(j+1)%len(poly)]))
 # Germ labels are neighboring abstract vertex IDs; auxiliary +/- are sheet-side germs.
 colors={}
 if chart=='doubled_T_left':
  seam=['O','P','Q'];original={'upper':['O','R','A0'],'right':['O','D0','C0'],'lower':['O','B0']};copy={'upper':['Q','A1'],'right':['Q','C1'],'lower':['Q','D1','B1']}
 else:
  seam=['O','P','Q','R'];original={'upper':['O','A0'],'right':['O','C0','C1','C2'],'lower':['O','B0']};copy={}
 for sv in seam:
  if sv==v:
   j=seam.index(v)
   for k in [j-1,j+1]:
    if 0<=k<len(seam):colors[seam[k]]=old
 for side,paths in [('s',original),('t',copy)]:
  for p,path in paths.items():
   if p not in pages or v not in path:continue
   j=path.index(v)
   nbrs=[path[k] for k in [j-1,j+1] if 0<=k<len(path)]
   # At O/Q original sheet book center, the two seam germs are shared by all pages.
   rays=[side+'-',side+'+'] if j==0 else [side+'-'+p,side+'+'+p]
   for u in nbrs:
    colors[u]=new
    for a in rays:edges.append((u,a))
   for a in rays:colors[a]=old if j==0 else 'degree2'
 # Other partial-polygon nodes are genuine degree2 internal edges.
 inc=defaultdict(int)
 for a,b in edges:inc[a]+=1;inc[b]+=1
 for n,d in inc.items():
  if n not in colors:
   assert d==2,(chart,pages,v,n,d)
   colors[n]='degree2'
 return calculate(edges,colors)
records=[]
for chart in examples:
 for pages_tuple in itertools.chain.from_iterable(itertools.combinations(['upper','right','lower'],k) for k in range(1,4)):
  pages=set(pages_tuple)
  vs=['O','P','Q']
  if chart=='doubled_T_left':vs += [v for p,v in [('upper','R'),('right','D0'),('lower','D1')] if p in pages]
  else:vs += ['C0','C1'] if 'right' in pages else []
  for old,new in itertools.product(COLORS,repeat=2):
   for v in vs:
    rec=t_link(chart,pages,v,old,new);rec.update(chart=chart,pages=pages_tuple,vertex=v,old_color=old,new_color=new);records.append(rec)
# Glued cross: wheel endpoint with C4 + central spoke germ. Both endpoint stars identical.
for c in COLORS:
 ed=[(str(i),str((i+1)%4)) for i in range(4)]+[('v',str(i)) for i in range(4)]
 rec=calculate(ed,{n:c for n in ['0','1','2','3','v']});rec.update(chart='glued_cross_box',vertex='O_or_P',new_color=c);records.append(rec)
# Free cross: each abstract copy is a single straight rib attachment, K_{2,3}.
for c in COLORS:
 ed=[(a,b) for a in ['r-','r+'] for b in ['sheet-','sheet+','band']]
 rec=calculate(ed,{'r-':c,'r+':c,'sheet-':'degree2','sheet+':'degree2','band':'degree2'});rec.update(chart='free_cross_box',vertex='each_independent_attachment',new_color=c);records.append(rec)
summary={}
for name in ['doubled_T_left','refinement_right','glued_cross_box','free_cross_box']:
 rs=[r for r in records if r['chart']==name]
 summary[name]={'cases':len(rs),'maximum_robust_X_weight':max(r['max_robust_weight'] for r in rs),'maximum_stalk_rank':max(r['rank'] for r in rs),'maximum_incident_qubits':max(r['number_qubits_incident'] for r in rs),'vertices':sorted(set(r['vertex'] for r in rs))}
out={'scope':'Inside-box stars only, with literal source polygon IDs and declared ordinary sheet collars; robust to every edge-stalk basis','cases':len(records),'summary':summary,'records':records}
(ROOT/'boxed_link_geometry_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'cases':len(records),'summary':summary},indent=2))
