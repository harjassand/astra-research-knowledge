"""Reviewer reconstruction from the equations; no trial routines are imported.

Synthetic checks only. The producer replays are separate, unmodified copies.
"""
from fractions import Fraction as F
from pathlib import Path
import itertools
import json
import math
import random

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import expit, ndtr, ndtri

HERE = Path(__file__).resolve().parent


def invert(a):
    n = len(a)
    b = [[F(v) for v in row] + [F(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if b[i][j])
        b[j], b[pivot] = b[pivot], b[j]
        scale = b[j][j]
        b[j] = [v / scale for v in b[j]]
        for i in range(n):
            if i != j:
                scale = b[i][j]
                b[i] = [x - scale * y for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def fsqrt(v):
    p, q = math.isqrt(v.numerator), math.isqrt(v.denominator)
    assert p * p == v.numerator and q * q == v.denominator
    return F(p, q)


def scalar_response(a, d):
    return invert([[a[i][j] + (d[i] if i == j else 0)
                    for j in range(len(a))] for i in range(len(a))])[0][0]


def recover_from_measurements(a, t):
    n = len(a)
    zero = [F(0)] * n
    baseline = scalar_response(a, zero)
    r = [[F(0)] * n for _ in range(n)]
    r[0][0] = baseline
    for i in range(1, n):
        d = zero.copy()
        d[i] = t
        l1 = baseline - scalar_response(a, d)
        d[i] = 2 * t
        l2 = baseline - scalar_response(a, d)
        # Solve the two rank-one relations without importing producer code.
        pii = (2 * l1 - l2) / (2 * t * (l2 - l1))
        ai = fsqrt(l1 * (1 + t * pii) / t)
        r[i][i], r[0][i], r[i][0] = pii, ai, ai
    for i, j in itertools.combinations(range(1, n), 2):
        d = zero.copy()
        d[i] = d[j] = t
        loss = baseline - scalar_response(a, d)
        ai, aj, pii, pjj = r[0][i], r[0][j], r[i][i], r[j][j]
        u, v = 1 + t * pii, 1 + t * pjj
        constant = (ai * ai * v + aj * aj * u) / t - loss * u * v / (t * t)
        disc = ai * ai * aj * aj - loss * constant
        roots = [(ai * aj + sign * fsqrt(disc)) / loss for sign in (-1, 1)]
        upper = min(ai * pjj / aj, aj * pii / ai)
        admissible = [x for x in roots if 0 < x <= upper]
        assert len(admissible) == 1
        r[i][j] = r[j][i] = admissible[0]
    assert invert(r) == a


def q54():
    # Integrating the derivative is independent of the supplied softplus routine.
    c, delta = .65, .01
    h = lambda x, c=c, delta=delta: 4 * quad(lambda s: expit((s-c)/delta), 0, x,
                           epsabs=1e-28, epsrel=1e-12, points=[c] if x > c else None)[0]
    safe, target = h(.5), h(1.)
    n5 = 4 * 1e-6 * ndtri(.95)**2 / safe**2
    reported = json.loads((HERE/'replay/Q54/numerical_summary.json').read_text())['selected_rate']
    assert math.isclose(safe, reported['safe_signal'], rel_tol=2e-13)
    assert math.isclose(target, reported['target_gap'], rel_tol=2e-13)
    jumps = []
    for delta in [.02, .005, .001, .0002, .00005]:
        center = .5 + math.sqrt(.5*delta)
        safe = 4*delta*(math.log1p(math.exp((.5-center)/delta))
                        - math.log1p(math.exp(-center/delta)))
        # Target uses a stable asymptotic identity for softplus.
        target = 4*((1-center)+delta*math.log1p(math.exp(-(1-center)/delta))
                    - delta*math.log1p(math.exp(-center/delta)))
        assert 0 < safe and target < 2
        jumps.append({'delta':delta,'safe_signature':safe,'target_gap':target})
    return {'safe_signal_quadrature':h(.5), 'target_gap_quadrature':h(1.),
            'optimal_error_n_1e6':float(ndtr(-1000*h(.5)/.002)),
            'real_threshold_5pct':float(n5),'sharp_modulus_sequence':jumps}


def q63():
    rng = random.Random(6310262)
    cases, non_dd = 0, 0
    # Congruences include SPD M-matrices outside row-diagonally-dominant networks.
    for n in range(1, 8):
        for mode in range(3):
            a = [[F(0)]*n for _ in range(n)]
            for i in range(n):
                a[i][i] = F(rng.randint(1, 4))
            for i in range(n):
                for j in range(i+1, n):
                    w = F(rng.randint(1, 4)) if mode == 0 or j == i+1 else F(0)
                    a[i][i] += w
                    a[j][j] += w
                    a[i][j] = a[j][i] = -w
            scale = [F(1)] + [F(rng.randint(1, 5), rng.randint(1, 5)) for _ in range(n-1)]
            a = [[a[i][j]*scale[i]*scale[j] for j in range(n)] for i in range(n)]
            non_dd += int(any(sum(row) < 0 for row in a))
            for t in (F(1, 7), F(3, 2), F(5)):
                recover_from_measurements(a, t)
                cases += 1
    # Constructed depth-L paths: compare loss removal without float subtraction.
    paths = []
    for depth in (8, 12, 20, 30):
        n = depth + 1
        base = [[F(0)]*n for _ in range(n)]
        for i in range(n-1):
            base[i][i] += 1
            base[i+1][i+1] += 1
            base[i][i+1] = base[i+1][i] = F(-1)
        leaky = [[base[i][j] + (F(1) if i == j else F(0)) for j in range(n)] for i in range(n)]
        r = invert(leaky)
        signal = r[0][-1]**2/(1+r[-1][-1])
        base[0][0] += 1
        isolated = invert(base)
        bypass = isolated[0][-1]**2/(1+isolated[-1][-1])
        assert bypass == F(1, depth+2)
        paths.append({'depth':depth,'max_leaky_signal_exact':str(signal),
                      'bypass_signal_exact':str(bypass)})
    return {'exact_reconstruction_cases':cases,'networks_with_negative_row_sum':non_dd,
            'shunt_amplitudes':['1/7','3/2','5'],'path_checks':paths}


def q95():
    # Continuous stress contrast is integrated directly, independent of bin code.
    sigma = .02
    def energy(rate, duration):
        return quad(lambda s: (-math.expm1(-rate*s))**2, 0., duration,
                    epsabs=1e-25, epsrel=1e-11)[0]
    lam = .001
    t5 = brentq(lambda t: energy(lam,t)-4*sigma*sigma*ndtri(.95)**2, 1, 100)
    exact = float(ndtr(-math.sqrt(energy(lam,1))/(2*sigma)))
    reported = json.loads((HERE/'replay/Q95/results.json').read_text())['checks']['hidden_mode']
    assert abs(t5-reported['minimum_duration_for_five_percent_white_noise_error']) < 1e-9
    assert abs(exact-reported['continuous_white_noise_best_error']) < 1e-13
    # Check positive composite test at mixtures close to the least-favorable atom.
    ell, duration, mass, amp = .1, 1., 1., 1.
    b = lambda t: mass*amp*(-math.expm1(-ell*t))
    d2 = energy(ell,duration)/(sigma*sigma)
    worst = float(ndtr(-math.sqrt(d2)/2))
    checks=[]
    for eps in (0., 1e-6, 1e-4, .01, .5):
        for weight in (.1, .5, .9):
            contrast = lambda t: weight*(-math.expm1(-ell*t))+(1-weight)*(-math.expm1(-ell*(1+eps)*t))
            projection = quad(lambda t:b(t)*contrast(t),0,duration,
                              epsabs=1e-14)[0]/sigma**2
            error = float(ndtr((d2/2-projection)/math.sqrt(d2)))
            assert error <= worst+1e-14
            checks.append({'relative_rate_offset':eps,'weight_at_floor':weight,'type_II_error':error})
    # The no-floor minimax lower bound approaches the midpoint risk 1/4.
    mse_bounds=[]
    for rate in (.1,.01,.001,.0001,1e-6):
        d = math.sqrt(energy(rate,1))/sigma
        tv = 2*ndtr(d/2)-1
        mse_bounds.append({'rate':rate,'two_point_MSE_lower_bound':float(.25-.5*tv)})
    return {'continuous_best_error_rate_001':exact,'duration_5pct_rate_001':t5,
            'rate_floor_minimax_error':worst,'near_boundary_spectrum_checks':checks,
            'no_floor_minimax_lower_bound_sequence':mse_bounds}


if __name__ == '__main__':
    result = {'Q54':q54(),'Q63':q63(),'Q95':q95()}
    (HERE/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
