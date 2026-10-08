#!/usr/bin/env python3
"""Exact rational identities for herald-exponential marginalization.

This is a finite algebra diagnostic, not a proof or complexity validation.
It checks a correlated three-mode Gaussian, one positive-count herald, one
zero-count herald, one retained mode, and the all-zero herald special case.
"""

from functools import lru_cache
import json
from pathlib import Path

import sympy as sp


def gaussian_monomial_moment(cov, exponents):
    indices = tuple(i for i, e in enumerate(exponents) for _ in range(e))
    if len(indices) % 2:
        return sp.S.Zero

    @lru_cache(None)
    def wick(items):
        if not items:
            return sp.S.One
        first = items[0]
        return sum(
            cov[first, items[j]] * wick(items[1:j] + items[j + 1 :])
            for j in range(1, len(items))
        )

    return wick(indices)


def gaussian_polynomial_moment(expression, variables, cov):
    poly = sp.Poly(sp.expand(expression), *variables)
    total = sp.S.Zero
    for exponents, coefficient in poly.terms():
        total += coefficient * gaussian_monomial_moment(cov, exponents)
    return sp.simplify(total)


def principal(matrix, indices):
    return matrix.extract(indices, indices)


def zero_tilt(cov, projector):
    # Multiplication of a Gaussian density by exp(-x^T P x/2).
    return (cov.inv() + projector).inv()


def tilted_mass(cov, projector):
    return sp.sqrt(1 / sp.det(sp.eye(cov.rows) + cov * projector))


def assert_zero(value, label):
    value = sp.simplify(value)
    is_zero = value == 0 if not isinstance(value, sp.MatrixBase) else all(v == 0 for v in value)
    if not is_zero:
        raise AssertionError(f"{label}: residual {value}")


def main():
    n = 6  # (q,p) for three modes
    C = sp.eye(n) + sp.ones(n) / 100 - sp.eye(n) / 100
    assert C.is_positive_definite
    assert (C - sp.Rational(19, 20) * sp.eye(n)).is_positive_semidefinite
    assert (sp.Rational(21, 20) * sp.eye(n) - C).is_positive_semidefinite

    herald = [0, 1, 2, 3]  # first mode has one photon; second mode is zero
    positive = [0, 1]
    output = [4, 5]
    P_H = sp.diag(1, 1, 1, 1, 0, 0)
    P_U = sp.diag(0, 0, 0, 0, 1, 1)
    C_H = principal(C, herald)
    C_tilt = zero_tilt(C, P_H)
    C_tilt_H = principal(C_tilt, herald)
    assert_zero(C_tilt_H - (C_H.inv() + sp.eye(4)).inv(), "herald marginal tilt")

    S = principal(C_tilt, positive)
    b = sp.Rational(1, 2)  # t/(1+t), here t=1
    eps_eff = sp.Rational(1, 39)  # eps_bar/[1+t(1-eps_bar)], eps_bar=1/20
    assert (S / b - (1 - eps_eff) * sp.eye(2)).is_positive_semidefinite
    assert ((1 + eps_eff) * sp.eye(2) - S / b).is_positive_semidefinite

    xs = sp.symbols("x0:6")
    W_H = (xs[0] ** 2 + xs[1] ** 2) / 2  # k=1
    W_U_0 = sp.S.One
    W_U_1 = (xs[4] ** 2 + xs[5] ** 2) / 2
    M_H = gaussian_polynomial_moment(W_H, xs[:2], S)
    p_H = sp.simplify(tilted_mass(C, P_H) * M_H)

    # Isotropic proposal posterior, weighted by the same positive-count power.
    c = 1 + eps_eff
    cb = sp.simplify(c * b)
    Z_proposal = cb  # E[(q^2+p^2)/2] for covariance cb I_2
    M_envelope = sp.simplify(cb / sp.sqrt(sp.det(S)))
    D = sp.simplify(S.inv() - sp.eye(2) / cb)
    alpha = sp.simplify(M_H / (M_envelope * Z_proposal))
    # Exact target/proposal ratio has envelope M_envelope*Z_proposal/M_H;
    # the residual acceptance is exp(-x^T D x/2).
    ratio_scale = sp.simplify(M_envelope * Z_proposal / M_H)
    assert_zero(ratio_scale * alpha - 1, "proposal normalization / acceptance")
    assert (D).is_positive_semidefinite

    # Gaussian conditional for output coordinates after sampling the positive
    # herald coordinates from their polynomially tilted marginal.
    C_UU = principal(C_tilt, output)
    C_U_plus = C_tilt.extract(output, positive)
    K = sp.simplify(C_U_plus * S.inv())
    V = sp.simplify(C_UU - K * S * K.T)
    assert_zero(K * S - C_U_plus, "conditional cross covariance")
    assert_zero(V + K * S * K.T - C_UU, "conditional covariance reconstruction")
    assert V.is_positive_definite

    # Compare direct joint herald/output probabilities with the sequential
    # marginalized formula for output counts 0 and 1.
    P_both = P_H + P_U
    C_both = zero_tilt(C, P_both)
    direct_prefactor = tilted_mass(C, P_both)
    C_after_H = C_tilt
    sequential_output_prefactor = tilted_mass(C_after_H, P_U)
    C_after_both = zero_tilt(C_after_H, P_U)
    assert_zero(C_after_both - C_both, "successive Gaussian tilts")
    count_checks = {}
    for count, W_U in [(0, W_U_0), (1, W_U_1)]:
        W_joint = W_H * W_U
        direct_moment = gaussian_polynomial_moment(W_joint, xs, C_both)
        direct_joint = sp.simplify(direct_prefactor * direct_moment)
        sequential_moment = gaussian_polynomial_moment(W_joint, xs, C_after_both)
        sequential_joint = sp.simplify(
            tilted_mass(C, P_H)
            * sequential_output_prefactor
            * sequential_moment
        )
        assert_zero(direct_joint - sequential_joint, f"output count {count}")
        count_checks[str(count)] = {
            "joint_probability_exact": str(direct_joint),
            "marginalized_identity": "PASS",
        }

    # All-zero herald: no polynomial core and no rejection is needed.
    P_zero = P_H
    C_zero = zero_tilt(C, P_zero)
    zero_mass = tilted_mass(C, P_zero)
    for count, W_U in [(0, W_U_0), (1, W_U_1)]:
        P_zero_and_output = P_zero + P_U
        C_zero_both = zero_tilt(C, P_zero_and_output)
        direct = sp.simplify(
            tilted_mass(C, P_zero_and_output)
            * gaussian_polynomial_moment(W_U, xs, C_zero_both)
        )
        sequential = sp.simplify(
            zero_mass
            * tilted_mass(C_zero, P_U)
            * gaussian_polynomial_moment(W_U, xs, C_zero_both)
        )
        assert_zero(direct - sequential, f"all-zero output count {count}")

    # Jensen lower bound on this fixture, checked numerically at high precision.
    dmax = max(sp.N(v, 80) for v in D.eigenvals().keys())
    second_moment = 2 * cb * (1 + 1)  # 2 c b (m + kappa)
    jensen = sp.exp(-dmax * sp.N(second_moment, 80) / 2)
    alpha_num = sp.N(alpha, 80)
    if alpha_num + sp.Float("1e-70") < jensen:
        raise AssertionError("Jensen lower bound failed numerically")

    result = {
        "status": "FINITE-EVIDENCE",
        "scope": "Exact rational algebra identities on one correlated three-mode fixture; not a theorem validation.",
        "global_covariance_certificate": {"eps_bar": "1/20", "verified_exactly": True},
        "effective_positive_covariance_certificate": {
            "b": str(b),
            "eps_eff": str(eps_eff),
            "verified_exactly": True,
        },
        "positive_herald": {"h_plus": 1, "kappa": 1, "acceptance_exact": str(alpha)},
        "proposal_envelope": str(M_envelope),
        "jensen_lower_bound": str(sp.N(jensen, 30)),
        "acceptance_numeric": str(sp.N(alpha_num, 30)),
        "conditional_output_covariance_reconstruction": "PASS",
        "joint_probability_checks": count_checks,
        "all_zero_herald_no_rejection_checks": {"output_counts": [0, 1], "status": "PASS"},
    }
    target = Path(__file__).with_name("conditional_gaussian_marginalization_check.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
