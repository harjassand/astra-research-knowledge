"""Small outward-rounded rational intervals, including exp/sinh and sqrt.

Every operation is performed with exact integers/Fractions and then rounded
outwards onto a fixed decimal grid. No binary floating arithmetic is used.
"""
from fractions import Fraction as Q
from math import isqrt

SCALE=10**85

def down(x):
    x=Q(x);return Q((x.numerator*SCALE)//x.denominator,SCALE)

def up(x):
    x=Q(x);return Q(-((-x.numerator*SCALE)//x.denominator),SCALE)

class I:
    def __init__(self,lo,hi=None):
        lo,hi=Q(lo),Q(lo if hi is None else hi)
        assert lo<=hi
        self.lo,self.hi=down(lo),up(hi)
    def __add__(self,y):
        y=iv(y);return I(self.lo+y.lo,self.hi+y.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,y):return self+-iv(y)
    def __rsub__(self,y):return iv(y)+-self
    def __mul__(self,y):
        y=iv(y);v=[a*b for a in [self.lo,self.hi] for b in [y.lo,y.hi]]
        return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,y):
        y=iv(y);assert y.lo*y.hi>0
        return self*I(1/y.hi,1/y.lo)
    def __rtruediv__(self,y):return iv(y)/self
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        ans=I(1);x=self
        while n:
            if n&1:ans=ans*x
            n//=2
            if n:x=x*x
        return ans
    def decimal(self,digits=24):
        sc=10**digits
        lo=(self.lo.numerator*sc)//self.lo.denominator
        hi=-((-self.hi.numerator*sc)//self.hi.denominator)
        def fmt(x):
            sg='-' if x<0 else '';x=abs(x)
            return sg+str(x//sc)+'.'+str(x%sc).zfill(digits)
        return '['+fmt(lo)+', '+fmt(hi)+']'

def iv(x):return x if isinstance(x,I) else I(x)

def sqrt(x):
    x=iv(x);assert x.lo>=0
    def floor_sqrt(y):return isqrt((y.numerator*SCALE*SCALE)//y.denominator)
    return I(Q(floor_sqrt(x.lo),SCALE),Q(floor_sqrt(x.hi)+1,SCALE))

def exp_positive(x,n=240):
    x=iv(x);assert 0<=x.lo<=x.hi
    if x.hi>16:
        half=exp_positive(x/2,n)
        return half*half
    total=term=I(1)
    for k in range(1,n):
        term=term*x/k;total+=term
    omitted=term*x/n
    ratio=I(x.hi)/(n+1)
    assert ratio.hi<1
    return I(total.lo,(total+omitted/(1-ratio)).hi)

def exp_negative(x):return 1/exp_positive(x)

def sinh(x):
    ep=exp_positive(x)
    return (ep-1/ep)/2

def cosh(x):
    ep=exp_positive(x)
    return (ep+1/ep)/2

def pi():
    def atan(x,n=100):
        total=sum(((-1)**j)*x**(2*j+1)/Q(2*j+1) for j in range(n))
        nxt=x**(2*n+1)/Q(2*n+1)
        return I(total,total+nxt) if n%2==0 else I(total-nxt,total)
    return 16*atan(Q(1,5))-4*atan(Q(1,239))

def bose(w):return (w/sinh(w))**2

def tail_integral(a,n=55):
    """Integral_a^infinity (w/sinh(w))^2 dw, with positive-series tail."""
    a=iv(a);assert a.lo>0
    z=exp_negative(2*a)
    term=z;ans=I(0)
    for j in range(1,n+1):
        ans+=term*(2*a*a+2*a/j+Q(1,j*j))
        term=term*z
    remainder=term/(1-z)*(2*a*a+2*a/(n+1)+Q(1,(n+1)**2))
    return I(ans.lo,(ans+remainder).hi)

def full_conductance(positive_edges):
    """Edges p,r,s,..., signs -,+,-,...; acoustic starts at zero."""
    out=pi()**2/6
    for j,a in enumerate(positive_edges):out+=(-1 if j%2==0 else 1)*tail_integral(a)
    return out

def polynomial(coeff,x):
    v=Q(0)
    for c in coeff:v=v*x+c
    return v

def isolate(coeff,lo,hi,steps=260):
    lo,hi=Q(lo),Q(hi)
    sl,sh=polynomial(coeff,lo),polynomial(coeff,hi)
    assert sl*sh<0
    for _ in range(steps):
        mid=(lo+hi)/2;sm=polynomial(coeff,mid)
        if sm==0:return I(mid)
        if sm*sl>0:lo,sl=mid,sm
        else:hi,sh=mid,sm
    return I(lo,hi)
