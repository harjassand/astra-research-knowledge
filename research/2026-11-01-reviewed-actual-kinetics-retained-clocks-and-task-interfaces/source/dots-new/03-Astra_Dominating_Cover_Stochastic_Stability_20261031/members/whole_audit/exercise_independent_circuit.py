"""Separate circuit implementation versus small exhaustive comparators only.
Production paths are tested with all exhaustive constructors disabled.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations,product,permutations
import os,sys,json,time,hashlib,importlib.util,copy
import independent_cover_receiver as S
import independent_circuit_receiver as I
START=time.perf_counter();HERE=Path(__file__).resolve().parent
SOURCE=Path(os.environ.get('CIRCUIT_SOURCE_DIR',str(HERE.parent if (HERE.parent/'cover_circuit.py').exists() else HERE.parent/'stochastic_cover_circuit_pending_20261031')))
OUT=Path(os.environ.get('AUDIT_OUTPUT_DIR',str(HERE)));OUT.mkdir(parents=True,exist_ok=True)
s=importlib.util.spec_from_file_location('circuit_under_test',SOURCE/'cover_circuit.py');C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
COUNT=dict(graphs=0,admitted_graphs=0,capacity_states=0,minimal_witnesses=0,active_edge_queries=0,large_binary_states=0,scaled_drift_checks=0,semantic_mutations=0,permutations=0,numeric_permutations=0,disabled_exhaustive_path_calls=0,budget_receipts=0,domain_refusals=0,structural_unknowns=0)
for m in range(2,6):
 vs=tuple(range(1,m+1));possible=list(combinations(vs,2))
 for mask in range(1,1<<len(possible)):
  edges=tuple(e for j,e in enumerate(possible) if mask>>j&1);rec=dict(satellites=vs,edges=edges);cv=S.minimal_covers(rec);es=set(edges)
  good=all(any(tuple(sorted((w,z))) in es for z in (u,v)) for cover in cv for u,v in edges if u in cover and v in cover for w in vs if w not in cover)
  COUNT['graphs']+=1
  if not good:continue
  COUNT['admitted_graphs']+=1;cc=C.compile_inventory(rec);ic=I.compile_inventory(rec);assert S.canonical(cc)==S.canonical(ic)
  for xx in product(range(3),repeat=m):
   x=(0,)+xx;weights=[sum(x[v] for v in cover) for cover in cv];tau=min(weights);opts=[cover for cover,w in zip(cv,weights) if w==tau]
   assert C.cover_weight(cc,x)==I.cover_weight(ic,x)==tau
   witness=I.optimal_minimal_cover(ic,x);assert witness in cv and sum(x[v] for v in witness)==tau
   expected=tuple((u,v) for u,v in edges if x[u]>0 and x[v]>0 and any(u in cover and v in cover for cover in opts))
   assert I.bad_active_edges(ic,x)==C.bad_active_edges(cc,x)==expected
   COUNT['capacity_states']+=1;COUNT['minimal_witnesses']+=1;COUNT['active_edge_queries']+=sum(x[u]>0 and x[v]>0 for u,v in edges)
  x=(0,)+tuple(0 if i%3==0 else 10**200+i for i in vs);assert I.cover_weight(ic,x)==C.cover_weight(cc,x)==min(sum(x[v] for v in cover) for cover in cv);COUNT['large_binary_states']+=1

def fixture(m=4,large=False):
 n=m+1;a=0
 def vec(*ix):return tuple(ix.count(i) for i in range(n))
 edges=[(1,2),(2,3),(3,4)] if not large else [(i,i+1) for i in range(1,m+1,2)]
 hubs=[vec(*e) for e in edges];E=len(edges)
 raw=[(vec(),vec(0),Q(1) if not large else Q(1,100)),(vec(0),vec(),Q(1))]
 for h in hubs:raw.extend([(vec(0,0),h,Q(1) if not large else Q(1,E)),(h,vec(0,0),Q(1) if not large else Q(16*E))])
 for off,x in enumerate(range(1,n)):
  h=hubs[(1 if off==3 else off%3)] if not large else hubs[off%E]
  raw.extend([(vec(0,x),h,Q(1) if not large else Q(1,m)),(h,vec(0,x),Q(2) if not large and x==4 else Q(1))])
 return raw
raw=fixture();t=Q(2);old=S.numerical(raw,t);new=C.numerical(raw,t);ind=I.numerical(raw,t)
assert S.canonical(ind)==C.canonical(new) and I.receive_qualitative(raw,C.qualitative(raw))
for field in ['constants','profile_head','Foster','stationary_moment']:assert old[field]==new[field]

# Independent production cannot silently invoke even this audit's exhaustive receiver.
def prohibited(*args,**kwargs):raise AssertionError('exhaustive fallback called')
saved=[(C.B,'covers',C.B.covers),(C.B,'numerical',C.B.numerical),(S,'minimal_covers',S.minimal_covers),(S,'numerical',S.numerical)]
for module,name,fn in saved:setattr(module,name,prohibited)
try:
 assert S.canonical(I.numerical(raw,t))==C.canonical(C.numerical(raw,t));COUNT['disabled_exhaustive_path_calls']+=2
 rec=S.parse(raw);mass=new['constants']['Nstar']
 for x in list(product(range(3),repeat=5))+[(0,1,1,0,10**30),(0,10**30,1,1,10**30),(1,0,0,0,10**30),(0,mass,mass,mass,mass)]:
  drift=I.scaled_drift(rec,ind,x);assert drift==C.scaled_drift(rec,new,x)
  if sum(x)>=mass:
   tau=I.cover_weight(ind['inventory'],x);r=x[0]+tau;g=ind['profile_head'][r] if r<ind['constants']['K'] else 1+ind['constants']['c']/r
   h=g+ind['constants']['q']*Q(x[0],(sum(x)+1)*(r+1)**2)-ind['constants']['epsilon']*Q(x[0],sum(x)+1)
   assert drift<=-ind['constants']['zeta']*h
  COUNT['scaled_drift_checks']+=1
 # 24 satellites: the old 2^m mask budget is exceeded, but neither production receiver enumerates covers.
 large=fixture(24,True);lc=C.numerical(large,Q(3,2));li=I.numerical(large,Q(3,2));assert S.canonical(lc)==S.canonical(li)
 assert lc['work']['cover_masks_enumerated']==0;COUNT['disabled_exhaustive_path_calls']+=2
 lr=S.parse(large);N=lc['constants']['Nstar'];targets=[]
 for A in [0,1,2,N]:
  x=[0]*25;x[0]=A;x[1]=N;targets.append(tuple(x))
 targets.append((0,)+tuple(N for _ in range(24)))
 for x in targets:assert I.scaled_drift(lr,li,x)==C.scaled_drift(lr,lc,x);COUNT['scaled_drift_checks']+=1
 large_result=dict(satellites=24,avoided_cover_masks=1<<24,profile_steps=lc['work']['profile_steps'],circuit_work=lc['inventory']['work'],wire_bytes=len(S.canonical(li).encode()),retained_scalar_bits=li['work']['retained_scalar_bits'])
 for tt,limit in [(Q(2),0),(1+Q(1,10**200),1000),(Q(10**100),1000)]:
  got=C.numerical(raw,tt,max_profile_steps=limit);assert got['status']=='UNKNOWN_NUMERICAL_BUDGET' and I.receive_numerical(raw,tt,got,max_profile_steps=limit);COUNT['budget_receipts']+=1
finally:
 for module,name,fn in saved:setattr(module,name,fn)
oldrefusal=S.numerical(large,Q(3,2));assert oldrefusal['status']=='UNKNOWN_NUMERICAL_BUDGET' and oldrefusal['required_cover_masks']==1<<24

for index,p in enumerate(permutations(range(5))):
 rr=[(tuple(u[j] for j in p),tuple(v[j] for j in p),k) for u,v,k in raw];assert I.receive_qualitative(rr,C.qualitative(rr));COUNT['permutations']+=1
 if index in [0,23,73,119]:
  cert=C.numerical(rr,t);assert I.receive_numerical(rr,t,cert) and cert['constants']==new['constants'];COUNT['numeric_permutations']+=1
for key in ['inventory','constants','profile_head','Foster','stationary_moment','work','qualitative','t','family','raw_sha256','cost_scope']:
 forged=copy.deepcopy(new);forged[key]=None;assert not I.receive_numerical(raw,t,forged);COUNT['semantic_mutations']+=1
# Deep circuit corruptions, including zero-weight witness-relevant shores and charged graph work.
for mutate in range(4):
 forged=copy.deepcopy(new)
 if mutate==0:forged['inventory']['edges']=()
 elif mutate==1:forged['inventory']['anchors']=()
 elif mutate==2:forged['inventory']['work']['component_neighbor_tests']+=1
 else:forged['inventory']['formula']+='!'
 assert not I.receive_numerical(raw,t,forged);COUNT['semantic_mutations']+=1

# Explicit circuit-interface refusals and UNKNOWN tampering, independently received.
def refuse(fn):
 try:fn()
 except (ValueError,TypeError):COUNT['domain_refusals']+=1;return
 raise AssertionError('invalid circuit domain accepted')
for val in [True,False,2.0,'2',0,1,-1,None]:
 for module in [C,I]:refuse(lambda module=module,val=val:module.numerical(raw,val))
for val in [True,False,1.0,Q(1),-1,None]:
 for module in [C,I]:refuse(lambda module=module,val=val:module.numerical(raw,t,max_profile_steps=val))
for val in [True,1.0,'1',0,-1,None]:
 rr=list(raw);u,v,k=rr[0];rr[0]=(u,v,val)
 for module in [C,I]:refuse(lambda module=module,rr=rr:module.qualitative(rr))
aa=(2,0,0,0,0);hub=(0,1,1,0,0);arm=(1,1,0,0,0)
negatives=[raw[:-1],[row for row in raw if (row[0],row[1]) not in [(aa,hub),(hub,aa)]],raw+[(aa,arm,1),(arm,aa,1)]]
for vertices,edges in [(5,[(1,2),(1,3),(2,3)]),(6,[(1,2),(2,3),(3,4)])]:
 def v(*ix):return tuple(ix.count(i) for i in range(vertices))
 rr=[(v(),v(0),Q(1)),(v(0),v(),Q(1))];hs=[v(*e) for e in edges]
 for h in hs:rr.extend([(v(0,0),h,Q(1)),(h,v(0,0),Q(1))])
 for x in range(1,vertices):rr.extend([(v(0,x),hs[0],Q(1)),(hs[0],v(0,x),Q(1))])
 negatives.append(rr)
for rr in negatives:
 got=C.qualitative(rr);assert got['status']=='UNKNOWN' and I.receive_qualitative(rr,got);COUNT['structural_unknowns']+=1
 forged=dict(got,stability='CERTIFIED');assert not I.receive_qualitative(rr,forged);COUNT['semantic_mutations']+=1

RESULT=dict(status='PASS',scope='Fresh independently implemented polynomial inventory circuit and whole semantic receiver; exhaustive comparators only on graphs with at most five satellites',counts=COUNT,large_no_enumeration_control=large_result,seconds=time.perf_counter()-START,source_sha256=hashlib.sha256((SOURCE/'cover_circuit.py').read_bytes()).hexdigest(),receiver_sha256=hashlib.sha256((HERE/'independent_circuit_receiver.py').read_bytes()).hexdigest(),no_simulation=True,no_expanded_power=True,no_exception_enumeration=True,no_complete_numerical_polynomial_claim=True)
(OUT/'INDEPENDENT_CIRCUIT_RESULTS.json').write_text(json.dumps(S.wire(RESULT),indent=2)+'\n');print(json.dumps(S.wire(RESULT),indent=2))
