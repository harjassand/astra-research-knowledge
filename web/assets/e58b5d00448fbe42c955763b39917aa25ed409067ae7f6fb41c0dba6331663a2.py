#!/usr/bin/env python3
"""Independent exact Hessian and fixed-state certificate; Python stdlib only.

Every interval endpoint is an integer multiple of 10^-60. Each arithmetic
operation rounds outward using integer floor/ceiling. No floating-point math
participates in the certificate. Root's reconstruction of the frozen variance
worker's witness, independently implementing Phi and its weighted transform.
"""
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path

def mat(a): return [[F(x) for x in row] for row in a]
def add(a,b): return [[a[i][j]+b[i][j] for j in range(2)] for i in range(2)]
def scale(c,a): return [[c*x for x in row] for row in a]
def mul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def trace(a): return a[0][0]+a[1][1]
def inner(a,b): return trace(mul(a,b))
P=[scale(F(1,25),mat([[9,12],[12,16]])),scale(F(1,25),mat([[16,-12],[-12,9]]))]
pi=[scale(F(1,265),mat([[9,48],[48,256]])),scale(F(1,10),mat([[1,-3],[-3,9]]))]
sigma=scale(F(1,17),mat([[1,0],[0,16]]))
ident=mat([[1,0],[0,1]])
def phi(a): return add(scale(inner(P[0],a),pi[0]),scale(inner(P[1],a),pi[1]))
D=mat([[1,0],[0,2]])
Di=mat([[1,0],[0,F(1,2)]])
def trans(a): return mul(mul(Di,phi(mul(mul(D,a),D))),Di)

assert add(P[0],P[1])==ident
assert phi(sigma)==sigma
for p,z in zip(P,pi):
    assert mul(p,p)==p and trace(z)==1 and z[0][0]*z[1][1]-z[0][1]*z[1][0]==0
    ss=mat([[1,0],[0,4]])
    assert scale(F(1,17),mul(mul(ss,p),ss))==scale(inner(sigma,p),z)

X=scale(F(1,17),mat([[-4,1],[1,4]]))
Q=mat([[-2,F(1,5)],[F(1,5),F(1,2)]])
E2=F(1,17)*inner(Q,add(Q,scale(-1,trans(Q))))
Delta=add(X,scale(-1,phi(X)))
Ja=inner(Delta,mat([[-4,0],[0,F(1,4)]]))
Jb=inner(Delta,mat([[0,F(4,15)],[F(4,15),0]]))
assert E2==F(1088273,4505000)
assert Ja==F(2559,2650) and Jb==-F(8,337875)
assert Ja-4*E2==-F(349,563125)

S=10**60
def ceildiv(a,b): return -((-a)//b)
class IV:
    def __init__(self,lo,hi):
        assert lo<=hi
        self.lo,self.hi=lo,hi
    @classmethod
    def exact(cls,x):
        x=F(x); return cls(x.numerator*S//x.denominator,ceildiv(x.numerator*S,x.denominator))
    def __add__(a,b):
        if not isinstance(b,IV): b=IV.exact(b)
        return IV(a.lo+b.lo,a.hi+b.hi)
    __radd__=__add__
    def __neg__(a): return IV(-a.hi,-a.lo)
    def __sub__(a,b): return a+-convert(b)
    def __rsub__(a,b): return convert(b)+-a
    def __mul__(a,b):
        b=convert(b); v=[a.lo*b.lo,a.lo*b.hi,a.hi*b.lo,a.hi*b.hi]
        return IV(min(v)//S,ceildiv(max(v),S))
    __rmul__=__mul__
    def __truediv__(a,b):
        b=convert(b); assert b.lo>0
        return a*IV(S*S//b.hi,ceildiv(S*S,b.lo))
    def sqrt(a):
        assert a.lo>=0
        lo=isqrt(a.lo*S); hi=isqrt(a.hi*S)
        if hi*hi<a.hi*S: hi+=1
        return IV(lo,hi)
    def export(a): return {'lower_numerator':str(a.lo),'upper_numerator':str(a.hi),'denominator':str(S)}
def convert(x): return x if isinstance(x,IV) else IV.exact(x)
def ivmat(a): return [[convert(x) for x in row] for row in a]
def atanh_over_x(x,N=600):
    # sum_{k=0}^{N-1} x^(2k)/(2k+1), with geometric upper tail.
    assert 0<=x.lo<=x.hi<S
    z=x*x; power=IV.exact(1); ans=IV.exact(0)
    for k in range(N):
        ans=ans+power/(2*k+1)
        power=power*z
    tail=power/((2*N+1)*(1-z))
    return IV(ans.lo,ans.hi+tail.hi)

log2=F(2,3)*atanh_over_x(IV.exact(F(1,3)))
cases=[]
for epsilon in [F(1,100),F(1,1000),F(1,10000)]:
    rho=add(sigma,scale(epsilon,X))
    det=rho[0][0]*rho[1][1]-rho[0][1]*rho[1][0]
    assert det>0 and trace(rho)==1
    delta=add(rho,scale(-1,phi(rho)))
    assert trace(delta)==0
    r=IV.exact((rho[0][0]-rho[1][1])**2+4*rho[0][1]**2).sqrt()
    J=atanh_over_x(r)*inner(delta,add(scale(2,rho),scale(-1,ident)))-delta[1][1]*4*log2
    u=IV.exact(det).sqrt(); v=(1+2*u).sqrt()
    q=[[ (IV.exact(rho[i][j])+(u if i==j else 0))/v for j in range(2)] for i in range(2)]
    E=1-inner(q,trans(q))
    gap=J-4*E
    assert E.lo>0 and gap.hi<0
    cases.append({'epsilon':str(epsilon),'rho':[[str(x) for x in row] for row in rho],
                  'J':J.export(),'E':E.export(),'J_minus_4E':gap.export(),
                  'negative_upper_bound_verified':True})

result={'scope':'Exact internally reconstructed rational interval certificate, not a proof-assistant formalization.',
        'arithmetic':'Python integer/Fraction only; fixed-point outward rounding at 10^-60; 600-term atanh series with positive geometric tail.',
        'E_second_coefficient':str(E2),'J_second_coefficients_constant_log2':[str(Ja),str(Jb)],
        'gap_second_coefficients_constant_log2':[str(Ja-4*E2),str(Jb)],
        'log2':log2.export(),'fixed_states':cases}
out=Path(__file__).with_suffix('.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
