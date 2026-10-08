#!/usr/bin/env python3
"""Exact finite hypergeometric/Bernoulli controls for the fixed-range corollary."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math


def falling(n, k):
    return math.prod(n - i for i in range(k)) if n >= k else 0


fixtures = 0
word_coefficients = 0
max_tv = F(0)
for r in range(1, 6):
    words = list(product((0, 1), repeat=r))
    table = {z: F(((sum((i + 1) * (2 * bit - 1) for i, bit in enumerate(z)) ** 2
                     + 7 * sum(z)) % 31) - 15, 7) for z in words}
    bound_m = max(abs(v) for v in table.values())
    for ell in range(r, 17):
        for k in range(ell + 1):
            p = F(k, ell)
            probs = {}
            iid = {}
            for z in words:
                h = sum(z)
                a = F(falling(k, h) * falling(ell - k, r - h), falling(ell, r))
                b = F(math.comb(ell - r, k - h), math.comb(ell, k)) if 0 <= k - h <= ell - r else F(0)
                assert a == b
                probs[z] = a
                iid[z] = p ** h * (1 - p) ** (r - h)
                word_coefficients += 1
            assert sum(probs.values()) == sum(iid.values()) == 1
            tv = sum(abs(probs[z] - iid[z]) for z in words) / 2
            assert tv <= F(r * (r - 1), 2 * ell)
            max_tv = max(max_tv, tv)
            exact_potential = sum(table[z] * probs[z] for z in words)
            bernoulli_potential = sum(table[z] * iid[z] for z in words)
            assert abs(exact_potential - bernoulli_potential) <= bound_m * F(r * (r - 1), ell)
            fixtures += 1

result = {"status": "PASS", "date": "2026-10-08", "range_r": [1, 5],
          "block_ell": [1, 16], "count_K": "ALL feasible K", "fixtures": fixtures,
          "word_coefficients": word_coefficients,
          "max_total_variation": str(max_tv), "arithmetic": "exact Fraction",
          "tested": ["hypergeometric compression coefficient", "normalization",
                     "collision total-variation bound", "bounded table potential error"],
          "not_tested": ["all-L replacement limit", "ground/free-energy theorem",
                         "external validation or novelty"]}
here = Path(__file__).resolve().parent
(here / "GENERAL_DIAGONAL_CHECKS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
