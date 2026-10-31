#!/usr/bin/env python3
"""Transport fixed-horizon path-entropy certificates between checkpoints.

Inference is uniform over time by calibrated FUTURE ENTROPY DESCENT, not by
claiming that the observable fixed-horizon e-values are supermartingales.
All witnesses, weights and checkpoint schedules must be predeclared.
"""
from fractions import Fraction as Q
from collections import deque
from pathlib import Path
import argparse
import json

from entropy_cone import load,log_bounds
from quadratic_trace import from_score,fraction_json
from general_trace import from_statistic


def checkpoints(mode='dense'):
    j=0;k=1
    while True:
        if mode=='dense':
            for r in range(k):
                j+=1
                yield j,2**k+(r*2**k)//k
        elif mode=='dyadic':
            j+=1;yield j,2**k
        else:raise ValueError('unknown deterministic checkpoint schedule')
        k+=1


def endpoint(result):
    value=result['lower_endpoint']
    return Q(int(value['numerator']),int(value['denominator']))


def round_lower(x):
    scale=2**96;scaled=x*scale
    return Q(scaled.numerator//scaled.denominator,scale)


def prepare(entries=None):
    if entries is None:entries=[{'name':'analytic_lag_two','kind':'quadratic','weight':'1'}]
    prepared=[];weights=[];alphabet=None
    for i,entry in enumerate(entries):
        weight=Q(entry['weight']);weights.append(weight)
        out={'name':entry.get('name',f'witness_{i+1}'),'kind':entry['kind'],'weight':weight}
        if entry['kind'] in ('quadratic','reflection'):
            s,L=2,1
            if entry['kind']=='reflection':out['lambda']=Q(entry.get('lambda','1/10'))
        elif entry['kind']=='grid':
            cert=load(entry['path']);out['certificate']=cert
            s,L=cert['alphabet'],cert['depth']
            out['lookup']=dict(zip(cert['words'],cert['W']))
        else:raise ValueError('unknown witness kind')
        if alphabet is not None and alphabet!=s:raise ValueError('witness alphabets differ')
        alphabet=s;out['depth']=L;prepared.append(out)
    if not prepared or any(w<=0 for w in weights) or sum(weights)>1:
        raise ValueError('positive inference weights must sum to at most one')
    return prepared,alphabet


def evaluate(symbols,alpha=Q(1,40),entries=None,mode='dense',keep_history=False,threshold=None):
    alpha=Q(alpha)
    if not 0<alpha<1:raise ValueError('invalid alpha')
    prepared,alphabet=prepare(entries)
    for entry in prepared:
        entry['window']=deque(maxlen=2*entry['depth']+1);entry['total']=Q(0)
    baseline=round_lower(log_bounds(alpha/2)[0])
    best=baseline;active=None;history=[];first_threshold=None
    schedule=checkpoints(mode);next_j,next_N=next(schedule)
    observations=0;inference_evaluations=0
    for symbol in symbols:
        if not isinstance(symbol,int) or not 0<=symbol<alphabet:raise ValueError('invalid observed symbol')
        observations+=1;N=observations-1
        for entry in prepared:
            window=entry['window'];window.append(symbol)
            if len(window)==window.maxlen:
                if entry['kind'] in ('quadratic','reflection'):entry['total']+=1 if window[0]==window[2] else -1
                else:entry['total']+=entry['lookup'][tuple(window)]
        if N!=next_N:continue
        allocation=alpha/Q(4*next_j*(next_j+1))
        local=[]
        for entry in prepared:
            if N<2*entry['depth']:continue
            risk=allocation*entry['weight']
            if entry['kind']=='quadratic':result=from_score(N,int(entry['total']),risk,False)
            elif entry['kind']=='reflection':
                lam=entry['lambda'];n=N-1
                log_e=-lam*entry['total']-2*n*lam*lam
                lower=round_lower(2*(log_e+log_bounds(risk,40+N.bit_length())[0]))
                result={'lower_endpoint':fraction_json(lower),'lower_preview':float(lower)}
            else:result=from_statistic(entry['certificate'],N,entry['total'],risk,False)
            inference_evaluations+=1
            local.append((endpoint(result),entry['name'],result))
        if local:
            inference,name,result=max(local,key=lambda x:x[0])
            descent=log_bounds(allocation,40+N.bit_length())[0]
            transported=round_lower(inference+descent)
            point={'checkpoint_index':next_j,'transitions':N,'inference_risk':str(allocation),
                'future_descent_risk':str(allocation),'witness':name,
                'fixed_horizon_endpoint':fraction_json(inference),
                'fixed_horizon_endpoint_preview':float(inference),
                'descent_allowance_preview':float(descent),
                'transported_endpoint':fraction_json(transported),
                'transported_endpoint_preview':float(transported)}
            if transported>best:
                best=transported;active=point
            point['running_lower_endpoint']=fraction_json(best)
            if threshold is not None and first_threshold is None and best>=Q(threshold):
                first_threshold={'transitions':N,'observations':N+1,'lower_preview':float(best)}
            if keep_history:history.append(point)
        next_j,next_N=next(schedule)
    if observations<1:raise ValueError('empty record')
    return {'target':'realised full hidden path entropy in nats',
        'observations':observations,'transitions':observations-1,
        'time_uniform':True,'family_alpha':str(alpha),'checkpoint_schedule':mode,
        'lower_endpoint':fraction_json(best),'lower_preview':float(best),
        'positive_path_entropy_certified':best>0,'negative_endpoints_retained':True,
        'active_checkpoint':active,'checkpoints_evaluated':next_j-1,
        'inference_evaluations':inference_evaluations,
        'first_threshold_crossing':first_threshold,
        'baseline_risk':str(alpha/2),
        'baseline_lower_endpoint':fraction_json(baseline),
        'budget':'inference and future-descent each alpha/[4j(j+1)]',
        'inference_contract':'fixed witnesses, weights and deterministic checkpoint schedule',
        'continuation_contract':'same stationary all-even Markov dynamics continues',
        'mechanism':'conditional entropy likelihood-ratio supermartingale; no observed-statistic martingale asserted',
        'history':history if keep_history else None}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('record',type=Path);p.add_argument('--alpha',default='1/40')
    p.add_argument('--library',type=Path);p.add_argument('--mode',choices=['dense','dyadic'],default='dense')
    p.add_argument('--history',action='store_true');p.add_argument('--threshold')
    args=p.parse_args();entries=None
    if args.library:
        entries=json.loads(args.library.read_text())
        for entry in entries:
            if entry['kind']=='grid' and not Path(entry['path']).is_absolute():
                entry['path']=str((args.library.parent/entry['path']).resolve())
    print(json.dumps(evaluate(json.loads(args.record.read_text()),Q(args.alpha),entries,args.mode,args.history,args.threshold),indent=2))


if __name__=='__main__':main()
