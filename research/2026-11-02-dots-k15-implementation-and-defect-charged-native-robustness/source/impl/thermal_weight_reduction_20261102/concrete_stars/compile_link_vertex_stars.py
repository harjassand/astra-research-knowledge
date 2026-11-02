"""Compile a complete ABSTRACT vertex link into F_v and fixed-edge-basis X generators.
Coordinate placement / final-family type coverage is not certified here.
Par3/Par4 anchors vary independently; each Par4 also permits the legacy [3,5,12] tree basis. Each basis is fixed during vertex-generator optimization. This is not every GL(3,2) parity basis.
"""
from pathlib import Path
from collections import defaultdict,Counter
import importlib.util,itertools,json
ROOT=Path(__file__).resolve().parents[2]/'prerequisites'/'source_fixture'
spec=importlib.util.spec_from_file_location('base',ROOT/'sheaf_incidence_compiler.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
def rank(xs):return len(b.echelon(xs))
def xor_image(coeff,cols):
 out=0
 for j,c in enumerate(cols):
  if coeff>>j&1:out^=c
 return out

def one_family(name,edges,colors,status,basis_mode="recorded"):
 def anchor_options(v):
  d=len(inc[v])
  if d!=4:return list(range(d))
  if basis_mode=="all_paths":
   return ["path_"+"_".join(str((1<<p[i])|(1<<p[i+1])) for i in range(3)) for p in itertools.permutations(range(4)) if p[0]<p[-1]]
  return list(range(d))+["legacy_tree_3_5_12"]
 nodes=sorted(set(x for e in edges for x in e));inc={v:[j for j,e in enumerate(edges) if v in e] for v in nodes}
 cons=[]
 for v in nodes:
  fs=inc[v]
  if colors[v]=='blue':cons.extend([(1<<fs[0])|(1<<f) for f in fs[1:]])
  else:cons.append(sum(1<<f for f in fs))
 kernel=b.nullspace(cons,len(edges));vectors=[xor_image(t,kernel) for t in range(1,1<<len(kernel))]
 anchor_nodes=[v for v in nodes if colors[v]=='red' and len(inc[v])>=3]
 anchor_sets=[anchor_options(v) for v in anchor_nodes]
 reports=[];profiles=Counter();best=None;worst=None
 for anchors in itertools.product(*anchor_sets):
  amap=dict(zip(anchor_nodes,anchors));ed=[];D1=[];qlabel=[]
  for v in nodes:
   fs=inc[v];d=len(fs);a=amap.get(v,0)
   basis=([int(t) for t in a.split('_')[1:]] if isinstance(a,str) and a.startswith('path_') else ([3,5,12] if a=='legacy_tree_3_5_12' else [((1<<a)|(1<<j)) for j in range(d) if j!=a])) if colors[v]=='red' else [(1<<d)-1]
   start=len(D1);solver=b.echelon(basis);ed.append((fs,basis,start,solver))
   for j,g in enumerate(basis):
    D1.append(sum(1<<fs[k] for k in range(d) if g>>k&1));qlabel.append({'edge_germ':v,'coordinate':j,'support_link_edges':[fs[k] for k in range(d) if g>>k&1]})
  def image(u):
   out=0
   for fs,basis,start,solver in ed:
    res=sum(((u>>f)&1)<<j for j,f in enumerate(fs));out^=b.solve(solver,res)<<start
   assert xor_image(out,D1)==0
   return out
  canonical=[image(u) for u in kernel];cand=sorted([(image(u),u) for u in vectors],key=lambda x:(x[0].bit_count(),x[0],x[1]));selected=[];chosen_u=[]
  for col,u in cand:
   if rank(selected+[col])>len(selected):selected.append(col);chosen_u.append(u)
   if len(selected)==len(kernel):break
  assert rank(selected)==len(kernel) and rank(canonical+selected)==len(kernel)
  weights=tuple(c.bit_count() for c in selected);qX=max((sum((c>>j)&1 for c in selected) for j in range(len(D1))),default=0)
  cw=[c.bit_count() for c in canonical]
  r={'anchors':amap,'optimized_weights':weights,'optimized_qX_per_vertex':qX,'canonical_weights':cw,'optimized_face_masks':chosen_u,'optimized_qubit_masks':selected,'C1_local':len(D1)}
  profiles[weights]+=1;reports.append(r)
  key=(max(weights,default=0),sum(weights),qX,str(anchors))
  if best is None or key<best[0]:best=(key,dict(r,qubit_labels=qlabel,D1_face_masks=D1))
  if worst is None or key>worst[0]:worst=(key,dict(r,qubit_labels=qlabel,D1_face_masks=D1))
 return {'template':name,'status':status,'link_nodes':nodes,'link_edges':edges,'edge_germ_colors':colors,'kernel_dimension':len(kernel),'kernel_face_masks':kernel,'enumerated_nonzero_kernel_vectors':len(vectors),'anchor_variants':len(reports),'best_max_weight':best[0][0],'worst_max_weight':worst[0][0],'min_optimized_qX_per_vertex':min(r['optimized_qX_per_vertex'] for r in reports),'max_optimized_qX_per_vertex':max(r['optimized_qX_per_vertex'] for r in reports),'optimized_weight_profiles':[{'weights':list(k),'count':v} for k,v in sorted(profiles.items())],'best':best[1],'worst':worst[1],'all_anchor_cases':reports,'global_family_type_coverage_certified':False}

if __name__=="__main__":
 families=[]
 edges=[('n'+str(i),'n'+str((i+1)%4)) for i in range(4)]
 families.append(one_family('ordinary_face_C4',edges,{v:'blue' for e in edges for v in e},'COMPLETE_ABSTRACT_ORDINARY_FACE_LINK'))
 for d in [1,2,3,4]:
  edges=[('s'+str(i),'t'+str(j)) for i in range(2) for j in range(d)]
  for old in ['blue','red']:
   colors={v:old if v.startswith('s') else 'blue' for e in edges for v in e}
   families.append(one_family('ordinary_edge_K2_'+str(d)+'_'+old,edges,colors,'COMPLETE_ABSTRACT_EDGE_SUBDIVISION_LINK; DEGREE4_CASE_REQUIRES_BINDING_TO_RESOLUTION_IN_FINAL_FAMILY'))
 for d in [1,2,3,4]:
  edges=[('s'+str(i),'t'+str(j)) for i in range(3) for j in range(d)]
  for old,new in itertools.product(['blue','red'],repeat=2):
   colors={v:old if v.startswith('s') else new for e in edges for v in e}
   families.append(one_family('normalized_T_K3_'+str(d)+'_'+old+'_'+new,edges,colors,'COMPLETE_ABSTRACT_NORMALIZED_ATTACHING_ENDPOINT; NOT_IDENTIFIED_WITH_RAW_OPQ_SUBDIVISION_STAR'))
 edges=[('r'+str(i),'r'+str((i+1)%4)) for i in range(4)]+[('c','r'+str(i)) for i in range(4)]
 for new in ['blue','red']:
  families.append(one_family('glued_cross_W5_'+new,edges,{v:new for e in edges for v in e},'COMPLETE_ABSTRACT_WHEEL_ATTACHING_ENDPOINT; PHYSICAL_FAMILY_TYPE_BINDING_PENDING'))
 summary={'status':'PASS_LOCAL_LINK_ALGEBRA_ONLY','template_color_families':len(families),'anchor_variants_total':sum(f['anchor_variants'] for f in families),'max_kernel_dimension':max(f['kernel_dimension'] for f in families),'best_anchor_worst_template_weight':max(f['best_max_weight'] for f in families),'all_anchor_worst_template_weight':max(f['worst_max_weight'] for f in families),'families':[{k:v for k,v in f.items() if k in ['template','status','kernel_dimension','anchor_variants','best_max_weight','worst_max_weight','min_optimized_qX_per_vertex','max_optimized_qX_per_vertex','optimized_weight_profiles']} for f in families],'global_family_type_coverage_certified':False}
 out=Path(__file__).parent;(out/'link_vertex_star_results.json').write_text(json.dumps(families,indent=2)+'\n');(out/'link_vertex_star_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='families'},indent=2))
 for f in summary['families']:print(f['template'],'dim',f['kernel_dimension'],'anchors',f['anchor_variants'],'weight',f['best_max_weight'],f['worst_max_weight'],'qX',f['min_optimized_qX_per_vertex'],f['max_optimized_qX_per_vertex'])
