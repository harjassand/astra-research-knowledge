#!/usr/local/bin/python3
"""Independent exact-rational interval verification of P84's lower bound.

No candidate imports, mpmath, floating-point comparisons, or quadratures.
Square roots are enclosed with integer isqrt; pi uses Machin's formula and
alternating-series rational remainders. Decimal strings are outward rounded.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json

SCALE = 10**45


class I:
    def __init__(self,a,b=None):
        if isinstance(a,I): self.lo,self.hi=a.lo,a.hi;return
        self.lo=F(a);self.hi=F(a if b is None else b)
        assert self.lo<=self.hi
    def __add__(self,o):
        o=I(o);return I(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,o):return self+-I(o)
    def __rsub__(self,o):return I(o)+-self
    def __mul__(self,o):
        o=I(o);p=[a*b for a in [self.lo,self.hi] for b in [o.lo,o.hi]]
        return I(min(p),max(p))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=I(o);assert o.lo*o.hi>0
        return self*I(1/o.hi,1/o.lo)
    def __rtruediv__(self,o):return I(o)/self
    def __pow__(self,n):
        assert n==2
        if self.lo>=0:return I(self.lo**2,self.hi**2)
        if self.hi<=0:return I(self.hi**2,self.lo**2)
        return I(0,max(self.lo**2,self.hi**2))
    def sqrt(self):
        assert self.lo>=0
        def lower(q):return F(isqrt(q.numerator*SCALE*SCALE//q.denominator),SCALE)
        return I(lower(self.lo),lower(self.hi)+F(1,SCALE))


def atan_small(q,n):
    assert n%2==0
    q=F(q)
    s=sum(((-1)**j*q**(2*j+1)/F(2*j+1) for j in range(n)),F(0))
    return I(s,s+q**(2*n+1)/F(2*n+1))


def decimal_bound(q,lower=True,n=60):
    q=F(q);s=10**n
    z=q.numerator*s//q.denominator
    if not lower and F(z,s)<q:z+=1
    sign='-' if z<0 else ''
    z=abs(z)
    return f'{sign}{z//s}.{z%s:0{n}d}'


def desc(i):
    i=I(i)
    return [decimal_bound(i.lo),decimal_bound(i.hi,False)]


pi=16*atan_small(F(1,5),80)-4*atan_small(F(1,239),24)
g=I(F(1,5));kp=2*g*g;km=g*g
ep=3-2*kp/(2+(3+4*kp).sqrt())
em=3+2*km/(2+(3+4*km).sqrt())
def atomweight(e,c,k):
    d=c-e if c==5 else e-c
    return 1/(1+2*k*(-1+d/(d*d-1).sqrt()))
zp=atomweight(ep,5,kp);zm=atomweight(em,1,km)
El=I('5.9785');Eh=I('5.9787');E=I('5.9785','5.9787')
def aa(z):return zp**2/(2*ep-z)+zm**2/(2*em-z)
Fleft=aa(El)+2*zp*(1-zp)/(ep+4-El)+(1-zp)**2/(8-El)
Fright=aa(Eh)-2*zm*(1-zm)/(Eh-em-2)-(1-zm)**2/(Eh-4)
assert Fleft.hi<0<Fright.lo
assert E.hi<ep.lo+em.lo
def rplus(z):
    d=5-z;q=2/(d+(d*d-1).sqrt())
    return 1/(3-z-kp*q)
def rminus(z):
    d=z-1;q=-2/(d+(d*d-1).sqrt())
    return 1/(3-z-km*q)
def density(x,c,k):
    u=x-c;v2=1-u*u
    return 2*k*v2.sqrt()/(pi*((3-x+2*k*u)**2+4*k*k*v2))
j1=I('4.1995','4.2005');j2=I('5.7995','5.8005')
w1=rplus(E-j1)+rminus(j1);w2=rplus(E-j2)+rminus(j2)
sep=w2.lo-w1.hi
assert sep>0
m1=I('.001')*density(j1,5,kp)*density(E-j1,1,km)
m2=I('.001')*density(j2,5,kp)*density(E-j2,1,km)
Dp=zp**2/(2*ep-E)**2+2*zp*(1-zp)/(ep+4-E)**2+(1-zp)**2/(8-E)**2
Dm=zm**2/(2*em-E)**2+2*zm*(1-zm)/(E-em-2)**2+(1-zm)**2/(E-4)**2
Nlower=2/(Dp+Dm).hi
lower=Nlower*m1.lo*m2.lo/(m1.lo+m2.lo)*sep**2
assert lower>F(4,10**16)
result={'method':'Exact rational intervals; integer-isqrt radicals; Machin pi alternating-series enclosure',
        'pi':desc(pi),'atom_plus':desc(ep),'atom_minus':desc(em),
        'F_left_upper':decimal_bound(Fleft.hi,False),'F_right_lower':decimal_bound(Fright.lo),
        'minimum_harmonic_atom_separation_from_root_interval':decimal_bound(ep.lo+em.lo-E.hi),
        'W_interval_1':desc(w1),'W_interval_2':desc(w2),
        'mass_1_lower':decimal_bound(m1.lo),'mass_2_lower':decimal_bound(m2.lo),
        'normalization_squared_lower':decimal_bound(Nlower),
        'source_separation_lower':decimal_bound(sep),
        'rho_lower_decimal_floor':decimal_bound(lower),
        'exact_comparison_rho_lower_gt_4e_minus_16':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
