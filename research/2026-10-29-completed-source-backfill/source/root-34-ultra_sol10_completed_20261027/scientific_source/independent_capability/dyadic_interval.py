"""Fixed-scale directed intervals using only exact Python integer arithmetic.

One precision per process. Every arithmetic enclosure is independently rounded
down/up at scale 2**BITS; no floating rounding assumption is used.
"""
from fractions import Fraction as Q

class Ball:
    BITS=512;SCALE=1<<512;operations=0;max_stored_bits=0;max_intermediate_bits=0
    @classmethod
    def configure(cls,bits):
        cls.BITS=bits;cls.SCALE=1<<bits;cls.operations=0
        cls.max_stored_bits=cls.max_intermediate_bits=0
    def __init__(self,lo,hi):
        assert lo<=hi
        self.lo=int(lo);self.hi=int(hi)
        type(self).max_stored_bits=max(type(self).max_stored_bits,abs(self.lo).bit_length(),abs(self.hi).bit_length())
    @classmethod
    def exact(cls,x):
        if isinstance(x,cls):return x
        if not isinstance(x,Q):x=Q(str(x))
        a=x.numerator*cls.SCALE;b=x.denominator
        cls.max_intermediate_bits=max(cls.max_intermediate_bits,abs(a).bit_length(),b.bit_length())
        return cls(a//b,-((-a)//b))
    @classmethod
    def track(cls,*vals):
        cls.operations+=1
        cls.max_intermediate_bits=max([cls.max_intermediate_bits]+[abs(v).bit_length() for v in vals])
    def __add__(self,y):
        y=self.exact(y);self.track(self.lo+y.lo,self.hi+y.hi)
        return Ball(self.lo+y.lo,self.hi+y.hi)
    __radd__=__add__
    def __neg__(self):return Ball(-self.hi,-self.lo)
    def __sub__(self,y):return self+(-self.exact(y))
    def __rsub__(self,y):return self.exact(y)+(-self)
    def __mul__(self,y):
        y=self.exact(y);v=[a*b for a in [self.lo,self.hi] for b in [y.lo,y.hi]]
        self.track(*v);lo=min(v);hi=max(v)
        return Ball(lo//self.SCALE,-((-hi)//self.SCALE))
    __rmul__=__mul__
    def __truediv__(self,y):
        y=self.exact(y);assert not y.lo<=0<=y.hi
        nums=[a*self.SCALE for a in [self.lo,self.hi]]
        self.track(*nums,y.lo,y.hi)
        lows=[a//b for a in nums for b in [y.lo,y.hi]]
        highs=[-((-a)//b) for a in nums for b in [y.lo,y.hi]]
        return Ball(min(lows),max(highs))
    def __rtruediv__(self,y):return self.exact(y)/self
    def __pow__(self,k):
        assert isinstance(k,int) and k>=0
        out=self.exact(1);base=self
        while k:
            if k&1:out=out*base
            k//=2
            if k:base=base*base
        return out
    def __bool__(self):return self.lo!=0 or self.hi!=0
    def __gt__(self,y):return self.lo>self.exact(y).hi
    def __le__(self,y):return self.hi<=self.exact(y).lo
    def __float__(self):return (self.lo+self.hi)/(2*self.SCALE)
    def contains(self,x):
        x=Q(x)
        return self.lo*x.denominator<=x.numerator*self.SCALE<=self.hi*x.denominator
    def record(self):
        return {'lower_numerator':str(self.lo),'upper_numerator':str(self.hi),
                'denominator_power_of_two':self.BITS,'midpoint_float':float(self),
                'width_float':(self.hi-self.lo)/self.SCALE}
