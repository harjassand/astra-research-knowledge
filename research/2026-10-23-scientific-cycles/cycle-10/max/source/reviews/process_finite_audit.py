"""Finite source audit for the Cycle10 process review.

Reads frozen files and performs descriptive arithmetic only.  Does not import or
execute producer scientific scripts, refit kinetics, simulate chemistry, use the
network, alter inputs, or inspect a live repository.
"""
from pathlib import Path
from decimal import Decimal, getcontext
from collections import Counter
import csv
import hashlib
import json

getcontext().prec = 40
ROOT = Path(__file__).resolve().parents[1]
INPUTS = ROOT / "inputs"
DOTS = INPUTS / "dots/nitrogen_cycle9_20261022"
MAX = INPUTS / "max/Astra_Amplification_Cycle9_MAX_20261022"
COLLECTION = INPUTS / "collection"

def read_json(path):
    return json.loads(path.read_text())

def identity(path):
    blob = path.read_bytes()
    return {"path": str(path.relative_to(ROOT)), "bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest()}

metadata = read_json(DOTS / "nitrite_finishing/zenodo_metadata.json")
dataset_checks = []
for spec in metadata["files"]:
    p = DOTS / "nitrite_finishing/dataset" / spec["key"]
    b = p.read_bytes()
    actual = "md5:" + hashlib.md5(b).hexdigest()
    dataset_checks.append({"file": spec["key"], "bytes": len(b),
                           "metadata_bytes_match": len(b) == spec["size"],
                           "metadata_md5_match": actual == spec["checksum"]})
assert all(x["metadata_bytes_match"] and x["metadata_md5_match"] for x in dataset_checks)

with (DOTS / "nitrite_finishing/dataset/Figure_4.csv").open() as f:
    rows = list(csv.reader(f))
labels = [rows[0][i + 1] for i in (0, 2, 4)]
fixed = {}
initial = {}
for i, label in zip((0, 2, 4), labels):
    hits = [r for r in rows[1:] if r[i] and Decimal(r[i]) == 2700]
    assert len(hits) == 1
    fixed[label] = Decimal(hits[0][i + 1])
    initial[label] = Decimal(rows[1][i + 1])
a = fixed["air"] / 1000
increments = {k: (fixed[k] - initial[k]) / 1000 for k in labels}
control_arithmetic = {
    "fixed_time_s": 2700,
    "values_mM": fixed,
    "initial_values_mM": initial,
    "air_over_N2": fixed["air"] / fixed["N2"],
    "KSCN_over_air": fixed["25mM KSCN_air"] / fixed["air"],
    "conditional_air_yield": a,
    "conditional_redox_e_per_original_N": 8 * a - 6,
    "overstatement_percent_relative_to_corrected_yield": (a / Decimal("0.75") - 1) * 100,
    "downward_correction_percent_relative_to_apparent_yield": (1 - Decimal("0.75") / a) * 100,
    "additive_correction_mM_to_750": fixed["air"] - 750,
    "initial_subtraction_stress_test_increments": increments,
    "stress_test_air_over_N2_increment": increments["air"] / increments["N2"],
    "scope": "Exact listed rows and conditional arithmetic. Initial subtraction is a stress test, not validated background correction. No replication, uncertainty, true yield, oxygen-only chemistry or plant qualification follows."
}

calibration = read_json(DOTS / "native_reconstruction/dataset_result.json")["calibration"]
with (DOTS / "nitrite_finishing/dataset/Figure_3.csv").open() as f:
    pairs = list(csv.reader(f))[1:]
s = Decimal(str(calibration["ratio_vs_Ceff_slope"]))
b = Decimal(str(calibration["intercept"]))
residuals = [Decimal(y) - s * Decimal(x) - b for x, y in pairs]
calibration_check = {
    "point_count": len(pairs),
    "method": "Read CSV and evaluate the saved producer slope/intercept; no fit performed.",
    "max_abs_residual_equivalent_mM": max(abs(r) for r in residuals) / s,
    "scope": "Descriptive residual of a supplied line, not a measured cross-matrix bias or uncertainty bound."
}

api = read_json(COLLECTION / "branches/max/COMPLETED_API.json")
turn = json.loads(api["content"][0]["text"])["turns"][0]
items = turn["items"]
mcp = [i for i in items if i.get("type") == "mcpToolCall"]
types = Counter(i.get("type") for i in items)
tool_counts = Counter(i["tool"] for i in mcp)
duration_ms = {name: sum(i.get("durationMs", 0) for i in mcp if i["tool"] == name)
               for name in sorted(tool_counts)}
visible_audit = {
    "source": str((COLLECTION / "branches/max/COMPLETED_API.json").relative_to(ROOT)),
    "item_counts": dict(types),
    "Page_tool_counts": dict(tool_counts),
    "Page_reported_duration_sums_ms": duration_ms,
    "Page_reported_duration_sum_seconds": sum(duration_ms.values()) / 1000,
    "reasoning_items_with_visible_summary": sum(bool(i.get("summary")) for i in items if i.get("type") == "reasoning"),
    "scope": "Counts and duration fields of one exported turn only. Duration sums are service-duration accounting, not wall time, model cost or a productivity comparison. Empty reasoning items expose no hidden thought process."
}

whole = read_json(MAX / "evaluator/meta_representation/results/WHOLE_PROCESS_RECEIPTS.json")
arms = {r["arm"]: r for r in whole["receipts"]}
A = arms["A_counts_flags"]
B = arms["B_occupancy_flags"]
C = arms["C_occupancy_support_flags"]
meta_arithmetic = {
    "all_reported_closed": all(r["reason"] == "closed" for r in whole["receipts"]),
    "A_over_C_CPU": A["whole_process_cpu_seconds"] / C["whole_process_cpu_seconds"],
    "B_over_C_CPU": B["whole_process_cpu_seconds"] / C["whole_process_cpu_seconds"],
    "A_minus_C_CPU_seconds": A["whole_process_cpu_seconds"] - C["whole_process_cpu_seconds"],
    "summed_CPU_seconds": sum(r["whole_process_cpu_seconds"] for r in whole["receipts"]),
    "scope": "Arithmetic on producer receipts only; no search, adapter test, correctness certification or timing replication."
}

proof = MAX / "evaluator/prior_review_originals/meta/control/REPORT.md"
current_proof = identity(proof)
assert current_proof["bytes"] == 10396
assert current_proof["sha256"] == "3e20089344870144e1a0e6ee9ea0ce78abbec395382d1c69affc94010c45e1c0"

source_paths = [
    DOTS / "REPORT.md", DOTS / "PROCESS_RECORD.txt", DOTS / "RECEIVING_USE.txt",
    DOTS / "tracer_independent/PROOF_AND_FAILURE_CONDITIONS.md",
    DOTS / "tracer_independent/NATIVE_RECEIPT_CHECK.md",
    DOTS / "nitrite_finishing/dataset_calibration_audit.md",
    DOTS / "intervention_evidence/REPORT.md",
    MAX / "README.txt", MAX / "REPOSITORY_STATE.json", MAX / "COSTS.json",
    MAX / "evaluator/REPORT.txt", MAX / "evaluator/evidence/REPRESENTATION_ADJUDICATION.txt",
    MAX / "evaluator/evidence/CYCLE8_CURRENT_PROOF_CORRECTION.txt",
    COLLECTION / "branches/dots/CURRENT_CHECKPOINT_MESSAGES_RENDERED_DOM.json",
    COLLECTION / "branches/max/COMPLETED_API.json", COLLECTION / "SOURCE_EXPORT_LIMITS.json"
]
result = {
    "review": "Cycle10 independent process evidence analyst",
    "scope": "Finite source observations only; no producer scientific code, new chemistry, network or live GitHub operation.",
    "dataset_checks_against_archived_metadata": dataset_checks,
    "control_arithmetic": control_arithmetic,
    "calibration_check": calibration_check,
    "visible_Max_record": visible_audit,
    "prior_meta_receipt_arithmetic": meta_arithmetic,
    "current_control_proof_identity": current_proof,
    "selected_source_identities": [identity(p) for p in source_paths]
}
dest = Path(__file__).with_suffix(".json")
dest.write_text(json.dumps(result, indent=2, default=str) + "\n")
print(json.dumps({"output": str(dest), "all_dataset_metadata_checks_pass": True,
                  "fixed_time_air_mM": str(fixed["air"]),
                  "max_Page_calls": len(mcp), "max_Page_duration_sum_s": sum(duration_ms.values()) / 1000,
                  "current_proof_identity_pass": True, "no_producer_scripts_executed": True}, indent=2))
