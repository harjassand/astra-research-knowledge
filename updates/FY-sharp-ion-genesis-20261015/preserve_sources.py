#!/usr/bin/env python3
"""Plan or copy the pinned three-file FY pasted-source packet; no extraction or authority writes."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fy_common import PREFIX, RESEARCH_ROOT, ORIGINAL_MANIFEST_SHA256, digest, encoded, local, need, source_outputs


def create_exclusive(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".fy-preserve-", delete=False) as stream:
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
    manifest_raw = local(research_root, "sources/SOURCE_MANIFEST.json").read_bytes()
    inputs = {"sources/SOURCE_MANIFEST.json": manifest_raw}

    def read(name):
        raw = local(research_root, name).read_bytes()
        inputs[name] = raw
        return raw

    outputs, wrapper = source_outputs(manifest_raw, read)
    expected = {x["research_relative_path"] for x in wrapper["files"]}
    expected.add("sources/SOURCE_MANIFEST.json")
    source_folder = local(research_root, "sources")
    for path in source_folder.rglob("*"):
        need(not path.is_symlink(), "Source symlink is forbidden")
    observed = {str(p.relative_to(research_root)) for p in source_folder.rglob("*") if p.is_file()}
    extra = observed - expected
    need(not expected - observed and all("__pycache__" in Path(x).parts and x.endswith(".pyc") for x in extra),
         "Research source inventory differs from pinned source inventory")
    caches = [{"research_relative_path": x, "sha256": digest(local(research_root, x).read_bytes()),
               "classification": "unmanifested runtime bytecode; excluded, not supplied source"} for x in sorted(extra)]
    before = {}
    for name, raw in outputs.items():
        p = local(repo, name)
        before[name] = p.read_bytes() if p.is_file() else None
        need(before[name] in (None, raw), "Immutable source-preservation collision: " + name)
    return {"repo": repo, "research_root": research_root, "inputs": inputs, "outputs": outputs,
            "before": before, "wrapper": wrapper, "excluded_runtime_cache_observations": caches}


def apply_sources(plan):
    for name, raw in plan["inputs"].items():
        need(local(plan["research_root"], name).read_bytes() == raw, "Source changed during preservation; replan")
    for name, before in plan["before"].items():
        p = local(plan["repo"], name)
        need((p.read_bytes() if p.is_file() else None) == before, "Concurrent preservation target change; replan")
    changed = 0
    for name, raw in plan["outputs"].items():
        if plan["before"][name] != raw:
            create_exclusive(local(plan["repo"], name), raw)
            changed += 1
    return changed


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", required=True, type=Path)
    p.add_argument("--copy", action="store_true")
    p.add_argument("--expect-manifest-sha256")
    args = p.parse_args()
    if args.copy:
        need(args.expect_manifest_sha256 == ORIGINAL_MANIFEST_SHA256, "Copy requires exact pinned intake-manifest SHA-256")
    plan = plan_sources(args.repo)
    m = plan["wrapper"]
    result = {"schema": "astra.fy-source-preservation-receipt.v1", "mode": "read_only",
              "original_manifest_sha256": ORIGINAL_MANIFEST_SHA256, "original_files": m["original_count"],
              "original_bytes": m["original_bytes"], "archives": m["archive_count"],
              "extracted_members": 0, "operative_request": m["operative_request"],
              "missing_artifacts": m["missing_artifacts"], "missing_artifact_replays": m["missing_artifact_replays"], "source_scripts_executed": False, "scientific_claims_curated": False,
              "excluded_runtime_cache_observations": plan["excluded_runtime_cache_observations"],
              "live_authority_application": "NOT_PERFORMED", "canonical_checkpoint_publication": "NOT_PERFORMED"}
    if args.copy:
        result.update({"new_file_count": apply_sources(plan), "mode": "source_packet_copy_only"})
    print(encoded(result).decode(), end="")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print("FY source preservation failed closed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
