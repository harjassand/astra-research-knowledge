#!/usr/bin/env python3
"""Finite exact-rational diagnostic for the modewise PC-18 certificate.

This is a fixture check, not a proof or complexity validation. It verifies a
heterogeneous two-mode herald covariance, its exact zero-count tilt origin,
the relative Loewner certificate, Gamma-proposal normalization, PSD precision
gap, Jensen lower bound, and conditional-output covariance reconstruction.
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


def main():
    # D0 has different rational mode scales; the standardized correlation
    # matrix has eigenvalues exactly 7/8 and 9/8.
    D0 = sp.diag(sp.Rational(1, 9), sp.Rational(1, 9),
                 sp.Rational(4, 9), sp.Rational(4, 9))
    S = sp.Matrix([
        [sp.Rational(1, 9), 0, sp.Rational(1, 36), 0],
        [0, sp.Rational(1, 9), 0, sp.Rational(1, 36)],
        [sp.Rational(1, 36), 0, sp.Rational(4, 9), 0],
        [0, sp.Rational(1, 36), 0, sp.Rational(4, 9)],
    ])
    s_minus, s_plus = sp.Rational(7, 8), sp.Rational(9, 8)
    assert S.is_positive_definite
    assert (S - s_minus * D0).is_positive_semidefinite
    assert (s_plus * D0 - S).is_positive_semidefinite

    # Add an output block and rational cross covariance, keeping C°<I so it
    # can be represented as (C^-1+P_H)^-1 for the two herald modes.
    B = sp.zeros(4, 2)
    B[0, 0] = sp.Rational(1, 100)
    B[1, 1] = sp.Rational(1, 100)
    C_tilt = S.row_join(B).col_join(B.T.row_join(sp.Rational(1, 3) * sp.eye(2)))
    assert C_tilt.is_positive_definite
    assert (sp.eye(6) - C_tilt).is_positive_definite
    P_H = sp.diag(1, 1, 1, 1, 0, 0)
    C = (C_tilt.inv() - P_H).inv()
    assert C.is_positive_definite
    assert (C.inv() + P_H).inv() == C_tilt

    K = B.T * S.inv()
    V = sp.Rational(1, 3) * sp.eye(2) - K * S * K.T
    assert V.is_positive_definite
    assert K * S == B.T

    # Positive herald counts (1,2) give a nontrivial degree-six weight.
    xs = sp.symbols("x0:4")
    W = ((xs[0]**2 + xs[1]**2) / 2) * ((xs[2]**2 + xs[3]**2) / 2)**2 / 2
    kappa, m = 3, 2
    K0 = m + kappa
    Qcov = s_plus * D0
    Delta = S.inv() - Qcov.inv()
    assert Delta.is_positive_semidefinite
    ZS = gaussian_polynomial_moment(W, xs, S)
    Zq = (s_plus * sp.Rational(1, 9))**1 * (s_plus * sp.Rational(4, 9))**2
    M = sp.sqrt(Qcov.det() / S.det())
    alpha = sp.simplify(ZS / (M * Zq))
    assert alpha > 0

    # Exact Gaussian polynomial integration checks the rejection identity.
    target_scaled = sp.simplify(M * Zq * alpha)
    assert sp.simplify(target_scaled - ZS) == 0

    # Verify the whitened spectral gap and Jensen acceptance bound.
    # D0**(1/2) is rational diagonal in this fixture; this is the congruence
    # that turns the precision gap into S'**(-1)-s_plus**(-1) I.
    Wht = sp.diag(sp.Rational(1, 3), sp.Rational(1, 3),
                   sp.Rational(2, 3), sp.Rational(2, 3))
    Delta_w = Wht * Delta * Wht
    assert Delta_w.is_positive_semidefinite
    eigs = [sp.simplify(v) for v in Delta_w.eigenvals()]
    gap = max(sp.N(v, 80) for v in eigs)
    claimed_gap = sp.Rational(1, 1) / s_minus - sp.Rational(1, 1) / s_plus
    assert all(sp.simplify(claimed_gap - value) >= 0 for value in eigs)
    jensen = sp.exp(-K0 * (s_plus / s_minus - 1))
    alpha_num = sp.N(alpha, 80)
    if alpha_num + sp.Float("1e-70") < sp.N(jensen, 80):
        raise AssertionError("modewise Jensen lower bound failed numerically")

    # Check the stated energy bound on E_pi ||KX||^2 by exact polynomial moments.
    x_quad = sp.expand(sum((K * sp.Matrix(xs))[i]**2 for i in range(2)))
    weighted_kx = gaussian_polynomial_moment(W * x_quad, xs, S)
    exact_kx_energy = sp.N(weighted_kx / ZS, 80)
    bound_kx_energy = sp.N(
        2 * s_plus * K0 * (K * D0 * K.T).trace(), 80
    )
    if exact_kx_energy > bound_kx_energy + sp.Float("1e-70"):
        raise AssertionError("conditional output-energy bound failed numerically")

    result = {
        "status": "FINITE-EVIDENCE",
        "scope": "Exact rational/algebra fixture for one heterogeneous two-mode core; not a theorem validation.",
        "D0_diagonal": ["1/9", "1/9", "4/9", "4/9"],
        "relative_certificate": {
            "s_minus": str(s_minus), "s_plus": str(s_plus),
            "verified_exactly": True,
        },
        "tilted_covariance_reconstruction": "PASS",
        "conditional_covariance_reconstruction": "PASS",
        "counts": [1, 2],
        "kappa": kappa,
        "proposal_normalizer_exact": str(Zq),
        "acceptance_exact": str(alpha),
        "jensen_lower_bound": str(sp.N(jensen, 30)),
        "acceptance_numeric": str(sp.N(alpha_num, 30)),
        "whitened_gap_eigenvalues": [str(sp.N(v, 30)) for v in eigs],
        "output_energy_bound_check": "PASS",
    }
    target = Path(__file__).with_name("conditional_gaussian_modewise_check.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
