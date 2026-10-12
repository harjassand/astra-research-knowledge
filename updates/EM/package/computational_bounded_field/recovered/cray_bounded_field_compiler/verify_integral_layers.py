#!/usr/bin/env python3
"""Finite rank-one diagnostic of the positive convex-volume sum.

No convex-volume algorithm is implemented: in one dimension the sublevel
body is an interval and its volume is computed explicitly. Arithmetic is
high precision but not interval-certified.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import mpmath as mp
from verify_compiler import log_normal_interval


def check_case(name, left, right, mu, variance, eta):
    k=mp.mpf(variance); mu=mp.mpf(mu)
    l=mp.mpf(left); u=mp.mpf(right)
    mode=max(l,min(u,mu)); dist=abs(mode-mu)
    qmin=dist*dist/(2*k)
    true_log_i=qmin+mp.log(2*mp.pi*k)/2+log_normal_interval((l-mu)/mp.sqrt(k),(u-mu)/mp.sqrt(k))
    s=eta/16
    T=16+4*math.ceil(math.log2(32/float(eta)))
    N=int(mp.ceil(T/s))
    accum=mp.mpf(0)
    geometric=mp.exp(-s)
    weight=1-geometric
    for j in range(1,N+1):
        rad=mp.sqrt(dist*dist+2*k*j*s)
        volume=max(mp.mpf(0),min(u,mu+rad)-max(l,mu-rad))
        accum+=weight*volume
        weight*=geometric
    log_error=mp.log(accum)-true_log_i
    assert abs(log_error)<eta
    return {'case':name,'levels':N,'eta':str(eta),'mode':mp.nstr(mode,20),
            'true_log_normalized_integral':mp.nstr(true_log_i,26),
            'signed_log_error':mp.nstr(log_error,24)}


def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,default=Path('integral_results.json'))
    args=p.parse_args(); mp.mp.dps=90; eta=mp.mpf(1)/8
    cases=[check_case('central',-1,2,0,1,eta),
           check_case('far_shifted',0,1,mp.mpf(2)**40,1,eta),
           check_case('thin_interval',0,mp.mpf(2)**-40,1,1,eta),
           check_case('narrow_gaussian',-1,2,0,mp.mpf(2)**-40,eta)]
    data={'status':'positive_sum_finite_checks_passed_not_general_volume_engine',
          'precision_decimal_digits':90,'cases':cases,
          'limitations':['Explicit one-dimensional sublevel volumes only.',
                         'No interval certification and no generic volume FPRAS.']}
    args.output.write_text(json.dumps(data,indent=2)+'\n'); print(json.dumps(data,indent=2))

if __name__=='__main__': main()
