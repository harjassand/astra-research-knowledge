#!/usr/bin/env python3
"""Freeze derived worker outputs and retain supplied/acquired provenance."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sympy
import numpy

ROOT = Path(__file__).resolve().parent
RESEARCH = ROOT.parents[1]
INPUT = RESEARCH / "originals/expanded/refresh_robustness_packet/refresh_robustness_packet"
PIN = "f937563cbc5d2249b8e0dd96bcbd3b8f78eb85c6"
ORIGINALS = [
    "robust_transfer/PROOF.md",
    "finite_pulse_obstruction/PROOF.md",
    "resolution_gate/RESULT.md",
    "prerequisites/causal_product.md",
    "prerequisites/schur_value.md",
    "prerequisites/scheduled_support.md",
    "prerequisites/original_memory_interface.md",
    "robust_transfer/check_exact.py",
]
PUBLISH = [
    "README.md", "DERIVATION.md", "COUNTEREXAMPLES.md", "PRIMARY_COMPARISON.md",
    "RESULT.json", "SOURCE_LEDGER.json", "tests/check_math.py", "tests/results.json",
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


intake = json.loads((RESEARCH / "SOURCE_MANIFEST.json").read_text())
assert intake["source_pin"] == PIN
initial = {entry["path"]: entry for entry in intake["members"]}
inputs = []
for relative in ORIGINALS:
    path = INPUT / relative
    intake_path = str(path.relative_to(RESEARCH))
    digest = sha(path)
    expected = initial[intake_path]["sha256"]
    assert digest == expected, (relative, digest, expected)
    inputs.append({"path": intake_path, "sha256": digest, "bytes": path.stat().st_size,
                   "role": "supplied original, read only",
                   "matches_root_intake_manifest": True})

checks = json.loads((ROOT / "tests/results.json").read_text())
assert checks["status"] == "PASS"
acquired = json.loads((ROOT / "acquired/acquisition_manifest.json").read_text())
for entry in acquired:
    assert entry["status"] == "ACQUIRED"
    assert sha(ROOT / entry["pdf_path"]) == entry["sha256"]
    assert sha(ROOT / entry["text_path"]) == entry["text_sha256"]
    entry["publication_policy"] = "metadata only; raw acquired PDF/text excluded"

ledger = {
    "schema": "astra.gf-robust-adversary.source-ledger.v1",
    "source_pin": PIN,
    "pin_evidence": "parent supplied pin also matches root intake SOURCE_MANIFEST.json; no Git operation",
    "original_sources": inputs,
    "acquired_sources": acquired,
    "publication_include": PUBLISH + ["FREEZE_MANIFEST.json"],
    "publication_exclude": ["acquired/**", "acquire_primary.py", "format_math.py", "freeze.py"],
    "acquisitions_segregated": True,
    "scientific_boundary": "Primary source evidence and finite checks are not external mathematical certification, historical novelty, device qualification, or original-generator transfer.",
    "execution_constraints": {
        "original_and_checkout_edits": False, "original_source_script_execution": False,
        "git_operations": False, "installations": False, "outreach": False,
        "nested_agents": False, "peer_result_reading": False,
    },
}
write_json(ROOT / "SOURCE_LEDGER.json", ledger)

result = {
    "schema": "astra.gf-robust-adversary.result.v1",
    "status": "STRONGER_CONDITIONAL_COHERENT_PRODUCT_DERIVED",
    "original_half_diamond_product": "RECONSTRUCTED_WITH_STRICT_LOCAL_FULL_JOINT_CAUSAL_CONTRACT",
    "stronger_factor": "sin^2(min(pi/2, asin(sqrt(f_i)) + delta_i))",
    "generic_weighted_cost": "b_a(N|T)=(||N-aT||_diamond+1-a)/2",
    "coherent_action_contract": "uniform full-joint local unitary/dilation or primitive-local Hamiltonian residual; fixed exact ideal reference tester",
    "stronger_result_scope": "source-relative application of established CP/convex and state/Bures-angle ingredients to causal first-erasure products",
    "support_requirement": "actual exact trusted endpoints with immutable genuine comparator, and correctability of the union of all propagated actual memory-error footprints",
    "actual_bad_event": "endpoint mismatch t_i != r_i, not ANY internal block mismatch",
    "original_generator_transfer": "NOT_ESTABLISHED",
    "physical_refresh_qualification": "NOT_ACHIEVED",
    "new_physical_operation": "NONE_QUALIFIED",
    "historical_novelty": "UNKNOWN",
    "external_review": "NOT_PERFORMED",
    "finite_checks": {
        "status": checks["status"],
        "shared_bath_full_input_fixtures": checks["shared_bath_full_input_effect_tests"]["fixtures"],
        "cross_parent_error_commutator_norm": checks["shared_bath_full_input_effect_tests"]["noncommuting_cross_parent_bath_error_commutator_norm"],
        "min_numerical_domination_slack": checks["shared_bath_full_input_effect_tests"]["minimum_slack"],
        "scope": checks["scope"],
        "test_development_correction": "Initial small-example fixture incorrectly used the triple 3,40,41; its normalization assertion failed. Replaced by the valid triple 200,9999,10001. Final exact and numerical checks passed.",
    },
    "runtime": {"sympy": sympy.__version__, "numpy": numpy.__version__},
    "publication_excluded_raw_acquisition_glob": "acquired/**",
}
write_json(ROOT / "RESULT.json", result)

for relative in PUBLISH:
    assert (ROOT / relative).is_file()
for relative in ("DERIVATION.md", "README.md"):
    content = (ROOT / relative).read_text()
    assert content.count(r"\[") == content.count(r"\]"), relative
    assert content.count(r"\(") == content.count(r"\)"), relative

manifest = {
    "schema": "astra.gf-robust-adversary.freeze.v1",
    "frozen_utc": datetime.now(timezone.utc).isoformat(),
    "source_pin": PIN,
    "status": "FROZEN",
    "original_source_hash_checks": "PASS, all eight read original sources match root intake",
    "test_status": "PASS",
    "publication_exclude": ledger["publication_exclude"],
    "files": [{"path": relative, "sha256": sha(ROOT / relative),
               "bytes": (ROOT / relative).stat().st_size} for relative in PUBLISH],
    "self_hash": "not included; parent publication manifest may hash this file",
}
write_json(ROOT / "FREEZE_MANIFEST.json", manifest)
print(json.dumps({"status": "FROZEN", "original_sources_unchanged": len(inputs),
                  "derived_publication_files_hashed": len(PUBLISH),
                  "acquired_primary_papers_excluded": len(acquired),
                  "finite_checks": "PASS"}, indent=2))
