"""Finite-chain checks of the new ordering inequality; not a universal proof."""
import json
import math
import time
from pathlib import Path

import numpy as np

START = time.perf_counter()
OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(20261021)
tol = 2e-7
metrics = {
    "seed": 20261021,
    "chains": 0,
    "threshold_time_checks": 0,
    "nonvacuous_checks": 0,
    "positive_tv_checks": 0,
    "max_tv": 0.0,
    "max_tv_to_bound": 0.0,
    "max_stationarity_residual": 0.0,
    "max_detailed_balance_residual": 0.0,
    "max_positive_violation": {},
    "tolerance": tol,
}


def check(name, actual, bound):
    violation = float(actual - bound)
    metrics["max_positive_violation"][name] = max(
        0.0, violation, metrics["max_positive_violation"].get(name, 0.0)
    )
    if violation > tol * max(1.0, abs(bound)):
        raise AssertionError((name, actual, bound, violation))


def softmax(x):
    x = np.exp(x - np.max(x))
    return x / x.sum()


for case in range(180):
    n = int(rng.integers(3, 11))
    logpi = -rng.exponential(3 if case % 3 else 1, size=n)
    pi = softmax(logpi)
    q = softmax(logpi + rng.normal(0, 6 if case % 3 else 2, size=n))
    W = pi / q
    proposal = rng.random((n, n))
    proposal = (proposal + proposal.T) / 2
    np.fill_diagonal(proposal, 0)
    proposal *= rng.uniform(0.3, 1.0) / proposal.sum(axis=1).max()
    L = proposal * np.minimum(1, pi[None, :] / pi[:, None])
    np.fill_diagonal(L, 1 - L.sum(axis=1))
    G = q[None, :] * np.minimum(1, W[None, :] / W[:, None])
    np.fill_diagonal(G, 0)
    np.fill_diagonal(G, 1 - G.sum(axis=1))
    alpha = float(rng.uniform(0.05, 0.95))
    beta = 1 - alpha
    H = alpha * G + beta * L
    C = (np.eye(n) + H) / 2
    db = np.max(np.abs(pi[:, None] * C - (pi[:, None] * C).T))
    stat = np.max(np.abs(pi @ C - pi))
    metrics["max_detailed_balance_residual"] = max(
        metrics["max_detailed_balance_residual"], float(db))
    metrics["max_stationarity_residual"] = max(
        metrics["max_stationarity_residual"], float(stat))
    assert db < 1e-12 and stat < 1e-12
    order = np.argsort(W)
    median_weight = W[order[np.searchsorted(np.cumsum(pi[order]), 0.5)]]
    M = float(max(math.e, median_weight * (1 + 1e-12)))
    anchor = W <= M
    s0 = float(pi[anchor].sum())
    assert s0 >= 0.5 - 1e-14
    metrics["chains"] += 1

    for t in [0, 1, 2, 5, 20, 100, 1000, 10000, 100000]:
        Ct = np.linalg.matrix_power(C, t)
        error = q @ Ct - pi
        tv = float(np.abs(error).sum() / 2)
        f = (error > 0).astype(float)
        g = Ct @ f
        # Minor floating-point row-sum drift is covered by the stated tolerance.
        m = float(pi[anchor] @ g[anchor] / s0)
        eta = math.exp(math.lgamma(t + 1) - math.lgamma(t // 2 + 1)
                       - math.lgamma(t - t // 2 + 1) - t * math.log(2))
        check("near_harmonic", np.max(np.abs(g - H @ g)), eta)
        metrics["max_tv"] = max(metrics["max_tv"], tv)

        for threshold in [math.e + 1, 10.0, 100.0]:
            B = R = threshold
            low, high = W < 1 / B, W > R
            core = ~(low | high)
            b = float(q[low].sum())
            a = float(pi[high].sum())
            u = float((q[low] - pi[low]).sum())
            v = float((pi[high] - q[high]).sum())
            U = M * (B + 1) + R
            delta = math.sqrt(U / (alpha * s0 * (2 * t + 1)))
            qg = float(q @ g)
            if low.any():
                check("low_tail_global_redraw", np.max(np.abs((G @ g)[low] - qg)), b)
            check("common_scalar", abs(qg - m), b + a / R + delta)
            core_term = float((q[core] - pi[core]) @ (g[core] - m))
            check("core", abs(core_term), delta)
            theta = alpha * (2 * b + a / R + delta) + eta
            outside_term = float((q[~core] - pi[~core]) @ (g[~core] - m))
            check("signed_tail", abs(outside_term), max(beta * u, v) + u * theta)
            bound = (max(a, beta * b) + 2 * alpha * b * b + alpha * a * b / R
                     + (1 + alpha * b) * delta + b * eta)
            check("final_tv", tv, bound)
            metrics["threshold_time_checks"] += 1
            metrics["nonvacuous_checks"] += int(bound < 1)
            metrics["positive_tv_checks"] += int(tv > 1e-4 and bound < 1)
            ratio = tv / bound
            if ratio > metrics["max_tv_to_bound"]:
                metrics["max_tv_to_bound"] = ratio
                metrics["largest_ratio_case"] = {
                    "case": case, "n": n, "t": t, "B": B, "R": R,
                    "alpha": alpha, "tv": tv, "bound": bound, "a": a, "b": b,
                    "delta": delta,
                    "K_actual": float(pi @ np.log(pi / q)),
                    "J_actual": float(q @ np.log(q / pi)),
                }

metrics["elapsed_seconds"] = time.perf_counter() - START
metrics["result"] = "All checks passed. Numerical evidence only; proof is in RESULT.txt."
(OUT / "numerical_checks.json").write_text(json.dumps(metrics, indent=2) + "\n")
print(json.dumps(metrics, indent=2))
