"""Independent exact-Fraction interval certificate; no numerical math library.
All endpoints are exact rationals. Arithmetic is rounded OUTWARD to 2^-180.
sqrt uses integer isqrt; log uses a positive atanh series and an explicit tail.
The Fourier kernel is evaluated algebraically as log(r)/(sqrt(r)-1/sqrt(r)).
Real basis X, J=iY, Z has the identical Pauli transfer entries because the
real Hermiticity-preserving maps preserve symmetric/antisymmetric sectors.
"""
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path
BITS=180; Q=1<<BITS; TERMS=80

def down(x): return F(x.numerator*Q//x.denominator,Q)
def up(x): return -down(-x)
class R:
    __slots__=('lo','hi')
    def __init__(self,lo=0,hi=None):
        if isinstance(lo,R): self.lo,self.hi=lo.lo,lo.hi; return
        self.lo,self.hi=F(lo),F(lo if hi is None else hi)
        assert self.lo<=self.hi
    @staticmethod
    def hull(lo,hi): return R(down(lo),up(hi))
    def __add__(self,b):
        b=R(b); return R.hull(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self): return R(-self.hi,-self.lo)
    def __sub__(self,b): return self+-R(b)
    def __rsub__(self,b): return R(b)+-self
    def __mul__(self,b):
        b=R(b); x=[self.lo*b.lo,self.lo*b.hi,self.hi*b.lo,self.hi*b.hi]
        return R.hull(min(x),max(x))
    __rmul__=__mul__
    def inv(self):
        assert not self.lo<=0<=self.hi, (self.lo,self.hi)
        return R.hull(1/self.hi,1/self.lo)
    def __truediv__(self,b): return self*R(b).inv()
    def __rtruediv__(self,b): return R(b)*self.inv()
    def __abs__(self):
        return R(0 if self.lo<=0<=self.hi else min(abs(self.lo),abs(self.hi)),max(abs(self.lo),abs(self.hi)))
    def contains(self,x): return self.lo<=F(x)<=self.hi
    def js(self): return {'lower':str(self.lo),'upper':str(self.hi),'midpoint_float':float((self.lo+self.hi)/2),'width_float':float(self.hi-self.lo)}

def sqrt(x):
    x=R(x); assert x.lo>=0
    lo=isqrt((x.lo.numerator*Q*Q)//x.lo.denominator)
    hi=isqrt((x.hi.numerator*Q*Q)//x.hi.denominator)
    if F(hi*hi,Q*Q)<x.hi: hi+=1
    return R(F(lo,Q),F(hi,Q))

def log_reduced(z):
    assert 1<=z<=2
    t=(R(z)-1)/(R(z)+1); power=t; t2=t*t; total=R(0)
    for n in range(TERMS):
        total+=power/F(2*n+1); power*=t2
    tail=2*F(1,3)**(2*TERMS+1)/((2*TERMS+1)*(1-F(1,9)))
    return 2*total+R(0,tail)
LN2=log_reduced(F(2))
def log_point(x):
    assert x>0
    z=x; k=0
    while z<1: z*=2; k-=1
    while z>2: z/=2; k+=1
    return log_reduced(z)+k*LN2

def log(x):
    x=R(x); assert x.lo>0
    return R(log_point(x.lo).lo,log_point(x.hi).hi)

def mat(x):return [[R(v) for v in row] for row in x]
def zero():return mat([[0,0],[0,0]])
def add(a,b):return [[a[i][j]+b[i][j] for j in range(2)] for i in range(2)]
def scale(a,c):return [[c*v for v in row] for row in a]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def trans(a):return [[a[j][i] for j in range(2)] for i in range(2)]
def sums(xs):
    out=zero()
    for x in xs:out=add(out,x)
    return out
I=mat([[1,0],[0,1]]); X=mat([[0,1],[1,0]]); J=mat([[0,1],[-1,0]]); Z=mat([[1,0],[0,-1]])
sigma=mat([[F(1,2),F(1,4)],[F(1,4),F(1,2)]])
K=[[[R(0),sqrt(F(1,2))],[R(1),R(0)]],[[R(0),R(0)],[R(0),sqrt(F(1,2))]]]
def phi(a):return sums(mul(mul(k,a),trans(k)) for k in K)
def adj(a):return sums(mul(mul(trans(k),a),k) for k in K)
s=[R(F(1,4)),R(F(3,4))]; P=[scale(add(I,scale(X,-1)),F(1,2)),scale(add(I,X),F(1,2))]
nu=phi(sigma); t=sqrt(6)/8; v=[R(F(1,2))-t,R(F(1,2))+t]
Qp=[scale(add(I,scale(add(nu,scale(I,-F(1,2))),-1/t)),F(1,2)),scale(add(I,scale(add(nu,scale(I,-F(1,2))),1/t)),F(1,2))]
ss=mat([[(sqrt(3)+1)/4,(sqrt(3)-1)/4],[(sqrt(3)-1)/4,(sqrt(3)+1)/4]])
ni=sums(scale(Qp[a],1/sqrt(v[a])) for a in range(2))
def r0(a):return mul(mul(ss,adj(mul(mul(ni,a),ni))),ss)
weights={}
for i in range(2):
 for j in range(2):
  for a in range(2):
   for b in range(2):
    if i==j and a==b:weights[i,j,a,b]=R(1)
    else:
     ratio=s[i]*v[b]/(s[j]*v[a]); rt=sqrt(ratio)
     weights[i,j,a,b]=log(ratio)/(rt-1/rt)
     assert weights[i,j,a,b].lo>0 and weights[i,j,a,b].hi<1

def rb(a):
 out=zero()
 for (i,j,c,d),weight in weights.items():
    out=add(out,scale(mul(mul(P[i],r0(mul(mul(Qp[c],a),Qp[d]))),P[j]),weight))
 return out
B=[scale(mul(mul(ss,mat([[int(u==j and w==j) for w in range(2)] for u in range(2)])),ss),2) for j in range(2)]
def eb(a):return add(scale(B[0],a[0][0]),scale(B[1],a[1][1]))
def coeffs(a):return [(a[0][1]+a[1][0])/2,(a[0][1]-a[1][0])/2,(a[0][0]-a[1][1])/2]
M=[[R(0) for j in range(3)] for i in range(3)];N=[[R(0) for j in range(3)] for i in range(3)]
for j,p in enumerate([X,J,Z]):
    cm=coeffs(add(p,scale(rb(phi(p)),-1)));cn=coeffs(add(p,scale(eb(p),-1)))
    for i in range(3):M[i][j]=cm[i];N[i][j]=cn[i]
# Mixed symmetric/antisymmetric coefficients vanish EXACTLY; validate interval inclusion.
for a in [M,N]:
 for i,j in [(0,1),(1,0),(1,2),(2,1)]:
    assert a[i][j].contains(0); a[i][j]=R(0)
# Instead of a generic adjugate use the independent 2x2 symmetric-sector inverse.
q=M[0][0]*M[2][2]-M[0][2]*M[2][0]
det=q*M[1][1]; assert det.lo>0
inv=[[M[2][2]/q,R(0),-M[0][2]/q],[R(0),1/M[1][1],R(0)],[-M[2][0]/q,R(0),M[0][0]/q]]
T=[[sum(N[i][k]*inv[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
bound=sum(abs(x) for row in T for x in row);assert bound.hi<5
# Check complete deficit factorization on real matrix units, including traceful ones.
residuals=[]
def linear(a):
    c=coeffs(a); out=zero()
    for i,p in enumerate([X,J,Z]):out=add(out,scale(p,sum(T[i][j]*c[j] for j in range(3))))
    return out
for a in range(2):
 for b in range(2):
    e=mat([[int(i==a and j==b) for j in range(2)] for i in range(2)])
    r=add(add(e,scale(eb(e),-1)),scale(linear(add(e,scale(rb(phi(e)),-1))),-1))
    for row in r:
     for x in row:assert x.contains(0);residuals.append(float(x.hi-x.lo))
for f in [lambda a:rb(phi(a)),eb]:
    r=add(f(sigma),scale(sigma,-1))
    for row in r:
     for x in row:assert x.contains(0)
# Cross-check author decimal certificate against independently bounded quantities.
author=json.loads((Path(__file__).parent/'source_snapshot/INTERVAL_CERTIFICATE.json').read_text())
def parse(text):return [F(x.strip()) for x in text.strip('[]').split(',')]
for ours,text in [(det,author['determinant_interval']),(bound,author['entry_l1_interval'])]+[(T[i][j],author['transfer_matrix_intervals'][i][j]) for i in range(3) for j in range(3)]:
    lo,hi=parse(text); assert lo<=ours.lo<=ours.hi<=hi
out={'method':'exact Fraction arithmetic, outward dyadic rounding, integer sqrt, log positive series with explicit tail; no mpmath, numpy, scipy, or floating certificate','bits':BITS,'log_terms':TERMS,'detM':det.js(),'T':[[x.js() for x in row] for row in T],'entry_l1':bound.js(),'strict_upper_bound':5,'all_independent_intervals_inside_author_intervals':True,'max_factorization_interval_width':max(residuals),'passed':True}
(Path(__file__).parent/'RATIONAL_INTERVAL_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['method','bits','entry_l1','strict_upper_bound','passed']},indent=2))
