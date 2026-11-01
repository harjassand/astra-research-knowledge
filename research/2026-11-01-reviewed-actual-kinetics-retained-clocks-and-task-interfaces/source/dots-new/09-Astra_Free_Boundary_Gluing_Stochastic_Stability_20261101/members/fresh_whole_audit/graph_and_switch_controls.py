from pathlib import Path
from fractions import Fraction as Q
from itertools import combinations,product
import os,sys,json,random,time
import independent_glue_receiver as I
HERE=Path(__file__).resolve().parent;SOURCE=Path(os.environ.get('GLUE_SOURCE_DIR',(HERE.parent if (HERE.parent/'free_port_glue.py').is_file() else HERE.parent/'stochastic_free_port_glue_pending_20261031'))).resolve();OUT=Path(os.environ.get('AUDIT_OUTPUT_DIR',HERE)).resolve();OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(SOURCE));import free_port_glue as G
counts=dict(graphs=0,admitted=0,cover_masks_charged=0,states=0,optimal_cover_ties=0,packing_checks=0,heavy_bounds=0,global_bad_bounds=0,enabled_edge_queries=0,raw_repartition_controls=0)
rng=random.Random(612033);start=time.monotonic()
def fixture(m,edges):
 n=m+2;z=lambda *v:tuple(v.count(i)for i in range(n));rr=[(z(),z(0),Q(1)),(z(0),z(),Q(1))]
 for edge in edges:rr.extend([(z(0,0),z(*edge),Q(1)),(z(*edge),z(0,0),Q(1))])
 for x in range(1,n):rr.extend([(z(0,x),z(*edges[(x-1)%len(edges)]),Q(1)),(z(*edges[(x-1)%len(edges)]),z(0,x),Q(1))])
 return rr
for m in range(2,6):
 pairs=list(combinations(range(1,m+1),2))
 for mask in range(1,1<<len(pairs)):
  edges=[e for j,e in enumerate(pairs)if mask>>j&1];raw=fixture(m,edges);counts['graphs']+=1
  # Independent direct graph condition: all minimal covers and all outside vertices.
  covers=[]
  for cm in range(1<<m):
   counts['cover_masks_charged']+=1;C={v for v in range(1,m+1)if cm>>(v-1)&1}
   if any(not (set(e)&C)for e in edges):continue
   if any(all(set(e)&(C-{v})for e in edges)for v in C):continue
   covers.append(C)
  graph_ok=all(any((min(w,u),max(w,u))in edges for u in e)for C in covers for e in edges if set(e)<=C for w in set(range(1,m+1))-C)
  iq=I.qualitative(raw);gq=G.qualitative(raw);assert (iq['status']=='CERTIFIED_QUALITATIVE')==graph_ok==(gq['status']=='CERTIFIED_QUALITATIVE')
  if not graph_ok:continue
  assert I.canonical(iq)==I.canonical(gq);counts['admitted']+=1;r=I.parse(raw);vs=r['rare']
  # Enumerate only these small fixtures, never production acquisition.
  cov=[]
  for cm in range(1<<len(vs)):
   counts['cover_masks_charged']+=1;C={v for j,v in enumerate(vs)if cm>>j&1}
   if all(set(e)&C for e in edges) and all(not all(set(e)&(C-{v})for e in edges)for v in C):cov.append(C)
  states=[(0,)*(m+2),(1,)*(m+2)]+[tuple(rng.randrange(6)for _ in range(m+2))for j in range(8)]
  for x in states:
   tau=min(sum(x[v]for v in C)for C in cov);opt=[C for C in cov if sum(x[v]for v in C)==tau];R=x[r['a']]+tau
   assert I.C.cover_weight(r['inventory'],x)==tau
   bad={e for e in edges if x[e[0]]*x[e[1]] and any(set(e)<=C for C in opt)}
   assert set(I.C.bad_active_edges(r['inventory'],x))==bad
   qbad=sum(x[u]*x[v]for u,v in bad);qgood=sum(x[u]*x[v]for u,v in edges if (u,v)not in bad);H=sum(x[v]for v in vs if x[v]>R)
   assert 4*len(edges)*(qbad+qgood)>=tau*tau;counts['packing_checks']+=1
   assert qbad<=len(edges)*R*R;counts['global_bad_bounds']+=1
   assert qbad*H<=len(edges)*R*qgood;counts['heavy_bounds']+=1
   assert x[r['a']]+min(x[v]for v in r['h0'])<=R
   counts['states']+=1;counts['optimal_cover_ties']+=int(len(opt)>1)
   for u,v in edges:
    if not x[u]*x[v]:continue
    y=list(x);y[u]-=1;y[v]-=1;newtau=min(sum(y[w]for w in C)for C in cov)
    assert (tau-newtau==2)==((u,v)in bad);counts['enabled_edge_queries']+=1
# Raw deletion can change candidate distinguished F/core, so every call reacquires.
raw=fixture(3,[(1,2),(1,3),(2,3)])
for edge in ([(1,2)],[(1,2),(2,3)]):
 rr=fixture(3,edge);q=I.qualitative(rr);assert q['status']=='CERTIFIED_QUALITATIVE' and I.canonical(q)==I.canonical(G.qualitative(rr));counts['raw_repartition_controls']+=1
result=dict(status='PASS',seconds=time.monotonic()-start,counts=counts,scope='Exhaustive graphs through five core vertices; exhaustive cover masks ONLY in these charged small tests, not production receiver.')
(OUT/'GRAPH_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
