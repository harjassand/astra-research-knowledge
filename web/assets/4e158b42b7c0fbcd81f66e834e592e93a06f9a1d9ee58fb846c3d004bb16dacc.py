#!/usr/bin/env python3
"""Finite arithmetic check of the displayed Haar union-bound exponent.
This checks numeric bookkeeping only, not the analytic packing proof.
"""
import json
import math

eta = 0.25
rows = []
for d in (8, 16, 32, 64, 128):
    m = d // 2
    log_bad = math.lgamma(d + 1) + m * m * math.log(eta / 2)
    # A proposed M=exp(0.1 d^2) random code has at most M^2 bad-pair union bound.
    log_union = 0.2 * d * d + log_bad
    rows.append({
        "d": d,
        "m": m,
        "log_haar_bad_upper_bound": log_bad,
        "log_union_bound_for_exp_0p1_d2_code": log_union,
        "bound_below_one": log_bad < 0,
        "union_bound_below_one": log_union < 0,
    })
print(json.dumps({"eta": eta, "rows": rows}, indent=2))
assert all(row["union_bound_below_one"] for row in rows if row["d"] >= 16)
