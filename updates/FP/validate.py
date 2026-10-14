#!/usr/bin/env python3
"""Check FP byte preservation, append-only authority and route coverage; no science certification."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASE = "1c45f77e32d6fbd72483aed5014061c7bda4f372"
N769 = "N769-rate-free-chemical-relocation-and-physical-adjoint-defect"
N771 = "N771-objective-specific-chemical-adjoints-and-capped-relative-flux-relocation"
IDS = ("N817-cyclewise-rate-free-flux-relocation-and-hidden-exchange",
       "N818-acquisition-boundaries-for-rare-rates-remote-response-and-routing-repair")


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(path):
    return json.loads((ROOT / path).read_text())


def rows(path):
    return [json.loads(line) for line in (ROOT / path).read_text().splitlines() if line]


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def refs(value):
    if isinstance(value, dict):
        if {"path", "sha256"} <= value.keys():
            yield value
        for child in value.values():
            yield from refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from refs(child)


def check_ref(ref):
    path = ref["path"]
    target = (ROOT / path).resolve()
    need(not Path(path).is_absolute() and target.is_relative_to(ROOT), "unsafe path: " + path)
    need(target.is_file() and sha(path) == ref["sha256"], "source hash drift: " + path)
    if "bytes" in ref:
        need(target.stat().st_size == ref["bytes"], "source size drift: " + path)
    if "lines" in ref:
        a, b = ref["lines"]
        need(1 <= a <= b <= len(target.read_text().splitlines()), "source range drift: " + path)


def main():
    manifest = load("updates/FP/INTAKE_MANIFEST.json")
    files = manifest["files"]
    need(manifest["intake"] == "FP" and len(files) == 26, "selected and frozen snapshot inventory")
    need(manifest["campaign_source_commit"] == "c25951907eef5d632b0061f5fed4764205e86d60",
         "frozen campaign source revision")
    need(len({f["copy"] for f in files}) == len(files), "duplicate source path")
    for row in files:
        check_ref({"path": row["copy"], "sha256": row["sha256"], "bytes": row["bytes"]})
        if "line_count" in row:
            need(row["line_count"] == len((ROOT / row["copy"]).read_text().splitlines()), "source line count")
        need(Path(row["original_absolute_path"]).is_absolute(), "missing original provenance")
    for path in ("indexes/claims.jsonl", "indexes/source_metadata.jsonl",
                 "frontier/CURRENT_CLAIM_STATUS.jsonl", "frontier/OPEN_PROOF_GATES.jsonl",
                 "web/documents.jsonl", "agent/SEMANTIC_NOTICES.jsonl", "state/branches.tsv"):
        need((ROOT / path).read_bytes().startswith(git("show", BASE + ":" + path)),
             "historical ledger changed: " + path)
    for path, key in (("indexes/agent_catalog.json", "claims"),
                      ("indexes/agent_graph.json", "nodes"),
                      ("indexes/agent_graph.json", "edges"),
                      ("mechanisms/bridge_candidates.json", "bridges"),
                      ("mechanisms/bridge_candidates.json", "rejected_transfers"),
                      ("web/catalog.json", None)):
        old = json.loads(git("show", BASE + ":" + path))
        new = load(path)
        if key is not None:
            old, new = old[key], new[key]
        need(new[:len(old)] == old, "historical sequence changed: " + path)
    old_alias = json.loads(git("show", BASE + ":indexes/query_aliases.json"))
    alias = load("indexes/query_aliases.json")
    need(all(alias.get(k) == v for k, v in old_alias.items()), "historical alias changed")
    for cid in (N769, N771):
        path = "frontier/cards/" + cid + ".json"
        need((ROOT / path).read_bytes() == git("show", BASE + ":" + path), "parent status changed")
    mapping = load("updates/FP/CLAIMS.json")
    need(mapping["base_revision"] == BASE and {c["id"] for c in mapping["claims"]} == set(IDS), "claim map")
    packet = mapping["campaign_publication"]
    need(packet["mission_status"] == "NOT_ACHIEVED" and packet["authored_archive"]["manifest_entries"] == 161
         and len(packet["public_packet_files"]) == 7, "frozen packet scope")
    need(packet["source_commit"] == manifest["campaign_source_commit"], "frozen packet source revision")
    for row in packet["public_packet_files"]:
        check_ref(row)
    spec = importlib.util.spec_from_file_location("packet_verifier", ROOT / "updates/FP/verify_campaign_packet.py")
    packet_verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(packet_verifier)
    packet_verifier.main()
    claim_rows = {x["id"]: x for x in rows("indexes/claims.jsonl")}
    status_rows = {x["card_id"]: x for x in rows("frontier/CURRENT_CLAIM_STATUS.jsonl")}
    catalog = {x["id"]: x for x in load("indexes/agent_catalog.json")["claims"]}
    web = {x["id"]: x for x in load("web/catalog.json")}
    source_ids = {"src-FP-" + f["sha256"][:16] for f in files}
    metadata = [x for x in rows("indexes/source_metadata.jsonl") if x.get("source_id", "").startswith("src-FP-")]
    docs = [x for x in rows("web/documents.jsonl") if x.get("id", "").startswith("src-FP-")]
    need(len(metadata) == len(docs) == len(files) and
         {x["source_id"] for x in metadata} == {x["id"] for x in docs} == source_ids,
         "source index coverage")
    for row in metadata:
        check_ref(row)
        if row["extraction"] != "original_bytes_not_rendered":
            need((ROOT / "web/pages" / (row["source_id"] + ".html")).is_file(), "source page absent")
    gates = [x for x in rows("frontier/OPEN_PROOF_GATES.jsonl") if x["gate_id"].startswith("G-FP-")]
    need(len(gates) == 7 and all(x["status"] == "open" and not x["completion_evidence"] for x in gates),
         "gate status")
    graph = load("indexes/agent_graph.json")
    nodes = {x["id"] for x in graph["nodes"]}
    need(set(IDS) | source_ids <= nodes, "graph coverage")
    for cid in IDS:
        c, s = claim_rows[cid], status_rows[cid]
        need(c == web[cid] and c["status"] == s["claim_status"] == catalog[cid]["status"] ==
             "source_derived_unreviewed", "claim/status/catalog mismatch")
        need(s == load("frontier/cards/" + cid + ".json"), "status sidecar mismatch")
        need(sha(c["path"]) == s["card_sha256"] == catalog[cid]["card_sha256"], "card hash mismatch")
        need((ROOT / "frontier/review_cards" / (cid + ".txt")).read_bytes().endswith((ROOT / c["path"]).read_bytes()),
             "review wrapper changed card")
        need((ROOT / "frontier/dossiers" / (cid.split("-")[0] + ".txt")).is_file(), "dossier missing")
        need((ROOT / "web/pages" / (cid + ".html")).is_file(), "card page missing")
        need(set(c["source_ids"]) <= source_ids and len(c["source_ids"]) == len(c["source_paths"]),
             "claim source inventory")
        for ref in refs(s):
            check_ref(ref)
    need(not any("N816" in str(x) for x in (claim_rows[IDS[1]]["depends_on"], status_rows[IDS[1]]["depends_on"])),
         "unmerged N816 became a dependency")
    notices = [x for x in rows("agent/SEMANTIC_NOTICES.jsonl") if x["notice_id"].startswith("SN-FP-")]
    need(len(notices) == 1 and set(notices[0]["card_ids"]) == {N769, N771, IDS[0]}, "reciprocal scope")
    for ref in refs(notices + gates):
        check_ref(ref)
    bridges = load("updates/FP/BRIDGES.json")["bridges"]
    need(len(bridges) == 2 and {x["state"] for x in bridges} ==
         {"PROVEN LOGICAL DEPENDENCY", "REFUTED TRANSFER"}, "bridge scopes")
    for b in bridges:
        need(load("mechanisms/bridges/" + b["id"] + ".json") == b, "bridge sidecar")
        for side in ("source_interface", "destination_interface"):
            need(all(b[side].get(k) for k in ("objects", "regime_and_quantifiers", "supplied_information",
                                              "acquired_information", "legal_access", "guarantee",
                                              "units_norm_and_precision", "costs")), "incomplete contract")
        for ref in refs(b):
            check_ref(ref)
    checkpoints = {p for c in mapping["claims"] for p in (c.get("initial_checkpoint"), c.get("checkpoint")) if p}
    if checkpoints:
        spec = importlib.util.spec_from_file_location("publisher", ROOT / "state/publish_checkpoint.py")
        publisher = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(publisher)
        for checkpoint in checkpoints:
            publisher.validate_record(load(checkpoint), ROOT)
        first = "state/checkpoints/worker-fp-frontier-capability-intake/2026-10-15-fp-selected-capability-intake.json"
        final = "state/checkpoints/worker-fp-frontier-capability-intake/2026-10-15-fp-frozen-authored-campaign.json"
        need(checkpoints == {first, final} and load(final)["parent_checkpoint_ids"] ==
             [load(first)["checkpoint_id"]], "FP checkpoint lineage")
        publication = load("updates/FP/PUBLICATION_STATUS.json")
        need(set(publication["individually_validated_new_checkpoints"]) == checkpoints and
             publication["standard_publisher_attempt"]["exit_code"] == 1 and
             publication["standard_second_publisher_attempt"]["exit_code"] == 1,
             "publication boundary")
        for path, digest in publication["new_record_sha256"].items():
            need(path in checkpoints and sha(path) == digest, "checkpoint hash drift")
    print(json.dumps({"status": "PASS_SCOPED_INTEGRITY", "base_revision": BASE,
                      "new_cards": len(IDS), "preserved_files": len(files),
                      "open_gates": len(gates), "paired_bridges": len(bridges),
                      "checkpoints": sorted(checkpoints), "scientific_truth_checked": False}, sort_keys=True))


if __name__ == "__main__":
    main()
