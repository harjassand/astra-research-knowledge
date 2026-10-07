#!/usr/bin/env python3
"""Certified finite-random-bit clipped normal, by rational CDF intervals.

Guarantee: returned value is h-close to a coupled clipped ideal N(0,1).
This is NOT total-variation approximation to a continuous normal law.
No floating-point value participates in numerical decisions or certificates.
"""
import argparse
import datetime
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import resource
import secrets
import time

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('rational_iv',HERE/'certified_two_spin.py')
base=importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
IV,iv=base.IV,base.iv
fa,fs,fm,fd=base.fa,base.fs,base.fm,base.fd


def ceil_fraction(x): return -((-x.numerator)//x.denominator)


def ceil_log2_positive(x):
    p=0
    z=F(1)
    while z<x:
        p+=1
        z*=2
    return p


def atan_inverse(d):
    # Alternating arctangent series; its next term bounds the exact remainder.
    base.ledger.add('arctangent_calls')
    tol=F(1,1<<(IV.P+12))
    term=F(1,d)
    total=term
    n=0
    while True:
        power_next=F(1,d**(2*n+3))
        rem=fd(power_next,F(2*n+3))
        if rem<=tol:
            break
        n+=1
        term=fd(F((-1)**n,d**(2*n+1)),F(2*n+1))
        total=fa(total,term)
        base.ledger.add('arctangent_series_terms')
    return IV(fs(total,rem),fa(total,rem))


class NormalCDF:
    def __init__(self,L,delta):
        self.L,self.delta=L,delta
        pi=16*atan_inverse(5)-4*atan_inverse(239)
        assert pi.lo>3 and pi.hi<4
        self.pi=pi
        self.coefficient=1/base.sqrt_iv(2*pi)
        self.cache={}
        self.calls=0
        self.series_terms=0
        self.max_interval_width=F(0)

    def evaluate(self,z):
        assert -self.L<=z<=self.L
        self.calls+=1
        base.ledger.add('cdf_requests')
        if z in self.cache:
            base.ledger.add('cdf_cache_hits')
            return self.cache[z]
        if z<0:
            result=1-self.evaluate(-z)
        elif z==0:
            result=iv(F(1,2))
        else:
            # Integral of the Taylor polynomial of exp(-t^2/2).
            # On t>=0, Lagrange's remainder yields
            # |integral remainder| <= z*(z^2/2)^(n+1)/(n+1)!.
            t=total=z
            n=0
            x=fm(fm(z,z),F(1,2))
            rem=fm(z,x)
            tol=self.delta/32
            while rem>tol:
                next_t=fd(fm(fm(-t,x),F(2*n+1)),F((n+1)*(2*n+3)))
                n+=1
                t=next_t
                total=fa(total,t)
                rem=fd(fm(rem,x),F(n+1))
                self.series_terms+=1
                base.ledger.add('cdf_integral_taylor_terms')
            integral=IV(fs(total,rem),fa(total,rem))
            result=iv(F(1,2))+self.coefficient*integral
        width=fs(result.hi,result.lo)
        self.max_interval_width=max(self.max_interval_width,width)
        if width>self.delta:
            raise ArithmeticError('CDF guard budget insufficient; no certificate emitted')
        self.cache[z]=result
        return result


def tail_upper(L):
    # Chernoff: P(|Z|>L)<=2 exp(-L^2/2). Positive Taylor terms enclose
    # exp(L^2/2) from BELOW, giving a purely rational upper bound.
    x=fm(fm(L,L),F(1,2))
    total=term=F(1)
    degree=ceil_fraction(L*L)+24
    for n in range(1,degree+1):
        term=fd(fm(term,x),F(n))
        total=fa(total,term)
        base.ledger.add('tail_positive_taylor_terms')
    return min(F(1),fd(F(2),total)),degree


def generate(L,ell,u_integer=None):
    assert F(1)<=L<=F(8) and 8<=ell<=128
    h=F(1,1<<ell)
    power=ceil_fraction(L*L)+3
    q=F(1,1<<power) # certified q<=phi(L), no exp/ceil of real needed
    random_bits=ell+power+5
    delta=F(1,1<<random_bits) # exactly h*q/32
    p=random_bits+ceil_log2_positive(L+1)+32
    IV.precision(p)
    if u_integer is None:
        u_integer=secrets.randbits(random_bits)
        source='OS secrets.randbits; theorem assumes ideal fair bits'
    else:
        source='supplied deterministic transcript; not a random-source validation'
    assert 0<=u_integer<(1<<random_bits)
    u=F(u_integer,1<<random_bits)
    cdf=NormalCDF(L,delta)
    left,right=cdf.evaluate(-L),cdf.evaluate(L)
    steps=[]
    if u<left.lo:
        answer,status=-L,'RESOLVED_LEFT_CLIP'
    elif u<=left.hi:
        answer,status=-L,'TOLERANCE_LEFT_ENDPOINT'
    elif u>right.hi:
        answer,status=L,'RESOLVED_RIGHT_CLIP'
    elif u>=right.lo:
        answer,status=L,'TOLERANCE_RIGHT_ENDPOINT'
    else:
        lo,hi=-L,L
        while True:
            mid=fd(fa(lo,hi),F(2))
            if hi-lo<=h/2:
                answer,status=mid,'BRACKET_RADIUS_STOP'
                break
            enclosure=cdf.evaluate(mid)
            steps.append({'point':str(mid),'cdf':enclosure.json()})
            if u<enclosure.lo:
                hi=mid
            elif u>enclosure.hi:
                lo=mid
            else:
                answer,status=mid,'TOLERANCE_INTERIOR_STOP'
                break
    trunc,tail_degree=tail_upper(L)
    # The clipped inverse is 1/q-Lipschitz. Any unresolved CDF comparison has
    # CDF error <=delta; the coupled full U differs from its bit prefix by delta.
    # Resolved bracket stopping has radius <=h/4. Both are dominated below.
    coupling_upper=max(2*delta/q,h/4+delta/q)
    assert coupling_upper<h
    return {'status':'CERTIFIED_CLIPPED_NORMAL_COUPLING','L':str(L),'h':str(h),
            'output_rational':str(answer),'termination':status,
            'ideal_clipped_normal_coupling_error_upper':str(coupling_upper),
            'normal_tail_probability_upper':str(trunc),
            'tail_certificate_positive_exp_degree':tail_degree,
            'normal_density_lower_bound_on_clip':str(q),
            'cdf_interval_width_budget':str(delta),
            'max_observed_cdf_interval_width':str(cdf.max_interval_width),
            'working_bits':p,'guard_bits_beyond_uniform':p-random_bits,
            'exact_fair_random_bit_count':random_bits,'uniform_integer':u_integer,
            'uniform_prefix_rational':str(u),'random_source':source,
            'cdf_request_count':cdf.calls,'cdf_integral_taylor_terms':cdf.series_terms,
            'pi_interval':cdf.pi.json(),'inverse_sqrt_2pi_interval':cdf.coefficient.json(),
            'bisection_steps':steps,
            'contract':'Pointwise coupling to clipped inverse CDF; no TV-to-continuous-Gaussian claim.',
            'limits':['Owned extension: configured L in [1,8], ell in [8,128]; analytic rational coupling guards unchanged; bounded new precision checks separately recorded',
                      'Not integrated with spin-path rejection or local filtering',
                      'Finite ideal fair-bit interface, not physical entropy certification']}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--L',default='4')
    ap.add_argument('--error-bits',type=int,default=24)
    ap.add_argument('--uniform-integer',type=int)
    ap.add_argument('--out',required=True)
    args=ap.parse_args()
    base.ledger=base.Ledger()
    start,cpu=time.perf_counter(),time.process_time()
    data=generate(F(args.L),args.error_bits,args.uniform_integer)
    data.update({'worker_id':'c07_s03','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 'costs':{**base.ledger.snapshot(),'wall_seconds':time.perf_counter()-start,
                           'cpu_seconds':time.process_time()-cpu,
                           'process_peak_rss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}})
    p=Path(args.out)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'output':str(p),'status':data['status'],
                      'point':data['output_rational'],'termination':data['termination'],
                      'fair_bits':data['exact_fair_random_bit_count'],
                      'coupling_error_upper':data['ideal_clipped_normal_coupling_error_upper'],
                      'tail_probability_upper':data['normal_tail_probability_upper'],
                      'wall_seconds':data['costs']['wall_seconds']}))


if __name__=='__main__': main()
