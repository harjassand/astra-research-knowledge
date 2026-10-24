#!/usr/bin/env python3
"""Threshold-free decisions on actual ORD labels, not independent product truth.

Run with the bundled Python. Dependencies are reused read-only from chemistry_search.
All product quantities are decoded from protobuf float values. No labels are clipped.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import re
import statistics
import sys
import time

BASE = Path(__file__).resolve().parent
SEARCH = BASE.parent / "chemistry_search"
sys.path.insert(0, str(SEARCH / ".python_packages"))
import pyarrow.parquet as pq
from google.protobuf.json_format import MessageToDict
from ord_schema.proto import reaction_pb2


def js(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(js(value).encode()).hexdigest()


def identity(component):
    ids = component.get("identifiers", [])
    for kind in ("SMILES", "INCHI", "NAME"):
        values = sorted({i["value"] for i in ids if i.get("type") == kind})
        if values:
            return [kind, values]
    return ["UNKNOWN", []]


def named(component):
    return next((i["value"] for i in component.get("identifiers", []) if i.get("type") == "NAME"), None)


def canonical_component(component):
    # Source CUSTOM codes have verified disagreements with structured chemistry.
    return {**{k: v for k, v in component.items() if k != "identifiers"}, "chemical_identity": identity(component)}


def input_chemistry(r):
    nonmetal_inputs, solvents = {}, defaultdict(float)
    catalyst = []
    for key, inp in r["inputs"].items():
        non_solvent = []
        for comp in inp.get("components", []):
            if comp.get("reaction_role") == "SOLVENT":
                amount = comp.get("amount", {})
                if set(amount) <= {"volume", "volume_includes_solutes"} and "volume" in amount:
                    v = amount["volume"]
                    solvents[(js(identity(comp)), v.get("units"), amount.get("volume_includes_solutes", False))] += v.get("value", 0)
                else:
                    # Fail closed rather than silently discarding a non-volume solvent amount.
                    raise ValueError((r["reaction_id"], "unexpected solvent", amount))
            elif key == "catalyst soln":
                catalyst.append(canonical_component(comp))
            else:
                non_solvent.append(canonical_component(comp))
        # Retain dispensing/addition metadata, including catalyst addition order.
        nonmetal_inputs[key] = {**{k: v for k, v in inp.items() if k != "components"}, "components": sorted(non_solvent, key=js)}
    solvent_vector = [[json.loads(i), units, inc, round(v, 12)] for (i, units, inc), v in sorted(solvents.items())]
    return nonmetal_inputs, solvent_vector, sorted(catalyst, key=js)


def value_for(product, kind):
    ms = [m for m in product.measurements if m.type == kind]
    assert len(ms) == 1, (product, kind)
    assert ms[0].HasField("percentage")
    return float(ms[0].percentage.value)


def summary_action(r):
    return {k: r[k] for k in ("reaction_id", "sample", "experiment", "temperature_c", "feed", "catalyst", "ligand", "base", "solvents", "T", "S", "physical_consistency") if k in r}


def pareto(rows):
    """Distinct nondominated (maximize T, minimize S) source-label vectors."""
    vectors = defaultdict(list)
    for r in rows:
        vectors[(r["S"], r["T"])].append(r)
    points = []
    best_t = -math.inf
    for (s, t), rs in sorted(vectors.items(), key=lambda item: (item[0][0], -item[0][1])):
        if t > best_t:
            points.append({"S": s, "T": t, "rows": rs})
            best_t = t
    return points


def slope(a, b):
    return (b["T"] - a["T"]) / (b["S"] - a["S"])


def slope_exact(a, b):
    return (Fraction(b["T"]) - Fraction(a["T"])) / (Fraction(b["S"]) - Fraction(a["S"]))


def support_envelope(points):
    """All exposed actions for U=T-lambda*S, for every lambda >= 0."""
    hull = []
    for p in points:
        while len(hull) >= 2 and slope_exact(hull[-2], hull[-1]) <= slope_exact(hull[-1], p):
            hull.pop()
        hull.append(p)
    result = []
    for i, p in enumerate(hull):
        low_exact = slope_exact(p, hull[i + 1]) if i + 1 < len(hull) else Fraction(0)
        high_exact = slope_exact(hull[i - 1], p) if i else None
        low, high = float(low_exact), float(high_exact) if high_exact is not None else None
        # Verify the full interval by every competitor at both finite endpoints;
        # linear differences then retain sign throughout. Unbounded end requires
        # smallest S and is also checked explicitly.
        for competitor in points:
            for lam in (low_exact, high_exact):
                if lam is not None:
                    assert Fraction(p["T"])-lam*Fraction(p["S"]) >= Fraction(competitor["T"])-lam*Fraction(competitor["S"])
            if high_exact is None:
                assert p["S"] <= competitor["S"]
        result.append({"T": p["T"], "S": p["S"], "lambda_min": low, "lambda_max": high,
                       "lambda_min_exact_source_label_rational": str(low_exact),
                       "lambda_max_exact_source_label_rational": str(high_exact) if high_exact is not None else None,
                       "lambda_max_null_means_infinity": high is None,
                       "tied_vector_count": len(p["rows"]),
                       "representative": summary_action(p["rows"][0])})
    return result


def frontier_output(rows):
    pts = pareto(rows)
    out = []
    for p in pts:
        out.append({"T": p["T"], "S": p["S"], "tied_vector_count": len(p["rows"]), "representative": summary_action(p["rows"][0])})
    # Two top distinct vectors establish the target-only worst-case margin.
    # Two measurements each with coordinate error <=eps need delta_T>2eps.
    distinct = sorted({(r["T"], r["S"]) for r in rows}, key=lambda z:(-z[0],z[1]))
    target_levels = sorted({t for t,s in distinct},reverse=True)
    best_t = target_levels[0]
    next_t = target_levels[1] if len(target_levels)>1 else None
    total_best = max(rows,key=lambda r:r["T"]+r["S"])
    top = {"max_target_yield_label": best_t, "next_distinct_target_yield_label": next_t,
           "target_order_equal_absolute_error_radius_pct_points": (best_t-next_t)/2 if next_t is not None else None,
           "target_maximizers": [summary_action(r) for r in rows if r["T"]==best_t][:10],
           "total_yield_argmax_representative": summary_action(total_best),
           "total_yield_argmax_is_target_maximizer": total_best["T"]==best_t,
           "total_yield_argmax_pareto_dominated": any(p["T"]>=total_best["T"] and p["S"]<=total_best["S"] and (p["T"]>total_best["T"] or p["S"]<total_best["S"]) for p in pts)}
    return {"rows": len(rows), "distinct_pareto_vectors": len(pts), "pareto_vectors": out, "support_envelope": support_envelope(pts), "target_only_and_total_yield_ranking": top}


def sign(x):
    return "positive" if x > 0 else "negative" if x < 0 else "zero"


def quantiles(xs):
    xs = sorted(xs)
    if not xs:
        return None
    def q(p):
        pos = p * (len(xs) - 1)
        lo, hi = math.floor(pos), math.ceil(pos)
        return xs[lo] * (hi-pos) + xs[hi] * (pos-lo) if hi != lo else xs[lo]
    return {"min": xs[0], "q25": q(.25), "median": q(.5), "q75": q(.75), "max": xs[-1]}


def finite_mean(xs):
    return statistics.mean(xs)


def main():
    started = time.perf_counter()
    source = SEARCH / "ord_dataset-805ad863feef48579d95d86a728035f4.parquet"
    rows, feeds, units, measurement_fields = [], {}, Counter(), Counter()
    for batch in pq.ParquetFile(source).iter_batches(batch_size=1024):
        for raw in batch.to_pylist():
            p = reaction_pb2.Reaction.FromString(raw["reaction"])
            assert raw["reaction_id"] == p.reaction_id
            assert len(p.outcomes) == 1
            desired = [x for x in p.outcomes[0].products if x.is_desired_product]
            sides = [x for x in p.outcomes[0].products if x.reaction_role == reaction_pb2.ReactionRole.SIDE_PRODUCT]
            assert len(desired) == len(sides) == 1
            T, S = value_for(desired[0], reaction_pb2.ProductMeasurement.YIELD), value_for(sides[0], reaction_pb2.ProductMeasurement.YIELD)
            assert math.isfinite(T) and math.isfinite(S)
            r = MessageToDict(p, preserving_proto_field_name=True)
            custom = {i["details"]: i["value"] for i in r["identifiers"] if i.get("type") == "CUSTOM"}
            inputs, solvents, catalyst = input_chemistry(r)
            target = identity(MessageToDict(desired[0], preserving_proto_field_name=True))
            feed = {key: [{"identity": identity(c), "amount": c.get("amount"), "limiting": c.get("is_limiting")} for c in r["inputs"][key]["components"] if c.get("reaction_role") == "REACTANT"] for key in ("electrophile soln", "nucleophile soln")}
            feed["desired_product"] = target
            feed_key = digest(feed)
            feeds[feed_key] = feed
            control_key = {"inputs": inputs, "solvents": solvents, "conditions": r.get("conditions", {}), "setup": r.get("setup", {}), "workups": r.get("workups", []), "reaction_time": r["outcomes"][0].get("reaction_time"), "target": target}
            recipe_key = digest({**control_key, "catalyst": catalyst})
            temperature = r["conditions"]["temperature"]["setpoint"]
            assert temperature["units"] == "CELSIUS"
            cat_names = [named(c) for c in r["inputs"]["catalyst soln"]["components"] if c.get("reaction_role") != "SOLVENT"]
            no_metal = cat_names == ["none"]
            consistency = "negative_component" if min(T, S) < 0 else "sum_above_100" if T+S > 100 else "within_stoichiometric_simplex"
            rec = {"reaction_id": p.reaction_id, "sample": custom["Sample Name_x"], "experiment": custom["experiment"], "temperature_c": temperature["value"], "feed_key": feed_key, "feed": feed, "T": T, "S": S, "no_metal": no_metal, "catalyst": cat_names, "ligand": [named(c) for c in r["inputs"]["ligand soln"]["components"] if c.get("reaction_role") != "SOLVENT"], "base": [named(c) for c in r["inputs"]["base"]["components"] if c.get("reaction_role") != "SOLVENT"], "solvents": solvents, "matching_key": digest(control_key), "recipe_key": recipe_key, "physical_consistency": consistency}
            # Analytical-subplate string is retained as a nuisance label only.
            rec["subplate"] = re.sub(r"[_-](?:[A-Pa-p]\d{1,2}|\d+)$", "", rec["sample"])
            rows.append(rec)
            for product in (desired[0], sides[0]):
                for m in product.measurements:
                    if m.type == m.YIELD:
                        measurement_fields[tuple(f.name for f, _ in m.percentage.ListFields())] += 1
            for inp in p.inputs.values():
                for comp in inp.components:
                    if comp.is_limiting:
                        units[(float(comp.amount.moles.value), comp.amount.moles.units)] += 1

    by_feed, by_control, by_recipe = defaultdict(list), defaultdict(list), defaultdict(list)
    for r in rows:
        by_feed[r["feed_key"]].append(r)
        by_control[(r["experiment"], r["matching_key"])].append(r)
        by_recipe[r["recipe_key"]].append(r)
    frontiers = {}
    for k, rs in by_feed.items():
        good = [r for r in rs if r["physical_consistency"] == "within_stoichiometric_simplex"]
        controls = [r for r in rs if r["no_metal"]]
        good_controls = [r for r in controls if r["physical_consistency"] == "within_stoichiometric_simplex"]
        # Same recipe means are descriptive aggregation, not independent batch estimates.
        recipe_means = []
        for key, observations in by_recipe.items():
            if observations[0]["feed_key"] != k:
                continue
            x = dict(observations[0])
            x.update(T=finite_mean([r["T"] for r in observations]), S=finite_mean([r["S"] for r in observations]))
            x["reaction_id"] = "recipe:" + key
            x["observation_count"] = len(observations)
            recipe_means.append(x)
        frontiers[k] = {"feed": feeds[k], "physical_consistency_counts": dict(Counter(r["physical_consistency"] for r in rs)), "raw_all_source_labels": frontier_output(rs), "stoichiometrically_consistent_source_labels": frontier_output(good), "no_metal_raw_labels": frontier_output(controls), "no_metal_consistent_labels": frontier_output(good_controls), "raw_recipe_means": frontier_output(recipe_means)}

    matched, signs, physical_signs, scope = [], Counter(), Counter(), Counter()
    for key, rs in by_control.items():
        controls = [r for r in rs if r["no_metal"]]
        treated = [r for r in rs if not r["no_metal"]]
        if not controls:
            scope["unmatched_treatment_rows"] += len(treated)
            continue
        cT, cS = finite_mean([r["T"] for r in controls]), finite_mean([r["S"] for r in controls])
        for r in treated:
            dT, dS = r["T"]-cT, r["S"]-cS
            quadrant = sign(dT) + "_T__" + sign(dS) + "_S"
            signs[quadrant] += 1
            good = r["physical_consistency"] == "within_stoichiometric_simplex" and all(c["physical_consistency"] == "within_stoichiometric_simplex" for c in controls)
            if good:
                physical_signs[quadrant] += 1
            same_subplate = [c for c in controls if c["subplate"] == r["subplate"]]
            scope["matched_treatment_rows"] += 1
            scope["same_subplate_available"] += bool(same_subplate)
            scope["control_well_count_greater_than_one"] += len(controls) > 1
            scope["all_components_consistent_matched_rows"] += good
            if dT >= 0 and dS <= 0 and (dT > 0 or dS < 0):
                decision = "metal_assay_vector_dominates_control_mean"
            elif dT <= 0 and dS >= 0 and (dT < 0 or dS > 0):
                decision = "control_mean_assay_vector_dominates_metal"
            elif dT == dS == 0:
                decision = "identical_assay_vector"
            else:
                decision = "tradeoff"
            scope[decision] += 1
            # Equal absolute per-coordinate error eps on each T/S measurement:
            # utility difference worst-case perturbation is 2*eps*(1+lambda).
            # eps_star(lambda)=abs(dT-lambda*dS)/(2*(1+lambda)).
            m = {"reaction_id": r["reaction_id"], "sample": r["sample"], "experiment": r["experiment"], "feed_key": r["feed_key"], "catalyst": r["catalyst"], "T": r["T"], "S": r["S"], "control_mean_T": cT, "control_mean_S": cS, "delta_T": dT, "delta_S": dS, "label_decision": decision, "all_labels_stoichiometrically_consistent": good, "control_ids": [c["reaction_id"] for c in controls], "control_wells": len(controls), "same_subplate_control_available": bool(same_subplate), "utility_switch_lambda": dT/dS if dT*dS > 0 else None, "target_order_equal_absolute_error_radius_pct_points": abs(dT)/2, "side_order_equal_absolute_error_radius_pct_points": abs(dS)/2}
            matched.append(m)

    repeated = [rs for rs in by_recipe.values() if len(rs) > 1]
    repeat_summary = {"distinct_recipe_keys": len(by_recipe), "recipe_observation_counts": dict(Counter(len(rs) for rs in by_recipe.values())), "recipes_with_multiple_experiments": sum(len({r["experiment"] for r in rs}) > 1 for rs in by_recipe.values()), "repeated_recipe_target_range_pct_points": quantiles([max(r["T"] for r in rs)-min(r["T"] for r in rs) for rs in repeated]), "repeated_recipe_side_range_pct_points": quantiles([max(r["S"] for r in rs)-min(r["S"] for r in rs) for rs in repeated]), "meaning": "Matching uses identical structured chemistry, dispensing metadata, conditions, workups, setup and target/time; observed repeats are not asserted to be independent batches."}
    # Only actual induced utility-switch penalties are saved; no chosen favorable threshold.
    switches = [m["utility_switch_lambda"] for m in matched if m["utility_switch_lambda"] is not None]
    summary = {"created_at_utc": datetime.now(timezone.utc).isoformat(), "source_path": str(source), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "status": "SOURCE_ASSAY_DECISION_AUDIT_ONLY", "rows": len(rows), "fixed_feed_count": len(feeds), "physical_consistency_counts": dict(Counter(r["physical_consistency"] for r in rows)), "yield_range_pct_points": {"T": [min(r["T"] for r in rows), max(r["T"] for r in rows)], "S": [min(r["S"] for r in rows), max(r["S"] for r in rows)]}, "limiting_amounts": [{"value": x[0], "protobuf_units_enum": x[1], "rows": n} for x,n in units.items()], "percentage_populated_field_counts": [{"fields": list(k), "measurements": v} for k,v in measurement_fields.items()], "matching_scope": dict(scope), "matched_delta_signs_all_labels": dict(signs), "matched_delta_signs_all_components_consistent": dict(physical_signs), "matched_delta_T_pct_points": quantiles([m["delta_T"] for m in matched]), "matched_delta_S_pct_points": quantiles([m["delta_S"] for m in matched]), "matched_tradeoff_switch_lambdas": quantiles(switches), "target_order_equal_absolute_error_radii_pct_points": quantiles([m["target_order_equal_absolute_error_radius_pct_points"] for m in matched]), "recipe_repeats": repeat_summary, "frontier_file": "FRONTIERS.json", "matched_file": "MATCHED_DECISIONS.json", "inference_tokens": "UNKNOWN", "inference_cost": "UNKNOWN", "energy": "UNKNOWN", "executed_code_wall_seconds": time.perf_counter()-started, "package_versions": {p: importlib.metadata.version(p) for p in ("pyarrow", "ord-schema", "protobuf")}, "limitations": ["All yields are producer-calibrated assays; no independent target-resolved mixture truth acquired.", "Raw label frontiers preserve negative and total-over-100 observations; the physical-consistency view exposes those cases without altering labels.", "No assay covariance or calibrated per-well error bounds are encoded in the inspected percentage fields.", "Pareto and penalty-envelope computations describe point labels and do not establish repeat synthesis, isolated recovery, purity, mechanistic attribution, or new information.", "Cross-subplate controls may share experiment and chemistry while retaining analytical nuisance differences.", "Unknown calibration gains, cross-talk and batch effects can alter utility rankings; conditional sensitivity radii are not achieved error bounds."]}
    (BASE / "AUDIT.json").write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n")
    (BASE / "FRONTIERS.json").write_text(json.dumps(frontiers, indent=2, allow_nan=False)+"\n")
    (BASE / "MATCHED_DECISIONS.json").write_text(json.dumps(matched, indent=2, allow_nan=False)+"\n")
    (BASE / "ANOMALOUS_LABEL_EXAMPLES.json").write_text(json.dumps([summary_action(r) for r in sorted(rows, key=lambda r:r["T"]+r["S"], reverse=True)[:30]] + [summary_action(r) for r in sorted(rows,key=lambda r:r["S"])[:30]],indent=2)+"\n")
    print(json.dumps(summary, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
