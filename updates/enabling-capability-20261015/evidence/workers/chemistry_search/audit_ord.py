"""Audit measured ORD C–N data, preserving exact catalyst-deletion comparisons.

Run with the bundled Python. Dependencies are local to .python_packages.
No interpolation, synthetic measurements, or unmeasured controls are used.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import statistics
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / ".python_packages"))
import pyarrow.parquet as pq
from google.protobuf.json_format import MessageToDict
from ord_schema.proto import reaction_pb2


def ident(component, kind="NAME"):
    return next((x["value"] for x in component.get("identifiers", []) if x.get("type") == kind), "UNKNOWN")


def product_record(product):
    yields = [m for m in product.get("measurements", []) if m.get("type") == "YIELD"]
    return {
        "smiles": ident(product, "SMILES"),
        "role": product.get("reaction_role", "UNKNOWN"),
        "is_desired": product.get("is_desired_product", False),
        "yield_pct": yields[0].get("percentage", {}).get("value") if yields else None,
        "yield_measurement": yields[0] if yields else None,
    }


def to_record(r):
    custom = {i.get("details"): i["value"] for i in r.get("identifiers", []) if i.get("type") == "CUSTOM"}
    ingredients = {}
    solvents = collections.defaultdict(float)
    for key, inp in r.get("inputs", {}).items():
        non_solvent = []
        for comp in inp.get("components", []):
            if comp.get("reaction_role") == "SOLVENT":
                vol = comp.get("amount", {}).get("volume", {})
                solvents[(ident(comp, "SMILES"), vol.get("units", "UNKNOWN"))] += vol.get("value", 0)
            else:
                non_solvent.append({"name": ident(comp), "smiles": ident(comp, "SMILES"), "amount": comp.get("amount", {}), "role": comp.get("reaction_role"), "identifiers": comp.get("identifiers", [])})
        ingredients[key] = {"addition_order": inp.get("addition_order"), "components": non_solvent}
    outcomes = r.get("outcomes", [])
    products = [product_record(p) for p in outcomes[0].get("products", [])] if outcomes else []
    desired = [p for p in products if p["is_desired"]]
    sides = [p for p in products if p["role"] == "SIDE_PRODUCT"]
    sample = custom.get("Sample Name_x", "UNKNOWN")
    # Source sample names use either a numeric injection index or A1..P24 well.
    # This prefix identifies a 384-well analytical plate, not the 1536-well reactor.
    plate = re.sub(r"[_-](?:[A-Pa-p]\d{1,2}|\d+)$", "", sample)
    catalyst_name = ";".join(c["name"] for c in ingredients.get("catalyst soln", {}).get("components", [])) or "UNKNOWN"
    nonmetal = catalyst_name.lower() in ("none", "blank", "no metal")
    condition = r.get("conditions", {})
    record = {
        "reaction_id": r["reaction_id"], "sample": sample, "plate": plate,
        "experiment": custom.get("experiment", "UNKNOWN"), "coded_recipe": custom.get("coded recipe", "UNKNOWN"),
        "ingredients": ingredients, "catalyst_name": catalyst_name,
        "no_metal": nonmetal,
        "solvents": [[s, u, round(v, 12)] for (s, u), v in sorted(solvents.items())],
        "temperature": condition.get("temperature", {}).get("setpoint", {}),
        "reaction_time": outcomes[0].get("reaction_time", {}) if outcomes else {},
        "target_yield_pct": desired[0]["yield_pct"] if len(desired) == 1 else None,
        "target_smiles": desired[0]["smiles"] if len(desired) == 1 else "UNKNOWN",
        "side_products": sides,
        "analyses": outcomes[0].get("analyses", {}) if outcomes else {},
        "outcome_count": len(outcomes),
    }
    record["side_yield_pct"] = sum(p["yield_pct"] for p in sides if p["yield_pct"] is not None) if sides else None
    record["target_fraction_among_reported_products"] = (
        record["target_yield_pct"] / (record["target_yield_pct"] + record["side_yield_pct"])
        if record["target_yield_pct"] is not None and record["side_yield_pct"] is not None and record["target_yield_pct"] + record["side_yield_pct"] > 0 else None
    )
    # Exact-match inputs, retaining original amount units; remove only catalyst identity/amount.
    # Catalyst carrier solvent remains included in total solvent composition above.
    key = {
        "ingredients_except_metal": {k: v for k, v in ingredients.items() if k != "catalyst soln"},
        "solvents": record["solvents"], "conditions": condition,
        "reaction_time": record["reaction_time"], "target_smiles": record["target_smiles"],
        "setup": r.get("setup", {}), "workups": r.get("workups", []),
    }
    # CUSTOM ingredient codes may change across campaigns; chemistry identity/amount is the match.
    for inp in key["ingredients_except_metal"].values():
        for c in inp["components"]:
            c.pop("identifiers", None)
    record["matching_key"] = json.dumps(key, sort_keys=True, separators=(",", ":"))
    return record


def main():
    start = time.perf_counter()
    path = BASE / "ord_dataset-805ad863feef48579d95d86a728035f4.parquet"
    pf = pq.ParquetFile(path)
    records = []
    examples = {}
    calibration_flags = collections.Counter()
    for batch in pf.iter_batches(batch_size=2048):
        for raw in batch.to_pylist():
            rxn = reaction_pb2.Reaction()
            rxn.ParseFromString(raw["reaction"])
            r = MessageToDict(rxn, preserving_proto_field_name=True)
            rec = to_record(r)
            records.append(rec)
            for p in r.get("outcomes", [{}])[0].get("products", []):
                if p.get("is_desired_product"):
                    for m in p.get("measurements", []):
                        if m.get("type") == "YIELD":
                            calibration_flags[(m.get("uses_internal_standard", False), m.get("uses_authentic_standard", False), m.get("details", ""))] += 1
            tag = "no_metal" if rec["no_metal"] else "metal"
            if tag not in examples or (rec["target_yield_pct"] or 0) > (examples[tag]["outcomes"][0]["products"][0]["measurements"][-1].get("percentage", {}).get("value", 0)):
                examples[tag] = r

    groups = collections.defaultdict(list)
    for rec in records:
        groups[rec["matching_key"]].append(rec)
    comparisons = []
    for key, group in groups.items():
        controls = [r for r in group if r["no_metal"]]
        treated = [r for r in group if not r["no_metal"]]
        if not controls or not treated:
            continue
        for metal in treated:
            # Prefer truly same-plate controls. Otherwise preserve cross-plate status explicitly.
            same_plate = [r for r in controls if r["plate"] == metal["plate"]]
            same_experiment = [r for r in controls if r["experiment"] == metal["experiment"]]
            # Share all exact chemistry controls from the same experimental campaign.
            # Analytical subplates are preserved, but are not independent reaction batches.
            selected = same_experiment or controls
            cy = [r["target_yield_pct"] for r in selected if r["target_yield_pct"] is not None]
            cs = [r["side_yield_pct"] for r in selected if r["side_yield_pct"] is not None]
            if not cy or metal["target_yield_pct"] is None:
                continue
            comparisons.append({
                "metal_reaction_id": metal["reaction_id"], "metal_name": metal["catalyst_name"],
                "target_smiles": metal["target_smiles"], "target_metal_yield_pct": metal["target_yield_pct"],
                "target_control_mean_pct": statistics.mean(cy),
                "target_difference_pct": metal["target_yield_pct"] - statistics.mean(cy),
                "side_metal_yield_pct": metal["side_yield_pct"],
                "side_control_mean_pct": statistics.mean(cs) if cs else None,
                "control_reaction_ids": [r["reaction_id"] for r in selected],
                "control_wells": len(selected), "control_sample_sd_pct": statistics.stdev(cy) if len(cy) > 1 else None,
                "same_plate": bool(same_plate), "same_experiment": bool(same_experiment),
                "metal_sample": metal["sample"], "control_samples": [r["sample"] for r in selected],
            })

    no_metal = [r for r in records if r["no_metal"]]
    def thresholds(rows):
        result = {}
        for threshold in (10, 20, 50, 80):
            hits = [r for r in rows if r["target_yield_pct"] is not None and r["target_yield_pct"] >= threshold]
            clean = [r for r in hits if r["target_fraction_among_reported_products"] is not None and r["target_fraction_among_reported_products"] >= .95]
            result[str(threshold)] = {"target_hits": len(hits), "target_hits_with_reported_two_product_fraction_ge_0.95": len(clean)}
        return result
    summary = {
        "source_file": str(path.name), "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "rows": len(records), "unique_reaction_ids": len(set(r["reaction_id"] for r in records)),
        "unique_samples": len(set(r["sample"] for r in records)),
        "experiments": dict(collections.Counter(r["experiment"] for r in records)),
        "analytical_subplate_prefix_count_including_source_naming_anomalies": len(set(r["plate"] for r in records)),
        "reaction_block_count_derived_from_experiment_and_temperature": len(set((r["experiment"], json.dumps(r["temperature"], sort_keys=True)) for r in records)),
        "no_metal_rows": len(no_metal), "metal_rows": len(records) - len(no_metal),
        "target_structures": dict(collections.Counter(r["target_smiles"] for r in records)),
        "product_side_structures": dict(collections.Counter(p["smiles"] for r in records for p in r["side_products"])),
        "catalyst_names": dict(collections.Counter(r["catalyst_name"] for r in records)),
        "calibration_claim_flags": [{"internal_standard": k[0], "authentic_standard": k[1], "details": k[2], "rows": n} for k, n in calibration_flags.items()],
        "no_metal_hit_counts": thresholds(no_metal),
        "exact_match_control_comparisons": len(comparisons),
        "same_plate_comparisons": sum(r["same_plate"] for r in comparisons),
        "same_experiment_comparisons": sum(r["same_experiment"] for r in comparisons),
        "comparisons_with_control_replicates": sum(r["control_wells"] > 1 for r in comparisons),
        "negative_target_differences": sum(r["target_difference_pct"] < 0 for r in comparisons),
        "target_yield_range": [min(r["target_yield_pct"] for r in records if r["target_yield_pct"] is not None), max(r["target_yield_pct"] for r in records if r["target_yield_pct"] is not None)],
        "wall_seconds": time.perf_counter() - start,
        "limitations": [
            "Yields are source-reported calibrated assay measurements, not isolated product recovery.",
            "A 0.95 target fraction among reported target/side products is not total purity or full mass balance.",
            "Authentic/internal-standard flags do not provide calibration curves, raw chromatograms, or uncertainty.",
            "Replicate wells can share stocks and plates; well counts are not independent-batch confirmation.",
            "Exact chemistry comparisons across plates remain vulnerable to plate/batch nuisance effects.",
        ],
    }
    (BASE / "ORD_AUDIT.json").write_text(json.dumps(summary, indent=2) + "\n")
    # Minimal genuine data, with all no-metal controls and their matching treated wells.
    relevant_ids = {r["metal_reaction_id"] for r in comparisons}
    relevant_ids.update(x for r in comparisons for x in r["control_reaction_ids"])
    # Keep a reviewable small subset; complete immutable numerical source is 5 MB.
    controls_ranked = sorted(no_metal, key=lambda r: r["target_yield_pct"], reverse=True)
    subset_ids = {r["reaction_id"] for r in controls_ranked[:50]}
    clean_hits = [r for r in no_metal if r["target_yield_pct"] >= 20 and (r["target_fraction_among_reported_products"] or 0) >= .95]
    subset_ids.update(r["reaction_id"] for r in clean_hits)
    chosen_comparisons = [r for r in comparisons if subset_ids.intersection(r["control_reaction_ids"])]
    chosen_comparisons = chosen_comparisons[:200]
    subset_ids.update(r["metal_reaction_id"] for r in chosen_comparisons)
    subset_ids.update(x for r in chosen_comparisons for x in r["control_reaction_ids"])
    subset = [r for r in records if r["reaction_id"] in subset_ids]
    for r in subset:
        r["matching_key_sha256"] = hashlib.sha256(r.pop("matching_key").encode()).hexdigest()
    (BASE / "ACTUAL_CONTROLLED_ROWS.json").write_text(json.dumps(subset, indent=2) + "\n")
    (BASE / "ACTUAL_MATCHED_COMPARISONS.json").write_text(json.dumps(comparisons, separators=(",", ":")) + "\n")
    compact_cols = ["reaction_id", "sample", "experiment", "catalyst_name", "no_metal", "target_smiles", "target_yield_pct", "side_yield_pct", "target_fraction_among_reported_products"]
    (BASE / "MEASURED_YIELDS.json").write_text(json.dumps({"columns": compact_cols, "rows": [[r[k] for k in compact_cols] for r in records]}, separators=(",", ":")) + "\n")
    (BASE / "REACTION_EXAMPLES.json").write_text(json.dumps(examples, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
