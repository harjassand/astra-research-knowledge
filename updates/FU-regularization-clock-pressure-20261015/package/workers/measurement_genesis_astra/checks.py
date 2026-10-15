#!/usr/bin/env python3
"""Finite diagnostics for RESULT.md; no positivity or hardware certification."""
from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp

BASE = Path(__file__).resolve().parent
SOURCE = BASE.parents[1] / "sources" / "regularization_pasted.txt"


def exact_zero(mat):
    return all(sp.trigsimp(sp.simplify(x)) == 0 for x in mat)


sx = sp.Matrix([[0, 1], [1, 0]])
sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
sz = sp.diag(1, -1)
si = sp.eye(2)
gamma = [sp.kronecker_product(sx, si),
         sp.kronecker_product(sy, si),
         sp.kronecker_product(sz, sx),
         sp.kronecker_product(sz, sy)]
ident = sp.eye(4)
for j, gj in enumerate(gamma):
    for k, gk in enumerate(gamma):
        assert gj * gk + gk * gj == (2 * ident if j == k else sp.zeros(4))
q = sp.I * gamma[0] * gamma[1]
assert q == -sp.kronecker_product(sz, si)
assert q * q == ident and q.H == q
rho_plus = (ident + q) / 4
rho_minus = (ident - q) / 4
assert rho_plus * rho_minus == sp.zeros(4)
assert sp.trace(rho_plus) == sp.trace(rho_minus) == 1
assert rho_plus.eigenvals() == rho_minus.eigenvals() == {0: 2, sp.Rational(1, 2): 2}
assert all(sp.trace(rho_plus * g) == sp.trace(rho_minus * g) == 0 for g in gamma)
theta = sp.symbols("theta", real=True)
unitary = sp.cos(theta / 2) * ident - sp.I * sp.sin(theta / 2) * gamma[1]
rotated_observable = unitary.H * gamma[0] * unitary
assert exact_zero(rotated_observable - sp.cos(theta) * gamma[0] + sp.sin(theta) * q)
response_plus = sp.trigsimp(sp.trace(rho_plus * rotated_observable))
response_minus = sp.trigsimp(sp.trace(rho_minus * rotated_observable))
assert sp.simplify(response_plus + sp.sin(theta)) == 0
assert sp.simplify(response_minus - sp.sin(theta)) == 0

X = np.array(sx).astype(complex)
Y = np.array(sy).astype(complex)
Z = np.array(sz).astype(complex)
I2 = np.eye(2, dtype=complex)


def tensor(factors):
    out = np.ones((1, 1), dtype=complex)
    for item in factors:
        out = np.kron(out, item)
    return out


def canonical(nq):
    out = []
    for k in range(nq):
        out.append(tensor([Z] * k + [X] + [I2] * (nq - k - 1)))
        out.append(tensor([Z] * k + [Y] + [I2] * (nq - k - 1)))
    out.append(tensor([Z] * nq))
    return out


rng = np.random.default_rng(20261015)
circuit_cases = []
max_error = 0.0
for m in range(2, 10):
    nq = m // 2
    gs = canonical(nq)[:m]
    dim = 2 ** nq
    eye = np.eye(dim, dtype=complex)
    for j, gj in enumerate(gs):
        for k, gk in enumerate(gs):
            target = 2 * eye if j == k else np.zeros_like(eye)
            assert np.array_equal(gj @ gk + gk @ gj, target)
    all_gs = canonical(nq)
    for j in range(2 * nq):
        if j == 2 * nq - 1:
            local = tensor([I2] * (nq - 1) + [X])
        elif j % 2 == 0:
            k = j // 2
            local = tensor([I2] * k + [Z] + [I2] * (nq - k - 1))
        else:
            k = (j - 1) // 2
            local = tensor([I2] * k + [X, X] + [I2] * (nq - k - 2))
        assert np.array_equal(all_gs[j] @ all_gs[j + 1], 1j * local)
    if m >= 4:
        hidden_q = 1j * gs[0] @ gs[1]
        assert np.trace(hidden_q) == 0
        assert all(np.trace(hidden_q @ g) == 0 for g in gs)
    errors = []
    # Include poles and a coordinate-zero vector as well as generic axes.
    axes = [np.eye(m)[0], -np.eye(m)[0], np.eye(m)[-1]]
    axes += [rng.normal(size=m) for _ in range(10)]
    for original in axes:
        original = original / np.linalg.norm(original)
        v = original.copy()
        compiled = eye.copy()
        for j in reversed(range(m - 1)):
            angle = math.atan2(v[j + 1], v[j])
            gate = math.cos(angle / 2) * eye + math.sin(angle / 2) * (gs[j] @ gs[j + 1])
            compiled = gate @ compiled
            v[j], v[j + 1] = (math.cos(angle) * v[j] + math.sin(angle) * v[j + 1],
                              -math.sin(angle) * v[j] + math.cos(angle) * v[j + 1])
        observable = sum(value * g for value, g in zip(original, gs))
        error = float(np.linalg.norm(compiled @ observable @ compiled.conj().T - gs[0], ord=2))
        assert error < 2e-13, (m, error)
        errors.append(error)
    max_error = max(max_error, *errors)
    circuit_cases.append({"m": m, "qubits": nq, "axes": len(axes),
                          "rotations_per_axis": m - 1, "max_operator_error": max(errors)})

endpoint_checks = []
for m in range(2, 21):
    spherical_third = Fraction(3 * m * m, m + 2)
    contract_third = Fraction(3 * m - 2, 1)
    difference = spherical_third - contract_third
    assert difference == Fraction(-4 * (m - 1), m + 2) < 0
    endpoint_checks.append({"m": m, "difference_for_a_1": str(difference)})

# Check the pointwise classical sign-channel identity with exact arithmetic.
eta, direction_signal = sp.symbols("eta direction_signal", real=True)
garbled = (1 + eta) / 2 * (1 + direction_signal) + (1 - eta) / 2 * (1 - direction_signal)
assert sp.expand(garbled - (1 + eta * direction_signal)) == 0

# The spherical second and fourth moments yield the information/TV constants.
angular_checks = []
for m in [2, 3, 4, 5, 8, 16, 32]:
    mean_abs = math.gamma(m / 2) / (math.sqrt(math.pi) * math.gamma((m + 1) / 2))
    angular_checks.append({"m": m, "E_n1_squared": 1 / m, "E_abs_n1": mean_abs})

out = {
    "status": "PASS",
    "diagnostic_scope": "Exact two-qubit algebra, finite Clifford algebra, pointwise garbling, rational third-moment contradiction, and floating-point circuit compilation only.",
    "not_verified": ["universal positivity", "general analytic proofs", "large-L asymptotic",
                     "finite-bit spherical sampler", "physical implementation", "advantage", "novelty"],
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "exact_two_qubit": {
        "rho_plus_eigenvalues": ["0", "0", "1/2", "1/2"],
        "rho_minus_eigenvalues": ["0", "0", "1/2", "1/2"],
        "orthogonal_supports": True,
        "all_four_static_spin_means": [0, 0, 0, 0],
        "response_plus": str(response_plus),
        "response_minus": str(response_minus),
        "purity_maximally_mixed": str(sp.trace((ident / 4) ** 2)),
        "purity_hidden_state": str(sp.trace(rho_plus ** 2)),
    },
    "circuit_seed": 20261015,
    "circuit_cases": circuit_cases,
    "circuit_max_operator_error": max_error,
    "third_moment_endpoint_checks": endpoint_checks,
    "angular_constants": angular_checks,
}
(BASE / "checks.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({"status": out["status"], "circuit_cases": len(circuit_cases),
                  "tested_axes": sum(x["axes"] for x in circuit_cases),
                  "max_operator_error": max_error,
                  "endpoint_cases": len(endpoint_checks)}, indent=2))
