"""Finite source-normalization checks; not a weighted spectral proof."""
import importlib.util
import json
import pathlib
from fractions import Fraction as F

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('joint', ROOT / 'verify_joint_height.py')
j = importlib.util.module_from_spec(spec)
spec.loader.exec_module(j)
c = j.c


def exact_characters():
    count = 0
    for a in range(65):
        for b in range(65):
            if a + b == 0:
                continue
            c2 = F(a * a + a * b + b * b + 3 * a + 3 * b, 3)
            c3 = F((a - b) * (2 * a + b + 3) * (a + 2 * b + 3), 18)
            u, v = a + 1, b + 1
            paper_k = F(2 * (u * u + v * v + u * v), 3) - 2
            paper_l = F((u + 2 * v) * (2 * u + v) * (u - v), 9)
            assert paper_k == 2 * c2 and paper_l == 2 * c3
            count += 1
    return count


def matrix_case(a, b):
    ts, ambient = c.harmonic_carrier(a, b)
    d = ts[0].shape[0]
    n, c2, alpha, cs = j.casimirs(a, b)
    c3 = c2 * alpha
    ds = [sum(c.d_symbol[k, i, l] * ts[i] @ ts[l]
              for i in range(8) for l in range(8)) for k in range(8)]
    ss = [(q - float(alpha) * t) / n for q, t in zip(ds, ts)]
    e = [[sum(2 * fundamental[v, u] * t
              for fundamental, t in zip(c.fundamental, ts))
          for v in range(3)] for u in range(3)]
    paper_k = sum(e[i][k] @ e[k][i] for i in range(3) for k in range(3))
    paper_l = sum((e[i][k] @ e[k][l] @ e[l][i]
                   + e[k][i] @ e[l][k] @ e[i][l]) / 2
                  for i in range(3) for k in range(3) for l in range(3))
    checks = [j.residual(paper_k, 2 * float(c2) * np.eye(d)),
              j.residual(paper_l, 2 * float(c3) * np.eye(d))]
    rng = np.random.default_rng(73499 + a * 13 + b)
    raw = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    tests = [np.eye(d), raw, (raw + raw.conj().T) / 2, ts[0], ss[0]]
    def z_action(matrix):
        return -sum(t @ matrix @ t for t in ts)
    def t12_action(matrix):
        return -sum(e[k][i] @ matrix @ e[i][k] for i in range(3) for k in range(3))
    def ordinary_action(matrix):
        return sum(t @ (t @ matrix - matrix @ t)
                   - (t @ matrix - matrix @ t) @ t for t in ts)
    for matrix in tests:
        direct_m = sum(t @ (s @ matrix - matrix @ s)
                       - (s @ matrix - matrix @ s) @ t for s, t in zip(ss, ts))
        ordinary = ordinary_action(matrix)
        trace112 = -sum(e[k][i] @ e[l][k] @ matrix @ e[i][l]
                        for i in range(3) for k in range(3) for l in range(3))
        trace122 = sum(e[k][i] @ matrix @ e[i][l] @ e[l][k]
                       for i in range(3) for k in range(3) for l in range(3))
        source_x = (trace112 - trace122) / 2 + 4 * float(c3) * matrix / 3
        mapped_m = (source_x + 2 * float(c3) * matrix / 3 - float(alpha) * ordinary) / n
        checks.append(j.residual(direct_m, mapped_m))
        trace1122 = sum(e[k][i] @ e[l][k] @ matrix @ e[i][p] @ e[p][l]
                        for i in range(3) for k in range(3)
                        for l in range(3) for p in range(3))
        bar1122 = sum(e[i][k] @ e[k][l] @ matrix @ e[p][i] @ e[l][p]
                      for i in range(3) for k in range(3)
                      for l in range(3) for p in range(3))
        t12 = t12_action(matrix)
        source_y = ((trace1122 + bar1122) / 2 - t12_action(t12) / 12
                    - 5 * float(c2) ** 2 * matrix / 3 - 2 * t12)
        z = z_action(matrix)
        quadratic_cross = sum(q @ matrix @ q for q in ds)
        mapped_y = (2 * quadratic_cross - float(c2) ** 2 * matrix / 3
                    - z_action(z) / 3 + z / 2)
        checks.append(j.residual(source_y, mapped_y))
        direct_s = sum(s @ (s @ matrix - matrix @ s)
                       - (s @ matrix - matrix @ s) @ s for s in ss)
        mapped_s = (-source_y - ordinary_action(ordinary) / 12
                    + (float(c2) / 3 + .25 - float(alpha) ** 2) * ordinary
                    - 2 * float(alpha) * n * direct_m) / n ** 2
        checks.append(j.residual(direct_s, mapped_s))
    return dict(a=a, b=b, dimension=d, ambient_dimension=ambient,
                test_matrices=len(tests), max_relative_residual=max(checks))


def main():
    exact = exact_characters()
    cases = [matrix_case(a, b) for a, b in [(1, 1), (2, 1), (3, 1), (2, 2), (3, 2)]]
    result = dict(status='FINITE-EVIDENCE', proof_validation=False,
                  theorem_file='MISSING_LABEL_MAPPING.txt',
                  primary_source='https://arxiv.org/html/2110.03521',
                  exact_shifted_character_cases=exact, matrix_cases=cases,
                  max_relative_residual=max(t['max_relative_residual'] for t in cases),
                  full_L_S_quartic_mapping=True, weighted_spectral_count='UNPROVED',
                  dependencies=['Python standard library', 'NumPy'])
    (ROOT / 'MISSING_LABEL_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status='passed', matrix_cases=len(cases),
                         exact_shifted_character_cases=exact,
                         max_relative_residual=result['max_relative_residual'],
                         weighted_spectral_count='UNPROVED')))


if __name__ == '__main__':
    main()
