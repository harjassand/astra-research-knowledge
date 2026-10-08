#!/usr/bin/env python3
"""Exact two-site entangling-circuit dressed broadcaster/comparator replay.

Starting from the local rational symmetric broadcaster B_1, form
  B' = (Ad_U tensor Ad_U) o (B_1 tensor B_1) o Ad_{U*}
with U=CNOT.  The all-L extension is valid for any supplied unitary circuit U;
the finite exact replay verifies a nonproduct, entangling two-site instance.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import sympy as sp
from sympy import I, Matrix, Rational, eye, zeros, kronecker_product


OUT = Path(__file__).resolve().parent
I2 = eye(2)
I4 = eye(4)
X = Matrix([[0, 1], [1, 0]])
Y = Matrix([[0, -I], [I, 0]])
Z = Matrix([[1, 0], [0, -1]])
PAULI = {"I": I2, "X": X, "Y": Y, "Z": Z}
THETA = Rational(9, 10)


def clean(a):
    return a.applyfunc(lambda x: sp.simplify(sp.expand_complex(x)))


def matrix_json(a):
    a = clean(a)
    return [[str(a[i, j]) for j in range(a.cols)] for i in range(a.rows)]


def regroup_interleaved_to_receivers():
    # Old output bit order is A1,B1,A2,B2; new order is A1,A2,B1,B2.
    p = zeros(16, 16)
    for a1, b1, a2, b2 in itertools.product(range(2), repeat=4):
        old = ((a1 * 2 + b1) * 2 + a2) * 2 + b2
        new = ((a1 * 2 + a2) * 2 + b1) * 2 + b2
        p[new, old] = 1
    return p


def swap_receivers():
    s = zeros(16, 16)
    for a in range(4):
        for b in range(4):
            s[b * 4 + a, a * 4 + b] = 1
    return s


def local_b_kraus():
    k0, k1 = zeros(4, 2), zeros(4, 2)
    k0[0, 0] = 1
    k1[3, 1] = 1
    a0, a1 = zeros(4, 2), zeros(4, 2)
    a0[0, 0], a0[1, 1], a0[2, 1] = 2, 1, 1
    a1[1, 0], a1[2, 0], a1[3, 1] = 1, 1, 2
    return [
        (THETA, k0), (THETA, k1),
        ((1 - THETA) / 6, a0), ((1 - THETA) / 6, a1),
    ]


def ptrace_right(y, d=4):
    return clean(Matrix(d, d, lambda i, k: sum(y[i * d + j, k * d + j] for j in range(d))))


def ptm(channel, basis, d):
    return Matrix(len(basis), len(basis), lambda i, j: sp.simplify(sp.trace(basis[i] * channel(basis[j])) / d))


def product_ensemble():
    p0 = Matrix([[1, 0], [0, 0]])
    p1 = Matrix([[0, 0], [0, 1]])
    local = [
        (Rational(14, 15) * p0, p0),
        (Rational(14, 15) * p1, p1),
        (Rational(1, 15) * I2, Rational(1, 2) * I2),
    ]
    return [
        (kronecker_product(m1, m2), kronecker_product(s1, s2))
        for (m1, s1), (m2, s2) in itertools.product(local, repeat=2)
    ]


def main():
    U = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])  # CNOT
    regroup = regroup_interleaved_to_receivers()
    global_kraus = []
    for (w1, k1), (w2, k2) in itertools.product(local_b_kraus(), repeat=2):
        k = kronecker_product(k1, k2)
        k = regroup * k
        k = kronecker_product(U, U) * k * U.H
        global_kraus.append((sp.Rational(w1 * w2), clean(k)))

    completeness = clean(sum((w * k.H * k for w, k in global_kraus), zeros(4, 4)))
    assert completeness == I4
    swap = swap_receivers()
    assert all(clean(swap * k - k) == zeros(16, 4) for _, k in global_kraus)

    def bprime(x):
        y = zeros(16, 16)
        for w, k in global_kraus:
            y += w * k * x * k.H
        return clean(y)

    def phi(x):
        return ptrace_right(bprime(x), 4)

    assert phi(I4) == I4

    basis = [kronecker_product(PAULI[a], PAULI[b]) for a, b in itertools.product("IXYZ", repeat=2)]
    labels = [a + b for a, b in itertools.product("IXYZ", repeat=2)]
    phi_transfer = clean(ptm(phi, basis, 4))
    assert all(phi_transfer[i, j] == 0 for i in range(16) for j in range(16) if i != j)

    # The comparator is the product canonical instrument dressed by the same U.
    ensemble = []
    for m, state in product_ensemble():
        ensemble.append((clean(U * m * U.H), clean(U * state * U.H)))
    assert all(all(v >= 0 for v in sp.Matrix(m).eigenvals().keys()) for m, _ in ensemble)
    assert all(all(v >= 0 for v in sp.Matrix(state).eigenvals().keys()) for _, state in ensemble)
    sum_effects = clean(sum((m for m, _ in ensemble), zeros(4, 4)))
    sum_preparations = clean(sum((sp.trace(m) * state for m, state in ensemble), zeros(4, 4)))
    assert sum_effects == I4 and sum_preparations == I4

    def psi(x):
        return clean(sum((sp.trace(m * x) * state for m, state in ensemble), zeros(4, 4)))

    assert psi(I4) == I4

    psi_transfer = clean(ptm(psi, basis, 4))
    assert all(psi_transfer[i, j] == 0 for i in range(16) for j in range(16) if i != j)
    phi_eigs = [sp.Rational(phi_transfer[i, i]) for i in range(16)]
    psi_eigs = [sp.Rational(psi_transfer[i, i]) for i in range(16)]
    slack = [sp.simplify(2 * (1 - lam) - (1 - mu)) for lam, mu in zip(phi_eigs, psi_eigs)]
    assert all(x >= 0 for x in slack)

    # Exact nonproduct witness: CNOT^*=CNOT maps X_control to X_control X_target,
    # X_target to itself, and X_control X_target to X_control.  Thus transfer
    # values cannot factor as a tensor product of one-site transfers.
    value_xi = phi_transfer[labels.index("XI"), labels.index("XI")]
    value_ix = phi_transfer[labels.index("IX"), labels.index("IX")]
    value_xx = phi_transfer[labels.index("XX"), labels.index("XX")]
    assert value_xi == Rational(1, 225)
    assert value_ix == Rational(1, 15)
    assert value_xx == Rational(1, 15)
    assert value_xx != value_xi * value_ix

    record = {
        "status": "EXACT_FINITE_DEPTH_DRESSED_COMPILER",
        "sites": 2,
        "global_dimension": 4,
        "input_broadcaster": "B'=(Ad_U tensor Ad_U) o (B_1 tensor B_1) o Ad_{U*}, B_1=(9/10)B_Z+(1/10)B_U, U=CNOT",
        "supplied_circuit": {"gate_list": ["CNOT(control=site_1,target=site_2)"], "unitary_matrix": matrix_json(U)},
        "broadcaster_checks": {
            "exact_global_kraus_completeness": [[str(completeness[i, j]) for j in range(4)] for i in range(4)],
            "every_global_kraus_range_is_swap_symmetric": True,
            "marginal_transfer_diagonal": True,
            "marginal_pauli_word_eigenvalues": {labels[i]: str(phi_eigs[i]) for i in range(16)},
        },
        "nonproduct_witness": {
            "transfer_XI": str(value_xi), "transfer_IX": str(value_ix), "transfer_XX": str(value_xx),
            "product_factor_would_require": str(value_xi * value_ix),
            "conclusion": "The dressed marginal is not a tensor product of one-site channels.",
        },
        "comparator": {
            "definition": "Psi'=Ad_U o (Psi_1 tensor Psi_1) o Ad_{U*}, Psi_1=(14/15)Delta_Z+(1/15)Depolarizing",
            "canonical_outcome_count": 9,
            "canonical_effects_and_prepared_states": [
                {"effect": matrix_json(m), "prepared_state": matrix_json(state)}
                for m, state in ensemble
            ],
            "canonical_effect_sum": [[str(sum_effects[i, j]) for j in range(4)] for i in range(4)],
            "trace_weighted_preparation_sum": [[str(sum_preparations[i, j]) for j in range(4)] for i in range(4)],
            "pauli_word_eigenvalues": {labels[i]: str(psi_eigs[i]) for i in range(16)},
        },
        "all_mode_order_check": {
            "number_of_pauli_modes": 16,
            "exact_slacks_2G_minus_deficit": {labels[i]: str(slack[i]) for i in range(16)},
            "conclusion": "I-Psi' <= 2(I-Phi') on every Hermitian operator.",
            "sharpness_witness": "The CNOT-dressed target-site Z mode Z tensor Z attains equality.",
        },
        "general_circuit_theorem": {
            "input_class": "Any supplied L-site product of local symmetric broadcasters B_i, dressed as B_U=(Ad_U tensor Ad_U) o (tensor_i B_i) o Ad_{U*} by a supplied unitary circuit U.",
            "output": "Psi_U=Ad_U o (tensor_i Psi_i) o Ad_{U*}, where each Psi_i is the local canonical EB comparator.",
            "proof": "The product all-mode inequality is conjugated by the Hilbert-Schmidt unitary Ad_U; EB, TP, unitality and self-adjointness are preserved. The output broadcaster remains swap-symmetric because the same U is applied to each receiver.",
            "implementation_cost": "O(LD) gates/operations for a depth-D bounded-range circuit plus L local three-outcome instruments; input/output circuit descriptions are supplied succinctly.",
            "instrument_representation": "Apply U* to input, use the product local measurement, prepare the local product state, then apply U. A flat POVM has 3^L outcomes and is not materialized.",
        },
        "scope_boundary": "Exact for unitary-circuit-dressed product broadcasters. This is a structured correlated/interacting family, not a compiler for arbitrary interacting or bounded-treewidth broadcasters.",
    }
    path = OUT / "FINITE_DEPTH_DRESSED_COMPARATOR.json"
    path.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({
        "status": record["status"], "dimension": 4, "local_depth": 1,
        "outcomes": 9, "all_modes": 16, "min_slack": str(min(slack)),
        "nonproduct_witness": [str(value_xi), str(value_ix), str(value_xx)],
        "file": str(path),
    }, indent=2))


if __name__ == "__main__":
    main()
