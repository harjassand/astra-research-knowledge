"""Finite antisymmetric-lift and pure-to-warm EB conventions only."""
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np


def occupations(k):
    return [(a, b, k - a - b) for a in range(k + 1)
            for b in range(k - a + 1)]


def factorial_product(n):
    return math.prod(math.factorial(x) for x in n)


def generators(k):
    occ = occupations(k)
    ix = {v: i for i, v in enumerate(occ)}
    d = len(occ)
    roots = [[np.zeros((d, d), complex) for j in range(3)]
             for i in range(3)]
    for col, n in enumerate(occ):
        for i in range(3):
            roots[i][i][col, col] = n[i]
            for j in range(3):
                if i == j or not n[j]:
                    continue
                target = list(n)
                target[i] += 1
                target[j] -= 1
                roots[i][j][ix[tuple(target)], col] = math.sqrt(
                    (n[i] + 1) * n[j])
    result = []
    for i, j in ((0, 1), (0, 2), (1, 2)):
        result += [(roots[i][j] + roots[j][i]) / 2,
                   (roots[i][j] - roots[j][i]) / (2j)]
    result += [(roots[0][0] - roots[1][1]) / 2,
               (roots[0][0] + roots[1][1] - 2 * roots[2][2]) /
               (2 * math.sqrt(3))]
    return result


def epsilon_isometry(k):
    occ = occupations(k)
    ix = {n: i for i, n in enumerate(occ)}
    d = len(occ)
    w = np.zeros((d, d, d), complex)
    pairs = ((1, 2), (2, 0), (0, 1))
    zero = (0, 0, 0, 0, 0, 0)
    for col, n in enumerate(occ):
        polynomial = {zero: 1}
        for axis, count in enumerate(n):
            i, j = pairs[axis]
            for step in range(count):
                next_poly = {}
                for power, coefficient in polynomial.items():
                    for x, z, sign in ((i, j, 1), (j, i, -1)):
                        target = list(power)
                        target[x] += 1
                        target[z + 3] += 1
                        target = tuple(target)
                        next_poly[target] = next_poly.get(target, 0) + sign * coefficient
                polynomial = next_poly
        den = (k + 1) * math.factorial(k) * factorial_product(n)
        for power, coefficient in polynomial.items():
            if coefficient:
                x, z = power[:3], power[3:]
                w[ix[x], ix[z], col] = coefficient * math.sqrt(
                    factorial_product(x) * factorial_product(z) / den)
    return w


def lift_cases():
    cases = []
    ws = {}
    for k in range(5):
        w = epsilon_isometry(k)
        ws[k] = w
        d = len(occupations(k))
        matrix = w.reshape(d * d, d)
        norm_error = float(np.linalg.norm(matrix.conj().T @ matrix - np.eye(d)))
        cov_error = 0.
        for t in generators(k):
            cov_error = max(cov_error, float(np.linalg.norm(
                (np.kron(t, np.eye(d)) + np.kron(np.eye(d), t)) @ matrix
                + matrix @ t.T)))
        assert norm_error < 1e-12
        assert cov_error < 1e-12
        cases.append({'k': k, 'epsilon_norm_error': norm_error,
                      'epsilon_covariance_error': cov_error})
    harmonic = []
    for k, m in ((1, 1), (1, 2), (2, 1), (2, 2), (3, 2)):
        hot, cold, source = occupations(k), occupations(m), occupations(m + k)
        hi, ci = {n: i for i, n in enumerate(hot)}, {n: i for i, n in enumerate(cold)}
        split = np.zeros((len(cold), len(hot), len(source)), complex)
        for col, n in enumerate(source):
            for a in cold:
                b = tuple(n[i] - a[i] for i in range(3))
                if min(b) < 0 or b not in hi:
                    continue
                split[ci[a], hi[b], col] = math.sqrt(
                    math.factorial(m) * math.factorial(k) * factorial_product(n) /
                    (math.factorial(m + k) * factorial_product(a) * factorial_product(b)))
        iso = np.einsum('abx,fcb->facx', split, ws[k])
        matrix = iso.reshape(len(hot) * len(cold) * len(hot), len(source))
        norm_error = float(np.linalg.norm(matrix.conj().T @ matrix - np.eye(len(source))))
        hotlow, coldlow = occupations(k - 1), occupations(m - 1)
        hli, cli = {n: i for i, n in enumerate(hotlow)}, {n: i for i, n in enumerate(coldlow)}
        delta = np.zeros((len(hotlow) * len(coldlow), len(hot) * len(cold)), complex)
        for h in hot:
            for c in cold:
                for i in range(3):
                    if h[i] and c[i]:
                        hl, cl = list(h), list(c)
                        hl[i] -= 1
                        cl[i] -= 1
                        row = hli[tuple(hl)] * len(coldlow) + cli[tuple(cl)]
                        col = hi[h] * len(cold) + ci[c]
                        delta[row, col] += math.sqrt(h[i] * c[i])
        kernel_error = float(np.linalg.norm(np.kron(delta, np.eye(len(hot))) @ matrix))
        vacuum = source.index((0, 0, m + k))
        psi = iso[:, :, :, vacuum].reshape(len(hot) * len(cold), len(hot))
        rho = psi @ psi.conj().T
        target = np.zeros_like(rho)
        for h in hot:
            if h[2] == 0:
                i = hi[h] * len(cold) + ci[(0, 0, m)]
                target[i, i] = 1 / (k + 1)
        output_error = float(np.linalg.norm(rho - target))
        assert max(norm_error, kernel_error, output_error) < 1e-12
        harmonic.append({'k': k, 'm': m, 'split_lift_norm_error': norm_error,
                         'harmonic_kernel_error': kernel_error,
                         'top_fiber_output_error': output_error})
    return cases, harmonic


def warm_cases():
    records = []
    for m in range(1, 129):
        eig = [Fraction((m + 1) * (m + 2) * math.factorial(m) *
                        math.factorial(2 * m - n),
                        math.factorial(m - n) * math.factorial(2 * m + 2))
               for n in range(m + 1)]
        assert sum(Fraction(n + 1) * eig[n] for n in range(m + 1)) == 1
        z = sum(Fraction(n + 1, 2 ** n) for n in range(m + 1))
        error = sum(Fraction(n + 1) * abs(eig[n] - Fraction(1, 2 ** n) / z)
                    for n in range(m + 1)) / 2
        assert error <= Fraction(5, m)
        records.append({'m': m, 'exact_half_trace': str(error),
                        'm_times_error': float(m * error)})
    return records


def main():
    epsilon, harmonic = lift_cases()
    warm = warm_cases()
    result = {'status': 'FINITE-EVIDENCE',
              'scope': 'Five normalized SU3 epsilon maps, five complete '
                       'split/harmonic/top-fiber lifts and 128 exact warm '
                       'EB output distributions only',
              'epsilon_maps': epsilon, 'harmonic_lifts': harmonic,
              'warm_outputs': warm,
              'max_covariance_error': max(x['epsilon_covariance_error'] for x in epsilon),
              'max_harmonic_error': max(x['harmonic_kernel_error'] for x in harmonic),
              'max_m_times_warm_error': max(x['m_times_error'] for x in warm),
              'old_suites_rerun': False,
              'uniform_external_or_iid_validation': False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ('epsilon_maps', 'harmonic_lifts', 'warm_outputs')},
                     indent=2))


if __name__ == '__main__':
    main()
