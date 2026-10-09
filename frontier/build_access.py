#!/usr/bin/env python3
"""Build/check bounded public agent views from existing records; no private DB or inference."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "astra.public-access.v1"
MAX_EXCERPT_BYTES = 32768
STOP = set("the and for with from into that this are can has have not only all any every under over which while where when its without through between does gives give using use source supplied known exact finite full stated same new old a an of to in on by as or is be at it no".split())
INPUTS = ["indexes/claims.jsonl", "indexes/agent_catalog.json", "indexes/agent_graph.json",
          "indexes/query_aliases.json", "indexes/blockers.json", "frontier/CURRENT_CLAIM_STATUS.jsonl",
          "frontier/OPEN_PROOF_GATES.jsonl", "literature/LEMMA_ATLAS.jsonl",
          "mechanisms/bridge_candidates.json", "agent/SEMANTIC_NOTICES.jsonl", "frontier/build_access.py",
          "frontier/retrieve.py", "00_START_HERE.txt", "AGENTS.md", "agent/README.txt",
          "agent/ACCESS.txt", "agent/COMPOSITION.txt", "agent/OPENAI_GUIDANCE.md", "UPDATE_PROTOCOL.txt"]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def jsonl(root, name):
    return [json.loads(line) for line in (root / name).read_text().splitlines() if line.strip()]


def unique(rows, key):
    result = {r[key]: r for r in rows}
    if len(result) != len(rows):
        raise ValueError("Duplicate identifiers in " + key)
    return result


def route_id(cid):
    """N/L numeric prefixes are stable; P/W historical IDs require their full names."""
    return cid.split("-", 1)[0] if re.match(r"^[NL]\d+(?:-|$)", cid) else cid


def local(root, path):
    target = (root / path).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("Reference outside repository: " + path)
    return target


def source_text(root, ref, inputs):
    """Never select an HTML block by position; select exact recorded bytes by hash."""
    for name in dict.fromkeys([ref["path"], ref.get("read_path", "")]):
        if not name:
            continue
        p = local(root, name)
        if not p.is_file():
            continue
        data = p.read_bytes()
        inputs[name] = digest(data)
        if digest(data) == ref["sha256"]:
            return data.decode("utf-8")
        if p.suffix == ".html":
            # Existing static edition escapes source text inside one or more pre blocks.
            for block in re.findall(r"<pre(?:\s[^>]*)?>(.*?)</pre>", data.decode("utf-8"), re.S):
                text = html.unescape(block)
                if digest(text.encode()) == ref["sha256"]:
                    return text
    raise ValueError("Recorded source hash cannot be recovered: " + ref["path"])


def evidence_refs(value):
    if isinstance(value, dict):
        if {"path", "sha256", "lines"} <= value.keys():
            yield value
        for child in value.values():
            yield from evidence_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from evidence_refs(child)


def compact_ref(ref):
    return {k: ref[k] for k in ("path", "sha256", "lines", "range_scope", "read_path", "source_id", "hash_kind", "original_sha256") if k in ref}


def build(root=ROOT, base_revision=None):
    inputs = {p: digest((root / p).read_bytes()) for p in INPUTS}
    claims_list = jsonl(root, "indexes/claims.jsonl")
    claims = unique(claims_list, "id")
    statuses = unique(jsonl(root, "frontier/CURRENT_CLAIM_STATUS.jsonl"), "card_id")
    catalog = unique(json.loads((root / "indexes/agent_catalog.json").read_text())["claims"], "id")
    if claims.keys() != statuses.keys() or claims.keys() != catalog.keys():
        raise ValueError("Claim/status/catalog coverage disagrees; refresh authoritative records")
    if len({route_id(cid) for cid in claims}) != len(claims):
        raise ValueError("Ambiguous stable route ID")
    ids = {route_id(cid): cid for cid in claims}
    def canonical(value):
        stem = Path(value).stem
        return value if value in claims else ids.get(stem, stem if stem in claims else None)
    outputs = {}
    issues = []
    graph = json.loads((root / "indexes/agent_graph.json").read_text())
    nodes = unique(graph["nodes"], "id")
    edges = defaultdict(list)
    for edge in graph["edges"]:
        if edge["from"] not in nodes or edge["to"] not in nodes:
            raise ValueError("Graph endpoint absent: " + str(edge))
        for cid in {edge["from"], edge["to"]} & claims.keys():
            edges[cid].append(edge)
    gates = unique(jsonl(root, "frontier/OPEN_PROOF_GATES.jsonl"), "gate_id")
    gate_by_card = defaultdict(list)
    for gid, gate in gates.items():
        outputs[f"frontier/gates/{gid}.json"] = encoded(gate)
        for reference in gate["card_ids"]:
            cid = canonical(reference)
            if cid is None:
                raise ValueError("Unknown gate card: " + reference)
            gate_by_card[cid].append(gate)
    lemmas = jsonl(root, "literature/LEMMA_ATLAS.jsonl")
    unique(lemmas, "id")
    lemma_by_card = defaultdict(list)
    for lemma in lemmas:
        path = "literature/lemmas/" + lemma["id"] + ".json"
        if not (root / path).is_file():
            raise ValueError("Missing lemma sidecar: " + lemma["id"])
        if json.loads((root / path).read_text()) != lemma:
            raise ValueError("Stale lemma sidecar: " + lemma["id"])
        inputs[path] = digest((root / path).read_bytes())
        for reference in lemma.get("claim_ids", []):
            cid = canonical(reference)
            if cid is not None:
                lemma_by_card[cid].append({"id": lemma["id"], "title": lemma["title"], "path": "literature/lemmas/" + lemma["id"] + ".json"})
    bridges = json.loads((root / "mechanisms/bridge_candidates.json").read_text())
    bridge_by_card = defaultdict(list)
    for bridge in bridges["bridges"] + bridges["rejected_transfers"]:
        outputs["mechanisms/bridges/" + bridge["id"] + ".json"] = encoded(bridge)
        for cid in bridge.get("cards", []):
            if cid not in claims:
                raise ValueError("Unknown bridge card: " + cid)
            bridge_by_card[cid].append({"id": bridge["id"], "status": bridge.get("status", bridges["status"]), "path": "mechanisms/bridges/" + bridge["id"] + ".json"})
    notices = jsonl(root, "agent/SEMANTIC_NOTICES.jsonl")
    unique(notices, "notice_id")
    notice_by_card = defaultdict(list)
    for notice in notices:
        for cid in notice["card_ids"]:
            if cid not in claims:
                raise ValueError("Unknown semantic-notice card: " + cid)
            notice_by_card[cid].append(notice)
    blockers = json.loads((root / "indexes/blockers.json").read_text())["blockers"]
    for blocker in blockers:
        outputs["frontier/blockers/" + blocker["id"] + ".json"] = encoded(blocker)
    outputs["frontier/gates/index.tsv"] = ("gate_id\ttitle\tresult_route_ids\tpath\n" + "\n".join(
        f"{gid}\t{g['title']}\t{','.join(route_id(canonical(c)) for c in g['card_ids'])}\tfrontier/gates/{gid}.json"
        for gid, g in sorted(gates.items())) + "\n").encode()
    outputs["frontier/blockers/index.tsv"] = ("blocker_id\ttrigger_terms\tpath\n" + "\n".join(
        f"{b['id']}\t{'; '.join(b['trigger_terms'])}\tfrontier/blockers/{b['id']}.json" for b in blockers) + "\n").encode()
    outputs["agent/OBSTRUCTIONS.txt"] = ("OBSTRUCTION ATLAS | optional routes over existing scoped records, not a new mathematical taxonomy\n"
        "Open frontier/gates/index.tsv for unresolved questions/pass conditions; frontier/blockers/index.tsv for failed transfers/interface limits.\n"
        "Fetch one exact gate/blocker JSON and the associated dossier before reasoning. Corrections in current status outrank historical blocker wording within their exact scope.\n"
        "These are curated, incomplete collections. Recurring words do not establish a shared obstruction or an impossibility theorem.\n"
        "Primitive Genesis may compare these failures or invent independently: agent/templates/PRIMITIVE_CANDIDATE.json. No indexed predecessor is required.\n").encode()

    # Check all referenced source blocks, once per exact byte version. Missing public
    # originals are expected; recoverable static text is sufficient for indexed hashes.
    source_cache = {}
    for ref in evidence_refs([list(statuses.values()), list(gates.values()), notices, bridges]):
        key = (ref["path"], ref["sha256"], ref.get("read_path"))
        if key not in source_cache:
            try:
                source_cache[key] = source_text(root, ref, inputs)
            except (ValueError, UnicodeError) as error:
                source_cache[key] = None
                issues.append({"path": ref["path"], "sha256": ref["sha256"], "read_path": ref.get("read_path"), "issue": str(error)})
        text = source_cache[key]
        a, b = ref["lines"]
        if text is not None and not 1 <= a <= b <= len(text.splitlines()):
            raise ValueError("Invalid recorded source line range: " + str(ref))

    windows = {}
    proof_routes = defaultdict(list)
    for cid, status in statuses.items():
        for ref in status["proof_availability"].get("located_proof_sources", []):
            entry = compact_ref(ref)
            key = (ref["path"], ref["sha256"], ref.get("read_path"))
            text = source_cache[key]
            if text is None:
                entry["access_issue"] = "Recorded source hash unavailable in public checkout; no excerpt generated"
            else:
                a, b = ref["lines"]
                excerpt = "".join(text.splitlines(keepends=True)[a - 1:b])
                if len(excerpt.encode()) <= MAX_EXCERPT_BYTES:
                    wid = digest(encoded({"path": ref["path"], "sha256": ref["sha256"], "lines": ref["lines"]}))[:24]
                    path = "frontier/proof_ranges/" + wid + ".txt"
                    header = ("EXACT INDEXED SOURCE RANGE | " + json.dumps(compact_ref(ref), ensure_ascii=False) + "\n"
                              + "range_sha256=" + digest(excerpt.encode()) + "; line numbers refer to the source, not this wrapper.\n"
                              + "Scope: located text only; imported premises, completeness, correctness and priority remain unverified.\n"
                              + "--- BEGIN SOURCE BYTES ---\n")
                    outputs[path] = header.encode() + excerpt.encode()
                    windows[path] = {"source": compact_ref(ref), "range_sha256": digest(excerpt.encode())}
                    entry["exact_range_path"] = path
                else:
                    entry["access_note"] = "Range exceeds 32 KiB; fetch complete source once at the recorded locator"
            proof_routes[cid].append(entry)

    # The input fingerprint includes recovered source pages and raw cards. It pins
    # working-tree inputs, without pretending the output can embed its own Git SHA.
    card_texts = {}
    for cid, claim in claims.items():
        status = statuses[cid]
        data = (root / claim["path"]).read_bytes()
        if digest(data) != status["card_sha256"] or digest(data) != catalog[cid]["card_sha256"]:
            raise ValueError("Card/status/catalog hash disagreement: " + cid)
        inputs[claim["path"]] = digest(data)
        for path in ["frontier/cards/" + cid + ".json", "frontier/review_cards/" + cid + ".txt"]:
            if not (root / path).is_file():
                raise ValueError("Missing legacy reviewed route: " + path)
            inputs[path] = digest((root / path).read_bytes())
        if not (root / ("frontier/review_cards/" + cid + ".txt")).read_bytes().endswith(data):
            raise ValueError("Legacy reviewed wrapper changed historical card bytes: " + cid)
        if json.loads((root / ("frontier/cards/" + cid + ".json")).read_text()) != status:
            raise ValueError("Stale status sidecar: " + cid)
        card_texts[cid] = data.decode()
    fingerprint = digest(encoded(inputs))
    snapshot = {"base_revision": base_revision, "input_sha256": fingerprint}
    for cid, claim in claims.items():
        rid = route_id(cid)
        status = statuses[cid]
        own_edges = sorted(edges[cid], key=lambda e: (e["from"], e["to"], e["raw_kind"]))
        endpoint_ids = {n for e in own_edges for n in (e["from"], e["to"])}
        connections = {"schema": SCHEMA, "snapshot": snapshot, "card_id": cid,
                       "policy": "Existing typed graph projection; raw kinds retained. No edge is promoted to a proved implication or compatible interface.",
                       "edges": own_edges, "nodes": [nodes[n] for n in sorted(endpoint_ids)],
                       "scoped_relations": {k: status[k] for k in ("depends_on", "supersedes", "invalidates", "material_updates", "requires_external_validation", "relation_coverage")},
                       "bridges": bridge_by_card[cid], "lemmas": lemma_by_card[cid]}
        outputs[f"frontier/connections/{rid}.json"] = encoded(connections)
        lines = [f"ASTRA RESULT DOSSIER | {cid}", f"snapshot_input_sha256={fingerprint}; base_revision={base_revision}",
                 "Current scoped records + historical card. Navigation/availability does not certify mathematics.",
                 f"claim_status={status['claim_status']}; proof_availability={status['proof_availability']['classification']}",
                 "availability_scope=" + status['proof_availability'].get('classification_scope', 'UNKNOWN'),
                 "scientific_scope_status=" + str(status.get('scientific_scope_status', 'See exact scoped status record; no inferred upgrade')),
                 "Exact full status: frontier/cards/" + cid + ".json", "\nMATERIAL UPDATES (complete recorded scopes)"]
        for update in status["material_updates"]:
            lines.append(json.dumps(update, ensure_ascii=False, separators=(",", ":")))
        if not status["material_updates"]:
            lines.append("None recorded; curated coverage is not an exhaustive absence claim.")
        alerts = []
        for dep in status["depends_on"]:
            target = dep.get("target") if isinstance(dep, dict) else dep
            dependent = canonical(target) if isinstance(target, str) else None
            if dependent is not None and statuses[dependent]["material_updates"]:
                alerts.append({"dependency": dependent, "dependency_scope": dep.get("scope", "UNKNOWN") if isinstance(dep, dict) else "UNKNOWN", "updates": statuses[dependent]["material_updates"]})
        if alerts:
            lines += ["\nDIRECT DEPENDENCY NOTICES (no automatic whole-claim invalidation)"] + [json.dumps(a, ensure_ascii=False, separators=(",", ":")) for a in alerts]
        for notice in notice_by_card[cid]:
            lines += ["\nSEMANTIC NOTICE " + notice["notice_id"], notice["status"] + ": " + notice["clarification"]]
        text = card_texts[cid]
        for notice in notice_by_card[cid]:
            if notice.get("display_replacements"):
                if not any(r["path"] == claim["path"] and r["sha256"] == digest(text.encode()) for r in notice["source_refs"]):
                    raise ValueError("Display normalization source hash changed: " + cid)
                for replacement in notice["display_replacements"]:
                    if text.count(replacement["before"]) != replacement["expected_occurrences"]:
                        raise ValueError("Display normalization occurrence count changed: " + cid)
                    text = text.replace(replacement["before"], replacement["after"])
                if digest(text.encode()) != notice["normalized_source_sha256"]:
                    raise ValueError("Display normalization result changed: " + cid)
        lines += ["\nTASK-RELEVANT OPEN GATES"]
        for gate in gate_by_card[cid]:
            lines += [f"{gate['gate_id']} | {gate['status']} | frontier/gates/{gate['gate_id']}.json", "Question: " + gate["question"], "Pass: " + gate["pass_condition"]]
        if not gate_by_card[cid]:
            lines.append("None associated in the curated gate ledger; this does not close unstated obligations.")
        lines += ["\nCONTRAST / COMPOSITION ROUTES (read before applying the historical card)"]
        lines += [json.dumps(b, ensure_ascii=False, separators=(",", ":")) for b in status["contrasting_blockers"]]
        lines += [json.dumps(b, ensure_ascii=False, separators=(",", ":")) for b in bridge_by_card[cid] + lemma_by_card[cid]]
        lines.append(f"Exact incident graph + scoped relations: frontier/connections/{rid}.json; composition protocol: agent/COMPOSITION.txt")
        lines += [f"\nCARD | raw={claim['path']} | raw_sha256={status['card_sha256']}",
                  "Source-preserving display normalization applies only where explicitly noticed above.", text.rstrip("\n")]
        lines += ["\nPROOF RECONSTRUCTION ROUTES | preserve inclusive source line numbers"]
        for ref in proof_routes[cid]:
            lines.append(json.dumps(ref, ensure_ascii=False, separators=(",", ":")))
        if not proof_routes[cid]:
            lines.append("No specifically located proof range classified; source inventory below is not a completeness claim.")
        for ref in status["proof_availability"].get("available_evidence_sources", []):
            if not any(p["path"] == ref["path"] for p in proof_routes[cid]):
                lines.append(json.dumps(compact_ref(ref), ensure_ascii=False, separators=(",", ":")))
        outputs[f"frontier/dossiers/{rid}.txt"] = ("\n".join(lines) + "\n").encode()

    aliases = json.loads((root / "indexes/query_aliases.json").read_text())
    concepts = defaultdict(set)
    for cid, claim in claims.items():
        for term in set(re.findall(r"[a-z][a-z0-9_]{2,}", (claim["title"] + " " + aliases.get(cid, "")).lower())) - STOP:
            concepts[term].add(route_id(cid))
    alphabet = defaultdict(list)
    for term, ids in sorted(concepts.items()):
        alphabet[term[0]].append(term + "\t" + ",".join(sorted(ids)))
    router = ["LEXICAL CONCEPT ROUTER | titles + existing aliases; navigation only, no inferred applicability.",
              "Choose the initial letter of a task word. Read its row, then frontier/dossiers/<route-ID>.txt.",
              "N/L use numeric IDs (N533, L01); P/W use full historical IDs. Try synonyms or agent/topics.txt when needed.",
              "Non-ASCII concepts may need an English alias; unindexed primitives need no existing route.", "initial\tpath\tbytes\tterms"]
    for initial, rows in sorted(alphabet.items()):
        path = f"agent/concepts/{initial}.tsv"
        data = ("term\tresult_route_ids\n" + "\n".join(rows) + "\n").encode()
        outputs[path] = data
        router.append(f"{initial}\t{path}\t{len(data)}\t{len(rows)}")
    outputs["agent/concepts.txt"] = ("\n".join(router) + "\n").encode()
    outputs["agent/RECENT.tsv"] = ("# Last 40 claim-ledger entries in recorded order; intake sequence is not scientific authority.\nroute_id\tcard_id\ttitle\tstatus\tdossier\n" + "\n".join(f"{route_id(c['id'])}\t{c['id']}\t{c['title']}\t{c['status']}\tfrontier/dossiers/{route_id(c['id'])}.txt" for c in claims_list[-40:]) + "\n").encode()
    counts = {"cards": len(claims), "gates": len(gates), "lemmas": len(lemmas), "graph_nodes": len(nodes), "graph_edges": len(graph["edges"]), "proof_ranges": len(windows), "source_access_issues": len(issues)}
    outputs["agent/CURRENT.txt"] = ("CURRENT PUBLIC RECORD INVENTORY | generated, not a research assessment\n" + json.dumps(counts, sort_keys=True) + "\nbase_revision=" + str(base_revision) + "; input_sha256=" + fingerprint + "\nPin the Git revision actually fetched. base_revision is the audited input ancestor, not a claim that all generated files existed there.\nAuthority: exact source bytes for mathematics; claim ledger + scoped frontier notices for status; checkpoint heads for published activity; generated views for access. Old reports/receipts apply only to their recorded scope.\nFreshness: frontier/build_access.py check checks current input/output hashes and regeneration.\n").encode()
    # Retain the legacy manifest interface/coverage, refreshing its existing hash
    # entries. New coverage is separately pinned below; avoid recursive manifests.
    legacy = json.loads((root / "agent/manifest.json").read_text())
    for path in legacy["hashes"]:
        if path in outputs:
            legacy["hashes"][path] = digest(outputs[path])
        elif (root / path).is_file():
            legacy["hashes"][path] = digest((root / path).read_bytes())
        else:
            raise ValueError("Legacy manifest route disappeared: " + path)
    legacy.setdefault("historical_bootstrap_o200k_tokens", legacy.get("bootstrap_o200k_tokens"))
    legacy["bootstrap_o200k_tokens"] = None
    legacy["bootstrap_bytes"] = len((root / "00_START_HERE.txt").read_bytes())
    legacy["tokenizer"] = "Current token count unmeasured; historical o200k estimate retained separately"
    legacy["claims"] = len(claims)
    legacy["public_access"] = {"manifest": "agent/access_manifest.json", "snapshot": snapshot,
                               "scope": "Current public projection; earlier incremental receipts retain historical scope"}
    outputs["agent/manifest.json"] = encoded(legacy)
    manifest = {"schema": SCHEMA, "snapshot": snapshot, "counts": counts, "inputs": inputs,
                "outputs": {p: digest(b) for p, b in sorted(outputs.items())}, "proof_ranges": windows,
                "source_access_issues": issues,
                "boundary": "Deterministic structure only. No inference, scientific investigation, performance claim, or claim-status upgrade."}
    outputs["agent/access_manifest.json"] = encoded(manifest)
    return outputs, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "check"])
    parser.add_argument("--base-revision")
    args = parser.parse_args()
    manifest_path = ROOT / "agent/access_manifest.json"
    base = args.base_revision
    if base is None and manifest_path.exists():
        base = json.loads(manifest_path.read_text())["snapshot"]["base_revision"]
    if base is None:
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    subprocess.run(["git", "cat-file", "-e", base + "^{commit}"], cwd=ROOT, check=True, capture_output=True)
    outputs, manifest = build(base_revision=base)
    if args.command == "build":
        if manifest_path.exists():
            old = json.loads(manifest_path.read_text())
            removed = set(old["outputs"]) - outputs.keys()
            if removed:
                raise ValueError("Generated routes would disappear; provide explicit migration: " + str(sorted(removed)))
        for path, data in outputs.items():
            p = ROOT / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
    else:
        stale = [p for p, data in outputs.items() if not (ROOT / p).is_file() or (ROOT / p).read_bytes() != data]
        if stale:
            raise ValueError("Missing/stale generated views: " + ", ".join(stale[:8]))
    print(json.dumps({"command": args.command, "counts": manifest["counts"], "input_sha256": manifest["snapshot"]["input_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
