#!/usr/bin/env python3
"""Verify the selected public source package without opening withheld material."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
PACKET = ROOT / "research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-25-later-completed-sources"
MANIFEST = PACKET / "source_manifest.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    record = json.loads(MANIFEST.read_text(encoding="utf-8"))
    files = record["files"]
    withheld = record["withheld"]
    if record["selected_source_files"] != 171 or record["copied_files"] != 165 or record["withheld_files"] != 6:
        raise SystemExit("Selected-source counts changed")
    if len(files) != 165 or len(withheld) != 6:
        raise SystemExit("Manifest entry counts do not match the selected-source counts")
    copied_bytes = 0
    copied_hashes = set()
    retained_paths = set()
    for entry in files:
        rel = Path(entry["retained_path"])
        target = (PACKET / rel).resolve()
        if not target.is_relative_to(PACKET.resolve()) or not target.is_file():
            raise SystemExit("Missing or unsafe selected source path")
        data = target.read_bytes()
        actual = sha256(data)
        if actual != entry["sha256"] or len(data) != entry["bytes"]:
            raise SystemExit("Selected source hash/size mismatch: " + rel.as_posix())
        if rel.as_posix() in retained_paths:
            raise SystemExit("Duplicate retained source path: " + rel.as_posix())
        retained_paths.add(rel.as_posix())
        copied_hashes.add(actual)
        copied_bytes += len(data)
    if copied_bytes != record["copied_bytes"] or copied_bytes != 5439014:
        raise SystemExit("Selected source byte total changed")
    if any(entry["sha256"] in copied_hashes for entry in withheld):
        raise SystemExit("A withheld exact-byte object appears in the copied set")
    for entry in withheld:
        if set(entry) != {"id", "bytes", "sha256", "git_blob", "disposition"}:
            raise SystemExit("Withheld record contains unexpected descriptive fields")
        if not (entry["id"].startswith("BIO-WITHHELD-") and len(entry["sha256"]) == 64 and len(entry["git_blob"]) == 40):
            raise SystemExit("Withheld hash-only record malformed")
    already = record["already_available_references"]
    if len(already) != 10:
        raise SystemExit("Already-available reference count changed")
    for entry in already:
        if len(entry["main_paths"]) != 1:
            raise SystemExit("Unexpected main reference shape")
        target = (ROOT / entry["main_paths"][0]).resolve()
        if not target.is_relative_to(ROOT.resolve()) or not target.is_file():
            raise SystemExit("Missing or unsafe existing-main reference")
        data = target.read_bytes()
        if sha256(data) != entry["sha256"] or len(data) != entry["bytes"]:
            raise SystemExit("Existing-main reference hash/size mismatch")
    print(json.dumps({"selected": 171, "copied": 165, "copied_bytes": copied_bytes,
                      "withheld_hash_only": len(withheld), "already_available": len(already),
                      "source_scripts_executed": False}, sort_keys=True))


if __name__ == "__main__":
    main()
