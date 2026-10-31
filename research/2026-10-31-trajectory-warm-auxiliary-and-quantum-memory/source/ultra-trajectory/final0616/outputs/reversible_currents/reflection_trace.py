#!/usr/bin/env python3
"""Frozen lag-two reflection test on one stationary binary record.

The null guarantee requires a stationary all-even reversible hidden Markov
chain. It requires no mixing envelope. This is the ordinary comparator in
PREDICTIVE_DUAL_PROOF.txt, not a claimed new reflection principle.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json

from currents import fraction_json, log_bounds
from dual_trace import rate_lower


def evaluate(record, alpha=Q(1,40)):
    alpha=Q(alpha)
    if len(record)<3 or any(a not in (0,1) for a in record):
        raise ValueError('supply at least three binary observations')
    if not 0<alpha<1:
        raise ValueError('alpha must lie between zero and one')
    n=len(record)-2
    score=sum(1 if a==b else -1 for a,b in zip(record,record[2:]))
    exponent=Q(min(score,0)**2,8*n)
    loglo,loghi=log_bounds(1/alpha)
    lower=rate_lower(exponent,len(record)-1,alpha)
    return {'observations':len(record),'transitions':len(record)-1,
        'overlapping_triples':n,'lag_two_product_sum':score,
        'null_tail_exponent':fraction_json(exponent),
        'null_tail_bound':'exp(-null_tail_exponent)',
        'reject_reversible':exponent>=loghi,
        'decision_unresolved_by_log_precision':loglo<=exponent<loghi,
        'alpha':fraction_json(alpha),'rate_lower_per_step':fraction_json(lower),
        'rate_lower_preview':float(lower),
        'contract':'fixed statistic; fixed horizon; one hidden-stationary record'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('record',type=Path,help='JSON list of binary observations')
    p.add_argument('--alpha',default='1/40')
    args=p.parse_args()
    print(json.dumps(evaluate(json.loads(args.record.read_text()),Q(args.alpha)),indent=2))


if __name__=='__main__':
    main()
