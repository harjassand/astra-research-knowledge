#!/usr/bin/env python3
"""Independent direct-history check of Cycle11 entropy/drift pressure.

This retains the physical vacuum seed exchange and every coherent amplitude.
There is no reflecting cutoff or resampled bath. Small matrices test the new
trace/log-compression inequalities and their noncommuting-initializer scope;
they do not certify an all-k theorem or calculate channel capacity.
"""
from itertools import product
from math import sqrt, exp, log, cosh
from pathlib import Path
import hashlib, json, resource, time
import numpy as np

ROOT = Path(__file__).resolve().parent
START = time.perf_counter()
A, B = 36 / 37, 1 / 37


def path(word, seed, stack):
    states = {((), seed, stack): 1 + 0j}
    for c in word:
        nxt = {}
        for (out, sd, st), amplitude in states.items():
            key = (out + (c,), sd, st)
            nxt[key] = nxt.get(key, 0j) + 1j * amplitude
            if c:
                key = (out + (0,), sd, (c,) + st)
            elif st:
                key = (out + (st[0],), sd, st[1:])
            else:
                key = (out + (0,), 1 - sd, ())
            nxt[key] = nxt.get(key, 0j) + 6 * amplitude
        states = nxt
    return states


def build(k, mixture):
    words = list(product(range(3), repeat=k))
    rows = {}
    for i, word in enumerate(words):
        for auxiliary, (weight, vector) in enumerate(mixture):
            for (seed, stack), coefficient in vector.items():
                for (out, sd, st), amplitude in path(word, seed, stack).items():
                    row = (out, sd, st, auxiliary)
                    if row not in rows:
                        rows[row] = np.zeros(len(words), dtype=np.complex128)
                    rows[row][i] += sqrt(weight) * coefficient * amplitude
    keys = list(rows)
    matrix = np.array([rows[row] for row in keys]) / 37 ** (k / 2)
    qout = np.array([sum(c != 0 for c in row[0]) for row in keys])
    qin = np.array([sum(c != 0 for c in w) for w in words])
    return matrix, qout, qin


def hermitian_function(matrix, function):
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2)
    return (vectors * function(values)) @ vectors.conj().T


def mixtures(k):
    one, two = (1,) * k, (2,) * k
    deep = [
        ('bulk_basis', [(1.0, {(0, one): 1.0})]),
        ('bulk_coherent_prefix', [(1.0, {(0, one): 1 / sqrt(2),
                                        (1, two): 1j / sqrt(2)})]),
    ]
    states = [(sd, word) for h in range(3) for sd in range(2)
              for word in product((1, 2), repeat=h)]
    raw = [(1 / 3) * (1 / 6) ** len(word) for sd, word in states]
    norm = sum(raw)
    arbitrary = [
        ('vacuum', [(1.0, {(0, ()): 1.0})]),
        ('coherent_depths', [(1.0, {(0, ()): 1 / sqrt(3),
                                   (0, (1,)): 1j / sqrt(3),
                                   (1, (2,) * (k + 1)): 1 / sqrt(3)})]),
        ('truncated_actual_tau_pi', [(weight / norm, {state: 1.0})
                                     for weight, state in zip(raw, states)]),
    ]
    return deep + arbitrary


observations = []
for k in (1, 2, 3):
    for name, mixture in mixtures(k):
        matrix, qout, qin = build(k, mixture)
        dim = len(qin)
        gram_error = float(np.max(np.abs(matrix.conj().T @ matrix - np.eye(dim))))
        assert gram_error < 3e-14
        M = matrix.conj().T @ (qout[:, None] * matrix)
        D = np.diag(qin) - M
        commutator = float(np.linalg.norm(qin[:, None] * M - M * qin[None, :], 2))
        tests = []
        for lam in (0.0, log(2) / 2, 1.0):
            T = matrix.conj().T @ (np.exp(lam * qout)[:, None] * matrix)
            logT = hermitian_function(T, np.log)
            jensen_min = float(np.linalg.eigvalsh(logT - lam * M)[0])
            pressure = float(np.exp(-lam * np.linalg.eigvalsh(D)).sum())
            tilted_trace = float(np.sum(np.exp(-lam * qin) * np.diag(T).real))
            bound = (3 * B + A * (exp(lam) + 2 * exp(-lam))) ** k
            assert jensen_min > -2e-13
            assert pressure <= tilted_trace + 4e-12
            assert tilted_trace <= bound + 4e-12
            tests.append({'lambda': lam, 'log_compression_min_eigenvalue': jensen_min,
                          'pressure': pressure, 'tilted_trace': tilted_trace,
                          'root_retaining_bound': bound})
        record = {'k': k, 'initializer': name, 'input_dimension': dim,
                  'output_dilation_rows': len(matrix), 'isometry_max_error': gram_error,
                  'M_Q_commutator_norm': commutator, 'pressure_tests': tests}
        if name.startswith('bulk'):
            assert commutator < 3e-13
            K = D - A * np.diag(2 * qin - k)
            sigma_diag = 2.0 ** (-k - qin)
            mgf_tests = []
            for t in (-2.0, -log(2) / (2 * A), log(2) / (2 * A), 2.0):
                actual = float(np.sum(sigma_diag * np.diag(
                    hermitian_function(-t * K, np.exp)).real))
                bound = (A * cosh(t * B) + B * cosh(t * A)) ** k
                assert actual <= bound + 4e-12
                mgf_tests.append({'t': t, 'actual_mgf': actual, 'analytic_bound': bound})
            record['bulk_weighted_mgf'] = mgf_tests
        observations.append(record)

assert max(o['M_Q_commutator_norm'] for o in observations
           if o['initializer'] == 'coherent_depths') > 0.01
beta = 1 / 32
alpha = sqrt(1 - beta * beta)
delta, g = beta / (8 * alpha), 1 / 8
one_block = np.array([[1 / 4 - delta / 2, 1j * g],
                      [-1j * g, 1 / 4 + delta / 2]])
joint = np.kron(np.eye(2), one_block)
edge_u = np.kron(np.eye(2), np.array([[0.0, 1.0], [1.0, 0.0]]))
edge_v = alpha * edge_u + 1j * beta * np.eye(4)
edge_q = np.diag([0.0, 1.0, 0.0, 1.0])
edge_drift = edge_q - edge_v.conj().T @ edge_q @ edge_v
joint_drift = float(np.trace(joint @ edge_drift).real)
marginal = np.array([1 / 2 - delta, 1 / 4 + delta / 2, 1 / 4 + delta / 2])
input_entropy = float(-np.sum(marginal * np.log2(marginal)))
ceiling = log(2 * sqrt(2) * (1 - beta * beta) + 3 * beta * beta, 2)
assert np.linalg.eigvalsh(joint)[0] > 0
assert abs(joint_drift + alpha * beta / 4) < 1e-15
assert input_entropy > ceiling and joint_drift < 0
counterexample = {'beta': beta, 'input_entropy_bits': input_entropy,
                  'independent_input_ceiling_bits': ceiling,
                  'actual_joint_drift': joint_drift,
                  'minimum_joint_eigenvalue': float(np.linalg.eigvalsh(joint)[0]),
                  'scope': 'Violates the bound only when initial input/bath independence is omitted; the stipulated channel operation excludes this correlated joint state.'}
out = {'device': '(6 U + i I)/sqrt(37), actual root exchange retained',
       'beta_squared': '1/37', 'all_checks': 'PASS', 'observations': observations,
       'necessary_independence_counterexample': counterexample,
       'wall_seconds': time.perf_counter() - START,
       'peak_rss_kib_linux': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
       'scope': 'New direct physical pressure diagnostic, not an all-k proof or capacity calculation. No old test suite was replayed. Discovery/inference cost unknown.'}
(ROOT / 'physical_pressure_check.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'all_checks': out['all_checks'], 'cases': len(observations),
                  'wall_seconds': out['wall_seconds'],
                  'max_noncommuting_MQ': max(o['M_Q_commutator_norm'] for o in observations),
                  'peak_rss_kib_linux': out['peak_rss_kib_linux']}, indent=2))
