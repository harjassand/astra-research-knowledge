#!/usr/bin/env python3
"""Append frozen FT2 records while retaining existing JSONL rows byte-for-byte."""
from __future__ import annotations
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
UPDATE = ROOT / "updates/FT-foundational-capability-v2-20261015"
PACKAGE = UPDATE / "package"
BASE = "0c789ca775808e23e57138b56a393ad1e58cb15c"
STARTING_REVISION = "03b51f364080972740e2207aa2c3e1fa803c08eb"
EXPECTED_MANIFEST = "c291512b7c7491a9b93e7048188dc6b4407518cc168f9949e081926fa9a1734a"
CARD_IDS = [
    "N853-laplace-positivity-convolution-and-dependent-kernel",
    "N854-scalar-control-response-acquisition-and-weak-anchor-boundary",
    "N855-radial-pauli-compiler-and-exact-projection-variance-cost",
    "N856-isotope-sequence-and-gated-graphene-qualification-boundaries",
]
BOUNDARY = ("Source-derived claims and internal reviews remain externally unreviewed. External mathematical "
            "correctness and historical priority are UNKNOWN. Physical capability and complete-resource "
            "advantage are not established. Indexing, hashes and access checks establish only their recorded "
            "integrity scope.")

def sha(data): return hashlib.sha256(data).hexdigest()
def enc(value): return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
def load(path): return json.loads(path.read_text(encoding="utf-8"))
def refs(value):
    out = []
    if isinstance(value, dict):
        if {"path", "sha256", "lines"} <= value.keys(): out.append(value)
        for child in value.values(): out.extend(refs(child))
    elif isinstance(value, list):
        for child in value: out.extend(refs(child))
    return out

def head_bytes(rel):
    return subprocess.run(["git", "show", "HEAD:" + rel], cwd=ROOT, check=True, capture_output=True).stdout

def append_jsonl(path, rows, key):
    rel = path.relative_to(ROOT).as_posix()
    base = head_bytes(rel)
    old = path.read_bytes()
    if not old.startswith(base):
        raise ValueError("Tracked JSONL baseline bytes changed before append: " + rel)
    if old and not old.endswith(b"\n"):
        raise ValueError("JSONL missing terminal newline: " + rel)
    existing = [json.loads(line) for line in old.decode().splitlines() if line.strip()]
    by_key = {item[key]: item for item in existing if key in item}
    additions = []
    for row in rows:
        ident = row[key]
        if ident in by_key:
            if by_key[ident] != row: raise ValueError("JSONL ID collision: " + str(ident))
        else:
            additions.append(row)
            by_key[ident] = row
    if additions:
        path.write_bytes(old + b"".join(
            (json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
            for row in additions
        ))

def array_bounds(text, target):
    decoder = json.JSONDecoder()
    i = 0
    while text[i].isspace(): i += 1
    if text[i] != "{": raise ValueError("Expected JSON object")
    i += 1
    while i < len(text):
        while i < len(text) and (text[i].isspace() or text[i] == ","): i += 1
        if text[i] == "}": break
        key, i = decoder.raw_decode(text, i)
        while text[i].isspace(): i += 1
        if text[i] != ":": raise ValueError("Malformed JSON")
        i += 1
        while text[i].isspace(): i += 1
        value_start = i
        _, value_end = decoder.raw_decode(text, i)
        if key == target:
            if text[value_start] != "[": raise ValueError("Expected array for " + target)
            depth = 0
            quoted = escaped = False
            for j in range(value_start, value_end):
                ch = text[j]
                if quoted:
                    if escaped: escaped = False
                    elif ch == "\\": escaped = True
                    elif ch == '"': quoted = False
                elif ch == '"': quoted = True
                elif ch == "[": depth += 1
                elif ch == "]":
                    depth -= 1
                    if depth == 0: return value_start, j
            raise ValueError("Unclosed JSON array: " + target)
        i = value_end
    raise KeyError("Missing top-level array " + target)

def append_array(path, target, additions, key):
    raw = path.read_bytes()
    current = json.loads(raw)[target]
    seen = {key(item): item for item in current}
    new = []
    for item in additions:
        ident = key(item)
        if ident in seen:
            if seen[ident] != item: raise ValueError("JSON array ID collision: " + str(ident))
        else:
            new.append(item)
            seen[ident] = item
    if not new: return
    text = raw.decode("utf-8")
    start, end = array_bounds(text, target)
    body = text[start + 1:end].rstrip()
    encoded_items = []
    for item in new:
        encoded_items.append("\n".join("    " + line for line in
                             json.dumps(item, ensure_ascii=False, indent=2).splitlines()))
    updated = body + ("," if body else "") + "\n" + ",\n".join(encoded_items) + "\n  "
    path.write_bytes((text[:start + 1] + updated + text[end:]).encode("utf-8"))

# Verify the exact frozen source package before making records that cite it.
manifest_bytes = (PACKAGE / "SOURCE_MANIFEST.json").read_bytes()
if sha(manifest_bytes) != EXPECTED_MANIFEST: raise ValueError("Frozen FT2 manifest SHA mismatch")
sm = json.loads(manifest_bytes)
if sm["file_count"] != 56 or sm["bytes"] != 363107: raise ValueError("Frozen manifest count/bytes mismatch")
expected_files = {"SOURCE_MANIFEST.json"} | {item["path"] for item in sm["files"]}
actual_files = {p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob("*") if p.is_file()}
if expected_files != actual_files: raise ValueError("Frozen package file set mismatch")
for item in sm["files"]:
    data = (PACKAGE / item["path"]).read_bytes()
    if len(data) != item["bytes"] or sha(data) != item["sha256"]:
        raise ValueError("Frozen file bytes/hash mismatch: " + item["path"])

manifest_rows = [{
    "source_path": item["path"],
    "preserved_path": "updates/FT-foundational-capability-v2-20261015/package/" + item["path"],
    "bytes": item["bytes"], "sha256": item["sha256"],
    "provenance": "Exact bytes from the frozen authored FT2 manifest; source status retained."
} for item in sm["files"]]
manifest_rows.append({
    "source_path": "SOURCE_MANIFEST.json",
    "preserved_path": "updates/FT-foundational-capability-v2-20261015/package/SOURCE_MANIFEST.json",
    "bytes": len(manifest_bytes), "sha256": EXPECTED_MANIFEST,
    "provenance": "Exact frozen source manifest retained as the 57th copied item."
})
(UPDATE / "SOURCE_MANIFEST.json").write_bytes(enc({
    "schema": "astra.capital-preservation-source-manifest.v1", "intake_id": "FT2",
    "source_handling": "source=DATA; exact frozen bytes retained",
    "campaign_source_root": "/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-foundational-capability-v2",
    "campaign_manifest_source_path": "research/2026-10-15-foundational-capability-v2/SOURCE_MANIFEST.json",
    "campaign_manifest_sha256": EXPECTED_MANIFEST, "declared_file_count": 56,
    "declared_bytes": 363107, "copied_item_count": 57,
    "observed_freeze_clock_utc": sm["observed_freeze_clock_utc"],
    "files": manifest_rows,
    "exclusions": "No unlisted files, raw third-party papers/data/images, caches, or __pycache__ were copied."
}))

statuses = {}
source_by_id = {}
claims = []
catalog = []
graph_nodes = []
graph_edges = []
gates = []
for cid in CARD_IDS:
    status = load(ROOT / "frontier/cards" / (cid + ".json"))
    if status["card_id"] != cid or status["claim_status"] != "source_derived_unreviewed":
        raise ValueError("Unexpected sidecar identity/status: " + cid)
    raw_card = (ROOT / status["card_path"]).read_bytes()
    if sha(raw_card) != status["card_sha256"]: raise ValueError("Card hash mismatch: " + cid)
    wrapper = (ROOT / "frontier/review_cards" / (cid + ".txt")).read_bytes()
    if not wrapper.endswith(raw_card): raise ValueError("Review wrapper raw bytes mismatch: " + cid)
    statuses[cid] = status
    by_id = {}
    for ref in refs(status):
        if not ref.get("source_id"): continue
        sid = ref["source_id"]
        if sid in by_id and (by_id[sid]["path"], by_id[sid]["sha256"]) != (ref["path"], ref["sha256"]):
            raise ValueError("Conflicting paths for source ID " + sid)
        by_id[sid] = ref
    source_by_id.update(by_id)
    source_paths = list(dict.fromkeys(ref["path"] for ref in by_id.values()))
    source_ids = list(by_id)
    deps = status.get("depends_on", [])
    scoped_deps = status.get("scoped_dependencies", [])
    claims.append({
        "id": cid, "title": status["title"], "path": status["card_path"],
        "topics": status["topics"], "status": status["claim_status"],
        "source_ids": source_ids, "source_paths": source_paths,
        "depends_on": deps, "scoped_dependencies": scoped_deps,
        "tokens": None, "token_count_status": "not_measured",
        "record_type": "source_and_integration_derived_scoped_result"
    })
    n = cid[1:4]
    cap = load(ROOT / ("frontier/gates/G-FT-N" + n + "-CAPABILITY.json"))
    catalog.append({
        "id": cid, "title": status["title"], "topics": status["topics"],
        "status": status["claim_status"], "card_sha256": status["card_sha256"],
        "dependencies": {"depends_on": deps, "scoped_dependencies": scoped_deps},
        "pointers": {"card_local": status["card_path"], "card_web": "frontier/dossiers/N" + n + ".txt",
                     "current_status": "frontier/cards/" + cid + ".json",
                     "reviewed_card": "frontier/review_cards/" + cid + ".txt",
                     "read_local": "python3 frontier/retrieve.py dossier N" + n,
                     "read_web": ["frontier/dossiers/N" + n + ".txt", source_paths[0],
                                  "frontier/connections/N" + n + ".json"]},
        "quoted_fields": {"status": [status["reported_status"].splitlines()[0]],
                          "interface": [status["scientific_scope_status"]],
                          "limits": [cap["question"]]}
    })
    graph_nodes.append({"id": cid, "node_kind": "claim"})
    for sid in source_ids:
        graph_nodes.append({"id": sid, "node_kind": "source"})
        graph_edges.append({"from": cid, "to": sid, "kind": "provenance",
                            "raw_kind": "source_or_internal_evidence", "source": "FT2",
                            "composition": BOUNDARY})
    for kind in ("REVIEW", "CAPABILITY"):
        gate_id = "G-FT-N" + n + "-" + kind
        gate = load(ROOT / ("frontier/gates/" + gate_id + ".json"))
        if gate["status"] != "open" or gate["completion_evidence"]:
            raise ValueError("New gate is not open: " + gate_id)
        gates.append(gate)

metadata_rows = []
for sid, ref in source_by_id.items():
    data = (ROOT / ref["path"]).read_bytes()
    if sha(data) != ref["sha256"]: raise ValueError("Referenced source hash mismatch: " + ref["path"])
    metadata_rows.append({
        "source_id": sid, "path": ref["path"],
        "title": pathlib.Path(ref["path"]).name + " [FT2 frozen source]",
        "sha256": sha(data), "bytes": len(data),
        "date_version": "2026-10-15 / FT2 frozen source",
        "read_depth": "Whole authored source file preserved for a scoped FT2 intake; no external completeness or correctness implied.",
        "reported_verification": BOUNDARY, "extraction": "original_utf8_bytes"
    })

notice_data = [
    ("N853", "Cone and tail-class qualifications belong to the exact theorem scope.",
     "The cone is C strictly contained in E, closed and convex with nonempty interior; pointedness is not required. The deep r log r tail-class separation is carried by the producer proof/root reconstruction, not the independent consequence report."),
    ("N854", "Scalar response acquisition does not establish an exponential query lower bound.",
     "The theorem is scalar-only under calibrated independent additive rank-one controls, a fixed source/detector and stable repeated reference. The weak-anchor example is an exact robustness boundary under its stated conditions."),
    ("N855", "The exact compiler is Blackwell dominated for state inference by the covariant spin incumbent.",
     "The supplied ideal radial POVM law is classical postprocessing of the covariant spin POVM. The gamma-only covariance gap and nonoptimal exact-all-t variance lower bound are separate statements; finite sampler precision/calibration remain open."),
    ("N856", "Prior gated-graphene experiments are device-specific precedent, not validation of proposed isotope or hBN routes.",
     "The isotope purge ratio assumes positive D-loss; zero-D-loss with H escape is its infinite-ratio limit. Published graphene active-control results are credited precedents in their own devices and establish no hBN, battery or isotope transfer.")
]
notices = []
for n, issue, clarification in notice_data:
    cid = next(cid for cid in CARD_IDS if cid.startswith(n + "-"))
    ev = next(ref for ref in refs(statuses[cid]["proof_availability"]) if ref.get("source_id"))
    notices.append({
        "notice_id": "SN-FT2-" + n + "-SCOPE", "card_ids": [cid],
        "issue": issue, "status": "source_derived_scoped_boundary",
        "clarification": clarification,
        "material_updates": [{"target": cid, "scope": clarification,
                              "relation_status": "Scoped source-derived boundary; evidence and open gates retained."}],
        "source_refs": [ev], "source_revision": BASE, "whole_claim_invalidated": False
    })

# This is a comparison only; no N712 Gibbs/Fisher theorem or status is transferred.
n855 = statuses[CARD_IDS[2]]
n712 = load(ROOT / "frontier/cards/N712-local-readout-thermal-information-loss-and-variance-certificate.json")
n855_ref = next(ref for ref in refs(n855["proof_availability"])
                if ref["path"].endswith("root/PAULI_OPERATION_AND_VARIANCE.md"))
n712_ref = next(ref for ref in refs(n712["proof_availability"]) if ref.get("source_id"))
bridge = {
    "id": "FT2_radial_pauli_to_N712_protocol_comparison",
    "status": "CANDIDATE CONNECTION", "kind": "scoped_comparison",
    "cards": [CARD_IDS[2], n712["card_id"]],
    "alignment": "Both concern Pauli measurement protocols. N855's supplied radial POVM law is classical postprocessing of a covariant spin POVM; N712's Gibbs local-readout Fisher theorem has a distinct Hamiltonian, detector and preparation contract. No theorem transfer is claimed.",
    "assumptions": [
        "N855's statistical-domination claim is limited to its exact ideal compiler and state-inference experiment.",
        "N712 retains its own full-rank Gibbs, independent detector calibration and acquisition assumptions.",
        "Neither result's status, variance bound or capability conclusion is promoted by this comparison."
    ],
    "acquisition": "No task input is acquired by the bridge. Gibbs-copy preparation, calibration and measurement costs for N712 remain distinct from N855's supplied tuple and output processing.",
    "cost": "A matched comparison must charge preparation, calibration, sampling variance, compiler precision and measurement/readout resources under a common task contract.",
    "falsifier": "A scope-matched review refuting the claimed classical randomized postprocessing relation or correcting the distinct N712 experiment contract.",
    "evidence": [n855_ref, n712_ref]
}
bridges = [bridge]

append_jsonl(ROOT / "indexes/claims.jsonl", claims, "id")
append_jsonl(ROOT / "frontier/CURRENT_CLAIM_STATUS.jsonl", [statuses[c] for c in CARD_IDS], "card_id")
append_jsonl(ROOT / "frontier/OPEN_PROOF_GATES.jsonl", gates, "gate_id")
append_jsonl(ROOT / "agent/SEMANTIC_NOTICES.jsonl", notices, "notice_id")
append_jsonl(ROOT / "indexes/source_metadata.jsonl", metadata_rows, "source_id")

append_array(ROOT / "indexes/agent_catalog.json", "claims", catalog, lambda x: x["id"])
append_array(ROOT / "indexes/agent_graph.json", "nodes", graph_nodes, lambda x: x["id"])
append_array(ROOT / "indexes/agent_graph.json", "edges",
             graph_edges, lambda x: (x["from"], x["to"], x["kind"], x["raw_kind"], x.get("source")))
append_array(ROOT / "mechanisms/bridge_candidates.json", "bridges", bridges, lambda x: x["id"])
bridge_file = ROOT / ("mechanisms/bridges/" + bridge["id"] + ".json")
bridge_file.parent.mkdir(parents=True, exist_ok=True)
bridge_file.write_bytes(enc(bridge))

(UPDATE / "CLAIMS.json").write_bytes(enc({
    "schema": "astra.intake-claim-map.v1", "intake_id": "FT2",
    "starting_revision": STARTING_REVISION, "base_revision": BASE,
    "mission_status": "NOT_ACHIEVED",
    "claims": [{"id": row["id"], "source_ids": row["source_ids"], "source_paths": row["source_paths"],
                "status": row["status"], "external_correctness": "UNKNOWN",
                "historical_priority": "UNKNOWN", "mission_status": "NOT_ACHIEVED"} for row in claims]
}))
(UPDATE / "OPEN_GATES.json").write_bytes(enc({"schema": "astra.ft2-open-gates.v1", "intake_id": "FT2", "gates": gates}))
(UPDATE / "SCOPED_NOTICES.json").write_bytes(enc({"schema": "astra.scoped-notices.v1", "intake_id": "FT2", "notices": notices,
                                                    "boundary": BOUNDARY}))
(UPDATE / "BRIDGES.json").write_bytes(enc({
    "schema": "astra.scoped-bridge-set.v1", "intake_id": "FT2",
    "status": "CANDIDATE CONNECTION; NO IMPLICATION OR STATUS PROMOTION", "bridges": bridges
}))

(UPDATE / "INTEGRATION_PLAN.md").write_text(
    "# FT2 Capital integration plan\n\n"
    "The frozen 2026-10-15 foundational-capability-v2 package is copied byte-identically from 56 manifest entries "
    "(363107 listed bytes) plus the manifest. Manifest SHA-256: " + EXPECTED_MANIFEST +
    "; observed freeze: " + sm["observed_freeze_clock_utc"] + ".\n\n"
    "Target branch codex/astra-foundational-capability-v2-20261015 is based at " + BASE +
    " after starting from " + STARTING_REVISION + " and rebasing onto current main. Four records N853–N856, "
    "eight open gates, four scope notices and one N855-to-N712 comparison are appended. Existing FT/v1 content "
    "and checkpoint history remain untouched.\n\n"
    "All four records remain source_derived_unreviewed; external correctness and historical priority are UNKNOWN; "
    "mission status is NOT_ACHIEVED. Root owns the checkpoint draft, final receipts/derived manifest, final "
    "validation, commit, push and pull request.\n", encoding="utf-8")
(UPDATE / "SYNTHESIS.md").write_text(
    "# Foundational capability v2: scoped Capital synthesis\n\n"
    "**Mission status: NOT_ACHIEVED.** N853–N856 remain source_derived_unreviewed. External correctness and "
    "priority are UNKNOWN; no physical capability or complete-resource advantage is established. The frozen "
    "campaign report preserves full detail; this file records Capital-facing boundaries.\n\n"
    "N853 records a Laplace-positivity/convolution criterion for a closed convex cone C strictly contained in E "
    "with nonempty interior; pointedness is not required. It includes an adaptive radial strictly log-concave "
    "kernel with all exponential moments and no prescribed exponential margin, plus a separate r log r "
    "tail-class counterexample. Only the producer proof/root reconstruction carries that deep tail-class "
    "separation. The scalar PDE construction has a global lower bound above 0.183p; product/Gaussian routes fail "
    "in the recorded scope. Diamond–Essén novelty remains open.\n\n"
    "N854 records scalar-only exact acquisition of a fixed response map under calibrated independent additive "
    "rank-one controls, fixed source/detector and stable repeated reference. The weak-anchor indistinguishability "
    "result is a scoped robustness failure, not an exponential query lower bound.\n\n"
    "N855 preserves the exact ideal radial Pauli compiler and its decisive limit: the output law is classical "
    "postprocessing of an existing covariant spin POVM and is Blackwell dominated for state inference. The "
    "gamma-only covariance comparison and nonoptimal exact-all-t variance lower bound are separate statements. "
    "Finite precision/calibration remain open. Its N712 bridge is a protocol comparison only and transfers no "
    "Gibbs/Fisher theorem.\n\n"
    "N856 separates a conditional, unqualified isotope sequence from published gated-graphene active-control "
    "precedents. The purge ratio assumes positive D-loss; zero-D-loss with H escape is its infinite-ratio limit. "
    "The published experiments apply to their own device settings and establish no hBN, battery or isotope "
    "transfer.\n\nAll eight review and capability gates remain open. Provenance and generated access provide "
    "evidence routes only; they do not close scientific or physical obligations.\n", encoding="utf-8")
(UPDATE / "RESEARCH_HANDOFF.md").write_text(
    "# FT2 research handoff\n\n"
    "All four Capital records remain source_derived_unreviewed, all eight gates remain open, and mission status "
    "is NOT_ACHIEVED. Root owns checkpoint drafting and publication flow.\n\n"
    "Obtain independent proof and prior-art review for N853 and N854 at their exact scopes. N853's cone condition "
    "is closed, convex, nonempty-interior C strictly contained in E; pointedness is not required. Preserve that "
    "the deep r log r tail-class separation is carried by the producer proof/root reconstruction, not the "
    "independent consequence report. N854 is scalar-only and does not supply an exponential query lower bound.\n\n"
    "For N855, review the exact compiler and Blackwell-domination argument with the separate variance quantifiers; "
    "do not claim information gain over the covariant incumbent. Its N712 relation is a scoped protocol comparison.\n\n"
    "For N856, keep published graphene experiments as attributed prior evidence in their own device settings. "
    "The isotope purge ratio assumes positive D-loss and the proposed route remains physically unqualified. "
    "No result transfers to hBN, batteries or a demonstrated isotope capability.\n", encoding="utf-8")

print(json.dumps({
    "status": "GENERATED", "cards": CARD_IDS, "open_gates": len(gates),
    "notices": len(notices), "bridges": [bridge["id"]],
    "source_manifest_sha256": EXPECTED_MANIFEST, "source_files": 56,
    "source_bytes": 363107, "copied_items_with_manifest": 57,
    "base_revision": BASE, "old_jsonl_rows_byte_preserved": True
}, indent=2))
