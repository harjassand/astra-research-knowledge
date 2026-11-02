"""Complete six genuine doubled-T stars by explicit ordinary sheet-book collars.
Only O,Q,P and the interior rib vertices R,D0,D1 are certified here.
Outer halo boundary choices are artificial and their stars are excluded.
"""
from pathlib import Path
from collections import defaultdict
import importlib.util,itertools,json
BASE=Path(__file__).resolve().parents[2]/'prerequisites'/'source_fixture'
spec=importlib.util.spec_from_file_location('b',BASE/'sheaf_incidence_compiler.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
EX=json.loads((BASE/'example_6_8_polygon_data.json').read_text())['doubled_T_left'];PAGES=['upper','right','lower']
PATHS={'original':{'upper':['O','R','A0'],'right':['O','D0','C0'],'lower':['O','B0']},'copy':{'upper':['Q','A1'],'right':['Q','C1'],'lower':['Q','D1','B1']}}
def rank(xs):return len(b.echelon(xs))
def xor(c,vs):
 y=0
 for j,v in enumerate(vs):
  if c>>j&1:y^=v
 return y

def compile_case(mask,old,new,exterior='blue'):
 pages=[p for j,p in enumerate(PAGES) if mask>>j&1];polys=[];faceids=[];colors={};owned=set();seamverts=['O','P','Q'];safe={'O','P','Q'}
 for p,poly in EX:
  if p in pages:polys.append(poly);faceids.append('cyl:'+p+':'+str(len(faceids)))
 for a,c in [('O','P'),('P','Q')]:colors[tuple(sorted((a,c)))]=old;owned.add(tuple(sorted((a,c))))
 for sheet,paths in PATHS.items():
  root='O' if sheet=='original' else 'Q'
  for sign in ['minus','plus']:
   re=(root,root+'_'+sign);colors[tuple(sorted(re))]=old;owned.add(tuple(sorted(re)))
  for page in pages:
   path=paths[page]
   safe.update(path[1:-1])
   for a,c in zip(path,path[1:]):
    re=tuple(sorted((a,c)));colors[re]=new;owned.add(re)
    for sign in ['minus','plus']:
     aa=root+'_'+sign if a==root else sheet+':'+page+':'+a+'_'+sign
     cc=sheet+':'+page+':'+c+'_'+sign
     polys.append([a,c,cc,aa]);faceids.append('sheet:'+sheet+':'+page+':'+a+c+':'+sign)
 edges=defaultdict(list);vf=defaultdict(set);ve=defaultdict(set)
 for f,poly in enumerate(polys):
  for v in poly:vf[v].add(f)
  for a,c in zip(poly,poly[1:]+poly[:1]):e=tuple(sorted((a,c)));edges[e].append(f);ve[a].add(e);ve[c].add(e)
 for e,fs in edges.items():
  if e not in colors:colors[e]='degree2' if len(fs)==2 else exterior
 for v in safe:
  assert all(len(edges[e])>=2 or e in owned for e in ve[v]),(v,ve[v])
 compiled=b.compile_sheaf(polys,colors,True);D1=compiled['D1'];ed={};offset=0
 for e,fs in sorted(edges.items()):
  d=len(fs);color=colors[e];basis=[(1<<d)-1] if color in ['blue','degree2'] else [1|(1<<j) for j in range(1,d)]
  ed[e]=(fs,basis,offset,b.echelon(basis));offset+=len(basis)
 stars=[]
 for v in sorted(safe):
  fs=sorted(vf[v]);pos={f:j for j,f in enumerate(fs)};constraints=[]
  for e in sorted(ve[v]):
   ef,eb,_,_=ed[e]
   for h in b.nullspace(eb,len(ef)):constraints.append(sum(1<<pos[ef[j]] for j in range(len(ef)) if h>>j&1))
  kernel=b.nullspace(constraints,len(fs))
  def image(u):
   out=0
   for e in sorted(ve[v]):
    ef,eb,off,solver=ed[e];r=sum(((u>>pos[f])&1)<<j for j,f in enumerate(ef));out^=b.solve(solver,r)<<off
   assert xor(out,D1)==0
   return out
  cand=sorted([(image(xor(t,kernel)),xor(t,kernel)) for t in range(1,1<<len(kernel))],key=lambda z:(z[0].bit_count(),z[0],z[1]));opt=[];facevec=[]
  for col,u in cand:
   if rank(opt+[col])>len(opt):opt.append(col);facevec.append(u)
   if len(opt)==len(kernel):break
  linknodes=sorted(ve[v]);lpos={e:j for j,e in enumerate(linknodes)};linkedges=[]
  for f in fs:
   poly=polys[f];j=poly.index(v);e1=tuple(sorted((v,poly[j-1])));e2=tuple(sorted((v,poly[(j+1)%len(poly)])));linkedges.append([lpos[e1],lpos[e2]])
  stars.append({'vertex':v,'complete_star_certified_by_named_sheet_book_collar':True,'physical_incident_edges':linknodes,'link_edges':linkedges,'link_node_colors':[colors[e] for e in linknodes],'face_ids':[faceids[f] for f in fs],'kernel_dimension':len(kernel),'canonical_weights':[image(u).bit_count() for u in kernel],'optimized_weights':[c.bit_count() for c in opt],'optimized_face_masks':facevec,'optimized_qubit_masks':opt,'optimized_qX_per_vertex':max((sum((c>>j)&1 for c in opt) for j in range(len(D1))),default=0)})
 return {'pages':pages,'old_color':old,'new_color':new,'artificial_outer_boundary':exterior,'polygons':polys,'face_ids':faceids,'edge_colors':[{'edge':e,'color':c} for e,c in colors.items()],'safe_vertices':sorted(safe),'D1_face_masks':D1,'stars':stars,'global_recursive_closure_certified':False}
reports=[]
for mask in range(1,8):
 for old,new in itertools.product(['blue','red'],repeat=2):
  r=compile_case(mask,old,new,'blue');t=compile_case(mask,old,new,'red')
  # Off-patch qubit coordinates change, while all certified star physics remains the same.
  for s,u in zip(r['stars'],t['stars']):
   assert s['vertex']==u['vertex'] and s['kernel_dimension']==u['kernel_dimension']
   assert sorted(s['optimized_weights'])==sorted(u['optimized_weights'])
   assert s['link_edges']==u['link_edges'] and s['link_node_colors']==u['link_node_colors']
  reports.append(r)
summary={'status':'PASS_COMPLETE_LOCAL_T_HALOS_NOT_GLOBAL_CLOSURE','page_color_cases':len(reports),'complete_stars':sum(len(r['stars']) for r in reports),'max_optimized_X_weight':max((w for r in reports for s in r['stars'] for w in s['optimized_weights']),default=0),'max_canonical_X_weight':max((w for r in reports for s in r['stars'] for w in s['canonical_weights']),default=0),'max_kernel_dimension':max(s['kernel_dimension'] for r in reports for s in r['stars']),'max_per_vertex_qX':max(s['optimized_qX_per_vertex'] for r in reports for s in r['stars']),'all_page_cases':[{'old':r['old_color'],'new':r['new_color'],'stars':[{k:v for k,v in s.items() if k in ['vertex','kernel_dimension','canonical_weights','optimized_weights','optimized_qX_per_vertex']} for s in r['stars']]} for r in reports if len(r['pages'])==3]}
out=Path(__file__).parent;(out/'complete_t_halo_results.json').write_text(json.dumps(reports,indent=2)+'\n');(out/'complete_t_halo_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
