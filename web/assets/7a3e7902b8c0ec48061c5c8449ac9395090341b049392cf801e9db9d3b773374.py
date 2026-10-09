"""Verify immutable proof/source hashes; inventory owned Cycle05 artifacts.

Integrity evidence only. This script does not verify any general theorem.
It reads only the owned directory and the four explicitly authorized
weighted dependency files, and writes only the owned MANIFEST.json.
"""

import hashlib
import json
from pathlib import Path


OWN = Path(__file__).resolve().parent
WORKSPACE = OWN.parents[3]
FROZEN = {
    "TRACIAL_B_INDEPENDENT_FREEZE.txt":
        "203cbe380011e6dbfc572b5aa8d32a155a573f807e0e4b41b118a46536a357bd",
    "WEIGHTED_C4_CONDITIONAL_ADDENDUM.txt":
        "964b93aab2eb39f341c416fcf4896360932416eb2dfce21bb80bae0413fc371b",
    "TRACIAL_POWER_ORBIT_PROOF.txt":
        "eca7ca5289c05ca8dda5cd15cd158dfe7b9cb6b162dec34a9b45d7228403a962",
    "NONCOMMUTING_MARGINAL_REPAIR_AUDIT.txt":
        "621856a8d18f05981827f72d37520df6225f2f7f598ba187d29dfdd284918150",
    "NONTRACIAL_Q_ORBIT_CONDITIONAL_PROOF.txt":
        "34b2a81b2bf576fd0d9433a0120dd0f17562ec3e5b5a71696e06f3b7c938dbb8",
    "DEPENDENCY_CLOSURE.txt":
        "598e0469c0f9e2499cbc3f79d823e03c35c45704237de37a2ef272b2b3e77a22",
    "ANTISYMMETRIC_INTERFACE_FALSIFIER.txt":
        "f06615ced85ac1a3880a382affe7f59d9d8cf48830f9a8825f69fe169e84bfe3",
    "CONSEQUENCES_AND_PRIMARY_COMPARISON.txt":
        "5bdd588f97ae46d95fbf563ec7ced69664f190dc18640ea537b26f7ba3704129",
}
AUTHORIZED_WEIGHTED = {
    "work/agents/covariant_obstruction_sol/cycle05_weighted_dirichlet/WEIGHTED_C4_PROOF.txt":
        "517fb90cfc750bd2bf5c070d9a9081459040b390eb029e93fcf03faaad7132c2",
    "work/agents/tensor_frame_sol/cycle05_weighted_blind/BLIND_BASELINE.txt":
        "e1f821d7a6ffe9eafdd50a9d0532d522e1e2258d8e9f6247268a55eb6cc45b12",
    "work/agents/tensor_frame_sol/cycle05_weighted_blind/POST_EXPOSURE_AUDIT.txt":
        "3db6cc70a946e9e5a397c940968ed3f1bc8bdae5fc1fd50f389c3b9eceb5eff8",
    "work/agents/covariant_obstruction_sol/cycle05_weighted_dirichlet/EXPOSED_AUDIT.txt":
        "c87c81497eaba2cfd892cf2f06a792727734ebc08c8078f737d4214646571b69",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(path, expected):
    actual = digest(path)
    if actual != expected:
        raise AssertionError(f"Immutable hash mismatch: {path}: {actual}")
    return actual


def main():
    for relative, expected in FROZEN.items():
        verify(OWN / relative, expected)
    dependency_records = []
    for relative, expected in AUTHORIZED_WEIGHTED.items():
        path = WORKSPACE / relative
        verify(path, expected)
        dependency_records.append({
            "path": relative,
            "sha256": expected,
            "bytes": path.stat().st_size,
            "scope": "AUTHORIZED_POST_FREEZE_WEIGHTED_DEPENDENCY",
        })

    primary = json.loads((OWN / "PRIMARY_SOURCE_REGISTRY.json").read_text())
    assert len(primary) == 8
    for record in primary:
        path = OWN / record["path"]
        verify(path, record["sha256"])
        assert path.stat().st_size == record["bytes"]

    opportunities = json.loads((OWN / "opportunities.json").read_text())
    assert len(opportunities["opportunities"]) == 1
    target = opportunities["opportunities"][0]
    assert target["proof_sha256"] == FROZEN[target["proof_artifact"]]
    assert target["consequences_sha256"] == FROZEN[target["consequences_artifact"]]
    assert target["load_bearing_gate"]["closure_sha256"] == FROZEN["DEPENDENCY_CLOSURE.txt"]

    finite = json.loads((OWN / "LOCAL_GATE_FINITE_CHECKS.json").read_text())
    assert finite["status"] == "PASS"
    assert finite["repair_cases"] == 240 and finite["weighted_cases"] == 24
    assert "not proof" in finite["scope"]

    records = []
    for path in sorted(OWN.rglob("*")):
        if not path.is_file() or path.name == "MANIFEST.json":
            continue
        relative = str(path.relative_to(OWN))
        if relative in FROZEN:
            scope = "IMMUTABLE_PROOF_OR_AUDIT_FREEZE"
        elif relative.startswith("primary/"):
            scope = "CACHED_PRIMARY_SOURCE"
        elif relative.endswith(".py"):
            scope = "OWNED_ACQUISITION_OR_FINITE_INTEGRITY_UTILITY"
        else:
            scope = "OWNED_REPORT_OR_SCOPED_EVIDENCE"
        records.append({
            "path": relative,
            "sha256": digest(path),
            "bytes": path.stat().st_size,
            "scope": scope,
        })

    manifest = {
        "schema_version": 1,
        "recorded_date": "2026-10-09",
        "worker": "foundational_transfer_sol",
        "cycle": "05",
        "artifact_count_excluding_manifest": len(records),
        "frozen_owned_hashes_verified": len(FROZEN),
        "authorized_dependency_hashes_verified": len(dependency_records),
        "primary_source_hashes_and_sizes_verified": len(primary),
        "integrity_is_not_mathematical_validation": True,
        "full_transfer_status": "INTERNALLY_RECONSTRUCTED_WEIGHTED_DEPENDENCY_CLOSED",
        "fresh_full_transfer_hostile_review": "PENDING_SEPARATELY_WITH_COORDINATOR",
        "external_validation_formal_replay_priority": "NOT_ESTABLISHED",
        "artifacts": records,
        "authorized_dependencies": dependency_records,
    }
    (OWN / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({
        "status": "PASS_INTEGRITY_ONLY",
        "owned_artifacts": len(records),
        "frozen_owned": len(FROZEN),
        "authorized_dependencies": len(dependency_records),
        "primary_sources": len(primary),
        "report_sha256": digest(OWN / "REPORT.txt"),
        "opportunities_sha256": digest(OWN / "opportunities.json"),
        "manifest_sha256": digest(OWN / "MANIFEST.json"),
    }, indent=2))


if __name__ == "__main__":
    main()
