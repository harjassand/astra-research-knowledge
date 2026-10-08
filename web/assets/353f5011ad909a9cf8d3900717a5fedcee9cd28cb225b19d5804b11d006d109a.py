"""Finite independent checks of the harmonic ordinary-Casimir comparator.

No Gibbs error is inferred from the ordinary energy. The order gap is
conditional on the separately unproved weighted spectral/rank lower.
Python standard library and NumPy only; no optimizers are imported.
"""
import importlib.util
import itertools
import json
import math
import pathlib
from fractions import Fraction as F

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    'regular', ROOT.parent / 'regular_su3' / 'verify_regular_su3.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


def exact_controls():
    norms = dimensions = ranges = sequences = 0
    for a in range(1, 129):
        for r in range(a + 1):
            norm = sum((s + 1) * (r + 1 - s) ** 2 for s in range(r + 1))
            energy = sum((s + 1) * (s + 2) * (a - s) for s in range(r + 1))
            assert norm == F((r + 1) * (r + 2) ** 2 * (r + 3), 12)
            assert F(energy, norm) == F(4 * a - 3 * r, r + 2)
            norms += 1
        for b in range(1, a + 1):
            n = a + b
            ambient = math.comb(a + 2, 2) * math.comb(b + 2, 2)
            dims = [(a - r + 1) * (b - r + 1) * (n - 2 * r + 2) // 2
                    for r in range(b + 1)]
            assert sum(dims) == ambient
            eig = [r * (n + 2 - r) for r in range(b + 1)]
            assert eig[1] == n + 1
            assert all(x < y for x, y in zip(eig, eig[1:]))
            dimensions += 1
            max_q = min(math.comb(a + 2, 2), (n + 1) ** 2 // (8 * b * b))
            for q in set([1, 2, 3, max_q, max(1, max_q // 2)]):
                if q > max_q:
                    continue
                r = math.isqrt(2 * q)
                while (r + 1) * (r + 2) // 2 > q:
                    r -= 1
                assert r <= a and 2 * b * r <= n + 1
                assert q < (r + 2) ** 2
                epsilon = F(b * r, n + 1)
                bound = (F(4 * a - 3 * r, r + 2) + 2 * b) / (1 - epsilon) ** 2
                assert bound <= F(16 * a, r + 2) + 8 * b
                ranges += 1
    for b in range(256, 4097, 16):
        a, q = b * b, b + 1
        n = a + b
        assert q <= (n + 1) ** 2 // (8 * b * b)
        assert a >= 8 * (b + 1)
        assert q <= (a + 1) * (b + 1) * (n + 2) // 4
        # The b/N^2 term in (4.4) is <=1/(N sqrt b).
        assert b ** 3 <= n * n
        sequences += 1
    return dict(exact_taper_norms_and_energies=norms,
                exact_fischer_dimensions_and_gaps=dimensions,
                exact_admitted_Q_ranges=ranges,
                exact_conditional_sequence_ranges=sequences)


def residual(value, expected, tolerance=1e-8):
    error = float(np.max(np.abs(np.asarray(value) - np.asarray(expected))))
    scale = max(1., float(np.max(np.abs(np.asarray(expected)))))
    if error / scale > tolerance:
        raise AssertionError((error, scale))
    return error / scale


def matrix_case(a, b):
    left = list(c.old.occupations(a, 3))
    right = list(c.old.occupations(b, 3))
    lower = list(itertools.product(c.old.occupations(a - 1, 3),
                                   c.old.occupations(b - 1, 3)))
    index = {pair: i for i, pair in enumerate(lower)}
    ambient = len(left) * len(right)
    contraction = np.zeros((len(lower), ambient), complex)
    pairs = list(itertools.product(left, right))
    for col, (alpha, beta) in enumerate(pairs):
        for j in range(3):
            if alpha[j] and beta[j]:
                u, v = list(alpha), list(beta)
                u[j] -= 1
                v[j] -= 1
                contraction[index[(tuple(u), tuple(v))], col] += math.sqrt(alpha[j] * beta[j])
    _, singular, vh = np.linalg.svd(contraction, full_matrices=True)
    rank = int(np.count_nonzero(singular > 1e-10))
    basis = vh[rank:].conj().T
    projection = basis @ basis.conj().T
    n = a + b
    dimension = (a + 1) * (b + 1) * (n + 2) // 2
    assert basis.shape == (ambient, dimension)
    expected_spectrum = []
    for r in range(b + 1):
        multiplicity = (a - r + 1) * (b - r + 1) * (n - 2 * r + 2) // 2
        expected_spectrum.extend([r * (n + 2 - r)] * multiplicity)
    square = contraction.conj().T @ contraction
    checks = [residual(np.linalg.eigvalsh(square), expected_spectrum)]
    full_ts = [np.kron(c.old.lift(t, left), np.eye(len(right)))
               - np.kron(np.eye(len(left)), c.old.lift(t, right).T)
               for t in c.fundamental]
    ts = [basis.conj().T @ t @ basis for t in full_ts]
    for t in full_ts:
        checks.append(residual(t @ projection, projection @ t))
    controls = []
    for r in range(min(a, (n + 1) // (2 * b)) + 1):
        support = [i for i, (alpha, beta) in enumerate(pairs)
                   if a - alpha[0] <= r and beta == (0, 0, b)]
        support_square = square[np.ix_(support, support)]
        checks.append(residual(support_square,
                               np.diag([b * pairs[i][0][2] for i in support])))
        overlap = projection[np.ix_(support, support)]
        epsilon = b * r / (n + 1)
        assert np.linalg.eigvalsh(overlap).min() >= 1 - epsilon - 1e-8
        values = np.array([max(0, r + 1 - (a - alpha[0]))
                           if beta == (0, 0, b) else 0 for alpha, beta in pairs], float)
        ambient_filter = np.diag(values)
        compressed = basis.conj().T @ ambient_filter @ basis
        ambient_norm = float(np.linalg.norm(ambient_filter) ** 2)
        compressed_norm = float(np.linalg.norm(compressed) ** 2)
        ambient_energy = c.old.energy(ambient_filter, full_ts)
        compressed_energy = c.old.energy(compressed, ts)
        exact_ratio = (4 * a - 3 * r) / (r + 2) + 2 * b
        checks.append(residual(ambient_energy / ambient_norm, exact_ratio))
        assert compressed_norm >= (1 - epsilon) ** 2 * ambient_norm - 1e-8
        assert compressed_energy <= ambient_energy + 1e-7
        exact_rank = (r + 1) * (r + 2) // 2
        assert np.linalg.matrix_rank(compressed, tol=1e-8) == exact_rank
        assert np.linalg.eigvalsh(compressed).min() >= -1e-8
        upper = exact_ratio / (1 - epsilon) ** 2
        assert compressed_energy / compressed_norm <= upper + 1e-7
        controls.append(dict(R=r, rank=exact_rank, epsilon=epsilon,
                             overlap_min=float(np.linalg.eigvalsh(overlap).min()),
                             norm_ratio=compressed_norm / ambient_norm,
                             E_T_over_norm=compressed_energy / compressed_norm,
                             proved_upper=upper))
    return dict(a=a, b=b, N=n, dimension=dimension, ambient_dimension=ambient,
                controls=controls, max_relative_residual=max(checks))


def main():
    exact = exact_controls()
    cases = [matrix_case(a, b) for a, b in [(1, 1), (2, 1), (3, 1), (4, 1),
             (6, 1), (3, 2), (4, 2), (5, 3), (8, 2), (12, 1)]]
    result = dict(status='FINITE-EVIDENCE', proof_validation=False,
                  theorem_file='HARMONIC_CASIMIR_COMPARATOR.txt',
                  Gibbs_error_from_Casimir='NOT-INFERRED',
                  operational_order_gap='CONDITIONAL-UNPROVED-WEIGHTED-LOWER',
                  exact_checks=exact, matrix_cases=cases,
                  max_relative_residual=max(t['max_relative_residual'] for t in cases),
                  dependencies=['Python standard library', 'NumPy'])
    (ROOT / 'HARMONIC_CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status='passed', matrix_cases=len(cases), **exact,
                         max_relative_residual=result['max_relative_residual'],
                         operational_order_gap=result['operational_order_gap'])))


if __name__ == '__main__':
    main()
