#!/usr/bin/env python3
"""Exact controls for the temporal-exposure information construction.

This is supplied-record mathematics. There are no native source observations,
preparations, physical measurements, or intervention assays in this checker.
Rational pseudo-random arrays below select mathematical inequality controls.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import random
import time

ROOT = Path(__file__).resolve().parent


def inverse(a):
    n = len(a)
    r = [[F(x) for x in row] + [F(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        pivot = next(k for k in range(j, n) if r[k][j])
        r[j], r[pivot] = r[pivot], r[j]
        scale = r[j][j]
        r[j] = [x / scale for x in r[j]]
        for i in range(n):
            if i != j:
                scale = r[i][j]
                r[i] = [x - scale * y for x, y in zip(r[i], r[j])]
    out = [row[n:] for row in r]
    for i in range(n):
        for j in range(n):
            assert sum(F(a[i][k]) * out[k][j] for k in range(n)) == (i == j)
    return out


def vm(v, a):
    return [sum(v[i] * a[i][j] for i in range(len(v)))
            for j in range(len(a[0]))]


def resolvent(q, dose, d=(0, 1, 10), clock=F(1), death=F(1)):
    return [[clock * x for x in row] for row in inverse([
        [F(i == j) * (clock + death + dose * d[i]) - q[i][j]
         for j in range(3)] for i in range(3)])]


def staged_probability(q, doses):
    z = [F(1, 3)] * 3
    for dose in doses:
        z = vm(z, resolvent(q, F(dose)))
    return sum(z)


def full_killed_probability(q, doses):
    m = len(doses)
    n = 3 * m
    g = [[F(0) for _ in range(n)] for _ in range(n)]
    success = [F(0)] * n
    for stage, dose in enumerate(doses):
        for i in range(3):
            for j in range(3):
                g[3 * stage + i][3 * stage + j] = -q[i][j]
            g[3 * stage + i][3 * stage + i] += 2 + dose * (0, 1, 10)[i]
            if stage + 1 < m:
                g[3 * stage + i][3 * (stage + 1) + i] = -1
            else:
                success[3 * stage + i] = 1
    gi = inverse(g)
    h = [sum(gi[i][j] * success[j] for j in range(n)) for i in range(n)]
    assert all(F(0) <= x <= F(1) for x in h)
    return sum(h[:3]) / 3


def temporal_inequality_controls():
    rng = random.Random(20261029)
    checks = 0
    n_fine = 64
    for channels in [1, 2]:
        for m in [1, 2, 4, 8, 16, 32, 64]:
            width = n_fine // m
            for trial in range(40):
                lhs = F(0)
                rhs = F(0)
                for _ in range(channels):
                    intensity = [F(rng.randrange(21), 2) for _ in range(n_fine)]
                    schedule = [F(rng.randrange(9), 4) for _ in range(n_fine)]
                    variation = sum(abs(schedule[i] - schedule[i-1])
                                    for i in range(1, n_fine))
                    masses = [sum(intensity[j*width:(j+1)*width]) / n_fine
                              for j in range(m)]
                    lhs += sum(abs(schedule[i] - schedule[(i//width)*width])
                               * intensity[i] / n_fine for i in range(n_fine))
                    rhs += variation * max(masses)
                assert lhs <= rhs
                if m == n_fine:
                    assert lhs == 0
                checks += 1
    return checks


def main():
    started = time.perf_counter()
    q = [[F(-1), F(1), F(0)], [F(0), F(-1), F(1)], [F(1), F(0), F(-1)]]
    qt = [list(row) for row in zip(*q)]
    assert all(sum(row) == 0 for row in q)
    assert all(sum(q[i][j] for i in range(3)) == 0 for j in range(3))
    constant_checks = []
    for dose in [F(0), F(1, 10), F(1), F(2), F(10), F(100)]:
        for clock in [F(1, 3), F(1), F(3), F(11)]:
            a = sum(vm([F(1, 3)]*3, resolvent(q, dose, clock=clock)))
            b = sum(vm([F(1, 3)]*3, resolvent(qt, dose, clock=clock)))
            assert a == b
            constant_checks.append({'dose': str(dose), 'stage_rate': str(clock),
                                    'probability': str(a)})
    switched = []
    for doses in [(1, 10), (10, 1), (1, 2, 10), (1, 10, 1), (0, 1, 10)]:
        p = staged_probability(q, doses)
        pt = staged_probability(qt, doses)
        assert p == full_killed_probability(q, doses)
        assert pt == full_killed_probability(qt, doses)
        assert p == staged_probability(qt, doses[::-1])
        switched.append({'doses': doses, 'clockwise': str(p), 'counterclockwise': str(pt),
                         'difference': str(p-pt), 'float_values': [float(p), float(pt)]})
    assert F(switched[0]['difference']) < 0
    assert F(switched[3]['difference']) == 0
    results = {
        'kind': 'supplied mathematical construction, not acquisition',
        'native_observations': 0, 'native_preparations': 0,
        'baseline_death_intensity': 1,
        'reset': ['1/3']*3, 'known_controlled_intensity_values': [0, 1, 10],
        'baseline_and_paired_total_exposure_equality': 'ordinary stationary path-reversal proof',
        'constant_resolvent_controls': constant_checks,
        'full_killed_system_comparisons': 2*len(switched),
        'switched': switched,
        'temporal_modulus_rational_controls': temporal_inequality_controls(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'elapsed_seconds': time.perf_counter()-started,
    }
    path = ROOT/'TEMPORAL_EXPOSURE_CHECKS.json'
    path.write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
