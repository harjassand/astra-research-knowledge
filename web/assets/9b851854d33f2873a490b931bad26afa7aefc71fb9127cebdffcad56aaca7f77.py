"""Finite exact/dense evidence for the uniform principal-height upper.

The weighted all-matrix lower remains unproved. This script checks
character counts, explicit filters, inverse ranks and finite endpoints.
"""
import bisect
import importlib.util
import itertools
import json
import math
import pathlib
from fractions import Fraction as F

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('joint', ROOT / 'verify_joint_height.py')
j = importlib.util.module_from_spec(spec)
spec.loader.exec_module(j)
c = j.c


def stable(t):
    return (t + 2) ** 2 // 4 if t >= 0 else 0


def character(a, b):
    n = a + b
    result = []
    shifts = [a + 1, b + 1, n + 2]
    for t in range(2 * n + 1):
        result.append(sum((-1) ** len(subset) * stable(t - sum(subset))
                          for size in range(4)
                          for subset in itertools.combinations(shifts, size)))
    return result


def exact_controls():
    chars = shells = taper_norms = inverse_ranks = hole_ranks = endpoints = 0
    for a in range(1, 97):
        for b in range(1, a + 1):
            n, B = a + b, b + 1
            d = (a + 1) * B * (n + 2) // 2
            g = character(a, b)
            assert all(v >= 0 for v in g) and sum(g) == d and g == g[::-1]
            assert B * a * a <= 2 * d <= 8 * B * a * a
            prefix = [0]
            s1 = s2 = 0
            for t in range(a):
                assert g[t] == stable(t) - stable(t - B)
                assert (t + 1) * min(t + 1, B) <= 4 * g[t]
                assert g[t] <= (t + 1) * min(t + 1, B)
                shells += 1
                r = t + 1
                prefix.append(prefix[-1] + g[t])
                s1 += t * g[t]
                s2 += t * t * g[t]
                assert r * r * min(r, B) <= 32 * prefix[-1]
                assert prefix[-1] <= r * r * min(r, B)
                norm = r * r * prefix[-1] - 2 * r * s1 + s2
                assert r ** 4 * min(r, B) <= 1024 * norm
                taper_norms += 1
            assert 2 * prefix[-1] <= d
            for q in set([1, d // 2, prefix[-1], max(1, prefix[-1] - 1),
                          min(d // 2, B ** 3), min(d // 2, B ** 3 + 1)]):
                if not 1 <= q <= d // 2:
                    continue
                r = min(a, bisect.bisect_right(prefix, q) - 1)
                assert r >= 1 and prefix[r] <= q
                assert 8 * r ** 3 >= q and 4 * B * r * r >= q
                inverse_ranks += 1
            if a >= 16:
                maximum = a // 16
                assert maximum >= F(a, 32)
                assert min(maximum, B) >= F(B, 64)
                assert prefix[maximum] * 2 ** 23 >= d
                for r in range(1, maximum + 1):
                    assert 32 * prefix[2 * r] <= d
                    for k in set([prefix[r], prefix[r - 1] + 1]):
                        h = r * min(r, B)
                        assert h ** 3 <= 64 ** 3 * k * k
                        assert h * h <= 64 ** 2 * B * k
                        hole_ranks += 1
                k = prefix[maximum]
                assert n ** 3 * k * k * 2 ** 51 >= d ** 3
                assert n * n * B * k * 2 ** 34 >= d * d
                endpoints += 1
            else:
                assert d <= 4096
            chars += 1
    return dict(exact_principal_characters=chars, exact_shell_comparisons=shells,
                exact_taper_norm_bounds=taper_norms, exact_inverse_rank_cases=inverse_ranks,
                exact_hole_rank_cases=hole_ranks, exact_fixed_fraction_endpoints=endpoints)


def root_controls():
    roots = tapers = holes = 0
    for a, b in [(1, 1), (4, 1), (8, 1), (12, 2), (16, 1),
                 (20, 3), (12, 8), (8, 8), (24, 4), (32, 1)]:
        data = j.exact_roots(a, b)
        n, B, cs, g = data['N'], b + 1, data['C_S'], data['g']
        assert g == character(a, b)
        for t in range(a + 1):
            v = (t + 1) ** 2 * min(t + 1, B)
            for i, k, step in j.POSITIVE_ROOTS:
                assert data['ordinary'][(i, k)][t] <= 4 * n * v
                assert data['mixed'][(i, k)][t] ** 2 <= 4 * cs * v * v
                roots += 1
        for r in range(1, a + 1):
            profile = [F(max(r - t, 0)) for t in range(2 * n + 1)]
            norm = sum(g[t] * p * p for t, p in enumerate(profile))
            et = j.energy(profile, data, 'ordinary')
            cross = j.energy(profile, data, 'mixed')
            v = r ** 3 * min(r, B)
            assert et <= 24 * n * v
            assert cross ** 2 <= 144 * cs * v * v
            assert et * r <= 24576 * n * norm
            assert (cross * r) ** 2 <= 12288 ** 2 * cs * norm * norm
            tapers += 1
        for r in range(1, a // 16 + 1):
            profile = [F(0) if t < r else min(F(1), F(t - r + 1, r))
                       for t in range(2 * n + 1)]
            norm = sum(g[t] * p * p for t, p in enumerate(profile))
            et = j.energy(profile, data, 'ordinary')
            cross = j.energy(profile, data, 'mixed')
            v = r * min(r, B)
            assert norm >= F(sum(g), 2)
            assert et <= 384 * n * v
            assert cross ** 2 <= 192 ** 2 * cs * v * v
            holes += 1
    return dict(exact_root_controls=roots, exact_extended_tapers=tapers,
                exact_extended_holes=holes)


def matrix_case(a, b):
    ts, ambient = c.harmonic_carrier(a, b)
    d = ts[0].shape[0]
    n, c2, alpha, cs = j.casimirs(a, b)
    ss = [(sum(c.d_symbol[k, i, l] * ts[i] @ ts[l]
               for i in range(8) for l in range(8)) - float(alpha) * ts[k]) / n
          for k in range(8)]
    coeff = [2 * np.trace(t @ np.diag([1., 0., -1.])) for t in c.fundamental]
    height = sum(w * t for w, t in zip(coeff, ts))
    vals, basis = np.linalg.eigh(height)
    data = j.exact_roots(a, b)
    B, checks, controls = b + 1, [], []
    profiles = []
    for r in sorted(set([1, b, min(a, B), max(1, a // 2), a])):
        profiles.append(('taper', r, [F(max(r - t, 0)) for t in range(2 * n + 1)]))
    for r in range(1, a // 16 + 1):
        profiles.append(('hole', r, [F(0) if t < r else min(F(1), F(t - r + 1, r))
                                     for t in range(2 * n + 1)]))
    defects = np.rint(n - vals).astype(int)
    for kind, r, profile in profiles:
        filter_matrix = (basis * [float(profile[t]) for t in defects]) @ basis.conj().T
        norm = float(np.linalg.norm(filter_matrix) ** 2)
        et = c.old.energy(filter_matrix, ts)
        cross = sum(np.trace((s @ filter_matrix - filter_matrix @ s).conj().T
                            @ (t @ filter_matrix - filter_matrix @ t)).real
                    for s, t in zip(ss, ts))
        checks.append(j.residual(et, float(j.energy(profile, data, 'ordinary'))))
        checks.append(j.residual(cross, float(j.energy(profile, data, 'mixed'))))
        checks.append(j.residual(norm, float(sum(data['g'][t] * p * p
                                                for t, p in enumerate(profile)))))
        rank = int(np.linalg.matrix_rank(filter_matrix, tol=1e-8))
        assert rank == sum(data['g'][t] for t, p in enumerate(profile) if p)
        if kind == 'taper':
            assert et <= 24576 * n * norm / r + 1e-7
            assert cross ** 2 <= 12288 ** 2 * float(cs) * norm * norm / (r * r) + 1e-7
        else:
            assert norm >= d / 2 - 1e-8
            assert et <= 384 * n * r * min(r, B) + 1e-7
        controls.append(dict(kind=kind, R=r, rank=rank,
                             E_T_over_norm=et / norm,
                             E_TS_over_norm=cross / norm))
    return dict(a=a, b=b, N=n, dimension=d, ambient_dimension=ambient,
                controls=controls, max_relative_residual=max(checks))


def main():
    exact = exact_controls()
    exact.update(root_controls())
    cases = [matrix_case(a, b) for a, b in [(4, 1), (6, 1), (8, 1),
                                          (4, 2), (6, 2), (4, 4), (16, 1)]]
    result = dict(status='FINITE-EVIDENCE', proof_validation=False,
                  theorem_file='UNIFORM_PRINCIPAL_UPPER.txt',
                  weighted_all_matrix_lower='UNPROVED', optimal_wall_profile='UNKNOWN',
                  exact_checks=exact, matrix_cases=cases,
                  max_relative_residual=max(t['max_relative_residual'] for t in cases),
                  dependencies=['Python standard library', 'NumPy'])
    (ROOT / 'UNIFORM_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status='passed', matrix_cases=len(cases), **exact,
                         max_relative_residual=result['max_relative_residual'],
                         weighted_all_matrix_lower='UNPROVED')))


if __name__ == '__main__':
    main()
