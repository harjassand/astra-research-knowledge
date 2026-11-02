"""Exhaust the colored SIMPLE subgraphs of the 6-direction octahedron.
The robust cost bounds every global Par3/Par4 PATH basis simultaneously.
No claim that this overclass covers boxed exceptional stars is made here.
"""
from pathlib import Path
import itertools,json,time
import os
OUT=Path(__file__).parent
MAX_DEGREE=int(os.environ.get('MAX_LINK_DEGREE','4'))
EDGES=[(a,b) for a in range(6) for b in range(a+1,6) if a//2!=b//2]
assert len(EDGES)==12

def nullspace(rows,n):
 d={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in d:x^=d[p]
   else:d[p]=x;break
 out=[]
 for j in range(n):
  if j in d:continue
  x=1<<j
  for p,r in sorted(d.items()):
   if (r&x).bit_count()%2:x^=1<<p
  out.append(x)
 return out

def independent_insert(piv,x):
 while x:
  p=x.bit_length()-1
  if p in piv:x^=piv[p]
  else:piv[p]=x;return True
 return False

start=time.time();cases=0;profile={};maxweight=0;maxdim=0;maxload=0;witness=None;dimwitness=None;loadwitness=None;maxvectors=0
for graphmask in range(1,1<<12):
 es=[e for j,e in enumerate(EDGES) if graphmask>>j&1];n=len(es);inc=[sum(1<<j for j,e in enumerate(es) if v in e) for v in range(6)];degrees=[x.bit_count() for x in inc]
 if max(degrees)>MAX_DEGREE:continue
 # Degree2 Rep and Par coincide, isolated directions have no physical germ.
 variable=[v for v in range(6) if degrees[v] in [1,3,4]]
 for colorpattern in range(1<<len(variable)):
  red=sum(1<<v for j,v in enumerate(variable) if colorpattern>>j&1);rows=[]
  for v,m in enumerate(inc):
   if not m:continue
   if red>>v&1:rows.append(m)
   else:
    first=m&-m;rest=m^first
    while rest:
     a=rest&-rest;rows.append(first|a);rest^=a
  basis=nullspace(rows,n);k=len(basis);vectors=[0]
  for x in basis:vectors += [y^x for y in vectors]
  candidates=[]
  for u in vectors[1:]:
   cost=0
   for v,m in enumerate(inc):
    s=(u&m).bit_count()
    if not s:continue
    if not(red>>v&1) or degrees[v]<=2:cost+=1
    elif degrees[v]==3:assert s==2;cost+=2
    else:assert s in [2,4];cost +=3 if s==2 else 2
   candidates.append((cost,u))
  candidates.sort();piv={};chosen=[];weights=[]
  for wt,u in candidates:
   if independent_insert(piv,u):chosen.append(u);weights.append(wt)
   if len(chosen)==k:break
  assert len(chosen)==k
  load=max((sum(bool(u&m) for u in chosen) for m in inc),default=0)
  w=max(weights,default=0);profile[w]=profile.get(w,0)+1;cases+=1
  record=lambda:{'graphmask':graphmask,'edges':es,'colors':['red' if red>>v&1 else 'blue/degree2' for v in range(6)],'degrees':degrees,'kernel_basis':basis,'selected_basis':chosen,'robust_weights':weights,'dimension':k,'active_generator_count_per_germ':[sum(bool(u&m) for u in chosen) for m in inc]}
  if w>maxweight:maxweight=w;witness=record()
  if k>maxdim:maxdim=k;dimwitness=record()
  if load>maxload:maxload=load;loadwitness=record()
  maxvectors=max(maxvectors,len(candidates))
 if graphmask%512==0:print('graphs',graphmask,'cases',cases,'maxweight',maxweight,'maxdim',maxdim,flush=True)
result={'status':'PASS_FINITE_OVERCLASS_ENUMERATION','geometric_coverage':'CONDITIONAL_ON_SIMPLE_OCTAHEDRAL_LINK_EXTERIOR_THEOREM','tested_graph_mask_range':4095,'maximum_permitted_link_degree':MAX_DEGREE,'colored_cases':cases,'maximum_robust_basis_weight':maxweight,'maximum_kernel_dimension':maxdim,'maximum_selected_active_generator_count_per_germ':maxload,'maximum_enumerated_nonzero_vectors':maxvectors,'weight_profile':profile,'weight_witness':witness,'dimension_witness':dimwitness,'load_witness':loadwitness,'seconds':time.time()-start,'robust_cost':'Rep nonzero1; Par2 nonzero1; Par3 pair<=2; Par4 pair<=3 and four<=2. Bounds all Hamiltonian-path edge bases, without independent endpoint choices.'}
(OUT/('octahedral_link_exhaustion_d'+str(MAX_DEGREE)+'.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
