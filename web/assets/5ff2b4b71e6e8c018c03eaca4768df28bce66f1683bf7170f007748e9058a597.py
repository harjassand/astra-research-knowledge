#!/usr/bin/env python3
"""Independent exact audit of S03's saved 512-panel weight constant.

Uses its OWN elementary interval kernel (160 bits) and NO peer imports.
Every Darboux enclosure and tail, not just a reported final number, is read.
Analytic envelope derivation is supplied in WEIGHT_ENVELOPE_AUDIT.txt.
"""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
P = 160
GRID = 1 << P


def outward(lo, hi):
    assert lo <= hi
    a, b = lo * GRID, hi * GRID
    return (F(a.numerator // a.denominator, GRID),
            F(-((-b.numerator) // b.denominator), GRID))


def exp_interval(x):
    x = F(x)
    if x <= -P:
        return F(0), F(1, GRID)  # e>2, and no declaration of exact zero.
    if x < 0:
        a, b = exp_interval(-x)
        assert a > 0
        return outward(1 / b, 1 / a)
    reduced, halvings = x, 0
    while reduced > F(1, 2):
        reduced /= 2
        halvings += 1
    order = 48
    lo = sum(reduced ** k / factorial(k) for k in range(order + 1))
    hi = lo + reduced ** (order + 1) / (factorial(order + 1) * (1 - reduced))
    lo, hi = outward(lo, hi)
    for _ in range(halvings):
        lo, hi = outward(lo * lo, hi * hi)
    return lo, hi


def gaussian_tail_upper(q, L):
    return exp_interval(-q * L * L)[1] * (L / (2 * q) + 1 / (4 * q * q * L))


def check_panels(rows, c, d, e, lower):
    cumulative = F(0)
    independent = F(0)
    preceding = F(0)
    for row in rows:
        a, b = F(row['a']), F(row['b'])
        assert a == preceding and b > a
        preceding = b
        # Natural interval polynomial range, without dyadic intermediate
        # rounding. The peer's 96-bit boxes must contain these 160-bit bounds.
        if d >= 0:
            exponent_lo = -c * b ** 4 + d * a ** 2 + e * a
            exponent_hi = -c * a ** 4 + d * b ** 2 + e * b
        else:
            exponent_lo = -c * b ** 4 + d * b ** 2 + e * a
            exponent_hi = -c * a ** 4 + d * a ** 2 + e * b
        independent_lo = a * a * exp_interval(exponent_lo)[0]
        independent_hi = b * b * exp_interval(exponent_hi)[1]
        lo, hi = F(row['integrand_interval']['lo']), F(row['integrand_interval']['hi'])
        assert lo <= independent_lo <= independent_hi <= hi
        charged = (b - a) * (lo if lower else hi)
        assert charged == F(row['charged_contribution'])
        cumulative += charged
        independent += (b - a) * (independent_lo if lower else independent_hi)
    return cumulative, independent, preceding


def main():
    started = time.monotonic()
    payload_path = HERE / 'peer_weight_constant_snapshot.json'
    data = json.loads(payload_path.read_text())
    p = data['parameters']
    k, q = data['constants'], data['quadrature']
    M, B, Lambda, Lc, Tc = (F(p[key]) for key in ('M', 'B', 'Lambda', 'Lc', 'trace_C_upper'))
    assert (M, B, Lambda, Lc, Tc) == (F(1, 10), F(1, 5), F(11, 10), F(6, 5), F(18, 5))
    nmin, sqrt_n, fourth_n = 65536, F(256), F(16)
    assert p['N_min'] == nmin and p['p'] == 2
    theta, young = F(p['theta']), F(p['Young_parameter'])
    amp = F(k['drift_amplification_upper'])
    assert amp >= exp_interval(Lc / (2 * sqrt_n))[1]
    beta = B / (2 * sqrt_n)
    d = 2 * Lc * amp ** 2 * (1 + theta) / 16
    e = 2 * B * amp / 4
    kz = 2 * Lc * amp ** 2 * (1 + 1 / theta) / 2
    ellz = 2 * B * amp / 2
    K = kz + young / 2
    aa = F(nmin) / (3 * Tc)
    assert aa > K
    mart = 1 + 6 * K / (aa - K)
    exponent = 2 * Tc / (4 * sqrt_n) + kz * beta ** 2 + ellz * beta + ellz ** 2 / (2 * young)
    assert d == F(k['seed_quadratic_tilt']) and e == F(k['seed_linear_tilt'])
    assert K == F(k['martingale_K']) and aa == F(k['martingale_tail_a_lower'])
    assert mart == F(k['conditional_martingale_factor_upper'])
    assert exponent == F(k['prefactor_exponent_upper'])
    prefactor = F(k['prefactor_upper'])
    assert prefactor >= exp_interval(exponent)[1] * mart
    exp044 = exp_interval(F(11, 25))
    exp1, expminus1 = exp_interval(1), exp_interval(-1)
    cosh1_hi = (exp1[1] + expminus1[1]) / 2
    assert exp044[0] > cosh1_hi  # hence delta>3/50.
    delta_lo = F(q['delta_lower'])
    assert delta_lo == F(3, 50)
    upper_d = d - Lambda / 16 + 1 / (24 * sqrt_n)
    c, L = F(11, 2880), F(16)
    assert upper_d == F(q['upper_quadratic_coefficient'])
    assert upper_d / L ** 2 + e / L ** 3 <= c / 2
    exterior_coef = delta_lo * sqrt_n / 4 - d - 1 / (4 * sqrt_n) - e / (2 * fourth_n)
    assert exterior_coef == F(q['exterior_coefficient_lower']) >= 1
    dmin = 1 - Lambda / (2 * sqrt_n)
    lower, own_lower, low_cap = check_panels(q['lower_panels'], F(1, 192), -Lambda / (16 * dmin), F(0), True)
    upper, own_upper, up_cap = check_panels(q['upper_panels'], c, upper_d, e, False)
    assert low_cap == up_cap == L
    assert len(q['lower_panels']) == len(q['upper_panels']) == 512
    assert lower == F(k['seed_normalizer_lower']) > 0
    tailq = c * L ** 2 / 2
    assert tailq == F(q['upper_tail_q'])
    tail_upper = F(q['upper_envelope_tail'])
    exterior_tail = F(q['exterior_seed_tail'])
    assert tail_upper >= gaussian_tail_upper(tailq, L)
    assert exterior_tail >= gaussian_tail_upper(F(1), 2 * fourth_n)
    upper_integral = upper + tail_upper + exterior_tail
    assert upper_integral == F(k['seed_tilt_integral_upper'])
    seed_moment = upper_integral / lower
    assert seed_moment == F(k['seed_tilt_moment_upper'])
    K2 = prefactor * seed_moment
    assert K2 == F(k['weight_p_moment_upper']) < F(17173, 1000)
    inverse_mean_sq = F(k['inverse_mean_squared_upper'])
    assert inverse_mean_sq >= exp_interval(B * B)[1]
    proposal = inverse_mean_sq * K2
    assert proposal == F(k['importance_proposal_coefficient_upper']) < F(17874, 1000)
    result = {'status': 'PASS_INDEPENDENT_ENVELOPES_AND_CONSTANT_FORMULAS',
              'origin_worker': 'c07_s03', 'auditor': 'c08_s03',
              'peer_snapshot_sha256': hashlib.sha256(payload_path.read_bytes()).hexdigest(),
              'own_interval_bits': P, 'all_1024_panels_enclosed': True,
              'parameter_scope': 'M=1/10,B=1/5,all N>=65536,exact heat seed contracted radially',
              'K2_upper_exact': str(K2), 'proposal_coefficient_upper_exact': str(proposal),
              'K2_display': float(K2), 'proposal_coefficient_display': float(proposal),
              'own_lower_sum_display': float(own_lower), 'own_upper_sum_display': float(own_upper),
              'elapsed_seconds': time.monotonic() - started,
              'quantum_heat_identity': 'IMPORTED_S02_BASELINE_NOT_PROVED_BY_QUADRATURE',
              'integrated_sampler': 'NOT_EXECUTED_HERE'}
    (HERE / 'weight_envelope_verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items()
                      if not key.endswith('_exact')}))


if __name__ == '__main__':
    main()
