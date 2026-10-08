#!/usr/bin/env python3
"""Exact-formula/rare-tail finite diagnostics, not theorem certification."""
from decimal import Decimal as D, localcontext
from math import ceil, comb, exp, expm1, lgamma, log, sqrt
from pathlib import Path
import json


def coth(x):
    return 1+2/((2*x).exp()-1)


def radius_and_derivative(r,j):
    t = ((1+r)/(1-r)).ln()/2
    d = 2*j+1
    u = d*t
    c = coth(u)
    sh = (u.exp()-(-u).exp())/2
    a = (d*c-1/r)/(d+1)
    ap = 2*((c+1/r)/(d+1)**2-d*t/(d+1)/sh**2)
    return a,ap


def log_spin_prob(n,r,l):
    k = (n-l)//2
    a,b = (1+r)/2,(1-r)/2
    beta = log(a/b)
    return (lgamma(n+1)-lgamma(k+1)-lgamma(n-k+1)
            +(n-k)*log(a)+k*log(b)
            +log(2*(l+1)/(n+l+2)*a/r)
            +log(-expm1(-beta*(l+1))))


def run():
    derivatives = pairs = stirling = bands = 0
    min_pair_ratio = D('Infinity')
    with localcontext() as ctx:
        ctx.prec = 75
        for r in (D(1)/2,D(1)/4,D(1)/16,D(1)/128):
            for z in (2,4,8,16,32,128):
                j = D(z)/r
                a,ap = radius_and_derivative(r,j)
                assert ap >= 1/(4*r*(j+1)**2)
                assert ap <= 1/(r*(j+1)**2)
                if r*j >= 4:
                    assert (j*ap-a)/j**2 <= -1/(2*j*j)
                derivatives += 1
            for q in (ceil(1/float(r)),2*ceil(1/float(r)),8*ceil(1/float(r))):
                for factor in (16,20,32):
                    j = D(factor*q)
                    aj,_ = radius_and_derivative(r,j)
                    s = D(1)/(16*q)
                    raw = [D(0),j/2,j-1,j-D('.5'),j,j+D('.5'),j+1,2*j,
                           j*(1-s),j/(1-s)]
                    ks = set((2*x).to_integral_value(rounding='ROUND_FLOOR')/2 for x in raw)
                    for k in ks:
                        if k == 0:
                            deficit = aj*aj/2+aj*aj/j
                        else:
                            ak,_ = radius_and_derivative(r,k)
                            m,M = min(j,k),max(j,k)
                            g = M/(32*q) if M-m <= M/(16*q) else D(0)
                            deficit = ((ak-aj)**2/2+aj*aj/j-aj*ak/M
                                       +aj*ak*g/(j*k))
                        bound = 1/(D(786432)*r*q**3)
                        assert deficit >= bound
                        min_pair_ratio = min(min_pair_ratio,deficit/bound)
                        pairs += 1

    for n in range(4,201):
        for l in range(n%2,n//2+1,2):
            actual = comb(n,(n-l)//2)*2.**(-n)
            lower = exp(-2*l*l/(3*n))/(2*sqrt(n))
            assert actual >= lower*(1-1e-13)
            stirling += 1

    rows = []
    for n in (512,1024,4096):
        for r in (.25,.125,.0625):
            for q in (ceil(1/r),2*ceil(1/r),n//128):
                if not 1/r <= q <= n/128:
                    continue
                ls = range(32*q+n%2,64*q+1,2)
                logs = [log_spin_prob(n,r,l) for l in ls]
                top = max(logs)
                logmass = top+log(sum(exp(x-top) for x in logs))
                loglower = (log(4096)+3*log(q)-1.5*log(n)
                            -2*n*r*r/3-(8192/3)*q*q/n)
                assert logmass >= loglower-3e-10
                rows.append(dict(n=n,r=r,Q=q,logmass=logmass,
                                 log_lower=loglower,allowed_points=len(logs)))
                bands += 1

    out = dict(status='FINITE-EVIDENCE',decimal_precision=75,
               derivative_fixtures=derivatives,all_output_pair_fixtures=pairs,
               unbiased_binomial_stirling_fixtures=stirling,
               rare_schur_band_fixtures=bands,
               minimum_pair_deficit_to_bound_ratio=str(min_pair_ratio),
               rows=rows,
               limitations='Finite scalar checks and exact-formula numerics; no optimization over all channels, physical implementation, formal theorem validation, or novelty evidence.')
    Path(__file__).with_name('quantum_tail_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k != 'rows'},indent=2))


if __name__ == '__main__':
    run()
