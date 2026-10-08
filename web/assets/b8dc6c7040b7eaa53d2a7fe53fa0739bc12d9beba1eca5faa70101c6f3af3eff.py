#!/usr/bin/env python3
"""Finite diagnostic for a truncated free XX canonical-sector mode sampler.

The mathematical truncation certificate is documented in RESULT.txt. This
program uses Decimal to select/check the cutoff and double-precision log-DP
for timed sampling, so it is a reproducible implementation diagnostic, not a
machine-verified interval certificate or quantum-circuit execution.
"""
from __future__ import annotations

from decimal import Decimal, localcontext
from itertools import combinations
import json
import math
import platform
import random
import statistics
import sys
import time
from pathlib import Path


def log_canonical_tail_bound(m: int, cutoff: int, J: Decimal, tau: Decimal) -> Decimal:
    """Log of a uniform upper bound on P(any occupied mode > cutoff | M=m).

    Put c=8*tau*J and w_k=exp(-tau*L^2 epsilon_k). Then
      e_m(w) >= prod_{k=1}^m w_k,
      e_{m-1}(w excluding k) <= (sum w)^(m-1)/(m-1)!,
    and sum_{k>cutoff} w_k <= exp(-c(cutoff+1)^2)
       * (1+1/(2c(cutoff+1))).
    The remaining sum is bounded by exp(-c)(1+1/(2c)).
    """
    if m < 1 or cutoff < m:
        raise ValueError("require m>=1 and cutoff>=m")
    c = Decimal(8) * tau * J
    pi = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286")
    sum_sq = Decimal(m * (m + 1) * (2 * m + 1)) / Decimal(6)
    log_c_bound = -c + (Decimal(1) + Decimal(1) / (Decimal(2) * c)).ln()
    k0 = Decimal(cutoff + 1)
    log_tail_sum = -c * k0 * k0 + (Decimal(1) + Decimal(1) / (Decimal(2) * c * k0)).ln()
    log_factorial = sum(Decimal(i).ln() for i in range(2, m))
    return Decimal(2) * tau * J * pi * pi * sum_sq + Decimal(m - 1) * log_c_bound - log_factorial + log_tail_sum


def choose_cutoff(m: int, J: Decimal, tau: Decimal, eta: Decimal) -> tuple[int, Decimal]:
    with localcontext() as ctx:
        ctx.prec = 80
        target = eta.ln()
        for cutoff in range(m, 1_000_001):
            bound = log_canonical_tail_bound(m, cutoff, J, tau)
            if bound <= target:
                return cutoff, bound.exp()
    raise RuntimeError("cutoff search exceeded one million modes")


def log_add(a: float, b: float) -> float:
    if a == -math.inf:
        return b
    if b == -math.inf:
        return a
    if a < b:
        a, b = b, a
    return a + math.log1p(math.exp(b - a))


def log_weights(L: int, cutoff: int, J: float, tau: float) -> list[float]:
    """Relative log weights; common exp(-tau*a_1) cancels at fixed m."""
    a = [8.0 * J * L * L * math.sin(math.pi * k / (2.0 * L)) ** 2
         for k in range(1, cutoff + 1)]
    return [-tau * (x - a[0]) for x in a]


def suffix_log_dp(logw: list[float], m: int) -> list[list[float]]:
    K = len(logw)
    E = [[-math.inf] * (m + 1) for _ in range(K + 1)]
    for i in range(K + 1):
        E[i][0] = 0.0
    for i in range(K - 1, -1, -1):
        max_j = min(m, K - i)
        for j in range(1, max_j + 1):
            E[i][j] = log_add(E[i + 1][j], logw[i] + E[i + 1][j - 1])
    return E


def sample_subset(logw: list[float], E: list[list[float]], m: int, rng: random.Random) -> tuple[int, ...]:
    chosen = []
    remaining = m
    K = len(logw)
    for i in range(K):
        if remaining == 0:
            break
        if K - i == remaining:
            chosen.extend(range(i + 1, K + 1))
            remaining = 0
            break
        lp = logw[i] + E[i + 1][remaining - 1] - E[i][remaining]
        p = 0.0 if lp < -745.0 else min(1.0, max(0.0, math.exp(lp)))
        u = rng.getrandbits(53) * (2.0 ** -53)
        if u < p:
            chosen.append(i + 1)
            remaining -= 1
    if remaining:
        raise ArithmeticError("sampler ended with unfilled particle count")
    return tuple(chosen)


def exact_small_check() -> dict:
    L, K, m, J, tau = 14, 9, 3, 1.0, 0.4
    lw = log_weights(L, K, J, tau)
    E = suffix_log_dp(lw, m)
    states = list(combinations(range(K), m))
    raw = [math.exp(sum(lw[k] for k in s)) for s in states]
    z = sum(raw)
    expected = {tuple(k + 1 for k in s): v / z for s, v in zip(states, raw)}
    # The recursion's joint probabilities are computed directly from the
    # conditional include/skip factors, independently of subset products.
    max_abs = 0.0
    for s in states:
        chosen = set(s)
        rem = m
        prob = 1.0
        for i in range(K):
            if rem == 0:
                break
            if K - i == rem:
                prob *= 1.0 if all(j in chosen for j in range(i, K)) else 0.0
                rem = 0
                break
            lp = lw[i] + E[i + 1][rem - 1] - E[i][rem]
            pin = math.exp(lp)
            if i in chosen:
                prob *= pin
                rem -= 1
            else:
                prob *= (1.0 - pin)
        key = tuple(k + 1 for k in s)
        max_abs = max(max_abs, abs(prob - expected[key]))
    return {"states": len(states), "max_subset_probability_abs_error": max_abs,
            "tolerance": 2e-13, "pass": max_abs < 2e-13}


def main() -> None:
    Jd, taud, eta = Decimal("1"), Decimal("1"), Decimal("1e-8")
    m = 8
    cutoff, tail_bound = choose_cutoff(m, Jd, taud, eta)
    L = 100_000
    lw = log_weights(L, cutoff, float(Jd), float(taud))

    dp_times = []
    E = None
    for _ in range(9):
        t0 = time.perf_counter()
        E = suffix_log_dp(lw, m)
        dp_times.append(time.perf_counter() - t0)

    samples = 2_000
    checksum = 0
    sample_times = []
    for trial in range(9):
        rng = random.Random(20261008 + trial)
        t0 = time.perf_counter()
        for _ in range(samples):
            subset = sample_subset(lw, E, m, rng)
            checksum += sum(subset)
        sample_times.append(time.perf_counter() - t0)
    dp_seconds = statistics.median(dp_times)
    sample_seconds = statistics.median(sample_times)

    check = exact_small_check()
    result = {
        "status": "PASS" if check["pass"] and tail_bound <= eta else "FAIL",
        "algorithm": "suffix log elementary-symmetric-polynomial DP plus sequential fixed-size sampling",
        "complexity": {"dp_operations": "O(K m)", "dp_memory": "O(K m)", "one_sample": "O(K)"},
        "input": {"L": L, "N_sites": L - 1, "J": str(Jd), "tau": str(taud), "sector_m": m, "target_tail_error": str(eta)},
        "truncation": {"retained_low_modes_K": cutoff, "analytic_union_bound_decimal": str(tail_bound), "bound_below_target": tail_bound <= eta, "bound_formula": "exp(2 tau J pi^2 sum_{i=1}^m i^2) C^(m-1)/(m-1)! * sum_{k>K} exp(-8 tau J k^2), C=sum_{k>=1} exp(-8 tau J k^2), with both sums upper-bounded by first-term-plus-integral bounds"},
        "timing_seconds": {"trials": 9, "dp_build_median": dp_seconds, "dp_build_min": min(dp_times), "samples_2000_median": sample_seconds, "samples_2000_min": min(sample_times), "dp_plus_2000_samples_median": dp_seconds + sample_seconds, "samples_per_second_at_median": samples / sample_seconds},
        "sample_checksum": checksum,
        "small_exact_enumeration": check,
        "runtime_environment": {"python": sys.version.split()[0], "platform": platform.platform()},
        "limitations": ["No interval-certified exponential/trigonometric implementation.", "No quantum gate synthesis or physical hardware execution.", "Timing covers Python DP and classical subset sampling only; the N-qubit sine/Givens state-preparation circuit is not included.", "This is not an advantage claim; a classical computer can use the same mode subset sampler."],
    }
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
