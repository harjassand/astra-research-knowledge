#!/usr/bin/env python3
"""Exact-rational audit of the facet-local N35 worked example."""
from fractions import Fraction as F
from math import exp
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from facet_local_calculation import certificate  # noqa: E402

# Deterministic inward margins over the declared rate interval [0.9, 1.1].
margin_checks = {
    "A_lower": F(9, 10) - F(11, 10) * F(11, 20) ** 2 - F(14, 25),
    "A_upper": F(9, 10) * F(39, 20) ** 2 - F(11, 10) - F(23, 10),
    "B_lower": F(9, 10) - F(11, 10) * F(11, 20) - F(29, 100),
    "B_upper": F(9, 10) * F(39, 20) - F(11, 10) - F(13, 20),
}
assert all(v > 0 for v in margin_checks.values())
assert margin_checks == {
    "A_lower": F(29, 4000),
    "A_upper": F(89, 4000),
    "B_lower": F(1, 200),
    "B_upper": F(1, 200),
}

global_box = certificate(local=False)
local_box = certificate(local=True)
assert global_box["V0"] == 8
assert local_box["V0"] == 3
assert global_box["Lambda"] == local_box["Lambda"] == "44/5"

def exact_c(result):
    return min(F(row["c_i"]) for row in result["facets"])

c_global = exact_c(global_box)
c_local = exact_c(local_box)
assert c_global == F(29, 39600)
assert c_local == F(29, 20460)
assert c_local / c_global == F(660, 341)

local_20k = next(row for row in local_box["volume_summaries"] if row["V"] == 20_000)
assert abs(local_20k["exit_bound"] - 0.00082237319966648) < 1e-15
assert abs(local_20k["independent_200_replicates_at_least_3_exits_tail"] - 0.00064719201416255) < 1e-14
same_horizon = next(row for row in global_box["common_horizon_comparison"] if row["V"] == 20_000)
assert same_horizon["global_box_bound_at_same_T"] > 700
assert abs(same_horizon["refined_bound_at_same_T"] - local_20k["exit_bound"]) < 1e-15

print(json.dumps({
    "status": "finite exact-rational certificate arithmetic plus floating exponential diagnostics",
    "deterministic_margin_surpluses": {k: str(v) for k, v in margin_checks.items()},
    "V0_global": global_box["V0"],
    "V0_facet_local": local_box["V0"],
    "Lambda": global_box["Lambda"],
    "c_global": str(c_global),
    "c_local": str(c_local),
    "c_ratio_local_over_global": str(c_local / c_global),
    "V20000_local_exit_bound": local_20k["exit_bound"],
    "V20000_200_replicates_3plus_tail": local_20k["independent_200_replicates_at_least_3_exits_tail"],
    "V20000_global_bound_at_local_horizon": same_horizon["global_box_bound_at_same_T"],
}, indent=2))
