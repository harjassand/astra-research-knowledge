"""Exact principal character/root trace tests and independent dense checks.

The joint filter upper is the theorem under review. This script does
not establish the all-matrix weighted spectral count or optimal profile.
"""
import functools
import importlib.util
import json
import math
import pathlib
from collections import Counter
from fractions import Fraction as F

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('moments', ROOT / 'verify_wall_moments.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
c = m.c
POSITIVE_ROOTS = [(0, 1, 1), (1, 2, 1), (0, 2, 2)]


def casimirs(a, b):
    n = a + b
    c2 = F(a * a + a * b + b * b + 3 * a + 3 * b, 3)
    c3 = F((a - b) * (2 * a + b + 3) * (a + 2 * b + 3), 18)
    delta = c2 * (c2 / 3 + F(1, 4)) - c3 * c3 / c2
    return n, c2, c3 / c2, delta / n ** 2


@functools.lru_cache(None)
def exact_roots(a, b):
    n, c2, alpha, cs = casimirs(a, b)
    g = [0] * (2 * n + 1)
    ni = [[0] * (2 * n + 1) for _ in range(3)]
    ni2 = [[0] * (2 * n + 1) for _ in range(3)]
    for nu, multiplicity in m.weights(a, b):
        t = n - nu[0] + nu[2]
        g[t] += multiplicity
        for i in range(3):
            ni[i][t] += multiplicity * (nu[i] + b)
            ni2[i][t] += multiplicity * (nu[i] + b) ** 2
    ordinary = {}
    for i, j, step in POSITIVE_ROOTS:
        w = []
        for t in range(2 * n + 1):
            previous = w[t - step] if t >= step else 0
            w.append(previous + ni[i][t] - ni[j][t])
            assert w[-1] >= 0
        ordinary[(i, j)] = w
    qi = [[F(t) for t in row] for row in ni2]
    for i, j, step in POSITIVE_ROOTS:
        w = ordinary[(i, j)]
        for t in range(2 * n + 1):
            qi[i][t] += w[t - step] if t >= step else 0
            qi[j][t] += w[t]
    second = {}
    charge = F(a + 2 * b, 3)
    for i, j, step in POSITIVE_ROOTS:
        cross = []
        for t in range(2 * n + 1):
            ordinary_cartan = ni[i][t] - ni[j][t]
            quadratic_cartan = qi[i][t] - qi[j][t] + (F(3, 2) - 2 * charge) * ordinary_cartan
            second_cartan = (quadratic_cartan - alpha * ordinary_cartan) / n
            cross.append((cross[t - step] if t >= step else F(0)) + second_cartan)
        second[(i, j)] = cross
    return dict(a=a, b=b, N=n, C_S=cs, g=g, ordinary=ordinary, mixed=second)


def energy(profile, data, kind):
    values = data[kind]
    return sum(values[(i, j)][t] * (profile[t] - (profile[t + step]
               if t + step < len(profile) else F(0))) ** 2
               for i, j, step in POSITIVE_ROOTS for t in range(len(profile)))


def principal_numerator(g):
    # (1-z)^2(1-z^2) =1-2z+2z^3-z^4.
    return Counter({t: sum(coefficient * (g[t - p] if 0 <= t - p < len(g) else 0)
                           for p, coefficient in [(0, 1), (1, -2), (3, 2), (4, -1)])
                    for t in range(len(g) + 4)
                    if sum(coefficient * (g[t - p] if 0 <= t - p < len(g) else 0)
                           for p, coefficient in [(0, 1), (1, -2), (3, 2), (4, -1)])})


def expected_numerator(a, b):
    result = Counter({0: 1})
    for exponent in [a + 1, b + 1, a + b + 2]:
        new = Counter(result)
        for p, v in result.items():
            new[p + exponent] -= v
        result = new
    return Counter({p: v for p, v in result.items() if v})


def exact_checks():
    character_cases = root_bound_cases = taper_cases = hole_cases = 0
    for a in range(1, 17):
        for b in range(1, a + 1):
            data = exact_roots(a, b)
            n, cs, g = data['N'], data['C_S'], data['g']
            assert principal_numerator(g) == expected_numerator(a, b)
            for t in range(b + 1):
                assert g[t] == (t + 2) ** 2 // 4
                assert F((t + 1) ** 2, 4) <= g[t] <= (t + 1) ** 2
                for i, j, step in POSITIVE_ROOTS:
                    w = data['ordinary'][(i, j)][t]
                    cross = data['mixed'][(i, j)][t]
                    assert 0 <= w <= 4 * n * (t + 1) ** 3
                    assert cross ** 2 <= 4 * cs * (t + 1) ** 6
                    root_bound_cases += 1
            for r in range(1, b + 1):
                profile = [F(max(r - t, 0)) for t in range(2 * n + 1)]
                rank = sum(g[:r])
                norm = sum(g[t] * f * f for t, f in enumerate(profile))
                et, cross = energy(profile, data, 'ordinary'), energy(profile, data, 'mixed')
                assert F(r ** 3, 12) <= rank <= r ** 3
                assert norm >= F(r ** 5, 120)
                assert et <= 24 * n * r ** 4
                assert cross ** 2 <= 144 * cs * r ** 8
                taper_cases += 1
            for r in range(1, b // 4 + 1):
                profile = [F(0) if t < r else min(F(1), F(t - r + 1, r))
                           for t in range(2 * n + 1)]
                norm = sum(g[t] * f * f for t, f in enumerate(profile))
                et, cross = energy(profile, data, 'ordinary'), energy(profile, data, 'mixed')
                assert norm >= F(sum(g), 2)
                assert et <= 216 * n * r ** 2
                assert cross ** 2 <= 108 ** 2 * cs * r ** 4
                assert sum(g[t] for t, f in enumerate(profile) if not f) == sum(g[:r])
                hole_cases += 1
            character_cases += 1
    return dict(exact_principal_characters=character_cases,
                exact_root_bound_cases=root_bound_cases,
                exact_joint_tapers=taper_cases, exact_joint_holes=hole_cases)


def residual(value, expected, tolerance=5e-9):
    error = float(np.max(np.abs(np.asarray(value) - np.asarray(expected))))
    scale = max(1., float(np.max(np.abs(np.asarray(expected)))))
    if error / scale > tolerance:
        raise AssertionError((error, scale, value, expected))
    return error / scale


def matrix_case(a, b):
    ts, ambient = c.harmonic_carrier(a, b)
    d = ts[0].shape[0]
    data = exact_roots(a, b)
    n, c2, alpha, cs = casimirs(a, b)
    ds = [sum(c.d_symbol[k, i, j] * ts[i] @ ts[j]
              for i in range(8) for j in range(8)) for k in range(8)]
    ss = [(q - float(alpha) * t) / n for q, t in zip(ds, ts)]
    h = np.diag([1., 0., -1.])
    coeff = [2 * np.trace(t @ h) for t in c.fundamental]
    j_operator = sum(t * w for t, w in zip(ts, coeff))
    vals, basis = np.linalg.eigh(j_operator)
    shells = []
    for t in range(2 * n + 1):
        columns = basis[:, np.abs(vals - (n - t)) < 1e-8]
        shells.append(columns @ columns.conj().T)
    checks = [residual(sum(shells), np.eye(d))]
    for i, j, step in POSITIVE_ROOTS:
        root = np.zeros((3, 3), complex)
        root[i, j] = 1
        coeff = [2 * np.trace(t @ root) for t in c.fundamental]
        tr, sr = sum(t * w for t, w in zip(ts, coeff)), sum(s * w for s, w in zip(ss, coeff))
        for t in range(2 * n + 1):
            checks.append(residual(np.trace(shells[t] @ tr @ tr.conj().T),
                                   data['ordinary'][(i, j)][t]))
            checks.append(residual(np.trace(shells[t] @ sr @ tr.conj().T).real,
                                   float(data['mixed'][(i, j)][t])))
    profiles = []
    for r in range(1, b + 1):
        profile = [F(max(r - t, 0)) for t in range(2 * n + 1)]
        profiles.append(('taper', r, profile))
    for r in range(1, b // 4 + 1):
        profile = [F(0) if t < r else min(F(1), F(t - r + 1, r))
                   for t in range(2 * n + 1)]
        profiles.append(('hole', r, profile))
    controls = []
    for kind, r, profile in profiles:
        f = sum(float(value) * p for value, p in zip(profile, shells))
        norm = float(np.linalg.norm(f) ** 2)
        et, es = c.old.energy(f, ts), c.old.energy(f, ss)
        cross = sum(np.trace((s @ f - f @ s).conj().T @ (t @ f - f @ t)).real
                    for s, t in zip(ss, ts))
        checks.append(residual(et, float(energy(profile, data, 'ordinary'))))
        checks.append(residual(cross, float(energy(profile, data, 'mixed'))))
        checks.append(residual(norm, float(sum(data['g'][t] * value * value
                                               for t, value in enumerate(profile)))))
        rank = int(np.linalg.matrix_rank(f, tol=1e-8))
        assert rank == sum(data['g'][t] for t, value in enumerate(profile) if value)
        controls.append(dict(kind=kind, R=r, rank=rank,
                             E_T_over_norm=et / norm,
                             E_S_over_norm=es / norm,
                             E_TS_over_norm=cross / norm,
                             weighted_energy=et / (norm * n ** 2)
                                              + es / (norm * n * math.sqrt(float(cs)))))
    return dict(a=a, b=b, N=n, dimension=d, ambient_dimension=ambient,
                controls=controls, max_relative_residual=max(checks))


def main():
    exact = exact_checks()
    cases = [matrix_case(a, b) for a, b in [(1, 1), (2, 1), (3, 2),
                                          (4, 3), (5, 2), (8, 1), (4, 4)]]
    result = dict(status='FINITE-EVIDENCE', proof_validation=False,
                  theorem_file='JOINT_HEIGHT_UPPER.txt',
                  optimal_wall_profile='UNKNOWN', weighted_spectral_count='UNPROVED',
                  exact_checks=exact, matrix_cases=cases,
                  max_relative_residual=max(t['max_relative_residual'] for t in cases),
                  dependencies=['Python standard library', 'NumPy'])
    (ROOT / 'JOINT_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status='passed', matrix_cases=len(cases), **exact,
                         max_relative_residual=result['max_relative_residual'],
                         optimal_wall_profile='UNKNOWN')))


if __name__ == '__main__':
    main()
