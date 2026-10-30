from itertools import product,combinations
from pathlib import Path
import json
counts=dict(error_configurations=0,nearest_choice_configurations=0,inactive_hub_checks=0,reversal_subsets=0,inactive_cases_with_remote_overlap=0)
for label,edges,n,kind in [('cycle6',[(i,(i+1)%6) for i in range(6)],6,'repetition'),('K4',list(combinations(range(4),2)),4,'even')]:
 stars=[sum(1<<j for j,e in enumerate(edges) if v in e) for v in range(n)]
 def subsets(mask):
  a=mask
  while True:
   yield a
   if a==0:break
   a=(a-1)&mask
 codes=[]
 for star in stars:
  codes.append([0,star] if kind=='repetition' else [x for x in subsets(star) if x.bit_count()%2==0])
 minima=[]
 for e in range(1<<len(edges)):
  choices=[]
  for star,code in zip(stars,codes):
   d=min(((e&star)^c).bit_count() for c in code)
   choices.append([((e&star)^c) for c in code if ((e&star)^c).bit_count()==d])
  minima.append(choices)
 U=[sum(ch[0].bit_count() for ch in choices) for choices in minima]
 for e,choices in enumerate(minima):
  counts['error_configurations']+=1
  inactive=[v for v,star in enumerate(stars) if all(U[e^F]>=U[e] for F in subsets(star))]
  for rs in product(*choices):
   counts['nearest_choice_configurations']+=1
   R=0;overlap=0
   for r in rs:overlap|=R&r;R|=r
   cs=[(e&s)^r for s,r in zip(stars,rs)]
   for v in inactive:
    counts['inactive_hub_checks']+=1
    assert not overlap&stars[v]
    if overlap&~stars[v]:counts['inactive_cases_with_remote_overlap']+=1
    for c in codes[v]:assert 2*((R&stars[v])&c).bit_count()<=c.bit_count()
    for F in subsets(R&stars[v]):
     new=tuple(r^(F&s) for r,s in zip(rs,stars))
     assert U[e^F]==U[e]
     assert all(r in candidates for r,candidates in zip(new,minima[e^F]))
     assert all(((e^F)&s)^r==c for s,r,c in zip(stars,new,cs))
     Rnew=0
     for r in new:Rnew|=r
     assert Rnew==R
     counts['reversal_subsets']+=1
out=dict(status='pass',**counts,scope='Exhaustive toy two-endpoint potential tests with all nearest-codeword ties; not a Tanner-code density simulation')
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
