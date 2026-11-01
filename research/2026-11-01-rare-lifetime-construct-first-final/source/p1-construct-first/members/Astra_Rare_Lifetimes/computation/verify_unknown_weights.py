"""Exact rational checks of all-target weight/short-cycle flow transfer."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json

from verify_capacity_stdlib import generator, hit


def flows(n, cycles, coeffs):
    out = [[F(0) for _ in range(n)] for _ in range(n)]
    for cycle, a in zip(cycles, coeffs):
        for x, y in zip(cycle, cycle[1:] + cycle[:1]):
            out[x][y] += a
    return out


def mean(q, w, A):
    _, _, _, mu, p = hit(q, w, A)
    return mu / (1-p)


def fixture(n, seed):
    w = [F(2+(i+seed)%7, 3+(2*i+seed)%5) for i in range(n)]
    if seed % 2:
        w[0] /= 2**20
    wfac = [F(8+(3*i+seed)%6, 10) for i in range(n)]
    wh = [x*y for x,y in zip(w,wfac)]
    cycles = [[i,j] for i in range(n) for j in range(i)]
    cycles += [[i,j,k] for i,j,k in combinations(range(n), 3)]
    coeff = [F(1+(5*i+seed)%11, 3+(i+seed)%7) for i in range(len(cycles))]
    fac = [F(7+(3*i+seed)%8, 10) for i in range(len(cycles))]
    coeffh = [x*y for x,y in zip(coeff,fac)]
    q = generator(w, flows(n, cycles, coeff))
    qh_w = generator(w, flows(n, cycles, coeffh))
    qh = generator(wh, flows(n, cycles, coeffh))
    R = max(max(fac), 1/min(fac))
    # K=7/6 is a rational valid sector constant for cycles of length<=3.
    kappa2 = F(49,36) * (R-1)**2 / R
    a, b = min(wfac), max(wfac)
    weight_lo, weight_hi = a*a/b, b*b/a
    target_count = 0
    largest_flow_ratio = F(1)
    largest_combined_ratio = F(1)
    for mask in range(1, 2**n-1):
        A = [i for i in range(n) if mask >> i & 1]
        M, Mh_w, Mh = mean(q,w,A), mean(qh_w,w,A), mean(qh,wh,A)
        rf = Mh_w/M
        rw = Mh/Mh_w
        # Equivalent to reciprocal bounds by exp(2 asinh(K sinh(logR/2))).
        assert (rf-1)**2 <= kappa2*rf
        assert weight_lo <= rw <= weight_hi
        largest_flow_ratio = max(largest_flow_ratio, rf, 1/rf)
        largest_combined_ratio = max(largest_combined_ratio, Mh/M, M/Mh)
        target_count += 1
    return dict(states=n, seed=seed, targets=target_count,
                rare_stationary_state=bool(seed%2),
                coefficient_ratio_bound=str(R), kappa_squared=str(kappa2),
                weight_ratio_lower=str(weight_lo), weight_ratio_upper=str(weight_hi),
                largest_observed_flow_mean_ratio=float(largest_flow_ratio),
                largest_observed_combined_mean_ratio=float(largest_combined_ratio))


if __name__ == '__main__':
    cases = [fixture(n, seed) for n in (3,4,5,6) for seed in range(3)]
    out = dict(all_passed=True, exact_rational=True, cases=cases,
               all_target_checks=sum(x['targets'] for x in cases))
    path = Path(__file__).with_name('unknown_weight_checks.json')
    path.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(dict(all_passed=True, exact_rational=True,
                          all_target_checks=out['all_target_checks'],
                          output=str(path.resolve())), indent=2))
