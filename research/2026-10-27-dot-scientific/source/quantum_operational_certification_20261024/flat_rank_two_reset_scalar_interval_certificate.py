"""Exact dyadic outward-rounded interval proof for the compact scalar derivative.
All arithmetic is Python integer arithmetic. Logs use a certified atanh series.
"""
from math import isqrt
from fractions import Fraction
import json
S=1<<80
class I:
 def __init__(self,lo,hi=None,raw=False):
  if raw:self.lo,self.hi=lo,hi
  else:
   lo=Fraction(lo);hi=lo if hi is None else Fraction(hi)
   self.lo=(lo.numerator*S)//lo.denominator;self.hi=-((-hi.numerator*S)//hi.denominator)
 def __add__(self,o):
  o=cv(o);return I(self.lo+o.lo,self.hi+o.hi,True)
 __radd__=__add__
 def __neg__(self):return I(-self.hi,-self.lo,True)
 def __sub__(self,o):return self+-cv(o)
 def __rsub__(self,o):return cv(o)+-self
 def __mul__(self,o):
  o=cv(o);v=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi];return I(min(v)//S,-((-max(v))//S),True)
 __rmul__=__mul__
 def __truediv__(self,o):
  o=cv(o);assert o.lo>0
  v=[Fraction(self.lo*S,o.lo),Fraction(self.lo*S,o.hi),Fraction(self.hi*S,o.lo),Fraction(self.hi*S,o.hi)];a=min(v);b=max(v)
  return I(a.numerator//a.denominator,-((-b.numerator)//b.denominator),True)
 def sqrt(self):
  assert self.lo>=0
  lo=isqrt(self.lo*S);h=isqrt(self.hi*S);return I(lo,h+(h*h<self.hi*S),True)
def cv(o):return o if isinstance(o,I) else I(o)
def basiclog(t): # t in[1,2], exact interval certified
 z=(t-1)/(t+1);z2=z*z;term=z;tot=I(0)
 for j in range(60):tot=tot+term/(2*j+1);term=term*z2
 # remaining sum from exponent121 bounded by first power /[121(1-z²)]
 tail=2*term/(121*(1-z2))
 return 2*tot+I(0,tail.hi,True)
LOG2=basiclog(I(2))
def log(t):
 # General endpoint range reduction via exact intervals avoids odd-integer loss.
 def endpoint(n):
  k=0;v=I(n,n,True)
  while v.lo<S:v=v*2;k-=1
  while v.hi>2*S:v=v/2;k+=1
  return basiclog(v)+k*LOG2
 a=endpoint(t.lo);b=endpoint(t.hi);return I(a.lo,b.hi,True)
def deriv(t):
 ds=(9*t*t+2*t+1).sqrt();do=(t*t+1).sqrt()
 cs=(1+9*t)/ds;co=4*t/do
 ls=(1+3*t+ds)/2;lo=(1+t+do)/2
 return (1-cs+co)*log(t)/2+log(I(Fraction(4,27)))+2*log((t+3)/(t+1))+cs*log(ls)-co*log(lo)-co*LOG2/2
stack=[(Fraction(1,20),Fraction(10),0)];leaves=[]
while stack:
 l,h,depth=stack.pop();v=deriv(I(l,h))
 if v.lo>0:
  leaves.append((l,h,v.lo));continue
 assert depth<30,(l,h,v.lo,v.hi)
 m=(l+h)/2;stack.extend([(l,m,depth+1),(m,h,depth+1)])
leaves.sort();assert leaves[0][0]==Fraction(1,20) and leaves[-1][1]==10
assert all(leaves[i][1]==leaves[i+1][0] for i in range(len(leaves)-1))
out={'status':'PASS','arithmetic':'exact integers; outward dyadic intervals; bounded log series','precision_bits':80,'log_series_terms':60,'cover':['1/20','10'],'intervals':len(leaves),'minimum_certified_derivative_lower_bound':str(Fraction(min(v for _,_,v in leaves),S))}
print(json.dumps(out,indent=2))
from pathlib import Path
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
