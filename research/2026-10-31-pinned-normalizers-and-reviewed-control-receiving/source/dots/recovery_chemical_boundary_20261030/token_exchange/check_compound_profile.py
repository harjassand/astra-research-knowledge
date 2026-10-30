from fractions import Fraction as F
from math import comb
from functools import lru_cache
import json

def law(N,a,d):
    den=comb(N,d)
    return [(j,F(comb(a,j)*comb(N-a,d-j),den))
      for j in range(max(0,d-(N-a)),min(a,d)+1)]
@lru_cache(None)
def profile(n,y,a,ell,k,s):
    dist={a:F(1)}
    for h in range(k):
        nxt={}
        for marked,p in dist.items():
            for out,w in law(n+ell-h-1,marked,y+ell-h-1):
                nxt[out]=nxt.get(out,F(0))+p*w
        dist=nxt
    return sum((p/F((1+a)**s) for a,p in dist.items()),F(0))
cases=0
for k in range(1,4):
 for ell in [k,k+1]:
  for n in range(1,11):
   for y in range(n):
    for a in range(y+1):
     for s in [1,2,3]:
      val=profile(n,y,a,ell,k,s)
      rhs=sum((p*profile(n,y+1,a-lost,ell,k,s)
       for lost,p in law(y+ell,a,k)),F(0))
      assert val==rhs,(n,y,a,ell,k,s,val,rhs)
      if a<y:assert profile(n,y,a+1,ell,k,s)<=val
      cases+=1
print(json.dumps({'exact_harmonic_cases':cases,'n_max':10,
 'batch_sizes':[1,2,3],'offsets':'k and k+1','grades':[1,2,3],
 'scope':'finite exact regression; not global coverage'},indent=2))
