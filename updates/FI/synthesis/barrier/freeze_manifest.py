#!/usr/bin/env python3
"""Create the deterministic SHA-256/byte inventory for the FI-barrier audit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "work" / "FI-barrier"
CAPITAL_PATHS = [
    "work/astra-capital/AGENTS.md",
    "work/astra-capital/00_START_HERE.txt",
    "work/astra-capital/agent/routes.tsv",
    "work/astra-capital/technology/README.md",
    "work/astra-capital/technology/routes.tsv",
    "work/astra-capital/frontier/dossiers/N774.txt",
    "work/astra-capital/frontier/dossiers/N777.txt",
    "work/astra-capital/updates/EZ/package/lattice_loop/recovered/astra_lattice_loop/DERIVATION_AND_EXPERIMENT.md",
    "work/astra-capital/updates/FA/package/controlled_matter/recovered/astra_controlled_matter_audit/REPORT.md",
    "work/astra-capital/updates/FA/synthesis/matter/SYNTHESIS_REPORT.md",
    "work/astra-capital/technology/records/T-phase-controlled-lattice-ion-transport/v0002.json",
]
ROOT_CLAIMS_PATHS = [
    "work/FI-root/mixed_compliance_gate.py",
    "work/FI-root/MIXED_GATE_RESULTS.json",
]


def digest(path: Path) -> dict[str, int | str]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> None:
    package_files = []
    for path in sorted(PACKAGE.rglob("*")):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(PACKAGE).parts
        if ".venv" in relative_parts or "__pycache__" in relative_parts:
            continue
        if path.name in {"MANIFEST.json", "MANIFEST.sha256"}:
            continue
        package_files.append(path)

    source_files = sorted((ROOT / "work" / "FI-sources" / "barrier").glob("*"))
    source_files.append(ROOT / "work" / "FI-sources" / "barrier_PASTED_SOURCE.txt")
    capital_files = [ROOT / relative for relative in CAPITAL_PATHS]
    root_claim_files = [ROOT / relative for relative in ROOT_CLAIMS_PATHS]
    for path in [*source_files, *capital_files, *root_claim_files]:
        if not path.is_file():
            raise FileNotFoundError(path)

    entries = [
        {**digest(path), "class": "owned_audit_package"} for path in package_files
    ]
    entries.extend({**digest(path), "class": "read_only_supplied_source"} for path in source_files)
    entries.extend({**digest(path), "class": "read_only_astra_capital_context"} for path in capital_files)
    entries.extend({**digest(path), "class": "root_claim_under_independent_audit"} for path in root_claim_files)
    entries.sort(key=lambda entry: entry["path"])

    manifest = {
        "schema": "sha256-byte-inventory-v1",
        "frozen_date": "2026-10-14",
        "workspace_relative_to": ".",
        "files": entries,
        "excluded": [
            "Disposable work/FI-barrier/.venv environment; dependencies are pinned in requirements.txt.",
            "MANIFEST.json and MANIFEST.sha256 (circular self-reference); the detached file contains MANIFEST.json's SHA-256.",
            "External third-party manuscript bytes; the versioned primary URL and read locations are recorded in READ_PRIMARY_LEDGER.md.",
        ],
        "external_primary_sources": [
            {
                "title": "Domain-induced control of latent heat in freestanding BaTiO3 membranes",
                "version": "arXiv:2604.26089v1",
                "url": "https://arxiv.org/html/2604.26089v1",
                "read_date": "2026-10-14",
                "manuscript_copied_into_package": False,
            }
        ],
        "evidence_scope": "byte integrity only; not proof, review, novelty, material validation, or physical performance",
    }
    manifest_path = PACKAGE / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest_sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    (PACKAGE / "MANIFEST.sha256").write_text(f"{manifest_sha}  MANIFEST.json\n", encoding="ascii")
    print(f"{manifest_sha}  {manifest_path.relative_to(ROOT)}")
    print(f"{len(entries)} inventoried files; {sum(int(row['bytes']) for row in entries)} bytes")


if __name__ == "__main__":
    main()
