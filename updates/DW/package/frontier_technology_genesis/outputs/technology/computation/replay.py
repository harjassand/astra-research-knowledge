#!/usr/bin/env python3
"""Model-relative checks for independently prethermalized capacitor assembly.

Uses NumPy only. No circuit/hardware performance is measured here.
Output: replay.json in this script's directory.
"""
import json
from pathlib import Path
import numpy as np


def sympower(a, exponent):
    w, u = np.linalg.eigh((a + a.T) / 2)
    if min(w) <= 0:
        raise ValueError("positive definite matrix required")
    return (u * w**exponent) @ u.T


def build(n, edges, cg=0.1, ce=1.0, cp=0.01, g=1.0):
    # One central grounded capacitor per computational node; one isolated
    # two-plate capacitor for each edge, with explicit grounded parasitics.
    size = n + 2 * len(edges)
    c0 = np.zeros((size, size))
    c0[:n, :n] = cg * np.eye(n)
    merger = np.zeros((size, size))
    j = np.zeros((size, n))
    j[:n, :] = np.eye(n)
    for k, (a, b) in enumerate(edges):
        l, r = n + 2*k, n + 2*k+1
        c0[np.ix_([l, r], [l, r])] = [[ce+cp, -ce], [-ce, ce+cp]]
        for leaf, center in [(l, a), (r, b)]:
            j[leaf, center] = 1.0
            merger[leaf, leaf] += g
            merger[center, center] += g
            merger[leaf, center] -= g
            merger[center, leaf] -= g
    p = np.eye(size)[:n]
    c = j.T @ c0 @ j
    return c0, merger, j, p, c


def check(name, n, edges, cg=0.1, ce=1, cp=0.01):
    c0, merger, j, p, c = build(n, edges, cg, ce, cp)
    cinv = np.linalg.inv(c)
    c0is = sympower(c0, -0.5)
    h = c0is @ merger @ c0is
    ev, u = np.linalg.eigh((h+h.T)/2)
    pos = ev > 1e-8
    if sum(~pos) != n:
        raise AssertionError("wrong conserved-subspace dimension")
    read = p @ c0is @ u
    slow = read[:, ~pos] @ read[:, ~pos].T
    exact_projection_error = np.linalg.norm(cinv-slow)/np.linalg.norm(cinv)
    croot = sympower(c, 0.5)
    integ = (read[:, pos] / ev[pos]) @ read[:, pos].T
    relative_integral = croot @ integ @ croot
    worst_integral = float(max(np.linalg.eigvalsh(relative_integral)))
    cblock = 2*ce+cp
    rate_bound = 1/cblock
    if min(ev[pos]) < rate_bound * (1-1e-8):
        raise AssertionError("assembly spectral bound failed")
    if worst_integral > cblock * (1+1e-8):
        raise AssertionError("integrated noise bound failed")
    windows = []
    for window in [2, 10, 40, 200]:
        x = ev[pos]*window
        f = 2*(x + np.expm1(-x))/(x*x)
        excess = (read[:, pos] * f) @ read[:, pos].T
        relative = croot @ excess @ croot
        windows.append({
            "W_in_R_times_ce": window,
            "worst_relative_excess_covariance": float(max(np.linalg.eigvalsh(relative))),
            "proved_upper_bound": 2*cblock/window,
        })
    eigen_c = np.linalg.eigvalsh(c)
    # Fair conductance matching: all expanded plate reset switches can be on
    # in parallel. Give the direct n-node RC sampler equal total conductance.
    total_g = c0.shape[0]
    g_per_direct_node = total_g/n
    lag_goal = 0.01
    direct_lag = max(eigen_c)/g_per_direct_node*np.log(1/lag_goal)
    quench_reset = max(np.linalg.eigvalsh(c0))*np.log(1/lag_goal)
    return {
        "graph": name,
        "n": n,
        "m": len(edges),
        "expanded_plates": c0.shape[0],
        "target_condition_number": float(max(eigen_c)/min(eigen_c)),
        "projection_identity_relative_error": float(exact_projection_error),
        "merger_min_nonzero_decay_rate": float(min(ev[pos])),
        "proved_rate_lower_bound": rate_bound,
        "relative_integrated_fast_noise": worst_integral,
        "proved_integrated_upper_bound": cblock,
        "readout_windows": windows,
        "matched_direct_RC_1percent_canonical_correlation_lag": float(direct_lag),
        "quench_local_reset_1percent_lag_before_readout": float(quench_reset),
    }


def rank_one_trials():
    rng = np.random.default_rng(11012)
    n = 12
    edges = [(i, i+1) for i in range(n-1)]
    _, _, _, _, c = build(n, edges)
    mean = rng.normal(size=n)*0.1
    v = mean[:, None] + np.linalg.cholesky(np.linalg.inv(c)) @ rng.normal(size=(n, 200000))
    a = np.zeros(n)
    a[2], a[8] = 1, -1
    alpha = 0.7
    y = 0.35
    cnew = c + alpha*np.outer(a,a)
    hnew = c @ mean + alpha*a*y
    eta = alpha*y + np.sqrt(alpha)*rng.normal(size=v.shape[1])
    updated = np.linalg.solve(cnew, c@v+a[:,None]*eta)
    actual_mean = np.mean(updated, axis=1)
    exact_mean = np.linalg.solve(cnew, hnew)
    actual_cov = np.cov(updated)
    exact_cov = np.linalg.inv(cnew)
    cr = sympower(cnew, 0.5)
    white_error = cr @ (actual_cov-exact_cov) @ cr
    # Deterministic identity is stronger than finite Monte Carlo evidence.
    transform = np.linalg.solve(cnew, c)
    gain = np.linalg.solve(cnew, a)
    identity_cov = transform @ np.linalg.inv(c) @ transform.T + alpha*np.outer(gain,gain)
    return {
        "samples": v.shape[1],
        "max_whitened_empirical_covariance_error": float(max(abs(np.linalg.eigvalsh(white_error)))),
        "empirical_mean_L2_error": float(np.linalg.norm(actual_mean-exact_mean)),
        "covariance_identity_relative_error": float(np.linalg.norm(identity_cov-exact_cov)/np.linalg.norm(exact_cov)),
        "qualification": "Fixed/exogenous observation; does not establish conditional correctness for adaptive data or circuit feasibility.",
    }


def main():
    grid_side = 5
    grid = []
    for i in range(grid_side):
        for j in range(grid_side):
            a = i*grid_side+j
            if i+1 < grid_side:
                grid.append((a, a+grid_side))
            if j+1 < grid_side:
                grid.append((a, a+1))
    data = {
        "evidence_scope": "Double-precision circuit-model linear algebra and fixed-seed Gaussian Monte Carlo; no hardware, SPICE, measured joules, or novelty certification.",
        "units": "Capacitance normalized to edge ce=1; resistance normalized R=1; thermal energy normalized kT=1.",
        "graphs": [
            check("path", 16, [(i,i+1) for i in range(15)]),
            check("grid_5x5", 25, grid),
            check("complete", 12, [(i,j) for i in range(12) for j in range(i+1,12)]),
            check("path_smaller_ground", 16, [(i,i+1) for i in range(15)], cg=0.001, cp=0.0001),
        ],
        "rank_one_insertion": rank_one_trials(),
    }
    dest = Path(__file__).with_name("replay.json")
    dest.write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
