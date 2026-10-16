#!/usr/bin/env python3
"""Build a read-only, out-of-repository overlay from root-authored GC records.

The program has no apply mode. It reads the checked-out Astra repository and
root-supplied source files, then stages new files and registry additions under
an output directory outside that repository for review.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

INTAKE = "GC-peak-stability-genesis-20261016"
PREFIX = f"updates/{INTAKE}/"
ROUTES = {"N894", "N895", "N896", "N897"}
STATUS = "source_derived_unreviewed"
UNKNOWN_FIELDS = (
    "external_correctness", "historical_priority", "physical_capability",
    "formal_verification", "empirical_confirmation",
)
BRIDGE_STATES = {
    "PROVEN LOGICAL DEPENDENCY", "ESTABLISHED COMPATIBLE INTERFACE",
    "CANDIDATE CONNECTION", "INCOMPATIBLE ASSUMPTIONS", "REFUTED TRANSFER",
}
PROVENANCE_ROLES = {
    "supplied_original_file", "root_synthesis", "worker_derivation",
    "same_team_review", "same_team_research_or_review",
    "root_or_worker_executable_check", "acquired_primary_literature_receipt",
    "capital_comparison",
}


def fail(message: str) -> None:
    raise ValueError(message)


def need(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object, *, sort: bool = False) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=sort) + "\n").encode("utf-8")


def compact_jsonl(rows: list[dict]) -> bytes:
    return b"".join((json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8") for row in rows)


def safe_repo_path(value: str) -> str:
    need(isinstance(value, str) and value and not Path(value).is_absolute(), "Repository path must be relative")
    path = Path(value)
    need(".." not in path.parts and "\\" not in value, f"Unsafe repository path: {value}")
    need(value.startswith(PREFIX), f"GC-owned source path must be under {PREFIX}: {value}")
    return value


def run_git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.PIPE).strip()


def check_pins(repo: Path, config: dict) -> dict:
    pins = config.get("pins")
    need(isinstance(pins, dict), "Config needs pins: base_revision, expected_branch_head, expected_remote_main")
    base = pins.get("base_revision")
    head = pins.get("expected_branch_head")
    remote_expected = pins.get("expected_remote_main")
    for name, value in (("base_revision", base), ("expected_branch_head", head), ("expected_remote_main", remote_expected)):
        need(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value), f"{name} must be a full Git SHA")
    actual = run_git(repo, "rev-parse", "HEAD")
    need(actual == head, f"HEAD changed: expected {head}, observed {actual}")
    # Reuse the repository's scoped append-only baseline guard. It checks that
    # historical cards/updates/checkpoints remain byte-stable and registry
    # values retain their original prefixes, while making no Git changes.
    fz_tools = repo / "updates/FZ-positive-memory-genesis-20261016"
    need((fz_tools / "protected_baseline.py").is_file(), "Pinned FZ baseline checker is unavailable")
    sys.path.insert(0, str(fz_tools))
    try:
        from protected_baseline import check_baseline  # type: ignore
        baseline = check_baseline(repo, immutable_base=base, expected_head=head,
                                  expected_remote_main=remote_expected, phase="integrated", check_remote=True)
    finally:
        try:
            sys.path.remove(str(fz_tools))
        except ValueError:
            pass
    dirty = run_git(repo, "status", "--porcelain")
    need(not dirty, "Repository working tree is not clean; refresh pins and review inputs before staging")
    return {"base_revision": base, "expected_branch_head": head,
            "actual_branch_head": actual, "expected_remote_main": remote_expected,
            "observed_remote_main": baseline["observed_remote_main"],
            "append_only_baseline": baseline, "working_tree": "clean"}


def read_source(repo: Path, config_path: Path, item: dict) -> tuple[dict, bytes]:
    record = item.get("record")
    need(isinstance(record, dict), "Each source needs its canonical source_metadata record in `record`")
    for key in ("source_id", "path", "title", "sha256", "bytes", "date_version", "read_depth",
                "reported_verification", "extraction", "provenance_role", "source_handling"):
        need(key in record, f"Source metadata is missing {key}")
    path = safe_repo_path(record["path"])
    need(re.fullmatch(r"src-GC-[A-Za-z0-9_-]+", record["source_id"]), "New source IDs must use src-GC- namespace")
    need(record["provenance_role"] in PROVENANCE_ROLES, "Unknown provenance_role: " + str(record["provenance_role"]))
    source_name = item.get("source_file")
    if source_name is not None:
        source_path = Path(source_name)
        if not source_path.is_absolute():
            source_path = (config_path.parent / source_path).resolve()
        need(source_path.is_file(), "Root-supplied source file is missing: " + str(source_path))
        raw = source_path.read_bytes()
    else:
        source_path = (repo / path).resolve()
        need(source_path.is_relative_to(repo.resolve()) and source_path.is_file(), "Source file missing from repository: " + path)
        raw = source_path.read_bytes()
    need(sha(raw) == record["sha256"], "Source SHA-256 mismatch: " + path)
    need(len(raw) == record["bytes"], "Source byte count mismatch: " + path)
    try:
        raw.decode("utf-8")
        extraction = "original_utf8_bytes"
    except UnicodeDecodeError:
        extraction = "original_binary_bytes"
    need(record["extraction"] == extraction, "Source extraction label disagrees with exact bytes: " + path)
    return record, raw


def walk_refs(value):
    if isinstance(value, dict):
        if {"path", "sha256", "lines"} <= value.keys():
            yield value
        for child in value.values():
            yield from walk_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_refs(child)


def recover_text(repo: Path, ref: dict, source_bytes: dict[str, bytes]) -> tuple[bytes, str]:
    for name in dict.fromkeys([ref["path"], ref.get("read_path", "")]):
        if not name:
            continue
        raw = source_bytes.get(name)
        if raw is None:
            p = (repo / name).resolve()
            need(p.is_relative_to(repo.resolve()), "Evidence path escapes repository: " + name)
            if p.is_file():
                raw = p.read_bytes()
        if raw is None:
            continue
        if sha(raw) == ref["sha256"]:
            return raw, name
        if name.endswith(".html"):
            try:
                for block in re.findall(rb"<pre(?:\s[^>]*)?>(.*?)</pre>", raw, re.S):
                    decoded = html.unescape(block.decode("utf-8"))
                    if sha(decoded.encode("utf-8")) == ref["sha256"]:
                        return decoded.encode("utf-8"), name
            except UnicodeDecodeError:
                pass
    fail("Evidence bytes/hash are not recoverable: " + str(ref.get("path")))


def verify_refs(repo: Path, refs, source_bytes: dict[str, bytes], metadata_rows: list[dict]) -> dict[str, dict]:
    checked = {}
    for ref in refs:
        path, digest = ref["path"], ref["sha256"]
        need(isinstance(path, str) and re.fullmatch(r"[0-9a-f]{64}", str(digest)), "Invalid evidence path or SHA-256")
        lines = ref["lines"]
        need(isinstance(lines, list) and len(lines) == 2 and all(type(x) is int for x in lines),
             "Evidence line range must be inclusive [first,last]: " + path)
        raw, recovered_by = recover_text(repo, ref, source_bytes)
        try:
            line_count = len(raw.decode("utf-8").splitlines())
        except UnicodeDecodeError:
            fail("Evidence line reference points to non-UTF-8 bytes: " + path)
        need(1 <= lines[0] <= lines[1] <= line_count, "Evidence line range is outside exact source bytes: " + path)
        candidates = {row.get("source_id", row.get("id")) for row in metadata_rows
                      if row.get("path") == path and row.get("sha256") == digest
                      and row.get("source_id", row.get("id"))}
        if ref.get("source_id") is not None:
            need(ref["source_id"] in candidates,
                 "Evidence/source catalog ID or path/hash disagreement: " + path)
        elif len(candidates) == 1:
            ref["source_id"] = next(iter(candidates))
        elif candidates:
            fail("Ambiguous evidence source_id; supply it explicitly: " + path)
        if ref.get("source_revision") is not None:
            revision = ref["source_revision"]
            need(re.fullmatch(r"[0-9a-f]{40}", revision), "source_revision must be a full SHA or null")
            pinned = subprocess.check_output(["git", "-C", str(repo), "show", revision + ":" + path])
            need(sha(pinned) == digest, "Pinned source revision/hash mismatch: " + path)
        checked[ref.get("id", path + ":" + str(lines[0]))] = {
            "path": path, "sha256": digest, "lines": lines, "recovered_by": recovered_by,
        }
    return checked


def load_jsonl(path: Path) -> tuple[list[dict], bytes]:
    raw = path.read_bytes()
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    return rows, raw


def require_unique(rows: list[dict], key: str, label: str) -> set:
    values = [row.get(key) for row in rows]
    need(None not in values and len(values) == len(set(values)), f"Duplicate/missing {key} in {label}")
    return set(values)


def page_html(title: str, target: str, text: str) -> bytes:
    return ("<!doctype html>\n<html lang=\"en\"><meta charset=\"utf-8\"><title>" + html.escape(title) +
            "</title><body><p>Scoped source-derived record; external status remains unknown. <a href=\"../../" +
            html.escape(target, quote=True) + "\">Exact bytes</a></p><pre>" + html.escape(text) +
            "</pre></body></html>\n").encode("utf-8")


def add_output(out: Path, stage: dict[str, bytes], relative: str, data: bytes) -> None:
    need(relative not in stage, "Duplicate staged output path: " + relative)
    stage[relative] = data


def build(repo: Path, config_path: Path, out: Path) -> dict:
    repo = repo.resolve()
    config_path = config_path.resolve()
    out = out.resolve()
    need(config_path.is_file(), "Missing root-supplied claim_config.json: " + str(config_path))
    need(not config_path.is_relative_to(repo), "claim_config.json must remain outside the repository")
    need(not out.is_relative_to(repo), "Output directory must remain outside the repository")
    need(not out.exists(), "Refusing to overwrite existing staging directory: " + str(out))
    config_raw = config_path.read_bytes()
    config = json.loads(config_raw)
    need(config.get("schema") == "astra.gc-claim-config.v1", "Unsupported config schema")
    need(config.get("intake_id") == INTAKE, "Unexpected GC intake_id")
    pins = check_pins(repo, config)

    # Route availability is checked again against the exact generation baseline.
    claim_rows, claim_raw = load_jsonl(repo / "indexes/claims.jsonl")
    known_ids = require_unique(claim_rows, "id", "indexes/claims.jsonl")
    occupied_routes = {x.split("-", 1)[0] for x in known_ids}
    need(not (ROUTES & occupied_routes), "A reserved card route is now occupied; recheck N894-N897")
    cards = config.get("cards")
    need(isinstance(cards, list) and 1 <= len(cards) <= len(ROUTES)
         and all(isinstance(c, dict) for c in cards),
         "Config must supply a nonempty variable-length list of root-authored cards (maximum four reserved routes)")
    ids = [c.get("id") for c in cards]
    route_ids = {x.split("-", 1)[0] for x in ids if isinstance(x, str)}
    need(len(set(ids)) == len(ids) and len(route_ids) == len(ids) and route_ids <= ROUTES,
         "Card IDs must use distinct, currently reserved N894-N897 numeric routes")
    for card_id in ids:
        need(re.fullmatch(r"N(?:894|895|896|897)-[a-z0-9]+(?:-[a-z0-9]+)*", card_id), "Unsafe numeric card ID: " + str(card_id))

    source_records, source_bytes = [], {}
    for item in config.get("sources", []):
        record, raw = read_source(repo, config_path, item)
        need(record["path"] not in source_bytes, "Duplicate source path: " + record["path"])
        source_records.append(record)
        source_bytes[record["path"]] = raw
    source_ids = require_unique(source_records, "source_id", "new source catalog records")
    metadata_by_path = {x["path"]: x for x in source_records}
    old_metadata, _ = load_jsonl(repo / "indexes/source_metadata.jsonl")
    # The inherited public catalog includes bibliography-only rows without IDs.
    # Preserve them exactly; uniqueness/collision checks apply to identified rows.
    identified_old_metadata = [row for row in old_metadata if row.get("source_id") is not None]
    old_source_ids = require_unique(identified_old_metadata, "source_id", "identified indexes/source_metadata.jsonl rows")
    need(not (source_ids & old_source_ids), "New GC source ID already exists")
    known_source_ids = old_source_ids | source_ids
    old_source_paths = {x.get("path") for x in old_metadata}
    need(not ({x["path"] for x in source_records} & old_source_paths),
         "New source path is already indexed; reuse its existing source_id instead")
    all_metadata = old_metadata + source_records

    statuses, catalog, new_claims = [], [], []
    stage: dict[str, bytes] = {}
    source_topics: dict[str, set[str]] = {x: set() for x in source_ids}
    aliases = {}
    for card in cards:
        cid = card["id"]
        title = card.get("title")
        topics = card.get("topics")
        body = card.get("card_text")
        status = card.get("status_record")
        need(isinstance(title, str) and title.strip() and isinstance(topics, list) and topics,
             f"{cid} needs title and topics")
        need(all(isinstance(t, str) and t.strip() for t in topics), f"{cid} has invalid topics")
        need(isinstance(body, str) and body.strip(), f"{cid} needs root-authored exact card_text")
        card_path = f"cards/{cid}.txt"
        raw = body.encode("utf-8")
        digest = sha(raw)
        need(body.splitlines()[0].startswith(cid + " | " + title), f"{cid} first line must match `ID | title`")
        need(isinstance(status, dict), f"{cid} needs its canonical status_record")
        need(status.get("card_id") == cid and status.get("card_path") == card_path and status.get("card_sha256") == digest,
             f"{cid} status/card identity or hash mismatch")
        need(status.get("title") == title and status.get("topics") == topics and status.get("claim_status") == STATUS,
             f"{cid} status metadata mismatch or attempted status promotion")
        validation = status.get("validation")
        need(isinstance(validation, dict), f"{cid} needs a structured validation boundary")
        need(all(validation.get(k) == "UNKNOWN" for k in UNKNOWN_FIELDS),
             f"{cid} validation boundary must keep external/capability fields UNKNOWN")
        external = status.get("requires_external_validation")
        need(isinstance(external, list) and external and all(isinstance(x, dict) for x in external),
             f"{cid} needs explicit open external-validation obligations")
        proof_availability = status.get("proof_availability")
        need(isinstance(proof_availability, dict), f"{cid} needs structured proof_availability")
        located = proof_availability.get("located_proof_sources", [])
        need(isinstance(located, list) and located, f"{cid} needs located proof-source metadata")
        for ref in located:
            need(isinstance(ref, dict), f"{cid} has a malformed located proof source")
            candidates = {row.get("source_id", row.get("id")) for row in all_metadata
                          if row.get("path") == ref.get("path") and row.get("sha256") == ref.get("sha256")
                          and row.get("source_id", row.get("id"))}
            need(ref.get("source_id") in candidates,
                 f"{cid} proof source must match indexed metadata by path, hash, and source_id")
        dependencies = status.get("depends_on", [])
        need(isinstance(dependencies, list) and all(isinstance(x, dict) and isinstance(x.get("target"), str)
                                                    for x in dependencies),
             f"{cid} has malformed scoped dependencies")
        need(all(x["target"] in known_ids | set(ids) for x in dependencies),
             f"{cid} dependency target is not an indexed claim")
        claim = {
            "id": cid, "title": title, "path": card_path, "topics": topics, "status": STATUS,
            "source_ids": list(dict.fromkeys(x.get("source_id") for x in located)),
            "source_paths": list(dict.fromkeys(x.get("path") for x in located)),
            "depends_on": [x["target"] for x in dependencies],
            "scoped_dependencies": dependencies, "tokens": None,
            "token_count_status": "not_measured", "record_type": "source_and_integration_derived_scoped_result",
        }
        need(claim["source_ids"] and all(isinstance(x, str) and x in known_source_ids for x in claim["source_ids"]),
             f"{cid} proof sources lack indexed source metadata")
        for sid in claim["source_ids"]:
            source_topics.setdefault(sid, set()).update(topics)
        catalog_row = {
            "id": cid, "title": title, "topics": topics, "status": STATUS, "card_sha256": digest,
            "dependencies": {"depends_on": claim["depends_on"], "scoped_dependencies": claim["scoped_dependencies"]},
            "pointers": {
                "card_local": card_path, "card_web": f"frontier/dossiers/{cid.split('-', 1)[0]}.txt",
                "current_status": f"frontier/cards/{cid}.json", "reviewed_card": f"frontier/review_cards/{cid}.txt",
                "read_local": f"python3 frontier/retrieve.py dossier {cid.split('-', 1)[0]}",
                "read_web": [f"frontier/dossiers/{cid.split('-', 1)[0]}.txt", claim["source_paths"][0],
                             f"frontier/connections/{cid.split('-', 1)[0]}.json"],
            },
            "quoted_fields": {
                "status": ["status=source_derived_unreviewed; supplied claims and internal work remain externally unreviewed."],
                "interface": [status.get("scientific_scope_status", "")],
                "limits": [external[0].get("scope", "")],
            },
        }
        need(all(isinstance(x, str) and x for x in catalog_row["quoted_fields"]["interface"] + catalog_row["quoted_fields"]["limits"]),
             f"{cid} needs scope and next-obligation text in its status record")
        status_bytes = json_bytes(status, sort=True)
        add_output(out, stage, "overlay/" + card_path, raw)
        add_output(out, stage, f"overlay/frontier/review_cards/{cid}.txt", raw)
        add_output(out, stage, f"overlay/frontier/cards/{cid}.json", status_bytes)
        add_output(out, stage, f"overlay/web/pages/{cid}.html", page_html(title, card_path, body))
        statuses.append(status)
        catalog.append(catalog_row)
        new_claims.append(claim)
        aliases[cid] = " ".join([title, *topics])

    # New source bytes and exact source records are staged without touching the checkout.
    for record in source_records:
        target = record["path"]
        repo_path = (repo / target).resolve()
        need(repo_path.is_relative_to(repo), "Source target escapes repository: " + target)
        if repo_path.exists():
            need(repo_path.is_file() and sha(repo_path.read_bytes()) == record["sha256"],
                 "Existing source target differs; refuse overwrite: " + target)
        else:
            add_output(out, stage, "overlay/" + target, source_bytes[target])

    gates = config.get("gates", [])
    notices = config.get("notices", [])
    bridges = config.get("bridges", [])
    need(isinstance(gates, list) and all(isinstance(x, dict) for x in gates)
         and isinstance(notices, list) and all(isinstance(x, dict) for x in notices)
         and isinstance(bridges, list) and all(isinstance(x, dict) for x in bridges),
         "gates, notices, and bridges must be arrays")
    known_all_cards = known_ids | set(ids)
    for gate in gates:
        gid = gate.get("gate_id", "")
        need(re.fullmatch(r"G-GC-[A-Za-z0-9_-]+", gid) is not None
             and gate.get("status") == "open" and gate.get("completion_evidence") == [],
             "New gates must be GC-scoped and remain open with no completion evidence")
        need(set(gate.get("card_ids", [])) <= set(ids), "New gate references a card outside the configured N894-N897 routes")
        add_output(out, stage, f"overlay/frontier/gates/{gid}.json", json_bytes(gate, sort=True))
    for notice in notices:
        nid = notice.get("notice_id", "")
        need(re.fullmatch(r"SN-GC-[A-Za-z0-9_-]+", nid) is not None
             and notice.get("status") == "unreviewed_scoped_update"
             and notice.get("whole_claim_invalidated") is False, "Notice must remain scoped and unreviewed")
        need(set(notice.get("card_ids", [])) <= known_all_cards, "Notice references an unknown card")
    for bridge in bridges:
        bid = bridge.get("id", "")
        state = bridge.get("state")
        need(re.fullmatch(r"GC_[A-Za-z0-9_-]+", bid) is not None
             and state in BRIDGE_STATES and bridge.get("status", state) == state,
             "Bridge must use GC namespace and a recognized scoped state")
        need(set(bridge.get("cards", [])) <= known_all_cards, "Bridge references an unknown card")
        if state in {"PROVEN LOGICAL DEPENDENCY", "ESTABLISHED COMPATIBLE INTERFACE"}:
            need(bool(bridge.get("transfer_proof_refs")), "Positive transfer state needs exact transfer proof refs")
        if state == "REFUTED TRANSFER":
            need(bool(bridge.get("counterexample_refs")), "Refuted transfer needs exact counterexample refs")
        add_output(out, stage, f"overlay/mechanisms/bridges/{bid}.json", json_bytes(bridge, sort=True))

    # Verify every referenced source against either exact root-supplied bytes or the checkout.
    all_records = [source_records, statuses, gates, notices, bridges]
    refs = [ref for item in all_records for ref in walk_refs(item)]
    verified_refs = verify_refs(repo, refs, source_bytes, all_metadata)
    # Detect identifier/path collisions before producing any review output.
    existing_status, _ = load_jsonl(repo / "frontier/CURRENT_CLAIM_STATUS.jsonl")
    existing_gates, _ = load_jsonl(repo / "frontier/OPEN_PROOF_GATES.jsonl")
    existing_notices, _ = load_jsonl(repo / "agent/SEMANTIC_NOTICES.jsonl")
    old_catalog = json.loads((repo / "indexes/agent_catalog.json").read_text())
    old_graph = json.loads((repo / "indexes/agent_graph.json").read_text())
    old_candidates = json.loads((repo / "mechanisms/bridge_candidates.json").read_text())
    need(not (set(ids) & require_unique(existing_status, "card_id", "claim status")), "Claim status ID collision")
    need(not (set(ids) & require_unique(old_catalog["claims"], "id", "agent catalog")), "Agent catalog ID collision")
    old_node_ids = require_unique(old_graph["nodes"], "id", "agent graph nodes")
    need(not (set(ids) & old_node_ids), "Agent graph claim node collision")
    need(not ({x["gate_id"] for x in gates} & require_unique(existing_gates, "gate_id", "open gates")), "Gate ID collision")
    need(not ({x["notice_id"] for x in notices} & require_unique(existing_notices, "notice_id", "semantic notices")), "Notice ID collision")
    old_bridge_ids = {x["id"] for x in old_candidates.get("bridges", []) + old_candidates.get("rejected_transfers", [])}
    need(not ({x["id"] for x in bridges} & old_bridge_ids), "Bridge ID collision")
    require_unique(gates, "gate_id", "new GC gates")
    require_unique(notices, "notice_id", "new GC notices")
    require_unique(bridges, "id", "new GC bridges")
    old_doc_ids = {x["id"] for x in load_jsonl(repo / "web/documents.jsonl")[0]}
    need(not (source_ids | set(ids)) & old_doc_ids, "Web document ID collision")
    old_web_catalog = json.loads((repo / "web/catalog.json").read_text())
    need(not (set(ids) & {x.get("id") for x in old_web_catalog}), "Web catalog card ID collision")
    old_aliases = json.loads((repo / "indexes/query_aliases.json").read_text())
    need(not (set(ids) & set(old_aliases)), "Query alias ID collision")
    # Build append-only deltas. Full repository registries stay outside the staging tree.
    claim_map = [{"id": c["id"], "source_path": c["source_paths"][0], "source_id": c["source_ids"][0],
                  "source_sha256": next(x["sha256"] for x in next(card for card in cards if card["id"] == c["id"])
                                         ["status_record"]["proof_availability"]["located_proof_sources"]
                                         if x["path"] == c["source_paths"][0]),
                  "status": STATUS, "missing_artifacts": [], "checkpoint": None,
                  "checkpoint_draft": None, "workflow_trace": None} for c in new_claims]
    source_docs = [{"id": x["source_id"], "path": x["path"], "title": x["title"], "role": "source", "cycle": 0,
                    "topics": sorted(source_topics.get(x["source_id"], set())), "extraction": x["extraction"],
                    "tokens": None, "url": "pages/" + x["source_id"] + ".html"} for x in source_records]
    card_docs = [{"id": c["id"], "path": c["path"], "title": c["title"], "role": "card", "cycle": 0,
                  "topics": c["topics"], "extraction": "original_utf8_bytes", "tokens": None,
                  "url": "pages/" + c["id"] + ".html"} for c in new_claims]
    web_rows = [{**c, "url": "pages/" + c["id"] + ".html", "text": next(x["card_text"] for x in cards if x["id"] == c["id"])} for c in new_claims]
    graph_nodes = [{"id": c["id"], "node_kind": "claim"} for c in new_claims]
    graph_nodes += [{"id": s["source_id"], "node_kind": "source"} for s in source_records if s["source_id"] not in {x["id"] for x in old_graph["nodes"]}]
    graph_edges = [{"from": c["id"], "to": sid, "kind": "provenance", "raw_kind": "source_or_internal_evidence",
                    "source": INTAKE, "composition": "Metadata provenance edge only; no theorem transfer is implied."}
                   for c in new_claims for sid in c["source_ids"]]
    old_graph_nodes = old_node_ids
    need(all(edge["to"] in old_graph_nodes | {x["id"] for x in graph_nodes} for edge in graph_edges), "Graph source endpoint missing")
    rejected = [x for x in bridges if x["state"] in {"INCOMPATIBLE ASSUMPTIONS", "REFUTED TRANSFER"}]
    accepted = [x for x in bridges if x not in rejected]

    jsonl_additions = {
        "indexes/source_metadata.jsonl": source_records,
        "indexes/claims.jsonl": new_claims,
        "frontier/CURRENT_CLAIM_STATUS.jsonl": statuses,
        "frontier/OPEN_PROOF_GATES.jsonl": gates,
        "agent/SEMANTIC_NOTICES.jsonl": notices,
        "web/documents.jsonl": source_docs + card_docs,
    }
    for target, rows in jsonl_additions.items():
        if not rows:
            continue
        if target.startswith("indexes/") or target.startswith("frontier/") or target.startswith("agent/") or target.startswith("web/"):
            # The target is included in the immutable base hash set for reviewer reconciliation.
            add_output(out, stage, "additions/" + target, compact_jsonl(rows))

    array_additions = {
        "indexes/agent_catalog.json": {"claims": catalog},
        "indexes/agent_graph.json": {"nodes": graph_nodes, "edges": graph_edges},
        "web/catalog.json": web_rows,
        "mechanisms/bridge_candidates.json": {"bridges": accepted, "rejected_transfers": rejected},
    }
    for target, delta in array_additions.items():
        if (any(delta.values()) if isinstance(delta, dict) else bool(delta)):
            add_output(out, stage, "additions/" + target, json_bytes(delta, sort=True))
    if aliases:
        add_output(out, stage, "additions/indexes/query_aliases.json", json_bytes(aliases, sort=True))

    for source in source_records:
        if source["path"] in source_bytes:
            try:
                text = source_bytes[source["path"]].decode("utf-8")
            except UnicodeDecodeError:
                text = ""
            page = page_html(source["title"], source["path"], text) if text else (
                "<!doctype html>\n<html lang=\"en\"><meta charset=\"utf-8\"><title>" + html.escape(source["title"]) +
                "</title><body><p>Original binary bytes; no text extraction substituted. <a href=\"../../" +
                html.escape(source["path"], quote=True) + "\">Exact bytes</a></p></body></html>\n").encode("utf-8")
            add_output(out, stage, f"overlay/web/pages/{source['source_id']}.html", page)

    update_base = "overlay/" + PREFIX
    new_artifacts = {
        "INDEXED_SOURCE_MANIFEST.v0001.json": {
            "schema": "astra.gc-source-manifest.v1", "intake_id": INTAKE,
            "initial_main": pins["base_revision"], "files": source_records,
            "preservation_scope": "Exact source bytes and source metadata only; no source content is interpreted by the generator.",
        },
        "CLAIMS.json": {"schema": "astra.intake-claim-map.v1", "intake_id": INTAKE,
                         "base_revision": pins["base_revision"], "claims": claim_map},
        "INDEXED_SOURCES.json": {"schema": "astra.gc-indexed-sources.v1", "base_revision": pins["base_revision"],
                                 "files": source_records},
        "EVIDENCE_REFS.json": {"schema": "astra.gc-evidence-refs.v1", "evidence": verified_refs,
                               "boundary": "Exact source locator/hash/line integrity only; no scientific verification."},
        "SCOPED_NOTICES.json": notices,
        "BRIDGES.json": {"base_revision": pins["base_revision"], "bridges": bridges},
        "CURATION.json": {"schema": "astra.gc-curation.v1", "base_revision": pins["base_revision"],
                          "new_cards": ids, "scientific_status": STATUS,
                          "external_truth_certified": False,
                          "boundary": "Metadata and route generation do not establish correctness, novelty, capability, or transfer."},
    }
    for name, value in new_artifacts.items():
        add_output(out, stage, update_base + name, json_bytes(value, sort=True))

    # Check every create-only overlay target after all overlay artifacts exist.
    # Canonical registry changes are deltas under additions/ and never replace
    # a historical file. Exact source files already in the checkout are omitted.
    existing_paths = set(run_git(repo, "ls-tree", "-r", "--name-only", "HEAD").splitlines())
    source_targets = {x["path"]: x["sha256"] for x in source_records}
    for staged_path, data in list(stage.items()):
        if not staged_path.startswith("overlay/"):
            continue
        target = staged_path[len("overlay/"):]
        repo_target = (repo / target).resolve()
        need(repo_target.is_relative_to(repo), "Overlay target escapes repository: " + target)
        if target in existing_paths or repo_target.exists():
            need(target in source_targets and repo_target.is_file()
                 and sha(repo_target.read_bytes()) == source_targets[target] == sha(data),
                 "Create-only target already exists in the checkout: " + target)
            del stage[staged_path]  # The exact source is already present; do not stage a duplicate.

    before_paths = [
        "indexes/source_metadata.jsonl", "indexes/claims.jsonl", "frontier/CURRENT_CLAIM_STATUS.jsonl",
        "frontier/OPEN_PROOF_GATES.jsonl", "agent/SEMANTIC_NOTICES.jsonl", "indexes/agent_catalog.json",
        "indexes/agent_graph.json", "web/catalog.json", "web/documents.jsonl",
        "indexes/query_aliases.json", "mechanisms/bridge_candidates.json",
    ]
    before = {p: sha((repo / p).read_bytes()) for p in before_paths}
    generated_hashes = {p: sha(data) for p, data in sorted(stage.items())}
    plan = {
        "schema": "astra.gc-overlay-plan.v1", "intake_id": INTAKE, "pins": pins,
        "claim_ids": ids, "source_ids": sorted(source_ids), "gate_ids": [x["gate_id"] for x in gates],
        "notice_ids": [x["notice_id"] for x in notices], "bridge_ids": [x["id"] for x in bridges],
        "config_sha256": sha(config_raw), "base_registry_sha256": before,
        "staged_files": generated_hashes, "staged_file_count": len(stage),
        "next_commands": [
            "python3 frontier/build_access.py build --base-revision " + pins["base_revision"],
            "python3 frontier/build_access.py check --base-revision " + pins["base_revision"],
        ],
        "application": "NOT_PERFORMED; staged overlay is outside the repository",
        "scientific_validation": "NOT_PERFORMED; generated statuses remain source_derived_unreviewed and external fields UNKNOWN",
    }
    stage["PLAN.json"] = json_bytes(plan, sort=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=out.name + ".tmp-", dir=out.parent) as temp_name:
        temp_base = Path(temp_name).resolve()
        temp = temp_base / "payload"
        temp.mkdir()
        for relative, data in stage.items():
            target = (temp / relative).resolve()
            need(target.is_relative_to(temp), "Staged path escapes output directory: " + relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
        need(not out.exists(), "Output directory appeared during generation; refusing replacement")
        os.rename(temp, out)
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True, help="Read-only checked-out Astra repository")
    parser.add_argument("--config", type=Path, required=True, help="Root-authored claim_config.json outside the repository")
    parser.add_argument("--output", type=Path, required=True, help="New staging directory outside the repository")
    args = parser.parse_args()
    plan = build(args.repo, args.config, args.output)
    print(json.dumps({"status": "STAGED_FOR_REVIEW", "output": str(args.output.resolve()),
                      "files": plan["staged_file_count"], "cards": plan["claim_ids"],
                      "config_sha256": plan["config_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print("GC staging failed closed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
