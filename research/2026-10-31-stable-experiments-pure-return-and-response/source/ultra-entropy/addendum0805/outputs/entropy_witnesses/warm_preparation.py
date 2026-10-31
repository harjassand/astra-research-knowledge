#!/usr/bin/env python3
"""Actual nonstationary path entropy with a certified initial density bound.

Input C means rho_0<=C*pi for a stationary reference pi of the SAME dynamics.
It must be externally certified. It is not estimated from the observation.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import json

from checkpoint_band import evaluate as stationary_band,endpoint,round_lower
from quadratic_trace import fraction_json
from entropy_cone import log_bounds


def evaluate(symbols,density_ratio_bound,alpha=Q(1,40),entries=None,mode='dense',
             keep_history=False,threshold=None):
    C=Q(density_ratio_bound);alpha=Q(alpha)
    if C<1:raise ValueError('preparation density ratio bound must be at least one')
    if not 0<alpha<1:raise ValueError('invalid confidence risk')
    if C==1:
        gamma=alpha;delta=None;shift=Q(0)
    else:
        gamma=alpha/(2*C);delta=alpha/2
        shift=round_lower(log_bounds(delta)[0]-log_bounds(C)[1])
    internal_threshold=None if threshold is None else Q(threshold)-shift
    base=stationary_band(symbols,gamma,entries,mode,keep_history,internal_threshold)
    lower=round_lower(endpoint(base)+shift)
    first=base['first_threshold_crossing']
    if first is not None:first={**first,'lower_preview':first['lower_preview']+float(shift)}
    history=None
    if keep_history:
        history=[{'transitions':p['transitions'],
                  'actual_total_lower_endpoint':fraction_json(round_lower(
                      Q(int(p['running_lower_endpoint']['numerator']),
                        int(p['running_lower_endpoint']['denominator']))+shift))}
                 for p in base['history']]
    return {'target':'actual total nonstationary hidden path entropy in nats',
            'observations':base['observations'],'transitions':base['transitions'],
            'time_uniform':True,'family_alpha':str(alpha),
            'certified_initial_density_ratio_bound':str(C),
            'stationary_reference_risk':str(gamma),
            'initial_boundary_risk':str(delta) if delta is not None else '0',
            'preparation_boundary_allowance':fraction_json(shift),
            'preparation_boundary_allowance_preview':float(shift),
            'lower_endpoint':fraction_json(lower),'lower_preview':float(lower),
            'positive_path_entropy_certified':lower>0,'negative_endpoints_retained':True,
            'first_threshold_crossing':first,'history':history,
            'preparation_contract':'external guarantee rho_0<=C*pi; same stationary-reference dynamics and all-even reversal',
            'stationary_reference_band':base}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('record',type=Path)
    p.add_argument('--density-ratio-bound',required=True)
    p.add_argument('--alpha',default='1/40')
    p.add_argument('--threshold')
    p.add_argument('--history',action='store_true')
    args=p.parse_args()
    print(json.dumps(evaluate(json.loads(args.record.read_text()),args.density_ratio_bound,
                              Q(args.alpha),keep_history=args.history,threshold=args.threshold),indent=2))


if __name__=='__main__':main()
