#!/usr/bin/env python3
"""Validate byte identity, JSON syntax and navigation; never theorem correctness."""
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
PACKAGED = (Path(__file__).resolve().parent.parent / "proofs").is_dir()
PACKAGE = Path(__file__).resolve().parent.parent if PACKAGED else ROOT / "outputs" / "research"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def reject_constant(value):
    raise ValueError(f"Non-standard JSON constant {value}")

inventory = json.loads((PACKAGE / "ARTIFACT_INVENTORY.json").read_text())
errors = []
included = [r for r in inventory["records"] if r["included"]]
for row in included:
    target = PACKAGE / row["package_path"]
    if not target.is_file() or sha(target) != row["sha256"]:
        errors.append(f"Retained source mismatch: {row['package_path']}")

frozen = json.loads((PACKAGE / "process/frozen_proofs.json").read_text())
for row in frozen["proofs"]:
    target = PACKAGE / "proofs" / Path(row["path"]).relative_to("work/agents")
    if sha(target) != row["expected_sha256"]:
        errors.append(f"Frozen proof changed: {row['path']}")

ledger = json.loads((PACKAGE / "CLAIM_LEDGER.json").read_text())
dependencies = json.loads((PACKAGE / "DEPENDENCIES.json").read_text())
claim_ids = {row["id"] for row in ledger["claims"]}
if len(claim_ids) != len(ledger["claims"]):
    errors.append("Duplicate claim identifiers")
for evidence_id, row in ledger["evidence"].items():
    target = PACKAGE / row["package_path"]
    if not target.is_file() or sha(target) != row["sha256"]:
        errors.append(f"Ledger evidence mismatch: {evidence_id}")
for claim in ledger["claims"]:
    for evidence_id in claim["evidence_ids"]:
        if evidence_id not in ledger["evidence"]:
            errors.append(f"Missing evidence identifier: {claim['id']} -> {evidence_id}")
    for dependency in claim["depends_on_claims"]:
        if dependency not in claim_ids:
            errors.append(f"Missing claim dependency: {claim['id']} -> {dependency}")
node_ids = {row["id"] for row in dependencies["nodes"]}
for edge in dependencies["edges"]:
    if edge["from"] not in node_ids or edge["to"] not in node_ids:
        errors.append(f"Dangling dependency edge: {edge}")

json_count = 0
for path in PACKAGE.rglob("*"):
    if not path.is_file():
        continue
    try:
        if path.suffix == ".json":
            json.loads(path.read_text(), parse_constant=reject_constant)
            json_count += 1
        elif path.suffix == ".jsonl":
            for line in path.read_text().splitlines():
                if line.strip():
                    json.loads(line, parse_constant=reject_constant)
            json_count += 1
    except Exception as err:
        errors.append(f"JSON parse failure: {path.relative_to(PACKAGE)}: {err}")

links = []
for name in ("README.md", "REPORT.md", "PROVENANCE_AND_REPRODUCTION.md"):
    path = PACKAGE / name
    if not path.is_file():
        errors.append(f"Missing navigation file: {name}")
        continue
    for raw in re.findall(r"\]\(([^)]+)\)", path.read_text()):
        href = raw.strip().strip("<>")
        if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", href) or href.startswith("#"):
            continue
        href = unquote(href.split("#", 1)[0])
        target = path.parent / href
        links.append({"from": name, "target": href, "exists": target.exists()})
        if not target.exists():
            errors.append(f"Broken local link: {name} -> {href}")

payload = {
    "scope": "Packaging integrity, strict JSON syntax and top-level navigation only; not proof validation.",
    "retained_source_files_checked": len(included),
    "frozen_proofs_checked": len(frozen["proofs"]),
    "ledger_evidence_files_checked": len(ledger["evidence"]),
    "dependency_edges_checked": len(dependencies["edges"]),
    "json_or_jsonl_files_checked": json_count,
    "local_links": links,
    "errors": errors,
}
if not PACKAGED:
    (PACKAGE / "verification/PACKAGE_VALIDATION.json").write_text(json.dumps(payload, indent=2) + "\n")
print(json.dumps({k:v for k,v in payload.items() if k != "local_links"}, indent=2))
raise SystemExit(bool(errors))
