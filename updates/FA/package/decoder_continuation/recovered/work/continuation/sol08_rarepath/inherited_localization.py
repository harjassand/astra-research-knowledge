#!/usr/bin/env python3
"""Rigorous original-Euler environmental exit bound; no simulation.

Uses exact Gaussian increments, discrete OU comparison, time-changed Brownian
embedding, a chord bound, and drifted reflection. Rational enclosure arithmetic
is imported from rarepath_certificate.py. See PROOF.txt.
"""
from fractions import Fraction as F
from pathlib import Path
import json,time
from rarepath_certificate import (floor_grid,ceil_grid,exp_negative_interval,
                                 normal_sf_interval,sqrt_interval,PI,frac_record)

HERE=Path(__file__).resolve().parent


def sf_upper(z2):
    if z2>36:
        return normal_sf_interval(z2)[1]
    # The first Mills bound Q(z)<=phi(z)/z holds at every positive z.
    assert z2>0
    _,e=exp_negative_interval(z2/2)
    _,root=sqrt_interval(1/(2*PI[0]*z2))
    return ceil_grid(e*root)


def hit_upper(a,kappa,variance):
    assert a-kappa*variance>0
    zplus=(a+kappa*variance)**2/variance
    zminus=(a-kappa*variance)**2/variance
    _,e=exp_negative_interval(2*a*kappa)
    return ceil_grid(sf_upper(zplus)+e*sf_upper(zminus)),(zplus,zminus)


def run():
    start=time.perf_counter()
    n=4000;r=F(49997,50000);sigma2=F(1,50000)
    rn_exact=1/r**n
    rnlo,rnhi=floor_grid(rn_exact,80),ceil_grid(rn_exact,80)
    c=(1-r*r)/sigma2
    variance_hi=ceil_grid((rnhi*rnhi-1)/c,80)
    kappa_lo=floor_grid(F(11,5)*c/(rnhi+1),80)
    lower_exit,zlower=hit_upper(F(2),kappa_lo,variance_hi)
    upper_exit,zupper=hit_upper(F(4),kappa_lo,variance_hi)
    total=ceil_grid(lower_exit+upper_exit)
    assert total<F(1,10**14)
    out={'status':'INTERNALLY_RECONSTRUCTED_PROOF_WITH_EXACT_RATIONAL_ENCLOSURE',
         'target':'P(any y_k outside [-3,3] at k<=4000, before or at stopped first x-boundary hit); original inherited Euler dt=.0005, x0=-.75,y0=-1',
         'physical_source_drift':'dy=.02, coupling=6: ynew=(1-.12dt)y+.12dt*x+sqrt(.04dt)*xi',
         'r':str(r),'N':n,'martingale_variance_upper':frac_record(variance_hi),
         'chord_slope_lower':frac_record(kappa_lo),
         'lower_exit_upper':frac_record(lower_exit),
         'upper_exit_upper':frac_record(upper_exit),
         'total_exit_upper':frac_record(total),
         'total_exit_upper_float':float(total),
         'relative_to_inherited_point_estimate_diagnostic_only':float(total/F('4.304224792713203e-10')),
         'reflection_z_squared_lower_exit':[str(x) for x in zlower],
         'scope':'rigorous physical-law localization bias budget only; does not certify the learned guide or path weight bound on the compact region',
         'no_sampling_or_force_queries':True,
         'execution_seconds':time.perf_counter()-start}
    (HERE/'localization_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','total_exit_upper_float','relative_to_inherited_point_estimate_diagnostic_only','execution_seconds']},indent=2))


if __name__=='__main__':
    run()
