from local_birth_oracle import LocalLoopBirthSampler
from exact_lazy_time import ExactTime
from pathlib import Path
from collections import Counter
import random,time,json
s=LocalLoopBirthSampler(20261105);out=[]
for box in[(3,3),None]:
 n=100000;K=[(1,1)];lens=Counter();t=time.monotonic()
 for _ in range(n):
  p=s.propose(K,box)
  if p is not None:lens[len(p)]+=1
 out.append({'box':box,'query':K,'attempts':n,'accepted':sum(lens.values()),'longest_accepted_loop':max(lens),'length_histogram':dict(lens),'observed_birth_intensity':sum(lens.values())/n*float(s.rate(K)),'seconds':time.monotonic()-t})
rng=random.Random(20261105);n=1000;positive=0;t=time.monotonic()
for _ in range(n):
 a=ExactTime.zero().minus_exp(rng);b=ExactTime.zero().minus_exp(rng)
 positive+=a<b
out={'birth':out,'time_comparison':{'independent_exponential_pairs':n,'a_less_b':positive,'seconds':time.monotonic()-t},'scope':'PRNG diagnostic and wallclock measurement; exact-law arguments are separate.'}
Path(__file__).with_name('primitive_benchmarks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
