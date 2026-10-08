#!/usr/bin/env python3
"""Arithmetic ledger for the hidden rank-one geometry example.

Checks substitutions and numerical consequences of the inherited N36
candidate bound. It does not validate N36's proof or establish novelty.
"""

from decimal import Decimal, getcontext
from fractions import Fraction
import json
from pathlib import Path

getcontext().prec = 40
d = 8
r = Decimal(1) / Decimal(4)
ratio = 2**24
eps = r / Decimal(ratio)
ln2 = Decimal(2).ln()
ln_ratio = Decimal(ratio).ln()
constant_nats_per_mode = Decimal(5) / Decimal(4) + ln2
lower_bits = (Decimal(d) * ln_ratio / Decimal(2) - Decimal(d) * constant_nats_per_mode) / ln2
known_index_leading_bits = ln_ratio / (Decimal(2) * ln2)
unknown_index_leading_bits = Decimal(d) * known_index_leading_bits

assert Decimal(128) * eps <= r <= 1
assert ratio == 2**24

# Verify A_i^T A_i=r^2 e_1 e_1^T exactly for every hidden left singular vector.
r_exact = Fraction(1, 4)
for i in range(d):
    matrix = [[r_exact if (row == i and col == 0) else Fraction(0)
               for col in range(d)] for row in range(d)]
    gram = [[sum(matrix[k][a] * matrix[k][b] for k in range(d))
             for b in range(d)] for a in range(d)]
    expected = [[r_exact * r_exact if (a == 0 and b == 0) else Fraction(0)
                 for b in range(d)] for a in range(d)]
    assert gram == expected

result = {
    "status": "finite arithmetic check only; N36/N31 theorem candidates not independently validated",
    "model": {
        "ambient_dimension": d,
        "singular_value_multiset_for_each_A_i": [str(r)] + ["0"] * (d - 1),
        "operator_shape": "d by d",
        "A_i": "r e_i e_1^T",
        "parameter_vectors": ["-e_1", "+e_1"],
        "noise_covariance": "I_d",
        "query": "one i in {1,...,d}, revealed after storage",
    },
    "parameters": {"r": str(r), "eps": str(eps), "r_over_eps": ratio},
    "N36_candidate_lower_bound": {
        "formula_nats": "(d/2) ln(r/eps) - (5/4 + ln 2)d",
        "log2_D_lower_bound_bits": str(lower_bits),
    },
    "leading_precision_terms_bits": {
        "known_index": str(known_index_leading_bits),
        "hidden_direction": str(unknown_index_leading_bits),
        "ratio": str(unknown_index_leading_bits / known_index_leading_bits),
    },
    "known_geometry_candidate_upper": {
        "formula": "(d/2) log2(r/eps) + O(d), via product positive scalar Gaussian hats",
        "leading_term_bits": str(unknown_index_leading_bits),
    },
}

out = Path(__file__).with_name("rank_one_no_go_check.json")
out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
