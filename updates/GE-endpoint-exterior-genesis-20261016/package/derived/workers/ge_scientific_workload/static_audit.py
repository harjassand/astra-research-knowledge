"""Original exact static audit for published cubic interchange workloads.

This is arithmetic/proof bookkeeping, not a runtime benchmark or new dataset.
It executes no acquired source. Source dimensions are documented in REPORT.md.
"""
from fractions import Fraction
from math import comb
from pathlib import Path
import json


def rational(x):
    return {"numerator": x.numerator, "denominator": x.denominator,
            "decimal_diagnostic": float(x)}


rows = []
for side in (80, 160):
    n = side**3
    pair_dim = comb(n, 2)
    # A tagged label makes at most 6 beta jumps in expectation. At beta <= 1,
    # Markov gives P(J >= 13) <= 6/13. At most 25^3 sites lie in the coordinate
    # cube of radius 12, including with periodic boundaries when side >= 25.
    # Uniform full-component shuffling puts the tag in that cube with at most
    # 25^3/n probability. TV dominates this event difference.
    lower = Fraction(7, 13) - Fraction(25**3, n)
    assert lower > Fraction(1, 2)
    rows.append({
        "side": side,
        "vertices": n,
        "open_cube_edges": 3 * side**2 * (side - 1),
        "periodic_cube_edges": 3 * n,
        "expected_direct_swaps_at_beta_1_open": 3 * side**2 * (side - 1),
        "expected_direct_swaps_at_beta_1_periodic": 3 * n,
        "pair_states": pair_dim,
        "one_pair_vector_at_8_bytes_per_entry_bytes": 8 * pair_dim,
        "explicit_label_array_bits_at_fixed_width": n * (n - 1).bit_length(),
        "full_component_uniformization_tv_lower_bound_beta_at_most_1": rational(lower),
    })

receipt = {
    "scope": "Exact integer/rational static arithmetic; no simulation or timing claim",
    "source": "Barp et al., arXiv:1505.00983v2, 2015-07-14, u=1 subcase",
    "boundary_convention": "Both open and periodic edge counts retained; rejection uses degree <= 6 only",
    "rows": rows,
    "assertions_passed": 2,
}
out = Path(__file__).with_name("STATIC_COST_RECEIPT.json")
out.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
