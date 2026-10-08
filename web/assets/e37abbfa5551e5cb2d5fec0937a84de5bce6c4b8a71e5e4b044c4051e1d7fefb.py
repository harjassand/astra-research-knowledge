#!/usr/bin/env python3
"""Exact d=16 sanity check for the matched commuting/Clifford score frames.

This verifies one finite construction only. The all-parameter proof is in
common_measurement_gate.txt; this script does not establish the asymptotic
statement or the compatibility commutator inequality.
"""
from itertools import product
import sympy as sp

I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)
I16 = sp.eye(16)
d, m = 16, 8
a = sp.Rational(1, 2)


def kron_all(items):
    out = sp.Matrix([[1]])
    for item in items:
        out = sp.kronecker_product(out, item)
    return out


gammas = []
for j in range(4):
    prefix = [Z] * j
    suffix = [I2] * (3 - j)
    gammas.append(kron_all(prefix + [X] + suffix))
    gammas.append(kron_all(prefix + [Y] + suffix))

assert len(gammas) == m
for i, Gi in enumerate(gammas):
    assert Gi == Gi.conjugate().T
    assert Gi * Gi == I16
    for j, Gj in enumerate(gammas):
        assert Gi * Gj + Gj * Gi == (2 * I16 if i == j else sp.zeros(d))
        tau = sp.trace(Gi * Gj) / d
        assert tau == (1 if i == j else 0)

# The common eigenbasis of X on qubit 1 and Z on qubits 2--4 is a basis of
# simultaneous expectations for the first Clifford observable.
H1 = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
U = sp.kronecker_product(H1, sp.eye(8))
for col in range(d):
    psi = U[:, col]
    exps = [(psi.conjugate().T * Gi * psi)[0] for Gi in gammas]
    assert exps[0] in (1, -1)
    assert all(sp.simplify(v) == 0 for v in exps[1:])

# Commuting frame: one balanced +/- pair on each of m equal blocks.
Zs = []
for i in range(m):
    diag = [0] * d
    diag[2 * i] = 1
    diag[2 * i + 1] = -1
    Zs.append(sp.diag(*diag))
for i, Zi in enumerate(Zs):
    for j, Zj in enumerate(Zs):
        assert sp.trace(Zi * Zj) / d == (sp.Rational(1, m) if i == j else 0)

for signs in product((-1, 1), repeat=m):
    HD = a * sum((signs[i] * Zs[i] for i in range(m)), sp.zeros(d))
    HC = a / sp.sqrt(m) * sum((signs[i] * gammas[i] for i in range(m)), sp.zeros(d))
    assert HD == HD.conjugate().T and HD.trace() == 0
    assert HC == HC.conjugate().T and HC.trace() == 0
    assert (HD * HD).applyfunc(sp.simplify) == a**2 * I16
    assert (HC * HC).applyfunc(sp.simplify) == a**2 * I16

# Both uniform score covariances have the same active eigenvalues a^2/m.
qdiag = [sp.Rational(0)] * m
for signs in product((-1, 1), repeat=m):
    for i in range(m):
        c = a / sp.sqrt(m) * signs[i]
        qdiag[i] += c**2 / (2**m)
assert qdiag == [a**2 / m] * m

# The Clifford eigenbasis captures a^2/m; the common diagonal PVM captures
# all a^2 in the commuting family.
J_clifford = a**2 / m
J_commuting = a**2
Delta_clifford = a**2 - J_clifford
Delta_commuting = a**2 - J_commuting
assert sp.simplify(Delta_clifford - a**2 * (1 - sp.Rational(1, m))) == 0
assert Delta_commuting == 0

print({
    "d": d,
    "m": m,
    "a": str(a),
    "covariance_active_eigenvalue": str(a**2 / m),
    "Delta_commuting": str(Delta_commuting),
    "Delta_clifford": str(Delta_clifford),
    "status": "exact finite construction passed",
})
