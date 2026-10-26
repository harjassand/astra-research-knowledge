#!/usr/bin/env python3
"""Exact 4x4 control-algebra checks; does not test the SSH spectral theorem."""
import hashlib
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
SOURCE = Path('/Users/harjas/Documents/ChatGPT/coordination/.astra-dispatch/sources/P2_return_2134_20261026/ASTRA_SSH_EMBEDDED_PAIR_RESONANCE_AND_CZ_20261027.md')
ii = sp.I
I2 = sp.eye(2)
I4 = sp.eye(4)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -ii], [ii, 0]])
Z = sp.diag(1, -1)
kron = sp.kronecker_product
XI, YI, ZI = (kron(p, I2) for p in (X, Y, Z))
IX, IY, IZ = (kron(I2, p) for p in (X, Y, Z))
XX, YY, ZZ = (kron(p, p) for p in (X, Y, Z))
A = XX + YY
C = kron(Y, X) - kron(X, Y)
D = ZI - IZ
S = ZI + IZ


def clean(M):
    return M.applyfunc(lambda x: sp.simplify(sp.expand_complex(x)))


def equal(A, B):
    return clean(A - B) == sp.zeros(*A.shape)


def vector(M):
    return sp.Matrix(list(M))


def lie_closure(generators):
    """Hermitian realization of Lie closure using [A,B]/(2i)."""
    basis = []
    columns = []
    for M in generators:
        v = vector(M)
        if sp.Matrix.hstack(*columns, v).rank() > len(columns):
            basis.append(M)
            columns.append(v)
    while True:
        count = len(basis)
        for a in range(count):
            for b in range(a):
                M = sp.simplify((basis[a] * basis[b] - basis[b] * basis[a]) / (2 * ii))
                v = vector(M)
                if sp.Matrix.hstack(*columns, v).rank() > len(columns):
                    basis.append(M)
                    columns.append(v)
        if len(basis) == count:
            return basis


def exchange(theta):
    """exp[-i theta (XX+YY)] in |00>,|01>,|10>,|11> order."""
    c, s = sp.cos(2 * theta), sp.sin(2 * theta)
    return sp.Matrix([[1, 0, 0, 0], [0, c, -ii*s, 0],
                      [0, -ii*s, c, 0], [0, 0, 0, 1]])


def block_ratio(U):
    even = U.extract([0, 3], [0, 3])
    odd = U.extract([1, 2], [1, 2])
    return sp.simplify(even.det() / odd.det())


theta = sp.Symbol('theta', real=True)
phase_z1 = sp.diag(sp.exp(-ii*theta), sp.exp(-ii*theta),
                   sp.exp(ii*theta), sp.exp(ii*theta))
phase_z2 = sp.diag(sp.exp(-ii*theta), sp.exp(ii*theta),
                   sp.exp(-ii*theta), sp.exp(ii*theta))
CZ = sp.diag(1, 1, 1, -1)
phase = (1 - ii) / sp.sqrt(2)  # exp(-i pi/4)
L = sp.diag(ii, 1, 1, -ii)  # exp[i pi(ZI+IZ)/4]
ZZ_gate = (I4 - ii*ZZ) / sp.sqrt(2)
hadamard = (X + Z) / sp.sqrt(2)
Q = kron(hadamard, hadamard)

# Two exchange pulses of angle pi/8, with X on the left memory.
E = exchange(sp.pi/8)
partial_echo = E * XI * E * XI
partial_CZ = phase * L * Q * partial_echo * Q

# Two full signed iSWAPs; inverse F^dagger = (Z tensor Z) F costs one F.
F = exchange(sp.pi/4)
R = (I4 + ii*XI) / sp.sqrt(2)
B = (I4 - ii*IX) / sp.sqrt(2)
full_ZZ = B * F * R * F.H * B.H
full_CZ = phase * L * full_ZZ

restricted = lie_closure([A, ZI, IZ])
expanded = lie_closure([A, XI, YI, ZI, IX, IY, IZ])
target_span = sp.Matrix.hstack(*(vector(M) for M in [S, D, A, C]))
restricted_in_span = all(sp.Matrix.hstack(target_span, vector(M)).rank() == 4
                         for M in restricted)
checks = {
    'restricted_lie_dimension_is_4': len(restricted) == 4,
    'restricted_lie_span_is_S_D_A_C': restricted_in_span,
    'expanded_lie_dimension_is_15': len(expanded) == 15,
    'exchange_block_determinant_ratio_is_1': block_ratio(exchange(theta)) == 1,
    'ZI_phase_block_determinant_ratio_is_1': block_ratio(phase_z1) == 1,
    'IZ_phase_block_determinant_ratio_is_1': block_ratio(phase_z2) == 1,
    'CZ_block_determinant_ratio_is_minus_1': block_ratio(CZ) == -1,
    'partial_echo_equals_exp_minus_i_pi_XX_over_4': equal(partial_echo, (I4-ii*XX)/sp.sqrt(2)),
    'two_partial_exchange_CZ_is_exact': equal(partial_CZ, CZ),
    'full_exchange_conjugates_XI_to_minus_ZY': equal(F*XI*F.H, -kron(Z,Y)),
    'full_exchange_inverse_equals_ZZ_times_full_exchange': equal(F.H, ZZ*F),
    'two_full_exchange_ZZ_is_exact': equal(full_ZZ, ZZ_gate),
    'two_full_exchange_CZ_is_exact': equal(full_CZ, CZ),
}
result = {
    'scope': 'Exact 4x4 algebra and ideal control resources only; no SSH spectral or device audit.',
    'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'sympy_version': sp.__version__,
    'restricted_lie_dimension': len(restricted),
    'expanded_lie_dimension': len(expanded),
    'checks': checks,
    'all_passed': all(checks.values()),
}
output = HERE / 'exact_control_check.json'
output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
assert result['all_passed']
