#!/usr/bin/env python3
"""Exact toy audit of average-over-A versus uniform-over-A quantifiers.

This is an abstract payoff-matrix witness only. It is not a quantum state or
channel counterexample, and it does not contradict the Brandao--Harrow theorem.
"""
import json
from pathlib import Path


rows = []
for n in (2, 4, 8, 16, 64, 256):
    # For M_ij = 1{i=j}, any probability vector mu gives
    # max_j E_i M_ij = max_j mu_j >= 1/n, with equality for uniform mu.
    avg_worst = 1.0 / n
    uniform_pairwise = 1.0
    rows.append({
        "number_of_A_tests": n,
        "min_over_mu_max_B_expected_payoff": avg_worst,
        "uniform_A_B_max_payoff": uniform_pairwise,
        "gap_factor": uniform_pairwise / avg_worst,
    })

result = {
    "scope": "abstract quantifier counterexample only; not a quantum state/channel counterexample",
    "payoff": "M_ij = 1 iff i=j",
    "exact_identity": "min_mu max_j sum_i mu_i M_ij = 1/n while max_ij M_ij = 1",
    "rows": rows,
}
path = Path(__file__).with_suffix(".json")
path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
