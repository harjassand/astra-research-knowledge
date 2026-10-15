"""Root-adjudicated record assembly; no authority application or Git mutations."""
from pathlib import Path
import hashlib
import json

R = Path(__file__).resolve().parents[1]
PREFIX = "updates/FW-moving-heat-observable-20261015/"
BASE = "8a1e001ac128468ae8d151c9a859b89ef3b9a664"
draft = R / "workers/curation_draft/v0003"
curation = json.loads((draft / "CURATION_INPUT.DRAFT.json").read_bytes())
selection = json.loads((draft / "DRAFT_SELECTED_FREEZE.json").read_bytes())
assert curation["base_revision"] == selection["base_revision"] == BASE
entries = {x["research_relative_path"]: x for x in selection["files"]}
allowed = {".md", ".txt", ".json", ".jsonl", ".py", ".csv", ".tsv", ".sh", ".tex"}
skip_dirs = {"sources", "tmp", "__pycache__", ".venv", "venv", ".git", "data"}
workers = [
    "moving_kernel_genesis", "smooth_null_classification", "obstruction_escape",
    "pulse_physical_validation", "pulse_observable_genesis", "dislocation_operation",
    "failure_capital_genesis", "control_acquisition_genesis", "source_identity_luna",
    "sharp_floor_independent", "sharp_boundary_qc", "nonlinear_flow_audit",
    "external_capital_luna", "interacting_bridge_audit", "contact_face_priority_audit",
    "sharp_certificate_audit", "pulse_hardpair_audit",
]

def add_file(path):
    rel = str(path.relative_to(R))
    raw = path.read_bytes()
    if rel in entries:
        assert hashlib.sha256(raw).hexdigest() == entries[rel]["sha256"], "Frozen draft source changed: " + rel
        entries[rel]["selection_reason"] = "Root reviewed exact final proof, scoped check, comparator, failure or acquisition receipt and its replay dependencies."
        return
    review = any(name in rel for name in ("_audit/", "_independent/", "source_identity_luna/", "external_capital_luna/"))
    role = "root_or_worker_executable_check" if path.suffix == ".py" else (
        "root_synthesis" if rel.startswith("root/") else "same_team_review" if review else "worker_derivation")
    kind = "code" if path.suffix == ".py" else "receipt" if path.suffix in {".json", ".jsonl", ".csv", ".tsv"} else "review" if review else "proof"
    entries[rel] = {"research_relative_path": rel, "path": PREFIX + "package/derived/" + rel,
                    "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "provenance_role": role, "payload_kind": kind,
                    "contains_external_fulltext": False, "contains_full_lj_network_or_coordinates": False,
                    "selection_reason": "Root-selected authored proof/check/review, scoped unsuccessful route, exact input snapshot or acquisition pointer; no external fulltext or binary dataset."}

for worker in workers:
    for path in (R / "workers" / worker).rglob("*"):
        if path.is_file() and path.suffix in allowed and not path.is_symlink():
            parts = path.relative_to(R / "workers" / worker).parts
            if not any(x in skip_dirs for x in parts[:-1]):
                add_file(path)
for path in (R / "root").glob("*"):
    if path.is_file() and path.suffix in allowed and path.name not in {
        "SELECTED_FREEZE.v0001.json", "CURATION_INPUT.root-final.v0001.json"}:
        add_file(path)

def index(rel, sid, title, key):
    ent = entries[rel]
    if not any(x["path"] == ent["path"] for x in curation["sources"]):
        curation["sources"].append({"path": ent["path"], "sha256": ent["sha256"], "source_id": sid,
            "title": title, "read_depth": "Root read the stated proof/limits; same-team analytic and exact reconstruction are separately cited. Historical priority and external review remain UNKNOWN.",
            "provenance_role": ent["provenance_role"]})
    curation["evidence"][key] = {"path": ent["path"], "sha256": ent["sha256"], "source_id": sid,
        "lines": [1, len((R / rel).read_text().splitlines())], "hash_kind": "original_utf8_bytes",
        "range_scope": title, "source_revision": None,
        "status": "source_derived_unreviewed; internal proof/check scope only; external review, priority and physical capability UNKNOWN"}

index("root/POSITIVE_OUTPUT_OPERATOR_OBSTRUCTION.md", "src-FW-MHO-positive-output-root", "All-output positive sharp-branch obstruction and finite generation boundary", "positive_all_output")
index("workers/sharp_boundary_qc/POSITIVE_INPUT_HEAT_OBSTRUCTION.txt", "src-FW-MHO-positive-input-proof", "Universal positive input-heat non-SOS separation", "positive_input_proof")
index("workers/sharp_certificate_audit/POSITIVE_AUDIT_REPORT.txt", "src-FW-MHO-positive-input-audit", "Independent exact reconstruction of all 411 necessary constraints and dual", "positive_input_audit")
index("workers/sharp_floor_independent/positive_branch/OUTPUT_SKEW_REDUCTION.md", "src-FW-MHO-positive-skew-independent", "Independent exhaustive output-operator reduction and skew elimination", "positive_skew_independent")
index("workers/contact_face_priority_audit/PRIORITY_AUDIT.txt", "src-FW-MHO-primary-priority-comparison", "Primary predecessor and applicability comparison; priority unresolved", "primary_priority_comparison")
index("root/SCIENTIFIC_SYNTHESIS.md", "src-FW-MHO-root-scientific-synthesis", "Root decision-grade scientific synthesis and continuation decisions", "root_synthesis")

card = curation["cards"][0]
card["statement"] += " For every sharp r>0, no fixed real constant strongly parabolic output-matrix linear operator admits a pointwise nonnegative quadratic closed-form corrected heat density, without an SOS restriction. The Peano tangent reduction excludes the corresponding smooth adaptive local class. Finite positive generation by invariant heat-certificate quartics plus arbitrary PC addends is also impossible; this does not refute QC."
card["proof_refs"] += ["positive_input_proof", "positive_input_audit", "positive_skew_independent", "positive_all_output"]
card["inventory_refs"] += ["root_synthesis", "primary_priority_comparison"]
card["proof_spine"] += ["The positive-input dual contradicts an actual compatible jet; exhaustive output averaging and the independent flat-contact Hessian identity force the only surviving skew coefficient to zero."]
card["paragraphs"] += ["The new positive-branch no-go covers all fixed real strongly parabolic output-matrix linear generators, then the stated smooth Peano tangent class. It is a method limitation, not a negative Jensen field or a non-QC theorem. The corrected root flat-curve formula, including its nonzero order-t4 skew term, is preserved with its initial-draft correction receipt."]
card["costs"] = "Exact coefficient reconstruction, rational matrix arithmetic and symbolic sign proofs are paid. The two LMIs give a small decision criterion within this explicit face, not a general quartic QC algorithm. Interior coercivity is explicit; no positive boundary margin, practical storage solver or physical implementation is inferred."
curation["notices"].append({"notice_id": "SN-FW-MHO-positive-sharp-method-boundary",
    "card_ids": [card["id"], curation["cards"][1]["id"]],
    "issue": "All-operator local-certificate failure is not failure of quasiconvexity.",
    "clarification": "Every r>0 sharp generator excludes the whole stated constant strongly parabolic output-matrix/local-quadratic-null class, not merely one SOS ansatz. Continuous adaptive operators with Peano-second-order null corrections reduce to this forbidden tangent. QC remains UNKNOWN; singular, degenerate, integrated nonlocal and higher-jet operations need a different proof.",
    "ref_ids": ["positive_input_proof", "positive_input_audit", "positive_skew_independent", "positive_all_output", "tangent_proof"]})
for evidence in curation["evidence"].values():
    evidence["status"] = "source_derived_unreviewed; supplied information, internal derivations and same-team checking are separately attributed in the artifact; no external review, priority or physical certification."

selection.update(status="root_frozen", selected_by="root", files=sorted(entries.values(), key=lambda x: x["path"]))
selection["total_files"] = len(selection["files"])
selection["total_bytes"] = sum(x["bytes"] for x in selection["files"])
selection["scope"] = "Root-adjudicated source-separated scientific preservation, exact proofs, adversarial checks, failures and replay dependencies; external correctness/priority/physical capability remain unresolved."
freeze = R / "root/SELECTED_FREEZE.v0001.json"
freeze.write_text(json.dumps(selection, indent=2, ensure_ascii=False) + "\n")
curation.update(curated_by="root", curation_status="root_final", checkpoint_path=None,
    checkpoint_draft_path=PREFIX + "CHECKPOINT_RECORD.integrated-draft.v0001.json",
    selected_freeze={"path": PREFIX + freeze.name, "sha256": hashlib.sha256(freeze.read_bytes()).hexdigest()})
curation["draft_metadata"] = {"review_history": "Three versioned worker drafts retained; final scientific scope/selection adjudicated by root after separate exact and analytic reviews.",
    "initial_source_revision": "33c1ff7ebd9411e9b8b4b0f951f62e36e631cb5d", "reconciled_base_revision": BASE}
(R / "root/CURATION_INPUT.root-final.v0001.json").write_text(json.dumps(curation, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"selected_files": selection["total_files"], "selected_bytes": selection["total_bytes"],
    "sources": len(curation["sources"]), "evidence_ranges": len(curation["evidence"]),
    "freeze_sha256": curation["selected_freeze"]["sha256"]}))
