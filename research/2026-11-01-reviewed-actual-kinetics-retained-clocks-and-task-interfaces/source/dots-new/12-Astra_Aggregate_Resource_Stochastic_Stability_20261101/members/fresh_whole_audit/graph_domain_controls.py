from itertools import combinations,product,permutations
from fractions import Fraction as F
from pathlib import Path
from copy import deepcopy
import json,sys,random,os
import independent_aggregate_receiver as I
sys.path.insert(0,os.environ.get('AGGREGATE_SOURCE_DIR','producer-workspace/stochastic_free_aggregate_mass_pending_20261031'));import aggregate_mass as A
counts={};hit=lambda k,n=1:counts.__setitem__(k,counts.get(k,0)+n)
def rawgraph(m,edges):
 n=m+3;z=lambda *ix:tuple(ix.count(i)for i in range(n));hs=[z(*e)for e in edges];raw=[(z(),z(0),F(1)),(z(0),z(),F(1))]
 for h in hs:raw.extend(((z(0,0),h,F(1)),(h,z(0,0),F(1))))
 for v in range(1,n):
  targets=hs if v>m else [hs[(v-1)%len(hs)]]
  for h in targets:raw.extend(((z(0,v),h,F(1)),(h,z(0,v),F(1))))
 return raw
def minimal_covers(vs,edges):
 out=[]
 for mask in range(1<<len(vs)):
  s={v for i,v in enumerate(vs)if mask>>i&1};hit('test_only_cover_masks')
  if not all(u in s or v in s for u,v in edges):continue
  if any(all(u in s-{a}or v in s-{a}for u,v in edges)for a in s):continue
  out.append(s)
 return out
for m in range(2,6):
 possible=list(combinations(range(1,m+1),2))
 for mask in range(1,1<<len(possible)):
  edges=[e for i,e in enumerate(possible)if mask>>i&1];vs=sorted(set().union(*map(set,edges)));cs=minimal_covers(vs,edges);adj={v:{w for e in edges if v in e for w in e if w!=v}for v in vs}
  D=all(all(w in adj[u]or w in adj[v]for w in set(vs)-cover)for cover in cs for u,v in edges if u in cover and v in cover)
  raw=rawgraph(m,edges);qa=I.qualitative(raw);assert (qa['status']!='UNKNOWN')==D;assert I.canonical(qa)==I.canonical(A.qualitative(raw));hit('all_graph_raw_cases')
  if not D:hit('structural_unknowns');continue
  hit('admitted_graphs');r=I.parse(raw)
  for weights in ([0]*m,[1]*m,*([1 if i!=j else 7 for i in range(m)]for j in range(m))):
   x=(1,*weights,11,13);tau=min(sum(x[v]for v in c)for c in cs);assert tau==I.P.C.cover_weight(r['inventory'],x);R=1+tau
   Q=sum(x[v]*x[w]for v,w in edges);assert tau*tau<=4*len(edges)*Q
   heavy=[v for v in vs if x[v]>R];H=sum(x[v]for v in heavy);bad=[e for e in edges if any(set(e)<=c and sum(x[v]for v in c)==tau for c in cs)];qb=sum(x[v]*x[w]for v,w in bad);qg=Q-qb
   assert qb<=len(edges)*R*R
   if H:assert qb*H<=len(edges)*R*qg
   hit('weighted_geometry_states')
   for src,dst,rate,y in I.P.enabled(r,x):
    if sum(src)!=sum(dst):continue
    N,a,f,u,j,rr=I.coords(r,x);_,ap,fp,up,jp,rp=I.coords(r,y)
    assert abs(rp-rr)<=1
    free_channel=any(src[v]or dst[v]for v in r['free'])
    if free_channel:
     assert jp==j
     if src[r['a']]:assert rp>=rr and F(ap,(rp+1)**2)<F(a,(rr+1)**2)
     hit('free_arm_inventory_geometry')
    if src[r['a']]and any(src[v]and x[v]>rr for v in r['rare']):assert rp>=rr;hit('heavy_arm_geometry')
raw=A.fixture();q=I.qualitative(raw)
for perm in permutations(range(5)):
 rr=[(tuple(u[i]for i in perm),tuple(v[i]for i in perm),k)for u,v,k in raw];assert I.canonical(I.qualitative(rr))==I.canonical(A.qualitative(rr));hit('qualitative_permutations')
for bad in (True,2.0,'2',1,0,-1,None):
 try:I.construct(raw,bad)
 except(ValueError,TypeError):hit('domain_refusals')
 else:raise AssertionError('bad t')
for bad in (True,1.0,'1',-1,None):
 try:I.construct(raw,2,bad)
 except(ValueError,TypeError):hit('domain_refusals')
 else:raise AssertionError('bad cap')
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
# Requests genuinely too costly remain UNKNOWN while retaining qualitative proof scope.
extremes=[]
for t,scale in ((F(1001,1000),F(1000)),(F(3,2),F(7)),(F(17,2),F(1,1000))):
 rr=[(u,v,k*(scale if i%3==0 else 1/scale if i%3==1 else 1))for i,(u,v,k)in enumerate(A.fixture(2))]
 c=I.construct(rr,t);assert I.canonical(c)==I.canonical(A.construct(rr,t));hit('extreme_receipt_matches')
 extremes.append(dict(t=t,scale=scale,status=c['status'],required_core_steps=c.get('required_core_steps'),K=c.get('mass_head',{}).get('K')))
res=dict(status='PASS_GRAPH_DOMAIN_AND_EXTREME_CONTROLS',counts=counts,extremes=extremes,scope='Exhaustive small graphs and covers only in test driver, never production acquisition; all-unit UNKNOWN graphs are detailed-balance controls, not instability.')
Path(__file__).with_name('GRAPH_DOMAIN_RESULTS.json').write_text(json.dumps(I.P.wire(res),indent=2)+'\n');print(json.dumps(counts),flush=True)
