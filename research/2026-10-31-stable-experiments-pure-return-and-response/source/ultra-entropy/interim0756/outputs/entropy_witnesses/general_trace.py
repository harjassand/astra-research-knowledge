#!/usr/bin/env python3
"""Evaluate a verified FULL entropy dual on one stationary dependent record.

Target is realised hidden trajectory entropy, not an ensemble mean rate.
The certificate must be frozen, or receive an explicit selection allocation.
"""
from fractions import Fraction as Q
from collections import deque
from pathlib import Path
import argparse
import json

from entropy_cone import load,log_bounds
from quadratic_trace import ceil_sqrt,fraction_json


def scan(cert,symbols):
    s,L=cert['alphabet'],cert['depth']
    lookup=dict(zip(cert['words'],cert['W']))
    window=deque(maxlen=2*L+1);total=Q(0);observations=0
    for symbol in symbols:
        if not isinstance(symbol,int) or not 0<=symbol<s:raise ValueError('invalid observed symbol')
        window.append(symbol);observations+=1
        if len(window)==window.maxlen:total+=lookup[tuple(window)]
    if observations<2*L+1:raise ValueError('record too short')
    return observations-1,total


def from_statistic(cert,N,word_sum,alpha=Q(1,40),time_uniform=False):
    alpha=Q(alpha);word_sum=Q(word_sum);L=cert['depth'];n=N-2*L+1
    if n<1 or not 0<alpha<1:raise ValueError('invalid horizon or confidence')
    spent=alpha/Q(N*(N+1)) if time_uniform else alpha
    _,ell=log_bounds(2/spent,40+N.bit_length())
    M=cert['M'];C=cert['C']
    denom=max(2,int(ceil_sqrt(N*M*M/(2*ell))))
    theta=Q(1,denom)
    noise=C*ceil_sqrt(2*n*ell,48)
    kernel=N*theta*M*M/2+ell/theta
    boundary=(2*L-1)*cert['H_min']-cert['O']
    lower=word_sum+boundary-noise-kernel
    scale=2**96;scaled=lower*scale
    lower=Q(scaled.numerator//scaled.denominator,scale)
    return {'target':'realised full hidden trajectory entropy in nats',
        'observations':N+1,'transitions':N,'overlapping_windows':n,
        'word_statistic_sum':str(word_sum),'boundary_contribution':str(boundary),
        'C':str(C),'M':str(M),'theta':str(theta),
        'martingale_cost_upper_preview':float(noise),'entropy_kernel_cost_upper_preview':float(kernel),
        'family_alpha':str(alpha),'horizon_alpha':str(spent),'time_uniform':time_uniform,
        'lower_endpoint':fraction_json(lower),'lower_preview':float(lower),
        'negative_endpoints_retained':True,'positive_path_entropy_certified':lower>0,
        'exact_entropy_cone_columns_checked':cert['columns_checked'],
        'source_generator_or_mixing_input':None,
        'selection_contract':'frozen certificate or prior alpha allocation required'}


def evaluate(cert,record,alpha=Q(1,40),time_uniform=False):
    return from_statistic(cert,*scan(cert,record),alpha,time_uniform)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('certificate',type=Path);p.add_argument('record',type=Path)
    p.add_argument('--alpha',default='1/40');p.add_argument('--time-uniform',action='store_true')
    args=p.parse_args()
    cert=load(args.certificate)
    print(json.dumps(evaluate(cert,json.loads(args.record.read_text()),Q(args.alpha),args.time_uniform),indent=2))


if __name__=='__main__':main()
