#!/usr/bin/env python3
"""A full-entropy witness from one stationary binary lag-two record.

Target: realised total hidden path entropy under stationary all-even Markov
dynamics. This is not a lower confidence bound on the ensemble mean rate.
Negative endpoints are retained. No source parameters or mixing bound enter.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json
import math
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'reversible_currents'))
from currents import log_bounds,fraction_json


def ceil_sqrt(x,bits=0):
    x=Q(x)
    if x<0:raise ValueError('negative square-root argument')
    scale=2**bits
    numerator=x.numerator*scale*scale
    root=math.isqrt(numerator//x.denominator)
    if root*root*x.denominator<numerator:root+=1
    return Q(root,scale)


def scan_lag_two(symbols):
    previous=[];score=0;observations=0
    for symbol in symbols:
        if symbol not in (0,1):raise ValueError('invalid binary symbol')
        if len(previous)==2:
            score+=1 if previous[0]==symbol else -1
            previous.pop(0)
        previous.append(symbol);observations+=1
    if observations<3:raise ValueError('supply at least three observations')
    return observations-1,score


def from_score(transitions,lag_two_score,alpha=Q(1,40),time_uniform=False):
    N=transitions;n=N-1;alpha=Q(alpha)
    if not isinstance(N,int) or N<2 or abs(lag_two_score)>n or (n-lag_two_score)%2:
        raise ValueError('invalid lag-two score')
    if not 0<alpha<1:raise ValueError('alpha must lie between zero and one')
    spent=alpha/Q(N*(N+1)) if time_uniform else alpha
    # Union of the entropy-kernel and two-sided-martingale failure events.
    _,ell=log_bounds(2/spent,40+N.bit_length())
    denominator=max(2,int(ceil_sqrt(Q(8*N)/ell)))
    theta=Q(1,denominator)
    noise=8*ceil_sqrt(2*n*ell,48)
    kernel=8*N*theta+ell/theta
    # One extra edge outside the n central transitions, min witness -8;
    # hidden prediction potential has oscillation <=2.
    boundary=Q(10)
    observed=-2*lag_two_score
    lower=observed-boundary-noise-kernel
    scale=2**96
    scaled=lower*scale
    lower=Q(scaled.numerator//scaled.denominator,scale)
    return {'target':'realised full hidden path entropy in nats',
        'transitions':N,'observations':N+1,'overlapping_triples':n,
        'lag_two_product_sum':lag_two_score,'observable_entropy_witness_sum':observed,
        'theta':str(theta),'family_alpha':str(alpha),'horizon_alpha':str(spent),
        'time_uniform':time_uniform,
        'boundary_cost':'10','martingale_cost_upper_preview':float(noise),
        'entropy_kernel_cost_upper_preview':float(kernel),
        'lower_endpoint':fraction_json(lower),'lower_preview':float(lower),
        'positive_path_entropy_certified':lower>0,'negative_endpoints_retained':True,
        'assumptions':'stationary hidden initialization; ordinary all-even Markov reversal',
        'source_generator_or_mixing_input':None,
        'selection':'one fixed analytic witness; theta determined by horizon and alpha only'}


def evaluate(record,alpha=Q(1,40),time_uniform=False):
    return from_score(*scan_lag_two(record),alpha,time_uniform)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('record',type=Path,help='JSON list of binary observations')
    p.add_argument('--alpha',default='1/40')
    p.add_argument('--time-uniform',action='store_true')
    args=p.parse_args()
    print(json.dumps(evaluate(json.loads(args.record.read_text()),Q(args.alpha),args.time_uniform),indent=2))


if __name__=='__main__':main()
