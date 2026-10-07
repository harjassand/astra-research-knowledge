#!/usr/bin/env python3
"""Arithmetic check of the sourced copy-ladder complexity boundary."""
import json
import math

rows = []
for L in range(3, 13):
    m = 2 ** (L - 1)
    d = L * m
    b_upper = 1 / L
    eb_lower = 1 - (m + 1) / (m + d)
    cover_lower = d  # d mutually orthogonal seed vectors, T-distance 1.
    rows.append({
        "L": L,
        "m": m,
        "seed_dimension_d": d,
        "broadcasting_error_upper": b_upper,
        "EB_error_lower": eb_lower,
        "covering_number_lower_for_radius_lt_1_over_2": cover_lower,
        "b_times_log_cover_lower": b_upper * math.log(cover_lower),
    })
assert rows[-1]["broadcasting_error_upper"] < 0.084
assert rows[-1]["EB_error_lower"] > 0.92
assert rows[-1]["b_times_log_cover_lower"] > math.log(2)
print(json.dumps({
    "rows": rows,
    "limiting_b_log_cover_lower": math.log(2),
    "status": "formula diagnostic passed; infinite-family theorem is separately sourced and derived in INITIAL.txt"
}, indent=2))
