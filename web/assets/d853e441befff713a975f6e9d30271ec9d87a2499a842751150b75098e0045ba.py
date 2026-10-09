"""Exact rational-interval certificate for a finite CMI counterexample.

Uses only Python's standard library. No floating-point arithmetic is used
in the mathematical assertions. This checks the stated finite witness,
not the general theorem and not historical novelty.

Logarithms: range reduction by powers of two, then the atanh series
  log z = 2 sum_{j=0}^{N-1} t^(2j+1)/(2j+1) + R,
  t=(z-1)/(z+1), 0<=R<=2t^(2N+1)/((2N+1)(1-t^2)), 1<=z<=2.
Square roots: integer square root of a rational scaled by 2^(2B).
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path

@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F
    def __post_init__(self) -> None:
        if self.lo > self.hi: raise ValueError('Invalid interval')
    @staticmethod
    def of(x) -> 'Interval':
        return x if isinstance(x, Interval) else Interval(F(x), F(x))
    def __add__(self, other):
        b=self.of(other);return Interval(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self): return Interval(-self.hi,-self.lo)
    def __sub__(self,other): return self+-self.of(other)
    def __rsub__(self,other): return self.of(other)+-self
    def __mul__(self,other):
        b=self.of(other);v=[self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi]
        return Interval(min(v),max(v))
    __rmul__=__mul__
    def reciprocal(self):
        if self.lo<=0<=self.hi: raise ZeroDivisionError('Interval contains zero')
        return Interval(1/self.hi,1/self.lo)
    def __truediv__(self,other):return self*self.of(other).reciprocal()
    def __rtruediv__(self,other):return self.of(other)*self.reciprocal()

NTERMS=24
ROOT_BITS=100

def unit_log_bounds(z:F)->Interval:
    if not 1<=z<=2: raise ValueError('Range reduction failed')
    t=(z-1)/(z+1);power=t;total=F(0)
    for j in range(NTERMS):
        total+=2*power/(2*j+1)
        power*=t*t
    rem=2*power/((2*NTERMS+1)*(1-t*t))
    return Interval(total,total+rem)

LOG2=unit_log_bounds(F(2))

def log_endpoint(z:F)->Interval:
    if z<=0:raise ValueError('Logarithm requires positive argument')
    shift=0
    while z<1:z*=2;shift-=1
    while z>2:z/=2;shift+=1
    return unit_log_bounds(z)+shift*LOG2

def log_interval(z:Interval)->Interval:
    return Interval(log_endpoint(z.lo).lo,log_endpoint(z.hi).hi)

def sqrt_endpoint(z:F)->Interval:
    if z<0:raise ValueError('Negative square root')
    scale=1<<ROOT_BITS
    m=isqrt((z.numerator*scale*scale)//z.denominator)
    lo=F(m,scale)
    hi=lo if m*m*z.denominator==z.numerator*scale*scale else F(m+1,scale)
    assert lo*lo<=z<=hi*hi
    return Interval(lo,hi)

def xlog(z)->Interval:
    z=Interval.of(z)
    if z.lo==z.hi==0:return Interval.of(0)
    return z*log_interval(z)

def f_input(p:F,s:F)->Interval:
    q=1-p
    return 2*xlog(q/2)+xlog(p)-xlog(q*(1-s))-xlog(p+q*s)

def f_output(p:F,s:F)->Interval:
    q=1-p
    root=sqrt_endpoint((1+p)**2-8*p*q*(1-s))
    low=(1+p-root)/8;high=(1+p+root)/8
    return (2*(xlog(low)+xlog(high))+xlog(q*(1-s)/2)+xlog(q*s/2)
            -xlog(q*(1-s))-xlog(p+q*s))

def decimal_outer(iv:Interval, digits:int=18)->dict:
    scale=10**digits
    low=(iv.lo.numerator*scale)//iv.lo.denominator
    high=-((-iv.hi.numerator*scale)//iv.hi.denominator)
    def show(n):
        sign='-' if n<0 else '';n=abs(n)
        return f'{sign}{n//scale}.{n%scale:0{digits}d}'
    return {'lower':show(low),'upper':show(high)}

def certify()->dict:
    p,s,h=F(1,10),F(1,100),F(1,100)
    cmis=[]
    for fun in (f_input,f_output):
        cmis.append((fun(p+h,s)+fun(p-h,s))/2-fun(p,s))
    ix,iy=cmis
    assert ix.lo>0
    ratio=iy/ix
    assert ratio.lo>F(9,10)
    assert ratio.hi<1
    # Ordinary classical coefficient is exactly 1/2 (proved in manuscript).
    assert iy.lo>F(1,2)*ix.hi
    return {
      'status':'PASS',
      'scope':'Exact finite rational-interval witness only; not formal verification of the general theorem.',
      'parameters':{'p':str(p),'s':str(s),'h':str(h)},
      'channel':'W(y|x)=1/2 for y!=x and 0 otherwise, x,y in {0,1,2}',
      'reference_dimension':2,'auxiliary':'uniform classical bit U',
      'logarithm':'natural','log_series_terms':NTERMS,'sqrt_binary_precision':ROOT_BITS,
      'input_CMI':decimal_outer(ix),'output_CMI':decimal_outer(iy),
      'ratio':decimal_outer(ratio),
      'exact_assertions':['I(U;X|R)>0','I(U;Y|R) > (9/10) I(U;X|R)',
                          'I(U;Y|R) < I(U;X|R)',
                          'I(U;Y|R) > (1/2) I(U;X|R)'],
      'method':'Fraction arithmetic with proved logarithm remainder and integer square-root enclosures; decimal endpoints rounded outward.'
    }

if __name__=='__main__':
    result=certify()
    target=Path(__file__).with_name('exact_triangle_certificate.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
