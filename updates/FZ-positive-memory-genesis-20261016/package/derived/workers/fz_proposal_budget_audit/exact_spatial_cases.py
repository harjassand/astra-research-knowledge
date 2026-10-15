#!/usr/bin/env python3
"""Exact small-incidence tests using rational arithmetic; no optimization oracle."""
from fractions import Fraction as Q
from itertools import combinations, product
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
MODES = frozenset(range(3))
SUBSETS = [frozenset(x) for size in range(1, 4) for x in combinations(range(3), size)]
AXES = (Q(1), Q(2), Q(3))
EPS = (Q(1), Q(2), Q(3))


def cell_objective(subset, floors, axes=AXES):
    return sum(floors[i] for i in subset) + max(axes[i]**2 / floors[i] for i in subset)


families = 0
compression_cases = 0
box_cases = 0
for mask in range(1, 1 << len(SUBSETS)):
    cells = [subset for j, subset in enumerate(SUBSETS) if mask & (1 << j)]
    if frozenset().union(*cells) != MODES:
        continue
    families += 1
    squared_norms = [sum(AXES[i]**2 for i in subset) for subset in cells]
    largest_squared = max(squared_norms)
    # Let B=sqrt(largest_squared). gamma_i=b_i^2/B gives
    # F_c=(squared_norm_c+largest_squared)/B. Compare after multiplying by B.
    assert all(norm + largest_squared <= 2 * largest_squared for norm in squared_norms)
    assert max(norm + largest_squared for norm in squared_norms) == 2 * largest_squared
    optimal_box = 2 * max(sum(EPS[i] for i in subset) for subset in cells)
    for floors in product((Q(1, 2), Q(1), Q(2)), repeat=3):
        z = [max(AXES[i]**2 / floors[i] for i in subset) for subset in cells]
        compressed = [max(AXES[i]**2 / z[c] for c, subset in enumerate(cells) if i in subset) for i in range(3)]
        assert all(compressed[i] <= floors[i] for i in range(3))
        q = max(cell_objective(subset, floors) for subset in cells)
        for c, subset in enumerate(cells):
            assert sum(compressed[i] for i in subset) + z[c] <= q
            assert all(AXES[i]**2 / compressed[i] <= z[c] for i in subset)
            assert cell_objective(subset, compressed) <= q
        compression_cases += 1
        worst_box = max(sum(floors[i] + EPS[i]**2 / floors[i] for i in subset) for subset in cells)
        assert worst_box >= optimal_box
        assert max(sum(EPS[i] + EPS[i]**2 / EPS[i] for i in subset) for subset in cells) == optimal_box
        box_cases += 1

axes_overlap = (Q(5), Q(12), Q(9))
cells_overlap = [frozenset((0, 1)), frozenset((1, 2))]
floors_overlap = tuple(x*x / 15 for x in axes_overlap)
rates_overlap = [cell_objective(subset, floors_overlap, axes_overlap) for subset in cells_overlap]
assert floors_overlap == (Q(5, 3), Q(48, 5), Q(27, 5))
assert rates_overlap == [Q(394, 15), Q(30)]
assert max(rates_overlap) == 30

result = {
    "scope": "Modewise diagonal Pauli floors; one global ellipsoid; common scalar spatial cap",
    "covered_three_mode_incidence_families": families,
    "feasibility_compression_grid_cases": compression_cases,
    "box_lower_bound_and_attainment_grid_cases": box_cases,
    "ellipsoid_shared_floor_certificates": families,
    "arbitrary_overlap_closed_form": "2 max_c sqrt(sum_{i in S_c} b_i^2)",
    "overlapping_unequal_cell_norm_example": {
        "axes": list(map(str, axes_overlap)),
        "cells_zero_based": [sorted(x) for x in cells_overlap],
        "floors": list(map(str, floors_overlap)),
        "cell_rates": list(map(str, rates_overlap)),
        "exact_optimum": "30",
    },
    "checks_passed": True,
}
(OUT / "EXACT_SPATIAL_CASES.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
