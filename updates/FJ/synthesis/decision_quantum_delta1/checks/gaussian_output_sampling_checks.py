#!/usr/bin/env python3
"""Small numerical checks for the Gaussian output-sampling lemma.

These checks validate formulas on finite examples; they do not prove the
general inequalities or certify a finite-bit implementation.
"""

from __future__ import annotations

import itertools
import json
import math

import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr


def bernoulli_centered(amplitude: float, probability: float):
    values = np.array([-amplitude * probability,
                       amplitude * (1.0 - probability)])
    probs = np.array([1.0 - probability, probability])
    return values, probs


def scalar_chi2_mixture(values, probs, sigma):
    exact = 0.0
    for vi, pi in zip(values, probs):
        for vj, pj in zip(values, probs):
            exact += pi * pj * math.exp(vi * vj / sigma**2)
    exact -= 1.0

    def integrand(x):
        ratio = sum(
            p * math.exp(x * v / sigma**2 - v**2 / (2.0 * sigma**2))
            for v, p in zip(values, probs)
        )
        q = math.exp(-x * x / (2.0 * sigma**2)) / (
            math.sqrt(2.0 * math.pi) * sigma
        )
        return q * (ratio - 1.0) ** 2

    # A finite twelve-sigma window avoids overflow in the *ratio* evaluated
    # by QUADPACK at extreme transformed tail nodes; omitted Gaussian tails
    # are negligible for these bounded shifts.
    numerical, error = quad(integrand, -12.0 * sigma, 12.0 * sigma,
                            epsabs=2e-13, epsrel=2e-13, limit=300)
    return exact, numerical, error


def scalar_factor(values, probs, sigma):
    return sum(
        pi * pj * math.exp(vi * vj / sigma**2)
        for vi, pi in zip(values, probs)
        for vj, pj in zip(values, probs)
    )


def rare_triangular_bump(d, amplitude=1.0, sigma=1.0):
    """g_i(x)=A*w*(1-|x_i|/w)_+, w=d^(-1/4), X=g(G)."""
    w = d ** (-0.25)
    normal_pdf = lambda x: math.exp(-x * x / 2.0) / math.sqrt(2.0 * math.pi)
    mu = 2.0 * amplitude * w * quad(
        lambda x: (1.0 - x / w) * normal_pdf(x), 0.0, w,
        epsabs=1e-15, epsrel=1e-13,
    )[0]
    second = 2.0 * amplitude**2 * w**2 * quad(
        lambda x: (1.0 - x / w) ** 2 * normal_pdf(x), 0.0, w,
        epsabs=1e-15, epsrel=1e-13,
    )[0]
    variance = second - mu**2
    support_probability = 2.0 * (ndtr(w) - 0.5)
    b = amplitude * w
    exponent = d * math.exp(b * b / sigma**2) * variance**2 / (
        2.0 * sigma**4
    )
    chi2_bound = math.expm1(exponent)
    tv_bound = 0.5 * math.sqrt(max(0.0, chi2_bound))
    target_tv_from_zero = 2.0 * (ndtr(math.sqrt(d) * abs(mu) / (2.0 * sigma)) - 0.5)
    raw_query_tv_from_zero_field = -math.expm1(
        d * math.log1p(-support_probability)
    )
    return {
        "d": d,
        "w": w,
        "support_probability": support_probability,
        "support_bound_sqrt_2_over_pi_times_w": math.sqrt(2.0 / math.pi) * w,
        "coordinate_mean": mu,
        "mean_vector_norm": math.sqrt(d) * abs(mu),
        "target_gaussian_tv_from_N_zero_sigma_I": target_tv_from_zero,
        "raw_one_query_tv_from_zero_field": raw_query_tv_from_zero_field,
        "coordinate_variance": variance,
        "coordinate_centered_bound": b,
        "chi2_exponent_bound": exponent,
        "tv_bound": tv_bound,
        "asymptotic_mean_norm": amplitude / math.sqrt(2.0 * math.pi),
        "asymptotic_tv_scale_d_minus_one_quarter": d ** (-0.25),
    }


def query_bound_check(d=100, lipschitz=1.0, sigma=2.0, epsilon=0.1):
    if lipschitz == 0:
        raw = 0.0
    else:
        tau2 = 1.0 - math.exp(-2.0 * math.log1p(4.0 * epsilon**2) / d)
        raw = (lipschitz**2 / sigma**2) / math.sqrt(tau2)
    k = max(1, math.ceil(raw))

    def tv_bound(kval):
        rho = lipschitz**2 / (kval * sigma**2)
        chi2 = math.expm1(-0.5 * d * math.log1p(-rho**2))
        return 0.5 * math.sqrt(max(0.0, chi2))

    asymptotic = (lipschitz**2 / sigma**2) * math.sqrt(
        d / (8.0 * epsilon**2)
    )
    return {
        "d": d,
        "L": lipschitz,
        "sigma": sigma,
        "epsilon": epsilon,
        "continuous_threshold": raw,
        "k_min_integer": k,
        "tv_upper_at_k": tv_bound(k),
        "tv_upper_at_k_minus_1": None if k <= 1 else tv_bound(k - 1),
        "small_epsilon_large_d_asymptotic_threshold": asymptotic,
        "whole_vector_queries": k,
        "scalar_coordinate_values_read": k * d,
    }


def main():
    sigma = 1.2
    values, probs = bernoulli_centered(amplitude=0.3, probability=0.08)
    exact_chi2, numerical_chi2, quadrature_error = scalar_chi2_mixture(
        values, probs, sigma
    )
    variance = float(np.dot(probs, values**2))
    b = float(np.max(np.abs(values)))
    taylor_delta = math.exp(b * b / sigma**2) * variance**2 / (
        2.0 * sigma**4
    )

    coordinates = [
        bernoulli_centered(0.3, 0.08),
        bernoulli_centered(0.2, 0.15),
    ]
    product = math.prod(scalar_factor(v, p, sigma) for v, p in coordinates)
    enumerated = 0.0
    for states in itertools.product(*[
        list(zip(v, p)) for v, p in coordinates
    ]):
        state = [entry[0] for entry in states]
        probability = math.prod(entry[1] for entry in states)
        for states2 in itertools.product(*[
            list(zip(v, p)) for v, p in coordinates
        ]):
            state2 = [entry[0] for entry in states2]
            probability2 = math.prod(entry[1] for entry in states2)
            enumerated += probability * probability2 * math.exp(
                sum(x * y for x, y in zip(state, state2)) / sigma**2
            )

    # For Gaussian V~N(0,S), the subGaussian determinant bound is exact.
    sigma_g = 1.3
    eigenvalues = np.array([0.2, 0.4])
    gaussian_determinant = float(np.prod(
        1.0 / np.sqrt(1.0 - eigenvalues**2 / sigma_g**4)
    ))

    # Same rare scalar bump in all coordinates: marginal rarity holds, but
    # independence does not. The true chi-square explodes for this example.
    d_corr = 10_000
    w_corr = d_corr ** (-0.25)
    corr_values, corr_probs = bernoulli_centered(w_corr, w_corr)
    corr_chi2_plus_one = sum(
        pi * pj * math.exp(d_corr * vi * vj)
        for vi, pi in zip(corr_values, corr_probs)
        for vj, pj in zip(corr_values, corr_probs)
    )
    false_independent_exponent = d_corr * math.exp(w_corr**2) * (
        (w_corr**2 * w_corr * (1.0 - w_corr)) ** 2
    ) / 2.0

    result = {
        "scalar_bernoulli_identity": {
            "chi2_formula": exact_chi2,
            "chi2_density_quadrature": numerical_chi2,
            "quadrature_reported_error": quadrature_error,
            "absolute_disagreement": abs(exact_chi2 - numerical_chi2),
            "variance": variance,
            "centered_support_bound_b": b,
            "taylor_delta_upper_bound": taylor_delta,
            "taylor_bound_holds": bool(exact_chi2 <= taylor_delta),
        },
        "two_coordinate_product_identity": {
            "factorized_product": product,
            "enumerated_joint_expectation": enumerated,
            "absolute_disagreement": abs(product - enumerated),
        },
        "Gaussian_subGaussian_determinant": {
            "sigma": sigma_g,
            "S_eigenvalues": eigenvalues.tolist(),
            "spectral_condition_holds": float(np.max(eigenvalues)) < sigma_g**2,
            "chi2_plus_one_exact_and_bound": gaussian_determinant,
        },
        "generic_query_threshold": query_bound_check(),
        "zero_lipschitz_edge_case": query_bound_check(
            d=10, lipschitz=0.0, sigma=1.0, epsilon=0.1
        ),
        "independent_gradient_bump_family": [
            rare_triangular_bump(d) for d in [100, 10_000, 1_000_000]
        ],
        "correlated_marginal_counterexample": {
            "d": d_corr,
            "w": w_corr,
            "each_coordinate_is_rare_and_bounded": True,
            "coordinates_independent": False,
            "exact_chi2_plus_one": corr_chi2_plus_one,
            "log_exact_chi2_plus_one": math.log(corr_chi2_plus_one),
            "what_false_independence_formula_would_bound_in_exponent":
                false_independent_exponent,
            "mean_vector_norm": math.sqrt(d_corr) * w_corr**2,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
