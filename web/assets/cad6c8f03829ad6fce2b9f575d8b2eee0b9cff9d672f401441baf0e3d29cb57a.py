#!/usr/bin/env python3
"""Bounded sector diagnostic for the strong antiferromagnetic counterexample.

For N even, choose A=-(N+2)sqrt(N) I, b=0, so K=-J^2 exactly.
The script computes the exact spin multiplicity recurrence and numerically
normalizes exp(-j(j+1)) sector weights. It reports the random-axis m=0 event
probability against the analytic separable upper bound 8/sqrt(N).
"""
import json
import math
from pathlib import Path


def log_sector_event(n):
    half = n // 2
    log_d = math.log(math.comb(n, half)) - math.log(half + 1)
    log_weights = []
    spins = range(half + 1)
    for j in spins:
        log_weights.append(log_d + math.log(2 * j + 1) - j * (j + 1))
        if j < half:
            log_d += math.log((half - j) * (2 * j + 3) / ((half + j + 2) * (2 * j + 1)))
    peak = max(log_weights)
    weights = [math.exp(x - peak) for x in log_weights]
    z = math.fsum(weights)
    p_zero_axis = math.fsum(w / (2 * j + 1) for j, w in zip(spins, weights)) / z
    return p_zero_axis


rows = []
for n in (256, 1024, 4096, 16384):
    rows.append({"N": n, "target_random_axis_m0": log_sector_event(n),
                 "separable_upper_8_over_sqrtN": min(1.0, 8 / math.sqrt(n)),
                 "gap_lower": log_sector_event(n) - min(1.0, 8 / math.sqrt(n))})

path = Path(__file__).with_suffix(".json")
path.write_text(json.dumps({
    "status": "floating-point sector normalization diagnostic; analytic bounds in INITIAL.txt are the proof",
    "model": "N=4k^2, A=-(N+2)sqrt(N) I, b=0, K=-J^2",
    "rows": rows,
}, indent=2) + "\n")
print(path)
for row in rows:
    print(row)
