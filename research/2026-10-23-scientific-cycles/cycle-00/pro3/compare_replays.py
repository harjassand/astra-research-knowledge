#!/usr/bin/env python3
"""Compare frozen principal, higher-precision and independently coded results."""
import argparse
from decimal import Decimal as D
import json
from pathlib import Path


def numeric_leaves(obj, path=()):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key not in {"resources", "decimal_precision", "kernel_checks"}:
                yield from numeric_leaves(value, path+(key,))
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            yield from numeric_leaves(value, path+(index,))
    elif isinstance(obj, str):
        try:
            yield path, D(obj)
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    root = args.root
    principal = json.loads((root/"results/principal_results.json").read_text())
    higher = json.loads((root/"precision_check/principal_results.json").read_text())
    independent = json.loads((root/"independent_counterexample_results.json").read_text())
    values, values_higher = dict(numeric_leaves(principal)), dict(numeric_leaves(higher))
    assert values.keys() == values_higher.keys()
    diffs = {str(k): abs(v-values_higher[k]) for k, v in values.items()}
    assert all(diff <= D("1e-28") for diff in diffs.values())
    mapped = {D(f["p"]): f for f in independent["families"]}
    compared = 0
    mapping = {
        "pure_IMH": "pure_imh_tv",
        "local_then_global": "local_then_global_tv_after_n_cycles",
        "global_then_local": "global_then_local_tv_after_n_cycles",
    }
    for family in principal["families"]:
        other = mapped[D(family["p"])]
        assert abs(D(family["forward_KL"])-D(other["forward_KL"])) < D("1e-18")
        other_steps = {r["global_proposals"]: r for r in other["checks"]}
        for row in family["matched_cost_results"]:
            transitions = row["total_global_candidates"]-1
            if transitions in other_steps:
                for mine, theirs in mapping.items():
                    assert abs(D(row["TV"][mine])-D(other_steps[transitions][theirs])) < D("1e-18")
                    compared += 1
    receipt = {
        "all_checks_passed": True,
        "principal_decimal_digits": principal["decimal_precision"],
        "higher_decimal_digits": higher["decimal_precision"],
        "numeric_leaves_compared": len(values),
        "maximum_difference_in_30_digit_recorded_values": str(max(diffs.values())),
        "independent_decimal_digits": independent["precision_decimal_digits"],
        "independently_coded_TV_comparisons": compared,
        "independent_absolute_tolerance": "1e-18",
        "cost_counting_clarification": "Independent global_proposals means G transitions; add one initialization draw. Principal counts that draw explicitly. Mixture comparisons use different total update counts and are not equated here.",
        "certification_limit": "Rounded finite arithmetic comparisons, not interval-certified universal proofs."
    }
    (root/"results/comparison_receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
