#!/usr/bin/env python3
"""Finite numerical diagnostics for the proved phase-clock construction.

This is not an all-parameter proof, a novelty check, or a physical execution.
Uses mpmath 1.3.0 for 100-decimal arithmetic and fractions.Fraction for one
independent exact rational state-distribution propagation.
"""

from fractions import Fraction
from pathlib import Path
import json
import platform
import sys

import mpmath as mp


mp.mp.dps = 100
ALPHA = (mp.sqrt(5) - 1) / 2
THETA = 2 * mp.pi * ALPHA


def as_mp(x):
    if isinstance(x, Fraction):
        return mp.mpf(x.numerator) / x.denominator
    return mp.mpf(x)


def rounded_fraction(x, bits):
    den = 1 << bits
    return Fraction(int(mp.floor(x * den + mp.mpf('0.5'))), den)


def convergent_at_least(lower):
    p, q = 0, 1
    p1, q1 = 1, 1
    while q1 < lower:
        p, q, p1, q1 = p1, q1, p + p1, q + q1
    return p1, q1


def make_model(horizon, epsilon):
    # Reserve half the requested budget for rational parameter rounding.
    lower = max(mp.mpf(3), (4 * mp.pi**2 * horizon / epsilon)**(mp.mpf(1) / 3))
    p, n = convergent_at_least(lower)
    h = 2 * mp.pi / n
    signed_error = THETA - 2 * mp.pi * p / n
    direction = 1 if signed_error > 0 else -1
    d = abs(signed_error)
    t = mp.sin(d) / (mp.sin(d) + mp.sin(h - d))
    r = mp.cos(h / 2) / mp.cos(d - h / 2)
    u = mp.exp(2j * mp.pi * p / n)
    v = mp.exp(2j * mp.pi * (p + direction) / n)
    eigenvalue = (1 - t) * u + t * v
    bits = int(mp.ceil(mp.log(4 * (horizon + 1) / epsilon, 2)))
    t_rational = rounded_fraction(t, bits)
    readout = [rounded_fraction((1 + mp.cos(2 * mp.pi * j / n)) / 2, bits)
               for j in range(n)]
    readout_error = max(abs(as_mp(readout[j]) -
                            (1 + mp.cos(2 * mp.pi * j / n)) / 2)
                        for j in range(n))
    rational_lambda = (1 - as_mp(t_rational)) * u + as_mp(t_rational) * v
    ideal_uniform_bound = 2 * mp.pi**2 * horizon / n**3
    rounding_uniform_bound = horizon * abs(as_mp(t_rational) - t) + readout_error
    assert 0 < t < 1 and 0 < r < 1 and 0 < d < h / n
    assert abs(eigenvalue - r * mp.exp(1j * THETA)) < mp.mpf('1e-95')
    assert 1 - r <= 4 * mp.pi**2 / n**3
    assert ideal_uniform_bound + rounding_uniform_bound < epsilon
    assert all(0 <= x <= 1 for x in readout)
    assert 0 <= t_rational <= 1
    return locals()


def numerical_diagnostic(horizon, epsilon):
    m = make_model(horizon, epsilon)
    n = m['n']
    # Exhaustive in the lag index for T<=10000; otherwise a declared sample.
    if horizon <= 10000:
        indices = range(horizon + 1)
        lag_scope = 'every integer lag 0 through T'
    else:
        indices = sorted(set(range(1001)) |
                         {horizon * j // 1000 for j in range(1001)})
        lag_scope = '2000 or fewer declared sampled lags; uniform bound is analytic'
    ideal_max = mp.mpf(0)
    rounded_transition_max = mp.mpf(0)
    for k in indices:
        target = (1 + mp.cos(THETA * k)) / 2
        ideal = (1 + m['r']**k * mp.cos(THETA * k)) / 2
        rounded = (1 + mp.re(m['rational_lambda']**k)) / 2
        ideal_max = max(ideal_max, abs(ideal - target))
        rounded_transition_max = max(rounded_transition_max, abs(rounded - target))
    assert ideal_max <= m['ideal_uniform_bound']
    assert rounded_transition_max + m['readout_error'] < epsilon
    result = {
        'T': horizon, 'epsilon': str(epsilon), 'states': n, 'convergent_numerator': m['p'],
        'direction': m['direction'], 'precision_bits': m['bits'],
        'second_shift_probability': str(m['t_rational']),
        'radial_loss': mp.nstr(1 - m['r'], 30),
        'ray_eigenvalue_residual': mp.nstr(abs(m['eigenvalue'] -
            m['r'] * mp.exp(1j * THETA)), 10),
        'ideal_uniform_error_bound': mp.nstr(m['ideal_uniform_bound'], 30),
        'rational_rounding_uniform_bound': mp.nstr(m['rounding_uniform_bound'], 30),
        'total_uniform_error_bound': mp.nstr(m['ideal_uniform_bound'] +
            m['rounding_uniform_bound'], 30),
        'lag_check_scope': lag_scope,
        'largest_checked_ideal_error': mp.nstr(ideal_max, 30),
        'largest_checked_rounded_transition_error': mp.nstr(rounded_transition_max, 30),
        'readout_rounding_error': mp.nstr(m['readout_error'], 30),
    }
    if horizon == 30:
        # Independent exact rational propagation with rounded readout and
        # transition probabilities. This does not use the Fourier formula.
        dist = [Fraction(int(j == 0)) for j in range(n)]
        max_exact_error = mp.mpf(0)
        t = m['t_rational']
        for k in range(horizon + 1):
            assert sum(dist) == 1 and all(x >= 0 for x in dist)
            output = sum(x * y for x, y in zip(dist, m['readout']))
            target = (1 + mp.cos(THETA * k)) / 2
            max_exact_error = max(max_exact_error, abs(as_mp(output) - target))
            if k < horizon:
                nxt = [Fraction(0) for _ in range(n)]
                for j, weight in enumerate(dist):
                    nxt[(j + m['p']) % n] += weight * (1 - t)
                    nxt[(j + m['p'] + m['direction']) % n] += weight * t
                dist = nxt
        assert max_exact_error < epsilon
        result['exact_rational_propagation_max_error'] = mp.nstr(max_exact_error, 30)
        result['exact_rational_probability_mass_checks'] = horizon + 1
    return result


def main():
    epsilon = mp.mpf(1) / 16
    results = [numerical_diagnostic(t, epsilon)
               for t in (30, 100, 1000, 10000, 1000000)]
    receipt = {
        'status': 'PASS_FINITE_DIAGNOSTICS_ONLY',
        'theorem_status': 'written all-parameter proof is separate',
        'historical_novelty': 'UNKNOWN',
        'physical_execution': False,
        'python': sys.version.split()[0], 'executable': sys.executable,
        'platform': platform.platform(), 'mpmath': mp.__version__,
        'decimal_precision': mp.mp.dps,
        'alpha': '(sqrt(5)-1)/2',
        'cases': results,
    }
    path = Path(__file__).with_name('VERIFICATION.json')
    path.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': receipt['status'], 'cases': len(results),
                      'receipt': str(path.resolve()),
                      'states': [r['states'] for r in results]}, indent=2))


if __name__ == '__main__':
    main()
