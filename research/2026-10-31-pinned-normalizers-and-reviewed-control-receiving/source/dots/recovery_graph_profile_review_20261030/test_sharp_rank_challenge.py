import runpy,contextlib,io,json,random
from fractions import Fraction as F
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):m=runpy.run_path('producer-workspace/check_sharp_rank_policy.py')
build=m['build'];w=build(5,{(1,0),(2,0),(3,0),(4,1)},{(2,3),(3,4)})
assert w['ranks']=={0:0,1:1,2:2,3:2,4:2}
assert w['parents']=={2:3,3:4} and w['distance'][2]==2
rng=random.Random(180334);tested=0;multi_parent=0;max_distance=0
for trial in range(5000):
 n=rng.randint(3,10);edges=[(i,j) for i in range(n) for j in range(n) if i!=j]
 Q={e for e in edges if rng.random()<.35};E={e for e in edges if e[0]!=0 and rng.random()<.13}
 a=build(n,Q,E)
 if a is None:continue
 rates={e:F(rng.randint(1,7),rng.randint(1,5)) for e in Q};qmax=max([F(0)]+[sum((q for (u,v),q in rates.items() if u==i),F(0)) for i in range(n)])
 d=a['distance'];D=set(a['dangerous']);K=F(13)
 for i in range(n):
  drift=sum((q*(d[j]-d[i]) for (u,j),q in rates.items() if u==i),F(0))
  if i in D:drift+=K*(d[a['parents'][i]]-d[i])
  assert drift<=-K*(i in D)+n*qmax
  assert all(a['ranks'][j]>=a['ranks'][i]-1 for u,j in Q if u==i and i not in D)
 tested+=1;mm=max(d.values());max_distance=max(max_distance,mm);multi_parent+=mm>=2
out={'explicit_two_edge_parent_chain':w,'random_graphs':5000,'accepted_exact_drift_checks':tested,'multiple_parent_chain_policies':multi_parent,'max_parent_distance':max_distance}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
