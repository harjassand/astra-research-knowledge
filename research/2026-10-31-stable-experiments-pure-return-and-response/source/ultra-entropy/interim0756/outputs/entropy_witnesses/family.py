#!/usr/bin/env python3
"""Time-uniform selection over a PREDECLARED finite entropy-witness library.

Adding a certificate after examining this record requires a prior universal
encoding weight; a new arbitrary list index does not supply that charge.
The complete-library limit theorem is in PROOF.txt. This finite driver
recovers only the largest population bound represented by its own library.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json

from entropy_cone import load,log_bounds
from general_trace import evaluate as grid_evaluate
from quadratic_trace import evaluate as quadratic_evaluate,fraction_json


def endpoint(result):
    x=result['lower_endpoint']
    return Q(int(x['numerator']),int(x['denominator']))


def evaluate(record,entries,alpha=Q(1,40)):
    alpha=Q(alpha)
    if not 0<alpha<1:raise ValueError('invalid alpha')
    weights=[Q(entry['weight']) for entry in entries]
    if any(x<=0 for x in weights) or sum(weights)>Q(1,2):
        raise ValueError('positive witness weights must sum to at most 1/2')
    # This baseline uses the ACTUAL hidden likelihood-ratio supermartingale,
    # not optional stopping applied to a fixed-horizon observed statistic.
    lo,_=log_bounds(alpha/2)
    scale=2**96;scaled=lo*scale
    base=Q(scaled.numerator//scaled.denominator,scale)
    candidates=[{'name':'universal_hidden_entropy_infimum_baseline',
        'target':'realised full hidden path entropy in nats',
        'lower_endpoint':fraction_json(base),'lower_preview':float(base),
        'time_uniform':True,'allocated_risk':str(alpha/2)}]
    for i,(entry,weight) in enumerate(zip(entries,weights),1):
        if entry['kind']=='quadratic':result=quadratic_evaluate(record,alpha*weight,True)
        elif entry['kind']=='grid':
            cert=load(entry['path'])
            if len(record)<2*cert['depth']+1:continue
            result=grid_evaluate(cert,record,alpha*weight,True)
        else:raise ValueError('unknown certificate kind')
        candidates.append({'name':entry.get('name',f'witness_{i}'),**result})
    return {'target':'realised full hidden path entropy in nats',
        'family_alpha':str(alpha),'time_uniform':True,
        'selection_contract':'entries and weights fixed before the record, or universal code weights supplied',
        'witness_weight_sum':str(sum(weights)),
        'best':max(candidates,key=endpoint),'all_candidates':candidates,
        'limit_scope':'largest expected word bound represented in this finite family; complete limit requires the complete growing library'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('library',type=Path,help='JSON list of frozen entries and prior weights')
    p.add_argument('record',type=Path);p.add_argument('--alpha',default='1/40')
    args=p.parse_args()
    entries=json.loads(args.library.read_text())
    for entry in entries:
        if entry['kind']=='grid' and not Path(entry['path']).is_absolute():
            entry['path']=str((args.library.parent/entry['path']).resolve())
    print(json.dumps(evaluate(json.loads(args.record.read_text()),entries,Q(args.alpha)),indent=2))


if __name__=='__main__':main()
