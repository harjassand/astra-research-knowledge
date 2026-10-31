#!/usr/bin/env python3
"""Stronger ordinary two-state binomial-tail incumbent, same acquired bits.

SciPy proposes inverse-beta endpoints. Directed rational binomial tails
independently certify both sides; no floating decision is trusted.
The additional iid-flip premise is true for the two fresh validation
sources. This is NOT an established all-hidden-model confidence band.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import json
import math
import sys
import time
from scipy.special import betaincinv

ROOT=Path(__file__).resolve().parents[1];HERE=ROOT/'outputs/coherent_generator'
sys.path.insert(0,str(HERE))
from kinetic import log_bounds


def integer_log_bounds(value,terms=64):
    shift=max(0,value.bit_length()-96);top=value>>shift
    a,b=log_bounds(top,terms)
    if top<<shift!=value:b=log_bounds(top+1,terms)[1]
    c,d=log_bounds(2,terms)
    return a+shift*c,b+shift*d


def tail_multiplier(N,d,q,bits=128):
    """Tail/pmf(d), with every positive recurrence rounded outwards."""
    assert 0<q<Q(d,N)<=1
    scale=2**bits;lo=hi=scale;total_lo=total_hi=scale;k=d
    while k<N:
        ratio=Q(N-k,k+1)*q/(1-q)
        assert 0<=ratio<1
        x=lo*ratio;lo=x.numerator//x.denominator
        y=hi*ratio;hi=-((-y.numerator)//y.denominator)
        total_lo+=lo;total_hi+=hi;k+=1
        if k==N:break
        following=Q(N-k,k+1)*q/(1-q)
        remainder=hi*following/(1-following)
        if remainder<Q(total_hi,2**80):
            total_hi+=-((-remainder.numerator)//remainder.denominator)
            break
    return Q(total_lo,scale),Q(total_hi,scale),k-d


def tail_log_bounds(N,d,q):
    sl,su,terms=tail_multiplier(N,d,q)
    cl,cu=integer_log_bounds(math.comb(N,d))
    ql,qu=log_bounds(q,64);rl,ru=log_bounds(1-q,64)
    tl,tu=log_bounds(sl,64)[0],log_bounds(su,64)[1]
    return cl+d*ql+(N-d)*rl+tl,cu+d*qu+(N-d)*ru+tu,terms


def inverse_tail(N,d,alpha):
    if d==0:return Q(0),Q(0),0
    proposal=Q(float(betaincinv(d,N-d+1,float(alpha))))
    al,au=log_bounds(alpha,64);margin=Q(1,2**35);calls=0
    while True:
        lo=max(Q(0),proposal-margin);hi=min(Q(d,N),proposal+margin)
        if lo:
            lower,upper,n=tail_log_bounds(N,d,lo);calls+=n
            left_ok=upper<=al
        else:left_ok=True
        if hi<Q(d,N):
            lower,upper,n=tail_log_bounds(N,d,hi);calls+=n
            right_ok=lower>=au
        else:
            # This branch is not needed by the retained controls. Do not
            # assert an uncertified boundary acceptance.
            right_ok=False
        if left_ok and right_ok:return lo,hi,calls
        margin*=2
        if margin>Q(1,1000):raise RuntimeError('proposal not enclosed to useful precision')


def finite_tail_controls():
    cases=0
    for N in range(1,13):
        for d in range(1,N+1):
            for q in (Q(1,10),Q(1,3)):
                if q>=Q(d,N):continue
                lo,hi,n=tail_multiplier(N,d,q)
                pmf=math.comb(N,d)*q**d*(1-q)**(N-d)
                exact=sum((math.comb(N,k)*q**k*(1-q)**(N-k) for k in range(d,N+1)),Q(0))
                assert pmf*lo<=exact<=pmf*hi;cases+=1
    return cases


def main():
    start=time.perf_counter();cases=finite_tail_controls()
    receipt=json.loads((HERE/'kinetic_receipt.json').read_text());out=[];recurrences=0
    for row in receipt['records']:
        first=None;points=[]
        for point in row['coherent']['history']:
            N=point['intervals'];d=point['observed_label_changes'];risk=Q(point['checkpoint_risk'])
            lo,hi,count=inverse_tail(N,d,risk);recurrences+=count
            assert 0<=lo<=hi<Q(1,2),'these source fixtures have finite two-state endpoints'
            rate_lo=lo/(1-2*lo);rate_hi=hi/(1-2*hi)
            if first is None and rate_lo>=3:first={'intervals':N,'lower_preview':float(rate_lo)}
            points.append({'intervals':N,'observed_changes':d,'risk':str(risk),
                           'probability_lower':str(lo),'probability_upper':str(hi),
                           'rate_lower':str(rate_lo),'rate_upper':str(rate_hi),
                           'rate_preview':float(rate_lo),'endpoint_width':float(rate_hi-rate_lo)})
        out.append({'name':row['name'],'exact_two_state_tail_endpoint_preview':points[-1]['rate_preview'],
                    'coherent_unrestricted_hidden_endpoint':row['coherent']['lower_preview'],
                    'first_threshold_crossing':first,'history':points,
                    'tail_incumbent_dominates_coherent_at_all_nonzero_checkpoints':all(
                        Q(p['rate_lower'])>=Q(q['lower_rate']) for p,q in zip(points,row['coherent']['history'])
                        if q['lower_rate']!='infinity')})
    result={'status':'ORDINARY_TWO_STATE_BINOMIAL_TAIL_INCUMBENT_CERTIFIED',
            'additional_assumption':'observed flips iid Bernoulli; valid on these exact two-state sources',
            'not_claimed':'exact binomial-tail dominance for arbitrary hidden CTMCs',
            'same_record_clock_schedule_and_risk':True,'new_acquisitions':0,
            'small_exact_tail_controls':cases,'directed_tail_recurrence_steps':recurrences,
            'records':out,'CPU_elapsed_seconds':time.perf_counter()-start,
            'receiver_arithmetic':'leading-integer log enclosure; positive fixed-point tail sum and geometric remainder',
            'code_SHA256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'earlier_design_and_draws_retained':True}
    (HERE/'kinetic_incumbent_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}|{'records':[
        {k:v for k,v in row.items() if k!='history'} for row in out]},indent=2))


if __name__=='__main__':main()
