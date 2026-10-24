#!/usr/bin/env python3
"""Build this publication's current public views without rewriting pinned v2 evidence.

Earlier checkpoint records pin agent/access_manifest.json and the v2 reader. Keep
those bytes as their historical snapshot; this wrapper writes a dated v3 manifest
and routes current reads through retrieve_v3.py.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import build_access as legacy
import build_access_v2 as v2

ROOT = legacy.ROOT
MANIFEST_PATH = "agent/access_manifest.2026-10-24-constructive-universal.json"


def build(root=ROOT, base_revision=None):
    shards = [p.relative_to(root).as_posix() for p in v2.notice_shards(root)]
    legacy.jsonl = v2.jsonl_with_shards
    legacy.INPUTS = list(dict.fromkeys([
        *v2.BASE_INPUTS,
        "frontier/build_access_v2.py",
        "frontier/build_access_v3.py",
        "frontier/retrieve.py",
        "frontier/retrieve_v3.py",
        "frontier/test_access_v3.py",
        *shards,
    ]))
    outputs, manifest = legacy.build(root=root, base_revision=base_revision)

    # Keep the checkpoint-pinned v2 manifest at its original path and hash.
    outputs.pop("agent/access_manifest.json", None)

    current = outputs["agent/CURRENT.txt"].replace(
        b"Freshness: frontier/build_access.py check checks current input/output hashes and regeneration.\n",
        ("Freshness: python3 frontier/build_access_v3.py check verifies current input/output hashes and regeneration.\n"
         f"Current access manifest: {MANIFEST_PATH}; current local reader: frontier/retrieve_v3.py.\n").encode(),
    )
    outputs["agent/CURRENT.txt"] = current
    manifest["outputs"]["agent/CURRENT.txt"] = legacy.digest(current)

    legacy_manifest = json.loads(outputs["agent/manifest.json"])
    legacy_manifest["public_access"] = {
        "manifest": MANIFEST_PATH,
        "snapshot": manifest["snapshot"],
        "scope": "Current versioned public projection; earlier checkpoint-pinned manifests remain immutable historical snapshots",
    }
    outputs["agent/manifest.json"] = legacy.encoded(legacy_manifest)
    manifest["outputs"]["agent/manifest.json"] = legacy.digest(outputs["agent/manifest.json"])
    outputs[MANIFEST_PATH] = legacy.encoded(manifest)
    return outputs, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "check"])
    parser.add_argument("--base-revision")
    args = parser.parse_args()
    manifest_path = ROOT / MANIFEST_PATH
    base_revision = args.base_revision
    if base_revision is None and manifest_path.exists():
        base_revision = json.loads(manifest_path.read_text())["snapshot"]["base_revision"]
    if base_revision is None:
        base_revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    subprocess.run(["git", "cat-file", "-e", base_revision + "^{commit}"], cwd=ROOT, check=True, capture_output=True)
    outputs, manifest = build(base_revision=base_revision)
    if args.command == "build":
        prior = manifest_path if manifest_path.exists() else ROOT / "agent/access_manifest.json"
        if prior.exists():
            old = json.loads(prior.read_text())
            removed = set(old.get("outputs", {})) - outputs.keys()
            if removed:
                raise ValueError("Generated routes would disappear; provide explicit migration: " + str(sorted(removed)))
        for name, data in outputs.items():
            target = ROOT / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    else:
        stale = [name for name, data in outputs.items() if not (ROOT / name).is_file() or (ROOT / name).read_bytes() != data]
        if stale:
            raise ValueError("Missing/stale generated views: " + ", ".join(stale[:8]))
    print(json.dumps({"command": args.command, "manifest": MANIFEST_PATH, "counts": manifest["counts"], "input_sha256": manifest["snapshot"]["input_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
