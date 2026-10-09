#!/usr/bin/env python3
"""Finite diagnostics for A17 v1. These checks do not prove the theorem."""

import math
import numpy as np


def rr_prob_from_counts(n0, n1, eps):
    e = math.exp(eps)
    r = e / (e + 2.0)
    s = 1.0 / (e + 2.0)
    if n0 + n1 == 0:
        z = np.array([1.0, 0.0, 0.0])  # empty, control, treatment
    else:
        k = n0 + n1
        z = np.array([0.0, n0 / k, n1 / k])
    channel = np.full((3, 3), s)
    np.fill_diagonal(channel, r)
    return z @ channel


def check_local_privacy(eps):
    records = [(a, b) for a in range(6) for b in range(6)]
    laws = [rr_prob_from_counts(a, b, eps) for a, b in records]
    max_ratio = 0.0
    for p in laws:
        for q in laws:
            max_ratio = max(max_ratio, float(np.max(p / q)))
    return max_ratio


def run_simulation(seed=20171009, n=150_000, reps=80, eps=0.8, rho=0.5, delta=0.05):
    rng = np.random.default_rng(seed)
    e = math.exp(eps)
    r = e / (e + 2.0)
    s = 1.0 / (e + 2.0)
    c = r - s
    B = 1.0
    uB = math.tanh(B / 2.0)
    errors = []
    covered = 0
    min_q = 1.0

    for _ in range(reps):
        # Pareto shape < 1 gives E[Lambda_0]=infinity. Beta_i is heterogeneous.
        u = np.maximum(rng.random(n), np.finfo(float).tiny)
        lam0 = 0.2 / np.power(u, 1.0 / 0.8)
        beta = np.where(rng.random(n) < 0.35, 0.6, -0.3)
        lam1 = lam0 * np.exp(beta)
        q_i = -np.expm1(-(lam0 + lam1))
        p_i = lam1 / (lam0 + lam1)
        q = float(q_i.mean())
        p_star = float(np.mean(q_i * p_i) / q)
        beta_star = math.log(p_star / (1.0 - p_star))
        min_q = min(min_q, q)

        n0 = rng.poisson(lam0)
        n1 = rng.poisson(lam1)
        k = n0 + n1
        z = np.zeros(n, dtype=np.int8)  # empty
        positive = k > 0
        choose_treated = np.zeros(n, dtype=np.int8)
        choose_treated[positive] = rng.binomial(
            1, n1[positive] / k[positive]
        )
        z[positive] = np.where(choose_treated[positive] == 1, 2, 1)

        # Ternary randomized response: report truth with r, otherwise one of
        # the other categories uniformly, each with probability s.
        report = z.copy()
        flip = rng.random(n) >= r
        offset = rng.integers(1, 3, size=n)
        report[flip] = (z[flip] + offset[flip]) % 3
        count_t = int(np.count_nonzero(report == 2))
        count_c = int(np.count_nonzero(report == 1))
        A = count_t - count_c
        D = count_t + count_c - 2.0 * n * s
        if D > 0:
            uhat = float(np.clip(A / D, -uB, uB))
        else:
            uhat = 0.0
        betahat = 2.0 * math.atanh(uhat)
        errors.append(abs(betahat - beta_star))

        # Check the theorem's conservative, data-independent confidence radius.
        L = math.log(4.0 / delta)
        t0 = math.sqrt(2.0 * n * L) + (2.0 / 3.0) * L
        if n * c * rho >= 2.0 * t0:
            radius = 8.0 * t0 / (n * c * rho * (1.0 - uB * uB))
            if abs(betahat - beta_star) <= radius:
                covered += 1

    L = math.log(4.0 / delta)
    t0 = math.sqrt(2.0 * n * L) + (2.0 / 3.0) * L
    condition = n * c * rho >= 2.0 * t0
    return {
        "n": n,
        "repetitions": reps,
        "epsilon": eps,
        "rho_lower_bound": rho,
        "minimum_empirical_q": min_q,
        "privacy_signal_c": c,
        "theorem_condition_holds": condition,
        "empirical_95pct_coverage_of_conservative_interval": covered / reps if condition else None,
        "median_absolute_beta_error": float(np.median(errors)),
        "p90_absolute_beta_error": float(np.quantile(errors, 0.90)),
        "median_error_bound_ratio": float(np.median(errors) / (8.0 * t0 / (n * c * rho * (1.0 - uB * uB)))) if condition else None,
        "pareto_shape": 0.8,
        "pareto_mean_is_infinite": True,
    }


if __name__ == "__main__":
    eps = 0.8
    print({"finite_grid_max_likelihood_ratio": check_local_privacy(eps),
           "target_epsilon_ratio": math.exp(eps)})
    print(run_simulation())
