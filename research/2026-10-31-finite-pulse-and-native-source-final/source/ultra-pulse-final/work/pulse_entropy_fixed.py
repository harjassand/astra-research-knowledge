#!/usr/bin/env python3
"""General fixed-witness receiver; avoids optional fitted-dual boundary issues.

The frozen study is retained verbatim. This entry point uses its exact CP,
KL and linear receivers with strictly positive predeclared weights. It makes
no optimizer calls beyond the certified inverse-binomial endpoint proposer.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'work'))
from pulse_entropy import cp_box, ordinary_bounds, dual_witness, down


def evaluate(record, B, alpha=F(1, 80)):
    start = time.perf_counter()
    B, alpha = F(B), F(alpha)
    if B <= 0 or not record or any(type(c) is not int or c not in range(4) for c in record):
        raise ValueError('positive exposure and nonempty endpoint-cell record required')
    counts = [record.count(c) for c in range(4)]
    box, work = cp_box(counts, alpha)
    ordinary = ordinary_bounds(box, B)
    best = F(0)
    witnesses = []
    # First witness is exactly the pre-draw power witness.
    proposals = [(F(3), F(13, 10))]
    empirical_terminal = F(counts[1]+counts[3], len(record))
    for w in (F(1, 9), F(1, 3), F(1), F(3), F(9)):
        proposals.append((w, 1+(w-1)*empirical_terminal))
    for w, Z0 in proposals:
        value, receipt = dual_witness(box, z=F(1), w=w, v=F(1), Z0=Z0)
        witnesses.append(receipt)
        best = max(best, value)
    lower = max(down(4*best/B), F(ordinary['ordinary_marginal_KL_rate_lower']),
        F(ordinary['ordinary_paired_Pinsker_rate_lower']))
    return {'target': 'zero-field stationary mean entropy production rate',
        'independent_stationary_trials': len(record), 'counts': counts,
        'alpha_fixed_n': str(alpha), 'exposure_B': str(B),
        'rate_lower': str(lower), 'rate_lower_preview': float(lower),
        'probability_box': [[str(a), str(b)] for a, b in box],
        'ordinary_comparators': ordinary, 'witnesses': witnesses,
        'positive_binomial_tail_recurrence_steps': work,
        'physical_contract': 'independent stationary starts; all-even reciprocal CTMC; calibrated deterministic bit; prescribed symmetric gate bounded in amplitude and physical time',
        'same_trial_feedback_or_general_asymmetric_error': 'NOT_COVERED',
        'CPU_wall_seconds': time.perf_counter()-start}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--exposure', required=True)
    parser.add_argument('--alpha', default='1/80')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = evaluate(json.loads(args.record.read_text()), F(args.exposure), F(args.alpha))
    text = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text)


if __name__ == '__main__':
    main()
