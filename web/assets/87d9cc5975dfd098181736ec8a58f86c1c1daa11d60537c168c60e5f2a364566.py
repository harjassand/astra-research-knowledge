#!/usr/bin/env python3
"""Succinct sharp-factor-2 EB comparator for repeated local qubit broadcasters.

This emits a local product-instrument representation.  It intentionally does
not flatten the global 3^L POVM outcome strings into an exponential table.
The all-Pauli-mode operator proof is symbolic in L and is recorded alongside
the concrete output descriptor.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp
from sympy import I, Matrix, Rational, eye, zeros


OUT = Path(__file__).resolve().parent
I2 = eye(2)
X = Matrix([[0, 1], [1, 0]])
Y = Matrix([[0, -I], [I, 0]])
Z = Matrix([[1, 0], [0, -1]])
PAULI = [X, Y, Z]


def exact(x):
    return sp.cancel(sp.expand_complex(x))


def matrix_json(a):
    return [[str(exact(a[i,j])) for j in range(a.cols)] for i in range(a.rows)]


def local_channel(ensemble, a):
    return exact(sum((sp.trace(m*a)*s for m,s in ensemble), zeros(2,2)))


def local_ptm(ensemble):
    basis = [I2, X, Y, Z]
    return Matrix(4,4,lambda i,j: exact(sp.trace(basis[i]*local_channel(ensemble,basis[j]))/2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sites", type=int, default=64)
    args = parser.parse_args()
    L = args.sites
    assert L >= 1

    p0 = Matrix([[1,0],[0,0]])
    p1 = Matrix([[0,0],[0,1]])
    local_ensemble = [
        (Rational(14,15)*p0, p0),
        (Rational(14,15)*p1, p1),
        (Rational(1,15)*I2, Rational(1,2)*I2),
    ]
    total_effect = exact(sum((m for m,_ in local_ensemble),zeros(2,2)))
    total_preparation = exact(sum((sp.trace(m)*s for m,s in local_ensemble),zeros(2,2)))
    assert total_effect == I2
    assert total_preparation == I2
    assert local_ptm(local_ensemble) == Matrix.diag(1,0,0,Rational(14,15))
    for m,s in local_ensemble:
        assert m == m.H and s == s.H
        assert all(sp.re(v).is_nonnegative for v in m.eigenvals().keys())
        assert all(sp.re(v).is_nonnegative for v in s.eigenvals().keys())
        assert sp.trace(s) == 1

    # One-site exact broadcaster: B=(9/10) B_Z+(1/10) B_universal-cloner.
    # Its marginal has eigenvalues (1/15,1/15,29/30).  The product of L
    # supplied local broadcasters is represented by the repeated tensor
    # network below; no global d^6 Liouville matrix is expanded.
    local_phi = Matrix.diag(1, Rational(1,15), Rational(1,15), Rational(29,30))
    local_psi = local_ptm(local_ensemble)
    assert local_psi[0,0] == 1
    assert [local_psi[i,i] for i in range(1,4)] == [0,0,Rational(14,15)]

    # Symbolic all-mode proof certificate.
    # At every site, labels I,X,Y,Z have (lambda,mu)=(1,1),(1/15,0),
    # (1/15,0),(29/30,14/15).  If any X/Y occurs, lambda_word<=1/15 and
    # mu_word=0, so 1-mu<=2(1-lambda) with margin >=13/15.  Otherwise, if
    # k>=1 Zs occur, the margin is 1+(14/15)^k-2(29/30)^k >=0 by the
    # product lemma below.  The all-I mode has zero slack.
    proof = {
        "mode_alphabet": {
            "I": {"lambda": "1", "mu": "1"},
            "X": {"lambda": "1/15", "mu": "0"},
            "Y": {"lambda": "1/15", "mu": "0"},
            "Z": {"lambda": "29/30", "mu": "14/15"},
        },
        "all_mode_cases": [
            {
                "case": "at least one X or Y",
                "lambda_word_upper_bound": "1/15",
                "mu_word": "0",
                "slack_2G_minus_comparator_deficit_lower_bound": "13/15",
            },
            {
                "case": "only I and Z, with k>=1 Z factors",
                "lambda_word": "(29/30)^k",
                "mu_word": "(14/15)^k",
                "slack": "1+(14/15)^k-2*(29/30)^k >= 0",
                "proof": "Set x=14/15=2*(29/30)-1. For x_i in [0,1], product(1+x_i)<=2^(k-1)*(1+product x_i); induction uses (1+p)(1+y)<=2(1+py), equivalent to (1-p)(1-y)>=0.",
            },
            {
                "case": "all I",
                "lambda_word": "1",
                "mu_word": "1",
                "slack": "0",
            },
        ],
        "operator_conclusion": "I-Psi_L <= 2*(I-Phi_L) on the full Hermitian operator space, not only a selected observable set.",
        "sharpness_witness": "A Pauli string with Z on one site and I elsewhere attains equality.",
    }

    # The normalized tracial near-fixed consequence follows from the exact
    # all-mode order, canonical EB positivity/contraction, and Cauchy--Schwarz.
    state_consequence = {
        "promise": "H=H*, tau(H)=0, ||H||_infinity<=1/2, and ||Phi_L(H)-H||_(1,tau)<=r uniformly over the promised family",
        "conclusion": "ordinary physical half-trace error 1/2||Psi_L(rho_H)-rho_H||_1 <= sqrt(r)/2 for rho_H=(I+H)/2^L",
        "derivation": "||(I-Psi_L)H||_(2,tau)^2 <= <H,(I-Psi_L)H>_tau <= 2<H,(I-Phi_L)H>_tau <= r; then ||.||_(1,tau)<=||.||_(2,tau) and physical half-trace error is 1/2||Psi_L(H)-H||_(1,tau).",
        "dimension_or_family_size_dependence": "none, under this supplied product-channel structure",
    }

    record = {
        "status": "EXACT_STRUCTURED_COMPILER",
        "sites": L,
        "global_dimension": str(2**L),
        "local_broadcaster": {
            "definition": "B_1=(9/10) B_Z+(1/10) B_U; B_Z copies the computational-basis label; B_U is the symmetric universal 1-to-2 qubit cloner",
            "local_marginal_ptm_XYZ": ["1/15", "1/15", "29/30"],
            "product_extension": "tensor product of local B_1 maps with output pairs regrouped into two L-qubit receivers; both marginals Phi_1^tensor_L",
            "input_encoding": "one local rational 16x4 Liouville descriptor plus site count L; no expanded global d^6 matrix",
            "input_descriptor_file": "INPUT_BROADCASTER_LIOUVILLE.json",
            "input_size_scaling": "O(1+log L) bits for the homogeneous repeated factor, or O(L) for explicit heterogeneous local descriptors",
        },
        "local_EB_instrument": {
            "formula": "Psi_1=(14/15) Delta_Z+(1/15) Depolarizing",
            "effects": [matrix_json(m) for m,_ in local_ensemble],
            "prepared_states": [matrix_json(s) for _,s in local_ensemble],
            "local_ptm_I_X_Y_Z": [str(local_psi[i,i]) for i in range(4)],
            "global_output_representation": "tensor product of the local three-outcome measure-and-prepare instrument; do not flatten the 3^L outcome strings",
            "global_outcome_count_if_flattened": str(3**L),
            "deployment_cost": "O(L) local 3-outcome measurements and local preparations; classical outcomes may be correlated for entangled inputs and are generated by the physical sequential/local measurement, not by independent outcome sampling",
        },
        "all_mode_operator_certificate": proof,
        "dimension_free_family_consequence": state_consequence,
        "scope_boundary": "This is an exact compiler for a supplied product/tensor-factorized broadcaster family. It does not compile arbitrary dense self-compatible channels or settle the arbitrary-channel conjecture.",
    }
    local_input = OUT / "INPUT_BROADCASTER_LIOUVILLE.json"
    if local_input.exists():
        record["local_broadcaster"]["input_descriptor_sha256"] = hashlib.sha256(local_input.read_bytes()).hexdigest()
    payload = json.dumps(record, indent=2) + "\n"
    path = OUT / "STRUCTURED_PRODUCT_COMPARATOR.json"
    path.write_text(payload)
    record["descriptor_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    summary = json.dumps(record, indent=2) + "\n"
    # Store the hash-bearing final record, whose hash field identifies the
    # hashless canonical payload just written above.
    path.write_text(summary)
    print(json.dumps({
        "status": record["status"],
        "sites": L,
        "dimension": str(2**L),
        "flat_outcomes": str(3**L),
        "local_effects": 3,
        "full_mode_certificate": "symbolic product cases",
        "file": str(path),
        "descriptor_sha256": record["descriptor_sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()
