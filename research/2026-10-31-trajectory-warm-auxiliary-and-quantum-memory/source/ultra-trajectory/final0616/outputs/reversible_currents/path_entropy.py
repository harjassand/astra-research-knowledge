#!/usr/bin/env python3
"""Confidence lower bounds on REALISED hidden path entropy, not its mean.

Stationary all-even hidden Markov dynamics and predeclared tuning are required.
Endpoints may be negative and MUST NOT be clamped to zero. The accompanying
PATH_ENTROPY_PROOF.txt distinguishes this target from a stationary mean rate.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json
import math
from currents import fraction_json, log_bounds
from dual_trace import trace_statistic


def round_lower(value,bits=96):
    scale=2**bits
    value*=scale
    return Q(value.numerator//value.denominator,scale)


def scan_binary_current(symbols):
    """One pass over any iterable; retain one bit, a count and a score."""
    iterator=iter(symbols)
    try:left=next(iterator)
    except StopIteration:raise ValueError('supply at least two observations')
    if left not in (0,1):raise ValueError('invalid binary symbol')
    n=score=0
    for right in iterator:
        if right not in (0,1):raise ValueError('invalid binary symbol')
        score+=(1 if left==right else -1)*(-1 if n%2 else 1)
        left=right;n+=1
    if n<1:raise ValueError('supply at least two observations')
    return n,score


def current_bound_from_score(n,score,theta=Q(1,16),v=Q(1,2),alpha=Q(1,40),terms=40):
    theta,v,alpha=map(Q,(theta,v,alpha))
    if not 0<theta<=Q(1,2) or not 0<=v<1 or not 0<alpha<1:
        raise ValueError('require 0<theta<=1/2, 0<=v<1, 0<alpha<1')
    if n<1 or abs(score)>n or (n-score)%2:raise ValueError('invalid current score')
    score=abs(score);c=1-2*theta
    avlo,avhi=log_bounds((1+v)/(1-v),terms); avlo/=2; avhi/=2
    acvlo,acvhi=log_bounds((1+c*v)/(1-c*v),terms); acvlo/=2; acvhi/=2
    lamlo=avlo-c*acvhi
    _,logChi=log_bounds((1-c*c*v*v)/(1-v*v),terms);logChi/=2
    logalpha,_=log_bounds(alpha,terms)
    _,log2hi=log_bounds(Q(2),terms)
    lower=round_lower((lamlo*score-n*logChi+logalpha-log2hi)/theta)
    return {'target':'realised total hidden trajectory entropy in nats',
        'observations':n+1,'transitions':n,'absolute_current':score,
        'theta':str(theta),'v':str(v),'alpha':str(alpha),
        'log_series_terms':terms,
        'lower_endpoint':fraction_json(lower),'lower_preview':float(lower),
        'positive_entropy_certified':lower>0,
        'tuning_contract':'theta and v fixed before this record or selection charged',
        'negative_endpoints_retained':True}


def current_bound(record,theta=Q(1,16),v=Q(1,2),alpha=Q(1,40)):
    return current_bound_from_score(*scan_binary_current(record),theta,v,alpha)


def current_grid_from_score(n,score,alpha=Q(1,40)):
    # This entire finite family is predefined, not fitted to the input trace.
    thetas=[Q(1,2**j) for j in range(1,7)]
    values=[Q(j,8) for j in range(1,8)]
    count=len(thetas)*len(values)
    results=[current_bound_from_score(n,score,t,v,Q(alpha)/count) for t in thetas for v in values]
    best=max(results,key=lambda x:Q(int(x['lower_endpoint']['numerator']),int(x['lower_endpoint']['denominator'])))
    return {'candidate_count':count,'family_alpha':str(alpha),
        'selection_charge':'alpha divided by all 42 predeclared candidates',
        'best':best}


def current_grid_bound(record,alpha=Q(1,40)):
    return current_grid_from_score(*scan_binary_current(record),alpha)


def sequential_current_from_score(n,score,alpha=Q(1,40)):
    """The explicit time-uniform, dense-library construction in Section 6.

    This is alpha spending over fixed-horizon inequalities, not an assertion
    that the observed exponential statistic is a supermartingale.
    """
    if n<1:raise ValueError('supply at least two observations')
    root=math.isqrt(math.isqrt(n))
    if root**4<n:root+=1
    theta=Q(1,2*root)
    count=max(1,n.bit_length())
    values=[];level=1
    while len(values)<count:
        for numerator in range(1,2**level,2):
            values.append(Q(numerator,2**level))
            if len(values)==count:break
        level+=1
    terms=40+n.bit_length()
    results=[current_bound_from_score(n,score,theta,v,Q(alpha)/(2**j*n*(n+1)),terms)
             for j,v in enumerate(values,1)]
    best=max(results,key=lambda x:Q(int(x['lower_endpoint']['numerator']),int(x['lower_endpoint']['denominator'])))
    return {'candidate_count':count,'family_alpha':str(alpha),'horizon':n,
        'theta_schedule':str(theta),'selection_charge':'alpha*2^-j/[n(n+1)]',
        'guarantee':'simultaneous realised-path lower endpoints at all integer horizons',
        'source_family_limit':'Section 6, with dyadic dense library and J_n=bit_length(n)',
        'best':best}


def sequential_current_bound(record,alpha=Q(1,40)):
    return sequential_current_from_score(*scan_binary_current(record),alpha)


def exponential_evalue_path_bound(log_evalue,alpha=Q(1,40)):
    logalpha,_=log_bounds(Q(alpha))
    return round_lower(2*(log_evalue+logalpha))


def reflection_bound(record,lam=Q(1,10),alpha=Q(1,40)):
    lam,alpha=Q(lam),Q(alpha)
    if lam<0 or not 0<alpha<1:raise ValueError('invalid tuning')
    if len(record)<3 or any(a not in (0,1) for a in record):raise ValueError('invalid record')
    n=len(record)-2
    score=sum(1 if a==b else -1 for a,b in zip(record,record[2:]))
    log_e=-lam*score-2*n*lam*lam
    lower=exponential_evalue_path_bound(log_e,alpha)
    return {'target':'realised full hidden path entropy in nats',
        'observations':len(record),'transitions':len(record)-1,
        'lambda':str(lam),'alpha':str(alpha),'log_evalue':str(log_e),
        'lower_endpoint':fraction_json(lower),'lower_preview':float(lower),
        'positive_entropy_certified':lower>0,'negative_endpoints_retained':True}


def dual_bound(cert,record,lam=Q(1,4),alpha=Q(1,40)):
    lam,alpha=Q(lam),Q(alpha)
    if lam<0 or not 0<alpha<1:raise ValueError('invalid tuning')
    n,T,_=trace_statistic(cert,record)
    log_e=-lam*T-lam*cert['R']/2-n*lam*lam*cert['C']**2/2
    lower=exponential_evalue_path_bound(log_e,alpha)
    return {'target':'realised full hidden path entropy in nats',
        'observations':len(record),'transitions':len(record)-1,
        'lambda':str(lam),'alpha':str(alpha),'log_evalue':str(log_e),
        'lower_endpoint':fraction_json(lower),'lower_preview':float(lower),
        'positive_entropy_certified':lower>0,'negative_endpoints_retained':True}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('record',type=Path,help='JSON list of binary observations')
    p.add_argument('--method',choices=['current','current_sequence','reflection','dual'],default='current')
    p.add_argument('--alpha',default='1/40')
    p.add_argument('--lambda',dest='lam',help='fixed rational tuning for reflection or dual')
    p.add_argument('--certificate',type=Path,help='verified finite dual, for method dual')
    args=p.parse_args();record=json.loads(args.record.read_text());alpha=Q(args.alpha)
    if args.method=='current':result=current_grid_bound(record,alpha)
    elif args.method=='current_sequence':result=sequential_current_bound(record,alpha)
    elif args.method=='reflection':result=reflection_bound(record,Q(args.lam or '1/10'),alpha)
    else:
        if not args.certificate:p.error('--certificate is required for method dual')
        from dual_trace import load_certificate
        result=dual_bound(load_certificate(args.certificate),record,Q(args.lam or '1/4'),alpha)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
