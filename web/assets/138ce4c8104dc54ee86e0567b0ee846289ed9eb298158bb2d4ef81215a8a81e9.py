#!/usr/bin/env python3
"""Exact bounded diagnostics for the analytically proved common nonlinear drift.

No simulation, solver, peer execution, or exhaustive core enumeration.  Rational
fixtures check transcription; the all-state proof is COMMON_NONLINEAR.txt.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import time


def potential(a, b, c):
    s = b + c
    u = max(b - 3 * c, 0)
    return 1 + F((a - 1) ** 2, 8) + s + F(u * u, 4 * (s + 1)) + F(a, s + 1) + F(a, 64 * (b + 1))


def generator(a, b, c, k):
    v = potential(a, b, c)
    reactions = [
        (k * a * c, (a, b + 1, c - 1)),
        (a * b, (a, b - 1, c + 1)),
        (a * b, (a - 1, b, c)),
        (b, (a + 1, b, c)),
        (c, (a, b, c - 1)),
        (1, (a, b, c + 1)),
    ]
    return sum((rate * (potential(*y) - v) for rate, y in reactions if rate), F(0))


def closed_generator(a, b, c, k):
    s = b + c
    if s == 0:
        return 1 - F(a, 2)
    u = b - 3 * c
    pos = lambda z: max(z, 0) ** 2
    conv = F(a, 4 * (s + 1)) * (k * c * (pos(u + 4) - pos(u)) + b * (pos(u - 4) - pos(u)))
    birth = 1 + F(pos(u - 3), 4 * (s + 2)) - F(pos(u), 4 * (s + 1))
    death = c * (-1 + F(pos(u + 3), 4 * s) - F(pos(u), 4 * (s + 1)))
    a_square = F(b * (-2 * a * a + 5 * a - 1), 8)
    total_ratio = F(b * (1 - a), s + 1) + F(a * c, s * (s + 1)) - F(a, (s + 1) * (s + 2))
    b_ratio = F(b * (1 - a), b + 1) - F(k * a * a * c, (b + 1) * (b + 2))
    if b:
        b_ratio += F(a * a, b + 1)
    return conv + birth + death + a_square + total_ratio + b_ratio / 64


def lead_bound(a, b, c):
    s = b + c
    assert s > 0
    r = F(max(b - 3 * c, 0), s)
    R = 1 - (6 * r + r * r) / 4
    return F(b * (-2 * a * a + 5 * a - 1), 8) - c * R - 2 * a * r * (b - 2 * c)


def broad_bound(a, b, c):
    s = b + c
    if not s:
        return 1 - F(a, 2)
    if not b:
        return 1 - c + F(7 * a, 12) - F(a * a * c, 128)
    if a >= 3:
        return -F(s, 8) - F(a * a * b, 64) + F(21 * a, 2) + 9
    return -F(s, 32) + 10 * a + 9 + 3


def check_state(a, b, c, k):
    if not a + b:
        return False
    actual = generator(a, b, c, k)
    exact = closed_generator(a, b, c, k)
    assert actual == exact, (a, b, c, k, actual, exact)
    upper = broad_bound(a, b, c)
    assert actual <= upper, (a, b, c, k, actual, upper)
    s = b + c
    if s:
        lead = lead_bound(a, b, c)
        if a < 3:
            assert lead <= -F(s, 32), (a, b, c, lead)
        else:
            assert lead <= -F(s, 8) - F(a * a * b, 36), (a, b, c, lead)
    if a >= 1536 or s >= 20000:
        assert actual <= -1, (a, b, c, k, actual)
    return True


def recovery_word_check(initial):
    a, b, c = initial
    n0 = a + b + c
    assert a + b >= 1
    jumps = 0
    maximum_count = n0

    def fire(reaction):
        nonlocal a, b, c, jumps, maximum_count
        if reaction == 0:
            assert a * c >= 1
            b += 1
            c -= 1
        elif reaction == 1:
            assert a * b >= 1
            b -= 1
            c += 1
        elif reaction == 2:
            assert a * b >= 1
            a -= 1
        elif reaction == 3:
            assert b >= 1
            a += 1
        elif reaction == 4:
            assert c >= 1
            c -= 1
        elif reaction == 5:
            c += 1
        else:
            raise AssertionError(reaction)
        assert min(a, b, c) >= 0 and a + b >= 1
        jumps += 1
        maximum_count = max(maximum_count, a + b + c)

    if a == 0:
        fire(3)
    if a >= 2 and b == 0:
        fire(5)
        fire(0)
    while a > 1:
        fire(2)
    while b:
        fire(1)
    while c:
        fire(4)
    assert (a, b, c) == (1, 0, 0)
    fire(5)
    fire(0)
    fire(5)
    assert (a, b, c) == (1, 1, 1)
    assert jumps <= 2 * n0 + 7
    assert maximum_count <= n0 + 2
    return {'initial': list(initial), 'jumps': jumps, 'maximum_count': maximum_count}


def main():
    started = time.perf_counter()
    # Algebraic coefficient certificates: Bernstein coefficients prove f0>0;
    # completing the square bounds f1; all coefficients of f2 are negative.
    f0_power = [F(11, 8), -F(19, 8), F(5, 4), F(1, 4)]
    f0_bernstein = [F(11, 8), F(7, 12), F(5, 24), F(1, 2)]
    assert f0_bernstein[1] == f0_power[0] + f0_power[1] / 3
    assert f0_bernstein[2] == f0_power[0] + 2 * f0_power[1] / 3 + f0_power[2] / 3
    assert f0_bernstein[3] == sum(f0_power)
    assert min(f0_bernstein) >= F(1, 8)
    assert -F(1, 4) + F(9, 464) <= -F(1, 8)
    assert F(23, 1152) >= F(1, 64)
    assert 16 * F(21, 2) ** 2 + 9 == 1773
    assert -F(20000, 8) + 1773 <= -1
    assert 1536 >= 128 * F(21, 2)
    assert 32 * F(7, 12) ** 2 == F(98, 9)

    small = sum(check_state(a, b, c, F(k)) for a, b, c, k in product(range(13), range(26), range(26), (1, 2)))
    stressed = 0
    outside = 0
    avals = (0, 1, 2, 3, 4, 100, 1535, 1536, 1537, 4000)
    bvals = (0, 1, 2, 100, 19998, 19999, 20000)
    cvals = (0, 1, 2, 100, 19999, 20000, 50000)
    for a, b, c, k in product(avals, bvals, cvals, (F(1), F(3, 2), F(2))):
        ok = check_state(a, b, c, k)
        stressed += ok
        outside += ok and (a >= 1536 or b + c >= 20000)
    extra = [(10 ** 9, 1, 10 ** 8), (0, 10 ** 9, 10 ** 8), (1, 10 ** 9, 0),
             (2, 3 * 10 ** 9, 10 ** 9), (10 ** 9, 0, 1), (10 ** 9, 0, 0),
             (4, 10 ** 9, 10 ** 10)]
    for x, k in product(extra, (F(1), F(2))):
        assert check_state(*x, k)

    words = [recovery_word_check(x) for x in (
        (0, 1, 0), (1, 0, 0), (1535, 0, 19999), (0, 19999, 0),
        (1535, 19999, 0), (0, 10000, 9999), (1, 1, 1), (2, 0, 0))]
    M, H = 22000, 44007
    intensity_upper = 2 * M * M + M + 1
    assert intensity_upper == 968022001
    assert H == 2 * M + 7
    assert max(z['jumps'] for z in words) <= H
    assert 3 * intensity_upper < 2 ** 32
    R = 1 + F((M + 2) ** 2, 8) + F(145 * (M + 1), 64)

    out = {
        'result': 'PASS', 'scope': 'exact finite diagnostics and coefficient transcription; all-state proof in COMMON_NONLINEAR.txt',
        'small_grid_states': small, 'stressed_states': stressed, 'stressed_outside_core_states': outside,
        'binary_large_count_fixtures': len(extra) * 2,
        'control_rates_checked': ['1', '3/2', '2'],
        'analytic_coefficient_certificates': {'f0_power': list(map(str, f0_power)), 'f0_bernstein': list(map(str, f0_bernstein)), 'f1_upper': str(-F(1, 4) + F(9, 464)), 'large_a_square_constant': 1773},
        'core': {'a_lt': 1536, 'b_plus_c_lt': 20000, 'enumerated': False},
        'recovery_word_fixtures': words,
        'recovery_constants': {'M': M, 'H': H, 'intensity_upper': intensity_upper,
                               'success_probability': f'(3*{intensity_upper})^(-{H})',
                               'potential_upper_after_abort': str(R),
                               'materialized_probability_denominator_bits_upper': 32 * H + 1,
                               'expected_total_firings': 'UNKNOWN'},
        'seconds': time.perf_counter() - started,
    }
    Path(__file__).with_name('common_nonlinear_checks.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
