import math,json
from fractions import Fraction as F
from functools import lru_cache
@lru_cache(None)
def phi(n,e,A,Y,s):
 N=n+e-1; d=Y+e-1
 if N==0:return F(1)
 den=math.comb(N,d)
 return sum((F(math.comb(A,h)*math.comb(N-A,d-h),den*(1+h)**s) for h in range(max(0,d-(N-A)),min(A,d)+1)),F(0))
cases=0;monotone=0
for n in range(1,16):
 for e in range(1,5):
  for s in range(1,4):
   for Y in range(n+1):
    for A in range(Y+1):
     p=phi(n,e,A,Y,s)
     if Y<n:
      rhs=(1-F(A,Y+e))*phi(n,e,A,Y+1,s)
      if A:rhs+=F(A,Y+e)*phi(n,e,A-1,Y+1,s)
      assert p==rhs,(n,e,A,Y,s,p,rhs)
      cases+=1
     if A<Y:
      assert phi(n,e,A+1,Y,s)<=p
      monotone+=1
     assert p*p<=phi(n,e,A,Y,2*s)
print(json.dumps({'exact_harmonic_states':cases,'monotonicity_states':monotone,'status':'all exact rational equalities/inequalities passed','scope':'finite falsification only; analytic proof reviewed separately'},indent=2))
