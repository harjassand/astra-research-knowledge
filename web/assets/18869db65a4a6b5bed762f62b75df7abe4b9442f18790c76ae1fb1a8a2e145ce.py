#!/usr/bin/env python3
"""Small float64 timing check for fixed-number free fermion subset sampling."""
from __future__ import annotations
import json
import math
import platform
import random
import time
from pathlib import Path


def logaddexp(a: float, b: float) -> float:
    if a == -math.inf:
        return b
    if b == -math.inf:
        return a
    hi, lo = (a, b) if a >= b else (b, a)
    return hi + math.log1p(math.exp(lo - hi))


def mode_energies(L: int, d: int, J: float):
    import itertools
    return [L * L * 4 * J * sum(1 - math.cos(math.pi * k / L) for k in ks)
            for ks in itertools.product(range(1, L), repeat=d)]


def build_suffix_log_esym(logw, tmax):
    Q = len(logw)
    D = [[-math.inf] * (tmax + 1) for _ in range(Q + 1)]
    D[Q][0] = 0.0
    for q in range(Q - 1, -1, -1):
        D[q][0] = 0.0
        for j in range(1, min(tmax, Q - q) + 1):
            D[q][j] = logaddexp(D[q + 1][j], logw[q] + D[q + 1][j - 1])
    return D


def sample_subset(logw, D, t, rng):
    Q = len(logw)
    selected = []
    j = t
    for q in range(Q):
        if j == 0:
            break
        remaining = Q - q
        if remaining == j:
            selected.extend(range(q, Q))
            break
        logp = logw[q] + D[q + 1][j - 1] - D[q][j]
        p = min(1.0, max(0.0, math.exp(logp)))
        if rng.random() < p:
            selected.append(q)
            j -= 1
    if j:
        raise ArithmeticError("backtracking failed to return requested particle count")
    return selected


L, d, copies, J, tau, particle_count = 32, 2, 2, 1.0, 0.2, 12
energies = mode_energies(L, d, J) * copies
logw = [-tau * e for e in energies]
start = time.perf_counter()
D = build_suffix_log_esym(logw, particle_count)
dp_seconds = time.perf_counter() - start
rng = random.Random(20261008)
samples = 100
start = time.perf_counter()
out = [sample_subset(logw, D, particle_count, rng) for _ in range(samples)]
sample_seconds = time.perf_counter() - start
assert all(len(x) == particle_count and len(set(x)) == particle_count for x in out)
result = {
    "status": "PASS",
    "scope": "float64 log-domain canonical subset DP and backtracking only; no Givens/gate or physical preparation",
    "python": platform.python_version(),
    "L": L,
    "d": d,
    "copies": copies,
    "mode_slots_Q": len(logw),
    "particle_sector_T": particle_count,
    "DP_entries": (len(logw) + 1) * (particle_count + 1),
    "DP_build_seconds": dp_seconds,
    "sample_count": samples,
    "backtracking_seconds": sample_seconds,
    "seconds_per_sample": sample_seconds / samples,
    "finite_diagnostic_only": True,
}
outfile = Path("outputs/research/spin_statistical/cycle2/d_dimensional_fermion/evidence/canonical_subset_dp_benchmark.json")
outfile.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
