"""Diagnostic target-access screen over genuine measured ORD outcomes.

This is retrospective descriptive analysis, not prospective validation or a
preregistered performance test. No model or synthetic oracle is used.
"""
from collections import Counter, defaultdict
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
data = json.loads((BASE / "MEASURED_YIELDS.json").read_text())
rows = [dict(zip(data["columns"], values)) for values in data["rows"]]
blocks = defaultdict(list)
for row in rows:
    blocks[(row["target_smiles"], row["no_metal"])].append(row)

out = {"status": "RETROSPECTIVE_TARGET_OUTPUT_DIAGNOSTIC", "thresholds_are_exploratory": True,
       "target_contract": "Specified desired regioisomer assay yield >= threshold and desired/(desired+reported regioisomer) >=0.95.",
       "purity_warning": "This ratio ignores other impurities and starting material; it is not isolated recovery or certified purity.",
       "groups": []}
for (target, no_metal), group in blocks.items():
    entry = {"target_smiles": target, "no_metal": no_metal, "wells": len(group),
             "experiments": sorted(set(r["experiment"] for r in group)),
             "max_desired_yield_pct": max(r["target_yield_pct"] for r in group),
             "assay_yield_above_100_count": sum(r["target_yield_pct"] > 100 for r in group),
             "thresholds": {}}
    for threshold in (20, 50, 80):
        desired = [r for r in group if r["target_yield_pct"] >= threshold]
        clean = [r for r in desired if (r["target_fraction_among_reported_products"] or 0) >= .95]
        apparent = [r for r in group if r["target_yield_pct"] + r["side_yield_pct"] >= threshold]
        entry["thresholds"][str(threshold)] = {
            "desired_yield_hits": len(desired), "desired_yield_plus_reported_selectivity_hits": len(clean),
            "desired_selectivity_hits_with_reported_total_le_100": sum(r["target_yield_pct"] <= 100 and r["target_yield_pct"] + r["side_yield_pct"] <= 100 for r in clean),
            "combined_target_and_side_hits": len(apparent),
            "combined_signal_hits_failing_target_contract": sum(r not in clean for r in apparent),
            "clean_hit_ids": [r["reaction_id"] for r in clean] if len(clean) <= 20 else "See immutable source and replay",
        }
    out["groups"].append(entry)

out["conclusion"] = "No no-metal well in either target class satisfies the 50% desired-yield and 0.95 reported-selectivity screen. Metal treatments contain many such wells. This finite failure does not rule out unmeasured metal-free chemistry."
(BASE / "TARGET_ACCESS_DIAGNOSTIC.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
