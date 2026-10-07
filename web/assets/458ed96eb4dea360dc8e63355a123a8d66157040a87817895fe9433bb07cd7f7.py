#!/usr/bin/env python3
"""Numerically audit the rank-growth corollary from the c05_s03 pinching modulus.

This verifies recurrence arithmetic only. It is not a proof of the peer's
pinching theorem or of the universal CP-range lifting claim.
"""
import json
import math
from pathlib import Path

MAX_K = 80
b = [0.0] * (MAX_K + 1)  # b[k] = C_k**2
for k in range(2, MAX_K + 1):
    g = (1.0 + 4.0 * (k - 1) ** (1.0 / 3.0)) ** (2.0 / (3.0 ** (k - 2)))
    b[k] = (k - 1) ** (2.0 / 3.0) + g * b[k - 1]

# The infinite product bounding all partial products of g_k converges because
# log(g_k)=O(k*3^{-k}); compute a finite partial product as a numerical check.
prod_g = 1.0
for k in range(3, MAX_K + 1):
    prod_g *= (1.0 + 4.0 * (k - 1) ** (1.0 / 3.0)) ** (2.0 / (3.0 ** (k - 2)))

rows = []
for m in (10**6, 10**12, 10**30, 10**100, 10**300):
    delta = 2.0 / math.sqrt(m + 1.0) + 4.0 / (m + 1.0)
    L = math.log(1.0 / delta)
    # r = floor(0.9 log_3 L), clipped to the computed recurrence range.
    r = max(1, min(MAX_K, math.floor(0.9 * math.log(L, 3))))
    log_bound = (-math.inf if r == 1 else
                 math.log(r) + 0.5 * math.log(b[r]) - L / (3.0 ** (r - 1)))
    rows.append({
        "m": str(m),
        "delta_m": delta,
        "L=log(1/delta)": L,
        "rank_r": r,
        "C_r": math.sqrt(b[r]),
        "log(r*C_r*delta^(1/3^(r-1)))": log_bound,
    })

result = {
    "scope": "recurrence arithmetic diagnostic; peer pinching proof and universal lifting remain unaudited/open",
    "recurrence_max_k": MAX_K,
    "partial_product_g_3_to_80": prod_g,
    "b80_over_80_pow_5over3": b[80] / (80.0 ** (5.0 / 3.0)),
    "rows": rows,
}
path = Path(__file__).with_suffix(".json")
path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
