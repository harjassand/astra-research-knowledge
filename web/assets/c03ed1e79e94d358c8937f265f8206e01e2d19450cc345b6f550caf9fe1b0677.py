#!/usr/bin/env python3
"""Fresh C07_S01 exact constants for the N>=200 optimal-endpoint tail.

This imports no peer checking or arithmetic code. The log2 endpoints are
reacquired from positive exp Taylor/geometric bounds, unlike the author's
atanh(1/3) logarithm series. No finite-prefix certificate is examined here.
"""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
from datetime import datetime, timezone
from hashlib import sha256
import json


def exp_bounds(x, degree=18):
    assert 0 <= x < degree + 2
    lower = sum((x**j / factorial(j) for j in range(degree + 1)), Q(0))
    upper = lower + x**(degree + 1) / factorial(degree + 1) / (1 - x / (degree + 2))
    return lower, upper


def cos_sum(z, degree):
    assert degree % 2 == 0
    return sum(((-1)**(j // 2) * z**j / factorial(j) for j in range(0, degree + 1, 2)), Q(0))


def sin_sum(z, degree):
    assert degree % 2 == 1
    return sum(((-1)**((j - 1) // 2) * z**j / factorial(j) for j in range(1, degree + 1, 2)), Q(0))


def main():
    dlo, dhi = Q(138629, 100000), Q(13863, 10000)
    dbar = Q(138629437, 100000000)
    a, lam, ell, core = Q(241, 100), Q(101, 100), Q(25703, 25000), Q(1, 2)
    edge = a / 2
    B = a**2 / (4 * dhi)
    glow = 1 / (4 * dhi) - 2 * lam / 15
    phase = Q(15, 32) * Q(121, 6000)**2 * Q(10201, 2000000) / (Q(8, 7) * Q(9, 200)**3 * Q(21, 100))
    kappa = 1 - dhi * lam / 2 - Q(13, 87)
    r = B - 3 * dhi / 4
    exp1lo, _ = exp_bounds(Q(1), 4)
    checks = {
        'delta_lower_from_independent_positive_exp_upper': exp_bounds(dlo / 2)[1] < 2,
        'delta_upper_from_independent_positive_exp_lower': exp_bounds(dhi / 2)[0] > 2,
        'rational_prefix_bar_is_strictly_above_endpoint': exp_bounds(dbar / 2)[0] > 2,
        'a_below_pi_lower_three': a < 3,
        'saddle_contraction': dhi * lam / 2 < Q(71, 100),
        'edge_cos_bounds_positive': 0 < cos_sum(edge, 10) < cos_sum(edge, 8),
        'edge_C_upper': cos_sum(edge, 8)**2 < Q(13, 100),
        'edge_logsec_bound': cos_sum(edge, 10) * exp_bounds(ell)[0] > 1,
        'core_tan_ratio': sin_sum(core, 5) < Q(11, 10) * core * cos_sum(core, 6),
        'core_logsec_bound': cos_sum(core, 6) * exp_bounds(Q(2, 15))[0] > 1,
        'u0_tan_lower': sin_sum(Q(11, 10), 7) > Q(49, 25) * cos_sum(Q(11, 10), 8),
        'u0_logsec_upper': cos_sum(Q(11, 10), 6) * exp_bounds(Q(121, 150))[0] > 1,
        'core_phase_coefficient': Q(2, 5) * Q(11, 10)**2 / 24 == Q(121, 6000),
        'core_amplitude_coefficient': Q(8, 15) / 4 == Q(2, 15),
        'b_lower_exact': 1 / (4 * dhi) == Q(2500, 13863),
        'b_upper': 1 / (4 * dlo) < Q(181, 1000),
        'g_above_91_over_2000': glow > Q(91, 2000) > Q(9, 200),
        'sqrt_delta_lower': dlo > Q(8, 7)**2,
        'sqrt_g_lower': Q(9, 200) > Q(21, 100)**2,
        'L2_over_N3_at200': Q(202**2, 200**3) == Q(10201, 2000000),
        'sixth_phase_loss_twentieth': phase < Q(1, 20),
        'core_Gaussian_tail_prefactor_below_one': 4 * dhi < 3 * 200,
        'core_Gaussian_tail_exponent': 200 / (4 * dhi) > 8,
        'exp8_greater1000': exp_bounds(Q(2), 5)[0] > 7 and 7**4 > 1000,
        'near_outer_endpoint_one': glow > Q(91, 2000),
        'near_outer_endpoint_u0': Q(121, 25) / (4 * dhi) - lam * Q(121, 150) > Q(91, 2000),
        'pi_times_delta_above_four': 3 * dlo > 4,
        'sqrt200_upper': 200 < Q(99, 7)**2,
        'near_outer_prefactor': Q(6, 5) * Q(99, 7) / 2 == Q(297, 35),
        'exp3_greater20': exp_bounds(Q(3), 8)[0] > 20,
        'exp_point_one_greater11_tenths': exp_bounds(Q(1, 10), 2)[0] > Q(11, 10),
        'near_outer_error_thousandth': Q(297, 35 * 8800) < Q(1, 1000),
        'near_outer_bound_decreases': Q(1, 2 * 200) < Q(91, 2000),
        'far_outer_derivative_bound': Q(22, 5) * Q(181, 1000) - Q(49, 50) < -Q(9, 50),
        'far_outer_second_derivative_negative': 2 * Q(181, 1000) - (1 + Q(49, 25)**2) / 4 < 0,
        'far_outer_B_exact': B == Q(58081, 55452),
        'far_outer_gap_at200': B - lam * ell > Q(9, 1000),
        'N_fa_slope_positive': B - ell > 0,
        'sqrt200_lower': 200 > 14**2,
        'exp_nine_fifths_greater_eleven_halves': exp_bounds(Q(9, 5), 5)[0] > Q(11, 2),
        'far_outer_error_twenty_fifth': Q(25, 126) * Q(2, 11) == Q(25, 693) < Q(1, 25),
        'vertical_kappa_above_three_twentieths': kappa > Q(3, 20),
        'C_below_S': Q(13, 100) < Q(87, 100),
        'c_below_141_hundredths': dhi * lam < Q(141, 100),
        'e_above_eight_thirds': exp1lo > Q(8, 3),
        'vertical_prefactor_below_eleven_tenths': Q(141, 100) / (3 * Q(8, 3) * Q(3, 20)) < Q(11, 10)**2,
        'vertical_error_fifth': Q(11, 10) * Q(2, 11) == Q(1, 5),
        'total_error_budget': Q(1, 1000) + Q(1, 20) + Q(1, 1000) + Q(1, 25) + Q(1, 5) == Q(73, 250),
        'surviving_margin_two_thirds': Q(177, 250) > Q(2, 3),
        'correction_rate_positive': r > 0,
        'correction_exponent_at200_negative': -200 * r + dhi + dhi / 200 < 0,
        'correction_prefactor_below_quarter': 2304 * dhi < a**2 * 3 * 200,
    }
    assert all(checks.values()), [k for k, v in checks.items() if not v]
    result = {'status': 'PASS independently acquired exact constants, analytic N>=200 scope only',
              'utc': datetime.now(timezone.utc).isoformat(), 'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'log2_acquisition': 'independent positive exp Taylor degree18 plus geometric upper tail; no peer log series',
              'count': len(checks), 'checks': checks,
              'exact_values': {'g_lower': str(glow), 'phase_loss_upper': str(phase), 'kappa_lower': str(kappa),
                               'f_a_lower_at200': str(B - lam * ell), 'correction_rate_lower': str(r),
                               'correction_exponent_upper_at200': str(-200 * r + dhi + dhi / 200)},
              'finite_prefix': 'NOT READ OR REPLAYED; separate independent certificate gate'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'count': len(checks), 'exact_values': result['exact_values']}, indent=2))


if __name__ == '__main__':
    main()
