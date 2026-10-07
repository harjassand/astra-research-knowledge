#!/usr/bin/env python3
"""Bounded sector-weight diagnostic for fixed vs growing critical couplings.

For even N, the multiplicity of spin j is
  d[N,j] = C(N,N/2-j) (2j+1)/(N/2+j+1).
The diagnostic compares the exact integer multiplicities with log Gibbs
weights exp(beta*j*(j+1)/N), beta=2 (critical A=0) and beta=1
(A=-sqrt(N)*I). Only the final exponentiation/normalization is floating
point; this is evidence for the derived scale change, not a proof.
"""
import json
import math
from pathlib import Path


def sector_median(n: int, beta: float) -> float:
    logs = []
    spins = range(n // 2 + 1)
    for j in spins:
        multiplicity = math.comb(n, n // 2 - j) * (2 * j + 1) // (n // 2 + j + 1)
        logs.append(math.log(multiplicity) + math.log(2 * j + 1) + beta * j * (j + 1) / n)
    peak = max(logs)
    weights = [math.exp(value - peak) for value in logs]
    total = math.fsum(weights)
    threshold = total / 2
    cumulative = 0.0
    for j, weight in zip(spins, weights):
        cumulative += weight
        if cumulative >= threshold:
            return float(j)
    raise RuntimeError("median not found")


rows = []
for n in (256, 1024, 4096, 16384):
    root = math.isqrt(n)
    assert root * root == n and root % 2 == 0
    for label, beta in (("fixed_critical_A0", 2.0), ("growing_isotropic_A=-sqrtN_I", 1.0)):
        median = sector_median(n, beta)
        rows.append({
            "N": n,
            "case": label,
            "median_j": median,
            "median_j_over_N_3_4": median / n ** 0.75,
            "median_j_over_sqrtN": median / math.sqrt(n),
            "beta": beta,
        })

path = Path(__file__).with_suffix(".json")
path.write_text(json.dumps({
    "status": "floating-point normalized exact-sector diagnostic; not an asymptotic proof",
    "multiplicities": "exact integers",
    "sequence": "N=4k^2, so A=-sqrt(N) I has integer entries",
    "rows": rows,
}, indent=2) + "\n")
print(path)
for row in rows:
    print(row)
