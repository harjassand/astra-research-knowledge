from fractions import Fraction as F
from math import comb
from functools import lru_cache
import json
@lru_cache(None)
def phi(n,y,a,ell,s):
    N=n+ell-1; d=y+ell-1
    if N==0:return F(1)
    den=comb(N,d)
    return sum((F(comb(a,h)*comb(N-a,d-h),den*(1+h)**s)
                for h in range(max(0,d-(N-a)),min(a,d)+1)),F(0))
count=0; max_square=F(1); max_loss=F(1)
for ell in range(1,4):
  for n in range(1,21):
    for y in range(n+1):
      for a in range(y+1):
        for s in range(1,4):
          v=phi(n,y,a,ell,s)
          if y<n:
            reset=F(a,y+ell)
            rhs=(1-reset)*phi(n,y+1,a,ell,s)
            if a:rhs+=reset*phi(n,y+1,a-1,ell,s)
            assert rhs==v
            assert (1-reset)*a*(y+ell)+reset*(a-1)*(y+ell)==a*(y+ell-1)
            count+=1
          if a<y:assert phi(n,y,a+1,ell,s)<=v
          max_square=max(max_square,phi(n,y,a,ell,2*s)/(v*v))
          for m in range(1,min(4,a)+1):
            max_loss=max(max_loss,phi(n-m,y-m,a-m,ell,s)/v)
print(json.dumps({'exact_harmonic_cases':count,'n_max':20,'ell_values':[1,2,3],
 'grades':[1,2,3], 'max_sampled_square_ratio':str(max_square),
 'max_sampled_bounded_loss_ratio':str(max_loss),
 'scope':'exact finite checks; not proof of uniform constants or global recurrence'},indent=2))
