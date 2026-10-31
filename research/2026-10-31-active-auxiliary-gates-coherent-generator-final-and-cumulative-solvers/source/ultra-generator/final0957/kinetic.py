#!/usr/bin/env python3
"""Certify the required MAXIMUM hidden CTMC escape rate from Poisson labels.

This is not stationary mean activity or entropy production. Inputs require
a stationary hidden CTMC, a fixed binary state label and a known independent
Poisson inspection rate. Hidden state count and mixing are not inputs.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'entropy_witnesses'))
from checkpoint_band import checkpoints
from entropy_cone import log_bounds


def kl_bounds(N,d,q,terms):
    p=Q(d,N);lo=hi=Q(0)
    if d:
        a,b=log_bounds(p/q,terms);lo+=d*a;hi+=d*b
    if d<N:
        a,b=log_bounds((1-p)/(1-q),terms);lo+=(N-d)*a;hi+=(N-d)*b
    return lo,hi


def lower_probability(N,d,alpha,max_probability=Q(1,2),bits=32):
    alpha=Q(alpha);maximum=Q(max_probability)
    if N<1 or not isinstance(d,int) or not 0<=d<=N or not 0<alpha<1:raise ValueError('invalid count or risk')
    if d==0:return Q(0),False
    p=Q(d,N);terms=40+N.bit_length();elllo,ellhi=log_bounds(1/alpha,terms)
    if p>maximum and maximum<1:
        lower,upper=kl_bounds(N,d,maximum,terms)
        if lower>=ellhi:return maximum,True
    lo=Q(0);hi=min(p,maximum);tolerance=Q(1,2**bits)
    while hi-lo>tolerance:
        mid=(lo+hi)/2
        while True:
            elllo,ellhi=log_bounds(1/alpha,terms)
            lower,upper=kl_bounds(N,d,mid,terms)
            if lower>=ellhi:lo=mid;break
            if upper<=elllo:hi=mid;break
            # Exact equality is possible for rational Chernoff probabilities.
            # Bracket around the ambiguous candidate instead of assuming
            # that more log terms must eventually decide its sign.
            left=max(lo,mid-tolerance/4);right=min(hi,mid+tolerance/4)
            left_ok=left==0 or kl_bounds(N,d,left,terms)[0]>=ellhi
            right_ok=right==p or kl_bounds(N,d,right,terms)[1]<=elllo
            if left_ok and right_ok:lo,hi=left,right;break
            terms+=16
    return lo,False


def from_counts(N,d,clock=Q(1),alpha=Q(1,40),method='coherent',bits=None):
    clock=Q(clock);alpha=Q(alpha)
    if clock<=0:raise ValueError('positive calibrated independent inspection rate required')
    if bits is None:bits=32+N.bit_length()
    if method=='coherent':maximum=Q(1,2)
    elif method=='row_hazard':maximum=Q(1)
    else:raise ValueError('unknown kinetic bound')
    q,rejected=lower_probability(N,d,alpha,maximum,bits)
    if rejected:
        rate='infinity';preview=None
    else:
        value=clock*q/(1-2*q) if method=='coherent' else clock*q/(1-q)
        rate=str(value);preview=float(value)
    return {'target':'maximum total hidden CTMC escape rate',
            'method':method,'intervals':N,'observations':N+1,'observed_label_changes':d,
            'inspection_rate':str(clock),'alpha':str(alpha),'flip_probability_lower':str(q),
            'lower_rate':rate,'lower_preview':preview,
            'all_finite_caps_rejected_under_model':rejected,
            'probability_precision_bits':bits,'mean_activity_or_entropy_target':False}


def at_least(rate,target):return rate=='infinity' or Q(rate)>=Q(target)


def evaluate(symbols,clock=Q(1),alpha=Q(1,40),method='coherent',threshold=None,keep_history=False):
    clock,alpha=Q(clock),Q(alpha)
    if clock<=0 or not 0<alpha<1:raise ValueError('invalid clock/risk')
    iterator=iter(symbols)
    try:left=next(iterator)
    except StopIteration:raise ValueError('empty record')
    if not isinstance(left,int) or left not in (0,1):raise ValueError('invalid binary symbol')
    N=d=0;schedule=checkpoints();j,nextN=next(schedule);latest='0';first=None;history=[];active=None
    for right in iterator:
        if not isinstance(right,int) or right not in (0,1):raise ValueError('invalid binary symbol')
        N+=1;d+=int(left!=right);left=right
        if N!=nextN:continue
        allocation=alpha/Q(j*(j+1));point=from_counts(N,d,clock,allocation,method)
        point.update(checkpoint_index=j,checkpoint_risk=str(allocation));latest=point['lower_rate'];active=point
        if first is None and threshold is not None and at_least(latest,threshold):
            first={'intervals':N,'observations':N+1,'lower_rate':latest,'lower_preview':point['lower_preview']}
        if keep_history:history.append(point)
        j,nextN=next(schedule)
    return {'target':'maximum total hidden CTMC escape rate','method':method,
            'time_uniform':True,'alpha':str(alpha),'inspection_rate':str(clock),
            'intervals':N,'observations':N+1,'observed_label_changes':d,
            'lower_rate':latest,'lower_preview':None if latest=='infinity' else float(Q(latest)),
            'first_threshold_crossing':first,'latest_checkpoint':active,'history':history if keep_history else None,
            'endpoint_rule':'latest checkpoint; no uncharged running-max consistency claim',
            'budget':'alpha/[j(j+1)] at deterministic dense checkpoints',
            'assumptions':'stationary homogeneous hidden CTMC; deterministic binary state label; known independent Poisson clock',
            'not_estimated':['hidden state count','mixing time','stationary mean jump activity','entropy production']}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('record',type=Path)
    p.add_argument('--clock',required=True);p.add_argument('--alpha',default='1/40')
    p.add_argument('--method',choices=['coherent','row_hazard'],default='coherent');p.add_argument('--threshold');p.add_argument('--history',action='store_true')
    args=p.parse_args()
    print(json.dumps(evaluate(json.loads(args.record.read_text()),Q(args.clock),Q(args.alpha),args.method,args.threshold,args.history),indent=2))


if __name__=='__main__':main()
