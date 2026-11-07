#!/usr/bin/env python3
"""Make an unperformed assay plan or score supplied acquired measurements.

No spectra, yields, truth observations or costs are simulated. A design's
intended proportions are not measured mixture truth. This script's schema
checks are not physical verification of a supplied provenance declaration.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import statistics
import uuid

ROOT = Path(__file__).resolve().parent


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2) + "\n")


def make_plan(output, max_concentration_mM=None):
    output.mkdir(parents=True, exist_ok=True)
    preparation_master = []
    analyst_manifest = []
    for batch, matrix, total, desired in itertools.product(
        ["independent_batch1_day1", "independent_batch2_day2"],
        ["clean_solvent", "specified_quenched_recipe_matrix"],
        [0.1, 0.2, 0.8],
        [0.0, 0.05, 0.5, 0.95, 1.0],
    ):
        sid = "blind_" + uuid.uuid4().hex[:12]
        preparation_master.append({
            "sample_id": sid, "preparation_batch": batch, "matrix": matrix,
            "intended_combined_fraction_of_theoretical_max": total,
            "intended_desired_mole_fraction": desired,
            "intended_side_mole_fraction": 1.0 - desired,
            "intended_desired_concentration_mM": None if max_concentration_mM is None else max_concentration_mM * total * desired,
            "intended_side_concentration_mM": None if max_concentration_mM is None else max_concentration_mM * total * (1.0 - desired),
            "measured_reference_desired_yield_percent": None,
            "measured_reference_side_yield_percent": None,
            "measured_reference_uncertainty_percent": None,
            "independent_reference_raw_files": [],
            "actual_standard_stock_lots": [],
        })
        analyst_manifest.append({
            "sample_id": sid, "preparation_batch": batch,
            "sample_raw_files": [], "calibration_raw_files": [],
            "source_labels_used_as_truth": False,
            "candidate": {"desired_yield_percent": None, "side_yield_percent": None, "desired_interval_percent": None},
            "incumbent": {"desired_yield_percent": None, "side_yield_percent": None, "desired_interval_percent": None},
        })
    random.SystemRandom().shuffle(analyst_manifest)
    plan = {
        "status": "PLANNED_NOT_PERFORMED",
        "truth_status": "No acquired measurements. Intended recipe is not truth.",
        "concentration_denominator_status": "UNRESOLVED" if max_concentration_mM is None else "EXPLICIT_USER_INPUT_REQUIRES_INDEPENDENT_RECONCILIATION",
        "input_theoretical_max_concentration_mM": max_concentration_mM,
        "held_out_mixture_preparations": len(preparation_master),
        "additional_pure_calibrations": 20,
        "additional_matrix_solvent_blanks": 4,
        "QC_reinjections": "Add bracketing calibration/QC scans and carryover blanks; record actual count separately.",
        "instructions": [
            "Prespecify application tolerances and freeze both methods before the independent key is released.",
            "Resolve theoretical yield denominator, caffeine amount and all dilution units against actual preparation records.",
            "Preparer obtains independently assayed stocks and independently quantifies validation-mixture amounts, including uncertainty.",
            "Protect the preparation master from analysts during an actual blinded run. This public unperformed design is not itself a blinded experiment.",
            "Acquire complete PDA time/wavelength arrays including full caffeine spectrum, raw MS, method metadata, plate mapping and injection order.",
            "An intended5% minor fraction requires a measured detection/quantification specification; no performance guarantee is implied by its inclusion.",
            "Run the same raw samples through both methods; repeat injections are technical repeats and do not increase independent preparation count.",
            "Measure actual costs/time/data volume; UNKNOWN remains UNKNOWN until measured.",
        ],
        "preparation_master": preparation_master,
    }
    write_json(output / "PLANNED_PREPARATION_MASTER.json", plan)
    write_json(output / "PLANNED_ANALYST_MANIFEST.json", {"status": "PLANNED_NOT_PERFORMED", "injection_order": analyst_manifest})
    print(json.dumps({"status": plan["status"], "held_out_preparations": len(preparation_master), "output_directory": str(output), "actual_measurements": 0}))


def number(value, label):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(label + " must be an acquired numeric value; null/UNKNOWN is not zero")
    return float(value)


def verify_raw_file(item, base):
    path = Path(item["path"])
    if not path.is_absolute():
        path = base / path
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != item["sha256"]:
        raise ValueError("Raw file SHA256 mismatch: " + str(path))


def score(input_file, output_file):
    obj = json.loads(input_file.read_text())
    if obj.get("status") != "ACQUIRED_MEASUREMENTS":
        raise ValueError("Only an ACQUIRED_MEASUREMENTS manifest can be scored")
    if obj.get("source_labels_used_as_truth") is not False:
        raise ValueError("Source-derived assay labels are not independent truth")
    if obj.get("normalization_contract_resolved") is not True:
        raise ValueError("Resolve the amount/standard/dilution denominator first")
    records = obj["records"]
    if not records:
        raise ValueError("No acquired records supplied")
    errors = {method: [] for method in ["candidate", "incumbent"]}
    side_errors = {method: [] for method in errors}
    coverage = {method: [] for method in errors}
    zero_side_calls = {method: [] for method in errors}
    batches = set()
    for record in records:
        batches.add(record["independent_preparation_batch"])
        truth = record["independent_reference"]
        if truth.get("method") not in ["validated_q19F_NMR", "validated_resolved_LC_authentic_coinjection"]:
            raise ValueError("Independent structural reference method is required")
        if truth.get("independent_of_assay_calibration") is not True:
            raise ValueError("Truth must be independent of the calibration being tested")
        if not truth.get("raw_files") or not record.get("sample_raw_files"):
            raise ValueError("Raw sample and independent reference files are required")
        for item in record["sample_raw_files"] + truth["raw_files"]:
            verify_raw_file(item, input_file.parent)
        desired = number(truth.get("desired_yield_percent"), "reference desired yield")
        side = number(truth.get("side_yield_percent"), "reference side yield")
        number(truth.get("expanded_uncertainty_percent"), "reference uncertainty")
        for method in errors:
            prediction = record[method]
            dp = number(prediction.get("desired_yield_percent"), method + " desired yield")
            sp = number(prediction.get("side_yield_percent"), method + " side yield")
            errors[method].append(dp - desired)
            side_errors[method].append(sp - side)
            interval = prediction.get("desired_interval_percent")
            if interval is not None:
                low, high = [number(x, method + " interval") for x in interval]
                coverage[method].append(low <= desired <= high)
            if side == 0:
                zero_side_calls[method].append(sp)
    result = {
        "status": "COMPUTED_FROM_SUPPLIED_RECORDS_UNREVIEWED",
        "input_manifest_sha256": hashlib.sha256(input_file.read_bytes()).hexdigest(),
        "record_count": len(records), "declared_independent_preparation_batches": len(batches),
        "scope": "Arithmetic on supplied measurements plus file integrity. Not verification that the provenance/independence declarations are physically true. Reference uncertainty is retained in input and has not been propagated into comparative inferential claims.",
        "methods": {},
        "full_cost_advantage": "UNKNOWN unless complete measured ledger and matched specification supplied",
        "new_operation_validated": "NOT ESTABLISHED by this scoring script",
    }
    for method, values in errors.items():
        result["methods"][method] = {
            "desired_yield_mean_absolute_error_percent": statistics.mean(map(abs, values)),
            "desired_yield_max_absolute_error_percent": max(map(abs, values)),
            "desired_yield_mean_signed_error_percent": statistics.mean(values),
            "side_yield_mean_absolute_error_percent": statistics.mean(map(abs, side_errors[method])),
            "intervals_supplied": len(coverage[method]),
            "fraction_intervals_covering_reference_point_estimate": statistics.mean(coverage[method]) if coverage[method] else None,
            "side_yield_calls_when_reference_side_zero_percent": zero_side_calls[method],
        }
    write_json(output_file, result)
    print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--plan", action="store_true")
    action.add_argument("--score", type=Path)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "planned_test")
    parser.add_argument("--output", type=Path, default=ROOT / "SUPPLIED_ASSAY_SCORE.json")
    parser.add_argument("--max-concentration-mM", type=float, default=None)
    args = parser.parse_args()
    if args.plan:
        make_plan(args.output_dir, args.max_concentration_mM)
    else:
        score(args.score, args.output)


if __name__ == "__main__":
    main()
