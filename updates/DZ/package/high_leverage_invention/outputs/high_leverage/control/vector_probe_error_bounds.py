#!/usr/bin/env python3
"""Real-arithmetic analytical error estimates for filtered vector probe grids.

These calculations are ordinary floating point evaluations of proved bounds;
they are not outward-rounded interval certificates.
"""
import json
import math
from pathlib import Path

N = 32768
M = 10
ell = 2 * M
r = 2 * math.pi
log_double_factorial = math.lgamma(2 * ell + 2) - ell * math.log(2) - math.lgamma(ell + 1)
first_legendre_term = (2 * ell + 1) * math.exp(
    ell * math.log(r) - log_double_factorial + r * r / (2 * (2 * ell + 3)))
orientation_bound = 2 * first_legendre_term / (1 - r / (2 * ell + 1))
out = {"orientation_degree_of_exactness": 2 * M - 1,
       "orientation_average_absolute_rate_error_bound": orientation_bound,
       "filtered_time_grid_bounds": []}
for K in (64, 256):
    y = math.log(2) / K
    tail_l1 = 2 * math.exp(2 * math.pi - N * y / 2) / (-math.expm1(-y))
    out["filtered_time_grid_bounds"].append({
        "Fejer_cutoff": K,
        "Fourier_alias_absolute_rate_error_bound": 2 * tail_l1 + 2 * tail_l1 ** 2,
        "true_peak_over_sampled_peak_upper_factor": 1 / (1 - math.pi ** 2 * K ** 2 / (2 * N ** 2)),
    })
Path(__file__).with_name("vector_probe_error_bounds.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
