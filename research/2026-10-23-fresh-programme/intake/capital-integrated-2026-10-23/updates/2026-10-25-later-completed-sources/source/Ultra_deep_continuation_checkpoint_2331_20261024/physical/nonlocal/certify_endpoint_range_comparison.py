"""Outward rational certificate for a common endpoint-motion comparator.

All interval endpoints are exact integers divided by SCALE.  Every operation
rounds outwards.  Positive exponential bounds use Taylor plus a geometric
tail after range reduction; pi uses Machin's identity and alternating series.
No frequency quadrature, numerical root finder, or external package is used.
"""
from fractions import Fraction as F
from math import factorial, isqrt
import json
from certify_distributed_comparisons import bose_tail_upper

SCALE=10**30


def floor_frac(x):
    return x.numerator//x.denominator


def ceil_frac(x):
    return -((-x.numerator)//x.denominator)


class I:
    def __init__(self,x=0,hi=None,*,raw=False):
        if raw:
            self.lo,self.hi=x,hi
        elif isinstance(x,I):
            self.lo,self.hi=x.lo,x.hi
        else:
            a=F(x);b=F(x if hi is None else hi)
            self.lo=floor_frac(a*SCALE)
            self.hi=ceil_frac(b*SCALE)
        assert self.lo<=self.hi

    @staticmethod
    def make(lo,hi):
        return I(lo,hi,raw=True)

    def __add__(self,other):
        o=I(other);return I.make(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__

    def __neg__(self):
        return I.make(-self.hi,-self.lo)

    def __sub__(self,other):
        return self+-I(other)

    def __rsub__(self,other):
        return I(other)+-self

    def __mul__(self,other):
        o=I(other)
        products=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi]
        return I.make(min(products)//SCALE,-((-max(products))//SCALE))
    __rmul__=__mul__

    def __truediv__(self,other):
        o=I(other)
        assert not o.lo<=0<=o.hi
        ends=[F(a*SCALE,b) for a in (self.lo,self.hi) for b in (o.lo,o.hi)]
        return I.make(floor_frac(min(ends)),ceil_frac(max(ends)))

    def __rtruediv__(self,other):
        return I(other)/self

    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        out=I(1)
        for _ in range(n):out=out*self
        return out

    def sqrt(self):
        assert self.lo>=0
        a=isqrt(self.lo*SCALE);b=isqrt(self.hi*SCALE)
        if b*b<self.hi*SCALE:b+=1
        return I.make(a,b)

    def exp(self):
        assert self.lo>=0
        x=I(self);halvings=0
        while x.hi>SCALE//2:
            x=x/2;halvings+=1
        out=term=I(1)
        order=32
        for j in range(1,order+1):
            term=term*x/j;out=out+term
        first=term*x/(order+1)
        remainder=first/(1-x/(order+2))
        out=I.make(out.lo,out.hi+remainder.hi)
        for _ in range(halvings):out=out*out
        return out

    def coth_csch(self):
        assert self.lo>0
        e=self.exp();e2=e*e
        return (e2+1)/(e2-1),2*e/(e2-1)

    def json(self):
        return [self.lo/SCALE,self.hi/SCALE]


def atan_bound(x,terms=50):
    total=sum(((-1)**j*x**(2*j+1)/F(2*j+1) for j in range(terms)),F(0))
    nextterm=(-1)**terms*x**(2*terms+1)/F(2*terms+1)
    return I(min(total,total+nextterm),max(total,total+nextterm))


PI=16*atan_bound(F(1,5))-4*atan_bound(F(1,239))
TAU=1/I(101).sqrt()


def trig_point(x,cosine=False,order=18):
    # For 0<=x<1 the alternating remainder is bounded by the next term.
    assert 0<=x<1
    if cosine:
        value=sum(((-1)**j*x**(2*j)/factorial(2*j) for j in range(order)),F(0))
        nextterm=(-1)**order*x**(2*order)/factorial(2*order)
    else:
        value=sum(((-1)**j*x**(2*j+1)/factorial(2*j+1) for j in range(order)),F(0))
        nextterm=(-1)**order*x**(2*order+1)/factorial(2*order+1)
    return min(value,value+nextterm),max(value,value+nextterm)


def trig_small(x,cosine=False):
    # Sine increases and cosine decreases on this small positive interval.
    lo,hi=F(x.lo,SCALE),F(x.hi,SCALE)
    lowpoint=trig_point(hi if cosine else lo,cosine)
    highpoint=trig_point(lo if cosine else hi,cosine)
    return I(lowpoint[0],highpoint[1])


def fejer_D(w,cosines):
    value=-I(F(100,101))*w*w
    for n,k,c in zip((1,2,3),(F(3,20),F(1,10),F(1,20)),cosines):
        z=n*TAU*w
        value=value+2*k*z*(trig_small(z,True)-c)/trig_small(z)
    return value


def pendant_motion(mb,k,length=F(2,5),terms=128):
    ms=1-mb-F(1,101)-k*length**2/F(101)
    assert ms>0
    rel=I(1/k);neighbour=I(1)
    for j in range(1,terms+1):
        nu=2*PI*j
        eta=nu*TAU;zeta=length*eta
        co,cs=eta.coth_csch();ci,si=zeta.coth_csch()
        P=k*zeta*ci;C=k*zeta*si
        D=ms*nu*nu+P
        A=mb*nu*nu+2*eta*co+P-C*C/D
        B=2*eta*cs
        root=((A-B)*(A+B)).sqrt()
        relative_compliance=1/D+(1-C/D)**2/root
        adjacent_compliance=2/root*(1-B/(A+root))
        assert relative_compliance.lo>0 and adjacent_compliance.lo>0
        rel=rel+2*relative_compliance
        neighbour=neighbour+2*adjacent_compliance
    # M_point-positive resolvent inequality bounds every remaining rod mode.
    rel_tail=I(1/mb+1/ms)/(2*PI*PI*terms)
    adj_tail=I(2/mb)/(2*PI*PI*terms)
    rel_full=I.make(rel.lo,rel.hi+rel_tail.hi)
    adj_full=I.make(neighbour.lo,neighbour.hi+adj_tail.hi)
    return rel_full,adj_full,ms


def main():
    # Sharpen the complete Fejer acoustic lower bound at three fixed q values.
    wlo=F(179,200)  # .895
    whi=F(431,500)  # .862
    at_halfpi=fejer_D(wlo,(0,-1,0))
    at_pi=fejer_D(wlo,(-1,1,-1))
    at_mintrial=fejer_D(whi,(F(-2,3),F(-1,9),F(22,27)))
    assert at_halfpi.lo>0 and at_pi.lo>0 and at_mintrial.hi<0
    G=lambda x:x-x**3/36
    fejer_lower=3*G(wlo)-2*G(whi)

    mb=F(7,1000);k=F(3,5);length=F(2,5)
    ms=1-mb-F(1,101)-k*length**2/F(101)
    left,right=F(79,100),F(29,5)
    denmargin=ms*left**2-k
    alpha2=right**2/F(101)
    zlower=k*(1-length**2*alpha2/2)-mb*right**2
    required=alpha2/(1-alpha2/8)
    assert denmargin>0 and zlower>required
    local_upper=left+bose_tail_upper(right)
    assert local_upper<fejer_lower

    # Fejer exact static compliances and an all-mode Gibbs upper bound.
    sq5=I(5).sqrt()
    u=((sq5-1)/10).sqrt();v=((sq5+1)/10).sqrt()
    compliances=(5*v,10*u,20-20*u-15*v)
    fejer_motion=[c+((F(101,50)*c).sqrt())/2 for c in compliances]
    assert all(c.hi<6*SCALE for c in fejer_motion)

    rel,adj,mscheck=pendant_motion(mb,k)
    assert mscheck==ms and rel.hi<6*SCALE and adj.hi<6*SCALE
    # The earlier heat-only winner really does violate this common cap.
    oldrel,oldadj,_=pendant_motion(F(1,1000),F(2,5),terms=20)
    assert oldadj.lo>6*SCALE

    result={
        'exact_outward_rational_assertions':'PASS',
        'scale_decimal_digits':30,
        'fejer_D_0895_at_halfpi':at_halfpi.json(),
        'fejer_D_0895_at_pi':at_pi.json(),
        'fejer_D_0862_at_cos_minus2thirds':at_mintrial.json(),
        'fejer_full_J_lower':float(fejer_lower),
        'range_matched_pendant_J_upper':float(local_upper),
        'strict_J_gap':float(fejer_lower-local_upper),
        'pendant_stopband_denominator_margin':float(denmargin),
        'pendant_stopband_stiffness_margin':float(zlower-required),
        'fejer_static_compliances':[c.json() for c in compliances],
        'fejer_endpoint_variance_upper':[c.json() for c in fejer_motion],
        'range_matched_pendant_relative_variance':rel.json(),
        'range_matched_pendant_adjacent_variance':adj.json(),
        'old_heat_only_pendant_relative_variance_20term_interval':oldrel.json(),
        'old_heat_only_pendant_adjacent_variance_20term_interval':oldadj.json(),
        'matsubara_positive_terms':128,
    }
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
