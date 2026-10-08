"""Small deterministic checks, not proof validation or optimality evidence.

Uses NumPy only. Run with the bundled Codex Python. The exact theorem is in
RESULT.txt; this catches normalization, root-edge and posterior-score errors.
"""
import itertools
import json
import math
import pathlib
from fractions import Fraction

import numpy as np


def occupations(n, m):
    if m == 1:
        yield (n,)
    else:
        for k in range(n, -1, -1):
            for tail in occupations(n - k, m - 1):
                yield (k,) + tail


def generators(m):
    result = []
    for i in range(m):
        for j in range(i + 1, m):
            x = np.zeros((m, m), complex)
            x[i, j] = x[j, i] = 0.5
            result.append(x)
            y = np.zeros((m, m), complex)
            y[i, j], y[j, i] = -0.5j, 0.5j
            result.append(y)
    for k in range(1, m):
        z = np.zeros((m, m), complex)
        for i in range(k):
            z[i, i] = 1
        z[k, k] = -k
        result.append(z / math.sqrt(2 * k * (k + 1)))
    return result


def lift(x, basis):
    m = x.shape[0]
    index = {beta: j for j, beta in enumerate(basis)}
    result = np.zeros((len(basis), len(basis)), complex)
    for col, beta in enumerate(basis):
        for i in range(m):
            result[col, col] += x[i, i] * beta[i]
            for j in range(m):
                if i != j and beta[j]:
                    gamma = list(beta)
                    gamma[i] += 1
                    gamma[j] -= 1
                    result[index[tuple(gamma)], col] += (
                        x[i, j] * math.sqrt((beta[i] + 1) * beta[j])
                    )
    return result


def beta_rule(q, a):
    """Gauss rule for normalized (a+1)(1-u)^a du on [0,1]."""
    diagonal = []
    for k in range(q):
        den = (2 * k + a) * (2 * k + a + 2)
        diagonal.append(-a * a / den if den else 0.0)
    matrix = np.diag(diagonal)
    for k in range(1, q):
        off = math.sqrt(
            4 * k * k * (k + a) ** 2 /
            ((2 * k + a) ** 2 * ((2 * k + a) ** 2 - 1))
        )
        matrix[k - 1, k] = matrix[k, k - 1] = off
    nodes, vectors = np.linalg.eigh(matrix)
    return (nodes + 1) / 2, vectors[0, :] ** 2


def projective_rule(n, m):
    s, q, ell = m - 1, n + 1, 2 * n + 1
    rules = [beta_rule(q, m - j - 2) for j in range(s)]
    for node_indices in itertools.product(range(q), repeat=s):
        residual, p, weight = 1.0, [], 1.0
        for j, index in enumerate(node_indices):
            u = rules[j][0][index]
            p.append(residual * u)
            residual *= 1 - u
            weight *= rules[j][1][index]
        p.append(residual)
        for phase_indices in itertools.product(range(ell), repeat=s):
            phases = np.array([0.0] + [2 * math.pi * k / ell for k in phase_indices])
            yield np.sqrt(p) * np.exp(1j * phases), weight / ell ** s


def energy(x, ts):
    return float(sum(np.linalg.norm(t @ x - x @ t) ** 2 for t in ts))


def thermal(b, h):
    vals, vecs = np.linalg.eigh(b)
    weights = np.exp(h * vals)
    return (vecs * (weights / weights.sum())) @ vecs.conj().T


def checked_close(observed, expected, atol=3e-10):
    residual = float(np.max(np.abs(observed - expected)))
    if residual > atol:
        raise AssertionError((residual, observed, expected))
    return residual


def arithmetic_controls():
    count = 0
    for m in range(2, 7):
        s = m - 1
        for n in range(1, 18):
            dim = math.comb(n + s, s)
            occ = list(occupations(n, m))
            mean = Fraction(sum(beta[0] for beta in occ), dim)
            var = sum((Fraction(beta[0], n) - Fraction(1, m)) ** 2 for beta in occ) / dim
            assert mean == Fraction(n, m)
            assert var == Fraction(s * (n + m), m * m * (m + 1) * n)
            for r in range(n):
                z = sum(math.comb(k + s - 1, s - 1) * (r + 1 - k) ** 2
                        for k in range(r + 1))
                w = sum((n - k) * (k + s) * math.comb(k + s - 1, s - 1)
                        for k in range(r + 1))
                assert z == math.comb(r + s + 2, s + 2) + math.comb(r + s + 1, s + 2)
                assert w == n * s * math.comb(r + s + 1, s + 1) - s * (s + 1) * math.comb(r + s + 1, s + 2)
                count += 1
    return count


def matrix_control(n, m, h):
    basis = list(occupations(n, m))
    dim, s = len(basis), m - 1
    fundamental = generators(m)
    ts = [lift(t, basis) for t in fundamental]
    casimir = n * s * (n + m) / (2 * m)
    residuals = {}
    residuals['casimir'] = checked_close(sum(t @ t for t in ts), casimir * np.eye(dim))
    trace_index = dim * n * (n + m) / (2 * m * (m + 1))
    residuals['trace_index'] = checked_close(
        np.array([[np.trace(t @ u) for u in ts] for t in ts]),
        trace_index * np.eye(m * m - 1))
    b = np.diag([beta[0] / n for beta in basis]).astype(complex)
    tau = thermal(b, h)
    mu = float(np.trace(tau @ b).real) * n
    r_n = (m * mu - n) / s
    assert r_n / n >= h * math.exp(-2 * h) / (m * (m + 1)) - 1e-12
    rng = np.random.default_rng(20261008 + 10 * n + m)
    positivity_gaps = []
    positivity_residuals = []
    for _ in range(10):
        rank = min(2, dim)
        u, _ = np.linalg.qr(rng.normal(size=(dim, rank)) + 1j * rng.normal(size=(dim, rank)))
        v, _ = np.linalg.qr(rng.normal(size=(dim, rank)) + 1j * rng.normal(size=(dim, rank)))
        singular = np.arange(1, rank + 1, dtype=float)
        a = (u * singular) @ v.conj().T
        left = (u * singular) @ u.conj().T
        right = (v * singular) @ v.conj().T
        gap = energy(a, ts) - (energy(left, ts) + energy(right, ts)) / 2
        exact_gap = sum(float(np.sum(singular[:, None] * singular[None, :] *
                           np.abs(u.conj().T @ t @ u - v.conj().T @ t @ v) ** 2))
                        for t in ts)
        positivity_residuals.append(abs(gap - exact_gap))
        assert gap >= -1e-10
        assert abs(np.linalg.norm(a) - np.linalg.norm(left)) < 1e-12
        assert abs(np.linalg.norm(a) - np.linalg.norm(right)) < 1e-12
        positivity_gaps.append(gap)
    residuals['positivity_identity'] = max(positivity_residuals)
    r = min(1, n - 1)
    f = np.diag([max(0, r + 1 - (n - beta[0])) for beta in basis]).astype(complex)
    z = float(np.trace(f @ f).real)
    e = energy(f, ts)
    expected_w = sum((n - k) * (k + s) * math.comb(k + s - 1, s - 1)
                     for k in range(r + 1))
    residuals['taper_energy'] = abs(e - expected_w)
    hole = np.eye(dim, dtype=complex)
    hole[0, 0] = 0
    residuals['near_full_energy'] = abs(energy(hole, ts) - n * s)

    first_moments = [np.zeros((dim, dim), complex) for _ in ts]
    avg_tau = np.zeros((dim, dim), complex)
    phi_tau = np.zeros((dim, dim), complex)
    completeness = np.zeros((dim, dim), complex)
    d_ts = [np.zeros((dim, dim), complex) for _ in ts]
    comm_b_square, labels, sum_weights = 0.0, 0, 0.0
    for v, weight in projective_rule(n, m):
        p = np.outer(v, v.conj())
        b_v = lift(p, basis) / n
        vals, vecs = np.linalg.eigh(b_v)
        k = np.rint(n * vals).astype(int)
        f_vals = np.maximum(0, r + 1 - (n - k))
        f_v = (vecs * f_vals) @ vecs.conj().T
        tau_v = thermal(b_v, h)
        avg_tau += weight * tau_v
        for a, t in enumerate(fundamental):
            first_moments[a] += weight * float(np.trace(t @ p).real) * tau_v
        phi_tau += weight * dim / z * f_v @ tau @ f_v
        completeness += weight * dim / z * f_v @ f_v
        comm_b_square += weight * np.linalg.norm(f_v @ b - b @ f_v) ** 2
        f2 = f_v @ f_v
        for a, t in enumerate(ts):
            d_ts[a] += weight * (f2 @ t + t @ f2 - 2 * f_v @ t @ f_v)
        labels += 1
        sum_weights += weight
    residuals['weights'] = abs(sum_weights - 1)
    residuals['average_tau'] = checked_close(avg_tau, np.eye(dim) / dim)
    residuals['first_harmonic'] = max(
        checked_close(first_moments[a], r_n * t / (dim * n * (n + m)))
        for a, t in enumerate(ts))
    residuals['instrument_TP'] = checked_close(completeness, np.eye(dim))
    residuals['adjoint_doublecomm'] = max(
        checked_close(d_ts[a], e * t / (dim * casimir)) for a, t in enumerate(ts))
    residuals['commutator_variance'] = abs(comm_b_square - 2 * e / (m * (m + 1) * n * n))
    observed_deficit = float(np.trace(b @ (tau - phi_tau)).real)
    expected_deficit = r_n * (e / z) / (n * n * (n + m))
    residuals['exact_score'] = abs(observed_deficit - expected_deficit)
    error = float(np.abs(np.linalg.eigvalsh((phi_tau - tau + (phi_tau - tau).conj().T) / 2)).sum() / 2)
    upper = (e / z) * math.exp(h) / 4 * (
        h / casimir + 2 * h * h / (m * (m + 1) * n * n))
    assert error + 1e-10 >= observed_deficit
    assert error <= upper + 1e-10
    assert labels == ((n + 1) * (2 * n + 1)) ** s
    assert max(residuals.values()) < 3e-10
    return dict(m=m, N=n, h=h, dimension=dim, labels=labels,
                quantum_rank=int(np.count_nonzero(np.diag(f))),
                score_deficit=observed_deficit, full_trace_error=error,
                rigorous_upper_bound=upper, positivity_samples=len(positivity_gaps),
                min_two_modulus_energy_gap=min(positivity_gaps), residuals=residuals)


def main():
    records = [matrix_control(n, m, h) for n, m, h in
               [(1, 2, .8), (3, 2, 1.7), (1, 3, .6),
                (2, 3, 1.2), (3, 3, 2.0), (1, 4, 1.1)]]
    result = dict(status='FINITE-EVIDENCE', proof_validation=False,
                  exact_arithmetic_controls=arithmetic_controls(),
                  deterministic_matrix_controls=records,
                  two_modulus_controls=sum(r['positivity_samples'] for r in records),
                  max_residual=max(max(r['residuals'].values()) for r in records),
                  dependencies=['Python standard library', 'NumPy'],
                  theorem_file='RESULT.txt')
    path = pathlib.Path(__file__).with_name('CHECKS.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status='passed', exact_controls=result['exact_arithmetic_controls'],
                         matrix_cases=len(records), two_modulus_controls=result['two_modulus_controls'],
                         max_residual=result['max_residual'])))


if __name__ == '__main__':
    main()
