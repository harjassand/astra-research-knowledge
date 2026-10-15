#!/usr/bin/env python3
"""Plan or preserve all pinned original bytes and safe ZIP member bytes only."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fw_common import PREFIX, RESEARCH_ROOT, ORIGINAL_MANIFEST_SHA256, digest, encoded, local, need, source_outputs


def create_exclusive(path, raw):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".fw-preserve-", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    try:
        os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def plan_sources(repo, *, research_root=RESEARCH_ROOT):
    repo = Path(repo).resolve()
    research_root = Path(research_root).resolve()
    manifest_raw = local(research_root, "SOURCE_MANIFEST.json").read_bytes()
    inputs = {"SOURCE_MANIFEST.json": manifest_raw}

    def read(name):
        raw = local(research_root, name).read_bytes()
        inputs[name] = raw
        return raw

    outputs, wrapper = source_outputs(manifest_raw, read)
    # Confirm the original extraction performed at acquisition. The preserved
    # extraction is reconstructed from the pinned ZIP, not trusted as a source.
    for entry in wrapper["files"]:
        name = entry["research_relative_path"]
        raw = local(research_root, name).read_bytes()
        need(digest(raw) == entry["sha256"] and len(raw) == entry["bytes"], "Research extraction/original changed: " + name)
        inputs[name] = raw
    observed = {str(p.relative_to(research_root)) for p in local(research_root, "sources").rglob("*") if p.is_file()}
    expected = {x["research_relative_path"] for x in wrapper["files"]}
    extra = observed - expected
    # Concurrent scientific replays may have created Python bytecode caches. They
    # are explicitly accounted for as unselected runtime artifacts, never treated
    # as supplied source, and never removed or copied by this preservation tool.
    need(not expected - observed and all("__pycache__" in Path(name).parts and name.endswith(".pyc") for name in extra),
         "Research source inventory differs from pinned original-plus-extraction inventory")
    cache_observations = []
    for name in sorted(extra):
        raw = local(research_root, name).read_bytes()
        cache_observations.append({"research_relative_path": name, "sha256": digest(raw), "bytes": len(raw),
                                   "classification": "unmanifested runtime bytecode; excluded, not supplied source"})
    for path in local(research_root, "sources").rglob("*"):
        need(not path.is_symlink(), "Source symlink is forbidden")
    before = {}
    for name, raw in outputs.items():
        path = local(repo, name)
        before[name] = path.read_bytes() if path.is_file() else None
        need(before[name] in (None, raw), "Immutable source-preservation collision: " + name)
    return {"repo": repo, "research_root": research_root, "inputs": inputs, "outputs": outputs, "before": before,
            "wrapper": wrapper, "excluded_runtime_cache_observations": cache_observations}


def apply_sources(plan):
    # Recheck all inputs and every target before the first write. Existing exact
    # bytes are idempotent; collisions never overwrite or delete evidence.
    for name, raw in plan["inputs"].items():
        need(local(plan["research_root"], name).read_bytes() == raw, "Source changed during preservation; replan")
    for name, before in plan["before"].items():
        path = local(plan["repo"], name)
        need((path.read_bytes() if path.is_file() else None) == before, "Concurrent preservation target change; replan")
    changed = 0
    for name, raw in plan["outputs"].items():
        if plan["before"][name] != raw:
            create_exclusive(local(plan["repo"], name), raw)
            changed += 1
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--copy", action="store_true", help="Create source packet only; no authority or scientific execution")
    parser.add_argument("--expect-manifest-sha256", help="Required with --copy")
    args = parser.parse_args()
    if args.copy:
        need(args.expect_manifest_sha256 == ORIGINAL_MANIFEST_SHA256, "Copy requires exact pinned intake-manifest SHA-256")
    plan = plan_sources(args.repo)
    result = {"schema": "astra.fw-source-preservation-receipt.v1", "mode": "read_only",
              "original_manifest_sha256": ORIGINAL_MANIFEST_SHA256,
              "original_files": plan["wrapper"]["original_count"], "original_bytes": plan["wrapper"]["original_bytes"],
              "archives": plan["wrapper"]["archive_count"], "extracted_members": plan["wrapper"]["extracted_member_count"],
              "preserved_source_files": plan["wrapper"]["source_count"], "preserved_source_bytes": plan["wrapper"]["total_bytes"],
              "safe_extraction_recomputed_from_original_archives": True, "research_existing_extraction_matches": True,
              "excluded_runtime_cache_observations": plan["excluded_runtime_cache_observations"],
              "source_scripts_executed": False, "scientific_claims_curated": False,
              "live_authority_application": "NOT_PERFORMED", "canonical_checkpoint_publication": "NOT_PERFORMED"}
    if args.copy:
        result["new_file_count"] = apply_sources(plan)
        result["mode"] = "source_packet_copy_only"
    print(encoded(result).decode(), end="")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print("FW source preservation failed closed: " + str(error), file=sys.stderr)
        raise SystemExit(1)
