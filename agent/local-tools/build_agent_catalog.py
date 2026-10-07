#!/usr/bin/env python3
"""Build compact, deterministic agent-facing catalog and typed graph snapshots."""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "indexes"
CARDS = ROOT / "cards"
SCHEMA_VERSION = "astra-agent-index-v1"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def quoted_fields(card_text: str) -> dict[str, list[str] | str]:
    """Collect only literal labeled lines; no contract inference or synthesis."""
    labels = {
        "interface": {"interface", "shared spin interface where applicable", "axis-queryobservationcontract"},
        "failure": {"failure", "failures", "counterexample", "counterexamples", "failed transfer", "mismatch"},
    }
    found: dict[str, list[str]] = {key: [] for key in labels}
    for line in card_text.splitlines():
        m = re.match(r"^\s*([^:]{1,80}):\s*(.*)$", line)
        if not m:
            continue
        raw_label, content = m.group(1).strip().lower(), m.group(2).strip()
        for field, accepted in labels.items():
            if raw_label in accepted:
                # Preserve the full labeled line exactly as it appears in the card.
                found[field].append(line)
                break
    return {k: (v if v else "UNKNOWN") for k, v in found.items()}


def relation_kind(raw_kind: str) -> tuple[str, str]:
    """Return safe graph class and composition policy; raw relation is retained."""
    if raw_kind == "supported_by":
        return "provenance", "never_proof_by_itself"
    if raw_kind == "links_to_not_logical_dependency":
        return "navigation", "forbidden"
    if raw_kind == "requires" or raw_kind.startswith("requires_") or raw_kind.startswith("requires_for_"):
        return "explicit_requirement", "obligation_only"
    return "scoped_relation", "forbidden_unless_manually_interpreted"


def main() -> None:
    claims = read_jsonl(INDEX / "claims.jsonl")
    raw_edges = read_jsonl(INDEX / "edges.jsonl")
    external = json.loads((INDEX / "external_dependencies.json").read_text(encoding="utf-8"))
    source_docs = read_jsonl(INDEX / "documents.jsonl")
    claim_ids = {c["id"] for c in claims}
    ext_by_id = {e["id"]: e for e in external}
    docs_by_id = {d["id"]: d for d in source_docs}

    with sqlite3.connect(f"file:{INDEX / 'knowledge.sqlite3'}?mode=ro", uri=True) as db:
        docs_by_path = {row[0]: {"id": row[1], "sha256": row[2], "role": row[3]}
                        for row in db.execute("SELECT path,id,sha256,role FROM docs")}

    catalog = []
    for c in sorted(claims, key=lambda x: x["id"]):
        card_path = ROOT / c["path"]
        if not card_path.is_file():
            raise SystemExit(f"Missing card: {c['path']}")
        card_bytes = card_path.read_bytes()
        card_text = card_bytes.decode("utf-8")
        card_hash = hashlib.sha256(card_bytes).hexdigest()
        doc = docs_by_path.get(c["path"])
        if not doc:
            raise SystemExit(f"No DB document for card: {c['path']}")
        if card_hash != doc["sha256"]:
            raise SystemExit(f"Card/DB SHA mismatch: {c['path']}")
        cid = c["id"]
        card_web = f"web/pages/{doc['id']}.html"
        if not (ROOT / card_web).is_file():
            raise SystemExit(f"Missing card web page: {card_web}")
        read_ids = [sid for sid in c.get("source_ids", []) if sid in docs_by_id]
        read_web = [f"web/pages/{sid}.html" for sid in read_ids if (ROOT / f"web/pages/{sid}.html").is_file()]
        deps = {
            "depends_on": c.get("depends_on", []),
            "scoped_dependencies": c.get("scoped_dependencies", []),
        }
        catalog.append({
            "id": cid,
            "title": c["title"],
            "status": c["status"],
            "topics": c.get("topics", []),
            "card_sha256": card_hash,
            "pointers": {
                "card_local": c["path"],
                "read_local": f"python3 tools/knowledge.py read {cid}",
                "card_web": card_web,
                "read_web": read_web,
            },
            "dependencies": deps,
            "quoted_fields": quoted_fields(card_text),
        })

    # Preserve all edge endpoints as explicit nodes, including source documents
    # and opaque historical identifiers, so references never silently disappear.
    node_ids = set(claim_ids) | set(ext_by_id) | set(docs_by_id)
    for e in raw_edges:
        node_ids.add(e["from"])
        node_ids.add(e["to"])
    nodes = []
    for nid in sorted(node_ids):
        if nid in claim_ids:
            nodes.append({"id": nid, "node_kind": "claim"})
        elif nid in ext_by_id:
            d = ext_by_id[nid]
            nodes.append({"id": nid, "node_kind": "dependency", "dependency": d})
        elif nid in docs_by_id:
            d = docs_by_id[nid]
            nodes.append({"id": nid, "node_kind": "evidence", "path": d.get("path"), "title": d.get("title"), "role": d.get("role")})
        else:
            nodes.append({"id": nid, "node_kind": "unresolved_reference", "detail": "No matching claim, dependency, or document record in this snapshot."})

    graph_edges = []
    for e in sorted(raw_edges, key=lambda x: (x["from"], x["to"], x["type"], x.get("source", ""))):
        kind, composition = relation_kind(e["type"])
        graph_edges.append({
            "from": e["from"], "to": e["to"], "kind": kind,
            "raw_kind": e["type"], "source": e.get("source", "UNKNOWN"),
            "composition": composition,
        })

    input_paths = [INDEX / "claims.jsonl", INDEX / "edges.jsonl", INDEX / "external_dependencies.json", INDEX / "documents.jsonl", INDEX / "knowledge.sqlite3"]
    card_hashes = {c["id"]: c["card_sha256"] for c in catalog}
    generated_by_sha = sha256(Path(__file__))
    card_manifest = "\n".join(f"{cid} {digest}" for cid, digest in sorted(card_hashes.items())).encode("utf-8")
    freshness = {
        "schema_version": SCHEMA_VERSION,
        "generator": "tools/build_agent_catalog.py",
        "generator_sha256": generated_by_sha,
        "inputs": {p.relative_to(ROOT).as_posix(): sha256(p) for p in input_paths},
        "cards_manifest_sha256": hashlib.sha256(card_manifest).hexdigest(),
    }
    write_json(INDEX / "agent_catalog.json", {"schema_version": SCHEMA_VERSION, "freshness": freshness, "claims": catalog})
    write_json(INDEX / "agent_graph.json", {"schema_version": SCHEMA_VERSION, "freshness": freshness, "nodes": nodes, "edges": graph_edges})

    topic_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in catalog:
        for topic in item["topics"]:
            topic_rows[topic].append({"id": item["id"], "title": item["title"], "status": item["status"], "card_sha256": item["card_sha256"], "card_local": item["pointers"]["card_local"], "read_local": item["pointers"]["read_local"], "card_web": item["pointers"]["card_web"]})
    topic_dir = INDEX / "agent_topics"
    topic_dir.mkdir(parents=True, exist_ok=True)
    for old in topic_dir.glob("*.json"):
        old.unlink()
    for topic, rows in sorted(topic_rows.items()):
        write_json(topic_dir / f"{topic}.json", {"schema_version": SCHEMA_VERSION, "topic": topic, "freshness": freshness, "claims": sorted(rows, key=lambda x: x["id"])})

    # Referential/pointer validation against on-disk objects and graph endpoints.
    known_nodes = {n["id"] for n in nodes}
    assert all(e["from"] in known_nodes and e["to"] in known_nodes for e in graph_edges)
    for item in catalog:
        assert (ROOT / item["pointers"]["card_local"]).is_file()
        assert (ROOT / item["pointers"]["card_web"]).is_file()
        for pointer in item["pointers"]["read_web"]:
            assert (ROOT / pointer).is_file()
        for dep in item["dependencies"]["scoped_dependencies"]:
            assert dep["id"] in known_nodes, (item["id"], dep["id"])

    metrics = {
        "schema_version": SCHEMA_VERSION,
        "claims": len(catalog), "graph_nodes": len(nodes), "graph_edges": len(graph_edges),
        "edge_kinds": {k: sum(e["kind"] == k for e in graph_edges) for k in ["provenance", "navigation", "explicit_requirement", "scoped_relation"]},
        "unresolved_graph_references": sum(n["node_kind"] == "unresolved_reference" for n in nodes),
        "topic_shards": len(topic_rows), "read_web_pointers": sum(len(c["pointers"]["read_web"]) for c in catalog),
        "sha_and_pointer_validation": "passed",
        "topic_shards_paths": [f"indexes/agent_topics/{t}.json" for t in sorted(topic_rows)],
    }
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
