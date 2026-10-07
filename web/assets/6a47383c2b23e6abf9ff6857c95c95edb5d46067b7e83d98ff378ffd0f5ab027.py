"""Exact arithmetic checks for the explicit robust inward certificate.

This checks facet bounds; the extinction and uniqueness proofs are in PROOF.txt.
It does not treat finite checks as a proof of stochastic long-time behavior.
"""
from fractions import Fraction as Q
import json

c_lo, c_hi = Q(39, 20), Q(41, 20)
d_lo, d_hi = Q(49, 50), Q(51, 50)
k_lo, k_hi = d_lo, d_hi
s_lo, s_hi = Q(7, 4), Q(9, 4)
b_lo, b_hi = Q(1, 2), Q(3, 2)

margins = {
    "total_lower_unnormalized": c_lo - d_hi*s_lo,
    "total_upper_unnormalized": d_lo*s_hi - c_hi,
    "B_lower_unit_normal": b_lo*(k_lo*(s_lo-b_lo)-d_hi),
    "B_upper_unit_normal": b_hi*(d_lo-k_hi*(s_hi-b_hi)),
}
claimed = Q(41, 400)
assert all(value > 0 for value in margins.values())
assert margins["total_lower_unnormalized"]**2 >= 2*claimed**2
assert margins["total_upper_unnormalized"]**2 >= 2*claimed**2
assert margins["B_lower_unit_normal"] >= claimed
assert margins["B_upper_unit_normal"] >= claimed
assert c_lo*k_lo > d_hi*d_hi
assert s_lo-b_hi == Q(1, 4)

print(json.dumps({
    "status": "PASS",
    "normalized_common_margin": str(claimed),
    "unnormalized_margins": {key: str(value) for key, value in margins.items()},
    "min_A_in_polytope": str(s_lo-b_hi),
    "min_B_in_polytope": str(b_lo),
    "positive_equilibrium_worst_case_slack": str(c_lo*k_lo-d_hi*d_hi),
    "scope": "Exact facet arithmetic only; stochastic proof is analytical."
}, indent=2))
