"""Independent numerical diagnostics for uniform Gaussian spectral-CDF bounds.

These simulations check implementation and scale, not the mathematical theorem.
No eigensolver or scientific benchmark is used: Gaussian rotational invariance
reduces the exact distribution to independent chi-square weights.
"""
import json
import math
from pathlib import Path
import resource
import time

import numpy as np


def main():
    start_wall = time.perf_counter()
    start_cpu = time.process_time()
    seed = 202610210731
    rng = np.random.default_rng(seed)
    trials = 50000
    delta = 0.1
    x = math.log(2 / delta)
    cases = []
    for n, s in [(4, 1), (4, 2), (16, 2), (16, 4), (64, 4), (128, 8)]:
        radius = 2 * math.sqrt(x / (n * s)) + 2 * x / (n * s)
        normalized_radius = math.sqrt(x / (n * s - 2)) if s % 2 == 0 else None
        bad_raw = 0
        bad_norm = 0
        max_raw = 0.0
        max_norm = 0.0
        means = []
        q = np.arange(1, n + 1, dtype=float) / n
        for batch_start in range(0, trials, 1000):
            b = min(1000, trials - batch_start)
            weights = rng.chisquare(s, (b, n))
            prefixes = np.cumsum(weights, axis=1)
            errors = np.max(np.abs(prefixes / (n * s) - q), axis=1)
            bad_raw += int(np.count_nonzero(errors > radius))
            max_raw = max(max_raw, float(np.max(errors)))
            if normalized_radius is not None:
                nerrors = np.max(np.abs(prefixes / prefixes[:, -1:] - q), axis=1)
                bad_norm += int(np.count_nonzero(nerrors > normalized_radius))
                max_norm = max(max_norm, float(np.max(nerrors)))
                means.append(float(np.sum(nerrors)))
        cases.append({
            "n": n,
            "s": s,
            "trials": trials,
            "nominal_failure_probability": delta,
            "unnormalized_radius": radius,
            "unnormalized_exceedances": bad_raw,
            "unnormalized_empirical_failure_rate": bad_raw / trials,
            "unnormalized_max_observed_error": max_raw,
            "normalized_radius": normalized_radius,
            "normalized_exceedances": bad_norm if normalized_radius is not None else None,
            "normalized_empirical_failure_rate": bad_norm / trials if normalized_radius is not None else None,
            "normalized_max_observed_error": max_norm if normalized_radius is not None else None,
        })

    # Pointwise check of the deterministic reduction to the ordinary KS statistic.
    # U_{km} is a grouped-spacings cumulative weight; the target is k/n.
    domination = []
    for n, m in [(2, 1), (4, 1), (5, 3), (16, 4), (64, 2)]:
        N = n * m - 1
        u = np.sort(rng.uniform(size=(5000, N)), axis=1)
        j = np.arange(1, N + 1, dtype=float)
        ks = np.maximum(np.max(j / N - u, axis=1), np.max(u - (j - 1) / N, axis=1))
        k = np.arange(1, n)
        grouped = u[:, k * m - 1]
        grouped_error = np.max(np.abs(grouped - k / n), axis=1)
        excess = float(np.max(grouped_error - ks))
        if excess > 2e-14:
            raise RuntimeError("Grouped-spacings error exceeded empirical KS statistic")
        domination.append({"n": n, "m": m, "uniform_count": N, "trials": 5000, "max_grouped_error_minus_KS": excess})

    # Ties select a subset of prefixes and cannot enlarge the supremum.
    n, s = 17, 4
    w = rng.chisquare(s, size=(5000, n))
    pref = np.cumsum(w, axis=1) / (n * s)
    all_error = np.abs(pref - np.arange(1, n + 1) / n)
    tied_indices = np.array([2, 6, 10, 16])
    tie_excess = float(np.max(np.max(all_error[:, tied_indices], axis=1) - np.max(all_error, axis=1)))
    if tie_excess > 0:
        raise RuntimeError("Tie-subset supremum exceeded full prefix supremum")

    out = {
        "schema": "astra-pro2-uniform-probe-diagnostics-v1",
        "claim_status": "simulation diagnostics only; theorem proof in uniform_probe_bound.md",
        "seed": seed,
        "numpy_version": np.__version__,
        "cases": cases,
        "grouped_spacings_domination": domination,
        "ties_max_excess": tie_excess,
        "wall_seconds": time.perf_counter() - start_wall,
        "cpu_seconds": time.process_time() - start_cpu,
        "peak_process_rss_bytes_linux": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
    }
    target = Path(__file__).with_name("uniform_probe_diagnostics.json")
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
