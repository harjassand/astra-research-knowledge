#!/usr/bin/env python3
"""Hidden midpoint entropy witness, using ONLY recorded adjacent binary pairs."""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'entropy_witnesses'))
from checkpoint_band import checkpoints,round_lower,endpoint
from entropy_cone import log_bounds,exponential_bounds
from quadratic_trace import ceil_sqrt,fraction_json


def from_score(N,S,alpha=Q(1,40),method='midpoint',lam=Q(1,25)):
    alpha=Q(alpha)
    if not isinstance(N,int) or N<1 or abs(S)>N or (N-S)%2:raise ValueError('invalid score')
    if not 0<alpha<1:raise ValueError('invalid confidence risk')
    terms=40+N.bit_length()
    if method=='midpoint':
        ell=log_bounds(2/alpha,terms)[1]
        denominator=max(2,int(ceil_sqrt(Q(16*N)/ell)))
        theta=Q(1,denominator)
        noise=8*ceil_sqrt(2*N*ell,48)
        kernel=16*N*theta+ell/theta
        lower=-4*S-noise-kernel
        constants={'theta':str(theta),'martingale_cost_upper_preview':float(noise),
                   'entropy_kernel_cost_upper_preview':float(kernel),'boundary_cost':'0'}
    elif method=='psd':
        lam=Q(lam)
        if lam<0:raise ValueError('lambda must be nonnegative and predeclared')
        elo,ehi=exponential_bounds(lam,80)
        coshhi=(ehi+1/elo)/2
        logcoshhi=log_bounds(coshhi,terms)[1]
        lower=2*(-lam*S-N*logcoshhi+log_bounds(alpha,terms)[0])
        constants={'lambda':str(lam),'logcosh_upper_preview':float(logcoshhi)}
    else:raise ValueError('unknown method')
    lower=round_lower(lower)
    return {'target':'realised full hidden CTMC path entropy in nats',
            'method':method,'transitions':N,'observations':N+1,'adjacent_product_sum':S,
            'alpha':str(alpha),'lower_endpoint':fraction_json(lower),'lower_preview':float(lower),
            'negative_endpoints_retained':True,**constants,
            'required_model':'stationary time-homogeneous all-even CTMC; fixed binary state observation at equal intervals',
            'inference_source_parameters':None,'unobserved_midpoints_acquired':0}


def evaluate(symbols,alpha=Q(1,40),method='midpoint',lam=Q(1,25),keep_history=False,threshold=None):
    alpha=Q(alpha)
    if not 0<alpha<1:raise ValueError('invalid confidence risk')
    iterator=iter(symbols)
    try:left=next(iterator)
    except StopIteration:raise ValueError('empty record')
    if not isinstance(left,int) or left not in (0,1):raise ValueError('invalid binary symbol')
    baseline=round_lower(log_bounds(alpha/2)[0]);best=baseline;active=None;history=[];first=None
    schedule=checkpoints();j,next_N=next(schedule);S=0;N=0;checks=0
    for right in iterator:
        if not isinstance(right,int) or right not in (0,1):raise ValueError('invalid binary symbol')
        S+=1 if left==right else -1;left=right;N+=1
        if N!=next_N:continue
        allocation=alpha/Q(4*j*(j+1));fixed=from_score(N,S,allocation,method,lam)
        transported=round_lower(endpoint(fixed)+log_bounds(allocation,40+N.bit_length())[0])
        point={'checkpoint_index':j,'transitions':N,'adjacent_product_sum':S,
               'inference_risk':str(allocation),'future_descent_risk':str(allocation),
               'fixed_horizon_endpoint':fixed['lower_endpoint'],
               'transported_endpoint':fraction_json(transported)}
        if transported>best:best=transported;active=point
        point['running_lower_endpoint']=fraction_json(best)
        if threshold is not None and first is None and best>=Q(threshold):
            first={'transitions':N,'observations':N+1,'lower_endpoint':fraction_json(best),
                   'lower_preview':float(best)}
        if keep_history:history.append(point)
        checks+=1;j,next_N=next(schedule)
    return {'target':'realised full hidden CTMC path entropy in nats','method':method,
            'time_uniform':True,'family_alpha':str(alpha),'transitions':N,'observations':N+1,
            'adjacent_product_sum':S,'lower_endpoint':fraction_json(best),'lower_preview':float(best),
            'baseline_lower_endpoint':fraction_json(baseline),'baseline_risk':str(alpha/2),
            'active_checkpoint':active,'checkpoints_evaluated':checks,
            'first_threshold_crossing':first,'history':history if keep_history else None,
            'negative_endpoints_retained':True,'unobserved_midpoints_acquired':0,
            'schedule':'predeclared dense integer schedule; inference/descent each alpha/[4j(j+1)]',
            'model_contract':'stationary time-homogeneous all-even CTMC at equal intervals',
            'continuation_contract':'same dynamics continues; future entropy descent charged',
            'inference_source_parameters':None}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('record',type=Path)
    p.add_argument('--alpha',default='1/40');p.add_argument('--method',choices=['midpoint','psd'],default='midpoint')
    p.add_argument('--lambda',dest='lam',default='1/25');p.add_argument('--threshold');p.add_argument('--history',action='store_true')
    args=p.parse_args()
    print(json.dumps(evaluate(json.loads(args.record.read_text()),Q(args.alpha),args.method,Q(args.lam),args.history,args.threshold),indent=2))


if __name__=='__main__':main()
