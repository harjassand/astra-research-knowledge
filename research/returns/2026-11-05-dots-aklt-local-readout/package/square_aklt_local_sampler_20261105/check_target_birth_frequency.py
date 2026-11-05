from local_birth_oracle import LocalLoopBirthSampler
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import json,math,time
route=((0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(1,1),(1,0));K={(0,0),(2,2)}
s=LocalLoopBirthSampler(927541038);n=1000000;count=0;valid=0;st=time.monotonic()
for _ in range(n):
 p=s.propose(K,(3,3));valid+=p is not None;count+=p==route
prob=F(1,2187)/s.rate(K);mean=n*float(prob);sd=math.sqrt(n*float(prob)*(1-float(prob)))
out={'proposals':n,'target_route':route,'observed':count,'expected':mean,'z_score':(count-mean)/sd,'probability_exact':str(prob),'valid':valid,'elapsed_seconds':time.monotonic()-st,'scope':'Independent empirical check of the exact-symbolic birth normalization; not a substitute for it.'}
Path(__file__).with_name('target_birth_frequency.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
