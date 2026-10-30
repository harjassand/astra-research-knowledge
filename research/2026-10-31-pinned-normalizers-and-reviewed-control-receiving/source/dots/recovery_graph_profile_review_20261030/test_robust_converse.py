import runpy,random,json,contextlib,io
from fractions import Fraction as F
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):m=runpy.run_path('producer-workspace/check_rank_obstruction.py')
rng=random.Random(301028);counts={};checked=0
for n in range(4,9):
 edges=[(i,j) for i in range(n) for j in range(n) if i!=j]
 for _ in range(200):
  Q={e for e in edges if rng.random()<.3};E={e for e in edges if e[0]!=0 and rng.random()<.3}
  w=m['rank_or_witness'](n,0,Q,E);assert m['verify'](n,Q,E,w)
  counts[w['status']]=counts.get(w['status'],0)+1
  if w['status']=='FAST_RESET_OBSTRUCTION':
   rates={e:F(rng.randint(1,9),rng.randint(1,5)) for e in Q};qmax=max([F(0)]+[sum((q for (u,v),q in rates.items() if u==i),F(0)) for i in range(n)])
   d={i:w['distance'].get(i,0) for i in range(n)};T=set(w['entry_types']);SS=set(w['processed']);K=F(11)
   for i in range(n):
    if i in SS:continue
    drift=sum((q*(d[j]-d[i]) for (u,j),q in rates.items() if u==i),F(0))
    if i in T:drift+=K*(d[w['parent'][i]]-d[i])
    assert drift<=-K*(i in T)+n*qmax
   checked+=1
out={'random_graphs_checked':1000,'counts':counts,'exact_rational_generator_checks':checked,'seed':301028}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
