#!/usr/bin/env python3
"""C07_S01 exact rational checks for the independently reconstructed 5/4 tail.

No author arithmetic or constant-check code is imported. These exact checks
verify arithmetic endpoints of a separately written symbolic analytic proof;
they do not themselves replace that proof's infinite quantifiers.
"""
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json


def exp_sum(x, degree):
    term = total = Q(1)
    for j in range(1, degree + 1):
        term *= x / j
        total += term
    return total


def rational_constant_checks():
    a, delta, lam = Q(12, 5), Q(5, 4), Q(33, 32)
    z = a / 2
    cos_upper = 1 - z**2 / 2 + z**4 / 24
    cos_lower = cos_upper - z**6 / 720
    c = delta * lam
    core_g = Q(59, 224)
    phase = 60 * Q(16, 735)**2 * delta**3 * Q(1089, 65536) / (core_g**3 * Q(51, 100))
    margin = 1 - Q(1, 10) - Q(1, 1000) - Q(1, 4) - Q(1, 8)
    checks = {
        'a_less_than_pi_lower_three': a < 3,
        'saddle_contraction': c / 2 == Q(165, 256) < 1,
        'saddle_shift_bound': c == Q(165, 128),
        'cos_upper_exact': cos_upper == Q(229, 625),
        'cos_lower_positive': cos_lower > 0,
        'correlated_edge_condition': c < 2 * (1 - cos_upper**2) < 2,
        'logsec_endpoint_from_positive_exp': cos_lower * exp_sum(Q(21, 20), 5) > 1,
        'core_cos_lower': 1 - Q(1, 2)**2 / 2 == Q(7, 8),
        'core_logsec_coefficient': Q(1, 2) / Q(7, 8) == Q(4, 7),
        'phase_cubic_coefficient': Q(2, 5) * Q(8, 7)**2 / 24 == Q(16, 735),
        'max_t_one_minus_t_squared': Q(4, 27) < Q(2, 5)**2,
        'core_g_margin': 1 - 4 * delta * lam / 7 == core_g,
        'core_g_sqrt': Q(51, 100)**2 < core_g,
        'L2_N3_endpoint': Q(66**2, 64**3) == Q(1089, 65536),
        'phase_loss_exact': phase == Q(2420000, 24440101) < Q(1, 10),
        'core_tail_prefactor_below_one': Q(5, 3 * 64) < 1,
        'core_tail_exponent': Q(64, 5) > 8,
        'exp_two_greater_seven': exp_sum(Q(2), 5) > 7,
        'core_tail_strict_thousand': 7**4 > 1000,
        'outer_psi_at_one': Q(1, 5) - lam / 7 == Q(59, 1120),
        'outer_psi_at_a': a**2 / (4 * delta) - lam * Q(21, 20) == Q(1107, 16000),
        'outer_endpoint_order': Q(1107, 16000) > Q(59, 1120),
        'outer_prefactor_monotone_in_delta': 64 > 2 * delta,
        'outer_prefactor_at64_below_six': 112**2 < 6**2 * 25 * 15,
        'outer_exp_at64_exponent': Q(59 * 64, 1120) == Q(118, 35),
        'outer_exp_at64_greater24': exp_sum(Q(118, 35), 6) > 24,
        'outer_bound_decreases': Q(1, 2 * 64) < Q(59, 1120),
        'vertical_exponent': a**2 / (4 * delta) - lam * Q(21, 20) == Q(1107, 16000),
        'vertical_sqrt_prefactor': Q(5, 12) < Q(2, 3)**2,
        'vertical_prefactor64': lam * Q(2, 3) * 8 == Q(11, 2),
        'vertical_exponent64': Q(1107 * 64, 16000) == Q(1107, 250) > 4,
        'exp_four_greater48': exp_sum(Q(4), 6) > 48,
        'vertical_error_eighth': Q(11, 96) < Q(1, 8),
        'vertical_bound_decreases': Q(1, 2 * 64) < Q(1107, 16000),
        'surviving_margin': margin == Q(131, 250) > Q(1, 2),
        'tail_mills_prefactor': Q(5, 3) < Q(4, 3)**2,
        'tail_mills_factor': 2 / a * Q(2, 3) == Q(5, 9),
        'tail_mills_exponent': a**2 / (4 * delta) == Q(144, 125),
        'log_two_lt_seven_tenths': exp_sum(Q(7, 10), 3) > 2,
        'correction_slope_negative': Q(7, 10) - Q(144, 125) + Q(5, 16) < 0,
        'correction_exponent_at64': Q(7, 10) * 67 - Q(144 * 64, 125) + Q(5 * 66**2, 16 * 64) == -Q(177871, 32000),
        'correction_prefactor_at64': Q(5, 9 * 8) == Q(5, 72) < Q(1, 2),
        # Physical negative control: N=2 H0 determinant is e^{-delta}-1/4.
        'delta_three_halves_fails_N2': exp_sum(Q(3, 2), 3) > 4,
        # Positive endpoint at N=2 via independent upper exp(5/4) bound.
        'delta_five_fourths_not_N2_obstruction':
            exp_sum(Q(5, 4), 8) + (Q(5, 4)**9 / factorial(9)) / (1 - Q(5, 40)) < 4,
    }
    # Independently check the degree-elevation column sum exactly in a finite
    # collection. The all-N identity is proved by integrating Bernstein bases.
    columns = 0
    for N in (2, 3, 7, 16, 64):
        for ell in range(N + 1):
            for j in range(ell + 1):
                total = Q(0)
                for k in range(N + 1):
                    if 0 <= k - j <= N - ell:
                        total += Q(comb(ell, j) * comb(N - ell, k - j), comb(N, k))
                assert total == Q(N + 1, ell + 1)
                columns += 1
    checks['degree_elevation_exact_columns_' + str(columns)] = True
    if not all(checks.values()):
        raise ValueError('false analytic constant checks: ' + repr([k for k, v in checks.items() if not v]))
    return checks


if __name__ == '__main__':
    checks = rational_constant_checks()
    result = {'status': 'PASS exact rational constants; analytic proof separately reconstructed',
              'utc': datetime.now(timezone.utc).isoformat(),
              'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'count': len(checks)}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'count': len(checks)}))
