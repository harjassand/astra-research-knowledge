#!/usr/bin/env python3
"""Small exact checks for the XXZ primary-source scope audit."""
from fractions import Fraction as F
import json
from pathlib import Path


def rank_diagonal(values):
    return sum(value != 0 for value in values)

# A rational infinitesimal-gate fixture. The new linear triangle holds, while
# Cai--Liu--Lu's older squared triangle fails in opposite ways for gamma signs.
alpha, s = F(1), F(1, 10)
gate_fixtures = []
for gamma in (F(1, 2), F(-1, 2)):
    a = 1 + s * (3 * alpha + gamma)
    b = 1 + s * (3 * alpha - gamma)
    c = 2 * s * alpha
    linear = (a <= b + c) and (b <= a + c) and (c <= a + b)
    squared = (a*a <= b*b + c*c) and (b*b <= a*a + c*c) and (c*c <= a*a + b*b)
    gap = (a*a - b*b - c*c) if gamma > 0 else (b*b - a*a - c*c)
    gate_fixtures.append({
        "alpha": str(alpha), "gamma": str(gamma), "s": str(s),
        "a": str(a), "b": str(b), "c": str(c),
        "linear_triangle": linear, "old_squared_triangle": squared,
        "violated_squared_inequality_gap": str(gap),
    })
    assert linear and not squared and gap == F(11, 50)

# For the full easy-plane cone, the HMS Theorem 47 zero-location hypothesis
# can be met after one global axis permutation: (Jxx,Jyy,Jzz)=(alpha,gamma,alpha).
# This checks the simplified no-cross-coupling inequality, not an algorithm.
zero_location = []
for alpha in (F(1), F(2)):
    for numerator in range(-2, 3):
        gamma = alpha * F(numerator, 2)
        lhs = alpha
        rhs = (abs(alpha - gamma) + abs(alpha + gamma)) / 2
        zero_location.append({
            "alpha": str(alpha), "gamma": str(gamma),
            "Jzz_after_axis_permutation": str(lhs),
            "required_half_sum": str(rhs), "condition_holds": lhs >= rhs,
        })
        assert lhs >= rhs

# Bilocal interaction rank is invariant under local unitaries (SO(3) actions).
# A nonzero ZZ coefficient gives rank 3, while the Bravyi--Gosset displayed
# interaction tensor has rank at most 2.
rank_comparison = {
    "target_gamma_plus_alpha": rank_diagonal((F(1), F(1), F(1))),
    "target_gamma_minus_alpha": rank_diagonal((F(1), F(1), F(-1))),
    "bravyi_gosset_maximum": 2,
    "rank3_excludes_BG_edge_under_local_unitaries": True,
}
assert rank_comparison["target_gamma_plus_alpha"] == 3
assert rank_comparison["target_gamma_minus_alpha"] == 3

# Pauli coefficient bookkeeping for the EPR endpoint. A common Rx(pi/2)
# rotates P_{Phi+}=(I+XX-YY+ZZ)/4 to P_{Psi+}=(I+XX+YY-ZZ)/4.
epr_coefficients = {
    "I": F(1, 4), "XX": F(1, 4), "YY": F(1, 4), "ZZ": F(-1, 4)
}
assert 4 * epr_coefficients["XX"] == 1
assert 4 * epr_coefficients["YY"] == 1
assert 4 * epr_coefficients["ZZ"] == -1

result = {
    "status": "PASS",
    "gate_fixtures": gate_fixtures,
    "HMS_Theorem47_zero_location_condition_samples": zero_location,
    "HMS_scope_caveat": "This is a zero-location theorem in a variable longitudinal field, not a partition-function approximation for the target.",
    "BG_rank_comparison": rank_comparison,
    "EPR_endpoint_pauli_coefficients": {k: str(v) for k, v in epr_coefficients.items()},
    "EPR_endpoint_identity": "XX+YY-ZZ = 4 P_PsiPlus - I; common axis rotation maps source P_PhiPlus to P_PsiPlus.",
    "scope": "Exact rational fixtures only; not a proof of imported theorems or novelty.",
}
out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
