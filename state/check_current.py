#!/usr/bin/env python3
"""Existing publication gate, current normalization and immutable historical evidence."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from knowledge.model import evidence_refs
from state import publish_checkpoint as checkpoints
from state import publish_result

ROOT = Path(__file__).resolve().parents[1]


def run(*arguments):
    subprocess.run([sys.executable, *arguments], cwd=ROOT, check=True)


def historical_integrity(base):
    changed = subprocess.check_output(["git", "diff", "--name-only", base, "--"], cwd=ROOT, text=True).splitlines()
    paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", base,
                                     "frontier/CURRENT_CLAIM_STATUS.jsonl", "frontier/CURRENT_CLAIM_STATUS.d"], cwd=ROOT, text=True).splitlines()
    protected = set()
    for path in paths:
        rows = subprocess.check_output(["git", "show", base + ":" + path], cwd=ROOT)
        for line in rows.splitlines():
            if not line.strip():
                continue
            for ref in evidence_refs(json.loads(line)):
                protected.update(name for name in (ref["path"], ref.get("read_path")) if name and not name.startswith("cards/"))
    frozen = ("frontier/dossiers/", "frontier/dossiers_v5/", "frontier/connections/", "frontier/connections_v5/",
              "frontier/proof_ranges/", "knowledge/units/", "knowledge/reviews/", "knowledge/audits/",
              "technology/records/")
    for path in changed:
        exists = subprocess.run(["git", "cat-file", "-e", base + ":" + path], cwd=ROOT,
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
        if exists and (path in protected or path.startswith(frozen)
                       or path.startswith("agent/access_manifest")
                       or path.startswith("frontier/build_access") or path.startswith("frontier/retrieve")):
            raise ValueError("Historical source/version must not be rewritten: " + path)
    original = subprocess.check_output(["git", "show", "d49387def190cb8c7ce8472baf7181c751d11bf6:index.html"], cwd=ROOT)
    if (ROOT / "index-historical-20261025.html").read_bytes() != original:
        raise ValueError("Historical public catalog bytes changed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-revision", required=True)
    parser.add_argument("--fetch-sources", action="store_true")
    args = parser.parse_args()
    try:
        checkpoints.require(bool(checkpoints.REVISION.fullmatch(args.base_revision)), "base-revision must be a full commit ID")
        checkpoints.git(ROOT, "cat-file", "-e", args.base_revision + "^{commit}")
        checkpoints.git(ROOT, "merge-base", "--is-ancestor", args.base_revision, "HEAD")
        historical_integrity(args.base_revision)
        tracked = set(subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0"))
        for path in sorted((ROOT / "state/checkpoints").glob("*/*.json")):
            record = json.loads(path.read_bytes())
            if "publication" in record:
                publish_result.validate_publication(record)
                for ref in record["evidence_refs"]:
                    checkpoints.require(ref["path"] in tracked, "Publication evidence absent from reviewed tree: " + ref["path"])
            if args.fetch_sources:
                for revision in sorted({ref["source_revision"] for ref in record.get("evidence_refs", []) if ref.get("source_revision")}):
                    checkpoints.require(bool(checkpoints.REVISION.fullmatch(revision)), "Invalid source revision")
                    if subprocess.run(["git", "cat-file", "-e", revision + "^{commit}"], cwd=ROOT,
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
                        subprocess.run(["git", "fetch", "--no-tags", "--no-write-fetch-head", "origin", revision], cwd=ROOT, check=True)
        packet = "research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-25-later-completed-sources/verify_manifest.py"
        run(packet)
        run("state/publish_checkpoint.py", "validate", "--immutable-base", args.base_revision)
        run("state/publish_checkpoint.py", "self-test")
        run("-m", "unittest", "discover", "-s", "state", "-p", "test_*.py")
        run("-m", "unittest", "discover", "-s", "knowledge", "-p", "test_*.py")
        run("-m", "unittest", "discover", "-s", "technology", "-p", "test_*.py")
        run("knowledge/build.py", "check")
        print("Current publication, historical evidence, deterministic intake and generated-view checks passed. Scientific usefulness is assessed separately.")
    except (OSError, ValueError, KeyError, TypeError, checkpoints.Invalid, subprocess.CalledProcessError) as error:
        print("ERROR: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
