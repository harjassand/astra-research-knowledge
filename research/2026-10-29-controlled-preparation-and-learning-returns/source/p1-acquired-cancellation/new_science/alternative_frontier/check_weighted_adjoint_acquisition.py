#!/usr/bin/env python3
"""Independent exact protocol check; synthetic native matrices, no physical samples.

The tested record is assembled chronologically from forward pulses and observed
endpoint weights. Hidden feature values are used only as verification targets.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import numpy as np


def mat(rows):
    return np.array([[F(v) for v in row] for row in rows], dtype=object)


def eye(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def inv(a):
    n = len(a)
    b = np.concatenate([a.copy(), eye(n)], axis=1)
    for i in range(n):
        p = next(j for j in range(i, n) if b[j, i])
        b[[i, p]] = b[[p, i]]
        b[i] = b[i] / b[i, i]
        for j in range(n):
            if i != j:
                b[j] = b[j] - b[j, i] * b[i]
    return b[:, n:]


def zero(a):
    return all(v == 0 for v in a.flat)


def tilt(q, h):
    a = q.copy()
    for i in range(len(q)):
        for j in range(len(q)):
            if i != j:
                a[i, j] = q[i, j] * h[j] / h[i]
        a[i, i] = -sum(a[i, j] for j in range(len(q)) if i != j)
    return a


n = 5
one = mat([[1] for _ in range(n)])
pi = mat([[F(j, 15) for j in range(1, n + 1)]])
dpi = np.diag(pi[0])
labels = [0, 0, 1, 1, 2]
edges = mat([[0, 2, 3, 5, 7], [2, 0, 11, 13, 17],
             [3, 11, 0, 19, 23], [5, 13, 19, 0, 29],
             [7, 17, 23, 29, 0]]) / F(100)
q = inv(dpi) @ edges
for i in range(n):
    q[i, i] = -sum(q[i, j] for j in range(n) if i != j)
assert zero(dpi @ q - q.T @ dpi) and zero(q @ one)
lam = max(-q[i, i] for i in range(n))
alpha = 4 * lam
es = [np.diag([F(int(a == b)) for a in labels]) for b in range(3)]
hs = [[F(1)] * n] + [[F(1 + int(a == b)) for a in labels] for b in range(2)]
ss = [alpha * inv(alpha * eye(n) - tilt(q, h)) for h in hs]


def operator(word):
    a = eye(n)
    for kind, j in word:
        a = a @ (es[j] if kind == 'label' else ss[j])
    return a


def adjoint_protocol(word, include_endpoint_weights=True):
    """Reverse order, but execute every pulse forward with visible weights."""
    a = eye(n)
    for kind, j in reversed(word):
        if kind == 'label':
            a = a @ es[j]
        elif include_endpoint_weights:
            start_weight = np.diag([v * v for v in hs[j]])
            end_weight = np.diag([1 / (v * v) for v in hs[j]])
            a = a @ start_weight @ ss[j] @ end_weight
        else:
            a = a @ ss[j]
    return a


words = [[('label', b)] for b in range(3)] + [
    [('label', 0), ('pulse', 1), ('label', 1), ('pulse', 2), ('label', 2)],
    [('label', 1), ('pulse', 2), ('label', 0), ('pulse', 1), ('label', 2)],
]
ops = [operator(w) for w in words]
features = np.column_stack([o @ one for o in ops])
assert zero(features @ inv(features) - eye(n))
adjoints = [adjoint_protocol(w) for w in words]
for a, o in zip(adjoints, ops):
    assert zero(dpi @ a - o.T @ dpi)

records = []
for h, s in zip(hs, ss):
    center_weight = np.diag([v * v for v in h])
    acquired = []
    transition = eye(n)
    for pulse_count in range(3):
        # A single stationary chronological trajectory: adjoint word,
        # center weight, zero/one/two pulse clocks, then forward future word.
        measured = mat([[(pi @ ai @ center_weight @ transition @ oj @ one)[0, 0]
                         for oj in ops] for ai in adjoints])
        native_target = features.T @ dpi @ center_weight @ transition @ features
        assert zero(measured - native_target)
        acquired.append(measured)
        transition = transition @ s
    g, k, d = acquired
    assert zero(d - k @ inv(g) @ k)
    c = inv(g) @ k
    reduced_q = alpha * (eye(n) - inv(c))
    assert zero(tilt(q, h) @ features - features @ reduced_q)
    records.append((g, reduced_q))

# Removing endpoint weights is a genuine failure, not a harmless convention.
unweighted = [adjoint_protocol(w, False) for w in words]
wrong_gram = mat([[(pi @ ai @ oj @ one)[0, 0] for oj in ops] for ai in unweighted])
assert not zero(wrong_gram - records[0][0])

g0, l0 = records[0]
projectors = [inv(g0) @ features.T @ dpi @ e @ features for e in es]
ws = []
for b in range(2):
    hb = eye(n) + projectors[b]
    ws.append(l0 @ hb - hb @ records[b + 1][1])
ws.append(-ws[0] - ws[1])
new_biases = [[F(3, 2), F(5, 4), F(7, 3)], [F(4), F(1), F(2)],
              [F(1), F(3), F(5)]]
for values in new_biases:
    hh = sum((v * p for v, p in zip(values, projectors)), np.zeros((n, n), dtype=object))
    forcing = sum((v * w for v, w in zip(values, ws)), np.zeros((n, n), dtype=object))
    reduced = inv(hh) @ (l0 @ hh - forcing)
    native_h = [values[a] for a in labels]
    assert zero(tilt(q, native_h) @ features - features @ reduced)

result = {
    'result': 'PASS',
    'scope': 'Exact rational synthetic review checks; no native observations or finite-data claim.',
    'stationary_distribution': [str(v) for v in pi[0]],
    'labels': labels,
    'exit_ceiling': str(lam),
    'pulse_clock_rate': str(alpha),
    'controlled_features': 5,
    'exact_chronological_moment_matrices_checked': 9,
    'endpoint_weights_are_necessary_in_fixture': True,
    'all_bias_completion_checked_for_label_count': 3,
    'additional_biases': [[str(v) for v in row] for row in new_biases],
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
path = Path(__file__).with_name('WEIGHTED_ADJOINT_ACQUISITION_REVIEW_RESULTS.json')
path.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
