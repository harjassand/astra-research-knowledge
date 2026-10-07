"""Exact finite-field diagnostics for the derived q-shift detector.

The oracle is simulated from a hidden realization. It returns a lossless
structured subvector of the full detector output, not a dense matrix trace.
Every arithmetic operation is in F_p. All-word equivalence is checked by an
independent reachable-space calculation on the difference realization.
"""
from __future__ import annotations

import itertools
import json
import time
from pathlib import Path

import numpy as np


def poly_mul(a, b, p, e):
    return np.convolve(a, b)[:e] % p


def build_u(p, n, m):
    n_z = 2 * n * m
    e_t = 1 + n_z * (n_z - 1) // 2 + n * (n_z - 1)
    u = []
    for letter in range(1, n + 1):
        a = np.zeros((n_z, n_z, e_t), dtype=np.int64)
        for row in range(n_z):
            for col in range(row):
                exp = letter * (row - col - 1)
                num = np.zeros(e_t, dtype=np.int64)
                num[0] = 1
                for _ in range(exp):
                    num[1:] = (num[1:] + num[:-1]) % p
                inv = np.zeros(e_t, dtype=np.int64)
                inv[::row] = p - 1
                a[row, col] = poly_mul(num, inv, p, e_t)
        u.append(a)
    return u, n_z, e_t


def lower_poly_matmul(a, b, p):
    n_z, _, e_t = a.shape
    c = np.zeros_like(a)
    for row in range(n_z):
        for col in range(row + 1):
            v = c[row, col]
            for mid in range(col, row + 1):
                if a[row, mid].any() and b[mid, col].any():
                    v[:] = (v + poly_mul(a[row, mid], b[mid, col], p, e_t)) % p
    return c


def word_images(u, m, p):
    n_z, _, e_t = u[0].shape
    ident = np.zeros((n_z, n_z, e_t), dtype=np.int64)
    ident[np.arange(n_z), np.arange(n_z), 0] = 1
    images = {(): ident}
    for length in range(1, m):
        for word in itertools.product(range(len(u)), repeat=length):
            images[word] = lower_poly_matmul(images[word[:-1]], u[word[-1]], p)
    return images


def coefficient(alpha, transitions, beta, word, p):
    row = alpha.copy()
    for letter in word:
        row = row @ transitions[letter] % p
    return int(row @ beta % p)


def row_basis(rows, p):
    """Reduced row basis and pivot positions, all in F_p."""
    echelon = []
    pivots = []
    for row in rows:
        v = np.array(row, dtype=np.int64, copy=True) % p
        for b, pivot in zip(echelon, pivots):
            v = (v - int(v[pivot]) * b) % p
        nz = np.flatnonzero(v)
        if not len(nz):
            continue
        pivot = int(nz[0])
        v = v * pow(int(v[pivot]), -1, p) % p
        for j, b in enumerate(echelon):
            echelon[j] = (b - int(b[pivot]) * v) % p
        at = sum(q < pivot for q in pivots)
        pivots.insert(at, pivot)
        echelon.insert(at, v)
    return echelon, pivots


def span_coordinates(basis, row, p):
    """Solve x*basis=row, returning None if row is independent."""
    if not basis:
        return np.zeros(0, dtype=np.int64) if not np.any(row) else None
    reduced, pivots = row_basis(basis, p)
    if len(reduced) != len(basis):
        raise AssertionError("dependent stored basis")
    if len(row_basis([*basis, row], p)[0]) > len(basis):
        return None
    square = np.array(basis, dtype=np.int64)[:, pivots].T % p
    rhs = np.array(row, dtype=np.int64)[pivots] % p
    aug = np.column_stack((square, rhs))
    r = len(basis)
    for col in range(r):
        pivot = next(j for j in range(col, r) if aug[j, col])
        aug[[col, pivot]] = aug[[pivot, col]]
        aug[col] = aug[col] * pow(int(aug[col, col]), -1, p) % p
        for j in range(r):
            if j != col:
                aug[j] = (aug[j] - int(aug[j, col]) * aug[col]) % p
    ans = aug[:, -1]
    assert np.array_equal(ans @ np.array(basis) % p, row % p)
    return ans


def structured_oracle(alpha, transitions, beta, images, m, p):
    shape = next(iter(images.values())).shape
    calls = []

    def query(prefix):
        calls.append(tuple(prefix))
        coeffs = np.zeros((m, *shape), dtype=np.int64)
        for word, image in images.items():
            value = coefficient(alpha, transitions, beta, (*prefix, *word), p)
            coeffs[len(word)] = (coeffs[len(word)] + value * image) % p
        return coeffs.reshape(-1), coefficient(alpha, transitions, beta, prefix, p)

    return query, calls


def learn(query, n, p):
    first, empty_value = query(())
    if not first.any():
        return np.zeros(0, dtype=np.int64), [np.zeros((0, 0), dtype=np.int64) for _ in range(n)], np.zeros(0, dtype=np.int64), 0
    prefixes = [()]
    features = [first]
    finals = [empty_value]
    cached = {(): first}
    at = 0
    while at < len(prefixes):
        prefix = prefixes[at]
        for letter in range(n):
            word = (*prefix, letter)
            feature, empty = query(word)
            cached[word] = feature
            if span_coordinates(features, feature, p) is None:
                prefixes.append(word)
                features.append(feature)
                finals.append(empty)
        at += 1
    r = len(prefixes)
    transitions = [np.zeros((r, r), dtype=np.int64) for _ in range(n)]
    for row, prefix in enumerate(prefixes):
        for letter in range(n):
            coord = span_coordinates(features, cached[(*prefix, letter)], p)
            assert coord is not None
            transitions[letter][row] = coord
    alpha = np.zeros(r, dtype=np.int64)
    alpha[0] = 1
    return alpha, transitions, np.array(finals, dtype=np.int64), r


def all_word_zero(alpha, transitions, beta, p):
    basis, _ = row_basis([alpha], p)
    at = 0
    while at < len(basis):
        assert int(basis[at] @ beta % p) == 0
        for matrix in transitions:
            new = basis[at] @ matrix % p
            if span_coordinates(basis, new, p) is None:
                basis.append(new)
        at += 1
    return len(basis)


def certify_equal(original, learned, p):
    a, b, v = original
    c, d, w, _ = learned
    alpha = np.concatenate((a, (-c) % p))
    beta = np.concatenate((v, w))
    transitions = []
    for x, y in zip(b, d):
        z = np.zeros((len(a) + len(c), len(a) + len(c)), dtype=np.int64)
        z[:len(a), :len(a)] = x
        z[len(a):, len(a):] = y
        transitions.append(z)
    return all_word_zero(alpha, transitions, beta, p)


def hankel_rank(original, p):
    alpha, transitions, beta = original
    m = len(alpha)
    words = [w for k in range(m) for w in itertools.product(range(len(transitions)), repeat=k)]
    hankel = np.array([[coefficient(alpha, transitions, beta, (*a, *b), p) for b in words] for a in words], dtype=np.int64)
    return len(row_basis(hankel, p)[0])


def evaluate_fixture(original, p, name):
    alpha, transitions, beta = original
    m = len(alpha)
    n = len(transitions)
    u, n_z, e_t = build_u(p, n, m)
    images = word_images(u, m, p)
    query, calls = structured_oracle(alpha, transitions, beta, images, m, p)
    learned = learn(query, n, p)
    certified_dimension = certify_equal((alpha, transitions, beta), learned, p)
    independent_rank = hankel_rank((alpha, transitions, beta), p)
    assert independent_rank == learned[-1]
    d = m * n_z * e_t
    query_dims = [d * (len(prefix) + 1) for prefix in calls]
    return {
        'p': p, 'promised_states': m, 'name': name,
        'N': n_z, 'E': e_t, 'prime_field_detector_dimension': d,
        'learned_minimal_states': learned[-1], 'independent_hankel_rank': independent_rank,
        'all_word_difference_reachable_dimension': certified_dimension,
        'structured_oracle_calls': len(calls),
        'maximum_corresponding_dense_query_dimension': max(query_dims),
        'nominal_dense_response_field_entries': sum(x*x for x in query_dims),
        'computed_feature_field_entries_per_query': m * n_z * n_z * e_t,
        'dense_oracle_trace_materialized': False,
    }


def fixture(p, m, seed, zero=False):
    n = 2
    rng = np.random.default_rng(seed)
    alpha = rng.integers(0, p, size=m, dtype=np.int64)
    beta = rng.integers(0, p, size=m, dtype=np.int64)
    transitions = [rng.integers(0, p, size=(m, m), dtype=np.int64) for _ in range(n)]
    if zero:
        beta[:] = 0
    return evaluate_fixture((alpha, transitions, beta), p, f'random_{seed}' + ('_zero' if zero else ''))


def polynomial_fixture(p, terms, name):
    """Trie automaton realizing the exact specified polynomial."""
    prefixes = [()]
    for word, _ in terms:
        for j in range(1, len(word) + 1):
            if word[:j] not in prefixes:
                prefixes.append(word[:j])
    at = {word: j for j, word in enumerate(prefixes)}
    m = len(prefixes)
    alpha = np.zeros(m, dtype=np.int64)
    alpha[0] = 1
    beta = np.zeros(m, dtype=np.int64)
    transitions = [np.zeros((m, m), dtype=np.int64) for _ in range(2)]
    for word in prefixes[1:]:
        transitions[word[-1]][at[word[:-1]], at[word]] = 1
    for word, coefficient_value in terms:
        beta[at[word]] = (beta[at[word]] + coefficient_value) % p
    return evaluate_fixture((alpha, transitions, beta), p, name)


def main():
    start = time.perf_counter()
    tests = [fixture(p, m, seed) for p, m, seed in [(2, 2, 8), (2, 3, 31), (3, 3, 2), (5, 3, 71)]]
    tests.append(fixture(2, 3, 31, zero=True))
    tests.append(polynomial_fixture(2, [((0,), -1), ((0, 0), 1)], 'finite_field_scalar_grade_counterexample'))
    tests.append(polynomial_fixture(2, [((1, 0, 1), 1)], 'last_permitted_word_grade'))
    tests.append(polynomial_fixture(2, [((0, 1), 1), ((1, 0), -1)], 'commutator_characteristic_two'))
    cancel_alpha = np.array([1, 1], dtype=np.int64)
    cancel_beta = np.array([1, 1], dtype=np.int64)
    cancel_transitions = [np.eye(2, dtype=np.int64), np.zeros((2, 2), dtype=np.int64)]
    tests.append(evaluate_fixture((cancel_alpha, cancel_transitions, cancel_beta), 2, 'nonminimal_cancelling_zero'))
    result = {
        'status': 'all scoped exact checks passed',
        'scope': 'structured finite-field detector and learner simulation; independent all-word equality and Hankel rank certificates; no acquired external oracle or dense trace',
        'wall_seconds': time.perf_counter() - start,
        'fixtures': tests,
    }
    path = Path(__file__).with_name('verification.json')
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
