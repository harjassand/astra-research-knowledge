#!/usr/bin/env python3
"""Finite mathematical checks; not experimental validation."""
import json
from pathlib import Path
import numpy as np
import mpmath as mp
from response_compiler import compile_experiment, summary, log10_fraction
ROOT=Path(__file__).resolve().parent
def fmp(q):
    return mp.mpf(q.numerator)/q.denominator
def run():
    rows=[]; certificates=[]
    cases=[(4,'1/10'),(16,'1/10'),(64,'1/10'),(256,'1/10'),
           (1024,'1/10'),(1000000,'1/10'),(16,'1/2'),(16,'1/5'),
           (16,'1/50'),(256,'1/2'),(256,'1/5'),(256,'1/50')]
    for band,horizon in cases:
        c=compile_experiment(upper=band,horizon=horizon)
        rows.append(summary(c)); certificates.append(c)
    rng=np.random.default_rng(20261105); examples=[]
    for c in [certificates[1],certificates[3],certificates[6]]:
        mp.mp.dps=max(90,int(log10_fraction(c['l1_amplification']))+70)
        mu,upper,duration,U=[fmp(c[x]) for x in ['mu','Lambda','T','U']]
        width,ramp=fmp(c['bin_width']),duration/2
        weights=list(map(fmp,c['weights'])); bound=fmp(c['bias_bound'])
        max_error=mp.mpf('0'); worst_ratio=mp.mpf('0')
        for dim in [1,2,8,32,128]:
            for trial in range(4):
                if dim==1:
                    rates=[mu+(upper-mu)*mp.mpf(trial)/3]; masses=[mp.mpf(1)]
                else:
                    rates=[mu*(upper/mu)**mp.mpf(str(v)) for v in rng.uniform(size=dim)]
                    raw=[mp.mpf(str(v)) for v in rng.exponential(size=dim)]
                    masses=[v/sum(raw) for v in raw]
                gain=sum(p*mu/lam for p,lam in zip(masses,rates)); means=[]
                for j in range(c['bin_count']):
                    means.append(sum(p*U/lam*(1-
                        (-mp.expm1(-lam*ramp))/(lam*ramp)*
                        (-mp.expm1(-lam*width))/(lam*width)*mp.exp(-lam*j*width))
                        for p,lam in zip(masses,rates)))
                estimate=mu/U*sum(w*y for w,y in zip(weights,means))
                error=abs(estimate-gain)
                if error>bound+mp.mpf('1e-40'):
                    raise AssertionError('Finite spectrum violates certificate.')
                max_error=max(max_error,error); worst_ratio=max(worst_ratio,error/bound)
        rates=[mu,upper]; masses=[mp.mpf('0.37'),mp.mpf('0.63')]
        def y(t):
            return sum(p*U/lam*(1-(-mp.expm1(-lam*ramp))/(lam*ramp)*
                       mp.exp(-lam*(t-ramp))) for p,lam in zip(masses,rates))
        integrated=[mp.quad(y,[ramp+j*width,ramp+(j+1)*width])/width
                    for j in range(c['bin_count'])]
        result=mu/U*sum(w*v for w,v in zip(weights,integrated))
        gain=sum(p*mu/lam for p,lam in zip(masses,rates))
        if abs(result-gain)>bound: raise AssertionError('Integrated check failed.')
        examples.append({'Lambda':str(c['Lambda']),'T':str(c['T']),
            'spectra_checked':20,'dimensions':[1,2,8,32,128],
            'precision_decimal_digits':mp.mp.dps,
            'largest_observed_absolute_error':float(max_error),
            'certified_bias_bound':float(bound),
            'largest_error_divided_by_bound':float(worst_ratio),
            'time_domain_quadrature_error':float(abs(result-gain)),
            'exact_rational_weights_sum_one':c['weights_sum']==1})
    result={'status':'All finite checks passed; analytic proofs govern uniform claims.',
        'random_seed':20261105,'physical_trials':0,'tables':rows,
        'finite_spectrum_checks':examples,
        'statistical_certificate':'Gaussian tail handled analytically using rational log upper bound.',
        'warning':'Sufficient counts can be astronomical; no engineering feasibility claim.'}
    (ROOT/'compiler_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': run()
