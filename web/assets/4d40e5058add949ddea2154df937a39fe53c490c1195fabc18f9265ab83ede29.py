#!/usr/bin/env python3
"""Finite exact-rational fixture for the local 2x2 anisotropy sampler.

This checks algebraic angular-mixture moments, local Gaussian normalizers,
the relative covariance certificate, the global rejection identity/Jensen
bound, zero-tilt reconstruction, and a conditional output-energy bound. It is
finite evidence only, not proof or complexity validation.
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
    return sp.simplify(sum(
        coefficient * gaussian_monomial_moment(cov, exponents)
        for exponents, coefficient in poly.terms()
    ))


def angular_moment(B, k):
    tr = sp.trace(B)
    disc = sp.simplify(tr**2 - 4 * B.det())
    return sp.simplify(sum(
        sp.binomial(k, 2 * r)
        * (tr / 2) ** (k - 2 * r)
        * (disc / 4) ** r
        * sp.binomial(2 * r, r) / 4**r
        for r in range(k // 2 + 1)
    ))


def angular_mixture(B, k, extra_power=0):
    tr = sp.trace(B)
    disc = sp.simplify(tr**2 - 4 * B.det())
    gap = sp.sqrt(disc)
    lam_hi, lam_lo = (tr + gap) / 2, (tr - gap) / 2
    delta = lam_hi - lam_lo
    weights = [
        sp.simplify(
            sp.binomial(k, ell)
            * lam_lo ** (k - ell)
            * delta**ell
            * sp.binomial(2 * ell, ell) / 4**ell
        )
        for ell in range(k + 1)
    ]
    norm = angular_moment(B, k)
    assert sp.simplify(sum(weights) - norm) == 0
    beta_moment = sum(
        weights[ell] * sp.rf(sp.Rational(1, 2) + ell, extra_power)
        / sp.rf(1 + ell, extra_power)
        for ell in range(k + 1)
    ) / norm
    direct = sp.simplify(sum(
        sp.binomial(k, ell)
        * lam_lo ** (k - ell)
        * delta**ell
        * sp.binomial(2 * (ell + extra_power), ell + extra_power)
        / 4 ** (ell + extra_power)
        for ell in range(k + 1)
    ) / norm)
    assert sp.simplify(beta_moment - direct) == 0
    return lam_hi, lam_lo, weights, norm, sp.simplify(beta_moment)


def main():
    B1 = sp.Matrix([
        [sp.Rational(1, 10), sp.Rational(1, 40)],
        [sp.Rational(1, 40), sp.Rational(1, 5)],
    ])
    B2 = sp.Matrix([
        [sp.Rational(3, 10), sp.Rational(1, 30)],
        [sp.Rational(1, 30), sp.Rational(2, 5)],
    ])
    B = sp.diag(B1, B2)
    assert B1.is_positive_definite and B2.is_positive_definite

    # Nonzero inter-mode correlation, with exact relative sandwich 0.9B<=S<=1.1B.
    cross = sp.Rational(1, 100) * sp.eye(2)
    S = B.copy()
    S[:2, 2:4] = cross
    S[2:4, :2] = cross.T
    s_minus, s_plus = sp.Rational(9, 10), sp.Rational(11, 10)
    assert S.is_positive_definite
    assert (S - s_minus * B).is_positive_semidefinite
    assert (s_plus * B - S).is_positive_semidefinite

    # Include an output block and reconstruct a rational pre-tilt covariance C.
    cross_out = sp.zeros(4, 2)
    cross_out[0, 0] = sp.Rational(1, 1000)
    cross_out[2, 1] = sp.Rational(1, 1000)
    C_tilt = S.row_join(cross_out).col_join(
        cross_out.T.row_join(sp.Rational(1, 5) * sp.eye(2))
    )
    assert C_tilt.is_positive_definite
    assert (sp.eye(6) - C_tilt).is_positive_definite
    P_H = sp.diag(1, 1, 1, 1, 0, 0)
    C = (C_tilt.inv() - P_H).inv()
    assert C.is_positive_definite
    assert (C.inv() + P_H).inv() == C_tilt

    counts = [1, 2]
    kappa, m, K0 = sum(counts), len(counts), len(counts) + sum(counts)
    xs = sp.symbols("x0:4")
    W = ((xs[0]**2 + xs[1]**2) / 2) * ((xs[2]**2 + xs[3]**2) / 2)**2 / 2

    # The local matrix normalizer is rational and equals a direct Wick moment.
    mus = [angular_moment(B1, counts[0]), angular_moment(B2, counts[1])]
    Qcov = s_plus * B
    Zq = sp.simplify(s_plus**counts[0] * mus[0] * s_plus**counts[1] * mus[1])
    Zq_direct = gaussian_polynomial_moment(W, xs, Qcov)
    assert sp.simplify(Zq - Zq_direct) == 0

    # Check the exact angular mixture moments for both anisotropic blocks.
    mix_data = []
    for block, k in zip([B1, B2], counts):
        hi, lo, weights, norm, first_moment = angular_mixture(block, k, 1)
        mix_data.append({
            "eigenvalues": [str(hi), str(lo)],
            "weights": [str(w) for w in weights],
            "normalizer": str(norm),
            "E_cos_squared": str(first_moment),
        })

    Delta = S.inv() - Qcov.inv()
    assert Delta.is_positive_semidefinite
    ZS = gaussian_polynomial_moment(W, xs, S)
    M = sp.sqrt(Qcov.det() / S.det())
    alpha = sp.simplify(ZS / (M * Zq))
    assert sp.simplify(M * Zq * alpha - ZS) == 0
    rho = sp.simplify(s_plus / s_minus)
    jensen = sp.exp(-K0 * (rho - 1))
    if sp.N(alpha, 80) + sp.Float("1e-70") < sp.N(jensen, 80):
        raise AssertionError("global Jensen acceptance lower bound failed")
    Lambda = 2 ** int(sp.ceiling(2 * K0 * (rho - 1)))

    K = cross_out.T * S.inv()
    V = sp.Rational(1, 5) * sp.eye(2) - K * S * K.T
    assert V.is_positive_definite
    assert K * S == cross_out.T
    xvec = sp.Matrix(xs)
    xout_quad = sp.expand(sum((K * xvec)[i] ** 2 for i in range(2)))
    exact_kx = sp.N(gaussian_polynomial_moment(W * xout_quad, xs, S) / ZS, 80)
    energy_bound = sp.N(
        2 * s_plus * K0 * Lambda * (K * B * K.T).trace(), 80
    )
    if exact_kx > energy_bound + sp.Float("1e-70"):
        raise AssertionError("output-energy bound failed")

    # A second family has exponentially growing local condition number,
    # constant whitened output map, rare herald, and non-vacuum conditional output.
    n = 40
    a = sp.Rational(1, 2**(2*n))
    gamma = sp.Rational(1, 3)
    B_extreme = sp.diag(a**2, a)
    R_extreme = sp.diag(a, sp.Rational(1, 2**n))
    T_extreme = B_extreme.row_join(gamma * R_extreme).col_join(
        (gamma * R_extreme).row_join(sp.eye(2))
    )
    P_H_extreme = sp.diag(1, 1, 0, 0)
    assert (sp.eye(2) - B_extreme).is_positive_definite
    assert T_extreme.is_positive_definite
    # C° may have eigenvalue >1; only T^{-1}-P_H must be positive.
    bad_I_minus_T_minor = (sp.eye(4) - T_extreme)[[1, 3], [1, 3]]
    assert bad_I_minus_T_minor.det() < 0
    raw_precision = T_extreme.inv() - P_H_extreme
    assert raw_precision.is_positive_definite
    C_extreme = raw_precision.inv()
    assert C_extreme.is_positive_definite
    assert (C_extreme.inv() + P_H_extreme).inv() == T_extreme

    C_hh_expected = B_extreme * (sp.eye(2) - B_extreme).inv()
    C_hu_expected = gamma * (sp.eye(2) - B_extreme).inv() * R_extreme
    C_uu_expected = sp.eye(2) + gamma**2 * B_extreme * (sp.eye(2) - B_extreme).inv()
    assert C_extreme[:2, :2] == C_hh_expected
    assert C_extreme[:2, 2:4] == C_hu_expected
    assert C_extreme[2:4, 2:4] == C_uu_expected
    raw_mean = sp.simplify(sp.trace(C_extreme) / 2)
    raw_mean_formula = sp.simplify(
        1 + (1 + gamma**2) * (B_extreme * (sp.eye(2) - B_extreme).inv()).trace() / 2
    )
    assert sp.simplify(raw_mean - raw_mean_formula) == 0

    K_extreme = gamma * R_extreme * B_extreme.inv()
    V_extreme = sp.eye(2) - K_extreme * B_extreme * K_extreme.T
    A_extreme = K_extreme * R_extreme
    assert K_extreme == gamma * B_extreme.inv() * R_extreme
    assert V_extreme == (1 - gamma**2) * sp.eye(2)
    assert A_extreme == gamma * sp.eye(2)
    assert V_extreme.is_positive_definite

    p_herald_direct = sp.simplify(
        (sp.trace(B_extreme) / 2)
        / sp.sqrt((sp.eye(4) + C_extreme * P_H_extreme).det())
    )
    p_herald_formula = sp.simplify(
        (sp.trace(B_extreme) / 2)
        * sp.sqrt((sp.eye(2) - B_extreme).det())
    )
    assert sp.simplify(p_herald_direct - p_herald_formula) == 0
    p_herald_asymptotic_ratio = sp.simplify(p_herald_formula / (a / 2))

    # Core equals its proposal. For count k=1, ||Y||^2=2 Gamma(2,1),
    # while the retained amplitude is gamma Y + N(0,(1-gamma^2)I).
    alpha_local = sp.S.One
    beta = a  # Smallest scalar covariance beta I dominating B.
    z_s_extreme = sp.trace(B_extreme) / 2
    alpha_scalar = sp.simplify(
        sp.sqrt(B_extreme.det() / beta**2)
        * z_s_extreme / beta
    )
    alpha_scalar_formula = sp.sqrt(a) * (1 + a) / 2
    assert sp.simplify(alpha_scalar - alpha_scalar_formula) == 0
    assert alpha_local == 1

    mean_output = sp.simplify(
        (sp.trace(V_extreme) + 4 * gamma**2) / 2
    )
    p_output_zero = sp.simplify((2 - gamma**2) / 4)
    assert mean_output == sp.Rational(10, 9)
    assert p_output_zero == sp.Rational(17, 36)
    mean_output_bound = sp.simplify(
        (sp.trace(V_extreme)
         + 2 * 2 * (K_extreme * B_extreme * K_extreme.T).trace()) / 2
    )
    assert sp.simplify(mean_output_bound - mean_output).is_nonnegative
    numeric_condition = sp.simplify(B_extreme[1, 1] / B_extreme[0, 0])

    result = {
        "status": "FINITE-EVIDENCE",
        "scope": "Exact rational/algebraic fixtures for local anisotropy and a rare herald with exponentially large condition number and nontrivial conditional output; not theorem validation.",
        "local_blocks": [
            [[str(v) for v in row] for row in B1.tolist()],
            [[str(v) for v in row] for row in B2.tolist()],
        ],
        "relative_certificate": {
            "s_minus": str(s_minus), "s_plus": str(s_plus),
            "verified_exactly": True,
        },
        "tilted_covariance_reconstruction": "PASS",
        "angular_mixture_checks": mix_data,
        "counts": counts,
        "proposal_normalizer_exact": str(Zq),
        "acceptance_exact": str(alpha),
        "jensen_lower_bound": str(sp.N(jensen, 30)),
        "acceptance_numeric": str(sp.N(alpha, 30)),
        "finite_envelope_Lambda": Lambda,
        "conditional_output_covariance_reconstruction": "PASS",
        "output_energy_bound_check": "PASS",
        "extreme_anisotropy_fixture": {
            "n": n,
            "anisotropy_parameter_a": str(a),
            "local_block_condition_number": str(numeric_condition),
            "Cprime_eigenvalue_above_one_witness": "negative 2x2 principal-minor determinant of I-Cprime",
            "raw_rational_covariance_reconstruction": "PASS",
            "raw_input_mean_energy": str(raw_mean),
            "raw_input_mean_energy_minus_one": str(sp.simplify(raw_mean - 1)),
            "local_matrix_acceptance": str(alpha_local),
            "best_scalar_acceptance": str(alpha_scalar),
            "best_scalar_expected_trials": str(sp.simplify(1 / alpha_scalar)),
            "herald_probability": str(p_herald_formula),
            "herald_probability_over_a_over_2": str(p_herald_asymptotic_ratio),
            "K_operator_norm": str(gamma / a),
            "whitened_output_map_A": str(A_extreme),
            "residual_covariance_V": str(V_extreme),
            "conditional_output_mean": str(mean_output),
            "conditional_output_zero_probability": str(p_output_zero),
            "conditional_output_nonvacuum_mass": str(1 - p_output_zero),
            "conditional_output_mean_bound": str(mean_output_bound),
            "scope": "Exact finite fixture; comparison proves scalar-proposal weakness only, not a general algorithmic lower bound.",
        },
    }
    target = Path(__file__).with_name("conditional_gaussian_local_anisotropic_check.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
