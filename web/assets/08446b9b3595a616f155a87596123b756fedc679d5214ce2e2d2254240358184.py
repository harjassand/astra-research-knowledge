#!/usr/bin/env python3
"""Small-N numerical replay for the range-2 hard-core-boson candidate.

This is explicitly a floating-point diagnostic, not an interval certificate.
It checks N=2,...,8, sector min-max ordering, archive tails, the relative-
entropy/free-reference bound, conditional-sector decoder error, and the stable
elementary-symmetric-polynomial recurrence against brute force.
"""
from __future__ import annotations

import itertools
import json
import math
import platform
import time
from pathlib import Path

import numpy as np


J = 1.0
TAU = 0.2
B = 0.5
V = 1.0
LAM = 0.25
TOL = 2.0e-9


def masks_of_weight(n: int, m: int) -> list[int]:
    return [sum(1 << i for i in c) for c in itertools.combinations(range(n), m)]


def sector_matrices(n: int, m: int, jval: float, vval: float):
    """Return free K0=hop+4JM and W in the computational sector basis."""
    states = masks_of_weight(n, m)
    index = {x: a for a, x in enumerate(states)}
    k0 = np.eye(len(states), dtype=float) * (4.0 * jval * m)
    w = np.zeros_like(k0)
    for col, x in enumerate(states):
        w[col, col] = vval * sum(
            ((x >> i) & 1) * ((x >> (i + 2)) & 1)
            for i in range(max(0, n - 2))
        )
        for i in range(n - 1):
            if ((x >> i) & 1) != ((x >> (i + 1)) & 1):
                y = x ^ (1 << i) ^ (1 << (i + 1))
                row = index[y]
                k0[row, col] += -2.0 * jval
    assert np.allclose(k0, k0.T, atol=1e-13)
    return states, k0, w


def canonical(k: np.ndarray, beta: float) -> tuple[float, np.ndarray, np.ndarray, np.ndarray]:
    vals, vecs = np.linalg.eigh(k)
    shift = float(vals[0])
    ew = np.exp(-beta * (vals - shift))
    zshift = float(np.sum(ew))
    rho = (vecs * (ew / zshift)) @ vecs.T
    logz = -beta * shift + math.log(zshift)
    return logz, rho, vals, vecs


def trace_distance(a: np.ndarray, b: np.ndarray) -> float:
    vals = np.linalg.eigvalsh((a - b + (a - b).T) * 0.5)
    return 0.5 * float(np.sum(np.abs(vals)))


def stable_esym_dp(weights: list[float], m: int) -> float:
    """Unshifted tiny-N reference DP for e_m(weights), used only diagnostically."""
    dp = [0.0] * (m + 1)
    dp[0] = 1.0
    used = 0
    for w in weights:
        used += 1
        for j in range(min(m, used), 0, -1):
            dp[j] += w * dp[j - 1]
    return dp[m]


def shifted_esym_dp(energies: list[float], beta: float, m: int) -> float:
    """F[0,m] from the shifted recurrence, bounded between 1 and binomial(N,m)."""
    n = len(energies)
    # F[i][j] is defined only when 0<=j<=n-i; impossible entries are zero.
    f = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        f[i][0] = 1.0
    for i in range(n - 1, -1, -1):
        maxj = min(m, n - i)
        for j in range(1, maxj + 1):
            include = f[i + 1][j - 1]
            if j <= n - i - 1:
                skip = math.exp(-beta * (energies[i + j] - energies[i])) * f[i + 1][j]
            else:
                skip = 0.0
            f[i][j] = include + skip
    return f[0][m]


def cstar(jval: float, tau: float, bval: float, cutoff: int = 80) -> float:
    total = 0.0
    for k in range(1, cutoff + 1):
        for ell in range(k + 1, cutoff + 1):
            total += (k * k + ell * ell) * math.exp(-8.0 * tau * jval * (k * k + ell * ell))
    return 32.0 * math.pi**2 * math.exp(2.0 * tau * bval) * total


def run_case(n: int) -> dict:
    case_started = time.perf_counter()
    ell = n + 1
    beta = TAU * ell * ell
    sectors = []
    total_logz_v_terms = []
    total_logz_0_terms = []
    per_sector = []
    avg_w_v = 0.0
    q_v_raw = []
    q_0_raw = []
    min_eig_gap = float("inf")
    for m in range(n + 1):
        states, k0, w = sector_matrices(n, m, J, V)
        kv = k0 + w
        ev0 = np.linalg.eigvalsh(k0)
        evv = np.linalg.eigvalsh(kv)
        gap = float(np.min(evv - ev0))
        min_eig_gap = min(min_eig_gap, gap)
        lv0, rho0, _, _ = canonical(k0, beta)
        lvv, rhov, _, _ = canonical(kv, beta)
        logterm0 = TAU * LAM * m + lv0
        logtermv = TAU * LAM * m + lvv
        total_logz_0_terms.append(logterm0)
        total_logz_v_terms.append(logtermv)
        q_0_raw.append(logterm0)
        q_v_raw.append(logtermv)
        avg_w_v += math.exp(logtermv) * float(np.trace(rhov @ w)) if logtermv < 700 else 0.0
        sectors.append((m, states, k0, w, rho0, rhov, logterm0, logtermv))
        per_sector.append({"m": m, "dimension": len(states), "min_eigenvalue_gap": gap})

    def normalize_logs(xs):
        z = max(xs)
        vals = np.exp(np.asarray(xs) - z)
        return vals / vals.sum(), z + math.log(float(vals.sum()))

    q0, logz0 = normalize_logs(q_0_raw)
    qv, logzv = normalize_logs(q_v_raw)
    # Recompute <W>_V under normalized sector probabilities.
    avg_w_v = 0.0
    avg_w_0 = 0.0
    qclass_kl = 0.0
    conditional_kl = 0.0
    global_t = 0.0
    weighted_conditional_t = 0.0
    blocks = []
    for m, states, k0, w, rho0, rhov, logterm0, logtermv in sectors:
        avg_w_v += qv[m] * float(np.trace(rhov @ w))
        avg_w_0 += q0[m] * float(np.trace(rho0 @ w))
        if qv[m] > 0:
            qclass_kl += qv[m] * math.log(qv[m] / q0[m])
        # This closed form is stable and exact for the two Gibbs matrices;
        # directly diagonalizing log(rho) is badly conditioned in rare sectors.
        dcond = -beta * float(np.trace(rhov @ w)) + sectors[m][6] - sectors[m][7]
        conditional_kl += qv[m] * max(0.0, dcond)
        tc = trace_distance(rhov, rho0)
        weighted_conditional_t += qv[m] * tc
        global_t += trace_distance(qv[m] * rhov, q0[m] * rho0)
        blocks.append({"m": m, "qV": float(qv[m]), "q0": float(q0[m]),
                       "conditional_relative_entropy": dcond,
                       "conditional_trace_distance": tc})

    dtotal_formula = -beta * avg_w_v + logz0 - logzv
    dtotal_chain = qclass_kl + conditional_kl
    cst = cstar(J, TAU, B)
    delta_bound = math.sqrt(TAU * V * cst / (2.0 * ell))
    full_dim = 1 << n
    rho_v_full = np.zeros((full_dim, full_dim), dtype=float)
    for m, states, k0, w, rho0, rhov, logterm0, logtermv in sectors:
        for r, x in enumerate(states):
            for s, y in enumerate(states):
                rho_v_full[x, y] = qv[m] * rhov[r, s]
    cutoff_results = []
    for d in range(1, n + 1):
        tail = float(np.sum(qv[d:]))
        conditional_prefix = sum(qv[m] * trace_distance(sectors[m][5], sectors[m][4])
                                 for m in range(d))
        dec_error = tail + conditional_prefix
        exact_archive = np.zeros_like(rho_v_full)
        free_archive = np.zeros_like(rho_v_full)
        for m in range(d):
            states = sectors[m][1]
            rho0, rhov = sectors[m][4], sectors[m][5]
            for r, x in enumerate(states):
                for s, y in enumerate(states):
                    exact_archive[x, y] = qv[m] * rhov[r, s]
                    free_archive[x, y] = qv[m] * rho0[r, s]
        exact_archive[0, 0] += tail
        free_archive[0, 0] += tail
        exact_archive_error = trace_distance(rho_v_full, exact_archive)
        free_archive_error = trace_distance(rho_v_full, free_archive)
        s = TAU * 8.0 * J * d * d / 4.0
        energies = [4.0 * J * ell * ell * (1.0 - math.cos(math.pi * k / ell))
                    for k in range(1, n + 1)]
        log_chernoff = -s * d + sum(float(np.logaddexp(0.0, s + TAU * B - TAU * a))
                                    for a in energies)
        cutoff_results.append({"d": d, "tail_probability": tail,
                               "free_sector_decoder_error": dec_error,
                               "free_sector_decoder_matrix_trace_distance": free_archive_error,
                               "exact_archive_matrix_trace_distance": exact_archive_error,
                               "exact_archive_tail_identity_abs_error": abs(exact_archive_error - tail),
                               "tail_plus_relative_entropy_bound": tail + delta_bound,
                               "log_chernoff_bound": log_chernoff,
                               "tail_le_chernoff": math.log(max(tail, 1e-300)) <= log_chernoff + 1e-10})

    energies = [4.0 * J * ell * ell * (1.0 - math.cos(math.pi * k / ell))
                for k in range(1, n + 1)]
    # Check the shifted DP exactly against a brute-force floating sum on a subset of m.
    dp_checks = []
    weights = [math.exp(-TAU * a) for a in energies]
    for m in range(n + 1):
        brute = sum(math.prod(weights[k] for k in c)
                    for c in itertools.combinations(range(n), m))
        direct_dp = stable_esym_dp(weights, m)
        shifted = shifted_esym_dp(energies, TAU, m)
        minimum_sum = sum(energies[:m])
        reconstructed = math.exp(-TAU * minimum_sum) * shifted
        dp_checks.append({"m": m, "brute_force": brute, "direct_dp": direct_dp,
                          "shifted_reconstructed": reconstructed,
                          "max_abs_error": max(abs(brute - direct_dp), abs(brute - reconstructed))})

    return {
        "N": n, "L": ell, "beta": beta, "parameters": {"J": J, "tau": TAU, "B": B, "V": V, "lambda": LAM},
        "sector_dimensions": [x["dimension"] for x in per_sector],
        "min_minmax_gap": min_eig_gap,
        "sector_minmax": per_sector,
        "pV": [float(x) for x in qv], "p0": [float(x) for x in q0],
        "P_V_M_ge_d": {str(x["d"]): x["tail_probability"] for x in cutoff_results},
        "archive_cutoffs": cutoff_results,
        "global_trace_distance_V_vs_free": global_t,
        "relative_entropy_formula": dtotal_formula,
        "relative_entropy_chain_rule": dtotal_chain,
        "relative_entropy_gap": dtotal_chain - dtotal_formula,
        "beta_expect_W_free": beta * avg_w_0,
        "beta_expect_W_interacting": beta * avg_w_v,
        "relative_entropy_le_betaWfree": bool(dtotal_formula <= beta * avg_w_0 + 2e-9),
        "weighted_conditional_trace_distance": weighted_conditional_t,
        "conditional_pinsker_bound": math.sqrt(max(0.0, conditional_kl) / 2.0),
        "delta_analytic_bound": delta_bound,
        "Cstar_truncated_k80": cst,
        "free_sector_dp_checks": dp_checks,
        "finite_check_pass": bool(min_eig_gap >= -TOL
                                  and dtotal_formula <= beta * avg_w_0 + TOL
                                  and abs(dtotal_chain - dtotal_formula) < 2e-7
                                  and weighted_conditional_t <= delta_bound + TOL
                                  and max(x["exact_archive_tail_identity_abs_error"] for x in cutoff_results) < 2e-8
                                  and max(abs(x["free_sector_decoder_error"] - x["free_sector_decoder_matrix_trace_distance"])
                                          for x in cutoff_results) < 2e-8
                                  and all(x["tail_le_chernoff"] for x in cutoff_results)
                                  and max(x["max_abs_error"] for x in dp_checks) < 2e-8),
        "dense_diagnostic_seconds": time.perf_counter() - case_started,
    }


def main() -> None:
    started = time.perf_counter()
    results = {
        "status": "FINITE-EVIDENCE; double precision; no exact-arithmetic or interval certificate",
        "purpose": "N=2..8 exact sector diagonalization checks for the open-chain candidate and free-sector DP identity",
        "python": platform.python_version(), "numpy": np.__version__,
        "cases": [run_case(n) for n in range(2, 9)],
        "all_finite_checks_pass": False,
    }
    results["all_finite_checks_pass"] = all(x["finite_check_pass"] for x in results["cases"])
    results["calculation_wall_seconds_before_serialization"] = time.perf_counter() - started
    path = Path(__file__).with_name("exact_numerical_check.json")
    path.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(path), "all_finite_checks_pass": results["all_finite_checks_pass"],
                      "cases": [{"N": x["N"], "min_minmax_gap": x["min_minmax_gap"],
                                 "T_V_free": x["global_trace_distance_V_vs_free"],
                                 "D_V_free": x["relative_entropy_formula"],
                                 "betaEW0": x["beta_expect_W_free"],
                                 "delta_bound": x["delta_analytic_bound"],
                                 "finite_check_pass": x["finite_check_pass"]}
                                for x in results["cases"]]}, indent=2))


if __name__ == "__main__":
    main()
