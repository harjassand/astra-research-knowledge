"""Exact rational enclosure of one universal passive-network design.

The chosen resource input is K=1,M=2,m0=1,theta=1/2. This is an
instantiation of FAMILY_THEOREM_v2.md, not a proof by parameter sampling.
"""
from dataclasses import dataclass
from fractions import Fraction as R
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from math import isqrt
from pathlib import Path
import json

BITS=160
TERMS=100

@dataclass(frozen=True)
class I:
    lo:R
    hi:R
    def __init__(self,lo,hi=None):
        object.__setattr__(self,"lo",R(lo))
        object.__setattr__(self,"hi",R(lo if hi is None else hi))
        assert self.lo<=self.hi
    def __add__(self,b):
        b=asI(b);return I(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,b):return self+-asI(b)
    def __rsub__(self,b):return asI(b)+-self
    def __mul__(self,b):
        b=asI(b);xs=[x*y for x in (self.lo,self.hi) for y in (b.lo,b.hi)]
        return I(min(xs),max(xs))
    __rmul__=__mul__
    def __truediv__(self,b):
        b=asI(b);assert b.lo>0 or b.hi<0
        return self*I(1/b.hi,1/b.lo)
    def __rtruediv__(self,b):return asI(b)/self
    def sq(self):
        if self.lo>=0:return I(self.lo*self.lo,self.hi*self.hi)
        if self.hi<=0:return I(self.hi*self.hi,self.lo*self.lo)
        return I(0,max(self.lo*self.lo,self.hi*self.hi))
def asI(x):return x if isinstance(x,I) else I(x)

def sqrt_bounds(x):
    x=R(x);assert x>=0
    z=isqrt((x.numerator<<(2*BITS))//x.denominator)
    return R(z,1<<BITS),R(z+1,1<<BITS)
def sqrtI(x):
    x=asI(x);assert x.lo>=0
    return I(sqrt_bounds(x.lo)[0],sqrt_bounds(x.hi)[1])

def exp_bounds(x):
    x=R(x);assert 0<=x<TERMS+2
    term=total=R(1)
    for n in range(1,TERMS+1):
        term*=x/n;total+=term
    first=term*x/(TERMS+1)
    return I(total,total+first/(1-x/R(TERMS+2)))
def expI(x):
    x=asI(x);return I(exp_bounds(x.lo).lo,exp_bounds(x.hi).hi)

def kernel_scalar(x):
    x=R(x);assert x>0
    e=exp_bounds(2*x)
    # E+1/E-2 is increasing for E>1.
    dl=e.lo+1/e.lo-2
    du=e.hi+1/e.hi-2
    return I(4*x*x/du,4*x*x/dl)
def kernel(x):
    x=asI(x)
    # (x/sinh x)^2 is strictly decreasing on x>0.
    return I(kernel_scalar(x.hi).lo,kernel_scalar(x.lo).hi)
def cothI(x):
    e=expI(2*asI(x))
    return I((e.hi+1)/(e.hi-1),(e.lo+1)/(e.lo-1))
def kernel_prime(x):
    x=asI(x)
    return 2*kernel(x)/x*(1-x*cothI(x))

A=I(4);B=I(2)
def endpoint_data(r):
    r=asI(r)
    d=sqrtI((r.sq()+A-2*B).sq()+4*B*(A-B))
    s2=(r.sq()+A+d)/2
    p2=B*r.sq()/s2
    p=sqrtI(p2);s=sqrtI(s2)
    pp=r*B*(A-B)/(p*d*(s2-B))
    sp=r*(s2-B)/(s*d)
    return p,s,d,pp,sp
def derivative(r):
    r=asI(r);p,s,d,pp,sp=endpoint_data(r)
    return kernel(p)*pp+kernel(s)*sp-kernel(r)

rlo=R(2336273985489,10**12)
rhi=R(2336273985490,10**12)
dlo=derivative(rlo);dhi=derivative(rhi)
assert dlo.hi<0<dhi.lo
rbox=I(rlo,rhi)
p,s,d,pp,sp=endpoint_data(rbox)
mu=(p*kernel(p)-rbox*kernel(rbox))/(2*(rbox.sq()-p.sq()))
lam=-p*kernel(p)-2*mu*p.sq()
assert mu.lo>0>lam.hi

def Fprime(x):
    return kernel(x)+x*kernel_prime(x)+4*mu*x
fpp=Fprime(p);fpr=Fprime(rbox);fps=Fprime(s)
assert fpp.lo>0>fpr.hi
assert fps.lo>0
curvature=fpp/p*pp.sq()-fpr/rbox+fps/s*sp.sq()
assert curvature.lo>0
kbox=rbox.sq()/2

def dec(x,up=False):
    with localcontext() as ctx:
        ctx.prec=35
        ctx.rounding=ROUND_CEILING if up else ROUND_FLOOR
        return str(Decimal(x.numerator)/Decimal(x.denominator))
def show(x):
    return [dec(x.lo),dec(x.hi,True)]

out=dict(resources=dict(K=1,M=2,m0=1,theta="1/2"),
         method=dict(arithmetic="exact Fraction interval arithmetic",
                     sqrt_binary_bits=BITS,exponential_terms=TERMS,
                     exponential_remainder="geometric bound after positive Taylor sum"),
         root_interval_exact=[str(rlo),str(rhi)],
         derivative_at_lower=show(dlo),derivative_at_upper=show(dhi),
         lower_band_edge=show(p),upper_band_edge=show(s),
         internal_spring=show(kbox),lambda_interval=show(lam),mu_interval=show(mu),
         Fprime_at_lower_edge=show(fpp),Fprime_at_optical_start=show(fpr),
         Fprime_at_upper_edge=show(fps),
         exact_root_curvature_interval=show(curvature),
         interpretation="The unique global optimum has r* in this exact rational interval; j''(r*) is strictly positive.",
         status="PASS: derivative signs, proper dual quadrant, all endpoint slopes and positive local curvature are exact interval assertions.")
pout=Path(__file__).resolve().parent/"certified_design_example.json"
pout.write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))

