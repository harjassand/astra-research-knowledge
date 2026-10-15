#!/usr/bin/env python3
"""Plan/apply FS public curation from finalized supplied data; no scientific inference.

Default is read-only. --apply additionally requires the finalized input hash, an
exact HEAD/base match, and a fresh read-only origin/main check. Existing scientific
artifacts are never replaced. Mutable registries receive additions only.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA = "astra.fs-curation-input.v1"
STATUS = "source_derived_unreviewed"
BOUNDARY = (
    "Source claims, supplied internal proofs, finite checks and same-team review remain "
    "unreviewed externally. External mathematical correctness, historical novelty and "
    "physical capability are UNKNOWN. Indexing, hashes and deterministic checks establish "
    "only their recorded integrity scope. Scientific review and capability gates remain open."
)
STATES = {
    "PROVEN LOGICAL DEPENDENCY", "ESTABLISHED COMPATIBLE INTERFACE",
    "CANDIDATE CONNECTION", "INCOMPATIBLE ASSUMPTIONS", "REFUTED TRANSFER",
}
INTERFACE = (
    "objects", "regime_and_quantifiers", "supplied_information", "acquired_information",
    "legal_access", "guarantee", "units_norm_and_precision", "costs",
)
RELATIONS = ("depends_on", "supersedes", "invalidates", "material_updates", "contrasting_blockers")


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value, *, sort=False):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=sort) + "\n").encode()


def required(obj, key):
    value = obj.get(key)
    need(isinstance(value, str) and value.strip(), "Required nonempty string: " + key)
    need(not value.startswith("REPLACE_"), "Unfilled template field: " + key)
    return value


def strings(obj, key, *, nonempty=True):
    value = obj.get(key)
    need(isinstance(value, list) and (value or not nonempty), "Required string array: " + key)
    need(all(isinstance(x, str) and x.strip() and not x.startswith("REPLACE_") for x in value),
         "Invalid string array: " + key)
    need(len(value) == len(set(value)), "Duplicate entry: " + key)
    return value


def safe_path(repo, name):
    need(isinstance(name, str) and name and not Path(name).is_absolute(), "Unsafe repository path")
    need(".." not in Path(name).parts, "Parent traversal is forbidden: " + name)
    result = (repo / name).resolve()
    need(result.is_relative_to(repo.resolve()), "Reference outside repository: " + name)
    return result


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def route(cid):
    return cid.split("-", 1)[0] if re.match(r"^[NL]\d+(?:-|$)", cid) else cid


def source_text(repo, ref):
    for name in dict.fromkeys([ref["path"], ref.get("read_path", "")]):
        if not name:
            continue
        p = safe_path(repo, name)
        if not p.is_file():
            continue
        data = p.read_bytes()
        if sha(data) == ref["sha256"]:
            return data.decode("utf-8")
        if p.suffix == ".html":
            for block in re.findall(r"<pre(?:\s[^>]*)?>(.*?)</pre>", data.decode("utf-8"), re.S):
                text = html.unescape(block)
                if sha(text.encode()) == ref["sha256"]:
                    return text
    raise ValueError("Evidence bytes/hash are not recoverable: " + ref["path"])


def source_page(title, path, data):
    try:
        text = data.decode("utf-8")
        body = "<pre>" + html.escape(text) + "</pre>"
    except UnicodeDecodeError:
        body = "<p>Original binary bytes; no text extraction substituted.</p>"
    return ("<!doctype html>\n<html lang=\"en\"><meta charset=\"utf-8\"><title>" +
            html.escape(title) + "</title><body><p>FS preserved source or supplied internal evidence; "
            "externally unreviewed. <a href=\"../../" + html.escape(path, quote=True) +
            "\">Exact bytes</a></p>" + body + "</body></html>\n").encode()


class Plan:
    def __init__(self, repo):
        self.repo = repo.resolve()
        self.before = {}
        self.after = {}
        self.owned = {}
        self.additions = {}

    def read(self, name):
        if name in self.after:
            return self.after[name]
        p = safe_path(self.repo, name)
        data = p.read_bytes() if p.is_file() else None
        self.before.setdefault(name, data)
        return data

    def load(self, name):
        data = self.read(name)
        need(data is not None, "Required registry absent: " + name)
        return json.loads(data)

    def rows(self, name):
        data = self.read(name)
        need(data is not None, "Required registry absent: " + name)
        return [json.loads(x) for x in data.decode().splitlines() if x.strip()]

    def new_file(self, name, data):
        old = self.read(name)
        need(old is None or old == data, "Immutable artifact collision: " + name)
        self.after[name] = data
        self.owned[name] = sha(data)

    @staticmethod
    def appended(old, additions, key, name):
        result = list(old)
        for item in additions:
            matches = [x for x in result if key(x) == key(item)]
            if matches:
                need(all(x == item for x in matches), "Conflicting existing identifier in " + name + ": " + str(key(item)))
            else:
                result.append(item)
        return result

    def append_jsonl(self, name, additions, key):
        old = self.rows(name)
        result = self.appended(old, additions, key, name)
        data = self.read(name)
        need(not data or data.endswith(b"\n"), "Registry needs a final newline; refusing old-byte repair: " + name)
        new = result[len(old):]
        self.after[name] = data + b"".join((json.dumps(x, ensure_ascii=False) + "\n").encode() for x in new)
        self.additions[name] = [key(x) for x in additions]

    def append_array(self, name, additions, key, field=None):
        document = self.load(name)
        old = document[field] if field else document
        updated = self.appended(old, additions, key, name + (":" + field if field else ""))
        if updated != old:
            if field:
                document[field] = updated
            else:
                document = updated
            self.after[name] = encoded(document)  # Preserve every historical JSON key order.
        self.additions[name + (":" + field if field else "")] = [key(x) for x in additions]

    def add_aliases(self, additions):
        name = "indexes/query_aliases.json"
        old = self.load(name)
        changed = False
        for key, value in additions.items():
            need(key not in old or old[key] == value, "Existing alias collision: " + key)
            if key not in old:
                old[key] = value
                changed = True
        if changed:
            self.after[name] = encoded(old)

    def summary(self):
        changed = {p: {"before_sha256": sha(self.before[p]) if self.before[p] is not None else None,
                       "after_sha256": sha(data), "bytes": len(data)}
                   for p, data in sorted(self.after.items()) if self.before[p] != data}
        return {"mode": "read_only_plan", "changed_file_count": len(changed), "files": changed,
                "scientific_boundary": BOUNDARY}


def build_plan(repo, curation, input_sha256):
    need(curation.get("schema") == SCHEMA, "Unsupported curation schema")
    need(curation.get("intake_id") == "FS", "This generator is scoped to FS")
    base = required(curation, "base_revision")
    need(re.fullmatch(r"[0-9a-f]{40}", base), "base_revision must be a full Git SHA")
    date_version = required(curation, "date_version")
    checkpoint_path = curation.get("checkpoint_path")
    if checkpoint_path is not None:
        safe_path(repo, checkpoint_path)
        need(checkpoint_path.startswith("state/checkpoints/") and checkpoint_path.endswith(".json"),
             "checkpoint_path must be a repository-relative checkpoint JSON path")
    plan = Plan(repo)
    existing_claims = plan.rows("indexes/claims.jsonl")
    known_cards = {x["id"] for x in existing_claims}
    old_metadata = plan.rows("indexes/source_metadata.jsonl")
    metadata = []
    source_by_path = {}
    for src in curation.get("sources", []):
        path = required(src, "path")
        need(path.startswith("updates/FS-phase-closure-20261015/"), "New indexed sources must be preserved under updates/FS-phase-closure-20261015/: " + path)
        data = plan.read(path)
        need(data is not None, "Preserved source is absent: " + path)
        expected = required(src, "sha256")
        need(sha(data) == expected, "Preserved source hash mismatch: " + path)
        sid = src.get("source_id", "src-FS-" + sha(path.encode())[:16])
        need(re.fullmatch(r"src-FS-[A-Za-z0-9_-]+", sid), "New source_id must use the FS namespace")
        need(path not in source_by_path, "Duplicate source path: " + path)
        try:
            data.decode("utf-8")
            extraction = "original_utf8_bytes"
        except UnicodeDecodeError:
            extraction = "original_binary_bytes"
        record = {"source_id": sid, "path": path, "title": required(src, "title"), "sha256": expected,
                  "bytes": len(data), "date_version": date_version, "read_depth": required(src, "read_depth"),
                  "reported_verification": BOUNDARY, "extraction": extraction}
        metadata.append(record)
        source_by_path[path] = record
        plan.new_file("web/pages/" + sid + ".html", source_page(record["title"], path, data))
    all_metadata = old_metadata + metadata
    evidence = {}
    for key, supplied in curation.get("evidence", {}).items():
        need(isinstance(key, str) and key.strip(), "Evidence keys must be named strings")
        ref = {"id": key, "path": required(supplied, "path"), "sha256": required(supplied, "sha256"),
               "lines": supplied.get("lines"), "range_scope": required(supplied, "range_scope"),
               "read_path": supplied.get("read_path", supplied["path"]),
               "hash_kind": supplied.get("hash_kind", "original_utf8_bytes"),
               "source_revision": supplied.get("source_revision"), "status": supplied.get("status", BOUNDARY)}
        need(re.fullmatch(r"[0-9a-f]{64}", ref["sha256"]), "Evidence hash must be full SHA256: " + key)
        lines = ref["lines"]
        need(isinstance(lines, list) and len(lines) == 2 and all(type(x) is int for x in lines), "Expected inclusive [first,last] lines: " + key)
        for dependency in dict.fromkeys([ref["path"], ref["read_path"]]):
            plan.read(dependency)
        text = source_text(repo, ref)
        need(1 <= lines[0] <= lines[1] <= len(text.splitlines()), "Invalid evidence range: " + key)
        if ref["source_revision"] is not None:
            need(re.fullmatch(r"[0-9a-f]{40}", ref["source_revision"]), "Evidence revision must be a full SHA or null")
        candidates = {x.get("source_id", x.get("id")) for x in all_metadata if x.get("path") == ref["path"] and x.get("sha256") == ref["sha256"] and x.get("source_id", x.get("id"))}
        sid = supplied.get("source_id")
        if sid is not None:
            need(sid in candidates, "Evidence source_id does not match metadata: " + key)
            ref["source_id"] = sid
        elif len(candidates) == 1:
            ref["source_id"] = next(iter(candidates))
        elif candidates:
            raise ValueError("Ambiguous evidence source_id; supply it explicitly: " + key)
        evidence[key] = ref
    need(evidence, "No selected evidence references supplied")

    def refs(obj, key="ref_ids"):
        names = strings(obj, key)
        need(all(x in evidence for x in names), "Unknown evidence key in " + key)
        return [evidence[x] for x in names]

    cards = curation.get("cards")
    need(isinstance(cards, list) and cards, "No cards supplied")
    card_ids = [required(x, "id") for x in cards]
    need(len(card_ids) == len(set(card_ids)), "Duplicate new card ID")
    need(all(re.fullmatch(r"N(?:840|841|842)-[a-z0-9-]+", x) for x in card_ids), "FS reservation is N840, N841, N842 only")
    need(len({route(x) for x in card_ids}) == len(card_ids), "Duplicate numeric route in input")
    for cid in card_ids:
        need(not any(route(old) == route(cid) and old != cid for old in known_cards), "Numeric route collision: " + route(cid))
    known_cards.update(card_ids)
    claim_rows, status_rows, catalog_rows, web_rows, graph_edges, graph_nodes, aliases = [], [], [], [], [], [], {}
    gates, claims_map, source_topics = [], [], {}
    for card in cards:
        cid = card["id"]
        title = required(card, "title")
        topics = strings(card, "topics")
        proof_refs = refs(card, "proof_refs")
        for ref in proof_refs:
            need("source_id" in ref, "Card proof must have indexed source metadata: " + ref["id"])
        scope = required(card, "scientific_scope")
        statement = required(card, "statement")
        assumptions = strings(card, "assumptions")
        proof_spine = strings(card, "proof_spine")
        fields = {k: required(card, k) for k in (
            "costs", "information_acquisition", "obstruction", "comparator", "missing_lemma",
            "next_decisive_step", "read_review_depth")}
        status_line = "status=" + STATUS + "; supplied claims and internal work remain externally unreviewed."
        body = [cid + " | " + title, status_line, "", scope, "", "Exact statement: " + statement,
                "Assumptions: " + "; ".join(assumptions), "Proof spine: " + "; ".join(proof_spine)]
        labels = {"costs": "Costs", "information_acquisition": "Supplied/acquired information boundary",
                  "obstruction": "Obstruction and failure scope", "comparator": "Comparator",
                  "missing_lemma": "Missing lemma or service", "read_review_depth": "Actual reading/review depth"}
        body += [labels[k] + ": " + fields[k] for k in labels]
        body += ["", *card.get("paragraphs", []), "", BOUNDARY, "",
                 "Exact proof routes: " + " ; ".join(dict.fromkeys(x["path"] for x in proof_refs)),
                 "Next decisive obligation: " + fields["next_decisive_step"]]
        raw = ("\n".join(body) + "\n").encode()
        card_path = "cards/" + cid + ".txt"
        digest = sha(raw)
        plan.new_file(card_path, raw)
        plan.new_file("frontier/review_cards/" + cid + ".txt", raw)
        plan.new_file("web/pages/" + cid + ".html", source_page(title, card_path, raw))
        relations = {}
        for name in RELATIONS:
            relations[name] = []
            for relation in card.get(name, []):
                r = {k: required(relation, k) for k in ("target", "scope", "relation_status")}
                r["evidence"] = refs(relation)
                if "whole_claim_invalidated" in relation:
                    need(relation["whole_claim_invalidated"] is False, "Whole-claim invalidation is outside this intake")
                    r["whole_claim_invalidated"] = False
                relations[name].append(r)
        st = {"schema_version": 1, "card_id": cid, "card_path": card_path, "card_sha256": digest,
              "title": title, "topics": topics, "claim_status": STATUS, "reported_status": status_line,
              "scientific_scope_status": scope, "status_authority": "FS supplied immutable evidence and scoped internal curation; " + BOUNDARY,
              "proof_availability": {"classification": "proof_text_located_not_completeness_audited",
                                     "classification_scope": "Selected supplied decisive ranges only; " + BOUNDARY,
                                     "located_proof_sources": proof_refs,
                                     "available_evidence_sources": refs(card, "inventory_refs") if card.get("inventory_refs") else []},
              "validation": {"internal": fields["read_review_depth"] + " This generator executes no scientific review.",
                             "external_correctness": "UNKNOWN", "historical_priority": "UNKNOWN",
                             "physical_capability": "UNKNOWN", "formal_verification": "UNKNOWN",
                             "empirical_confirmation": "UNKNOWN", "reported_status_evidence": proof_refs[:1]},
              **relations,
              "requires_external_validation": [{"target": "external:scope_matched_review_and_capability",
                  "scope": fields["next_decisive_step"], "relation_status": "open; not acquired by curation", "evidence": proof_refs[:1]}],
              "relation_coverage": "Selected scoped relations and paired contracts only; no topic-based dependency or exhaustive search.",
              "reported_failed_attempts": card.get("reported_failed_attempts", [])}
        plan.new_file("frontier/cards/" + cid + ".json", encoded(st, sort=True))
        status_rows.append(st)
        source_ids = list(dict.fromkeys(x["source_id"] for x in proof_refs))
        paths = list(dict.fromkeys(x["path"] for x in proof_refs))
        for sid in source_ids:
            source_topics.setdefault(sid, set()).update(topics)
        claim = {"id": cid, "title": title, "path": card_path, "topics": topics, "status": STATUS,
                 "source_ids": source_ids, "source_paths": paths,
                 "depends_on": [x["target"] for x in relations["depends_on"]], "scoped_dependencies": relations["depends_on"],
                 "tokens": None, "token_count_status": "not_measured", "record_type": "source_and_integration_derived_scoped_result"}
        claim_rows.append(claim)
        web_rows.append({**claim, "url": "pages/" + cid + ".html", "text": raw.decode()})
        catalog_rows.append({"id": cid, "title": title, "topics": topics, "status": STATUS, "card_sha256": digest,
             "dependencies": {"depends_on": claim["depends_on"], "scoped_dependencies": relations["depends_on"]},
             "pointers": {"card_local": card_path, "card_web": "frontier/dossiers/" + route(cid) + ".txt",
                          "current_status": "frontier/cards/" + cid + ".json", "reviewed_card": "frontier/review_cards/" + cid + ".txt",
                          "read_local": "python3 frontier/retrieve.py dossier " + route(cid),
                          "read_web": ["frontier/dossiers/" + route(cid) + ".txt", paths[0], "frontier/connections/" + route(cid) + ".json"]},
             "quoted_fields": {"status": [status_line], "interface": [scope], "limits": [fields["next_decisive_step"]]}})
        aliases[cid] = card.get("aliases", title + " " + " ".join(topics))
        graph_nodes.append({"id": cid, "node_kind": "claim"})
        for sid in source_ids:
            graph_edges.append({"from": cid, "to": sid, "kind": "provenance", "raw_kind": "source_or_internal_evidence",
                                "source": "FS", "composition": BOUNDARY})
        claims_map.append({"id": cid, "source_path": paths[0], "source_id": source_ids[0],
                           "source_sha256": proof_refs[0]["sha256"], "status": STATUS,
                           "missing_artifacts": card.get("missing_artifacts", []), "checkpoint": checkpoint_path, "workflow_trace": None})
        for suffix, question in [("REVIEW", "Independently review the exact statement, assumptions, proof obligations and nearest prior art for " + cid + "."),
                                 ("CAPABILITY", fields["next_decisive_step"])]:
            gates.append({"schema_version": 1, "gate_id": "G-FS-" + route(cid) + "-" + suffix,
                "card_ids": [cid], "gate_kind": "explicit_proof_or_acquisition_obligation",
                "title": "Open " + suffix.lower() + " obligation: " + route(cid), "question": question,
                "pass_condition": question + " Scope-matched independent evidence is required; metadata does not close this gate.",
                "status": "open", "completion_evidence": [], "evidence": proof_refs[:1],
                "priority_order": int(route(cid)[1:]), "priority_rationale": "Stable retrieval order only; no impact/readiness ranking.",
                "validation_boundary": BOUNDARY})
    for meta in metadata:
        graph_nodes.append({"id": meta["source_id"], "node_kind": "source"})
    # Existing source nodes must already exist; do not silently invent a historical graph repair.
    graph = plan.load("indexes/agent_graph.json")
    node_ids = {x["id"] for x in graph["nodes"] + graph_nodes}
    need(all(x["to"] in node_ids for x in graph_edges), "Referenced existing source is absent from the graph")

    notices = []
    for item in curation.get("notices", []):
        nid = required(item, "notice_id")
        need(nid.startswith("SN-FS-"), "Notice must use FS namespace")
        ids = strings(item, "card_ids")
        need(set(ids) <= known_cards, "Unknown semantic-notice card")
        clarification = required(item, "clarification")
        notices.append({"notice_id": nid, "card_ids": ids, "issue": required(item, "issue"),
            "status": "unreviewed_scoped_update", "clarification": clarification,
            "material_updates": [{"target": cid, "scope": clarification,
                "relation_status": "Scoped supplied internal update; prior evidence and open gates retained."} for cid in ids],
            "source_refs": refs(item), "source_revision": base, "whole_claim_invalidated": False})
    bridges = []
    for item in curation.get("bridges", []):
        bid = required(item, "id")
        need(bid.startswith("FS_"), "Bridge must use FS namespace")
        state = required(item, "state")
        need(state in STATES, "Invalid bridge state")
        ids = strings(item, "cards")
        need(set(ids) <= known_cards, "Unknown bridge card")
        sides = {side: {k: required(item.get(side, {}), k) for k in INTERFACE}
                 for side in ("source_interface", "destination_interface")}
        alignment = required(item, "alignment")
        missing = required(item, "missing_lemma")
        reciprocity = item.get("reciprocity", {"forward": missing, "reverse": "No broader converse, regime or scientific status is established."})
        need(all(isinstance(reciprocity.get(k), str) and reciprocity[k] for k in ("forward", "reverse")), "Incomplete bridge reciprocity")
        bridges.append({"id": bid, "state": state, "status": state, "kind": "scoped_supplied_proof_or_interface_audit",
            "cards": ids, **sides, "alignment": alignment,
            "assumptions": [sides[s]["regime_and_quantifiers"] for s in sides] + [BOUNDARY],
            "acquisition": "; ".join(sides[s]["acquired_information"] for s in sides),
            "cost": "; ".join(sides[s]["costs"] for s in sides), "missing_lemma": missing,
            "falsifier": required(item, "falsifier"), "scope": alignment + " " + BOUNDARY,
            "evidence_refs": refs(item), "reciprocity": reciprocity})
    for item in curation.get("gates", []):
        gid = required(item, "gate_id")
        need(gid.startswith("G-FS-"), "Gate must use FS namespace")
        ids = strings(item, "card_ids")
        need(set(ids) <= known_cards, "Unknown gate card")
        gates.append({"schema_version": 1, "gate_id": gid, "card_ids": ids,
            "gate_kind": "explicit_proof_or_acquisition_obligation", "title": required(item, "title"),
            "question": required(item, "question"), "pass_condition": required(item, "pass_condition"),
            "status": "open", "completion_evidence": [], "evidence": refs(item),
            "priority_order": item.get("priority_order", 824), "priority_rationale": "Retrieval order only; no impact/readiness ranking.",
            "validation_boundary": BOUNDARY})

    key_id = lambda x: x["id"]
    plan.append_jsonl("indexes/claims.jsonl", claim_rows, key_id)
    plan.append_jsonl("frontier/CURRENT_CLAIM_STATUS.jsonl", status_rows, lambda x: x["card_id"])
    plan.append_jsonl("indexes/source_metadata.jsonl", metadata, lambda x: x.get("source_id", x.get("id")))
    plan.append_jsonl("frontier/OPEN_PROOF_GATES.jsonl", gates, lambda x: x["gate_id"])
    plan.append_jsonl("agent/SEMANTIC_NOTICES.jsonl", notices, lambda x: x["notice_id"])
    plan.append_array("indexes/agent_catalog.json", catalog_rows, key_id, "claims")
    plan.append_array("indexes/agent_graph.json", graph_nodes, key_id, "nodes")
    plan.append_array("indexes/agent_graph.json", graph_edges,
                      lambda x: (x["from"], x["to"], x["kind"], x["raw_kind"], x.get("source")), "edges")
    plan.append_array("web/catalog.json", web_rows, key_id)
    documents = [{"id": m["source_id"], "path": m["path"], "title": m["title"], "role": "source", "cycle": 0,
                  "topics": sorted(source_topics.get(m["source_id"], [])), "extraction": m["extraction"], "tokens": None,
                  "url": "pages/" + m["source_id"] + ".html"} for m in metadata]
    documents += [{"id": x["id"], "path": x["path"], "title": x["title"], "role": "card", "cycle": 0,
                   "topics": x["topics"], "extraction": "original_utf8_bytes", "tokens": None, "url": x["url"]} for x in web_rows]
    plan.append_jsonl("web/documents.jsonl", documents, key_id)
    plan.add_aliases(aliases)
    rejected = [x for x in bridges if x["state"] in {"INCOMPATIBLE ASSUMPTIONS", "REFUTED TRANSFER"}]
    accepted = [x for x in bridges if x not in rejected]
    plan.append_array("mechanisms/bridge_candidates.json", accepted, key_id, "bridges")
    plan.append_array("mechanisms/bridge_candidates.json", rejected, key_id, "rejected_transfers")
    for bridge in bridges:
        plan.new_file("mechanisms/bridges/" + bridge["id"] + ".json", encoded(bridge, sort=True))
    for name, data in {
        "CURATION.json": {"schema": SCHEMA, "base_revision": base, "new_cards": card_ids,
                          "scientific_status": STATUS, "external_truth_certified": False,
                          "architecture_change": "None; existing public curation and projection schemas.", "boundary": BOUNDARY},
        "CLAIMS.json": {"schema": "astra.intake-claim-map.v1", "intake_id": "FS", "base_revision": base, "claims": claims_map},
        "INDEXED_SOURCES.json": {"schema": "astra.fs-indexed-sources.v1", "base_revision": base, "files": metadata, "boundary": BOUNDARY},
        "EVIDENCE_REFS.json": {"schema": "astra.fs-selected-evidence.v1", "evidence": evidence, "boundary": BOUNDARY},
        "SCOPED_NOTICES.json": notices,
        "BRIDGES.json": {"base_revision": base, "bridges": bridges},
    }.items():
        plan.new_file("updates/FS-phase-closure-20261015/" + name, encoded(data, sort=True))
    receipt = {"schema": "astra.fs-generator-receipt.v1", "base_revision": base,
               "curation_input_sha256": input_sha256, "generator_sha256": sha(Path(__file__).read_bytes()),
               "cards": card_ids, "source_count": len(metadata), "notice_ids": [x["notice_id"] for x in notices],
               "bridge_ids": [x["id"] for x in bridges], "gate_ids": [x["gate_id"] for x in gates],
               "owned_artifacts": dict(sorted(plan.owned.items())), "boundary": BOUNDARY,
               "checkpoint_and_technology": "Handled separately; this generator publishes neither.",
               "next_commands": ["python3 frontier/build_access.py build --base-revision " + base,
                                 "python3 frontier/build_access.py check --base-revision " + base]}
    plan.new_file("updates/FS-phase-closure-20261015/INTEGRATION_GENERATOR_RECEIPT.json", encoded(receipt, sort=True))
    return plan


def apply_plan(plan):
    # Preflight every input before any write. Interrupted apply is safe to rerun with
    # the same finalized input: immutable files and registry identifiers must match.
    for name, before in plan.before.items():
        p = safe_path(plan.repo, name)
        current = p.read_bytes() if p.is_file() else None
        need(current == before, "Concurrent modification detected; replan: " + name)
    changed = [(p, data) for p, data in plan.after.items() if plan.before[p] != data]
    for name, data in changed:
        p = safe_path(plan.repo, name)
        p.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=p.parent, prefix=".fs-curation-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            if plan.before[name] is None:
                os.link(temporary, p)  # Exclusive, atomic publication of complete new bytes.
            else:
                os.replace(temporary, p)
        finally:
            temporary.unlink(missing_ok=True)
    return len(changed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Read-only plan (default)")
    mode.add_argument("--apply", action="store_true", help="Apply finalized curation; explicit hash and fresh remote check required")
    parser.add_argument("--expect-input-sha256", help="Required with --apply")
    parser.add_argument("--report", type=Path, help="Optional external JSON plan report; cannot be inside the repository")
    args = parser.parse_args()
    repo = args.repo.resolve()
    input_data = args.input.read_bytes()
    input_sha = sha(input_data)
    curation = json.loads(input_data)
    need(not args.report or not args.report.resolve().is_relative_to(repo), "Plan reports must stay outside the repository")
    if args.expect_input_sha256:
        need(input_sha == args.expect_input_sha256, "Finalized curation input changed")
    lock_path = None
    if args.apply:
        need(args.expect_input_sha256, "--apply requires --expect-input-sha256")
        base = curation.get("base_revision")
        need(git(repo, "rev-parse", "HEAD") == base, "HEAD changed; refresh/reconcile curation base before applying")
        remote = git(repo, "ls-remote", "--heads", "origin", "main").split()
        need(remote and remote[0] == base, "Remote main changed; refresh and recheck reserved IDs before applying")
        lock_path = Path(git(repo, "rev-parse", "--git-path", "fs-curation.lock"))
        if not lock_path.is_absolute():
            lock_path = repo / lock_path
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.write(descriptor, (str(os.getpid()) + "\n").encode())
        os.close(descriptor)
    try:
        plan = build_plan(repo, curation, input_sha)
        report = plan.summary()
        report.update({"curation_input_sha256": input_sha, "base_revision": curation.get("base_revision")})
        if args.apply:
            need(args.input.read_bytes() == input_data, "Finalized curation input changed during planning")
            report["applied_file_count"] = apply_plan(plan)
            report["mode"] = "applied_without_projection_or_publication"
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_bytes(encoded(report, sort=True))
        print(json.dumps({k: v for k, v in report.items() if k != "files"}, ensure_ascii=False, indent=2))
    finally:
        if lock_path is not None:
            lock_path.unlink(missing_ok=True)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print("FS curation failed closed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
