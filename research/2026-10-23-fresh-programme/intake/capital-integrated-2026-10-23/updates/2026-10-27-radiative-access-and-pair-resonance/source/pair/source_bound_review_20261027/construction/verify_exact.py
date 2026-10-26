#!/usr/bin/env python3
"""Exact two-qubit checks for the source-bound constructive comparator.

This checks finite matrices and normalization conventions. It does not test a
physical SSH implementation or the source's infinite-volume spectral theorem.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
SOURCE = Path(
    "/Users/harjas/Documents/ChatGPT/coordination/.astra-dispatch/sources/"
    "P2_return_2134_20261026/"
    "ASTRA_SSH_EMBEDDED_PAIR_RESONANCE_AND_CZ_20261027.md"
)

I = sp.I
eye = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -I], [I, 0]])
Z = sp.diag(1, -1)
H = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
Sd = sp.diag(1, -I)
kron = sp.kronecker_product
X1 = kron(X, eye)
XX = kron(X, X)
YY = kron(Y, Y)
ZZ = kron(Z, Z)
Hex = (XX + YY) / 2  # J = 1; odd-block off-diagonal is J.
B = kron(H, H)
D = kron(Sd, Sd)
CZ = sp.diag(1, 1, 1, -1)
CNOT = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0],
                  [0, 0, 0, 1], [0, 0, 1, 0]])


def clean(matrix: sp.Matrix) -> sp.Matrix:
    # Normalize roots of unity as well as radicals before exact comparison.
    return matrix.applyfunc(lambda value: sp.simplify(sp.expand_complex(value)))


def zero(matrix: sp.Matrix) -> bool:
    return clean(matrix) == sp.zeros(*matrix.shape)


def exchange(theta: sp.Expr) -> sp.Matrix:
    c, s = sp.cos(theta), sp.sin(theta)
    return sp.Matrix([[1, 0, 0, 0], [0, c, -I * s, 0],
                      [0, -I * s, c, 0], [0, 0, 0, 1]])


E = exchange(sp.pi / 4)
echo = clean(X1 * E * X1 * E)
Uxx = (sp.eye(4) - I * XX) / sp.sqrt(2)
Uzz = (sp.eye(4) - I * ZZ) / sp.sqrt(2)
cz_constructed = clean(sp.exp(I * sp.pi / 4) * D * B * echo * B)
cnot_constructed = clean(kron(eye, H) * cz_constructed * kron(eye, H))

even, odd = [0, 3], [1, 2]
restricted_generators = {"exchange": Hex, "ZI": kron(Z, eye),
                         "IZ": kron(eye, Z), "identity": sp.eye(4)}
trace_gaps = {
    name: sp.simplify(gen.extract(even, even).trace()
                      - gen.extract(odd, odd).trace())
    for name, gen in restricted_generators.items()
}

# Magic basis: local SU(2) generators become real antisymmetric matrices.
e00, e01, e10, e11 = [sp.eye(4)[:, j] for j in range(4)]
Q = sp.Matrix.hstack((e00 + e11) / sp.sqrt(2),
                     I * (e00 - e11) / sp.sqrt(2),
                     I * (e01 + e10) / sp.sqrt(2),
                     (e01 - e10) / sp.sqrt(2))
magic_h = clean(Q.H * Hex * Q)
local_generator_checks = {}
for label, pauli in [("X", X), ("Y", Y), ("Z", Z)]:
    for site, gen in [("L", kron(pauli, eye)),
                      ("R", kron(eye, pauli))]:
        a = clean(Q.H * (-I * gen) * Q)
        local_generator_checks[label + site] = (
            zero(a.T + a) and zero(a.conjugate() - a)
        )
Uhat = clean(sp.exp(I * sp.pi / 4) * CZ)
Uhat_magic = clean(Q.H * Uhat * Q)
m_target = clean(Uhat_magic.T * Uhat_magic)
lam = sp.Symbol("lambda")

checks = {
    "exchange_formula_matches_matrix_exponential": zero(
        E - (-I * sp.pi * Hex / 4).exp()),
    "echo_is_XX_pi_over_4": zero(echo - Uxx),
    "echo_hamiltonians_commute": zero(Hex * (X1 * Hex * X1)
                                       - (X1 * Hex * X1) * Hex),
    "Hadamards_convert_XX_to_ZZ": zero(B * Uxx * B - Uzz),
    "CZ_exact_including_global_phase": zero(cz_constructed - CZ),
    "CNOT_exact": zero(cnot_constructed - CNOT),
    "restricted_even_minus_odd_trace_all_zero": all(v == 0 for v in trace_gaps.values()),
    "magic_basis_is_unitary": zero(Q.H * Q - sp.eye(4)),
    "local_generators_are_real_antisymmetric": all(local_generator_checks.values()),
    "magic_exchange_diagonal_0_0_1_minus1": magic_h == sp.diag(0, 0, 1, -1),
    "SU4_normalized_CZ_determinant_one": sp.simplify(Uhat.det()) == 1,
    "CZ_magic_invariant_spectrum_plus_minus_i_twice":
        sp.factor(m_target.charpoly(lam).as_expr()) == (lam**2 + 1)**2,
}

result = {
    "source": str(SOURCE),
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "checks": checks,
    "all_pass": all(checks.values()),
    "restricted_trace_gaps": {k: str(v) for k, v in trace_gaps.items()},
    "CZ_determinant_even": str(CZ.extract(even, even).det()),
    "CZ_determinant_odd": str(CZ.extract(odd, odd).det()),
    "magic_exchange_eigenvalues_J_equals_1": [0, 0, 1, -1],
    "magic_target_characteristic_polynomial": str(sp.factor(m_target.charpoly(lam).as_expr())),
    "exchange_normalization": "H_ex = (J/2)(XX+YY), E(theta) = exp(-i theta (XX+YY)/2), theta=J t",
    "CZ_formula": "CZ = exp(i*pi/4) (Sd tensor Sd) (H tensor H) XL E(pi/4) XL E(pi/4) (H tensor H)",
    "total_exchange_time": "pi/(2*abs(J))",
    "source_small_g_time": "4*pi/g^2 * (1 + O(g^2))",
    "scope": "Exact effective two-qubit matrix check; ideal arbitrary local gates assumed for constructive sequence.",
}
(ROOT / "exact_check_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
if not result["all_pass"]:
    raise SystemExit(1)
