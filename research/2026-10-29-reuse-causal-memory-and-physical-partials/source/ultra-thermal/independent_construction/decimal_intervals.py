"""Outward decimal intervals, with correctly-rounded backend contract.

Every algebraic endpoint uses an explicit directed Context. sqrt/exp
are correctly rounded HALF_EVEN by Decimal; one adjacent number outward
therefore encloses them independently of the requested rounding mode.
No binary floating value is accepted as an exact interval endpoint.
"""
from decimal import (Decimal as D,Context,ROUND_FLOOR,ROUND_CEILING,
                     ROUND_HALF_EVEN,MAX_EMAX,MIN_EMIN,getcontext)

PRECISION=32
getcontext().prec=96
DN=Context(prec=PRECISION,rounding=ROUND_FLOOR,Emax=MAX_EMAX,Emin=MIN_EMIN)
UP=Context(prec=PRECISION,rounding=ROUND_CEILING,Emax=MAX_EMAX,Emin=MIN_EMIN)
NEAR=Context(prec=PRECISION,rounding=ROUND_HALF_EVEN,Emax=MAX_EMAX,Emin=MIN_EMIN)

class I:
    __slots__=('lo','hi')
    def __init__(self,lo,hi=None):
        assert not isinstance(lo,float)and not isinstance(hi,float)
        self.lo=D(lo);self.hi=D(lo if hi is None else hi)
        assert self.lo<=self.hi
    def __add__(self,other):
        o=as_i(other);return I(DN.add(self.lo,o.lo),UP.add(self.hi,o.hi))
    __radd__=__add__
    def __neg__(self):return I(self.hi.copy_negate(),self.lo.copy_negate())
    def __sub__(self,other):return self+-as_i(other)
    def __rsub__(self,other):return as_i(other)+-self
    def __mul__(self,other):
        o=as_i(other)
        pairs=((self.lo,o.lo),(self.lo,o.hi),(self.hi,o.lo),(self.hi,o.hi))
        return I(min(DN.multiply(a,b)for a,b in pairs),
                 max(UP.multiply(a,b)for a,b in pairs))
    __rmul__=__mul__
    def __truediv__(self,other):
        o=as_i(other);assert o.lo*o.hi>0
        return self*I(DN.divide(D(1),o.hi),UP.divide(D(1),o.lo))
    def __rtruediv__(self,other):return as_i(other)/self
    def sq(self):
        low=D(0)if self.lo<=0<=self.hi else min(DN.multiply(self.lo,self.lo),DN.multiply(self.hi,self.hi))
        return I(low,max(UP.multiply(self.lo,self.lo),UP.multiply(self.hi,self.hi)))
    def sqrt(self):
        assert self.lo>=0
        lower=D(0)if self.lo==0 else DN.next_minus(NEAR.sqrt(self.lo))
        return I(lower,UP.next_plus(NEAR.sqrt(self.hi)))
    def exp(self):
        return I(max(D(0),DN.next_minus(NEAR.exp(self.lo))),
                 UP.next_plus(NEAR.exp(self.hi)))
    def abs(self):
        return I(0,max(abs(self.lo),abs(self.hi)))if self.lo<=0<=self.hi else I(min(abs(self.lo),abs(self.hi)),max(abs(self.lo),abs(self.hi)))
    def max(self,other):
        o=as_i(other);return I(max(self.lo,o.lo),max(self.hi,o.hi))
    def min(self,other):
        o=as_i(other);return I(min(self.lo,o.lo),min(self.hi,o.hi))
    def encode(self):return [str(self.lo),str(self.hi)]

def as_i(value):return value if isinstance(value,I)else I(value)

def eigenvalues32():
    cosine=(I(2)+(I(2)+I(2).sqrt()).sqrt()).sqrt()/2
    cosines=[I(1),cosine]
    for k in range(2,17):cosines.append(2*cosine*cosines[-1]-cosines[-2])
    eigen=[]
    for k in range(2,17):
        lam=(I(2)/3)*(1-cosines[k])/(1-cosine)-1
        assert lam.lo>0
        eigen.extend([lam]*(1 if k==16 else 2))
    assert len(eigen)==29
    return eigen

EIGEN=eigenvalues32()
KAPPA=EIGEN[0]
LAM2=EIGEN[0]
LAM3=EIGEN[2]
SH=sum((1/x for x in EIGEN),I(0))
EPS=I(1)/200
LAM=-I(1)/3

def trace_shift(c):return sum((1/(x+c)for x in EIGEN),I(0))

def det_ratio(c):
    result=I(1)
    for x in EIGEN:result=result*x/(x+c)
    return result.sqrt()

def field_bounds(m,t,which):
    p=m.sq()
    f=(p-1).sq()/4+(LAM+3*p)*t/2+3*t.sq()/8
    if which in ('L','R'):
        sh=trace_shift(3*p)
        low=det_ratio(3*p)*(-f/EPS-3*sh*t/2-3*EPS*sh.sq()/4).exp()
        if which=='L':return low
        a4=p.sq()+6*p*t+3*t.sq()/2
        ar=a4.sqrt().sqrt()
        root=(ar+(ar.sq()+12*EPS*SH).sqrt())/2
        moment=root.sq().sq()
        return (1+9*moment/KAPPA.sq())/low
    assert which=='U'
    eta=(m.abs()-(2*t).sqrt()).max(0).sq()
    correction=9*p*t.sq()/(4*(LAM2+eta))+t*t.sq()/(8*(LAM3+eta))
    up1=det_ratio(eta)*(-(f-correction)/EPS).exp()
    fproj=(p-1).sq()/4+(LAM+p)*t/2+t.sq()/4
    return up1.min((-fproj/EPS).exp())
