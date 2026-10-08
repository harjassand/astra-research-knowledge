#!/usr/bin/env python3
"""Exact rational qubit replay for a non-HS-self-adjoint bistochastic lift.

Checks B'=(Lambda* tensor Lambda*) o B0 o Lambda, its direct and staged
Heisenberg outcome effects, the transformed canonical comparator, and a
wrong-adjoint control.  All channel data are Gaussian-rational weighted
Kraus data.
"""

from __future__ import annotations

import json
from pathlib import Path
from itertools import combinations

import sympy as sp
from sympy import I, Matrix, Rational, eye, zeros, kronecker_product


OUT = Path(__file__).resolve().parent
I2 = eye(2)
I4 = eye(4)
X = Matrix([[0, 1], [1, 0]])
Y = Matrix([[0, -I], [I, 0]])
Z = Matrix([[1, 0], [0, -1]])
PAULI = [I2, X, Y, Z]
P0 = (I2 + Z) / 2
P1 = (I2 - Z) / 2
SWAP = Matrix(4, 4, lambda r, c: 1 if (r // 2 == c % 2 and r % 2 == c // 2) else 0)


def clean(x):
    return sp.simplify(sp.expand_complex(x))


def clean_matrix(a):
    return a.applyfunc(clean)


def ptrace_right(y):
    return clean_matrix(Matrix(2, 2, lambda i, k: sum(y[2*i+j, 2*k+j] for j in range(2))))


def ptrace_left(y):
    return clean_matrix(Matrix(2, 2, lambda j, l: sum(y[2*i+j, 2*i+l] for i in range(2))))


# Base broadcaster B0=(9/10) B_Z+(1/10) B_U in weighted Kraus form.
# A rational weight w means the summand is w A X A^dagger.
Kz0 = zeros(4, 2)
Kz1 = zeros(4, 2)
Kz0[0, 0] = 1
Kz1[3, 1] = 1
A0 = zeros(4, 2)
A1 = zeros(4, 2)
A0[0, 0] = 2
A0[1, 1] = 1
A0[2, 1] = 1
A1[1, 0] = 1
A1[2, 0] = 1
A1[3, 1] = 2
B0_KRAUS = [
    (Rational(9, 10), Kz0),
    (Rational(9, 10), Kz1),
    (Rational(1, 60), A0),
    (Rational(1, 60), A1),
]


def b0(x):
    return clean_matrix(sum((w * a * x * a.H for w, a in B0_KRAUS), zeros(4, 4)))


def b0_adj(e):
    return clean_matrix(sum((w * a.H * e * a for w, a in B0_KRAUS), zeros(2, 2)))


def phi0(x):
    return ptrace_right(b0(x))


# Rational unitary U=(3 I+4 i X)/5 and rational weighted-unitary
# bistochastic channel Lambda=(9/25)Ad_I+(16/25)Ad_U.
U = clean_matrix((3 * I2 + 4 * I * X) / 5)
LAMBDA_KRAUS = [Rational(3, 5) * I2, Rational(4, 5) * U]


def lam(x):
    return clean_matrix(sum((l * x * l.H for l in LAMBDA_KRAUS), zeros(x.rows, x.cols)))


def lam_adj(x):
    return clean_matrix(sum((l.H * x * l for l in LAMBDA_KRAUS), zeros(x.rows, x.cols)))


def lam_tensor(x):
    return clean_matrix(sum(
        (kronecker_product(l, r) * x * kronecker_product(l, r).H
         for l in LAMBDA_KRAUS for r in LAMBDA_KRAUS),
        zeros(4, 4),
    ))


def lam_adj_tensor(x):
    return clean_matrix(sum(
        (kronecker_product(l.H, r.H) * x * kronecker_product(l.H, r.H).H
         for l in LAMBDA_KRAUS for r in LAMBDA_KRAUS),
        zeros(4, 4),
    ))


def bprime(x):
    return lam_adj_tensor(b0(lam(x)))


def bprime_adj_staged(e):
    return lam_adj(b0_adj(lam_tensor(e)))


def bprime_weighted_kraus():
    # The outer channel factors are Lambda* and have Kraus L_j^dagger.
    # Weight w_a stays separate, so every matrix remains rational.
    out = []
    for w, a in B0_KRAUS:
        for li in LAMBDA_KRAUS:
            for lj in LAMBDA_KRAUS:
                for lk in LAMBDA_KRAUS:
                    k = kronecker_product(lj.H, lk.H) * a * li
                    out.append((w, clean_matrix(k)))
    return out


BPRIME_KRAUS = bprime_weighted_kraus()


def bprime_direct(x):
    return clean_matrix(sum((w * k * x * k.H for w, k in BPRIME_KRAUS), zeros(4, 4)))


def bprime_adj_direct(e):
    return clean_matrix(sum((w * k.H * e * k for w, k in BPRIME_KRAUS), zeros(2, 2)))


def phi_lift(x):
    return lam_adj(phi0(lam(x)))


def phi_prime(x):
    return ptrace_right(bprime(x))


def wrong_phi(x):
    # Deliberately use Lambda instead of Lambda* after B0.
    return lam(phi0(lam(x)))


def ptm(channel):
    return clean_matrix(Matrix(4, 4, lambda i, j: sp.trace(PAULI[i] * channel(PAULI[j])) / 2))


def psi0(x):
    effects = [Rational(14, 15) * P0, Rational(14, 15) * P1, Rational(1, 15) * I2]
    states = [P0, P1, I2 / 2]
    return clean_matrix(sum((sp.trace(m * x) * s for m, s in zip(effects, states)), zeros(2, 2)))


PSI0_EFFECTS = [Rational(14, 15) * P0, Rational(14, 15) * P1, Rational(1, 15) * I2]
PSI0_STATES = [P0, P1, I2 / 2]
PSI_LIFT_EFFECTS = [lam_adj(m) for m in PSI0_EFFECTS]
PSI_LIFT_STATES = [lam_adj(s) for s in PSI0_STATES]


def psi_lift(x):
    return clean_matrix(sum(
        (sp.trace(m * x) * s for m, s in zip(PSI_LIFT_EFFECTS, PSI_LIFT_STATES)),
        zeros(2, 2),
    ))


def gamma_noisy_povm(axis, gamma=Rational(1, 10)):
    pauli = {"X": X, "Y": Y, "Z": Z}[axis]
    return [clean_matrix((1-gamma) * (I2 + sign * pauli) / 2 + gamma * I2 / 2)
            for sign in (1, -1)]


def tree_effects(pull, leaf_effects):
    level = list(leaf_effects)
    while len(level) > 1:
        assert len(level) % 2 == 0
        level = [pull(level[i], level[i+1]) for i in range(0, len(level), 2)]
    return level[0]


def full_tree_effect_list(pull, leaf_sets):
    level = [[((), e) for e in fx] for fx in leaf_sets]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            combined = []
            for zl, el in level[i]:
                for zr, er in level[i+1]:
                    combined.append((zl + zr, pull(el, er)))
            nxt.append(combined)
        level = nxt
    return level[0]


def pull_bprime_staged(left, right):
    return bprime_adj_staged(kronecker_product(left, right))


def pull_bprime_direct(left, right):
    return bprime_adj_direct(kronecker_product(left, right))


def serialize_matrix(a):
    return [[str(clean(a[i, j])) for j in range(a.cols)] for i in range(a.rows)]


def rational_bits(x):
    x = sp.cancel(x)
    if x.is_Rational:
        return max(abs(int(x.p)).bit_length(), int(x.q).bit_length())
    re, im = sp.re(x), sp.im(x)
    return max(rational_bits(re), rational_bits(im))


def is_psd_2(a):
    assert a == a.H
    return (sp.re(a[0, 0]) >= 0 and sp.re(a[1, 1]) >= 0
            and sp.det(a) >= 0)


def principal_minors(a):
    out = []
    for size in range(1, a.rows + 1):
        for indices in combinations(range(a.rows), size):
            out.append(clean(a.extract(indices, indices).det()))
    return out


def main():
    # Exact Kraus completeness/unitality for Lambda.
    lambda_tp = clean_matrix(sum((l.H * l for l in LAMBDA_KRAUS), zeros(2, 2)))
    lambda_unital = clean_matrix(sum((l * l.H for l in LAMBDA_KRAUS), zeros(2, 2)))
    assert lambda_tp == I2 and lambda_unital == I2
    assert U.H * U == I2

    lambda_ptm = ptm(lam)
    phi0_ptm = ptm(phi0)
    phi_lift_ptm = ptm(phi_lift)
    phi_prime_ptm = ptm(phi_prime)
    wrong_ptm = ptm(wrong_phi)
    assert phi_prime_ptm == phi_lift_ptm
    assert phi_lift_ptm == phi_lift_ptm.T
    assert lambda_ptm != lambda_ptm.T
    assert wrong_ptm != wrong_ptm.T

    # Direct 32-term weighted-Kraus and staged-composition checks.
    tp_bprime = clean_matrix(sum((w * k.H * k for w, k in BPRIME_KRAUS), zeros(2, 2)))
    assert tp_bprime == I2
    basis2 = [Matrix(2,2,lambda r,c: 1 if (r,c)==(i,j) else 0)
              for i,j in ((0,0),(0,1),(1,0),(1,1))]
    bprime_liouville_entries = []
    for x in basis2:
        out = bprime(x)
        assert bprime_direct(x) == out
        assert phi_prime(x) == phi_lift(x)
        assert clean_matrix(SWAP * out * SWAP) == out
        bprime_liouville_entries.extend(list(out))
    assert bprime_adj_direct(eye(4)) == I2
    for e in [kronecker_product(P0, P1), kronecker_product((I2+X)/2, (I2+Y)/2)]:
        assert bprime_adj_direct(e) == bprime_adj_staged(e)

    # The transformed three-outcome comparator remains canonical and has
    # the inherited exact factor-2 operator order.
    sum_effects = clean_matrix(sum(PSI_LIFT_EFFECTS, zeros(2, 2)))
    sum_prepared = clean_matrix(sum(
        (sp.trace(m) * s for m, s in zip(PSI_LIFT_EFFECTS, PSI_LIFT_STATES)),
        zeros(2, 2),
    ))
    assert sum_effects == I2 and sum_prepared == I2
    assert all(clean_matrix(m / sp.trace(m)) == s
               for m, s in zip(PSI_LIFT_EFFECTS, PSI_LIFT_STATES))
    psi_lift_ptm = ptm(psi_lift)
    assert psi_lift_ptm == psi_lift_ptm.T

    # Pauli-basis exact PSD slack.  The lifted identity is
    # I - 2 Lambda*Phi0Lambda + Lambda*Psi0Lambda
    # = I-Lambda*Lambda + Lambda*(I-2Phi0+Psi0)Lambda.
    eye3 = eye(3)
    d0 = phi0_ptm[1:4, 1:4]
    s0 = ptm(psi0)[1:4, 1:4]
    r = lambda_ptm[1:4, 1:4]
    actual_slack = clean_matrix(eye3 - 2 * phi_lift_ptm[1:4, 1:4]
                                + psi_lift_ptm[1:4, 1:4])
    base_slack = clean_matrix(eye3 - 2*d0 + s0)
    decomposed_slack = clean_matrix(eye3 - r.T*r + r.T*base_slack*r)
    assert actual_slack == decomposed_slack
    assert actual_slack == actual_slack.T
    assert all(sp.factor(v) >= 0 for v in principal_minors(actual_slack))

    # Four-leaf exact outcome-effect replay with rational full-support POVMs.
    leaf_sets = [gamma_noisy_povm(axis) for axis in ("X", "Y", "Z", "X")]
    staged_records = full_tree_effect_list(pull_bprime_staged, leaf_sets)
    direct_records = full_tree_effect_list(pull_bprime_direct, leaf_sets)
    assert [z for z, _ in staged_records] == [z for z, _ in direct_records]
    assert all(e == f for (_, e), (_, f) in zip(staged_records, direct_records))
    effects = [e for _, e in staged_records]
    assert clean_matrix(sum(effects, zeros(2,2))) == I2
    assert all(is_psd_2(e) for e in effects)
    probabilities = [sp.trace(e)/2 for e in effects]
    assert sum(probabilities) == 1
    gamma = Rational(1, 10)
    lower_bound = (gamma/2)**4
    assert all(p >= lower_bound for p in probabilities)
    states = [clean_matrix(e/sp.trace(e)) for e in effects]
    assert all(sp.trace(s) == 1 and s == s.H for s in states)
    max_prob_bits = max(rational_bits(p) for p in probabilities)
    max_effect_bits = max(rational_bits(v) for e in effects for v in e)
    max_state_bits = max(rational_bits(v) for s in states for v in s)
    max_comparator_bits = max(
        rational_bits(v)
        for a in (PSI_LIFT_EFFECTS + PSI_LIFT_STATES)
        for v in a
    )
    max_bprime_bits = max(rational_bits(v) for v in bprime_liouville_entries)

    # Wrong-star effect orientation is detected by an exact nonzero witness.
    e_left = leaf_sets[0][0]
    e_right = leaf_sets[1][0]
    wrong_effect = lam_adj(b0_adj(kronecker_product(lam_adj(e_left), lam_adj(e_right))))
    correct_effect = bprime_adj_staged(kronecker_product(e_left, e_right))
    wrong_effect_gap = clean_matrix(wrong_effect - correct_effect)
    assert wrong_effect_gap != zeros(2,2)

    result = {
        "status": "EXACT_RATIONAL_DISSIPATIVE_LIFT_REPLAY",
        "dimension": 2,
        "base_broadcaster": "cycle-7 qubit B0=(9/10) computational copier+(1/10) universal cloner in rational weighted-Kraus form",
        "lambda": {
            "kraus": [serialize_matrix(l) for l in LAMBDA_KRAUS],
            "unitary_component": serialize_matrix(U),
            "pauli_transfer": serialize_matrix(lambda_ptm),
            "is_bistochastic": True,
            "is_HS_selfadjoint": False,
        },
        "lift": {
            "formula": "B'=(Lambda* tensor Lambda*) o B0 o Lambda",
            "raw_weighted_kraus_count": len(BPRIME_KRAUS),
            "formula_for_each_kraus": "(L_j^dagger tensor L_k^dagger) A_a L_i with base weight w_a",
            "direct_equals_staged_on_basis": True,
            "symmetric_output": True,
            "TP": True,
            "marginal_equals_Lambda_star_Phi0_Lambda": True,
            "liouville_entry_num_den_bit_length_max": max_bprime_bits,
            "marginal_pauli_transfer": serialize_matrix(phi_lift_ptm),
            "wrong_output_Lambda_instead_of_Lambda_star_is_not_HS_selfadjoint": True,
            "wrong_output_transfer": serialize_matrix(wrong_ptm),
        },
        "lifted_comparator": {
            "formula": "Psi'=Lambda* o Psi0 o Lambda",
            "outcome_count": len(PSI_LIFT_EFFECTS),
            "effects": [serialize_matrix(m) for m in PSI_LIFT_EFFECTS],
            "prepared_states": [serialize_matrix(s) for s in PSI_LIFT_STATES],
            "canonical_normalization_verified": True,
            "effect_sum_I": True,
            "trace_weighted_preparation_sum_I": True,
            "HS_selfadjoint": True,
            "pauli_transfer": serialize_matrix(psi_lift_ptm),
            "factor2_slack_pauli_block": serialize_matrix(actual_slack),
            "slack_decomposition": "I-Lambda*Lambda + Lambda*(I-2Phi0+Psi0)Lambda",
            "factor2_slack_PSD_exact": True,
        },
        "depth2_outcome_replay": {
            "tree_leaf_axes": ["X", "Y", "Z", "X"],
            "leaf_noise_gamma": "1/10",
            "outcome_count": len(effects),
            "staged_effects_equal_direct_32_kraus_adjoint": True,
            "effects_sum_to_I": True,
            "all_effects_PSD": True,
            "probability_sum": "1",
            "minimum_probability": str(min(probabilities)),
            "uniform_full_support_lower_bound": str(lower_bound),
            "max_probability_num_den_bit_length": max_prob_bits,
            "max_effect_entry_num_den_bit_length": max_effect_bits,
            "max_prepared_state_entry_num_den_bit_length": max_state_bits,
            "max_lifted_comparator_entry_num_den_bit_length": max_comparator_bits,
            "wrong_star_effect_gap": serialize_matrix(wrong_effect_gap),
        },
        "cost_boundary": {
            "general_q_lambda_r0_base": "one B' call has at most r0*q^3 weighted Kraus terms",
            "K_leaf_tree": "naively expanded global Kraus-index count (r0*q^3)^(K-1); retain a recursive circuit instead",
            "tree_POVM_outcomes": "d^K; do not enumerate for the sampled compiler",
            "transformed_known_comparator_outcomes": len(PSI_LIFT_EFFECTS),
            "density_matrix_messages": "one d-by-d effect/state per active tree node",
        },
        "claim_boundary": "This exact small replay validates the adjoint placement, Kraus count, and canonical lifted instrument for finite rational Kraus data. It does not establish that a succinct circuit-only Lambda has a polynomial-size circuit for Lambda*.",
    }
    (OUT / "DISSIPATIVE_REPLAY.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "kraus_count_Bprime": len(BPRIME_KRAUS),
        "lambda_non_HS_selfadjoint": True,
        "phi_prime_HS_selfadjoint": phi_lift_ptm == phi_lift_ptm.T,
        "depth2_effect_count": len(effects),
        "min_depth2_probability": str(min(probabilities)),
        "factor2_slack_PSD": True,
        "artifact": str(OUT / "DISSIPATIVE_REPLAY.json"),
    }, indent=2))


if __name__ == "__main__":
    main()
