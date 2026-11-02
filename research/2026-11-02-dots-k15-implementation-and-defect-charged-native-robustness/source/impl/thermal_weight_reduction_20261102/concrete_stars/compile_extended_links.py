"""All path-tree Par4 bases / Par3 anchors, subdivided T endpoints, theta stars,
and all face deletions of those graphs and partial wheels. Abstract link certificates only.
"""
import itertools,json,time
from pathlib import Path
from collections import Counter,defaultdict
from compile_link_vertex_stars import one_family
cases={}
def add(name,edges,colors,status,latent=(),deletions=False):
 masks=range(1,1<<len(edges)) if deletions else [(1<<len(edges))-1]
 for mask in masks:
  es=[e for j,e in enumerate(edges) if mask>>j&1];deg=Counter(v for e in es for v in e);amb=[v for v in latent if deg.get(v)==1]
  for choices in itertools.product(['blue','red'],repeat=len(amb)):
   cc={v:colors[v] for v in deg};cc.update(dict(zip(amb,choices)))
   key=(tuple(sorted(tuple(sorted(e)) for e in es)),tuple(sorted(cc.items())))
   provenance={'family':name,'edge_mask':mask,'latent_boundary_colors':dict(zip(amb,choices))}
   if key in cases:cases[key]['provenance'].append(provenance);continue
   cases[key]={'edges':es,'colors':cc,'status':status,'provenance':[provenance]}
# Core full templates; all path bases now replace the older star+one-path sweep.
ed=[('n'+str(i),'n'+str((i+1)%4)) for i in range(4)];add('C4',ed,{v:'blue' for e in ed for v in e},'COMPLETE_ABSTRACT_CORE')
for k in [2,3]:
 for d in range(1,5):
  ed=[('s'+str(i),'t'+str(j)) for i in range(k) for j in range(d)]
  for old,new in itertools.product(['blue','red'],repeat=2):
   cc={v:(old if v.startswith('s') else new) for e in ed for v in e}
   if k==2:cc.update({v:'blue' for v in cc if v.startswith('t')})
   add(f'K{k}_{d}_{old}_{new}',ed,cc,'COMPLETE_ABSTRACT_CORE; K3d IS NORMALIZED, NOT A RAW OPQ IDENTIFICATION')
# One specified edge subdivided in K3,d; all nonempty face-subcomplex deletions.
for d in range(1,4):
 ed=[('s'+str(i),'t'+str(j)) for i in range(3) for j in range(d)];ed.remove(('s0','t0'));ed += [('s0','u'),('u','t0')]
 for old,new in itertools.product(['blue','red'],repeat=2):
  cc={v:('blue' if v=='u' else old if v.startswith('s') else new) for e in ed for v in e}
  add(f'subdivided_K3_{d}_{old}_{new}',ed,cc,'ONE SUBDIVIDED LINK EDGE; EXTERIOR/TYPE BINDING STILL REQUIRED',latent=['u'],deletions=True)
# Theta graphs: two degree-3 branches, arbitrary inherited/new colors.
for lengths in [(1,2,2),(2,2,2),(1,2,3)]:
 ed=[];latent=[]
 for j,L in enumerate(lengths):
  path=['a']+[f'p{j}_{i}' for i in range(L-1)]+['b'];latent.extend(path[1:-1]);ed.extend(zip(path,path[1:]))
 for ca,cb in itertools.product(['blue','red'],repeat=2):
  cc={v:('blue' if v not in ['a','b'] else ca if v=='a' else cb) for e in ed for v in e}
  add('theta_'+''.join(map(str,lengths))+'_'+ca+'_'+cb,ed,cc,'THETA LINK WITH DEGREE2 INTERIORS; ALL FACE DELETIONS',latent=latent,deletions=True)
# Every spoke subset, every edge deletion; colored degree-one germs retain color.
ring=[('r'+str(i),'r'+str((i+1)%4)) for i in range(4)]
for smask in range(1,16):
 ed=ring+[('c','r'+str(i)) for i in range(4) if smask>>i&1]
 for color in ['blue','red']:
  add(f'partial_wheel_{smask}_{color}',ed,{v:color for e in ed for v in e},'PARTIAL WHEEL AND FACE DELETIONS; COMMON INHERITED/NEW COLOR',deletions=True)
records=[];start=time.monotonic();count=0;max_weight=0;max_qx=0
for ix,case in enumerate(cases.values()):
 f=one_family('extended_'+str(ix),case['edges'],case['colors'],case['status'],basis_mode='all_paths')
 count+=f['anchor_variants'];max_weight=max(max_weight,f['worst_max_weight']);max_qx=max(max_qx,f['max_optimized_qX_per_vertex']);f['provenance']=case['provenance'];f.pop('all_anchor_cases')
 records.append(f)
 if ix%200==0:print('progress',ix,'/',len(cases),'basis_variants',count,'seconds',round(time.monotonic()-start,1),flush=True)
summary={'status':'PASS_ABSTRACT_LINK_ALGEBRA_ONLY','distinct_colored_link_cases':len(records),'basis_variants_checked':count,'max_optimized_X_weight':max_weight,'max_optimized_qX_per_vertex':max_qx,'max_kernel_dimension':max(f['kernel_dimension'] for f in records),'all_12_Par4_path_bases':True,'all_Par3_anchors':True,'all_requested_nonempty_face_deletions':True,'latent_degree1_subdivision_colors_both_enumerated':True,'global_family_type_coverage_certified':False,'runtime_seconds':time.monotonic()-start,'max_weight_examples':[{'id':f['template'],'provenance':f['provenance'][:3],'colors':f['edge_germ_colors'],'edges':f['link_edges'],'kernel_dimension':f['kernel_dimension'],'worst':f['worst']} for f in records if f['worst_max_weight']==max_weight][:8]}
out=Path(__file__).parent;(out/'extended_link_results.json').write_text(json.dumps(records,indent=2)+'\n');(out/'extended_link_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='max_weight_examples'},indent=2))
