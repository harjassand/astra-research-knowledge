"""Directed Decimal intervals sufficient for the sparse quantum-channel audit."""
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_EVEN
import math
P=50
loctx=Context(prec=P,rounding=ROUND_FLOOR)
hictx=Context(prec=P,rounding=ROUND_CEILING)
midctx=Context(prec=P,rounding=ROUND_HALF_EVEN)

def dec(x):
 if isinstance(x,Decimal):return x
 if isinstance(x,float):return Decimal.from_float(x)
 return Decimal(x)
class IR:
 __slots__=('lo','hi')
 def __init__(self,x=0,hi=None):
  if isinstance(x,IR):self.lo,self.hi=x.lo,x.hi
  else:self.lo,self.hi=dec(x),dec(x if hi is None else hi)
 def __add__(self,y):
  if isinstance(y,IC):return IC(self)+y
  y=IR(y);return IR(loctx.add(self.lo,y.lo),hictx.add(self.hi,y.hi))
 __radd__=__add__
 def __neg__(self):return IR(self.hi.copy_negate(),self.lo.copy_negate())
 def __sub__(self,y):return self+-IR(y) if not isinstance(y,IC) else IC(self)-y
 def __rsub__(self,y):return IR(y)+-self
 def __mul__(self,y):
  if isinstance(y,IC):return IC(self)*y
  y=IR(y)
  pairs=[(a,b) for a in (self.lo,self.hi) for b in (y.lo,y.hi)]
  return IR(min(loctx.multiply(a,b) for a,b in pairs),max(hictx.multiply(a,b) for a,b in pairs))
 __rmul__=__mul__
 def __truediv__(self,y):
  y=IR(y)
  if y.lo<=0<=y.hi:raise ValueError('zero denominator')
  return self*IR(loctx.divide(Decimal(1),y.hi),hictx.divide(Decimal(1),y.lo))
 def __rtruediv__(self,y):return IR(y)/self
 def __abs__(self):
  if self.lo>=0:return self
  if self.hi<=0:return -self
  return IR(0,max(self.hi,self.lo.copy_negate()))
 def sqrt(self):
  assert self.lo>=0
  return IR(midctx.next_minus(midctx.sqrt(self.lo)) if self.lo else Decimal(0),midctx.next_plus(midctx.sqrt(self.hi)))
 @property
 def b(self):return self.hi
class IC:
 __slots__=('real','imag')
 def __init__(self,x=0,y=None):
  if isinstance(x,IC) and y is None:self.real,self.imag=x.real,x.imag
  elif isinstance(x,complex) and y is None:self.real,self.imag=IR(float(x.real)),IR(float(x.imag))
  else:self.real,self.imag=IR(x),IR(0 if y is None else y)
 def __add__(self,y):
  y=IC(y);return IC(self.real+y.real,self.imag+y.imag)
 __radd__=__add__
 def __neg__(self):return IC(-self.real,-self.imag)
 def __sub__(self,y):return self+-IC(y)
 def __rsub__(self,y):return IC(y)+-self
 def __mul__(self,y):
  y=IC(y);return IC(self.real*y.real-self.imag*y.imag,self.real*y.imag+self.imag*y.real)
 __rmul__=__mul__

def arctan_reciprocal(n,terms):
 # Alternating series remainder encloses arctan(1/n).
 total=IR(0);x=IR(1)/n;power=x;xx=x*x
 for k in range(terms):
  v=power/(2*k+1);total=total+v if k%2==0 else total-v;power=power*xx
 nextterm=power/(2*terms+1)
 if terms%2==0:return IR(total.lo,hictx.add(total.hi,nextterm.hi))
 return IR(loctx.subtract(total.lo,nextterm.hi),total.hi)
class IV:
 mpf=IR
 mpc=IC
 @staticmethod
 def sqrt(x):return IR(x).sqrt()
 # Machin identity, with an explicit alternating-series enclosure.
 pi=16*arctan_reciprocal(5,100)-4*arctan_reciprocal(239,30)
iv=IV()
if __name__=='__main__':print(iv.pi.lo,iv.pi.hi)
