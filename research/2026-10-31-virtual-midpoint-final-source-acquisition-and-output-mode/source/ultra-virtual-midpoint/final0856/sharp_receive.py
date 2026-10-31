#!/usr/bin/env python3
"""Directed arithmetic checks and labelled replays for the sharp root layer."""
from fractions import Fraction as Q
from pathlib import Path
import ast
import json
import math
import time

from sharp_midpoint import evaluate,coefficients,from_score,bias
from midpoint_band import from_score as gaussian,endpoint,ceil_sqrt,round_lower
from entropy_cone import conjugate_bounds,log_bounds

HERE=Path(__file__).resolve().parent


def high_precision_bound(N,S,b,alpha,theta):
    ll,lh,cl,ch=coefficients(b,160)
    ell=log_bounds(2/alpha,160)[1]
    return min(-2*ll*S,-2*lh*S)-2*N*ch-4*lh*ceil_sqrt(2*N*ell,100)-4*N*lh*lh*theta-ell/theta


def main():
    start=time.perf_counter();conechecks=scorechecks=0;safety=Q(1,2**25)
    for name in ('sharp_midpoint.py','sharp_receive.py'):ast.parse((HERE/name).read_text())
    for b in (Q(0),Q(1,8),Q(1,2),Q(7,8)):
        ll,lh,cl,ch=coefficients(b,80)
        for t in (Q(i,8) for i in range(-8,9)):
            upper=conjugate_bounds(2*lh*t,40)[1]-ll*t*t-ch
            assert upper<=safety
            conechecks+=1
        for N in (10,1000,100000):
            for S in (-N,0 if N%2==0 else 1,N):
                result=from_score(N,S,b,Q(1,40));theta=Q(result['theta'])
                assert endpoint(result)<=high_precision_bound(N,S,b,Q(1,40),theta)
                scorechecks+=1
                if b==0:assert endpoint(result)==endpoint(gaussian(N,S,Q(1,40)))
    receipt=json.loads((HERE/'receipt.json').read_text())
    rlo,rhi=map(Q,receipt['source']['correlation_magnitude_interval'])
    scale=2**96;loarg=rlo*scale*scale
    blo=Q(math.isqrt(loarg.numerator//loarg.denominator),scale)
    bhi=ceil_sqrt(rhi,96)
    vlo=2*blo*log_bounds((1+blo)/(1-blo),120)[0]
    vhi=2*bhi*log_bounds((1+bhi)/(1-bhi),120)[1]
    vpreview=float((vlo+vhi)/2)
    replays=[]
    for name in ('driven_alias','reversible_matched'):
        record=json.loads((HERE/(name+'_record.json')).read_text())
        result=evaluate(iter(record),Q(1,80),threshold=1000)
        replays.append({'name':name,'lower':result['lower_preview'],
                        'first_crossing':result['first_threshold_crossing'],
                        'critic_evaluations':result['critic_evaluations'],
                        'scope':'existing-record implementation replay; library derived after acquisition'})
    out={'status':'SHARP_ROOT_LAYER_ARITHMETIC_AND_REPLAYS_CHECKED',
         'quadratic_conjugate_enclosures':conechecks,'finite_cone_enclosure_safety_margin':str(safety),
         'cone_check_scope':'finite rational enclosures with stated margin; the exact universal cone is the analytic inequality(S2)',
         'directed_score_bounds_checked_against_tighter_enclosures':scorechecks,
         'b0_matches_frozen_Gaussian_exactly':True,
         'exact_first_root_minimum_formula':'2phi(sqrt r)',
         'exact_first_root_minimum_preview':vpreview,
         'Gaussian_witness_rate_preview':float(2*(rlo+rhi)),
         'Gaussian_fraction_of_first_root_minimum_preview':float(2*(rlo+rhi))/vpreview,
         'comparison_is_to_full_CTMC_minimum':False,
         'replays':replays,'seconds':time.perf_counter()-start,
         'scope':'analytic theorem in SHARP_LAYER.txt; finite arithmetic checks and retrospective replays are separate; no new acquisition'}
    (HERE/'sharp_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
