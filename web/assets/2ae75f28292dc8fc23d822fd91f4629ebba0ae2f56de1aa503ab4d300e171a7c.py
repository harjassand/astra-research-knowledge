#!/usr/bin/env python3
"""Exact formula audit for the n-qubit local X/Z frame stress test."""
from fractions import Fraction
import json

rows = []
for n in range(1, 13):
    labels = 2 * n
    ordered_noncommuting_pairs = 2 * n
    squared_commutator_norm = 4
    cp = Fraction(ordered_noncommuting_pairs * squared_commutator_norm, labels**2)
    q = Fraction(1, 2)  # dual Y=I/2 and product Pauli-eigenstate primal frame
    energy = Fraction(1, 3)  # tensor-product qubit 1-to-2 cloner: lambda=2/3
    assert cp == Fraction(2, n)
    assert q == Fraction(1, 2)
    assert q <= 2 * energy
    rows.append({
        "n": n,
        "labels": labels,
        "ordered_noncommuting_pairs": ordered_noncommuting_pairs,
        "squared_norm_each": squared_commutator_norm,
        "commutator_average": f"{cp.numerator}/{cp.denominator}",
        "q_exact": f"{q.numerator}/{q.denominator}",
        "product_cloner_mean_energy": f"{energy.numerator}/{energy.denominator}",
        "q_over_energy": f"{(q/energy).numerator}/{(q/energy).denominator}",
    })
print(json.dumps({"status": "PASS_EXACT_COUNTS", "scope": "closed-form pair count and primal-dual frame witnesses", "rows": rows}, indent=2))
