#!/usr/bin/env python3
"""Check selected decimal enclosures against unchanged exact receipt fractions."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = "morrey_law_first_stress_20261026/cube_brownian_completion/"
A = "morrey_effective_affinity_20261025/"
W = "morrey_global_w1_receiver_20261025/intrinsic/"
ENTRIES = [
    ("adopted141", M + "fully_corrective141_half_K48/received_full_Gram_candidate.json", ["global_negative_mass_upper"], "upper", "0.004714574814154892", "0.004714574814154893"),
    ("same-law-w1", W + "stationary_tail_same_law_transfer_receipt.json", ["laws", 1, "same_finite_AC_upper"], "upper", "0.06718566499649657", "0.06718566499649658"),
    ("overlap-credit", M + "same_law_AC/compatible_box_overlap_receipt.json", ["strict_finite_bulk_reduction_lower"], "lower", "2.1346001363868332e-20", "2.1346001363868332e-20"),
    ("union-hull-ceiling", M + "same_law_AC/posterior_hull_bulk_ceiling_receipt.json", ["rows", 2, "maximum_possible_finite_bulk_credit"], "upper", "4.0449265918215316e-5", "4.0449265918215316e-5"),
    ("affinity-three-axis-lower", A + "three_axis_w1_a625/actual_policy_affinity_sharp_receipt.json", ["actual_paid_affinity_lower"], "lower", "0.8893041904600858", "0.8893041904600857"),
    ("affinity-three-axis-upper", A + "three_axis_w1_a625/actual_policy_affinity_sharp_receipt.json", ["actual_paid_affinity_upper"], "upper", "0.8978776135719108", "0.8978776135719108"),
    ("affinity-smoothed-lower", A + "w1_smoothed_a625/actual_policy_affinity_sharp_receipt.json", ["actual_paid_affinity_lower"], "lower", "0.8859884591073331", "0.8859884591073331"),
    ("affinity-smoothed-upper", A + "w1_smoothed_a625/actual_policy_affinity_sharp_receipt.json", ["actual_paid_affinity_upper"], "upper", "0.8977410500370644", "0.8977410500370644"),
]


def verify(root=ROOT):
    selected = {row["repository_path"]: row for row in json.loads((root / "SOURCE_INDEX.json").read_text())["files"]}
    rows = []
    for label, logical, selector, direction, display, safe in ENTRIES:
        relative = "source/" + logical
        data = (root / relative).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == selected[relative]["sha256"], logical
        value = json.loads(data)
        for key in selector:
            value = value[key]
        exact, decimal, outward = Fraction(value), Fraction(display), Fraction(safe)
        valid = outward >= exact if direction == "upper" else outward <= exact
        assert valid, label
        rows.append({"id": label, "source": relative, "sha256": digest, "field": selector,
                     "exact_rational": str(exact), "bound_direction": direction,
                     "source_rounded_display": display,
                     "source_display_already_outward": decimal >= exact if direction == "upper" else decimal <= exact,
                     "safe_decimal_enclosure": safe, "safe_decimal_verified": valid})
    return {"scope": "Selected finite exact-rational presentation checks; unchanged scientific receipts govern. Not a new theorem, acquisition or comparison of different laws/metrics.",
            "checked_enclosures": len(rows), "rows": rows}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
