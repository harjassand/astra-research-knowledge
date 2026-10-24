#!/usr/bin/env python3
"""Versioned compatibility wrapper for the checkpoint-pinned public builder.

The v1 builder remains byte-stable because an immutable handoff pins it. This
wrapper adds append-only semantic-notice shards to that builder's existing
projection and freshness checks without changing its generation rules.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import build_access as legacy

ROOT = legacy.ROOT
BASE_INPUTS = tuple(legacy.INPUTS)
BASE_JSONL = legacy.jsonl


def notice_shards(root=ROOT):
    folder = root / "agent/SEMANTIC_NOTICES.d"
    return sorted(p for p in folder.glob("*.jsonl") if p.is_file()) if folder.is_dir() else []


def jsonl_with_shards(root, name):
    result = BASE_JSONL(root, name)
    if name == "agent/SEMANTIC_NOTICES.jsonl":
        for path in notice_shards(root):
            result.extend(BASE_JSONL(root, path.relative_to(root).as_posix()))
    return result


def build(root=ROOT, base_revision=None):
    shards = [p.relative_to(root).as_posix() for p in notice_shards(root)]
    legacy.jsonl = jsonl_with_shards
    legacy.INPUTS = list(dict.fromkeys([*BASE_INPUTS, "frontier/build_access_v2.py", "frontier/retrieve.py", *shards]))
    outputs, manifest = legacy.build(root=root, base_revision=base_revision)
    current = outputs["agent/CURRENT.txt"].replace(
        b"frontier/build_access.py check", b"frontier/build_access_v2.py check"
    )
    outputs["agent/CURRENT.txt"] = current
    manifest["outputs"]["agent/CURRENT.txt"] = legacy.digest(current)
    outputs["agent/access_manifest.json"] = legacy.encoded(manifest)
    return outputs, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "check"])
    parser.add_argument("--base-revision")
    args = parser.parse_args()
    manifest_path = ROOT / "agent/access_manifest.json"
    base_revision = args.base_revision
    if base_revision is None and manifest_path.exists():
        base_revision = json.loads(manifest_path.read_text())["snapshot"]["base_revision"]
    if base_revision is None:
        base_revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    subprocess.run(["git", "cat-file", "-e", base_revision + "^{commit}"], cwd=ROOT, check=True, capture_output=True)
    outputs, manifest = build(base_revision=base_revision)
    if args.command == "build":
        if manifest_path.exists():
            old = json.loads(manifest_path.read_text())
            removed = set(old["outputs"]) - outputs.keys()
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
    print(json.dumps({"command": args.command, "counts": manifest["counts"], "input_sha256": manifest["snapshot"]["input_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
