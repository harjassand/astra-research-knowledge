#!/usr/bin/env python3
"""Check the FM HIP source selection and public card wiring; no research replay."""

from __future__ import annotations

import hashlib
import html
import json
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from state.publish_checkpoint import validate_record, views

PACKET = Path("updates/FM/package/hip_capability_v1")
CARD_ID = "N815-hot-pore-access-and-isotope-clock-acquisition-boundaries"
ULTRA_COMMIT = "788beabca49c9821a86c8237b1328a53313a22c5"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: str | Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def assert_recorded(path: str, expected: str) -> bytes:
    target = (ROOT / path).resolve()
    assert target.is_relative_to(ROOT), path
    data = target.read_bytes()
    assert digest(data) == expected, path
    return data


def main() -> None:
    manifest = read_json(PACKET / "SOURCE_MANIFEST.json")
    root_manifest = read_json("updates/FM/SOURCE_MANIFEST.json")
    assert root_manifest["source_commit"] == ULTRA_COMMIT
    assert root_manifest["selection_manifest"]["sha256"] == digest(
        (ROOT / PACKET / "SOURCE_MANIFEST.json").read_bytes())
    comparison = root_manifest["selected_commit_comparison"]
    comparison_receipt = read_json(comparison["path"])
    assert digest((ROOT / comparison["path"]).read_bytes()) == comparison["sha256"]
    assert comparison_receipt["result"] == comparison["status"] == "PASS_EXACT_SELECTED_BYTES"
    assert comparison_receipt["compared_count"] == comparison["compared_files"] == 21
    assert comparison_receipt["copied_readable_count"] == 14
    assert manifest["source_commit"] == ULTRA_COMMIT
    assert manifest["source_packet_path"] == "research/2026-10-14-capability-v1"
    archive = manifest["selective_archive"]
    archive_data = assert_recorded(archive["path"], archive["sha256"])
    assert len(archive_data) == archive["bytes"]

    originals = set()
    with zipfile.ZipFile(ROOT / archive["path"]) as zf:
        names = set(zf.namelist())
        assert len(names) == archive["members"]
        for record in manifest["files"]:
            rel = record["archive_member"]
            assert rel not in originals and rel in names
            assert not Path(rel).is_absolute() and ".." not in Path(rel).parts
            originals.add(rel)
            member_data = zf.read(rel)
            assert digest(member_data) == record["sha256"], rel
            assert len(member_data) == record["bytes"], rel
            if record["capital_path"] is not None:
                assert assert_recorded(record["capital_path"], record["sha256"]) == member_data
        assert names == originals

    full_manifest = next(
        row for row in manifest["files"] if row["archive_member"] == "MANIFEST.json"
    )
    assert full_manifest["sha256"] == manifest["full_source_manifest_sha256"]
    assert {row["path"] for row in root_manifest["selected_copied_files"]} == {
        row["capital_path"] for row in manifest["files"] if row["capital_path"]}
    for row in root_manifest["selected_copied_files"]:
        assert_recorded(row["path"], row["sha256"])
    for row in read_json("updates/FM/DERIVED_MANIFEST.json")["records"]:
        assert len(assert_recorded(row["path"], row["sha256"])) == row["bytes"]
    card_path = f"cards/{CARD_ID}.txt"
    card_hash = digest((ROOT / card_path).read_bytes())
    status = read_json(f"frontier/cards/{CARD_ID}.json")
    assert status["card_sha256"] == card_hash
    assert status["claim_status"] == "source_derived_unreviewed"
    assert "No civilization-enabling capability is established" in (ROOT / card_path).read_text()
    wrapped = (ROOT / f"frontier/review_cards/{CARD_ID}.txt").read_bytes()
    assert wrapped.endswith((ROOT / card_path).read_bytes())

    claims = [json.loads(line) for line in (ROOT / "indexes/claims.jsonl").read_text().splitlines()]
    statuses = [json.loads(line) for line in (ROOT / "frontier/CURRENT_CLAIM_STATUS.jsonl").read_text().splitlines()]
    assert len([item for item in claims if item["id"] == CARD_ID]) == 1
    assert len([item for item in statuses if item["card_id"] == CARD_ID]) == 1
    assert next(item for item in statuses if item["card_id"] == CARD_ID) == status
    claim = next(item for item in claims if item["id"] == CARD_ID)
    assert claim["status"] == status["claim_status"]
    catalog = read_json("indexes/agent_catalog.json")
    assert next(item for item in catalog["claims"] if item["id"] == CARD_ID)["card_sha256"] == card_hash
    gates = [json.loads(line) for line in (ROOT / "frontier/OPEN_PROOF_GATES.jsonl").read_text().splitlines()]
    own_gates = [item for item in gates if CARD_ID in item["card_ids"] and item["gate_id"].startswith("G-FM-")]
    assert len(own_gates) == 2 and all(item["status"] == "open" and not item["completion_evidence"] for item in own_gates)

    web_claims = read_json("web/catalog.json")
    web_claim = next(item for item in web_claims if item["id"] == CARD_ID)
    assert web_claim["text"] == (ROOT / card_path).read_text()
    assert web_claim["source_ids"] == claim["source_ids"]
    assert web_claim["source_paths"] == claim["source_paths"]
    assert (ROOT / "web" / web_claim["url"]).is_file()

    route = f"{CARD_ID}\t"
    assert sum(line.startswith(route) for line in (ROOT / "agent/routes.tsv").read_text().splitlines()) == 1
    topic_index = (ROOT / "agent/topics.txt").read_text()
    for topic in status["topics"]:
        path = f"agent/topics/{topic}.tsv"
        lines = (ROOT / path).read_text().splitlines()
        assert sum(line.startswith(route) for line in lines) == 1, path
        assert f"{topic}: {path} ({len(lines)-1} cards)" in topic_index

    refs = {ref["source_id"]: ref for ref in
            status["proof_availability"]["located_proof_sources"] +
            status["proof_availability"]["available_evidence_sources"]}
    assert set(refs) == set(claim["source_ids"])
    sources = {item["source_id"]: item for item in
               (json.loads(line) for line in (ROOT / "indexes/source_metadata.jsonl").read_text().splitlines())
               if item.get("source_id") in refs}
    docs = {item["id"]: item for item in
            (json.loads(line) for line in (ROOT / "web/documents.jsonl").read_text().splitlines())
            if item.get("id") in refs}
    assert set(sources) == set(docs) == set(refs)
    for source_id, ref in refs.items():
        source = sources[source_id]
        doc = docs[source_id]
        assert source["path"] == doc["path"] == ref["path"]
        assert source["sha256"] == ref["sha256"]
        page = (ROOT / "web" / doc["url"]).read_text()
        assert html.escape((ROOT / ref["path"]).read_text()) in page

    claim_map = read_json("updates/FM/CLAIMS.json")
    assert claim_map["claims"][0]["id"] == CARD_ID
    checkpoint_path = claim_map["claims"][0]["checkpoint"]
    checkpoint = read_json(checkpoint_path)
    validate_record(checkpoint, ROOT)
    assert checkpoint["base_revision"] == claim_map["base_revision"]
    assert checkpoint["parent_checkpoint_ids"] == []
    branch = checkpoint["branch_id"]
    projected = views(ROOT, {branch: {checkpoint["checkpoint_id"]: checkpoint}})
    branch_path = f"state/branches/{branch}.txt"
    assert (ROOT / branch_path).read_text() == projected[branch_path]
    row = next(line for line in projected["state/branches.tsv"].splitlines()
               if line.startswith(branch + "\t"))
    assert (ROOT / "state/branches.tsv").read_text().splitlines().count(row) == 1

    base = claim_map["base_revision"]
    for path in ("indexes/claims.jsonl", "indexes/source_metadata.jsonl",
                 "frontier/CURRENT_CLAIM_STATUS.jsonl", "frontier/OPEN_PROOF_GATES.jsonl",
                 "agent/routes.tsv", "state/branches.tsv", "web/documents.jsonl"):
        old = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{base}:{path}"])
        assert (ROOT / path).read_bytes().startswith(old), path

    print(json.dumps({
        "status": "PASS",
        "scope": "selected committed source bytes, archive, N815 public wiring and new-only checkpoint; no scientific replay",
        "source_commit": ULTRA_COMMIT,
        "copied_files": sum(row["capital_path"] is not None for row in manifest["files"]),
        "archive_members": len(originals),
        "card": CARD_ID,
        "new_open_gates": len(own_gates),
        "scientific_correctness": "NOT_EVALUATED",
        "novelty": "NOT_ESTABLISHED",
        "physical_capability": "NOT_ESTABLISHED",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
