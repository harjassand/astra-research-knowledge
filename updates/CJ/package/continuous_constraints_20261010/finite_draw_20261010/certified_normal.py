#!/usr/bin/env python3
"""Arbitrary-precision finite normal cells, with exact directed certificates.

mpmath proposes a quantile quickly. Exact integer CDF bounds accept it or the
code uses bounded, ambiguity-safe bisection. No special-function accuracy claim
is trusted. Endpoint/out-of-domain cells return an explicit fallback marker.
"""
from __future__ import annotations
import argparse, functools, json, math, random, sys, time
from fractions import Fraction as Q
import mpmath as mp
sys.set_int_max_str_digits(0)

def floor(x):return x.numerator//x.denominator
def ceil(x):return -((-x.numerator)//x.denominator)
def ceildiv(a,b):return -((-a)//b)
def nearest(x,scale):return floor(x*scale+Q(1,2))

def atan_bounds(q,terms):
    s=sum((Q((-1)**k,(2*k+1)*q**(2*k+1)) for k in range(terms)),Q(0))
    t=Q((-1)**terms,(2*terms+1)*q**(2*terms+1))
    return min(s,s+t),max(s,s+t)

@functools.lru_cache(maxsize=16)
def normal_constant(bits):
    sc=1<<bits
    a=atan_bounds(5,bits//4+20);b=atan_bounds(239,bits//15+20)
    plo,phi=16*a[0]-4*b[1],16*a[1]-4*b[0]
    lo=math.isqrt((sc*sc*phi.denominator)//(2*phi.numerator))
    hi=math.isqrt((sc*sc*plo.denominator)//(2*plo.numerator))+1
    assert Q(lo*lo,sc*sc)*2*phi<=1 and Q(hi*hi,sc*sc)*2*plo>=1
    return lo,hi

class CertifiedNormal:
    def __init__(self,rho_bits,L0,uniform_bits=None):
        self.rho_bits=int(rho_bits);self.L0=int(L0);self.bound=self.L0+1
        assert self.rho_bits>=1 and self.L0>=2
        self.rho=Q(1,1<<self.rho_bits)
        self.uniform_bits=uniform_bits or self.rho_bits+self.bound**2+8
        assert self.uniform_bits>=self.rho_bits+self.bound**2+8
        self.fraction_bits=self.rho_bits+6;self.scale=1<<self.fraction_bits
        # CDF enclosure width <=rho*phi_min/256. Outward arithmetic is checked.
        self.cdf_target_bits=self.rho_bits+self.bound**2+10
        self.working_bits=self.cdf_target_bits+2*self.bound**2+2*(self.cdf_target_bits+self.bound**2+1).bit_length()+32
        # Exact a-priori majorants exclude a good-set arithmetic abort. For
        # term interval widths D_k, summing the recurrence gives
        # sum D_k <= 2*u*(B0+K+1)*exp(B0^2/2+1). Bound exp by an integer.
        while True:
            w=self.working_bits;K=16*(w+self.bound*self.bound+1)
            sc=1<<w;clo,chi=normal_constant(w)
            C=3**((self.bound*self.bound+1)//2+1)
            rounding=Q(2*(self.bound+K+1)*C,sc)
            tau=Q(1,1<<(self.cdf_target_bits+4))
            final_width=rounding+tau+Q(3*(chi-clo)+2,sc)
            # K! >= (K/e)^K and K >= 3*B0^2 imply t_K <= B0*2^-K.
            tail_at_cap=Q(self.bound,1<<K)+rounding
            if (K>=3*self.bound*self.bound and tail_at_cap<=tau
                and final_width<=Q(1,1<<self.cdf_target_bits)
                and rounding+tau<=1 and chi<=sc):
                break
            self.working_bits+=16
        self.series_cap=K
        self.majorant_proof={'series_cap':K,'rounding_width_upper':rounding,
            'tail_at_cap_upper':tail_at_cap,'tail_stop_threshold':tau,
            'final_CDF_width_upper':final_width,
            'required_CDF_width':Q(1,1<<self.cdf_target_bits)}
        self.cdf_calls=0;self.bisection_calls=0

    def cdf(self,x):
        """Return rational lower/upper bounds enclosing Phi(x)."""
        self.cdf_calls+=1;x=Q(x)
        if x<0:
            a,b=self.cdf(-x);return 1-b,1-a
        if x==0:return Q(1,2),Q(1,2)
        if x>self.bound:raise ValueError('CDF input exceeds certified bounded domain')
        bits=self.working_bits;sc=1<<bits
        tlo,thi=floor(x*sc),ceil(x*sc);q=x*x/2
        qlo,qhi=floor(q*sc),ceil(q*sc);slo=shi=0
        # A generous finite cap for the alternating tail on this bounded domain.
        limit=self.series_cap
        threshold=1<<(bits-self.cdf_target_bits-4)
        for k in range(limit):
            if k%2==0:slo+=tlo;shi+=thi
            else:slo-=thi;shi-=tlo
            den=sc*(k+1)*(2*k+3)
            nlo=tlo*qlo*(2*k+1)//den
            nhi=ceildiv(thi*qhi*(2*k+1),den)
            if k>=ceil(q) and nhi<=threshold:
                if (k+1)%2==0:shi+=nhi
                else:slo-=nhi
                slo=max(0,slo) # The integrated nonnegative density is >=0.
                assert shi>=slo
                clo,chi=normal_constant(bits)
                a=Q(sc//2+(slo*clo)//sc,sc)
                b=Q(sc//2+ceildiv(shi*chi,sc),sc)
                if b-a>Q(1,1<<self.cdf_target_bits):
                    raise ArithmeticError('Directed CDF width exceeds proved evaluator contract')
                return a,b
            tlo,thi=nlo,nhi
        raise ArithmeticError('Directed CDF finite series cap exceeded')

    def bracket_midpoint(self,q,force_bisection=False):
        """Produce z with a certified cell neighborhood, or None for tail cells."""
        # A proposed dyadic midpoint has no semantic force until certified below.
        if not force_bisection:
            try:
                with mp.workprec(self.uniform_bits+80):
                    uq=mp.mpf(q.numerator)/q.denominator
                    zmp=mp.sqrt(2)*mp.erfinv(2*uq-1)
                    z=Q(int(mp.nint(zmp*self.scale)),self.scale)
                if abs(z)+self.rho/4<=self.bound:
                    return z,'mpmath proposal; exact CDF verification required'
            except (ArithmeticError,ValueError,OverflowError):
                pass # Proposal failure never controls a certified output.
        self.bisection_calls+=1
        left,right=Q(-self.bound),Q(self.bound)
        a,b=self.cdf(left);c,d=self.cdf(right)
        if q<=b or q>=c:return None,'out-of-domain/tail fallback'
        # After B iterations width <=rho/32, irrespective of exact comparisons.
        max_steps=self.rho_bits+(2*self.bound).bit_length()+7
        phi_min=Q(1,1<<(self.bound**2+2))
        for _ in range(max_steps):
            mid=(left+right)/2;a,b=self.cdf(mid)
            if q<a:right=mid
            elif q>b:left=mid
            else:
                # |Phi(mid)-q|<=b-a; the inverse derivative is <=1/phi_min.
                radius=(b-a)/phi_min
                assert radius<=self.rho/256
                return Q(nearest(mid,self.scale),self.scale),'ambiguity-safe bisection'
            if right-left<=self.rho/32:
                return Q(nearest((left+right)/2,self.scale),self.scale),'bounded bisection'
        raise ArithmeticError('Impossible bisection iteration bound violated')

    def from_cell(self,k,force_bisection=False):
        den=1<<self.uniform_bits
        if not 0<=k<den:raise ValueError('Cell index out of range')
        if k==0 or k==den-1:
            return {'fallback':True,'reason':'endpoint uniform cell','uniform_cell_index':str(k)}
        ulo,uhi=Q(k,den),Q(k+1,den);q=(ulo+uhi)/2
        for force in ([True] if force_bisection else [False,True]):
            z,method=self.bracket_midpoint(q,force)
            if z is None:return {'fallback':True,'reason':method,'uniform_cell_index':str(k)}
            lo,hi=z-self.rho/4,z+self.rho/4
            if lo < -self.bound or hi > self.bound:continue
            alo,ahi=self.cdf(lo);blo,bhi=self.cdf(hi)
            if ahi<=ulo and blo>=uhi:
                return {'fallback':False,'value':z,'error_bound':self.rho/4,
                    'interval':(lo,hi),'uniform_cell_index':str(k),
                    'uniform_bits':self.uniform_bits,'fraction_bits':self.fraction_bits,
                    'normal_integer':str(int(z*self.scale)),
                    'cdf_upper_at_lower':ahi,'cdf_lower_at_upper':blo,
                    'cdf_working_bits':self.working_bits,'method':method}
        # This can occur only for cells whose true quantiles cross the outer domain;
        # on |Z|<=L0, the quantitative margin proves final CDF tests succeed.
        return {'fallback':True,'reason':'outer-domain cell did not certify','uniform_cell_index':str(k)}

    def draw(self,rng):return self.from_cell(rng.getrandbits(self.uniform_bits))

def encoded(x):
    if isinstance(x,Q):return {'num':str(x.numerator),'den':str(x.denominator)}
    if isinstance(x,dict):return {k:encoded(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encoded(y) for y in x]
    return x

def selftest():
    start=time.perf_counter();checks=[]
    for bits,L in [(20,4),(80,6),(280,9)]:
        gen=CertifiedNormal(bits,L);rng=random.Random(137+bits)
        cases=[gen.draw(rng) for _ in range(3)]
        # Force the hard fallback at the exact dyadic midpoint Phi(0)=1/2.
        cases.append(gen.from_cell((1<<(gen.uniform_bits-1))-1,force_bisection=True))
        for c in cases:
            assert not c['fallback']
            lo,hi=c['interval'];a,b=gen.cdf(lo);d,e=gen.cdf(hi)
            k=int(c['uniform_cell_index']);den=1<<gen.uniform_bits
            assert b<=Q(k,den) and d>=Q(k+1,den)
            assert c['error_bound']<=gen.rho and hi-lo==gen.rho/2
        assert gen.from_cell(0)['fallback'] and gen.from_cell((1<<gen.uniform_bits)-1)['fallback']
        checks.append({'rho_bits':bits,'L0':L,'uniform_bits':gen.uniform_bits,
                       'cdf_working_bits':gen.working_bits,'certified_cells':len(cases),
                       'a_priori_CDF_majorants_verified':True,
                       'cdf_calls':gen.cdf_calls,'bisection_calls':gen.bisection_calls})
    return {'exact_certificate_checks_passed':True,'cases':checks,'runtime_seconds':time.perf_counter()-start,
            'provenance':'Only exact rational inequalities establish brackets; mpmath proposes midpoints.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--self-test',action='store_true');args=ap.parse_args()
    print(json.dumps(selftest(),indent=2))
