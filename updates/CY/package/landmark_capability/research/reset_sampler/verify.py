#!/usr/bin/env python3
"""Finite check of the additive-hazard, product-reset resolvent construction.

All model inputs below are terminating decimals (hence rational).  The
product-integral path never constructs the 2**n state generator; the dense
matrix is built separately as a small-instance reference.  This is a
floating-point identity check, not a certified implementation of RESULT.txt.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss


# The fourth coordinate is omitted in the three-coordinate fixture.  Every
# local chain, reset law, and hazard is heterogeneous.  A channel's hazard is
# the sum of its local entries; a firing redraws *all* coordinates jointly
# from the channel's product law.
INPUT = {
    "flip_up": ["0.35", "0.50", "0.20", "0.65"],
    "flip_down": ["0.80", "1.10", "0.60", "0.40"],
    "hazards": [
        [["0.10", "0.35"], ["0.20", "0.05"], ["0.05", "0.25"], ["0.12", "0.08"]],
        [["0.16", "0.03"], ["0.04", "0.19"], ["0.21", "0.06"], ["0.03", "0.18"]],
    ],
    "reset_one_prob": [
        ["0.85", "0.75", "0.90", "0.65"],
        ["0.15", "0.25", "0.35", "0.10"],
    ],
    "initial_one_prob": ["0.60", "0.20", "0.55", "0.30"],
}


def make_model(n: int) -> dict:
    q = []
    for up, down in zip(INPUT["flip_up"][:n], INPUT["flip_down"][:n]):
        u, d = float(up), float(down)
        q.append(np.array([[-u, u], [d, -d]], dtype=float))
    hazards = np.asarray(INPUT["hazards"], dtype=float)[:, :n, :]
    reset = np.asarray(INPUT["reset_one_prob"], dtype=float)[:, :n]
    initial = np.asarray(INPUT["initial_one_prob"], dtype=float)[:n]
    nu = np.stack([np.stack([1.0 - p, p], axis=-1) for p in reset])
    mu = np.stack([1.0 - initial, initial], axis=-1)
    local_killed = [q[i] - np.diag(np.sum(hazards[:, i, :], axis=0)) for i in range(n)]
    base_pi_one = np.array(
        [float(INPUT["flip_up"][i]) / (float(INPUT["flip_up"][i]) + float(INPUT["flip_down"][i]))
         for i in range(n)]
    )
    return dict(n=n, q=q, hazards=hazards, nu=nu, mu=mu,
                local_killed=local_killed, base_pi_one=base_pi_one)


def binary_exponential_data(a: np.ndarray) -> tuple:
    """Real spectral projectors for an irreducible killed binary generator."""
    disc = np.sqrt((a[0, 0] - a[1, 1]) ** 2 + 4.0 * a[0, 1] * a[1, 0])
    lam_plus = (np.trace(a) + disc) / 2.0
    lam_minus = (np.trace(a) - disc) / 2.0
    p_plus = (a - lam_minus * np.eye(2)) / disc
    p_minus = np.eye(2) - p_plus
    return lam_plus, lam_minus, p_plus, p_minus


def binary_exponential(data: tuple, t: float) -> np.ndarray:
    lp, lm, pp, pm = data
    return np.exp(lp * t) * pp + np.exp(lm * t) * pm


def product_probability(local_laws: np.ndarray, state: tuple[int, ...]) -> float:
    return float(np.prod([local_laws[i, x] for i, x in enumerate(state)]))


def dense_reference(model: dict) -> dict:
    n = model["n"]
    states = list(itertools.product(range(2), repeat=n))
    index = {x: j for j, x in enumerate(states)}
    dimension = 2**n
    q0 = np.zeros((dimension, dimension))
    u = np.zeros((dimension, 2))
    v = np.zeros((2, dimension))
    mu = np.zeros(dimension)
    pi0 = np.zeros(dimension)
    for row, x in enumerate(states):
        for i in range(n):
            y = list(x)
            y[i] = 1 - y[i]
            rate = model["q"][i][x[i], y[i]]
            q0[row, index[tuple(y)]] += rate
            q0[row, row] -= rate
        for channel in range(2):
            u[row, channel] = sum(model["hazards"][channel, i, x[i]] for i in range(n))
        mu[row] = product_probability(model["mu"], x)
        pi0[row] = float(np.prod([
            model["base_pi_one"][i] if x[i] else 1 - model["base_pi_one"][i]
            for i in range(n)
        ]))
        for channel in range(2):
            v[channel, row] = product_probability(model["nu"][channel], x)
    killed = q0 - np.diag(np.sum(u, axis=1))
    q = killed + u @ v
    # Two independent observables: a rare full-cylinder indicator and a
    # genuinely additive statistic.  Both have product-sum descriptions.
    g = np.stack([np.array([float(all(x)) for x in states]),
                  np.array([sum(x) / n for x in states])], axis=1)
    stat_system = q.T.copy()
    stat_rhs = np.zeros(dimension)
    stat_system[-1, :] = 1.0
    stat_rhs[-1] = 1.0
    pi = np.linalg.solve(stat_system, stat_rhs)
    moments = np.array([sum(pi[j] * x[i] for j, x in enumerate(states)) for i in range(n)])
    covariance_01 = sum(pi[j] * x[0] * x[1] for j, x in enumerate(states)) - moments[0] * moments[1]
    return dict(q=q, q0=q0, killed=killed, u=u, v=v, mu=mu, pi=pi, pi0=pi0,
                g=g, states=states, stationary=pi @ g, base_stationary=pi0 @ g,
                moments=moments, covariance_01=covariance_01,
                row_sum_error=float(np.max(np.abs(q @ np.ones(dimension)))))


def product_integrands(model: dict, heat: list[np.ndarray]) -> np.ndarray:
    """Rows mu, nu_1, nu_2; columns U_1, U_2, g_cylinder, g_activity."""
    n = model["n"]
    out = np.zeros((3, 4))
    for row, local_laws in enumerate([model["mu"], *model["nu"]]):
        propagated = np.stack([local_laws[i] @ heat[i] for i in range(n)])
        survival = np.sum(propagated, axis=1)
        for channel in range(2):
            parts = np.array([
                propagated[i] @ model["hazards"][channel, i] for i in range(n)
            ])
            out[row, channel] = sum(
                parts[i] * np.prod(np.delete(survival, i)) for i in range(n)
            )
        out[row, 2] = np.prod(propagated[:, 1])
        out[row, 3] = sum(
            propagated[i, 1] * np.prod(np.delete(survival, i)) / n
            for i in range(n)
        )
    return out


def product_integrals(model: dict, s: float, quadrature_order: int = 40,
                      tmax: float = 128.0) -> tuple[np.ndarray, int, float]:
    """Integrate e^{-st} times the product contractions on dyadic intervals."""
    nodes, weights = leggauss(quadrature_order)
    intervals = [(0.0, 1.0)]
    left = 1.0
    while left < tmax:
        right = min(2.0 * left, tmax)
        intervals.append((left, right))
        left = right
    exp_data = [binary_exponential_data(a) for a in model["local_killed"]]
    integral = np.zeros((3, 4))
    for left, right in intervals:
        scale = (right - left) / 2.0
        centre = (left + right) / 2.0
        for x, w in zip(nodes, weights):
            t = centre + scale * x
            heat = [binary_exponential(data, t) for data in exp_data]
            integral += scale * w * np.exp(-s * t) * product_integrands(model, heat)
    # Killing has a simple positive lower bound: for each local coordinate,
    # its total channel hazard is at least the minimum over its two states.
    amin = sum(np.min(np.sum(model["hazards"][:, i, :], axis=0)) for i in range(model["n"]))
    # For the tested contractions, |g|<=1 and 0<=a_l<=amax.  The maximum
    # omitted tail is bounded by max(1,amax)*e^{-(s+amin)T}/(s+amin).
    amax = max(sum(np.max(model["hazards"][channel, i]) for i in range(model["n"]))
               for channel in range(2))
    tail_bound = max(1.0, amax) * np.exp(-(s + amin) * tmax) / (s + amin)
    return integral, len(intervals) * quadrature_order, float(tail_bound)


def product_response(integrals: np.ndarray, s: float) -> tuple[np.ndarray, np.ndarray, float]:
    # Integral row 0 is mu; rows 1:3 are nu_1,nu_2.  Columns 0:2 are U.
    m = integrals[1:, :2]
    j = np.eye(2) - m
    response = s * (integrals[0, 2:] + integrals[0, :2] @
                    np.linalg.solve(j, integrals[1:, 2:]))
    return response, j, float(np.linalg.cond(j, np.inf))


def run_case(n: int) -> dict:
    model = make_model(n)
    dense = dense_reference(model)
    cases = []
    for s in [0.1, 0.01, 0.001, 0.0001]:
        integrals, node_count, tail_bound = product_integrals(model, s)
        product_value, j, cond = product_response(integrals, s)
        dense_value = s * dense["mu"] @ np.linalg.solve(s * np.eye(2**n) - dense["q"], dense["g"])
        cases.append({
            "s": s,
            "product_abel": product_value.tolist(),
            "dense_abel": dense_value.tolist(),
            "max_product_vs_dense_resolvent_error": float(np.max(np.abs(product_value - dense_value))),
            "max_abel_vs_stationary_bias": float(np.max(np.abs(product_value - dense["stationary"]))),
            "woodbury_small_matrix": j.tolist(),
            "woodbury_inf_condition": cond,
            "quadrature_nodes": node_count,
            "absolute_integrand_tail_bound": tail_bound,
        })
    return {
        "n": n,
        "dense_state_count": 2**n,
        "stationary_observables_cylinder_activity": dense["stationary"].tolist(),
        "independent_base_stationary_observables": dense["base_stationary"].tolist(),
        "reset_stationary_bit_marginals": dense["moments"].tolist(),
        "reset_stationary_covariance_bits_0_1": float(dense["covariance_01"]),
        "dense_generator_max_row_sum_error": dense["row_sum_error"],
        "total_variation_to_independent_base_stationary": float(np.sum(np.abs(dense["pi"] - dense["pi0"])) / 2.0),
        "cases": cases,
    }


def main() -> None:
    cases = [run_case(3), run_case(4)]
    for case in cases:
        assert case["dense_generator_max_row_sum_error"] < 1e-12
        assert case["total_variation_to_independent_base_stationary"] > 0.1
        assert case["reset_stationary_covariance_bits_0_1"] > 0.01
        assert max(entry["max_product_vs_dense_resolvent_error"]
                   for entry in case["cases"]) < 1e-9
        assert case["cases"][-1]["max_abel_vs_stationary_bias"] < 1e-5
    receipt = {
        "purpose": "finite floating-point check of product killed-heat plus two-channel Woodbury steady response",
        "reproduce": "python3 work/reset_sampler/verify.py",
        "python_version": sys.version.split()[0],
        "numpy_version": np.__version__,
        "input": INPUT,
        "observables": ["all coordinates equal one", "mean of coordinate bits"],
        "quadrature": {"order_per_interval": 40, "intervals": "[0,1],[1,2],...,[64,128]", "tmax": 128},
        "cases": cases,
        "validation": {
            "max_dense_generator_row_sum_error": max(c["dense_generator_max_row_sum_error"] for c in cases),
            "max_product_vs_dense_resolvent_error": max(
                e["max_product_vs_dense_resolvent_error"] for c in cases for e in c["cases"]
            ),
            "checks_passed": True,
        },
        "scope": "finite numerical identity checks only; no certificate of the polynomial-bit theorem or exact sampling claim",
    }
    path = Path(__file__).with_name("verify_receipt.json")
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    for case in receipt["cases"]:
        max_identity_error = max(entry["max_product_vs_dense_resolvent_error"] for entry in case["cases"])
        print(f"n={case['n']} states={case['dense_state_count']} "
              f"stationary={case['stationary_observables_cylinder_activity']} "
              f"corr01={case['reset_stationary_covariance_bits_0_1']:.6g} "
              f"max_identity_error={max_identity_error:.3g}")
    print(path)


if __name__ == "__main__":
    main()
