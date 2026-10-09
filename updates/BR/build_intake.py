#!/usr/bin/env python3
"""Reproduce the BR public intake; verify originals, never execute research code.

Uses existing public ledgers/graph/catalog. No private SQLite rebuild is claimed.
Prepare every output in memory before writing; publication is a reviewed Git commit.
The same input is idempotent. Check mode performs no writes.
"""
import argparse
import hashlib
import html
import json
import stat
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
PREFIX = "updates/BR/package/research_packet/"
SCOPED_READ = {"RESEARCH_REPORT.txt", "CLAIM_LEDGER.json", "CROSS_BRANCH_HANDOFF.txt",
               "SOURCE_MANIFEST.json", "PORTABLE_REPLAY.json", "START_HERE.txt",
               "work/calibration_audit/audit.txt", "work/gaussian_displaced_audit/report.txt",
               "work/gaussian_transfer/displaced_followup.txt", "work/gaussian_transfer/displaced_parity_audit.txt",
               "work/gaussian_transfer/displaced_gate.txt", "work/gaussian_software_audit/report.txt"}
STATUS = "source_derived_unreviewed"
BOUNDARY = ("Source-reported internal model-assisted proof/review and finite software checks; "
            "not replayed or independently reconstructed during intake. No historic-scale "
            "breakthrough, external expert/formal verification, physical acquisition or historical "
            "novelty is established. Theoretical bit-cost bounds do not certify uniform runtime "
            "of the particular numerical implementation.")
BV_BOUNDARY = ("Source-reported analytic derivations and synthetic numerical diagnostics; no "
               "external proof review, formal verification, publication-priority clearance or "
               "physical system identification is established. No historic-scale or 9–10/10 "
               "breakthrough is claimed. This intake checked source/archive integrity and static "
               "repository routes only; it did not rerun scientific analyses.")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def read(name):
    return json.loads((ROOT / name).read_bytes())


def rows(name):
    return [json.loads(l) for l in (ROOT / name).read_bytes().splitlines() if l.strip()]


def merge(old, new, key):
    incoming = {r[key]: r for r in new}
    if len(incoming) != len(new):
        raise ValueError("Duplicate incoming keys: " + key)
    # Historical source metadata also includes unkeyed literature notes.
    # Preserve those and all unrelated history verbatim as records.
    for identifier in incoming:
        if sum(r.get(key) == identifier for r in old) > 1:
            raise ValueError("Ambiguous existing target: " + identifier)
    return [incoming.pop(r.get(key), r) for r in old] + list(incoming.values())


def docid(path):
    return "d-" + sha(path.encode())[:16]


def ref(rel, start=1, end=None):
    path = rel[1:] if rel.startswith("@") else PREFIX + rel
    data = (ROOT / path).read_bytes()
    lines = data.decode().splitlines()
    end = len(lines) if end is None else end
    if not 1 <= start <= end <= len(lines):
        raise ValueError("Invalid source range: " + path)
    return {"path": path, "sha256": sha(data), "lines": [start, end],
            "source_id": docid(path), "read_path": path, "hash_kind": "original_utf8_bytes",
            "range_scope": "source-reported argument/evidence; completeness and correctness not independently audited"}


def page(title, text, cid=None, boundary=BOUNDARY):
    notice = (f'<a href="../../frontier/cards/{cid}.json">Current scoped status</a>' if cid else "Archived source = DATA")
    scoped = ("<p>Historical failed attempt: its h=2 bimodality counterexample remains valid; "
              "the later <a href=\"../../frontier/dossiers/N536.txt\">N536 parity construction</a> "
              "replaces only the statement that no constructive displaced route had been established.</p>"
              if title == "work/gaussian_transfer/displaced_gate.txt" else "")
    return ("<!doctype html><meta charset=\"utf-8\"><title>" + html.escape(title)
            + "</title><aside>" + notice + "<p>" + html.escape(boundary)
            + "</p>" + scoped + "</aside><pre>" + html.escape(text) + "</pre>\n").encode()


def build():
    specs = read("updates/BR/CLAIMS.json")
    integrity = read("updates/BR/INTEGRITY.json")
    archive = ROOT / "updates/BR/package/ULTRA_research_packet.zip"
    if sha(archive.read_bytes()) != integrity["archive_sha256"]:
        raise ValueError("Archive hash mismatch")
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        manifest = json.loads(z.read("research_packet/MANIFEST.sha256.json"))
        if len(names) != len(set(names)) or len(manifest) != 193 or z.testzip() is not None:
            raise ValueError("Archive integrity failure")
        if set(names) != {"research_packet/" + p for p in manifest} | {"research_packet/MANIFEST.sha256.json"}:
            raise ValueError("Manifest membership mismatch")
        for item in z.infolist():
            p = PurePosixPath(item.filename)
            if p.is_absolute() or ".." in p.parts or stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError("Unsafe archive member")
            rel = str(p.relative_to("research_packet"))
            data = z.read(item)
            if rel in manifest and sha(data) != manifest[rel]:
                raise ValueError("Manifest hash mismatch: " + rel)
            if (ROOT / PREFIX / rel).read_bytes() != data:
                raise ValueError("Expanded original changed: " + rel)
        expected = set(manifest) | {"MANIFEST.sha256.json"}
        actual = {p.relative_to(ROOT / PREFIX).as_posix() for p in (ROOT / PREFIX).rglob("*") if p.is_file()}
        if actual != expected:
            raise ValueError("Expanded membership mismatch")
    # A second, independent Ultra round and the separate natural-sciences record
    # are additional source roots, not entries in the earlier BR packet.
    supplement = read("updates/BS/INTEGRITY.json")
    archive2_rel = supplement["evidence_archive"]
    archive2 = ROOT / archive2_rel
    if sha(archive2.read_bytes()) != supplement["archive_sha256"]:
        raise ValueError("BS archive hash mismatch")
    tree2 = "updates/BS/package/evidence"
    source_items = [{"path": PREFIX + rel, "rel": rel, "title": rel,
                     "data": (ROOT / PREFIX / rel).read_bytes(), "depth": "scoped review; see source map"}
                    for rel in sorted(expected)]
    with zipfile.ZipFile(archive2) as z:
        manifest = json.loads(z.read("MANIFEST.json"))
        files = manifest["files"]
        if len(z.namelist()) != len(set(z.namelist())) or len(files) != 96 or z.testzip() is not None:
            raise ValueError("BS archive integrity failure")
        if set(z.namelist()) != set(files) | {"MANIFEST.json"}:
            raise ValueError("BS archive/manifest membership mismatch")
        for info in z.infolist():
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Unsafe BS archive member")
            data = z.read(info)
            target = (ROOT / tree2 / info.filename) if info.filename != "MANIFEST.json" else ROOT / tree2 / "MANIFEST.json"
            if target.read_bytes() != data:
                raise ValueError("BS expanded source differs from archive: " + info.filename)
            expected_hash = files.get(info.filename)
            if expected_hash and (len(data) != expected_hash["bytes"] or sha(data) != expected_hash["sha256"]):
                raise ValueError("BS source hash mismatch: " + info.filename)
            source_items.append({"path": tree2 + "/" + info.filename, "rel": info.filename,
                                 "title": info.filename, "data": data,
                                 "depth": "scoped source inspection; not full independent verification" if info.filename in {
                                     "RESEARCH_REPORT.txt", "SPECTRAL_PROOF.txt", "RARE_EVENT_PROOF.txt",
                                     "GAUSSIAN_CONDITIONING_PROOF.txt", "EQUILIBRIUM_PROOF.txt",
                                     "CLAIM_LEDGER.json", "BRANCH_HANDOFFS.json", "PORTABLE_REPLAY.json"}
                                 else "hash and archive membership only; not reviewed"})
    bt_path = "updates/BT/package/research_record.md"
    bt_data = (ROOT / bt_path).read_bytes()
    bt_origin = supplement["natural_science_record"]
    if sha(bt_data) != bt_origin["sha256"] or len(bt_data) != bt_origin["bytes"]:
        raise ValueError("BT attached record hash mismatch")
    source_items.append({"path": bt_path, "rel": "research_record.md", "title": "Delayed division responses: a falsification-first continuation",
                         "data": bt_data, "depth": "complete attached record read; cited code/data bundle not supplied"})
    # BU is the first Primitive Genesis handoff. Preserve the exact folder and
    # its sibling ZIP; verify both against the internal SHA-256 manifest.
    genesis = read("updates/BU/INTEGRITY.json")
    archive3_rel = genesis["archive_path"]
    archive3 = ROOT / archive3_rel
    if sha(archive3.read_bytes()) != genesis["archive_sha256"] or len(archive3.read_bytes()) != genesis["archive_bytes"]:
        raise ValueError("BU archive hash/size mismatch")
    tree3 = "updates/BU/package/primitive_genesis_retention"
    manifest_path = ROOT / tree3 / "MANIFEST.sha256"
    manifest3 = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, rel = line.split(None, 1)
            manifest3[rel.strip().lstrip("*")] = digest
    if len(manifest3) != 14 or sha(manifest_path.read_bytes()) != genesis["manifest_sha256"]:
        raise ValueError("BU source manifest mismatch")
    with zipfile.ZipFile(archive3) as z:
        names = z.namelist()
        expected_names = {"primitive_genesis_retention/" + p for p in manifest3} | {
            "primitive_genesis_retention/MANIFEST.sha256"}
        if len(names) != 15 or len(names) != len(set(names)) or set(names) != expected_names or z.testzip() is not None:
            raise ValueError("BU archive membership/CRC failure")
        for info in z.infolist():
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Unsafe BU archive member")
            rel = str(member.relative_to("primitive_genesis_retention"))
            data = z.read(info)
            target = ROOT / tree3 / rel
            if not target.is_file() or target.read_bytes() != data:
                raise ValueError("BU expanded source differs from archive: " + rel)
            if rel in manifest3 and sha(data) != manifest3[rel]:
                raise ValueError("BU source hash mismatch: " + rel)
            if rel == "MANIFEST.sha256":
                source_items.append({"path": tree3 + "/" + rel, "rel": rel, "title": rel,
                                     "data": data, "depth": "internal source checksum manifest; hashes independently checked"})
                continue
            reviewed = rel in {"README.md", "RESEARCH_NOTE.md", "QUANTUM_ORBIT_EXTENSION.md",
                               "HANDOFF.md", "CLAIMS.json", "SOURCE_PROVENANCE.json",
                               "CHECKER_CORRECTION.json"}
            source_items.append({"path": tree3 + "/" + rel, "rel": rel, "title": rel,
                                 "data": data,
                                 "depth": "scoped source reading; not independently proof-verified" if reviewed
                                 else "preserved receipt or code; no scientific verifier executed"})
    summary_path = "updates/BU/PRESENTED_SUMMARY.txt"
    summary_data = (ROOT / summary_path).read_bytes()
    if sha(summary_data) != genesis["presented_summary_sha256"] or len(summary_data) != genesis["presented_summary_bytes"]:
        raise ValueError("BU pasted-summary hash/size mismatch")
    source_items.append({"path": summary_path, "rel": "PRESENTED_SUMMARY.txt", "title": "User-pasted Primitive Genesis summary",
                         "data": summary_data, "depth": "abridged conversational summary; full source note is authoritative"})

    # BV is a separate stationary-generator investigation. Preserve its exact
    # source folder and verify the sibling ZIP, manifest and expanded bytes;
    # never execute embedded research scripts during repository intake.
    tomography = read("updates/BV/INTEGRITY.json")
    archive4_rel = tomography["archive_path"]
    archive4 = ROOT / archive4_rel
    if sha(archive4.read_bytes()) != tomography["archive_sha256"] or len(archive4.read_bytes()) != tomography["archive_bytes"]:
        raise ValueError("BV archive hash/size mismatch")
    tree4 = "updates/BV/package/astra_static_generator_tomography"
    manifest4_path = ROOT / tree4 / "MANIFEST.json"
    manifest4_bytes = manifest4_path.read_bytes()
    if sha(manifest4_bytes) != tomography["manifest_sha256"]:
        raise ValueError("BV source manifest hash mismatch")
    manifest4 = json.loads(manifest4_bytes)
    files4 = manifest4["files"]
    expected4 = {"astra_static_generator_tomography/" + item["path"] for item in files4} | {
        "astra_static_generator_tomography/MANIFEST.json"}
    if len(files4) != 17:
        raise ValueError("BV manifest file count mismatch")
    with zipfile.ZipFile(archive4) as z:
        names = z.namelist()
        if len(names) != 18 or len(names) != len(set(names)) or set(names) != expected4 or z.testzip() is not None:
            raise ValueError("BV archive membership/CRC failure")
        hashes4 = {item["path"]: item for item in files4}
        for info in z.infolist():
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Unsafe BV archive member")
            rel = str(member.relative_to("astra_static_generator_tomography"))
            data = z.read(info)
            target = ROOT / tree4 / rel
            if not target.is_file() or target.read_bytes() != data:
                raise ValueError("BV expanded source differs from archive: " + rel)
            item = hashes4.get(rel)
            if item and (len(data) != item["bytes"] or sha(data) != item["sha256"]):
                raise ValueError("BV source hash mismatch: " + rel)
            if rel == "MANIFEST.json":
                source_items.append({"path": tree4 + "/" + rel, "rel": rel, "title": rel,
                                     "data": data, "depth": "embedded source integrity manifest; hashes independently checked",
                                     "boundary": BV_BOUNDARY})
                continue
            reviewed = rel in {"README.md", "RESEARCH_HANDOFF.md", "ASTRA_BRIDGE.txt",
                               "ASTRA_SESSION_RECORD.json", "proof_checks_results.json",
                               "results.json", "torus_results.json", "entropy_production_results.json",
                               "stein_results.json", "matched_comparator_results.json"}
            source_items.append({"path": tree4 + "/" + rel, "rel": rel, "title": rel,
                                 "data": data,
                                 "depth": "scoped source/result inspection; not independently proof-verified" if reviewed
                                 else "preserved source code or environment record; no research code executed",
                                 "boundary": BV_BOUNDARY})
    secondary_expected = {i["path"] for i in source_items if not i["path"].startswith(PREFIX)}
    secondary_actual = {p.relative_to(ROOT).as_posix() for root in [ROOT / tree2, ROOT / "updates/BT/package", ROOT / tree3, ROOT / tree4]
                        for p in root.rglob("*") if p.is_file()}
    secondary_actual.add(summary_path)
    if secondary_actual != secondary_expected:
        raise ValueError("Supplemental source tree membership mismatch")
    outputs = {}

    def put(path, data):
        outputs[path] = data

    def put_json(path, obj):
        put(path, encoded(obj))

    def put_rows(path, data):
        put(path, b"".join((json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n").encode() for r in data))

    new_claims, new_statuses, new_catalog, new_docs, new_sources, new_gates = [], [], [], [], [], []
    aliases = read("indexes/query_aliases.json")
    graph = read("indexes/agent_graph.json")
    catalog = read("indexes/agent_catalog.json")
    nodes = {r["id"]: r for r in graph["nodes"]}
    extra_edges = []
    resolve_source = lambda rel: rel[1:] if rel.startswith("@") else PREFIX + rel
    selected = {resolve_source(r[0]) for s in specs["claims"] for r in s["proofs"]}
    selected |= {resolve_source(r) for s in specs["claims"] for r in s["evidence"]}
    selected |= {resolve_source(r) for s in specs["claims"] for r in s.get("status_evidence", [])}
    source_topics = {}
    for claim_spec in specs["claims"]:
        refs = [r[0] for r in claim_spec["proofs"]] + claim_spec["evidence"] + claim_spec.get("status_evidence", [])
        for source_ref in refs:
            source_topics.setdefault(resolve_source(source_ref), set()).update(claim_spec["topics"])
    for source in sorted(source_items, key=lambda s: s["path"]):
        path, rel, data = source["path"], source["rel"], source["data"]
        sid = docid(path)
        try:
            text = data.decode("utf-8")
            extraction = "exact_utf8"
        except UnicodeError:
            text = None
            extraction = "binary_preserved"
        title = source["title"]
        new_sources.append({"source_id": sid, "path": path, "title": title, "sha256": sha(data),
                            "bytes": len(data), "date_version": "2026-10-10 immutable original",
                            "read_depth": source.get("depth", "Hash and membership only; not reviewed"),
                            "reported_verification": source.get("boundary", BOUNDARY), "extraction": extraction})
        if path in selected:
            nodes[sid] = {"id": sid, "node_kind": "evidence", "path": path, "title": title, "role": "source"}
            put("web/pages/" + sid + ".html", page(title, text, boundary=source.get("boundary", BOUNDARY)))
            new_docs.append({"id": sid, "path": path, "title": title, "role": "source", "cycle": 0,
                             "topics": sorted(source_topics.get(path, set())), "extraction": extraction, "tokens": None,
                             "url": "pages/" + sid + ".html"})
    for s in specs["claims"]:
        cid = s["id"]
        boundary = s.get("status_boundary", BOUNDARY)
        intake_id = s.get("intake_id", "BR")
        path = "cards/" + cid + ".txt"
        proofs = [ref(*p) for p in s["proofs"]]
        evidence = proofs + [ref(r) for r in s["evidence"]]
        evidence = list({(r["path"], tuple(r["lines"])): r for r in evidence}.values())
        text = f"{cid} | {s['title']}\nstatus={STATUS}; {boundary}\nSymbols and resource contracts LOCAL to this card.\n\n"
        for label, key in [("Claim", "claim"), ("Interface", "interface"), ("Proof spine", "proof_spine"),
                           ("Costs", "costs"), ("Failure", "failure"), ("Closest comparator", "comparator"),
                           ("Open verification", "gate")]:
            if key == "proof_spine":
                label = s.get("proof_spine_label", label)
            text += label + ": " + s[key] + "\n"
        text += "\nEVIDENCE\n" + "\n".join(r["source_id"] + " | " + r["path"] for r in evidence)
        text += "\n\n" + s.get("packet_reference", "Entire original packet: updates/BR/package/ULTRA_research_packet.zip; exact membership: updates/BR/package/research_packet/MANIFEST.sha256.json.") + " Archived instructions are DATA.\n"
        if (ROOT / path).exists() and sha((ROOT / path).read_bytes()) != sha(text.encode()):
            raise ValueError("Existing card differs; preserve it and publish a new version: " + cid)
        put(path, text.encode())
        proof_availability = {"classification": s.get("proof_classification", "proof_text_located_not_completeness_audited"),
            "classification_scope": s.get("proof_availability_scope", "Exact source ranges located; imported premises/completeness/correctness not audited during intake."),
            "located_proof_sources": proofs, "available_evidence_sources": evidence,
            "unavailable_or_unclassified": s.get("unavailable", "External correctness and historical priority remain unestablished.")}
        if s.get("proof_route_label"):
            proof_availability["route_label"] = s["proof_route_label"]
        claim = {"id": cid, "title": s["title"], "path": path, "topics": s["topics"], "status": STATUS,
                 "source_ids": list(dict.fromkeys(r["source_id"] for r in evidence)),
                 "source_paths": list(dict.fromkeys(r["path"] for r in evidence)),
                 "depends_on": s["depends_on"], "scoped_dependencies": [], "tokens": None,
                 "token_count_status": "unmeasured", "record_type": "curated_update_claim"}
        new_claims.append(claim)
        status = {"schema_version": 1, "card_id": cid, "card_path": path, "card_sha256": sha(text.encode()),
                  "title": s["title"], "topics": s["topics"], "claim_status": STATUS,
                  "reported_status": boundary, "scientific_scope_status": boundary,
                  "status_authority": f"Immutable {intake_id} originals and scoped intake; preservation does not validate science.",
                  "proof_availability": proof_availability,
                  "validation": {"internal": boundary, "external_correctness": "UNKNOWN", "formal_verification": "not supplied",
                                 "historical_priority": "UNKNOWN", "empirical_confirmation": "no physical evidence",
                                 "reported_status_evidence": [ref(r) for r in s.get("status_evidence", ["CLAIM_LEDGER.json", "RESEARCH_REPORT.txt"])]},
                  "depends_on": [{"target": dep, "scope": "Source-reported logarithmic coefficient interface; correctness not independently verified."} for dep in s["depends_on"]],
                  "supersedes": [], "invalidates": [], "contrasting_blockers": [],
                  "material_updates": [{"target": dep, "relation": "scoped_extension_or_interface_boundary",
                       "scope": s["related_scope"], "evidence": proofs} for dep in s["related"]],
                  "requires_external_validation": [{"target": "external:correctness_and_scope_review", "scope": s["gate"], "evidence": proofs}],
                  "relation_coverage": "Explicit source evidence only; no automatic logical composition or exhaustive relations."}
        new_statuses.append(status)
        put_json("frontier/cards/" + cid + ".json", status)
        notice = {"card_id": cid, "reported_claim_status": STATUS,
                  "proof_availability": status["proof_availability"]["classification"],
                  "material_updates": status["material_updates"], "status_path": "frontier/cards/" + cid + ".json"}
        put("frontier/review_cards/" + cid + ".txt", ("CURRENT STATUS: " + json.dumps(notice, ensure_ascii=False, separators=(",", ":"))
            + "\nORIGINAL CARD (unchanged bytes after this line):\n" + text).encode())
        card_sid = docid(path)
        put("web/pages/" + card_sid + ".html", page(s["title"], text, cid, boundary=boundary))
        new_docs.append({"id": card_sid, "path": path, "title": s["title"], "role": "card", "cycle": 0,
                         "topics": s["topics"], "extraction": "curated_summary", "tokens": None, "url": "pages/" + card_sid + ".html"})
        new_sources.append({"source_id": card_sid, "path": path, "title": s["title"], "sha256": sha(text.encode()),
                            "date_version": "2026-10-10 " + intake_id + " curated summary", "read_depth": "Scoped summary, no independent proof replay",
                            "reported_verification": boundary, "extraction": "curated_summary"})
        item = {"id": cid, "title": s["title"], "status": STATUS, "topics": s["topics"], "card_sha256": sha(text.encode()),
                "dependencies": {"depends_on": s["depends_on"], "scoped_dependencies": []},
                "pointers": {"card_local": path, "current_status": "frontier/cards/" + cid + ".json",
                             "reviewed_card": "frontier/review_cards/" + cid + ".txt",
                             "read_local": "python3 frontier/retrieve.py dossier " + cid,
                             "card_web": "web/pages/" + card_sid + ".html",
                             "read_web": ["web/pages/" + sid + ".html" for sid in claim["source_ids"]]},
                "quoted_fields": {"interface": ["Interface: " + s["interface"]], "failure": ["Failure: " + s["failure"]]}}
        new_catalog.append(item)
        aliases[cid] = " ".join(s["aliases"])
        nodes[cid] = {"id": cid, "node_kind": "claim"}
        for sid in claim["source_ids"]:
            extra_edges.append({"from": cid, "to": sid, "kind": "provenance", "raw_kind": "supported_by",
                                "source": intake_id + " source locator", "composition": "never_proof_by_itself"})
        for dep in s["related"]:
            extra_edges.append({"from": cid, "to": dep, "kind": "navigation", "raw_kind": "links_to_not_logical_dependency",
                                "source": intake_id + " scoped interface comparison", "composition": "forbidden"})
        for dep in s["depends_on"]:
            extra_edges.append({"from": cid, "to": dep, "kind": "explicit_requirement", "raw_kind": "requires",
                                "source": intake_id + " source-reported proof obligation", "composition": "obligation_only"})
        new_gates.append({"schema_version": 1, "gate_id": "G-" + intake_id + "-" + cid.split("-")[0],
                          "priority_order": s.get("gate_priority_order", 92 + len(new_gates)),
                          "title": s["gate"], "status": "open", "gate_kind": "independent_proof_or_interface_obligation",
                          "card_ids": [cid], "question": s["gate"], "pass_condition": s["gate"],
                          "priority_rationale": "Scoped unresolved obligation; no predicted breakthrough value.",
                          "evidence": proofs, "completion_evidence": [], "validation_boundary": boundary})

    statuses = rows("frontier/CURRENT_CLAIM_STATUS.jsonl")
    for old in statuses:
        for s, new in zip(specs["claims"], new_statuses):
            if old["card_id"] in s["related"]:
                update = {"target": s["id"], "relation": "scoped_followup_not_invalidation",
                          "scope": s["related_scope"], "evidence": new["proof_availability"]["located_proof_sources"]}
                old["material_updates"] = [u for u in old["material_updates"] if u.get("target") != s["id"]] + [update]
        if old["card_id"] in {c for s in specs["claims"] for c in s["related"]}:
            cid = old["card_id"]
            put_json("frontier/cards/" + cid + ".json", old)
            original = (ROOT / old["card_path"]).read_bytes()
            previous_catalog = next(c for c in catalog["claims"] if c["id"] == cid)
            put(previous_catalog["pointers"]["card_web"], page(old["title"], original.decode(), cid,
                boundary=old.get("scientific_scope_status", BOUNDARY)))
            put("frontier/review_cards/" + cid + ".txt", ("CURRENT STATUS: " + json.dumps({"card_id": cid,
                "reported_claim_status": old["claim_status"], "material_updates": old["material_updates"],
                "status_path": "frontier/cards/" + cid + ".json"}, ensure_ascii=False, separators=(",", ":"))
                + "\nORIGINAL CARD (unchanged bytes after this line):\n").encode() + original)
    claims = merge(rows("indexes/claims.jsonl"), new_claims, "id")
    put_rows("indexes/claims.jsonl", claims)
    put_rows("frontier/CURRENT_CLAIM_STATUS.jsonl", merge(statuses, new_statuses, "card_id"))
    put_rows("indexes/source_metadata.jsonl", merge(rows("indexes/source_metadata.jsonl"), new_sources, "source_id"))
    put_rows("frontier/OPEN_PROOF_GATES.jsonl", merge(rows("frontier/OPEN_PROOF_GATES.jsonl"), new_gates, "gate_id"))
    put_rows("web/documents.jsonl", merge(rows("web/documents.jsonl"), new_docs, "id"))
    web_new = []
    for c, item in zip(new_claims, new_catalog):
        web_new.append({**c, "url": item["pointers"]["card_web"].removeprefix("web/"),
                        "text": outputs[c["path"]].decode(), "current_status": "../" + item["pointers"]["current_status"],
                        "reviewed_card": "../" + item["pointers"]["reviewed_card"]})
    put("web/catalog.json", (json.dumps(merge(read("web/catalog.json"), web_new, "id"), ensure_ascii=False, indent=2) + "\n").encode())
    put_json("indexes/query_aliases.json", aliases)
    catalog["claims"] = merge(catalog["claims"], new_catalog, "id")
    freshness = {"schema_version": catalog["schema_version"], "base_commit": specs["base_revision"],
                 "generator": "updates/BR/build_intake.py", "generator_sha256": sha(Path(__file__).read_bytes()),
                 "full_private_database_rebuild": "not performed; incremental public append only",
                 "inputs": {p: sha(outputs.get(p, (ROOT / p).read_bytes())) for p in ["indexes/claims.jsonl", "frontier/CURRENT_CLAIM_STATUS.jsonl", "web/catalog.json", "web/documents.jsonl", "updates/BR/CLAIMS.json"]},
                 "cards_manifest_sha256": sha("\n".join(c["id"] + " " + c["card_sha256"] for c in sorted(catalog["claims"], key=lambda c:c["id"])).encode())}
    catalog["freshness"] = freshness
    graph["freshness"] = freshness
    graph["nodes"] = sorted(nodes.values(), key=lambda n:n["id"])
    key = lambda e:(e["from"], e["to"], e["raw_kind"], e["source"])
    existing_keys = {key(e) for e in graph["edges"]}
    # Preserve even repeated historical graph records; append only absent new edges.
    graph["edges"] = sorted(graph["edges"] + [e for e in extra_edges if key(e) not in existing_keys], key=key)
    put_json("indexes/agent_catalog.json", catalog)
    put_json("indexes/agent_graph.json", graph)
    header = "id\ttopics\tstatus\ttitle\tcard_path\n"
    route = lambda c: "\t".join([c["id"], ",".join(c["topics"]), c["status"], c["title"], "frontier/review_cards/" + c["id"] + ".txt"]) + "\n"
    put("agent/routes.tsv", (header + "".join(route(c) for c in claims)).encode())
    topics = sorted({t for c in claims for t in c["topics"]})
    for topic in topics:
        selected_claims = [c for c in claims if topic in c["topics"]]
        put("agent/topics/" + topic + ".tsv", (header + "".join(route(c) for c in selected_claims)).encode())
        shard_path = ROOT / ("indexes/agent_topics/" + topic + ".json")
        shard = read("indexes/agent_topics/" + topic + ".json") if shard_path.is_file() else {
            "schema_version": "astra-agent-index-v1", "topic": topic, "freshness": {}, "claims": []}
        additions = [{"id": c["id"], "title": c["title"], "status": c["status"], "card_sha256": c["card_sha256"],
                      **{k:v for k,v in c["pointers"].items() if k in {"current_status", "card_local", "read_local", "card_web"}}}
                     for c in new_catalog if topic in c["topics"]]
        shard["claims"] = sorted(merge(shard["claims"], additions, "id"), key=lambda c:c["id"])
        shard["freshness"] = freshness
        put_json("indexes/agent_topics/" + topic + ".json", shard)
    topic_text = (ROOT / "agent/topics.txt").read_text()
    import re
    for t in topics:
        pattern = r"(" + re.escape(t) + r": agent/topics/[^\n]+ \()\d+( cards\))"
        updated, count = re.subn(pattern, lambda m:m[1] + str(sum(t in c["topics"] for c in claims)) + m[2], topic_text)
        if count:
            topic_text = updated
        else:
            topic_text += f"{t}: agent/topics/{t}.tsv ({sum(t in c['topics'] for c in claims)} cards)\n"
    put("agent/topics.txt", topic_text.encode())
    paths = sorted(p for p in outputs if p.startswith(("cards/", "frontier/cards/", "frontier/review_cards/")) and any(s["id"] in p for s in specs["claims"]))
    legacy = read("agent/manifest.json")
    for p in paths:
        legacy["hashes"][p] = sha(outputs[p])
    put_json("agent/manifest.json", legacy)
    return outputs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "check"])
    args = parser.parse_args()
    outputs = build()
    # build_access owns the evolving legacy manifest; compare BR-owned hash entries only.
    if args.command == "check":
        outputs.pop("agent/manifest.json")
        stale = [p for p,d in outputs.items() if not (ROOT / p).is_file() or (ROOT / p).read_bytes()!=d]
        if stale:
            raise SystemExit("Stale BR views: " + ", ".join(stale[:10]))
    else:
        for p,d in outputs.items():
            target = ROOT / p
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(d)
    print(json.dumps({"command": args.command, "generated_outputs": len(outputs),
                      "source_archive_members_checked": {"BR": 194, "BS": 97, "BU": 15, "BV": 18},
                      "attached_records_checked": 2,
                      "science_replayed": False, "private_database_rebuilt": False}))
