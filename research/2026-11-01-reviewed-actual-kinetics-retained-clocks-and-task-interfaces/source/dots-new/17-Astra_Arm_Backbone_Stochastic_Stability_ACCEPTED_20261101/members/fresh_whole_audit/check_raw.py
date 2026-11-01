from itertools import combinations,permutations
from fractions import Fraction as F
from copy import deepcopy
from pathlib import Path
import sys,os,json
import independent_backbone as I
from fixtures import raw_graph,production
sys.path.insert(0,os.environ.get('BACKBONE_SOURCE_DIR','producer-workspace/stochastic_arm_backbone_recovery_20261101'));import arm_backbone as A
counts={};hit=lambda k,n=1:counts.__setitem__(k,counts.get(k,0)+n)
def guard(vertices,edges):
 adj={v:{w for e in edges if v in e for w in e if v!=w}for v in vertices};covers=[]
 for mask in range(1<<len(vertices)):
  s={v for i,v in enumerate(vertices)if mask>>i&1};hit('test_only_cover_masks')
  if all(u in s or v in s for u,v in edges)and not any(all(u in s-{v}or w in s-{v}for u,w in edges)for v in s):covers.append(s)
 return all(w in adj[u]or w in adj[v]for s in covers for u,v in edges if u in s and v in s for w in set(vertices)-s)
for m in range(2,6):
 edges=list(combinations(range(1,m+1),2))
 for mask in range(1,1<<len(edges)):
  armed=[e for i,e in enumerate(edges)if mask>>i&1];unused=[e for e in edges if e not in armed];used=sorted({v for e in armed for v in e});ok=guard(used,armed)
  for aux in {(),tuple(unused),tuple(unused[::2])}:
   raw=raw_graph(m,armed,list(aux));iq=I.qualitative(raw);aq=A.qualitative(raw);assert(iq['status']!='UNKNOWN')==ok==(aq['status']!='UNKNOWN');hit('raw_decompositions');hit('accepted'if ok else'UNKNOWN')
   if ok:
    r=I.parse(raw);ar=A.recognize(raw);assert r['edges']==ar['edges']and r['free']==ar['free']and r['auxiliary']==ar['auxiliary'];hit('complete_raw_splits')
armed=[(1,2),(2,3),(3,4),(5,6)];aux=[e for e in combinations(range(1,7),2)if e not in armed];assert I.qualitative(raw_graph(6,armed,aux))['status']=='UNKNOWN';hit('P4_edge_UNKNOWN')
armed=[(1,2),(1,3),(2,3),(4,5)];aux=[e for e in combinations(range(1,6),2)if e not in armed];raw=raw_graph(5,armed,aux);assert I.qualitative(raw)['status']=='UNKNOWN'and A.G.C.B.qualitative(raw)['status']=='CERTIFIED_QUALITATIVE';assert all(k==1 for u,v,k in raw);hit('old_route_and_detailed_balance_win')
raw=A.fixture();c=I.construct(raw,2);r=I.parse(raw)
for perm in list(permutations(range(6)))[:120]:
 rr=[(tuple(u[i]for i in perm),tuple(v[i]for i in perm),k)for u,v,k in raw];assert I.canonical(I.qualitative(rr))==I.canonical(A.qualitative(rr));hit('permutations')
rr=[(u,v,k/3)for u,v,k in reversed(raw)]+[(u,v,2*k/3)for u,v,k in reversed(raw)];assert I.canonical(I.construct(rr,2))==I.canonical(c);hit('duplicate_normalization')
for cap in (0,c['plan']['core_profile_steps']-1,c['plan']['core_profile_steps']):assert I.canonical(I.construct(raw,2,cap))==I.canonical(A.construct(raw,2,cap));hit('loop_budget_boundaries')
for bad in (True,2.0,'2',1,0,-1,None):
 try:I.construct(raw,bad)
 except(ValueError,TypeError):hit('domain_refusals')
 else:raise AssertionError('bad t')
for bad in (True,1.0,'1',-1,None):
 try:I.construct(raw,2,bad)
 except(ValueError,TypeError):hit('domain_refusals')
 else:raise AssertionError('bad budget')
for bad in (True,1.0,'1',0,-1,None):
 rr=deepcopy(raw);u,v,k=rr[0];rr[0]=u,v,bad
 try:I.qualitative(rr)
 except(ValueError,TypeError):hit('domain_refusals')
 else:raise AssertionError('bad rate')
for bad in (True,1.0,'1',F(1),-1,None):
 rr=deepcopy(raw);u,v,k=rr[0];u=list(u);u[1]=bad;rr[0]=u,v,k
 try:I.qualitative(rr)
 except(ValueError,TypeError):hit('domain_refusals')
 else:raise AssertionError('bad count')
# Production does not call old acceptance or exhaustive/numerical paths.
prod=production();expected=A.construct(prod,2)
def forbidden(*a,**k):raise AssertionError('unpaid/old/candidate dependency')
targets=[(I.I,n,getattr(I.I,n))for n in('parse','construct','qualitative')]+[(I.P,n,getattr(I.P,n))for n in('parse','construct','qualitative')]+[(I.P.B,n,getattr(I.P.B,n))for n in('minimal_covers','numerical')]+[(I.P.C,'numerical',I.P.C.numerical)]+[(A,n,getattr(A,n))for n in('recognize','construct','qualitative','plan')]
for mod,n,fn in targets:setattr(mod,n,forbidden)
pc=I.construct(prod,2);assert I.canonical(pc)==I.canonical(expected)
for mod,n,fn in targets:setattr(mod,n,fn)
pr=I.parse(prod);assert len(pr['free'])==24 and len(pr['auxiliary'])==133 and len(pr['channels'])==322
assert len(I.canonical(pc).encode())==150663 and I.digest(pc)=='181979210f47b93a7d8b8e21a2b726ae0f5161360ae2a5b8397901df61619442';hit('production_no_old_or_exhaustive_dependency')
# Extra dense-armed independent fixture genuinely costs more than default cap.
extra=raw_graph(6,[(1,2),(2,3),(3,4)],[(1,3),(1,5),(5,6)],True,True);q=I.construct(extra,2)
assert q['status']=='UNKNOWN_CORE_PROFILE_BUDGET'and q['qualitative']['status']!='UNKNOWN';hit('dense_fixture_honest_default_UNKNOWN')
res=dict(status='PASS_FRESH_INDEPENDENT_RAW_AND_PRODUCTION',counts=counts,production=dict(canonical_bytes=len(I.canonical(pc).encode()),canonical_sha256=I.digest(pc),steps=pc['plan']['core_profile_steps'],work=pc['work'],old_acceptance_and_exhaustive_entrypoints_disabled=len(targets)),dense_fixture_default_required_steps=q['required_core_steps'],scope='Direct minimal-cover guard and enumeration are test-only. Higher-cost custom components explicitly run with 300000 core-loop allowance. UNKNOWN is not instability.')
Path(__file__).with_name('RAW_RESULTS.json').write_text(json.dumps(I.P.wire(res),indent=2)+'\n');print(json.dumps(counts),flush=True)
