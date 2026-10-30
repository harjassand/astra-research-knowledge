from pathlib import Path
from fractions import Fraction as F
import importlib.util,sys,itertools,json,random
base=Path(__file__).parent;sys.path.insert(0,str(base/'integrated_phase_sources'))
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
new=load('review_new_rank',base/'rank_sources/acquire_rank_face.py');old=load('review_old_integrated',base/'integrated_phase_sources/acquire_integrated_phase_face.py')
def brute(k,Q,E):
 for vals in itertools.product(range(1,k),repeat=k-1):
  r=(0,)+vals
  if any(r[j]>r[i] for i,j in E):continue
  if all(any(u==i and r[v]<r[i] for u,v,q in Q) for i in range(1,k)):return r
 return None
count=0
for k in (2,3):
 edges=[(i,j) for i in range(k) for j in range(k) if i!=j]
 for qb in range(1<<len(edges)):
  Q=[(i,j,F(1)) for l,(i,j) in enumerate(edges) if qb>>l&1]
  for eb in range(1<<len(edges)):
   E=[e for l,e in enumerate(edges) if eb>>l&1]
   a=new.acquire_ranks(k,0,Q,E);b=brute(k,Q,E)
   assert (a is not None)==(b is not None),(k,Q,E,a,b)
   count+=1
rng=random.Random(3010)
for trial in range(2000):
 k=4;edges=[(i,j) for i in range(k) for j in range(k) if i!=j]
 Q=[(i,j,F(rng.randint(1,7),rng.randint(1,5))) for i,j in edges if rng.random()<.4]
 E=[e for e in edges if rng.random()<.3]
 a=new.acquire_ranks(k,0,Q,E);b=brute(k,Q,E)
 assert (a is not None)==(b is not None),(Q,E,a,b)
 count+=1
raw=json.loads((base/'rank_sources/raw_inputs.json').read_text());results={}
for key,net in raw.items():
 results[key]={'new':new.acquire(net),'old':old.acquire(net)}
out={'graph_comparisons':count,'all_graph_comparisons_match':True,'raw_comparisons':results}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print('graph comparisons',count)
for key,r in results.items():print(key,r['new']['status'],r['old']['status'],r['new'].get('pool_certificate',{}).get('rank_certificate'))
