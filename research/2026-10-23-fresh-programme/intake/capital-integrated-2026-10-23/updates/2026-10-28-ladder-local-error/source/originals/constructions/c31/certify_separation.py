#!/usr/local/bin/python3
"""Exact rational interval Riemann certificate; all files stay in this arm.

Only numerical enclosure step is sqrt, implemented by integer sqrt with a
rigorous 10^-36 rational bracket. Pi uses Machin's alternating series.
"""
from fractions import Fraction as F
from math import isqrt
import json, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
S=10**36
class I:
    __slots__=('a','b')
    def __init__(self,a,b=None):
        self.a=a if isinstance(a,F) else F(a)
        self.b=self.a if b is None else (b if isinstance(b,F) else F(b))
        assert self.a<=self.b
    def __add__(self,o):
        o=cv(o);return I(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self):return I(-self.b,-self.a)
    def __sub__(self,o):return self+-cv(o)
    def __rsub__(self,o):return cv(o)+-self
    def __mul__(self,o):
        o=cv(o);x=(self.a*o.a,self.a*o.b,self.b*o.a,self.b*o.b);return I(min(x),max(x))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=cv(o);assert o.a*o.b>0, (o.a,o.b)
        return self*I(1/o.b,1/o.a)
    def __rtruediv__(self,o):return cv(o)/self
    def sq(self):
        return I(0 if self.a<=0<=self.b else min(self.a*self.a,self.b*self.b),max(self.a*self.a,self.b*self.b))
    def sqrt(self):
        assert self.a>=0
        aa=isqrt(self.a.numerator*S*S//self.a.denominator)
        bb=isqrt(self.b.numerator*S*S//self.b.denominator)
        return I(F(aa,S),F(bb+1,S))
    def absolute(self):
        return I(0 if self.a<=0<=self.b else min(abs(self.a),abs(self.b)),max(abs(self.a),abs(self.b)))
    def show(self):return [float(self.a),float(self.b)]
    def exact(self):
        T=10**20
        low=(self.a.numerator*T)//self.a.denominator
        high=-((-self.b.numerator*T)//self.b.denominator)
        return [str(F(low,T)),str(F(high,T))]
def cv(x):return x if isinstance(x,I) else I(x)
def atan_inv(n,N):
    ss=sum((F((-1)**j,(2*j+1)*n**(2*j+1)) for j in range(N)),F(0))
    nex=F((-1)**N,(2*N+1)*n**(2*N+1))
    return I(min(ss,ss+nex),max(ss,ss+nex))
PI=16*atan_inv(5,60)-4*atan_inv(239,20)
class Ch:
    def __init__(self,c,k):
        self.c=c;self.k=k;a=F(3-c)
        sg=1 if a>0 else -1
        d=(a*(1-2*k)-sg*2*k*I(3+4*k).sqrt())/(1-4*k)
        self.atom=c+d
        self.mass=1/(1+k*2*(-1+d.absolute()/(d.sq()-1).sqrt()))
    def m(self,z):
        z=cv(z);d=z-self.c
        assert d.b < -1 or d.a > 1
        rt=(d.sq()-1).sqrt()
        if d.b< -1: rt=-rt
        rr=2*(-d+rt)
        return 1/(3-z-self.k*rr)
    def integrand(self,u,E):
        q=1-u.sq()
        den=(3-self.c-(1-2*self.k)*u).sq()+4*self.k*self.k*q
        rho=2*self.k*q.sqrt()/(PI*den)
        return rho*self.m(E-self.c-u)
    def L(self,E,N):
        val=self.mass*self.m(E-self.atom)
        width=F(2,N)
        ss=I(0)
        for j in range(N):
            u=I(-1+j*width,-1+(j+1)*width)
            ss+=self.integrand(u,E)*width
        return val+ss
N=int(sys.argv[1]) if len(sys.argv)>1 else 2048
p=Ch(5,F(2,25));m=Ch(1,F(1,25))
Elo=F('5.9785');Ehi=F('5.97865')
start=time.time()
lo=p.L(Elo,N)+m.L(Elo,N)
hi=p.L(Ehi,N)+m.L(Ehi,N)
atom_sum=p.atom+m.atom
assert lo.b<0,(lo.show(),N)
assert hi.a>0,(hi.show(),N)
assert Ehi<6
assert Ehi<atom_sum.a
out={'method':'exact-rational interval Riemann sums with integer-sqrt enclosure and Machin pi',
     'N_per_band':N,'root_bracket':['5.9785','5.97865'],
     'Lsum_at_lower':lo.show(),'Lsum_at_upper':hi.show(),
     'E_plus':p.atom.show(),'E_minus':m.atom.show(),
     'atom_sum':atom_sum.show(),
     'exact_E_plus':p.atom.exact(),'exact_E_minus':m.atom.exact(),
     'exact_atom_sum':atom_sum.exact(),'root_below_atom_sum_by_at_least':float(atom_sum.a-Ehi),
     'root_below_threshold_6_by_at_least':float(6-Ehi),
     'seconds':time.time()-start,
     'exact_Lsum_bounds':{'lower_test':lo.exact(),'upper_test':hi.exact()}}
(ROOT/'separation_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='exact_Lsum_bounds'},indent=2))
