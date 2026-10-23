"""Independent exact-rational diagnostics of the finite-bit secant compiler.

This is a small falsification harness, not the main implementation or a benchmark.
Run with: python p3_work/verification/check_secant.py
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import time


def mv(A, x):
    return [sum((a*v for a, v in zip(row, x)), F(0)) for row in A]


def lower(z):
    return z**3/4


def upper(z, M=F(1)):
    return 3*M*M*z - 3*M*z*z + z**3


def down(x, B):
    den = 1 << B
    return F((x*den).__floor__(), den)


def up(x, B):
    den = 1 << B
    return F((x*den).__ceil__(), den)


def scalar_checks():
    pairs = monotone_pairs = 0
    for M in (F(1, 4), F(1, 2), F(1)):
        grid = [M*F(i, 16) for i in range(-16, 17)]
        for a in grid:
            for b in grid:
                if a < b:
                    continue
                z = a-b
                assert lower(z) <= a**3-b**3 <= upper(z, M)
                pairs += 1
        zs = [2*M*F(i, 32) for i in range(33)]
        for z0, z1 in zip(zs, zs[1:]):
            assert lower(z0) <= lower(z1)
            assert upper(z0, M) <= upper(z1, M)
            monotone_pairs += 1
        for z in zs:
            assert (z/2)**3-(-z/2)**3 == lower(z)
            assert M**3-(M-z)**3 == upper(z, M)
    return {'endpoint_pairs_exact': pairs,
            'adjacent_monotonicity_pairs_exact': monotone_pairs,
            'sharp_endpoints_checked_exactly': True}


def envelope(case, start, site, B=8):
    d, T = case['d'], case['T']
    rho, kappa, sigma, A = (case[k] for k in ('rho', 'kappa', 'sigma', 'A'))
    M = [F(0)]
    Mgrid = [F(0)]
    for t in range(T):
        M.append(rho*M[-1]+kappa*M[-1]**3+sigma)
        Mgrid.append(min(F(1), up(rho*Mgrid[-1]+kappa*Mgrid[-1]**3+sigma, B)))
        assert M[-1] <= Mgrid[-1] <= 1
    impulse = [2*sigma*(j == site) for j in range(d)]
    lo, hi, hit = (list(impulse) for _ in range(3))
    dlo, dhi = (list(impulse) for _ in range(2))
    glo = [down(z, B) for z in impulse]
    ghi = [min(up(z, B), 2*Mgrid[start+1]) for z in impulse]
    result = {}
    for s in range(start+1, T+1):
        assert all(0 <= l <= h <= 2 for l, h in zip(lo, hi))
        assert all(0 <= h <= 2*M[s] for h in hit)
        assert all(dl <= l <= ht <= h <= dh
                   for dl, l, ht, h, dh in zip(dlo, lo, hit, hi, dhi))
        assert all(gl <= l and ht <= gh
                   for gl, l, ht, gh in zip(glo, lo, hit, ghi))
        result[s] = {'lo': lo, 'hi': hi, 'time_hi': hit,
                     'derivative_lo': dlo, 'derivative_hi': dhi,
                     'grid_lo': glo, 'grid_hi': ghi}
        if s == T:
            break
        alo, ahi, ahit = mv(A, lo), mv(A, hi), mv(A, hit)
        adhi, aglo, aghi = mv(A, dhi), mv(A, glo), mv(A, ghi)
        lo = [rho*l+kappa*lower(z) for l, z in zip(lo, alo)]
        hi = [rho*h+kappa*upper(z) for h, z in zip(hi, ahi)]
        hit = [rho*h+kappa*upper(z, M[s]) for h, z in zip(hit, ahit)]
        dlo = [rho*l for l in dlo]
        dhi = [rho*h+3*kappa*z for h, z in zip(dhi, adhi)]
        glo = [max(F(0), down(rho*l+kappa*lower(z), B))
               for l, z in zip(glo, aglo)]
        ghi = [min(2*Mgrid[s+1], up(rho*h+kappa*upper(z, Mgrid[s]), B))
               for h, z in zip(ghi, aghi)]
    return result


def trajectory(case, bits):
    d, T = case['d'], case['T']
    rho, kappa, sigma, A = (case[k] for k in ('rho', 'kappa', 'sigma', 'A'))
    x = [F(0)]*d
    path = [x]
    for t in range(T):
        ax = mv(A, x)
        x = [rho*v+kappa*z**3+sigma*(2*bits[t*d+j]-1)
             for j, (v, z) in enumerate(zip(x, ax))]
        assert all(-1 <= v <= 1 for v in x)
        path.append(x)
    return path


def trajectory_checks(case):
    d, T = case['d'], case['T']
    states = list(product((0, 1), repeat=d*T))
    paths = [trajectory(case, bits) for bits in states]
    env = {(t, j): envelope(case, t, j) for t in range(T) for j in range(d)}
    bits_checked = components_checked = 0
    max_grid_width = F(0)
    for i, bits in enumerate(states):
        for k in range(d*T):
            if bits[k]:
                continue
            t, j = divmod(k, d)
            other = i ^ (1 << (d*T-1-k))
            actual_score = lower_score = upper_score = grid_low_score = grid_up_score = F(0)
            for s in range(t+1, T+1):
                delta = [y-x for x, y in zip(paths[i][s], paths[other][s])]
                e = env[t, j][s]
                for z, lo, hi, th, gl, gh in zip(delta, e['lo'], e['hi'], e['time_hi'],
                                                e['grid_lo'], e['grid_hi']):
                    assert 0 <= lo <= z <= th <= hi
                    assert gl <= z <= gh
                    max_grid_width = max(max_grid_width, gh-gl)
                    components_checked += 1
                # Nonconstant positive b_s catches time-index mistakes in summation.
                b = [F((s+j) % 4+1, 20) for j in range(d)]
                actual_score += sum((v*w for v, w in zip(b, delta)), F(0))
                lower_score += sum((v*w for v, w in zip(b, e['lo'])), F(0))
                upper_score += sum((v*w for v, w in zip(b, e['time_hi'])), F(0))
                grid_low_score += sum((v*w for v, w in zip(b, e['grid_lo'])), F(0))
                grid_up_score += sum((v*w for v, w in zip(b, e['grid_hi'])), F(0))
            assert lower_score <= actual_score <= upper_score
            assert grid_low_score <= actual_score <= grid_up_score
            bits_checked += 1
    return {'name': case['name'], 'd': d, 'T': T, 'paths': len(states),
            'bit_pairs_exact': bits_checked, 'component_comparisons_exact': components_checked,
            'all_enclosures_hold_exactly': True, 'derivative_dominance_exact': True,
            'reachable_cube_dominance_exact': True, 'outward_grid_bits': 8,
            'max_grid_component_interval_width': float(max_grid_width),
            'rho_plus_3kappa': str(case['rho']+3*case['kappa'])}


def invalid_variant_checks():
    # Wrong absolute time index: at propagation X_1 -> X_2, use M_0=0
    # instead of the proved M_1=sigma=9/20. Shared other innovation is +1.
    rho, kappa, sigma = F(1, 2), F(1, 20), F(9, 20)
    A = [[F(3, 4), F(1, 4)], [F(1, 4), F(3, 4)]]
    before = [-sigma, sigma]
    after = [sigma, sigma]
    z0, z1 = mv(A, before), mv(A, after)
    gap = z1[1]-z0[1]
    actual = kappa*(z1[1]**3-z0[1]**3)
    wrong = kappa*upper(gap, F(0))
    correct = kappa*upper(gap, sigma)
    assert wrong < actual == correct
    # Inward rounding of the upper impulse excludes the actual initial difference.
    impulse = 2*sigma
    inward = down(impulse, 8)
    assert inward < impulse
    return {'wrong_time_index': {'actual_component_gap': str(actual),
                               'invalid_upper_bound': str(wrong),
                               'correct_upper_bound': str(correct),
                               'violation_factor': float(actual/wrong)},
            'inward_rounding': {'actual_impulse': str(impulse),
                               'invalid_upper_impulse': str(inward)}}


if __name__ == '__main__':
    start = time.perf_counter()
    cases = [
        {'name': 'symmetric_two_site', 'd': 2, 'T': 4, 'rho': F(1, 2),
         'kappa': F(1, 20), 'sigma': F(9, 20),
         'A': [[F(3, 4), F(1, 4)], [F(1, 4), F(3, 4)]]},
        {'name': 'asymmetric_three_site', 'd': 3, 'T': 3, 'rho': F(1, 3),
         'kappa': F(1, 10), 'sigma': F(17, 30),
         'A': [[F(1, 2), F(1, 2), F(0)], [F(0), F(1, 3), F(2, 3)],
               [F(1, 4), F(0), F(3, 4)]]},
        {'name': 'noncontractive_but_box_invariant', 'd': 2, 'T': 3, 'rho': F(4, 5),
         'kappa': F(1, 10), 'sigma': F(1, 10),
         'A': [[F(1, 3), F(2, 3)], [F(3, 4), F(1, 4)]]}
    ]
    result = {'scalar': scalar_checks(),
              'trajectory_cases': [trajectory_checks(c) for c in cases],
              'invalid_variant_counterexamples': invalid_variant_checks()}
    result['elapsed_seconds_observed'] = time.perf_counter()-start
    Path(__file__).with_name('secant_audit_results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
