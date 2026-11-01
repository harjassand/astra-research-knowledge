"""Exact ordinary-win and strict family-extension controls, not prior-art exclusion."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json,sys,os
import independent_aggregate_receiver as I
sys.path.insert(0,os.environ.get('AGGREGATE_SOURCE_DIR','producer-workspace/stochastic_free_aggregate_mass_pending_20261031'));import aggregate_mass as A
rows=[]
for nf in (1,2):
 raw=A.fixture(nf);r=I.parse(raw);unit=[(u,v,F(1))for u,v,k in raw];table={(u,v):k for u,v,k in unit}
 assert all(table[v,u]==k for (u,v),k in table.items()) # c=(1,...,1) detailed balance.
 assert A.G.qualitative(raw)['status']=='UNKNOWN' # Actual older one-hub finder.
 # Remove leaf A+rare nodes; remaining internal complex graph has unit symmetric
 # edges and is connected. Its Laplacian's kernel is the constants (tree proof).
 a=r['a'];leaves={u for u,v,k in r['internal']if u[a]==1 and any(u[x]for x in r['rare'])}
 remain={u for u,v,k in r['internal']if u not in leaves};rates={(u,v):k for u,v,k in r['internal']if u in remain and v in remain}
 assert all(rates[v,u]==k==1 for (u,v),k in rates.items())
 seen={next(iter(remain))};todo=list(seen)
 while todo:
  u=todo.pop()
  for x,v in rates:
   if x==u and v not in seen:seen.add(v);todo.append(v)
 assert seen==remain
 # All three hub products equal a^2; positivity forces B=C=D=A.
 # The rate-2 reverse leaf has zero net leaf balance, forcing A*D=2*C*D,
 # contradictory to A=C>0. Identify the leaf directly, not by coordinate label.
 bad=[(u,v,k)for u,v,k in r['internal']if u not in leaves and v in leaves and k!=1]
 assert len(bad)==1 and bad[0][2]==2
 # A triangle has no vertex cover meeting each of its three target edges only once.
 vs=r['rare'];covers=[]
 for mask in range(1<<len(vs)):
  ss={v for i,v in enumerate(vs)if mask>>i&1}
  if all(u in ss or v in ss for u,v in r['edges']):covers.append(ss)
 assert not any(all(len({u,v}&ss)==1 for u,v in r['edges'])for ss in covers)
 rows.append(dict(free_species=nf,ordinary_unit_detailed_balance=True,old_one_hub_finder='UNKNOWN',all_target_triangle_has_no_single_hit_cover=True,perturbed_leaf_noncomplex_balance=True,residual_symmetric_complex_nodes=len(remain)))
res=dict(status='PASS_ORDINARY_AND_STRICT_EXTENSION_CONTROLS',rows=rows,scope='No exclusion of ordinary Foster/angular/piecewise/fluid-regeneration methods; no historical novelty claim.')
Path(__file__).with_name('COMPARATOR_RESULTS.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
