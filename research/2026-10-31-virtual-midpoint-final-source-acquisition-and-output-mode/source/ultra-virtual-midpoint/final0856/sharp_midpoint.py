#!/usr/bin/env python3
"""Selection-charged sharp midpoint library, attaining the first root layer."""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json

from midpoint_band import log_bounds,ceil_sqrt,fraction_json,round_lower,endpoint,checkpoints


def bias(index):
    if index<1:raise ValueError('positive witness index required')
    if index==1:return Q(0)
    n=index-1;level=n.bit_length();first=2**(level-1)
    return Q(2*(n-first)+1,2**level)


def coefficients(b,terms):
    b=Q(b)
    if not 0<=b<1:raise ValueError('require0<=b<1')
    if b==0:return Q(2),Q(2),Q(0),Q(0)
    lo,hi=log_bounds((1+b)/(1-b),terms);lo/=2;hi/=2
    lamlo=lo/b+1/(1-b*b);lamhi=hi/b+1/(1-b*b)
    clo=max(Q(0),b*b/(1-b*b)-b*hi);chi=b*b/(1-b*b)-b*lo
    return lamlo,lamhi,clo,chi


def from_score(N,S,b,alpha):
    alpha=Q(alpha);b=Q(b)
    if N<1 or abs(S)>N or (N-S)%2 or not 0<alpha<1:raise ValueError('invalid score/risk')
    terms=40+N.bit_length();lamlo,lamhi,clo,chi=coefficients(b,terms)
    ell=log_bounds(2/alpha,terms)[1]
    denom=max(2,int(ceil_sqrt(4*N*lamhi*lamhi/ell)));theta=Q(1,denom)
    noise=4*lamhi*ceil_sqrt(2*N*ell,48)
    kernel=4*N*lamhi*lamhi*theta+ell/theta
    score=min(-2*lamlo*S,-2*lamhi*S)-2*N*chi
    lower=round_lower(score-noise-kernel)
    return {'b':str(b),'lambda_interval':[str(lamlo),str(lamhi)],
            'quadratic_intercept_interval':[str(clo),str(chi)],'theta':str(theta),
            'alpha':str(alpha),'lower_endpoint':fraction_json(lower),'lower_preview':float(lower)}


def evaluate(symbols,alpha=Q(1,40),keep_history=False,threshold=None):
    alpha=Q(alpha)
    if not 0<alpha<1:raise ValueError('invalid confidence risk')
    iterator=iter(symbols)
    try:left=next(iterator)
    except StopIteration:raise ValueError('empty record')
    if left not in (0,1):raise ValueError('invalid binary symbol')
    baseline=round_lower(log_bounds(alpha/2)[0]);best=baseline;active=None;first=None;history=[]
    schedule=checkpoints();j,nextN=next(schedule);S=N=evaluations=0
    for right in iterator:
        if right not in (0,1):raise ValueError('invalid binary symbol')
        S+=1 if left==right else -1;left=right;N+=1
        if N!=nextN:continue
        allocation=alpha/Q(4*j*(j+1));count=N.bit_length()
        result=max((from_score(N,S,bias(i),allocation/2**i) for i in range(1,count+1)),key=endpoint)
        evaluations+=count
        transported=round_lower(endpoint(result)+log_bounds(allocation,40+N.bit_length())[0])
        point={'transitions':N,'checkpoint_index':j,'witness':result['b'],
               'candidate_count':count,'inference_risk':str(allocation),
               'future_descent_risk':str(allocation),'transported_endpoint':fraction_json(transported)}
        if transported>best:best=transported;active=point
        point['running_lower_endpoint']=fraction_json(best)
        if first is None and threshold is not None and best>=Q(threshold):
            first={'transitions':N,'lower_endpoint':fraction_json(best),'lower_preview':float(best)}
        if keep_history:history.append(point)
        j,nextN=next(schedule)
    return {'target':'realised full hidden CTMC path entropy; also valid for Markov square roots',
            'time_uniform':True,'alpha':str(alpha),'transitions':N,'observations':N+1,
            'adjacent_product_sum':S,'lower_endpoint':fraction_json(best),'lower_preview':float(best),
            'active_checkpoint':active,'first_threshold_crossing':first,
            'critic_evaluations':evaluations,'history':history if keep_history else None,
            'selection_charge':'predeclared dyadic b_j; weight2^-j; J_N=bit_length(N)',
            'asymptotic_contract':'2phi(sqrt r) for the complete binary Markov law with eigenvalue-r',
            'streaming_state':'one previous bit and integer count/score; all critics share the statistic',
            'negative_endpoints_retained':True,'source_parameters_supplied':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('record',type=Path)
    p.add_argument('--alpha',default='1/40');p.add_argument('--history',action='store_true');p.add_argument('--threshold')
    args=p.parse_args()
    print(json.dumps(evaluate(json.loads(args.record.read_text()),Q(args.alpha),args.history,args.threshold),indent=2))


if __name__=='__main__':main()
