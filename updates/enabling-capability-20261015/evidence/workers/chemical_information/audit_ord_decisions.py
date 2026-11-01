#!/usr/bin/env python3
"""Descriptive audit of source-provided assay labels, not independent ground truth.

Run with pyarrow, ord-schema, and protobuf installed. No model is fitted.
The source's deconvolved labels are retained without clipping or alteration.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import time

import pyarrow.parquet as pq
from ord_schema.proto import reaction_pb2


def name(component):
    return next((i.value for i in component.identifiers if i.type == i.NAME), None)


def smiles(component):
    return next((i.value for i in component.identifiers if i.type == i.SMILES), None)


def product_yield(product):
    measurements = [m for m in product.measurements if m.type == m.YIELD]
    if len(measurements) != 1 or not measurements[0].HasField("percentage"):
        return None
    return float(measurements[0].percentage.value)


def summarize(rows):
    paired = [r for r in rows if r["dp"] is not None and r["sp"] is not None]
    finite = [r for r in paired if math.isfinite(r["dp"]) and math.isfinite(r["sp"])]
    admissible = [r for r in finite if min(r["dp"], r["sp"]) >= 0 and r["dp"] + r["sp"] <= 100]
    threshold_audit = []
    for threshold in (10, 50, 80):
        selected = [r for r in admissible if r["dp"] + r["sp"] >= threshold]
        desired_below = [r for r in selected if r["dp"] < threshold]
        purity_below = [r for r in selected if r["dp"] / (r["dp"] + r["sp"]) < 0.95]
        both_pass = [r for r in selected if r["dp"] >= threshold and r["dp"] / (r["dp"] + r["sp"]) >= 0.95]
        threshold_audit.append({
            "combined_yield_threshold_percent": threshold,
            "selected_by_combined_yield": len(selected),
            "desired_yield_below_threshold": len(desired_below),
            "desired_fraction_below_0_95": len(purity_below),
            "desired_yield_and_fraction_pass": len(both_pass),
            "selected_but_fail_one_or_both": len(selected) - len(both_pass),
        })
    return {
        "records": len(rows), "paired_assay_yields": len(paired), "finite_pairs": len(finite),
        "negative_component": sum(min(r["dp"], r["sp"]) < 0 for r in finite),
        "sum_above_100": sum(r["dp"] + r["sp"] > 100 for r in finite),
        "admissible_pairs_no_clipping": len(admissible),
        "thresholds": threshold_audit,
        "largest_side_product_records": sorted(admissible, key=lambda r: r["sp"], reverse=True)[:5],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("parquet", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    started = time.monotonic()
    rows = []
    product_counts = Counter()
    measurements = Counter()
    limiting_amounts = Counter()
    for batch in pq.ParquetFile(args.parquet).iter_batches(batch_size=512):
        for source in batch.to_pylist():
            r = reaction_pb2.Reaction.FromString(source["reaction"])
            assert r.reaction_id == source["reaction_id"]
            assert len(r.outcomes) == 1, (r.reaction_id, len(r.outcomes))
            desired = [p for p in r.outcomes[0].products if p.is_desired_product]
            side = [p for p in r.outcomes[0].products if p.reaction_role == reaction_pb2.ReactionRole.SIDE_PRODUCT]
            assert len(desired) == 1, (r.reaction_id, len(desired))
            assert len(side) <= 1, (r.reaction_id, len(side))
            p = desired[0]
            side_smiles = smiles(side[0]) if side else None
            product_counts[(smiles(p), side_smiles)] += 1
            for outcome_product in r.outcomes[0].products:
                for m in outcome_product.measurements:
                    if m.type == m.YIELD:
                        measurements[(m.details, m.uses_authentic_standard, m.uses_internal_standard)] += 1
            for inp in r.inputs.values():
                for c in inp.components:
                    if c.is_limiting:
                        limiting_amounts[(c.amount.moles.value, c.amount.moles.units)] += 1
            rows.append({
                "reaction_id": r.reaction_id,
                "dp_smiles": smiles(p),
                "sp_smiles": side_smiles,
                "dp": product_yield(p),
                "sp": product_yield(side[0]) if side else None,
            })
    groups = defaultdict(list)
    for r in rows:
        groups[r["dp_smiles"]].append(r)
    output = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "DESCRIPTIVE_AUDIT_OF_PRODUCER_ASSAY_LABELS_ONLY",
        "source_path": str(args.parquet.resolve()),
        "source_sha256": hashlib.sha256(args.parquet.read_bytes()).hexdigest(),
        "meaning": "Decision disagreement against source-reported component assays, not independently established false positives. Combined yield assumes unit-compatible molar yields; it is not reconstructed raw mass-spectrometer signal.",
        "threshold_design": "Descriptive thresholds 10, 50, 80 percent yield and 0.95 desired fraction chosen before calculation. Exclude missing, nonfinite, negative, or sum-over-100 pairs rather than clipping.",
        "all": summarize(rows),
        "by_desired_structure": {key: summarize(value) for key, value in groups.items()},
        "product_pairs": [{"desired_smiles": key[0], "side_smiles": key[1], "count": value} for key, value in product_counts.items()],
        "yield_measurement_metadata": [{"details": key[0], "uses_authentic_standard": key[1], "uses_internal_standard": key[2], "count": value} for key, value in measurements.items()],
        "limiting_amount_metadata": [{"value": key[0], "protobuf_units_enum": key[1], "count": value} for key, value in limiting_amounts.items()],
        "package_versions": {p: importlib.metadata.version(p) for p in ("pyarrow", "ord-schema", "protobuf")},
        "elapsed_seconds": time.monotonic() - started,
        "inference_cost": "UNKNOWN",
    }
    args.output.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"all": output["all"], "product_pairs": output["product_pairs"], "elapsed_seconds": output["elapsed_seconds"]}, indent=2))


if __name__ == "__main__":
    main()
