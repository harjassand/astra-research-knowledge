#!/usr/local/bin/python3
"""Independent exact-rational interval audit of P84; no endpoint imports.

All interval arithmetic is fractions.Fraction. Square-root endpoints use
integer isqrt; pi is enclosed by Machin's identity and alternating sums.
Decimal text is display only. The final inequalities are exact predicates.
"""
from fractions import Fraction as F
from math import isqrt
from decimal import Decimal, localcontext
from pathlib import Path
import json

class Q:
    def __init__(self, a, b=None):
        if isinstance(a, Q): self.a,self.b=a.a,a.b
        else: self.a,self.b=F(a),F(a if b is None else b)
        assert self.a <= self.b
    def __add__(self, x):
        x=Q(x); return Q(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self):return Q(-self.b,-self.a)
    def __sub__(self,x):return self+-Q(x)
    def __rsub__(self,x):return Q(x)+-self
    def __mul__(self,x):
        x=Q(x); v=[self.a*x.a,self.a*x.b,self.b*x.a,self.b*x.b]
        return Q(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,x):
        x=Q(x);assert x.a*x.b>0
        return self*Q(1/x.b,1/x.a)
    def __rtruediv__(self,x):return Q(x)/self
    def __pow__(self,n):
        if n==2:
            return Q(0 if self.a<=0<=self.b else min(self.a*self.a,self.b*self.b),
                     max(self.a*self.a,self.b*self.b))
        assert n>=0
        r=Q(1)
        for _ in range(n):r=r*self
        return r
    def sqrt(self):
        assert self.a>=0
        scale=10**55
        lo=F(isqrt(self.a.numerator*scale*scale//self.a.denominator),scale)
        hi=F(isqrt(self.b.numerator*scale*scale//self.b.denominator)+1,scale)
        return Q(lo,hi)
    def absolute(self):
        return Q(0 if self.a<=0<=self.b else min(abs(self.a),abs(self.b)),
                 max(abs(self.a),abs(self.b)))
    def text(self):
        with localcontext() as c:
            c.prec=25
            return [str(Decimal(x.numerator)/Decimal(x.denominator)) for x in (self.a,self.b)]

def atan_inv(q,n):
    terms=[F((-1)**j,(2*j+1)*q**(2*j+1)) for j in range(n)]
    s=sum(terms,F(0));nextterm=F((-1)**n,(2*n+1)*q**(2*n+1))
    return Q(min(s,s+nextterm),max(s,s+nextterm))

pi=16*atan_inv(5,60)-4*atan_inv(239,20)
kp,km=Q(F(2,25)),Q(F(1,25))
ap=3-2*kp/(2+(3+4*kp).sqrt())
am=3+2*km/(2+(3+4*km).sqrt())
def weight(e,c,k):
    d=(e-c).absolute()
    return 1/(1+2*k*(-1+d/(d*d-1).sqrt()))
wp,wm=weight(ap,5,kp),weight(am,1,km)
E=Q('5.9785','5.9787')
def faa(e):return wp**2/(2*ap-e)+wm**2/(2*am-e)
def cp(e):return 2*wp*(1-wp)/(ap+4-e)+(1-wp)**2/(8-e)
def cm(e):return 2*wm*(1-wm)/(e-am-2)+(1-wm)**2/(e-4)
left=faa(Q('5.9785'))+cp(Q('5.9785'))
right=faa(Q('5.9787'))-cm(Q('5.9787'))
assert left.b<0<right.a
def bathbelow(z,c):
    d=c-z;return 2/(d+(d*d-1).sqrt())
def bathabove(z,c):
    d=z-c;return -2/(d+(d*d-1).sqrt())
def mp(z):return 1/(3-z-kp*bathbelow(z,5))
def mm(z):return 1/(3-z-km*bathabove(z,1))
def density(x,c,k):
    u=x-c;v2=1-u**2
    return 2*k*v2.sqrt()/(pi*((3-x+2*k*u)**2+4*k*k*v2))
J1,J2=Q('4.1995','4.2005'),Q('5.7995','5.8005')
W1,W2=mp(E-J1)+mm(J1),mp(E-J2)+mm(J2)
gap=W2.a-W1.b
m1=F(1,1000)*density(J1,5,kp)*density(E-J1,1,km)
m2=F(1,1000)*density(J2,5,kp)*density(E-J2,1,km)
dup=wp**2/(2*ap-E)**2+2*wp*(1-wp)/(ap+4-E)**2+(1-wp)**2/(8-E)**2
dum=wm**2/(2*am-E)**2+2*wm*(1-wm)/(E-am-2)**2+(1-wm)**2/(E-4)**2
N2=2/(dup+dum).b
lower=N2*(m1.a*m2.a/(m1.a+m2.a))*gap**2
assert gap>0 and m1.a>0 and m2.a>0
assert lower>F(4,10**16)
out=dict(method='Exact Fraction intervals; integer square roots; Machin alternating-series pi enclosure',
         Eplus=ap.text(),Eminus=am.text(),pi=pi.text(),
         F_left_upper=left.text(),F_right_lower=right.text(),
         W1=W1.text(),W2=W2.text(),
         shell_mass_lower=[Q(m1.a).text(),Q(m2.a).text()],
         normalizer_squared_lower=Q(N2).text(),rho_lower=Q(lower).text(),
         exact_rational_predicate_rho_gt_4e_minus16=True)
Path(__file__).with_name('rational_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
