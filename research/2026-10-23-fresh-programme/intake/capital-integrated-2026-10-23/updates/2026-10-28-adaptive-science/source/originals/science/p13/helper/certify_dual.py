"""Exact-rational interval certificate for the binding-cap dual multipliers.

Only Python standard-library integer/Fraction operations are used. The sinh
tail is bounded by a geometric series after 80 positive Taylor terms.
"""
from fractions import Fraction as Q
from math import isqrt, factorial
from pathlib import Path

class I:
    def __init__(self, lo, hi=None):
        self.lo=Q(lo); self.hi=Q(lo if hi is None else hi)
        assert self.lo<=self.hi
    def __add__(self,y):
        y=iv(y); return I(self.lo+y.lo,self.hi+y.hi)
    __radd__=__add__
    def __neg__(self): return I(-self.hi,-self.lo)
    def __sub__(self,y): return self+-iv(y)
    def __rsub__(self,y): return iv(y)+-self
    def __mul__(self,y):
        y=iv(y); z=[self.lo*y.lo,self.lo*y.hi,self.hi*y.lo,self.hi*y.hi]
        return I(min(z),max(z))
    __rmul__=__mul__
    def __truediv__(self,y):
        y=iv(y); assert y.lo*y.hi>0
        return self*I(1/y.hi,1/y.lo)
    def __rtruediv__(self,y): return iv(y)/self
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        ans=I(1)
        for _ in range(n):ans=ans*self
        return ans
    def outward(self, digits=36):
        scale=10**digits
        left=(self.lo.numerator*scale)//self.lo.denominator
        right=-((-self.hi.numerator*scale)//self.hi.denominator)
        return f'[{Q(left,scale)}, {Q(right,scale)}]'

def iv(x): return x if isinstance(x,I) else I(x)

def sqrt_int(n,digits=65):
    scale=10**digits
    a=isqrt(n*scale*scale)
    assert a*a<=n*scale*scale<(a+1)*(a+1)
    return I(Q(a,scale),Q(a+1,scale))

def sinh_point(x,n=80):
    assert 0<=x<=4
    term=x; total=term
    for j in range(1,n):
        term*=x*x/Q((2*j)*(2*j+1))
        total+=term
    first_omitted=term*x*x/Q((2*n)*(2*n+1))
    ratio=x*x/Q((2*n+2)*(2*n+3))
    assert ratio<1
    return total,total+first_omitted/(1-ratio)

def sinh(x):
    assert x.lo>=0
    low=sinh_point(x.lo)[0]; high=sinh_point(x.hi)[1]
    return I(low,high)

sqrt5=sqrt_int(5); p=sqrt5-1;r=2*sqrt_int(2);s=sqrt5+1
nodes=[p*p,r*r,s*s]
H=[w**5/(sinh(w)**2) for w in (p,r,s)]
coefs=[I(0),I(0),I(0)]
for i in range(3):
    j,k=[a for a in range(3) if a!=i]
    den=(nodes[i]-nodes[j])*(nodes[i]-nodes[k])
    term=H[i]/den
    coefs[0]+=term*nodes[j]*nodes[k]
    coefs[1]-=term*(nodes[j]+nodes[k])
    coefs[2]+=term
eta=coefs[0]; lam=-coefs[1];mu=-coefs[2]/2
assert lam.hi<0 and mu.lo>0 and eta.lo>0
B1=lam-eta/3
B2=lam+6*mu-2*eta/15
B3=lam+15*mu-eta/14
B4=lam+28*mu-2*eta/45
B5=lam+45*mu-eta/33
assert B1.hi<0 and B2.hi<0 and B3.hi<0 and B4.hi<0
assert B5.lo>0
lines=[
    'Exact Fraction interval computation; no binary floating arithmetic.',
    'sqrt intervals: decimal grid with 65 digits and integer isqrt proof.',
    'sinh: 80 positive Taylor terms; geometric tail ratio bound.',
]
for name,value in [('p',p),('r',r),('s',s),('lambda',lam),('mu',mu),('eta',eta),
                   ('B1',B1),('B2',B2),('B3',B3),('B4',B4),('B5',B5)]:
    lines.append(f'{name} {value.outward()}')
lines.append('PASS: lambda<0<mu, eta>0, and even coefficient transition B4<0<B5.')
text='\n'.join(lines)+'\n'
(Path(__file__).parent/'CERTIFIED_MULTIPLIERS.txt').write_text(text)
print(text)
