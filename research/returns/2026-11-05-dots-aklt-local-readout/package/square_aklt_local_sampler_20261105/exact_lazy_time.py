"""Exact almost-sure ordering of rational linear combinations of Exp(1) atoms.
An exponential is −log(U), where U is revealed lazily in fair-bit blocks.
All enclosures are rational and proven by a positive atanh power series tail.
No float participates in ordering. PRNG streams provide reproducible tests;
exactness is the mathematical ideal-independent-fair-bits specification.
"""
from fractions import Fraction as F
from functools import lru_cache,total_ordering
import random

def log_reduced_bounds(x,terms):
 assert F(1)<=x<=F(2) and terms>=1
 z=(x-1)/(x+1);z2=z*z;power=z;s=F(0)
 for j in range(terms):s+=2*power/(2*j+1);power*=z2
 tail=2*power/((2*terms+1)*(1-z2))
 return s,s+tail

@lru_cache(maxsize=64)
def log_two_bounds(terms):return log_reduced_bounds(F(2),terms)

def log_bounds(x,terms=16):
 x=F(x);assert x>0
 k=x.numerator.bit_length()-x.denominator.bit_length()
 scale=F(2)**k;y=x/scale
 if y<1:k-=1;y*=2
 elif y>=2:k+=1;y/=2
 assert 1<=y<2
 lo,hi=log_reduced_bounds(y,terms);l2,h2=log_two_bounds(terms)
 return (lo+k*l2,hi+k*h2) if k>=0 else(lo+k*h2,hi+k*l2)

class LazyExp:
 __slots__=('rng','bits','prefix','cache')
 def __init__(self,rng=None):
  self.rng=rng if rng is not None else random.SystemRandom();self.bits=0;self.prefix=0;self.cache=[]
 def uniform_bounds(self,bits):
  if bits>self.bits:
   new=bits-self.bits;self.prefix=(self.prefix<<new)|self.rng.getrandbits(new);self.bits=bits
  return F(self.prefix,1<<self.bits),F(self.prefix+1,1<<self.bits)
 def bounds(self,level=0):
  assert level>=0
  while len(self.cache)<=level:
   lev=len(self.cache);bits=32*(1<<lev);terms=16*(1<<lev)
   low,up=self.uniform_bounds(bits)
   while low==0:
    bits*=2;low,up=self.uniform_bounds(bits)
   ll,lh=log_bounds(low,terms);ul,uh=log_bounds(up,terms)
   lo,hi=-uh,-ll
   if self.cache:lo=max(lo,self.cache[-1][0]);hi=min(hi,self.cache[-1][1])
   assert lo<=hi
   self.cache.append((lo,hi))
  return self.cache[level]
 def time(self):return ExactTime({self:F(1)})

@total_ordering
class ExactTime:
 __slots__=('terms','constant')
 __hash__=None
 def __init__(self,terms=None,constant=0):
  self.terms={a:F(c) for a,c in(terms or {}).items() if c};self.constant=F(constant)
 @classmethod
 def zero(cls):return cls()
 def plus_exp(self,rng=None):return self+exponential_time(rng)
 def minus_exp(self,rng=None):return self-exponential_time(rng)
 @staticmethod
 def coerce(x):
  if isinstance(x,ExactTime):return x
  if isinstance(x,LazyExp):return x.time()
  return ExactTime(constant=F(x))
 def __add__(self,other):
  other=self.coerce(other);terms=self.terms.copy()
  for a,c in other.terms.items():
   terms[a]=terms.get(a,F(0))+c
   if not terms[a]:del terms[a]
  return ExactTime(terms,self.constant+other.constant)
 __radd__=__add__
 def __neg__(self):return ExactTime({a:-c for a,c in self.terms.items()},-self.constant)
 def __sub__(self,other):return self+-self.coerce(other)
 def __rsub__(self,other):return self.coerce(other)+-self
 def __mul__(self,c):
  c=F(c);return ExactTime({a:c*v for a,v in self.terms.items()},self.constant*c)
 __rmul__=__mul__
 def bounds(self,level=0):
  lo=hi=self.constant
  for a,c in self.terms.items():
   l,h=a.bounds(level)
   if c>=0:lo+=c*l;hi+=c*h
   else:lo+=c*h;hi+=c*l
  return lo,hi
 def compare(self,other):
  d=self-self.coerce(other)
  if not d.terms:return(d.constant>0)-(d.constant<0)
  level=0
  while True:
   lo,hi=d.bounds(level)
   if lo>0:return 1
   if hi<0:return -1
   level+=1
 def __lt__(self,other):return self.compare(other)<0
 def __eq__(self,other):
  try:return self.compare(other)==0
  except(TypeError,ValueError):return False
 def __repr__(self):return f'ExactTime({len(self.terms)} exponential atoms, constant={self.constant})'

ZERO=ExactTime()
def exponential_time(rng=None):return LazyExp(rng).time()
