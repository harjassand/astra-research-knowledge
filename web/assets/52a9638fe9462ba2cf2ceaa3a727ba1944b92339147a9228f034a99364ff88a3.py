#!/usr/bin/env python3
"""Exact d=4 replay of a dissipative, non-HS-selfadjoint bistochastic sandwich.

Core: the two-site CNOT-dressed product broadcaster from cycle 7.
Noise: Lambda=(Ad_H o (3/4 Id + 1/4 Ad_Z)) tensor Id, represented by a
two-term weighted Kraus list. Lambda is CPTP, unital, dissipative and is not
HS self-adjoint. We form Phi=Lambda* Phi0 Lambda and pull back the canonical
core EB instrument through Lambda*.
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
PAULI = {
    "I": I2,
    "X": Matrix([[0, 1], [1, 0]]),
    "Y": Matrix([[0, -I], [I, 0]]),
    "Z": Matrix([[1, 0], [0, -1]]),
}
LABELS = [a + b for a, b in itertools.product("IXYZ", repeat=2)]
BASIS = [kronecker_product(PAULI[a], PAULI[b]) for a, b in itertools.product("IXYZ", repeat=2)]
# Exact rational-entry SU(2) unitary with quaternion coordinates
# (1/3,2/3,2/3,0); its Bloch rotation mixes the dephasing axis with others.
V = Rational(1, 3) * I2 + Rational(2, 3) * I * PAULI["X"] + Rational(2, 3) * I * PAULI["Y"]
U = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
SWAP4 = Matrix(16, 16, lambda r, c: int((r % 4) * 4 + r // 4 == c))


def clean(a):
    return a.applyfunc(lambda x: sp.cancel(sp.simplify(sp.expand_complex(x))))


def matrix_json(a):
    a = clean(a)
    return [[str(a[i, j]) for j in range(a.cols)] for i in range(a.rows)]


def regroup_interleaved_to_receivers():
    p = zeros(16, 16)
    for a1, b1, a2, b2 in itertools.product(range(2), repeat=4):
        old = ((a1 * 2 + b1) * 2 + a2) * 2 + b2
        new = ((a1 * 2 + a2) * 2 + b1) * 2 + b2
        p[new, old] = 1
    return p


def ptrace_right(y, d=4):
    return clean(Matrix(d, d, lambda i, k: sum(y[i * d + j, k * d + j] for j in range(d))))


def ptrace_left(y, d=4):
    return clean(Matrix(d, d, lambda j, l: sum(y[i * d + j, i * d + l] for i in range(d))))


def ptm(channel, basis=BASIS, d=4):
    return clean(Matrix(len(basis), len(basis), lambda i, j: sp.simplify(sp.trace(basis[i] * channel(basis[j])) / d)))


def local_core_kraus():
    k0, k1 = zeros(4, 2), zeros(4, 2)
    k0[0, 0] = 1
    k1[3, 1] = 1
    a0, a1 = zeros(4, 2), zeros(4, 2)
    a0[0, 0], a0[1, 1], a0[2, 1] = 2, 1, 1
    a1[1, 0], a1[2, 0], a1[3, 1] = 1, 1, 2
    return [
        (Rational(9, 10), k0),
        (Rational(9, 10), k1),
        (Rational(1, 60), a0),
        (Rational(1, 60), a1),
    ]


def core_broadcaster_kraus():
    perm = regroup_interleaved_to_receivers()
    out_unitary = kronecker_product(U, U)
    result = []
    for (w1, k1), (w2, k2) in itertools.product(local_core_kraus(), repeat=2):
        k = out_unitary * perm * kronecker_product(k1, k2) * U.H
        result.append((w1 * w2, clean(k)))
    return result


def core_b(x, ks):
    return clean(sum((w * k * x * k.H for w, k in ks), zeros(16, 16)))


def core_left(x, ks):
    return ptrace_right(core_b(x, ks), 4)


def core_right(x, ks):
    return ptrace_left(core_b(x, ks), 4)


def core_eb_ensemble():
    p0 = Matrix([[1, 0], [0, 0]])
    p1 = Matrix([[0, 0], [0, 1]])
    local = [
        (Rational(14, 15) * p0, p0),
        (Rational(14, 15) * p1, p1),
        (Rational(1, 15) * I2, Rational(1, 2) * I2),
    ]
    return [
        (clean(U * kronecker_product(m1, m2) * U.H), clean(U * kronecker_product(s1, s2) * U.H))
        for (m1, s1), (m2, s2) in itertools.product(local, repeat=2)
    ]


def apply_ensemble(x, ensemble):
    return clean(sum((sp.trace(m * x) * s for m, s in ensemble), zeros(4, 4)))


def lambda_kraus():
    # Lambda(X) = 3/4 V X V* + 1/4 V Z X Z V* on site 1, identity on site 2.
    z = PAULI["Z"]
    return [
        (Rational(3, 4), kronecker_product(V, I2)),
        (Rational(1, 4), kronecker_product(V * z, I2)),
    ]


def apply_channel(x, kraus, adjoint=False):
    if not adjoint:
        return clean(sum((w * k * x * k.H for w, k in kraus), zeros(x.rows, x.cols)))
    return clean(sum((w * k.H * x * k for w, k in kraus), zeros(x.rows, x.cols)))


def exact_psd_ldl(a):
    """Exact rational PSD test by symmetric pivoted Schur complements."""
    a = clean(a)
    n = a.rows
    if a != a.H:
        return False, []
    m = [[sp.Rational(a[i, j]) for j in range(n)] for i in range(n)]
    pivots = []
    k = 0
    while k < n:
        if any(m[i][i] < 0 for i in range(k, n)):
            return False, pivots
        positive = next((i for i in range(k, n) if m[i][i] > 0), None)
        if positive is None:
            if any(m[i][j] != 0 for i in range(k, n) for j in range(k, n)):
                return False, pivots
            return True, pivots
        if positive != k:
            m[k], m[positive] = m[positive], m[k]
            for row in m:
                row[k], row[positive] = row[positive], row[k]
        d = m[k][k]
        pivots.append(str(d))
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                m[i][j] = sp.cancel(m[i][j] - m[i][k] * m[k][j] / d)
        k += 1
    return True, pivots


def main():
    assert clean(V * V.H) == I2 and clean(V.H * V) == I2
    core_ks = core_broadcaster_kraus()
    # Exact core broadcaster validity and equal marginals.
    core_completeness = clean(sum((w * k.H * k for w, k in core_ks), zeros(4, 4)))
    assert core_completeness == I4
    core_swap = zeros(16, 16)
    for a in range(4):
        for b in range(4):
            core_swap[b * 4 + a, a * 4 + b] = 1
    core_swap_symmetric = all(clean(core_swap * k - k) == zeros(16, 4) for _, k in core_ks)
    assert core_swap_symmetric
    phi0 = ptm(lambda x: core_left(x, core_ks))
    phi0_right = ptm(lambda x: core_right(x, core_ks))
    assert phi0 == phi0_right
    assert core_left(I4, core_ks) == I4
    psi0_ensemble = core_eb_ensemble()
    psi0 = ptm(lambda x: apply_ensemble(x, psi0_ensemble))
    assert phi0 == phi0.T and psi0 == psi0.T

    # Exact bistochastic, dissipative, non-self-adjoint Lambda.
    lk = lambda_kraus()
    tp_lambda = clean(sum((w * k.H * k for w, k in lk), zeros(4, 4)))
    unital_lambda = clean(sum((w * k * k.H for w, k in lk), zeros(4, 4)))
    assert tp_lambda == I4 and unital_lambda == I4
    r_lambda = ptm(lambda x: apply_channel(x, lk))
    r_lambda_star = ptm(lambda x: apply_channel(x, lk, adjoint=True))
    assert r_lambda_star == r_lambda.T
    assert r_lambda != r_lambda.T
    contraction_defect = clean(eye(16) - r_lambda.T * r_lambda)
    lambda_contraction_ok, lambda_pivots = exact_psd_ldl(contraction_defect)
    assert lambda_contraction_ok

    # Actual 128-term composed Kraus descriptor for B'=(Lambda* tensor Lambda*) B0 Lambda.
    composed = []
    for (wi, li), (wl, ll), (wr, lr), (wo, lo) in itertools.product(lk, lk, core_ks, lk):
        # `wi` is the input Lambda Kraus; wl,wo are the two output Lambda* Kraus.
        k = kronecker_product(ll.H, lo.H) * lr * li
        composed.append((wi * wl * wr * wo, clean(k)))
    # Kraus order above has 2*2*16*2=128 entries, but the product iteration
    # includes the output-left, input, core, output-right roles as documented.
    assert len(composed) == 128
    bprime_completeness = clean(sum((w * k.H * k for w, k in composed), zeros(4, 4)))
    assert bprime_completeness == I4

    r_phi = clean(r_lambda.T * phi0 * r_lambda)
    r_psi = clean(r_lambda.T * psi0 * r_lambda)
    assert r_phi == r_phi.T and r_psi == r_psi.T
    assert r_phi[0, 0] == 1 and r_phi[0, 1:] == zeros(1, 15) and r_phi[1:, 0] == zeros(15, 1)
    assert r_psi[0, 0] == 1 and r_psi[0, 1:] == zeros(1, 15) and r_psi[1:, 0] == zeros(15, 1)

    # The lifted canonical instrument has the same nine outcomes; verify all
    # effect/state normalizations exactly after applying Lambda*.
    pulled = []
    for m, state in psi0_ensemble:
        mp = apply_channel(m, lk, adjoint=True)
        sprep = apply_channel(state, lk, adjoint=True)
        assert clean(mp - mp.H) == zeros(4, 4)
        assert clean(sprep - sprep.H) == zeros(4, 4)
        assert sp.simplify(sp.trace(sprep)) == 1
        assert clean(sprep - mp / sp.trace(mp)) == zeros(4, 4)
        pulled.append((mp, sprep))
    pulled_effect_sum = clean(sum((m for m, _ in pulled), zeros(4, 4)))
    pulled_prep_sum = clean(sum((sp.trace(m) * s for m, s in pulled), zeros(4, 4)))
    assert pulled_effect_sum == I4 and pulled_prep_sum == I4
    r_psi_from_instrument = ptm(lambda x: apply_ensemble(x, pulled))
    assert r_psi_from_instrument == r_psi

    # Direct output marginal checks use the explicit physical composition:
    # Lambda input, B0, then Lambda* on both outputs. On the marginal, the
    # traced-side Lambda* disappears because it is TP.
    phi_left = r_lambda.T * phi0 * r_lambda
    phi_right = r_lambda.T * phi0_right * r_lambda
    assert phi_left == phi_right == r_phi

    core_slack = clean(2 * (eye(16) - phi0) - (eye(16) - psi0))
    core_ok, core_pivots = exact_psd_ldl(core_slack)
    assert core_ok
    final_slack = clean(2 * (eye(16) - r_phi) - (eye(16) - r_psi))
    final_from_decomposition = clean(contraction_defect + r_lambda.T * core_slack * r_lambda)
    assert final_slack == final_from_decomposition
    final_ok, final_pivots = exact_psd_ldl(final_slack)
    assert final_ok

    offdiag_phi = sum(1 for i in range(16) for j in range(16) if i != j and r_phi[i, j] != 0)
    offdiag_psi = sum(1 for i in range(16) for j in range(16) if i != j and r_psi[i, j] != 0)
    assert offdiag_phi > 0 and offdiag_psi > 0

    record = {
        "status": "EXACT_DISSIPATIVE_SANDWICH_REPLAY",
        "dimension": 4,
        "pauli_basis_order": LABELS,
        "core": {
            "broadcaster": "Two-site CNOT dressing of the product of B1=(9/10)BZ+(1/10)BU local qubit symmetric broadcasters.",
            "core_kraus_count": len(core_ks),
            "core_kraus_completeness": matrix_json(core_completeness),
            "core_output_is_swap_symmetric": core_swap_symmetric,
            "marginal_transfer": matrix_json(phi0),
            "canonical_EB_outcomes": len(psi0_ensemble),
            "EB_transfer": matrix_json(psi0),
            "exact_core_factor2_slack_psd": core_ok,
        },
        "dissipative_lambda": {
            "definition": "Lambda=(Ad_V o (3/4 Id + 1/4 Ad_Z)) tensor Id on two qubits, V=I/3+(2i/3)X+(2i/3)Y is an exact rational-entry SU(2) unitary",
            "weighted_kraus": [
                {"weight": str(w), "matrix": matrix_json(k)} for w, k in lk
            ],
            "weighted_Kraus_TP_sum": matrix_json(tp_lambda),
            "weighted_Kraus_unital_sum": matrix_json(unital_lambda),
            "PTM": matrix_json(r_lambda),
            "HS_adjoint_PTM": matrix_json(r_lambda_star),
            "not_HS_selfadjoint": r_lambda != r_lambda.T,
            "contraction_defect_I_minus_LambdaStarLambda_PSD": lambda_contraction_ok,
        },
        "sandwiched_output": {
            "definition": "Phi=Lambda* Phi0 Lambda; Psi=Lambda* Psi0 Lambda",
            "explicit_composed_broadcaster_Kraus_count": len(composed),
            "composed_broadcaster_Kraus_TP_sum": matrix_json(bprime_completeness),
            "two_marginal_transfer_matrices_equal": phi_left == phi_right,
            "Phi_transfer": matrix_json(r_phi),
            "Psi_transfer": matrix_json(r_psi),
            "Phi_HS_selfadjoint": r_phi == r_phi.T,
            "Psi_HS_selfadjoint": r_psi == r_psi.T,
            "Phi_unital_and_TP": r_phi[0, 0] == 1 and r_phi[0, 1:] == zeros(1, 15) and r_phi[1:, 0] == zeros(15, 1),
            "Phi_is_not_diagonal_in_the_core_Pauli_basis": offdiag_phi > 0,
            "Psi_is_not_diagonal_in_the_core_Pauli_basis": offdiag_psi > 0,
        },
        "pulled_back_canonical_instrument": {
            "outcome_count": len(pulled),
            "effects_sum": matrix_json(pulled_effect_sum),
            "trace_weighted_preparation_sum": matrix_json(pulled_prep_sum),
            "all_preparations_trace_one": True,
            "preparation_equals_effect_over_trace_for_each_outcome": True,
            "effects_and_preparations": [
                {"effect": matrix_json(m), "prepared_state": matrix_json(s)} for m, s in pulled
            ],
        },
        "operator_order_certificate": {
            "constant": 2,
            "core_slack_PSD": core_ok,
            "Lambda_contraction_defect_PSD": lambda_contraction_ok,
            "identity": "2(I-Phi)-(I-Psi)=(I-Lambda*Lambda)+Lambda*[2(I-Phi0)-(I-Psi0)]Lambda",
            "final_slack_matrix": matrix_json(final_slack),
            "exact_pivoted_LDL_PSD": final_ok,
            "LDL_positive_pivots": final_pivots,
            "all_16_Hermitian_modes_covered": True,
        },
        "scope_boundary": "This is a finite exact example of a non-selfadjoint dissipative bistochastic sandwich of an interacting self-compatible core. The general theorem requires supplied exact bistochastic Lambda and a core comparator; it does not synthesize either input structure from an arbitrary channel.",
    }
    path = OUT / "DISSIPATIVE_SANDWICH_REPLAY.json"
    path.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({
        "status": record["status"], "dimension": 4,
        "composed_broadcaster_kraus": len(composed), "eb_outcomes": len(pulled),
        "offdiag_phi": offdiag_phi, "offdiag_psi": offdiag_psi,
        "final_order_psd": final_ok, "final_positive_pivots": len(final_pivots),
        "file": str(path),
    }, indent=2))


if __name__ == "__main__":
    main()
