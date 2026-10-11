"""Finite exact checks for REACH.md; these do not prove its analytic theorem."""

from itertools import product
from pathlib import Path
import hashlib
import json

import numpy as np
import sympy as s


def zero_matrix(a):
    return all(s.simplify(v) == 0 for v in a)


def left(q):
    a, b, c, d = q
    return s.Matrix([[a, -b, -c, -d], [b, a, -d, c],
                     [c, d, a, -b], [d, -c, b, a]])


paulis = [s.Matrix([[0, 1], [1, 0]]),
          s.Matrix([[0, -s.I], [s.I, 0]]),
          s.Matrix([[1, 0], [0, -1]])]


def unitary(q):
    return q[0] * s.eye(2) - s.I * sum(
        (q[j + 1] * paulis[j] for j in range(3)), s.zeros(2))


def state(q):
    u = unitary(q)
    return s.eye(2).row_join(u.H / 2).col_join(
        (u / 2).row_join(s.eye(2))) / 4


def effect(q):
    u = unitary(q)
    return s.eye(2).row_join(u.H).col_join(u.row_join(s.eye(2))) / 2


def qutrit_coherence(q):
    psi = unitary(q)[:, 0]
    return s.zeros(1).row_join(psi.H).col_join(psi.row_join(s.zeros(2)))


def qutrit_state(q):
    return s.eye(3) / 3 + qutrit_coherence(q) / 4


def qutrit_effect(q):
    return s.eye(3) / 2 + qutrit_coherence(q) / 2


n = 2
alpha = 1 - s.Rational(3, 2 * n * n)
vertices = []
for a in product(range(-n, n + 1), repeat=3):
    square = sum(v * v for v in a)
    v = s.Matrix([2 * n * a[0], 2 * n * a[1], 2 * n * a[2],
                  n * n - square]) / (n * n + square)
    vertices.extend([v, -v])
assert all(s.simplify(v.dot(v) - 1) == 0 for v in vertices)

e = [s.eye(4)[:, j] for j in range(4)]
gx = s.Matrix([2, 1, 0, 0]) / s.sqrt(5)
gz = s.Matrix([2, 0, 0, 1]) / s.sqrt(5)
gate_quaternions = [e[0], gx, gz, left(gz) * gx]
preps = e + [-v for v in e] + [vertices[40]]
queries = [e[0], e[2], vertices[80]]

prefix_checks = 0
for q in e + [-v for v in e]:
    controlled = s.diag(s.eye(2), unitary(q))
    assert zero_matrix(controlled * state(e[0]) * controlled.H - state(q))
    prefix_checks += 1

physical_checks = 0
for q in preps:
    rho = state(q)
    assert s.simplify(s.trace(rho) - 1) == 0
    # (4 rho - I)^2 = delta^2 I certifies the stated two eigenvalues.
    assert zero_matrix((4 * rho - s.eye(4)) ** 2 - s.eye(4) / 4)
    for g in gate_quaternions:
        assert zero_matrix(unitary(left(g) * q) - unitary(g) * unitary(q))
        controlled = s.diag(s.eye(2), unitary(g))
        assert zero_matrix(controlled * rho * controlled.H - state(left(g) * q))
        for u in queries:
            measurement = effect(u)
            assert zero_matrix(measurement * measurement - measurement)
            born = s.trace(measurement * state(left(g) * q))
            expected = (1 + (u.dot(left(g) * q)) / 2) / 2
            assert s.simplify(born - expected) == 0
            physical_checks += 1

qutrit_checks = 0
for q in preps:
    coherence = qutrit_coherence(q)
    assert zero_matrix(coherence ** 3 - coherence)
    assert s.simplify(s.trace(coherence ** 2) - 2) == 0
    for g in gate_quaternions:
        gate = s.diag(1, unitary(g))
        assert zero_matrix(gate * qutrit_state(q) * gate.H - qutrit_state(left(g) * q))
        for u in queries:
            born = s.trace(qutrit_effect(u) * qutrit_state(left(g) * q))
            expected = (1 + (u.dot(left(g) * q)) / 2) / 2
            assert s.simplify(born - expected) == 0
            qutrit_checks += 1

signed_basis = e + [-v for v in e]
basis_matrix = s.Matrix.vstack(*(v.T for v in signed_basis))
probability_matrix = s.ones(8) / 2 + basis_matrix * basis_matrix.T / 4
assert probability_matrix.rank() == 5
assert zero_matrix(basis_matrix.T * basis_matrix - 2 * s.eye(4))
assert zero_matrix(basis_matrix.T * s.ones(8, 1))
assert zero_matrix(probability_matrix * basis_matrix - basis_matrix / 2)
assert zero_matrix(probability_matrix * s.ones(8, 1) - 4 * s.ones(8, 1))

# Find one simplex numerically, then verify its full certificate exactly.
q = s.Matrix([s.Rational(2, 3), s.Rational(2, 3), 0, s.Rational(1, 3)])
target = alpha * left(gx) * q
vertex_array = np.array([[float(a) for a in v] for v in vertices])
augmented = np.vstack([vertex_array.T, np.ones(len(vertices))])
target_array = np.array([float(a) for a in target] + [1.0])
rng = np.random.default_rng(20261011)
indices = None
for _ in range(100000):
    trial = rng.choice(len(vertices), size=5, replace=False)
    try:
        weights = np.linalg.solve(augmented[:, trial], target_array)
    except np.linalg.LinAlgError:
        continue
    if np.min(weights) > 1e-8:
        indices = [int(j) for j in trial]
        break
assert indices is not None
matrix = s.Matrix.hstack(*(vertices[j].col_join(s.Matrix([1])) for j in indices))
weights_exact = matrix.inv() * target.col_join(s.Matrix([1]))
weights_exact = [s.simplify(v) for v in weights_exact]
assert all(v.is_positive is True for v in weights_exact)
assert s.simplify(sum(weights_exact) - 1) == 0
row_value = sum((w * vertices[j] for j, w in zip(indices, weights_exact)), s.zeros(4, 1))
assert zero_matrix(row_value - target)

report = {
    "status": "PASS",
    "scope": "Finite symbolic identities and one exact positive row, not universal proof, gap or novelty certification",
    "rational_unit_vertices": len(vertices),
    "fixed_preparation_prefix_fixtures": prefix_checks,
    "physical_born_fixtures": physical_checks,
    "qutrit_born_fixtures": qutrit_checks,
    "two_letter_probability_matrix_rank": int(probability_matrix.rank()),
    "barycentric_row": {
        "vertex_indices": indices,
        "weights": [str(w) for w in weights_exact],
        "initial_quaternion": [str(v) for v in q],
        "target_quaternion": [str(s.simplify(v)) for v in target],
        "alpha": str(alpha),
    },
    "source_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
destination = Path(__file__).with_name("reach_diagnostics.json")
destination.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
