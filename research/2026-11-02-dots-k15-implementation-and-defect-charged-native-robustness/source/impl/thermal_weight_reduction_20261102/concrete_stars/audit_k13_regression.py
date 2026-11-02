"""Independent arithmetic/algebra check of K13 local capacity and Clifford identities.
Does not infer a geometric collar from a rank calculation.
"""
from pathlib import Path
import itertools,json,hashlib
ROOT=Path(__file__).resolve().parent
records=json.loads((ROOT/'boxed_link_geometry_results.json').read_text())['records']
def rank(rows):
 piv={}
 for x in rows:
  for p in sorted(piv,reverse=True):
   if x>>p&1:x^=piv[p]
  if x:piv[x.bit_length()-1]=x
 return len(piv)
summary={};checks=0
for r in records:
 es=r['link_edges'];ns=sorted(set(v for e in es for v in e));inc={v:[j for j,e in enumerate(es) if v in e] for v in ns};rows=[];Q=0
 for e in es:assert len(e)==2 and e[0]!=e[1]
 for v,ids in inc.items():
  c=r['node_colors'].get(v,'degree2');d=len(ids)
  if c in ('blue','degree2'):
   rows += [(1<<ids[0])^(1<<j) for j in ids[1:]];Q+=1
  else:rows.append(sum(1<<j for j in ids));Q+=d-1
 dim=len(es)-rank(rows)
 assert dim==r['rank'] and Q==r['number_qubits_incident']
 assert 2*dim<=Q and Q<=13
 assert rank(r['face_basis_vectors'])==dim
 assert all(not ((a&h).bit_count()%2) for a in r['face_basis_vectors'] for h in rows)
 s=summary.setdefault(r['chart'],{'count':0,'max_Q':0,'max_rank':0});s['count']+=1;s['max_Q']=max(s['max_Q'],Q);s['max_rank']=max(s['max_rank'],dim);checks+=1
# Exact integer-position inventories against open boxes.
left={'O':(0,0,0),'P':(1,0,0),'Q':(1,0,1),'R':(0,0,1),'D0':(1,0,0),'D1':(1,0,0),'A0':(0,0,2),'A1':(1,0,2),'B0':(0,0,-1),'B1':(1,0,-1),'C0':(2,0,0),'C1':(2,0,1)}
right={'O':(0,0,0),'P':(1,0,0),'Q':(2,0,0),'R':(2,0,1),'A0':(0,0,1),'A1':(1,0,1),'C0':(1,0,0),'C1':(2,0,0),'C2':(3,0,0),'C3':(3,0,1),'B0':(0,0,-1),'B1':(1,0,-1),'B2':(2,0,-1),'B3':(2,1,-1),'B4':(2,1,0),'B5':(2,1,1)}
def inside7(p,hi):return all(-2<7*x<h for x,h in zip(p,hi))
li=sorted(v for v,p in left.items() if inside7(p,[9,2,9]));ri=sorted(v for v,p in right.items() if inside7(p,[16,2,2]))
assert li==['D0','D1','O','P','Q','R'] and ri==['C0','C1','O','P','Q']
# All possible local binary linear Clifford frames on k<=3 qubits.
def ap(cols,x):
 y=0
 for j,c in enumerate(cols):
  if x>>j&1:y^=c
 return y
nmat=0;identities=0
for k in range(1,4):
 for cols in itertools.product(range(1<<k),repeat=k):
  if rank(cols)!=k:continue
  inv=[next(x for x in range(1<<k) if ap(cols,x)==1<<j) for j in range(k)]
  invT=[sum(((inv[i]>>j)&1)<<i for i in range(k)) for j in range(k)]
  nmat+=1
  for u,v,x in itertools.product(range(1<<k),repeat=3):
   # U_A X(u) U_A† on |x>; U_A Z(v) U_A† phase on |x>.
   assert ap(cols,ap(inv,x)^u)==(x^ap(cols,u))
   assert (v&ap(inv,x)).bit_count()%2==(ap(invT,v)&x).bit_count()%2
   identities+=2
# All 12 Hamiltonian paths on four labels have per-face incidence <=2.
pathcounts={}
for d in range(1,5):
 paths=[p for p in itertools.permutations(range(d)) if d==1 or p[0]<p[-1]]
 for p in paths:
  cs=[(1<<p[j])|(1<<p[j+1]) for j in range(d-1)]
  assert rank(cs)==d-1
  assert all(sum((c>>i)&1 for c in cs)<=2 for i in range(d))
 pathcounts[d]=len(paths)
result={'status':'PASS_ALGEBRA_AND_LISTED_COORDINATES','boxed_cases':checks,'boxed_summary':summary,'doubled_box_named_vertices':li,'recursive_box_named_vertices':ri,'R_B4_recursive_outside':True,'invertible_Clifford_frames_checked':nmat,'Pauli_action_identities':identities,'path_counts':pathcounts,'source_vertex_basis_unchanged':True,'cold_overhead_from_basis_conjugation':0,'optional_path_frame_K':13,'governing_untouched_K':15,'governing_overlap_bound':196,'qX_bound':12,'qZ_bound':4,'overlap_bound':1+13*(12+4-1),'historical_optional_to_K180_peak_ratio':(13/180)**3,'optional_to_untouched_peak_ratio':(13/15)**3,'untouched_to_historical_peak_ratio':(15/180)**3,'scope':'Geometry coverage still uses the declared atlas and admitted source box/edge closure; tests do not create missing collars.'}
(ROOT/'audit_k13_regression.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
