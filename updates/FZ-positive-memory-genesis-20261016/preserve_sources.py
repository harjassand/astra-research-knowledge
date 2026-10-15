#!/usr/bin/env python3
"""Plan or exclusively copy the exact FZ supplied inventory and both manifests."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fz_common import PREFIX, RESEARCH_ROOT, ORIGINAL_MANIFEST_NAME, ORIGINAL_MANIFEST_SHA256, PREVIOUS_MANIFEST_NAME, digest, encoded, local, need, source_outputs


def create_exclusive(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".fz-preserve-", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    try:
        os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def plan_sources(repo, *, research_root=RESEARCH_ROOT):
    repo, research_root = Path(repo).resolve(), Path(research_root).resolve()
    inputs = {}

    def read(name):
        inputs[name] = local(research_root, name).read_bytes()
        return inputs[name]

    manifest_raw, previous_raw = read(ORIGINAL_MANIFEST_NAME), read(PREVIOUS_MANIFEST_NAME)
    outputs, wrapper = source_outputs(manifest_raw, previous_raw, read)
    before = {}
    for name, raw in outputs.items():
        path = local(repo, name)
        before[name] = path.read_bytes() if path.is_file() else None
        need(before[name] in (None, raw), "Immutable source-preservation collision: " + name)
    return {"repo": repo, "research_root": research_root, "inputs": inputs, "outputs": outputs,
            "before": before, "wrapper": wrapper}


def apply_sources(plan):
    for name, raw in plan["inputs"].items():
        need(local(plan["research_root"], name).read_bytes() == raw, "Source changed during preservation; replan")
    for name, before in plan["before"].items():
        path = local(plan["repo"], name)
        need((path.read_bytes() if path.is_file() else None) == before, "Concurrent source-preservation change; replan")
    changed = 0
    for name, raw in plan["outputs"].items():
        if plan["before"][name] != raw:
            create_exclusive(local(plan["repo"], name), raw)
            changed += 1
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--copy", action="store_true")
    parser.add_argument("--expect-manifest-sha256")
    args = parser.parse_args()
    if args.copy:
        need(args.expect_manifest_sha256 == ORIGINAL_MANIFEST_SHA256, "Copy requires the exact pinned v2 manifest SHA-256")
    plan = plan_sources(args.repo)
    wrapper = plan["wrapper"]
    result = {"schema": "astra.fz-source-preservation-receipt.v1", "mode": "read_only",
              "original_manifest_sha256": ORIGINAL_MANIFEST_SHA256,
              "original_files": wrapper["original_count"], "original_bytes": wrapper["original_bytes"],
              "original_manifest_files": wrapper["original_manifest_files"],
              "all_preserved_file_count": wrapper["all_preserved_file_count"],
              "all_preserved_bytes": wrapper["all_preserved_bytes"],
              "operative_request": wrapper["operative_request"], "source_scripts_executed": False,
              "scientific_claims_curated": False, "worker_evidence_selected": False,
              "live_authority_application": "NOT_PERFORMED", "canonical_checkpoint_publication": "NOT_PERFORMED"}
    if args.copy:
        result.update({"new_file_count": apply_sources(plan), "mode": "source_packet_copy_only"})
    print(encoded(result).decode(), end="")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print("FZ source preservation failed closed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
