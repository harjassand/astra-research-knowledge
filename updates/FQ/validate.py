#!/usr/bin/env python3
"""FQ preservation checks; integrity and scope only, never scientific truth."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
BASE = "00631610750c708263d5cf6d812ebbb8edc77335"
CARD = "N822-matched-clock-three-snapshot-hidden-dissipation-certificate"
GATE = "G-FQ-N822-OPERATIONAL-INTERFACE"
BRIDGES = {
    "FQ_N512_affinity_to_matched_snapshot",
    "FQ_snapshot_to_N507_all_word_CP",
    "FQ_N541_discrete_chain_to_CTMC_sampling",
}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def load(path: str):
    return json.loads((ROOT / path).read_text())


def sha(path: str) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True)


def rows(path: str):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line]


def references(obj):
    if isinstance(obj, dict):
        if isinstance(obj.get("path"), str) and isinstance(obj.get("sha256"), str):
            yield obj
        for value in obj.values():
            yield from references(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from references(value)


def check_reference(ref: dict) -> None:
    path = ref["path"]
    file = ROOT / path
    require(not Path(path).is_absolute() and file.resolve().is_relative_to(ROOT), f"unsafe path: {path}")
    require(file.is_file(), f"missing reference: {path}")
    require(sha(path) == ref["sha256"], f"hash drift: {path}")
    if "bytes" in ref:
        require(file.stat().st_size == ref["bytes"], f"byte drift: {path}")
    if ref.get("lines"):
        first, last = ref["lines"]
        require(1 <= first <= last <= len(file.read_text().splitlines()), f"line range: {path}")


def check_append_only(path: str) -> None:
    old = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{BASE}:{path}"])
    require((ROOT / path).read_bytes().startswith(old), f"not append-only: {path}")


def preflight() -> None:
    require(git("merge-base", "HEAD", BASE).strip() == BASE, "branch is not based on pinned main")
    require(git("branch", "--show-current").strip() == "codex/operational-closure-genesis", "wrong integration branch")
    prior = set(git("ls-tree", "-r", "--name-only", BASE).splitlines())
    require(not any(path.startswith("updates/FQ/") for path in prior), "FQ was already occupied at base")
    require(not any(path.startswith("cards/N822-") for path in prior), "N822 was already occupied at base")
    for path in ["updates/FQ/SYNTHESIS.md", f"cards/{CARD}.txt", "updates/FQ/validate.py"]:
        require((ROOT / path).is_file(), f"missing prepared file: {path}")
    # Prior raw claims, status sidecars, checkpoints, and update packets are immutable.
    changed = set(git("diff", "--name-only", BASE).splitlines())
    for path in changed & prior:
        require(not path.startswith(("cards/", "frontier/cards/", "frontier/review_cards/", "updates/", "state/checkpoints/")), f"historical file changed: {path}")


def complete() -> dict:
    preflight()
    manifest = load("updates/FQ/INTAKE_MANIFEST.json")
    require(manifest["base_revision"] == BASE and manifest["intake_id"] == "FQ", "manifest pin")
    listed = {record["path"] for record in manifest["files"]}
    actual = {
        str(path.relative_to(ROOT))
        for path in (ROOT / "updates/FQ/package").rglob("*")
        if path.is_file()
    }
    require(listed == actual, "packet file inventory differs from immutable intake manifest")
    for record in manifest["files"]:
        check_reference(record)
    source_manifest_path = manifest["source_manifest"]
    appendix_path = manifest["appendix_manifest"]
    require(sha(source_manifest_path) == manifest["source_manifest_sha256"], "original source manifest drift")
    require(sha(appendix_path) == manifest["appendix_manifest_sha256"], "appendix manifest drift")
    original = load(source_manifest_path)
    appendix = load(appendix_path)
    require(len(original["files"]) == 82 and len(appendix["files"]) == 2, "source inventory changed")
    require(appendix["parent_sha256"] == sha(source_manifest_path), "appendix parent pin")
    prefix = "updates/FQ/package/operational_closure_v1/"
    require({
        prefix + item["path"] for item in original["files"] + appendix["files"]
    } | {source_manifest_path, appendix_path} == listed, "source/appendix inventory coverage")
    for item in original["files"] + appendix["files"]:
        require(sha(prefix + item["path"]) == item["sha256"], "source manifest file drift")
        require((ROOT / (prefix + item["path"])).stat().st_size == item["bytes"], "source manifest byte drift")

    claims = load("updates/FQ/CLAIMS.json")
    require(claims["schema"] == "astra.intake-claim-map.v1" and claims["intake_id"] == "FQ", "claim schema")
    require([claim["id"] for claim in claims["claims"]] == [CARD], "claim set")
    require(claims["claims"][0]["status"] == "source_derived_unreviewed", "claim promotion")
    claim = claims["claims"][0]
    require(claim["source_path"] in listed, "claim source is outside preserved packet")
    require(sha(claim["source_path"]) == claim["source_sha256"], "claim source hash drift")
    require(claim["missing_artifacts"] == [], "intake still records missing source artifacts")
    status = load(f"frontier/cards/{CARD}.json")
    require(status["claim_status"] == "source_derived_unreviewed", "status promotion")
    require(status["card_path"] == f"cards/{CARD}.txt" and status["card_sha256"] == sha(status["card_path"]), "card hash")
    require("UNKNOWN" in status["scientific_scope_status"], "novelty/physical scope missing")

    bridges = load("updates/FQ/BRIDGES.json")["bridges"]
    require({bridge["id"] for bridge in bridges} == BRIDGES, "bridge set")
    states = {
        "PROVEN LOGICAL DEPENDENCY", "ESTABLISHED COMPATIBLE INTERFACE",
        "CANDIDATE CONNECTION", "INCOMPATIBLE ASSUMPTIONS", "REFUTED TRANSFER",
    }
    for bridge in bridges:
        require(bridge["state"] == bridge["status"] and bridge["state"] in states, "bridge state")
        require(load(f"mechanisms/bridges/{bridge['id']}.json") == bridge, "bridge mirror")
        for side in ("source_interface", "destination_interface"):
            require(all(bridge[side].get(key) for key in (
                "objects", "regime_and_quantifiers", "supplied_information",
                "acquired_information", "legal_access", "guarantee",
                "units_norm_and_precision", "costs",
            )), f"incomplete {side}: {bridge['id']}")

    notices = load("updates/FQ/SCOPED_NOTICES.json")
    require(len(notices) == 1 and notices[0]["notice_id"] == "SN-FQ-N512-N507-N541-SAMPLED-SCOPE", "notice set")
    recorded_notices = rows("agent/SEMANTIC_NOTICES.jsonl")
    require(notices[0] in recorded_notices, "notice ledger mirror")
    gates = [gate for gate in rows("frontier/OPEN_PROOF_GATES.jsonl") if gate["gate_id"].startswith("G-FQ-")]
    require(len(gates) == 1 and gates[0]["gate_id"] == GATE and gates[0]["status"] == "open", "one open gate")
    require(gates[0]["completion_evidence"] == [], "gate falsely closed")
    require(load("updates/FQ/GATE.json") == gates[0], "gate mirror")
    check_append_only("agent/SEMANTIC_NOTICES.jsonl")
    check_append_only("frontier/OPEN_PROOF_GATES.jsonl")
    for obj in (claims, status, bridges, notices, gates):
        for ref in references(obj):
            check_reference(ref)

    checkpoint_paths = list((ROOT / "state/checkpoints/worker-fq-operational-closure").glob("*.json"))
    require(len(checkpoint_paths) <= 1, "unexpected checkpoint multiplicity")
    if checkpoint_paths:
        import importlib.util
        spec = importlib.util.spec_from_file_location("publisher", ROOT / "state/publish_checkpoint.py")
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        checkpoint = load(str(checkpoint_paths[0].relative_to(ROOT)))
        module.validate_record(checkpoint, ROOT)
        require(checkpoint["base_revision"] == BASE, "checkpoint base")
    return {
        "status": "PASS_INTEGRITY_ONLY", "base_revision": BASE,
        "packet_files": len(listed), "original_science_files": len(original["files"]),
        "appendix_files": len(appendix["files"]), "claims": 1, "bridges": len(bridges),
        "notices": len(notices), "gates": len(gates),
        "individual_checkpoint": bool(checkpoint_paths),
        "scientific_truth_checked": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    if args.preflight:
        preflight()
        print(json.dumps({"status": "PASS_PREFLIGHT", "base_revision": BASE}))
    else:
        print(json.dumps(complete(), indent=2))
