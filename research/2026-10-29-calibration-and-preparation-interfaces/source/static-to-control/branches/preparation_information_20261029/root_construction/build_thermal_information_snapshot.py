#!/usr/bin/env python3
"""Preserve the current scientific branch plus its exact complete predecessor."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import zipfile


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    here = Path(__file__).resolve()
    branch = here.parents[1]
    project = here.parents[3]
    workspace = project.parent
    previous = workspace / "Astra_P1_Physical_Information_and_Hidden_Memory_20261029.zip"
    previous_hash = "e053e46fb9bbbdb1d32c1a2abc7dbc05f895d4b83e7d8571a004d6eca0ede9c7"
    prior_bytes = previous.read_bytes()
    assert digest(prior_bytes) == previous_hash, "Predecessor bytes changed"
    output = workspace / "Astra_P1_Thermal_Information_and_Control_20261029.zip"

    entries: dict[str, bytes] = {}
    for path in sorted(branch.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            entries[str(path.relative_to(workspace))] = path.read_bytes()
    for name in ("README.md", "CURRENT_SCIENCE_STATE.md"):
        entries[str((project / name).relative_to(workspace))] = (project / name).read_bytes()
    entries["HANDOFF.md"] = (branch / "HANDOFF.md").read_bytes()
    predecessor_entry = "predecessor/" + previous.name
    entries[predecessor_entry] = prior_bytes
    manifest = {
        "date": "2026-10-29",
        "title": "Astra P1 thermal information and controlled prediction",
        "entrypoint": "HANDOFF.md",
        "current_branch": str(branch.relative_to(workspace)),
        "predecessor": {
            "archive": predecessor_entry,
            "sha256": previous_hash,
            "scope": "Complete prior snapshot preserved byte-for-byte, including earlier archives",
        },
        "scientific_scope": {
            "new": "Native static-information/entropy-to-control principle, quantitative transition/path bounds, snapshot-memory composition, fine-path one-bit boundary, finite acquisition contracts",
            "evidence": "Ordinary proofs, scoped internal independent reviews, exact finite arithmetic controls and selective primary sources",
            "not_executed": [
                "Native physical acquisition or apparatus operation",
                "Physical stationary/Gibbs preparation",
                "Instantiated numerical Schauder/product/cutoff constants",
                "End-to-end controlled simulation and practical cost comparison",
            ],
            "priority": "Unresolved; no external acceptance or exclusive speedup claimed",
        },
        "files": [
            {"path": name, "bytes": len(data), "sha256": digest(data)}
            for name, data in sorted(entries.items())
        ],
        "manifest_hash_scope": "The manifest lists every other archive entry; it does not hash itself.",
    }
    entries["MANIFEST.json"] = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(entries.items()):
            archive.writestr(name, data, compress_type=(zipfile.ZIP_STORED if name == predecessor_entry else zipfile.ZIP_DEFLATED))
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert len(archive.namelist()) == len(entries)
        saved = json.loads(archive.read("MANIFEST.json"))
        for item in saved["files"]:
            data = archive.read(item["path"])
            assert len(data) == item["bytes"] and digest(data) == item["sha256"]
        assert digest(archive.read(predecessor_entry)) == previous_hash
    result = {
        "path": str(output),
        "bytes": output.stat().st_size,
        "sha256": digest(output.read_bytes()),
        "entries": len(entries),
        "manifest_file_hashes_verified": len(manifest["files"]),
        "zip_crc": "passed",
        "predecessor_unchanged": True,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
