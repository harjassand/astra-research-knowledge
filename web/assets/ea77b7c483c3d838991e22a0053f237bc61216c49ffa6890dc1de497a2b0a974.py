#!/usr/bin/env python3
"""Targeted exact checks for the arithmetic/geometry used by certificate.py."""
import copy
from fractions import Fraction as Q
import json
from certificate import check, power_bounds, sample, vertices

checks = 0
for base in map(Q, ("0", "1/3", "2/3", "3/2", "10")):
    for exponent in map(Q, ("0", "1/2", "2/3", "3/2", "4/3", "3")):
        lo, hi = power_bounds(base, exponent, 16)
        # Integer comparisons establish the direction of both rounded bounds.
        assert lo ** exponent.denominator <= base ** exponent.numerator
        assert hi ** exponent.denominator >= base ** exponent.numerator
        checks += 1
box = ((Q(0), Q(1)), (Q(0), Q(1)))
assert vertices([(Q(1), Q(1))], [Q(3)], [], box) == []
assert vertices([(Q(1), Q(1))], [Q(1)], [], box) == [(Q(0), Q(1)), (Q(1), Q(0))]
assert vertices([(Q(1), Q(0)), (Q(0), Q(1))], [Q(1, 2), Q(1, 2)], [], box) == [(Q(1, 2), Q(1, 2))]
checks += 3
good = check(sample())
assert good["status"] == "CERTIFIED"
assert good["uniform_entry_time_upper_bound"] == Q(4, 5)
assert all(row["tree"]["lower_bound"] == Q(5, 16)
           for row in good["active_cells"] if "tree" in row)
checks += 1
wide = sample()
wide["K"] = 16
bad = check(wide)
assert bad["status"] == "REFUTED"
assert bad["active_cells"][1]["tree"]["derivative_interval"] == (Q(-7, 16), Q(-7, 16))
checks += 1
narrow = sample()
narrow["inner_box"] = [["3/8", "5/8"], ["3/8", "5/8"]]
narrow["containment_margin"] = "1/32"
assert check(narrow)["status"] == "UNKNOWN"
checks += 1
print(json.dumps({"status": "PASS", "exact_checks": checks,
                  "scope": "arithmetic_geometry_and_named_examples_only"}, indent=2))
