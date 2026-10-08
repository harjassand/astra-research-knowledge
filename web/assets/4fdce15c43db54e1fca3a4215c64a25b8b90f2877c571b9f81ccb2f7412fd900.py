#!/usr/bin/env python3
"""Exact heterogeneous local-broadcaster compiler certificate.

The input is a list of qubit broadcasters
  B_i = theta_i B_{Z,n_i} + (1-theta_i) B_U,
where theta_i are rational in [1/4,1], n_i is one of X,Y,Z, B_{Z,n_i}
copies the n_i eigenbasis, and B_U is the universal symmetric cloner.
The output is the product of the local three-outcome EB instruments.  The
script validates a finite heterogeneous instance exactly; the all-L proof is
the product lemma recorded in the accompanying certificate/report.
"""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

import sympy as sp
from sympy import I, Matrix, Rational, eye, zeros, sqrt, kronecker_product


OUT = Path(__file__).resolve().parent
I2 = eye(2)
SWAP = Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
PAULI = {
    "X": Matrix([[0, 1], [1, 0]]),
    "Y": Matrix([[0, -I], [I, 0]]),
    "Z": Matrix([[1, 0], [0, -1]]),
}
H = Matrix([[1, 1], [1, -1]]) / sqrt(2)
S = Matrix([[1, 0], [0, I]])
TO_AXIS = {"Z": I2, "X": H, "Y": S * H}


def symq(q: Q):
    return Rational(q.numerator, q.denominator)


def clean(a):
    return a.applyfunc(lambda x: sp.simplify(sp.expand_complex(x)))


def matrix_json(a):
    return [[str(clean(a)[i, j]) for j in range(a.cols)] for i in range(a.rows)]


def ptrace_right(y):
    return clean(Matrix(2, 2, lambda i, k: sum(y[2 * i + j, 2 * k + j] for j in range(2))))


def rotate_kraus(k, axis):
    u = TO_AXIS[axis]
    return clean(kronecker_product(u, u) * k * u.H)


def local_broadcaster_kraus(theta, axis):
    # B_Z Kraus matrices |00><0| and |11><1|.
    k0, k1 = zeros(4, 2), zeros(4, 2)
    k0[0, 0] = 1
    k1[3, 1] = 1
    # Universal cloner Kraus numerators; physical matrices are A_j/sqrt(6).
    a0, a1 = zeros(4, 2), zeros(4, 2)
    a0[0, 0], a0[1, 1], a0[2, 1] = 2, 1, 1
    a1[1, 0], a1[2, 0], a1[3, 1] = 1, 1, 2
    return [
        (theta, rotate_kraus(k0, axis)),
        (theta, rotate_kraus(k1, axis)),
        ((1 - theta) / 6, a0),
        ((1 - theta) / 6, a1),
    ]


def local_phi(kraus, x):
    y = zeros(4, 4)
    for weight, k in kraus:
        y += symq(weight) * k * x * k.H
    return ptrace_right(clean(y))


def local_ptm(kraus, basis):
    return Matrix(4, 4, lambda i, j: sp.simplify(sp.trace(basis[i] * local_phi(kraus, basis[j])) / 2))


def eb_instrument(theta, axis):
    p_plus = clean((I2 + PAULI[axis]) / 2)
    p_minus = clean((I2 - PAULI[axis]) / 2)
    alpha = (1 + 2 * theta) / 3
    effects = [(alpha, p_plus), (alpha, p_minus), (1 - alpha, I2)]
    states = [p_plus, p_minus, Rational(1, 2) * I2]
    # Return (coefficient, effect), state; coefficients remain rational.
    weighted_effects = [(symq(weight) * effect, state) for (weight, effect), state in zip(effects, states)]
    return alpha, weighted_effects


def ptm_from_ensemble(ensemble, basis):
    def apply(x):
        return clean(sum((sp.trace(m * x) * state for m, state in ensemble), zeros(2, 2)))
    return Matrix(4, 4, lambda i, j: sp.simplify(sp.trace(basis[i] * apply(basis[j])) / 2))


def parse_theta_list(raw):
    vals = [Q(s) for s in raw.split(",")]
    assert vals and all(Q(1, 4) <= t <= 1 for t in vals)
    return vals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--theta", default="1/4,1/3,1/2,2/3,3/4,9/10,1")
    parser.add_argument("--axes", default="Z,X,Y,Z,X,Y,Z")
    args = parser.parse_args()
    thetas = parse_theta_list(args.theta)
    axes = list(args.axes.split(","))
    assert len(axes) == len(thetas) and all(a in TO_AXIS for a in axes)
    L = len(thetas)

    sites = []
    exact_categories = []
    local_tests = []
    for i, (theta, axis) in enumerate(zip(thetas, axes)):
        kraus = local_broadcaster_kraus(theta, axis)
        # Exact TP, with Kraus weights left rational; all ranges are symmetric.
        completeness = clean(sum((symq(w) * k.H * k for w, k in kraus), zeros(2, 2)))
        assert completeness == I2
        assert all(clean(SWAP * k - k) == zeros(4, 2) for _, k in kraus)
        n = PAULI[axis]
        tangents = [p for key, p in PAULI.items() if key != axis]
        basis = [I2, n, tangents[0], tangents[1]]
        phi_ptm = local_ptm(kraus, basis)
        lam_perp = 2 * (1 - symq(theta)) / 3
        lam_parallel = (2 + symq(theta)) / 3
        expected_phi = Matrix.diag(1, lam_parallel, lam_perp, lam_perp)
        assert clean(phi_ptm) == expected_phi

        alpha, ensemble = eb_instrument(theta, axis)
        sum_effects = clean(sum((m for m, _ in ensemble), zeros(2, 2)))
        sum_prepared = clean(sum((sp.trace(m) * state for m, state in ensemble), zeros(2, 2)))
        assert sum_effects == I2 and sum_prepared == I2
        psi_ptm = ptm_from_ensemble(ensemble, basis)
        assert clean(psi_ptm) == Matrix.diag(1, alpha, 0, 0)
        assert alpha == 2 * lam_parallel - 1
        assert lam_perp <= Rational(1, 2)

        local_tests.append({
            "site": i,
            "theta": f"{theta.numerator}/{theta.denominator}",
            "axis": axis,
            "phi_ptm_I_parallel_transverse_transverse": [str(x) for x in expected_phi.diagonal()],
            "psi_ptm_I_parallel_transverse_transverse": ["1", str(alpha), "0", "0"],
            "local_factor2_checked_exactly": True,
            "broadcaster_kraus_completeness": matrix_json(completeness),
            "every_kraus_range_in_symmetric_subspace": True,
            "eb_effect_sum": matrix_json(sum_effects),
            "eb_trace_weighted_preparation_sum": matrix_json(sum_prepared),
        })
        sites.append({
            "theta": f"{theta.numerator}/{theta.denominator}",
            "axis": axis,
            "alpha": str(alpha),
        })
        exact_categories.append((
            (Q(1), Q(lam_parallel), Q(lam_perp)),
            (Q(1), Q(alpha), Q(0)),
        ))

    # Finite exact instance check over the 3^L distinct local spectral types.
    # A transverse label has multiplicity two, so this covers all 4^L basis
    # elements up to eigenvalue degeneracy, not merely selected observables.
    checked = 0
    minimum_slack = None
    for word in itertools.product(range(3), repeat=L):
        lam = Q(1)
        mu = Q(1)
        for i, symbol in enumerate(word):
            lam *= exact_categories[i][0][symbol]
            mu *= exact_categories[i][1][symbol]
        slack = 2 * (1 - lam) - (1 - mu)
        assert slack >= 0
        minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
        checked += 1

    record = {
        "status": "EXACT_HETEROGENEOUS_PRODUCT_COMPILER",
        "sites": L,
        "global_dimension": str(2**L),
        "input_representation": "site list of rational theta_i in [1/4,1] and Pauli axes X/Y/Z; each factor is theta_i times the rotated basis-copy broadcaster plus (1-theta_i) times the universal symmetric cloner",
        "local_sites": sites,
        "local_exact_checks": local_tests,
        "finite_instance_all_mode_check": {
            "spectral_type_words_checked": checked,
            "basis_coverage": "All 4^L tensor eigenoperators are covered; each transverse category represents two orthogonal local modes with the same eigenvalue pair.",
            "minimum_exact_slack": f"{minimum_slack.numerator}/{minimum_slack.denominator}",
        },
        "compiler_output": {
            "local_alpha_formula": "alpha_i=(1+2 theta_i)/3",
            "local_EB_map": "Psi_i=alpha_i Delta_{axis_i}+(1-alpha_i) Depolarizing",
            "canonical_instrument": "effects alpha_i P_{i,+}, alpha_i P_{i,-}, (1-alpha_i)I; preparations P_{i,+}, P_{i,-}, I/2",
            "global_map": "Psi= tensor_i Psi_i",
            "representation_cost": "O(L) local rational records plus total rational bit length; each site applies a 3-outcome local instrument",
            "flat_outcome_count": str(3**L),
            "no_independent_marginal_sampling": "For an entangled input, implement the product POVM physically or by sequential conditional measurements; product outcome marginals are not independent.",
        },
        "all_L_proof": {
            "transverse_case": "Any transverse factor has lambda_i=2(1-theta_i)/3<=1/2 and mu_i=0; all other lambda factors are at most 1, so lambda_word<=1/2 and mu_word=0.",
            "parallel_case": "For the k active parallel sites, mu_i=2 lambda_i-1 in [0,1]. The inequality product_i(1+mu_i)<=2^(k-1)(1+product_i mu_i), proved by induction, implies product_i mu_i>=2 product_i lambda_i-1.",
            "identity_case": "All identity factors have lambda=mu=1 and zero slack.",
            "conclusion": "I-Psi <= 2(I-Phi) on the full Hermitian space for every L, with equality on a single-site parallel mode tensored with identities.",
        },
        "scope_boundary": "Exact for this supplied heterogeneous tensor product family; does not address interacting/bounded-treewidth broadcasters or arbitrary dense self-compatible channels.",
    }
    path = OUT / "HETEROGENEOUS_PRODUCT_COMPARATOR.json"
    path.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({
        "status": record["status"], "sites": L, "dimension": str(2**L),
        "axes": args.axes, "theta": args.theta,
        "spectral_type_words_checked": checked,
        "minimum_slack": record["finite_instance_all_mode_check"]["minimum_exact_slack"],
        "descriptor": str(path),
    }, indent=2))


if __name__ == "__main__":
    main()
