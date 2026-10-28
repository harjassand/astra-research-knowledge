"""Independent rational scalar bounds, with no producer-function imports."""
from fractions import Fraction as Q
from functools import lru_cache
from math import isqrt
BITS=80
TERMS=24
def iv(x):return Q(x),Q(x)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
 v=[x*y for x in a for y in b];return min(v),max(v)
def scale(a,b):return mul(a,iv(b))
def sqrtq(x):
 x=Q(x);assert x>=0
 n=isqrt((x.numerator<<(2*BITS))//x.denominator)
 lo=Q(n,1<<BITS)
 return (lo,lo)if lo*lo==x else(lo,Q(n+1,1<<BITS))
def sqrtiv(a):return sqrtq(a[0])[0],sqrtq(a[1])[1]
def series(y):
 z=(y-1)/(y+1);assert 0<=z<=Q(1,3)
 total=2*sum(z**(2*j+1)/Q(2*j+1)for j in range(TERMS))
 tail=2*z**(2*TERMS+1)/(Q(2*TERMS+1)*(1-z*z))
 return total,total+tail
LOG2=series(Q(2))
@lru_cache(None)
def logq(x):
 x=Q(x);assert x>0
 if x<1:return neg(logq(1/x))
 n=0
 while x>=2:x/=2;n+=1
 return add(series(x),scale(LOG2,n))
def logiv(a):
 assert a[0]>0
 return logq(a[0])[0],logq(a[1])[1]
def hterm(a):
 lo=max(Q(0),a[0]);hi=min(Q(1),a[1]);assert lo<=hi
 if hi==0:return iv(0)
 if lo==0:
  assert hi<=Q(1,4)
  return Q(0),-hi*logq(hi)[0]
 return neg(mul((lo,hi),logiv((lo,hi))))
def entropy(intervals):
 ans=iv(0)
 for a in intervals:ans=add(ans,hterm(a))
 return ans
def upper_entropy(s,n):
 zz=scale(add(iv(1),sqrtq((n-1)*(n*s-1))),Q(1,n))
 small=scale(sub(iv(1),zz),Q(1,n-1))
 return add(hterm(zz),scale(hterm(small),n-1))
def lower_entropy3(q):
 if q<Q(1,2):
  a=scale(add(iv(2),sqrtq(6*q-2)),Q(1,6))
  return add(scale(hterm(a),2),hterm(sub(iv(1),scale(a,2))))
 t=scale(add(iv(1),sqrtq(2*q-1)),Q(1,2))
 return entropy([t,sub(iv(1),t)])
def serial(x):
 x=Q(x);return str(x.numerator)+'/'+str(x.denominator)
def record(a):return{'lower':serial(a[0]),'upper':serial(a[1]),'display_only':list(map(float,a))}
