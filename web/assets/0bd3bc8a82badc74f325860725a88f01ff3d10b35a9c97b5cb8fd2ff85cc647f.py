#!/usr/bin/env python3
"""Exact rational diagnostics for the bounded sensor archive counterexample.

This verifies the algebraic input facts and finite identity-code fixtures. The
quantum rate lower bound is proved in the companion text using Holevo,
strong-subadditivity, and maximum-entropy inequalities; this script is not a
proof checker for those analytic steps.
"""
from fractions import Fraction as F
from itertools import product
import json
import math
from pathlib import Path


def int_moment_uniform_minus1_1(power: int) -> F:
    if power % 2:
        return F(0)
    # Probability density 1/2 on [-1,1].
    return F(1, power + 1)


def finite_product_mass(v, signs, r=F(1, 2)):
    out = F(1)
    for vi, si in zip(v, signs):
        out *= (1 + r * vi * si / 4) / 2
    return out


checks = {}
# Continuous channel C: mu = Unif[-1,1], h_C(x)=sqrt(3)x/4.
# Discrete channel D: nu = Unif{-1,+1}, h_D(s)=s/4.
# Their null Fisher scores have exactly equal squared norm 1/16.
checks["continuous_reference_normalized"] = int_moment_uniform_minus1_1(0) == 1
checks["continuous_reference_centered"] = int_moment_uniform_minus1_1(1) == 0
checks["continuous_reference_second_moment"] = int_moment_uniform_minus1_1(2) == F(1, 3)
checks["continuous_score_fisher_exact"] = F(3, 16) * int_moment_uniform_minus1_1(2) == F(1, 16)
checks["discrete_score_fisher_exact"] = (F(1, 4) ** 2) == F(1, 16)
checks["same_null_fisher_exact"] = checks["continuous_score_fisher_exact"] == checks["discrete_score_fisher_exact"]
# sqrt(3)/4 < 1/2, so for |theta|<=1 both likelihood ratios are positive;
# the continuous one is uniformly >1/2.
checks["continuous_likelihood_positive"] = 3 < 4
checks["discrete_likelihood_positive"] = F(1, 4) < 1

# Check exact normalization and lossless round-trip of the d-bit identity code
# for every rational grid parameter in the unit ball, d<=4.
fixture_count = 0
for d in range(1, 5):
    grid = (F(-1, 2), F(0), F(1, 2))
    for v in product(grid, repeat=d):
        if sum((vi * vi for vi in v), F(0)) > 1:
            continue
        mass_sum = F(0)
        for signs in product((-1, 1), repeat=d):
            # Mixed-radix code 0..2^d-1 and inverse decode.
            code = sum((1 << i) for i, s in enumerate(signs) if s == 1)
            recovered = tuple(1 if (code >> i) & 1 else -1 for i in range(d))
            assert recovered == signs
            mass_sum += finite_product_mass(v, signs)
        assert mass_sum == 1
        fixture_count += 1

checks["finite_identity_code_roundtrips"] = True
checks["finite_discrete_law_normalizes_exactly"] = True

# Rare-event family with h(u)=u/2, U~Unif[-1,1].
# E[h^2]=1/12 and E[|h|]=1/4 exactly.
Eh2 = F(1, 4) * int_moment_uniform_minus1_1(2)
Eabs_h = F(1, 2) * F(1, 2)  # E|U|/2 = (1/2)/2
checks["rare_score_second_moment_exact"] = Eh2 == F(1, 12)
checks["rare_tv_coefficient_exact"] = Eabs_h / 2 == F(1, 8)
# For any rational delta, the rare family's Fisher at theta=0 is
# delta*(1/delta)*E[h^2], while TV to the null reference is at most delta/8.
delta = F(1, 64)
rare_fisher = delta * (F(1, 1) / delta) * Eh2
rare_tv_max = delta * Eabs_h / 2
checks["rare_fisher_equals_nonrare_exact"] = rare_fisher == Eh2 == F(1, 12)
checks["rare_tv_bound_exact"] = rare_tv_max == delta / 8

assert all(checks.values()), checks
result = {
    "status": "FINITE-EVIDENCE",
    "checks": checks,
    "exact_fixture_counts": {
        "parameter_vectors_checked": fixture_count,
        "dimensions": [1, 2, 3, 4],
        "parameter_grid_per_coordinate": ["-1/2", "0", "1/2"],
        "admission": "sum(v_i^2) <= 1",
        "support_strings_per_vector": "2^d",
    },
    "exact_values": {
        "continuous_null_fisher": "1/16",
        "discrete_null_fisher": "1/16",
        "rare_and_nonrare_null_fisher": "1/12",
        "rare_tv_upper": "delta/8",
        "delta_fixture": "1/64",
        "rare_tv_fixture": "1/512",
    },
    "scope": "Exact rational algebra and finite identity-code fixtures only; the continuous archive lower bound uses analytic information inequalities stated in the companion report.",
}
out = Path(__file__).with_name("check_witness.json")
out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, sort_keys=True))
