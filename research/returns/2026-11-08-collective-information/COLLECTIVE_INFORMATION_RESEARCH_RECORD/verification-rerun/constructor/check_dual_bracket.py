#!/usr/bin/env python3
"""Exact small-cell audit of primal/dual normalizations and known gradient D.

Enumeration is a diagnostic only. The proposed algorithm samples local paths.
"""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
from check_cell_current import solve


def rate(eta, x, a, mode):
    return 1 + a * (eta[x-1] + eta[x+2] if mode == 'gradient' else eta[x-1] * eta[x+2])


def primal(length, a, rho, mode):
    interior = tuple(range(1, length-1))
    ghosts = tuple(x for x in range(-1, length+2) if x not in interior)
    states = list(product((0, 1), repeat=len(interior)))
    lookup = {s: i for i, s in enumerate(states)}
    n = len(states)
    gen = [[F(0) for _ in states] for _ in states]
    drift = [F(0) for _ in states]
    activity = F(0)
    for i, s in enumerate(states):
        sw = rho ** sum(s) * (1-rho) ** (len(s)-sum(s))
        for gs in product((0, 1), repeat=len(ghosts)):
            gw = rho ** sum(gs) * (1-rho) ** (len(gs)-sum(gs))
            eta = dict(zip(interior, s)) | dict(zip(ghosts, gs))
            for x in range(length):
                r = gw * rate(eta, x, a, mode)
                mark = eta[x]-eta[x+1]
                after = eta.copy()
                after[x], after[x+1] = eta[x+1], eta[x]
                k = lookup[tuple(after[y] for y in interior)]
                if k != i:
                    gen[i][k] += r
                    gen[i][i] -= r
                drift[i] += r * mark
                activity += sw * r * mark * mark
    g = [[-x for x in row] for row in gen]
    f = solve([row[:-1] for row in g[:-1]], drift[:-1]) + [F(0)]
    var = activity - 2 * sum(rho ** sum(s) * (1-rho) ** (len(s)-sum(s)) * drift[i] * f[i] for i, s in enumerate(states))
    return var / (2 * rho * (1-rho) * length)


def dual(length, a, rho, mode):
    sites = tuple(range(length+1))
    ghosts = (-1, length+1)
    numerator = F(0)
    for gs in product((0, 1), repeat=2):
        gw = rho ** sum(gs) * (1-rho) ** (2-sum(gs))
        for count in range(1, len(sites)):
            states = [s for s in product((0, 1), repeat=len(sites)) if sum(s) == count]
            lookup = {s:i for i, s in enumerate(states)}
            g = [[F(0) for _ in states] for _ in states]
            rhs = [F(s[-1]-s[0]) for s in states]  # G_1 ell = eta_L - eta_0.
            assert sum(rhs) == 0
            for i, s in enumerate(states):
                eta = dict(zip(sites, s)) | dict(zip(ghosts, gs))
                for x in range(length):
                    after = list(s)
                    after[x], after[x+1] = after[x+1], after[x]
                    k = lookup[tuple(after)]
                    if k != i:
                        r = rate(eta, x, a, mode)
                        g[i][k] -= r
                        g[i][i] += r
            f = solve([row[:-1] for row in g[:-1]], rhs[:-1]) + [F(0)]
            assert all(sum(g[i][k]*f[k] for k in range(len(states))) == rhs[i] for i in range(len(states)))
            sw = rho ** count * (1-rho) ** (len(sites)-count)
            inner = sum(x*y for x,y in zip(rhs, f))
            assert inner >= 0
            numerator += gw * sw * inner
    return numerator / (rho * (1-rho) * length)


if __name__ == '__main__':
    rows = []
    for mode in ('gradient', 'nongradient'):
        for a in (F(0), F(1)):
            for rho in (F(1,3), F(1,2), F(2,3)):
                for length in (3, 5):
                    upper = primal(length, a, rho, mode)
                    h = dual(length, a, rho, mode)
                    lower = 1/h
                    lam = 1 + (2*a if mode == 'gradient' else a)
                    assert 1 <= lower <= upper <= lam
                    row = {'mode':mode, 'a':str(a), 'rho':str(rho), 'length':length,
                           'primal_upper_U':str(upper), 'dual_inverse_H':str(h),
                           'dual_lower_1_over_H':str(lower)}
                    if mode == 'gradient':
                        exact = 1 + 2*a*rho
                        assert lower <= exact <= upper
                        row['known_infinite_volume_D'] = str(exact)
                    if a == 0:
                        assert lower == upper == 1
                    rows.append(row)
    # The smaller open cells happen to have zero current drift after refreshing
    # ghosts, even for the nongradient dictionary. This larger cell checks a
    # genuinely nonzero Poisson correction rather than just its zero limit.
    stress_primal = primal(7, F(1), F(1,2), 'nongradient')
    assert stress_primal < F(5,4)
    stress = {'mode':'nongradient', 'a':'1', 'rho':'1/2', 'length':7,
              'primal_upper_U':str(stress_primal), 'uncorrected_activity_D':'5/4',
              'strictly_positive_Green_Kubo_correction':True}
    target = Path(__file__).with_name('dual_bracket_check.json')
    target.write_text(json.dumps({'scope':'Exact finite diagnostic; not a proof of infinite-volume bracketing',
                                 'all_checks_passed':True, 'cases':rows,
                                 'nonzero_corrector_stress_case':stress}, indent=2)+'\n')
    print(json.dumps({'cases':len(rows), 'nonzero_corrector_stress_passed':True,
                      'all_checks_passed':True, 'output':str(target.resolve())}))
