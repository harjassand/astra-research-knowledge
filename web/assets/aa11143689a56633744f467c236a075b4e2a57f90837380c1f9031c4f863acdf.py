"""Acquired exact coefficient layer for the higher-spin positive mixture.

Computes population/critical parameters, normalized-kernel drift/potential,
diffusion, and a certified rational 3x3 square-root approximation. It does
NOT implement Brownian paths, radial seed or normalized path reweighting.
Every code output stays in c06_s01. Cost is charged in numerical site count.
"""
from fractions import Fraction as F
from math import comb
from dataclasses import dataclass
from pathlib import Path
import json

def ceil_log2(x):
    x=F(x)
    if x<=1:return 0
    k=max(0,x.numerator.bit_length()-x.denominator.bit_length())
    while x.numerator>x.denominator*(1<<k):k+=1
    while k and x.numerator<=x.denominator*(1<<(k-1)):k-=1
    return k

def ceil_fraction(x):
    x=F(x)
    return (x.numerator+x.denominator-1)//x.denominator

def eye(k=3):return [[F(int(i==j)) for j in range(k)] for i in range(k)]
def add(a,b):return [[a[i][j]+b[i][j] for j in range(len(a))] for i in range(len(a))]
def scale(a,x):return [[v*x for v in row] for row in a]
def transpose(a):return list(map(list,zip(*a)))
def multiply(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0))
              for j in range(len(b[0]))] for i in range(len(a))]
def matvec(a,b):return [sum((x*y for x,y in zip(row,b)),F(0)) for row in a]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def outer(a,b):return [[x*y for y in b] for x in a]
def det(a):
    n=len(a)
    if n==1:return a[0][0]
    return sum(((-1)**j*a[0][j]*det([row[:j]+row[j+1:] for row in a[1:]])
                for j in range(n)),F(0))
def inverse(a):
    n=len(a); d=det(a);assert d!=0
    cof=[]
    for i in range(n):
        row=[]
        for j in range(n):
            minor=[r[:j]+r[j+1:] for k,r in enumerate(a) if k!=i]
            row.append((-1)**(i+j)*det(minor)/d)
        cof.append(row)
    return transpose(cof)
def psd(a):
    from itertools import combinations
    return all(det([[a[i][j] for j in subset] for i in subset])>=0
               for k in range(1,len(a)+1) for subset in combinations(range(len(a)),k))

def integer_s(n):
    assert n>=1
    lo,hi=0,1
    while hi**4<n**3:hi*=2
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**4>=n**3:hi=mid
        else:lo=mid
    assert hi**4>=n**3 and (hi-1)**4<n**3
    return hi

@dataclass(frozen=True)
class Population:
    # Histogram permits coefficient evaluation without repeated identical work;
    # emitting the product state still costs the NUMERICAL number of sites.
    counts:tuple
    def validate(self):
        assert self.counts and all(q>=1 and count>=1 for q,count in self.counts)
        assert len({q for q,count in self.counts})==len(self.counts)
    @property
    def n(self):return sum(count for q,count in self.counts)
    @property
    def Q(self):return sum(q*count for q,count in self.counts)
    @property
    def chi(self):return sum((F(q*(q+2)*count,12) for q,count in self.counts),F(0))
    @property
    def qmax(self):return max(q for q,count in self.counts)
    def kernel_log_derivatives(self,m):
        """Return grad(log a), Hess(a)/a without tiny product a(0)."""
        r2=dot(m,m); h=F(0); hprime=F(0)
        for q,count in self.counts:
            cs=[F(comb(q+1,2*j+1)) for j in range(q//2+1)]
            p=sum((c*r2**j for j,c in enumerate(cs)),F(0))
            dp=sum((j*c*r2**(j-1) for j,c in enumerate(cs) if j),F(0))
            ddp=sum((j*(j-1)*c*r2**(j-2) for j,c in enumerate(cs) if j>=2),F(0))
            assert p>0
            h+=count*dp/p
            hprime+=count*(ddp/p-(dp/p)**2)
        grad=[2*h*v for v in m]
        hess=add(scale(eye(),2*h),scale(outer(m,m),4*(hprime+h*h)))
        return grad,hess

def coefficients(pop,C,b,M,B,m):
    pop.validate();C=[[F(v) for v in row] for row in C];b=list(map(F,b));m=list(map(F,m))
    M,B=F(M),F(B);assert M>=0 and B>=0 and len(b)==len(m)==3
    L=2*M+1;Lambda=M+1
    assert C==transpose(C) and psd(add(C,scale(eye(),-1)))
    assert psd(add(scale(eye(),L),scale(C,-1))) and dot(b,b)<=B*B
    r0sq=1/(16*(L+1));assert dot(m,m)<=r0sq
    s=integer_s(pop.n);ss=F(s*s)
    critical=1/(2*pop.chi); t0=critical-Lambda/ss
    P=add(eye(),scale(outer(m,m),-1))
    cross=[[F(0),-m[2],m[1]],[m[2],F(0),-m[0]],[-m[1],m[0],F(0)]]
    D=add(multiply(multiply(P,C),P),scale(multiply(multiply(cross,C),transpose(cross)),-1))
    assert psd(add(D,scale(eye(),F(-3,4)))) and psd(add(scale(eye(),L),scale(D,-1)))
    u=dot(m,matvec(C,m));Pb=matvec(P,b)
    original=[F(pop.Q-1,2)*v/ss+Pb[i]/(2*s)
              for i,v in enumerate([v-u*m[i] for i,v in enumerate(matvec(C,m))])]
    grad,hess=pop.kernel_log_derivatives(m)
    extra=matvec(D,grad)
    drift=[original[i]+extra[i]/(2*ss) for i in range(3)]
    V=F(pop.Q*(pop.Q-1),4)*u/ss+F(pop.Q,4)*sum(C[i][i] for i in range(3))/ss
    V+=F(pop.Q,2)*dot(b,m)/s
    V+=dot(original,grad)+sum(D[i][j]*hess[i][j] for i in range(3) for j in range(3))/(4*ss)
    jmax=F(pop.Q,2);h=L*jmax*(jmax+1)/ss+B*jmax/s
    assert abs(V)<=h
    return {"n":pop.n,"Q":pop.Q,"s":s,"chi":pop.chi,"tcrit":critical,
       "t0":t0,"seed_time_positive":t0>0,"r0_squared":r0sq,"L":L,
       "drift":drift,"potential":V,"diffusion_D":D,
       "kernel_log_gradient":grad,"hess_a_over_a":hess,"norm_bound_h":h}

def certified_sqrt(D,L,tolerance):
    """Newton root with a rational Frobenius residual certificate.

    Requires 3/4 I<=D<=L I. X starts scalar and commutes with D. The
    deterministic cap below guarantees residual <=tol/2; no random search.
    """
    D=[[F(v) for v in row] for row in D];L=F(L);tol=F(tolerance)
    assert 0<tol<=1 and L>=1 and D==transpose(D)
    assert psd(add(D,scale(eye(),F(-3,4)))) and psd(add(scale(eye(),L),scale(D,-1)))
    a=max(1,ceil_fraction(L))
    first=ceil_log2(8*a)
    second=ceil_log2(max(1,ceil_log2(32*a/tol)))
    cap=first+second+2
    xx=scale(eye(),F(a))
    for iterations in range(cap+1):
        residual=add(multiply(xx,xx),scale(D,-1))
        frobsq=sum(v*v for row in residual for v in row)
        if frobsq<=tol*tol/4:
            return {"root":xx,"iterations":iterations,"cap":cap,
               "residual_frobenius_squared":frobsq,"operator_error_upper":tol,
               "certificate":"X commutes with D, is positive, and residual Frobenius <=tol/2; D>=3/4 I implies ||X-sqrt(D)||2<=tol."}
        xx=scale(add(xx,multiply(D,inverse(xx))),F(1,2))
    raise AssertionError("proved deterministic Newton cap violated")

def serial(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {k:serial(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)):return [serial(v) for v in value]
    return value

def main():
    pop=Population(((1,32768),(2,32768)))
    C=[[F(2),F(0),F(0)],[F(0),F(2),F(0)],[F(0),F(0),F(3,2)]]
    b=[F(1,10),F(0),F(-1,20)]
    M,B=F(1),F(1,4)
    cases=[]
    for point in ((F(0),F(0),F(0)),(F(1,100),F(-1,150),F(1,200)),
                  (F(1,12),F(1,16),F(-1,20))):
        data=coefficients(pop,C,b,M,B,point)
        assert data["seed_time_positive"]
        root=certified_sqrt(data["diffusion_D"],data["L"],F(1,2**30))
        cases.append({"point":point,"coefficients":data,"sqrt_certificate":root})
    result={"status":"PASS_EXACT_COEFFICIENT_LAYER","cases":serial(cases),
       "scope":"65536 known spin sites in a histogram, rational coefficient acquisition and certified 3x3 square roots only. No radial, Brownian, normalized path or quantum output sampler executed.",
       "cost":"Fixed-spin population operations and polynomial precision rational work; emitting all local states costs numerical n. Histogram compression does not give logarithmic-n physical output."}
    Path(__file__).with_name("higher_spin_mixture_coefficients.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":result["status"],"sites":pop.n,"cases":len(cases),
       "max_newton_iterations":max(c["sqrt_certificate"]["iterations"] for c in cases),
       "scope":result["scope"]},indent=2))

if __name__=="__main__":main()
