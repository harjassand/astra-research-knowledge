"""Independent finite diagnostics, without importing any producer module.

Exact fractions verify finite generators. Floating integration/ODE/calibration
checks are scoped diagnostics, not interval or general proof certificates.
"""
from __future__ import annotations

from fractions import Fraction as F
from math import ceil, exp, factorial, log, pi, sqrt
from pathlib import Path
import json

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.linalg import expm
from scipy.special import eval_genlaguerre, poch


def partition_generator(n):
    states = [(n,)]
    lookup = {states[0]: 0}
    rows = []
    for state in states:
        row = {}
        for i, size in enumerate(state):
            for left in range(1, size):
                dest = tuple(sorted(state[:i] + state[i+1:] + (left, size-left)))
                if dest not in lookup:
                    lookup[dest] = len(states)
                    states.append(dest)
                j = lookup[dest]
                row[j] = row.get(j, F(0)) + F(1, size+1)
        row[lookup[state]] = -sum(row.values(), F(0))
        rows.append(row)
    matrix = [[F(0) for _ in states] for _ in states]
    for i, row in enumerate(rows):
        for j, rate in row.items():
            matrix[i][j] = rate
        assert sum(matrix[i], F(0)) == 0
        assert all(rate >= 0 for j, rate in enumerate(matrix[i]) if j != i)
        # Every transition increases the number of blocks and conserves marks.
        for j, rate in row.items():
            if j != i and rate:
                assert len(states[j]) == len(states[i])+1
                assert sum(states[j]) == n
    return states, np.array(matrix, dtype=float)


def coefficients(count):
    c = np.ones(count+1)
    for j in range(1, count+1):
        c[j] = c[j-1]*(j+.5)/j
    return c


def centered_moments(values, weights, times, degree=80):
    mu = float(np.dot(values, weights))
    initial = np.array([np.dot(weights, (values-mu)**j) for j in range(degree+1)])
    initial[0], initial[1] = 1., 0.
    def rhs(_t, moments):
        out = np.zeros_like(moments)
        for k in range(2, degree+1):
            out[k] = -(k-1)/(k+1)*moments[k]
            out[k] += sum(moments[j]*moments[k-j] for j in range(1, k))/(k+1)
        return out
    sol = solve_ivp(rhs, (0., max(times)), initial, t_eval=times,
                    method='DOP853', atol=1e-15, rtol=1e-12)
    assert sol.success
    return mu, sol.y.T


def main():
    result = {'status': 'Independent exact finite algebra plus floating diagnostics; no general proof or exact-real certification.',
              'producer_imports': [], 'seed': 2026101307}
    rows = []
    for n in range(2, 9):
        states, generator = partition_generator(n)
        squares = np.array([sum(q*q for q in state) for state in states])
        for t in [0., 1., 3., 30.]:
            law = expm(t*generator)[0]
            exact = n+n*(n-1)*exp(-t/3)
            error = abs(float(law@squares)-exact)
            assert error < 2e-11
            rows.append({'n': n, 'time': t, 'states': len(states), 'pair_identity_error': error})
    result['exact_partition_structure'] = {'generators': 7, 'floating_pair_checks': rows}

    rows = []
    for a, b, mu in [(1., 1.1, 1.05), (1., 1.4, 1.13), (1., 3., 2.)]:
        for s in [a, mu, b]:
            for u in [a, b]:
                rate = .5*(1/s+1/u-1/mu)
                constant = (2*pi)**(-1.5)*mu**1.5/(s*u)**1.5
                numerical, error_estimate = quad(lambda r: 4*pi*r*r*constant*exp(-rate*r*r), 0., np.inf,
                                                 epsabs=1e-12, epsrel=1e-12)
                identity = (1-(s-mu)*(u-mu)/mu**2)**(-1.5)
                assert abs(numerical-identity) < 1e-10
                rows.append({'a': a, 'b': b, 'mu': mu, 's': s, 'u': u,
                             'absolute_error': abs(numerical-identity),
                             'quadrature_error_estimate': error_estimate})
    result['overlap_integrals'] = rows

    c = coefficients(80)
    times = [0., 1., 3., 10.]
    rows = []
    examples = [(np.array([1., 1.1]), np.array([.5, .5])),
                (np.array([1., 1.4]), np.array([.7, .3])),
                (np.array([1., 2., 3.]), np.array([.25, .5, .25]))]
    constants = []
    for values, weights in examples:
        a, b = float(values.min()), float(values.max())
        mu, moment_rows = centered_moments(values, weights, times)
        sigma2 = float(weights@((values-mu)**2))
        distance = max(mu-a, b-mu)
        q = (distance/mu)**2
        # Evaluate the positive series instead of a cancellation-prone formula.
        aq = sum(c[j]*q**(j-2) for j in range(2, len(c)))
        bound_constant = aq*(sigma2/mu**2)**2
        constants.append({'values': values.tolist(), 'weights': weights.tolist(), 'mu': mu,
                          'sigma2': sigma2, 'q': q, 'A_series_to_80': aq,
                          'B_series_to_80': bound_constant,
                          'lower_N_prefactor': log(2)/bound_constant})
        for t, moments in zip(times, moment_rows):
            assert abs(moments[2]-sigma2*exp(-t/3)) < 1e-12
            normalized = moments/mu**np.arange(len(moments))
            chi_series = float(c[2:]@(normalized[2:]**2))
            bound = bound_constant*exp(-2*t/3)
            assert chi_series <= bound*(1+1e-8)+1e-15
            # Independent radial density integration of the derivative expansion.
            def integrand(radius):
                x = radius*radius/(2*mu)
                ratio_minus_one = sum((-1)**j*normalized[j]*eval_genlaguerre(j,.5,x)
                                      for j in range(1, len(normalized)))
                return 4*pi*radius*radius*(2*pi*mu)**(-1.5)*exp(-x)*ratio_minus_one**2
            numerical, qe = quad(integrand, 0., 18*sqrt(b), epsabs=2e-13, epsrel=1e-9, limit=300)
            assert abs(numerical-chi_series) < 1e-9
            rows.append({'values': values.tolist(), 'time': t, 'chi2_series_to_80': chi_series,
                         'chi2_radial_quadrature': numerical, 'quadrature_error_estimate': qe,
                         'theorem_bound': bound, 'quadrature_series_error': abs(numerical-chi_series)})
    result['transient_chi2_checks'] = rows
    result['testing_constants'] = constants
    narrow = constants[0]
    result['producer_narrow_information_example'] = {
        'B': narrow['B_series_to_80'],
        'lower_N_times': [{'time': t, 'lower_N': narrow['lower_N_prefactor']*exp(2*t/3)}
                          for t in [0., 3., 10., 100.]],
        'status': 'Floating evaluation of rigorous analytic bound, not outward-rounded certification.'}

    # Gaussian radial polynomial expectations, exactly in rational arithmetic.
    def gaussian_h2(s, mu):
        return 945*s**4-2100*mu*s**3+1950*mu**2*s**2-900*mu**3*s+225*mu**4
    for mu in [F(1), F(21,20), F(2)]:
        assert gaussian_h2(mu,mu) == 120*mu**4
    result['exact_quartic_variance_identities'] = 3

    # Small measured-velocity acquisition fixtures. This does not validate a
    # physical sensor/model, nor convert continuous target TV to finite-float TV.
    rng = np.random.default_rng(result['seed'])
    a, b, epsilon, zeta = 1., 3., .2, .05
    m0 = ceil(10*b*b/(a*a*epsilon*epsilon))
    blocks = ceil(8*log(1/zeta))
    if blocks%2 == 0:
        blocks += 1
    delta = a*epsilon*sqrt(2/3)
    rows = []
    for k in range(12):
        variance = rng.choice(np.array([a,b]), size=(blocks,m0))
        radius2 = variance*rng.chisquare(3, size=(blocks,m0))
        estimate = float(np.clip(np.median(np.mean(radius2/3, axis=1)), a,b))
        rows.append({'fixture': k, 'mu_hat': estimate, 'absolute_error': abs(estimate-2.),
                     'within_calibration_event': abs(estimate-2.)<=delta})
    threshold = max(0., 3*log(sqrt(15/2)*(b-a)**2/(8*a*a*epsilon)))
    result['mean_only_acquisition'] = {'a': a, 'b': b, 'epsilon': epsilon, 'zeta': zeta,
         'per_block': m0, 'blocks': blocks, 'observations_per_calibration': m0*blocks,
         'delta_mu': delta, 'late_time_threshold': threshold,
         'analytic_failure_bound': exp(-blocks/8), 'diagnostics': rows}
    Path('independent_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'partition_generators': 7, 'partition_pair_checks': 28,
                      'overlap_integrals': len(result['overlap_integrals']), 'chi2_checks': len(result['transient_chi2_checks']),
                      'quartic_exact': 3, 'calibration_fixtures': len(rows),
                      'narrow_B': narrow['B_series_to_80'], 'narrow_N0': narrow['lower_N_prefactor']}, indent=2))


if __name__ == '__main__':
    main()
