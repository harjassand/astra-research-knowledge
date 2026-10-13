from fractions import Fraction
from itertools import combinations, product
import json, time

def vals(terms,cs,n,p):
    return [sum(c for a,c in zip(terms,cs) if u&a==a)%p for u in range(1<<n)]
def main():
  start=time.monotonic(); counts=0; worst=(0,None); bad=[]
  for n in range(1,5):
    for m in range(1,min(6,1<<n)+1):
      for terms in combinations(range(1<<n),m):
        mins=[a for a in terms if not any(b!=a and b&a==b for b in terms)]
        ss=sum(Fraction(1,1<<a.bit_count()) for a in mins)
        for p in [2,3]:
          for cs in product(range(1,p),repeat=m):
            vs=vals(terms,cs,n,p); mass=Fraction(sum(v!=0 for v in vs),1<<n)
            ratio=ss/mass/m; counts+=1
            if ratio>worst[0]: worst=(ratio,dict(n=n,m=m,p=p,terms=terms,cs=cs,mins=mins,mass=str(mass),sum_min=str(ss)))
            if ratio>1:
              bad.append(worst[1]); print(json.dumps(dict(counts=counts,worst_ratio=str(worst[0]),witness=worst[1],elapsed=time.monotonic()-start))); return
  print(json.dumps(dict(counts=counts,worst_ratio=str(worst[0]),witness=worst[1],elapsed=time.monotonic()-start)))
if __name__=='__main__': main()
