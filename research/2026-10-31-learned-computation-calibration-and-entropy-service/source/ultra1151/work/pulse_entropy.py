#!/usr/bin/env python3
"""Finite kinetic-pulse entropy receiver. No hidden generator input.

Trials must be independent stationary preparations. A prescribed symmetric
rate multiplier bounded by M is a physical assumption, with known exposure
B=integral M dt. The extra nonnegative-covariance witness requires a constant
pulse. This is fixed-n stationary mean entropy inference, not pulse path heat.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'work'))
from kinetic_incumbent_control import inverse_tail
sys.path.insert(0, str(ROOT / 'outputs/reversible_currents'))
from currents import log_bounds


def enclose(lo, hi, bits=112):
    scale = 2**bits
    a, b = lo*scale, hi*scale
    return F(a.numerator//a.denominator, scale), F(-((-b.numerator)//b.denominator), scale)


def down(x, bits=96):
    return enclose(F(x), F(x), bits)[0]


@lru_cache(maxsize=1024)
def logs(x):
    return enclose(*log_bounds(F(x), 64))


def linear_min(coefficients, box):
    """Exact LP over box intersect simplex; return primal attaining vertex."""
    if len(coefficients) != 4 or len(box) != 4:
        raise ValueError('four endpoint cells required')
    low, high = [F(x[0]) for x in box], [F(x[1]) for x in box]
    if any(not 0 <= a <= b <= 1 for a, b in zip(low, high)):
        raise ValueError('invalid probability box')
    if not sum(low) <= 1 <= sum(high):
        raise ValueError('empty probability box/simplex intersection')
    p = low[:]
    left = 1-sum(p)
    for j in sorted(range(4), key=lambda j: coefficients[j]):
        amount = min(left, high[j]-p[j])
        p[j] += amount
        left -= amount
    assert left == 0 and sum(p) == 1
    return sum((c*x for c, x in zip(coefficients, p)), F(0)), p


def linear_range(coefficients, box):
    low = linear_min(coefficients, box)[0]
    high = -linear_min([-c for c in coefficients], box)[0]
    return low, high


def cp_box(counts, alpha):
    n = sum(counts)
    if n < 1 or len(counts) != 4 or any(type(c) is not int or c < 0 for c in counts):
        raise ValueError('four nonnegative integer counts required')
    alpha = F(alpha)
    if not 0 < alpha < 1:
        raise ValueError('risk must be strictly between zero and one')
    box, work = [], 0
    for c in counts:
        left, _, calls = inverse_tail(n, c, alpha/8)
        complement, _, more = inverse_tail(n, n-c, alpha/8)
        box.append((left, 1-complement))
        work += calls+more
    assert sum(a for a, b in box) <= 1 <= sum(b for a, b in box)
    return box, work


def dual_witness(box, z=F(1), w=F(3), v=F(1), Z0=F(13, 10), r0=F(1, 3), constant=True):
    z, w, v, Z0, r0 = map(F, (z, w, v, Z0, r0))
    if z <= 0 or w <= 0 or v < 1 or Z0 <= 0 or r0 < 0:
        raise ValueError('invalid exponential witness')
    if v != 1 and not constant:
        raise ValueError('positive covariance requires a constant pulse')
    lwlo, lwhi = logs(z*w)
    clo, chi = logs(v)
    Zlo, Zhi = logs(Z0)
    intercept = 1-Zhi-chi*r0*r0
    coeff = [-weight/Z0 for weight in (F(1), w, z, z*w*v)]
    for j in (2, 3):
        coeff[j] += lwlo+2*r0*clo
    value, vertex = linear_min(coeff, box)
    return down(intercept+value), {'z': str(z), 'w': str(w), 'v': str(v),
        'Z0': str(Z0), 'r0': str(r0), 'worst_box_vertex': list(map(str, vertex)),
        'certified_KL_lower': str(down(intercept+value)),
        'arithmetic': 'directed rational logs, tangent lower bounds, exact box/simplex LP'}


def binary_kl_lower(r, s):
    r, s = F(r), F(s)
    if not 0 <= r <= 1 or not 0 < s < 1:
        raise ValueError('KL endpoint outside finite-data interior')
    ans = F(0)
    if r:
        ans += r*logs(r/s)[0]
    if r < 1:
        ans += (1-r)*logs((1-r)/(1-s))[0]
    return max(F(0), down(ans))


def ordinary_bounds(box, B):
    r = linear_range([0, 0, 1, 1], box)
    s = linear_range([0, 1, 0, 1], box)
    delta = linear_range([0, 1, -1, 0], box)
    if r[0] > s[1]:
        kl = binary_kl_lower(r[0], s[1])
    elif s[0] > r[1]:
        kl = binary_kl_lower(r[1], s[0])
    else:
        kl = F(0)
    separation = max(F(0), delta[0], -delta[1])
    return {'initial_mean_interval': list(map(str, r)),
        'terminal_mean_interval': list(map(str, s)),
        'paired_mean_change_interval': list(map(str, delta)),
        'ordinary_marginal_KL_rate_lower': str(down(4*kl/B)),
        'ordinary_paired_Pinsker_rate_lower': str(down(8*separation**2/B))}


def propose(p, constant):
    """Conventional numerical dual optimizer proposes, never certifies."""
    import numpy as np
    from scipy.optimize import minimize
    p = np.array([float(x) for x in p])
    r = p[2]+p[3]
    rows = []
    for corr in ([False, True] if constant else [False]):
        def objective(t):
            a, b, c = t
            f = np.array([0, b, a, a+b+c])
            shift = max(f)
            return np.log(p @ np.exp(f-shift))+shift-(a+b)*r-c*r*r
        fit = minimize(objective, [0, 0, 0], method='L-BFGS-B',
            bounds=[(-10, 10), (-10, 10), (0, 10) if corr else (0, 0)],
            options={'ftol': 1e-13, 'gtol': 1e-9, 'maxiter': 200})
        weights = [F(float(math.exp(float(t)))).limit_denominator(10000) for t in fit.x]
        weights[2] = max(F(1), weights[2])
        rows.append({'positive_covariance': corr, 'success': bool(fit.success),
            'iterations': int(fit.nit), 'empirical_KL_objective_preview': -float(fit.fun),
            'weights': list(map(str, weights)),
            'role': 'post-data proposal valid only through exact receiver on simultaneous set'})
    return rows


def evaluate(record, B, alpha=F(1, 80), constant=True):
    start = time.perf_counter()
    B, alpha = F(B), F(alpha)
    if B <= 0:
        raise ValueError('positive known amplitude-time exposure required')
    if not record or any(type(x) is not int or x not in range(4) for x in record):
        raise ValueError('nonempty record of endpoint cells 2*x+y required')
    counts = [record.count(j) for j in range(4)]
    n = len(record)
    p = [F(c, n) for c in counts]
    box, recurrence = cp_box(counts, alpha)
    incumbent = ordinary_bounds(box, B)
    fixed, receipt = dual_witness(box, constant=constant)
    witnesses = [dict(name='frozen_z1_w3_v1_Z13over10', **receipt)]
    best = max(F(0), fixed)
    proposals = propose(p, constant)
    for k, proposal in enumerate(proposals):
        z, w, v = map(F, proposal['weights'])
        Z0 = p[0]+w*p[1]+z*p[2]+z*w*v*p[3]
        value, row = dual_witness(box, z, w, v, Z0, p[2]+p[3], constant)
        witnesses.append(dict(name=f'empirical_dual_proposal_{k}', **row))
        best = max(best, value)
    dual_rate = down(4*best/B)
    lower = max(dual_rate, F(incumbent['ordinary_marginal_KL_rate_lower']),
        F(incumbent['ordinary_paired_Pinsker_rate_lower']))
    return {'target': 'zero-field stationary mean entropy production rate',
        'units': 'nats per supplied physical time unit', 'independent_stationary_trials': n,
        'readouts': 2*n, 'endpoint_cell_order': ['00', '01', '10', '11'], 'counts': counts,
        'alpha_fixed_n': str(alpha), 'one_sided_cell_tail_risk': str(alpha/8),
        'amplitude_time_exposure_B': str(B), 'constant_pulse': constant,
        'probability_box': [[str(a), str(b)] for a, b in box],
        'empirical_initial_mean': str(p[2]+p[3]), 'empirical_terminal_mean': str(p[1]+p[3]),
        'witnesses': witnesses, 'floating_proposals': proposals,
        'pair_reference_dual_rate_lower': str(dual_rate),
        'ordinary_shared_method_comparators': incumbent,
        'rate_lower': str(lower), 'rate_lower_preview': float(lower),
        'binomial_positive_recurrence_steps': recurrence,
        'hidden_state_count_rate_cap_rank_or_generator_inputs': False,
        'not_observed': ['microscopic jumps', 'pulse path entropy', 'full controlled law'],
        'coverage_requires': ['independent stationary preparations of the same generator',
            'deterministic calibrated binary state sensor', 'all-even reciprocal CTMC',
            'prescribed symmetric microscopic rate multiplication',
            'known amplitude envelope and physical pulse duration'],
        'CPU_wall_seconds': time.perf_counter()-start}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--exposure', required=True)
    parser.add_argument('--alpha', default='1/80')
    parser.add_argument('--time-varying', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    row = evaluate(json.loads(args.record.read_text()), F(args.exposure), F(args.alpha), not args.time_varying)
    row['receiver_code_SHA256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    text = json.dumps(row, indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text)


if __name__ == '__main__':
    main()
