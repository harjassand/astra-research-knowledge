#!/usr/bin/env python3
"""Exact sufficient-inequality certificate for one scalar activity family.

This checks the rational inequalities in RESULT.txt section 5. It uses no
sampled state/scale grid, floating-point roots, or simulated trajectories.
The general all-dimensional affine theorem is not implemented here.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def qstr(q):
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def main():
    slopes = [F(-1), F(-3, 5), F(0), F(3, 5), F(1)]
    cuts = [F(-3, 4), F(-2, 5), F(2, 5), F(3, 4)]
    max_transition_shift = F(1, 20)
    increments = [b - a for a, b in zip(slopes, slopes[1:])]
    cutoff_base = min(increments)
    cutoff = cutoff_base ** 20
    assert all(F(0) < d < F(1) for d in increments)
    assert all(q > -1 for q in cuts)
    assert all(a < b for a, b in zip(cuts, cuts[1:]))
    assert all(b - a > max_transition_shift for a, b in zip(cuts, cuts[1:]))
    assert all(cut.denominator <= 20 and (cut * 20).denominator == 1 for cut in cuts)

    # For h <= min(increments)^20, h^(1/20) <= every increment.
    # Therefore adjacent equality h^eta=increment gives 0<eta<=1/20.
    # Ordered adjacent thresholds q_j-eta_j certify the lower envelope.
    lower = [F(-1)] + [q - max_transition_shift for q in cuts]
    upper = cuts + [F(1)]
    records = []
    for index, (slope, lo, hi) in enumerate(zip(slopes, lower, upper)):
        tolerance = F(1, 2) if slope == 0 else abs(slope) / 2
        error = max(abs(lo - slope), abs(hi - slope))
        assert lo <= hi
        assert error < tolerance
        records.append({
            "label": index,
            "slope": qstr(slope),
            "negative_offset_exponents": [qstr(q) for q in cuts[:index]],
            "activity_exponent_range_containing_all_ties": [qstr(lo), qstr(hi)],
            "tolerance": qstr(tolerance),
            "maximum_error_bound": qstr(error),
            "strict_slack": qstr(tolerance - error),
        })
    output = {
        "status": "CERTIFIED_EXACT_SUFFICIENT_INEQUALITIES",
        "scope": "scalar fixed-family activity for every -1<=p<=1 and 0<h<=cutoff",
        "proof_location": "RESULT.txt section 5",
        "general_compiler": False,
        "input_tolerance": "E(0)=1/2; E(r)=abs(r)/2 otherwise",
        "cutoff": qstr(cutoff),
        "cutoff_form": "(2/5)^20",
        "max_transition_shift": qstr(max_transition_shift),
        "puiseux_substitution": "h=z^20, 0<z<=2/5",
        "laurent_exponents": [int(q * 20) for q in cuts],
        "labels": records,
        "minimum_strict_slack": qstr(min(F(r["strict_slack"]) for r in records)),
        "sampling_used": False,
    }
    path = Path(__file__).with_name("affine_fixture.json")
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({"status": output["status"], "labels": len(slopes),
                      "minimum_strict_slack": output["minimum_strict_slack"],
                      "cutoff_form": output["cutoff_form"], "output": str(path)}))


if __name__ == "__main__":
    main()
