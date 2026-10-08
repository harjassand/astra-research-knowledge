#!/usr/bin/env python3
"""Finite-precision check of critical Curie-Weiss magnetization moments.

This evaluates the exact N+1 magnetization masses at beta=1,h=0. It is a
diagnostic for the asymptotic constants, not a proof of convergence.
"""

import json
import math


LIMIT_VAR = math.sqrt(12.0) * math.gamma(0.75) / math.gamma(0.25)


def exact_critical_moments(n: int) -> dict[str, float | int]:
    mags = list(range(-n, n + 1, 2))
    logw = []
    for m in mags:
        k = (n + m) // 2
        log_choose = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
        logw.append(log_choose + (m * m) / (2.0 * n))
    peak = max(logw)
    weights = [math.exp(z - peak) for z in logw]
    total = math.fsum(weights)
    ex2 = math.fsum(w * (m * m) for w, m in zip(weights, mags)) / total
    ex4 = math.fsum(w * (m**4) for w, m in zip(weights, mags)) / total
    var = ex2
    scaled_var = var / (n**1.5)
    scaled_fourth = ex4 / (n**3)
    return {
        "N": n,
        "Var_M_over_N_3_2": scaled_var,
        "E_X4": scaled_fourth,
        "standardized_kurtosis": ex4 / (var * var),
        "limit_Var_X": LIMIT_VAR,
        "limit_E_X4": 3.0,
        "limit_kurtosis": 3.0 / (LIMIT_VAR * LIMIT_VAR),
    }


if __name__ == "__main__":
    print(json.dumps([exact_critical_moments(n) for n in (64, 128, 256, 512, 1024, 2048, 4096, 8192)], indent=2))
