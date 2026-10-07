#!/usr/bin/env python3
"""Small exact diagnostics for the CP-range stability audit.

The Hamming calculation is a rigorous greedy-packing lower bound, not an
enumeration of optimal codes.  It shows that the full image of an abelian
pinching map need not have dimension-uniform trace nets.
"""
from fractions import Fraction
from math import comb, sqrt
import json
from pathlib import Path


def cp_range_commutator_bound(m: int) -> float:
    return 2 / sqrt(m + 1) + 4 / (m + 1)


def hamming_packing_lower_bound(d: int) -> Fraction:
    assert d % 8 == 0
    balanced = comb(d, d // 2)
    removed_per_greedy_step = sum(comb(d, j) for j in range(d // 4))
    return Fraction(balanced, removed_per_greedy_step)


rows = []
for d in (8, 16, 24, 32, 64):
    lower = hamming_packing_lower_bound(d)
    rows.append({
        "dimension": d,
        "balanced_sign_vectors": comb(d, d // 2),
        "greedy_packing_lower_bound_exact": f"{lower.numerator}/{lower.denominator}",
        "greedy_packing_lower_bound_ceiling": (
            lower.numerator + lower.denominator - 1
        ) // lower.denominator,
        "pairwise_half_trace_distance_lower_bound": "theta/4",
        "cover_radius_tested": "theta/9",
    })

pair_rows = []
for m in (1, 4, 16, 256, 65536):
    delta = cp_range_commutator_bound(m)
    pair_rows.append({
        "power": m,
        "uniform_commutator_bound": delta,
        "Bansil_Kachkovskiy_two_matrix_error_bound": 5 * delta ** (1 / 3),
        "scope": "one pair only; commuting corrections may depend on both matrices",
    })

result = {
    "status": "finite exact arithmetic / formula evaluation; not a theorem replay",
    "hamming_packing": rows,
    "pair_stability_rate": pair_rows,
    "analytic_claim": (
        "For every d divisible by 8, greedy selection from the balanced sign "
        "vectors gives at least binom(d,d/2)/sum_{j<d/4}binom(d,j) vectors "
        "with pairwise Hamming distance at least d/4. Their diagonal states "
        "(I+theta diag(s))/d have half-trace distance at least theta/4."
    ),
}
out = Path(__file__).with_name("stability_audit_check.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(out.read_text())
