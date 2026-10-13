from fractions import Fraction
import random,json,time
r=random.Random(39102); start=time.monotonic(); worst=(0,None)
for it in range(100000):
 n=r.randrange(3,10); m=r.randrange(2,min(35,1<<n)+1); p=r.choice([2,3,4,5,6])
 terms=r.sample(range(1<<n),m); cs=[r.randrange(1,p) for a in terms]
 mins=[a for a in terms if not any(b!=a and b&a==b for b in terms)]
 s=sum(1<<(n-a.bit_count()) for a in mins)
 nonzero=sum(sum(c for a,c in zip(terms,cs) if u&a==a)%p!=0 for u in range(1<<n))
 ratio=Fraction(s,m*nonzero)
 if ratio>worst[0]: worst=(ratio,dict(n=n,m=m,p=p,terms=terms,cs=cs,mins=mins,nonzero=nonzero,sum_min=s))
 if ratio>1: break
print(json.dumps(dict(counts=it+1,worst_ratio=str(worst[0]),witness=worst[1],elapsed=time.monotonic()-start)))
