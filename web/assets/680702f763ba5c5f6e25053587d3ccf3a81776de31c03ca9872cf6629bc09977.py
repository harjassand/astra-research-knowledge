#!/usr/bin/env python3
"""Sector diagnostic for a growing one-axis anisotropy A_N=sqrt(N) e_x e_x^T.

J^2 and J_x commute, so exact (j,m_x) weights are
  d[N,j] exp(2 j(j+1)/N + m_x^2/N),
where d[N,j] is the exact spin-j multiplicity. Multiplicities are formed from
exact central binomials and a stable recurrence; only normalized exponentials
are floating point. This is a bounded diagnostic, not a proof of concentration.
"""
import json
import math
from pathlib import Path


def logsumexp(xs):
    peak = max(xs)
    return peak + math.log(math.fsum(math.exp(x - peak) for x in xs))


def median(n):
    half = n // 2
    log_d = math.log(math.comb(n, half)) - math.log(half + 1)
    logs = []
    spins = range(half + 1)
    for j in spins:
        mlogs = [m * m / n for m in range(-j, j + 1)]
        logs.append(log_d + 2 * j * (j + 1) / n + logsumexp(mlogs))
        if j < half:
            log_d += math.log((half - j) * (2 * j + 3) / ((half + j + 2) * (2 * j + 1)))
    peak = max(logs)
    weights = [math.exp(x - peak) for x in logs]
    threshold = math.fsum(weights) / 2
    cumulative = 0.0
    for j, w in zip(spins, weights):
        cumulative += w
        if cumulative >= threshold:
            return float(j)
    raise RuntimeError("median not found")


rows = []
for n in (256, 1024, 4096):
    jmed = median(n)
    rows.append({"N": n, "median_j": jmed, "median_j_over_N": jmed / n,
                 "median_j_over_N_3_4": jmed / n ** 0.75})
path = Path(__file__).with_suffix(".json")
path.write_text(json.dumps({
    "status": "floating-point normalized exact-sector diagnostic; not a proof",
    "model": "A_N=sqrt(N) diag(1,0,0), b=0; K=2J^2/N+J_x^2/N",
    "rows": rows,
}, indent=2) + "\n")
print(path)
for row in rows:
    print(row)
