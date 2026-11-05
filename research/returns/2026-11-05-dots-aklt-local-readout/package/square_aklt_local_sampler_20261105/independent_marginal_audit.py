"""Exact finite-law comparator plus independent local-sampler distribution screen."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import sys,json,time,math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'square_aklt_boundary_operation_20261105'))
from perfect_loop_sampler import geometry
from exact_loop_birth_sampler import canonical
from crossed_loop_influence import variants
from local_perfect_sampler import LocalPerfectLoopSampler
query=frozenset([(0,0),(2,2)])
cat=json.loads((ROOT/'square_aklt_loop_audit_20261105/loop_catalog_through12.json').read_text());loops={}
for item in cat:
 for p in variants(item['cyclic_vertices']):
  mx=max(x for x,y in p);my=max(y for x,y in p)
  for dx in range(3-mx):
   for dy in range(3-my):loops[canonical([(x+dx,y+dy)for x,y in p])]=F(item['activity'])
items=sorted(loops.items());ix={p:i for i,(p,w)in enumerate(items)};gs=[geometry(p)for p,w in items];dist=Counter();fullstates=0

def dfs(i,chosen,w):
 global fullstates
 if i==len(items):
  fullstates+=1;k=tuple(j for j in chosen if gs[j][0]&query);dist[k]+=w;return
 dfs(i+1,chosen,w)
 fac=F(1)
 for j in chosen:
  if gs[i][1]&gs[j][1]:return
  fac*=F(3,5)**len(gs[i][0]&gs[j][0])
 dfs(i+1,chosen+[i],w*items[i][1]*fac)
dfs(0,[],F(1));Z=sum(dist.values(),F(0));dist={k:w/Z for k,w in dist.items()}
assert Z==F(2558,2187)
n=int(sys.argv[1])if len(sys.argv)>1 else 100000
seed=int(sys.argv[2]) if len(sys.argv)>2 else 719481
if "--geometric" in sys.argv:
 from geometric_reference_sampler import GeometricReferenceSampler
 factory=GeometricReferenceSampler
else:factory=LocalPerfectLoopSampler
s=factory(query,box=(3,3),seed=seed);counts=Counter();work=Counter();st=time.monotonic()
for _ in range(n):
 routes,stats=s.sample();key=tuple(sorted(ix[p]for p in routes));assert key in dist
 counts[key]+=1;work.update(stats)
rows=[]
for k,p in sorted(dist.items()):
 obs=counts[k];mu=n*float(p);sd=math.sqrt(n*float(p)*(1-float(p)))
 rows.append({'loop_ids':k,'probability':str(p),'observed':obs,'expected':mu,'z_score':(obs-mu)/sd if sd else 0})
out={'seed':seed,'samples':n,'query':sorted(query),'exact_full_configurations':fullstates,'exact_marginal_categories':len(dist),'exact_partition':str(Z),'total_seconds':time.monotonic()-st,'empirical_total_variation':sum(abs(counts[k]/n-float(p))for k,p in dist.items())/2,'mean_work':{k:v/n for k,v in work.items()},'categories':rows,'scope':'Exact comparator and independent empirical sanity check. Correctness relies on Poisson exposure invariant, not a finite statistical test.'}
Path(__file__).with_name('geometric_marginal_audit.json' if '--geometric' in sys.argv else 'independent_marginal_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
