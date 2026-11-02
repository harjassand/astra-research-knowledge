"""Exact local T-book vertex stars, not an exterior-gluing certificate.
Preserve parent-page IDs; identify only declared seam vertices. Edge bases:
blue repetition vector, red star basis anchored at first ordered coface.
Port-incident stars are explicitly artificial boundary completions.
"""
from pathlib import Path
from collections import defaultdict
import importlib.util,json,itertools
ROOT=Path(__file__).resolve().parents[2]/'prerequisites'/'source_fixture'
spec=importlib.util.spec_from_file_location('base',ROOT/'sheaf_incidence_compiler.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
EX=json.loads((ROOT/'example_6_8_polygon_data.json').read_text())
PAGES=['upper','right','lower']
def rank(xs):return len(b.echelon(xs))
def xor_image(coeff,cols):
 out=0
 for j,c in enumerate(cols):
  if coeff>>j&1:out^=c
 return out

def compile_fixture(name,source,chosen,seam_color,port_color):
 seamword=['O','P','Q'] if name=='doubled_T_left' else ['O','P','Q','R']
 seam=set(seamword);seam_edges={tuple(sorted(e)) for e in zip(seamword,seamword[1:])}
 fs=[(region,poly) for region,poly in source if region in chosen]
 polygons=[[v if v in seam else region+':'+v for v in poly] for region,poly in fs]
 faceids=[region+':'+str(j) for j,(region,_) in enumerate(fs)]
 edges=defaultdict(list);vf=defaultdict(set);ve=defaultdict(set)
 for f,poly in enumerate(polygons):
  for v in poly:vf[v].add(f)
  for a,c in zip(poly,poly[1:]+poly[:1]):
   e=tuple(sorted((a,c)));edges[e].append(f);ve[a].add(e);ve[c].add(e)
 edge_data={};D1=[];q_labels=[];port_edges=[];colors={}
 for e,ef in sorted(edges.items()):
  n=len(ef)
  if e in seam_edges:color=seam_color
  elif n==2:color='degree2'
  elif n==1:color=port_color;port_edges.append(e)
  else:raise AssertionError((name,e,ef))
  colors[e]=color
  basis=[(1<<n)-1] if color in ('blue','degree2') else [1|(1<<j) for j in range(1,n)]
  start=len(D1)
  for j,g in enumerate(basis):
   D1.append(sum(1<<ef[k] for k in range(n) if g>>k&1));q_labels.append({'edge':e,'coordinate':j,'basis_face_ids':[faceids[ef[k]] for k in range(n) if g>>k&1]})
  edge_data[e]=(ef,basis,start,b.echelon(basis))
 compiled=b.compile_sheaf(polygons,colors,True)
 assert compiled['D1']==D1
 stars=[];oldcols=[];optcols=[]
 for v,face_set in sorted(vf.items()):
  fids=sorted(face_set);pos={f:j for j,f in enumerate(fids)};constraints=[]
  for e in sorted(ve[v]):
   ef,basis,_,_=edge_data[e]
   for h in b.nullspace(basis,len(ef)):
    constraints.append(sum(1<<pos[ef[j]] for j in range(len(ef)) if h>>j&1))
  kernel=b.nullspace(constraints,len(fids))
  def image(u):
   col=0
   for e in sorted(ve[v]):
    ef,basis,start,solver=edge_data[e]
    restriction=sum(((u>>pos[f])&1)<<j for j,f in enumerate(ef))
    col ^= b.solve(solver,restriction)<<start
   assert xor_image(col,D1)==0
   return col
  canonical=[image(u) for u in kernel];assert rank(canonical)==len(kernel)
  candidates=[(image(xor_image(t,kernel)),xor_image(t,kernel)) for t in range(1,1<<len(kernel))]
  candidates.sort(key=lambda x:(x[0].bit_count(),x[0],x[1]))
  selected=[];selected_u=[]
  for col,u in candidates:
   if rank(selected+[col])>len(selected):selected.append(col);selected_u.append(u)
   if len(selected)==len(kernel):break
  assert rank(selected)==len(kernel)
  assert rank(canonical+selected)==len(kernel)
  oldcols.extend(canonical);optcols.extend(selected)
  localdeg=[sum((col>>j)&1 for col in selected) for j in range(len(D1))]
  olddeg=[sum((col>>j)&1 for col in canonical) for j in range(len(D1))]
  exterior=[e for e in ve[v] if e in port_edges]
  stars.append({'vertex':v,'incident_face_ids':[faceids[f] for f in fids],'incident_edges':sorted(ve[v]),'exterior_port_edges':sorted(exterior),'star_status':'EXTERIOR_TRUNCATED_ARTIFICIAL_BOUNDARY_CLOSURE' if exterior else 'CLOSED_RELATIVE_TO_DECLARED_SELECTED_PAGE_SEAM_INCIDENCE','not_global_gluing_certificate':True,'kernel_dimension':len(kernel),'constraints_local_face_masks':constraints,'kernel_basis_local_face_masks':kernel,'enumerated_nonzero_kernel_vectors':len(candidates),'canonical_X_global_qubit_masks':canonical,'optimized_X_global_qubit_masks':selected,'optimized_local_face_masks':selected_u,'canonical_weights':[x.bit_count() for x in canonical],'optimized_weights':[x.bit_count() for x in selected],'canonical_max_qX_at_this_vertex':max(olddeg,default=0),'optimized_max_qX_at_this_vertex':max(localdeg,default=0),'optimization_objective':'minimum total generator weight and minimum bottleneck weight by weighted linear-matroid greedy; not qX minimization'})
 assert oldcols==compiled['D0'];assert rank(oldcols)==rank(optcols)
 return {'chart':name,'selected_pages':chosen,'seam_color':seam_color,'artificial_exterior_port_color':port_color,'polygons':polygons,'face_ids':faceids,'seam_edges':sorted(seam_edges),'exterior_port_edges':sorted(port_edges),'qubit_labels':q_labels,'D1_face_masks':D1,'C0':len(oldcols),'C1':len(D1),'C2':len(polygons),'k_artificial_closed_patch':compiled['k'],'rank_delta0':rank(oldcols),'canonical_global_max_X_weight':max((c.bit_count() for c in oldcols),default=0),'optimized_global_max_X_weight':max((c.bit_count() for c in optcols),default=0),'canonical_global_max_qX':max((sum((c>>j)&1 for c in oldcols) for j in range(len(D1))),default=0),'optimized_global_max_qX':max((sum((c>>j)&1 for c in optcols) for j in range(len(D1))),default=0),'stars':stars}
reports=[]
for name,source in EX.items():
 for mask in range(1,8):
  chosen=[p for j,p in enumerate(PAGES) if mask>>j&1]
  for seam_color in ['blue','red']:
   for port_color in ['blue','red']:reports.append(compile_fixture(name,source,chosen,seam_color,port_color))
closed=[]
for f in reports:
 if f['artificial_exterior_port_color']!='blue':continue
 for s in f['stars']:
  if not s['exterior_port_edges']:
   twin=next(g for g in reports if g['chart']==f['chart'] and g['selected_pages']==f['selected_pages'] and g['seam_color']==f['seam_color'] and g['artificial_exterior_port_color']=='red')
   ts=next(x for x in twin['stars'] if x['vertex']==s['vertex'])
   # Global qubit indices differ between closures, compare physical basis labels.
   def supports(fix,star,key):return sorted([sorted([str(fix['qubit_labels'][j]) for j in range(fix['C1']) if col>>j&1]) for col in star[key]])
   assert supports(f,s,'canonical_X_global_qubit_masks')==supports(twin,ts,'canonical_X_global_qubit_masks')
   assert s['kernel_dimension']==ts['kernel_dimension'] and sorted(s['optimized_weights'])==sorted(ts['optimized_weights'])
   closed.append({'chart':f['chart'],'selected_pages':f['selected_pages'],'seam_color':f['seam_color'],'vertex':s['vertex'],'kernel_dimension':s['kernel_dimension'],'canonical_weights':s['canonical_weights'],'optimized_weights':s['optimized_weights'],'canonical_qX':s['canonical_max_qX_at_this_vertex'],'optimized_qX':s['optimized_max_qX_at_this_vertex']})
summary={'status':'PASS_LOCAL_ALGEBRA_ONLY','fixture_variants':len(reports),'distinct_page_color_cases':len(reports)//2,'stars_total':sum(len(f['stars']) for f in reports),'closed_local_star_cases':len(closed),'largest_enumerated_kernel_dimension':max(s['kernel_dimension'] for f in reports for s in f['stars']),'closed_max_canonical_weight':max((w for s in closed for w in s['canonical_weights']),default=0),'closed_max_optimized_weight':max((w for s in closed for w in s['optimized_weights']),default=0),'closed_max_optimized_qX_per_vertex':max((s['optimized_qX'] for s in closed),default=0),'artificial_patch_max_canonical_weight':max(f['canonical_global_max_X_weight'] for f in reports),'artificial_patch_max_optimized_weight':max(f['optimized_global_max_X_weight'] for f in reports),'artificial_patch_max_optimized_qX':max(f['optimized_global_max_qX'] for f in reports),'closed_local_stars':closed,'global_family_certified':False}
out=Path(__file__).parent
(out/'t_vertex_star_results.json').write_text(json.dumps(reports,indent=2)+'\n');(out/'t_vertex_star_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='closed_local_stars'},indent=2))
print('All-page closed stars:')
for s in closed:
 if len(s['selected_pages'])==3:print(s)
