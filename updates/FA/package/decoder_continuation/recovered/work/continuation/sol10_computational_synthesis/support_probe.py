from fractions import Fraction
from itertools import combinations
import random,json,time
r=random.Random(39002); start=time.monotonic(); worst=(0,None);count=0

def check(v,n):
 global worst,count
 c=v[:]
 for i in range(n):
  for u in range(1<<n):
   if u>>i&1: c[u]^=c[u^(1<<i)]
 terms=[u for u in range(1<<n) if c[u]]; m=len(terms)
 mins=[a for a in terms if not any(b!=a and b&a==b for b in terms)]
 ss=sum(1<<(n-a.bit_count()) for a in mins); nonzero=sum(v); ratio=Fraction(ss,m*nonzero); count+=1
 if ratio>worst[0]: worst=(ratio,dict(n=n,m=m,support=[u for u,b in enumerate(v) if b],terms=terms,mins=mins,sum_min=ss))
 return ratio>1
bad=False
for n in range(1,6):
 for k in range(1,min(4,1<<n)+1):
  for supp in combinations(range(1<<n),k):
   v=[0]*(1<<n)
   for u in supp: v[u]=1
   if check(v,n): bad=True;break
  if bad:break
 if bad:break
for it in range(100000 if not bad else 0):
 n=r.randrange(4,9); k=r.randrange(1,min(64,(1<<n)//2)+1);v=[0]*(1<<n)
 for u in r.sample(range(1<<n),k):v[u]=1
 if check(v,n):break
print(json.dumps(dict(counts=count,worst_ratio=str(worst[0]),witness=worst[1],elapsed=time.monotonic()-start)))
