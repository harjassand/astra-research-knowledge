#!/usr/bin/env python3
"""One local/CI check of publication integrity against an actual Git PR base.

No scientific scripts, model calls, or private research are executed.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

import publish_checkpoint as checkpoints
import publish_result


def run(root, *args):
    subprocess.run([sys.executable, *args], cwd=root, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-revision", required=True, help="full actual PR base SHA; fetch its history first")
    parser.add_argument("--fetch-sources", action="store_true", help="explicitly fetch missing exact evidence revisions from origin")
    args = parser.parse_args()
    root = checkpoints.ROOT
    try:
        checkpoints.require(bool(checkpoints.REVISION.fullmatch(args.base_revision)), "base-revision must be a full commit ID")
        checkpoints.git(root, "cat-file", "-e", args.base_revision + "^{commit}")
        checkpoints.git(root, "merge-base", "--is-ancestor", args.base_revision, "HEAD")
        if args.fetch_sources:
            revisions = set()
            for path in sorted((root / "state/checkpoints").glob("*/*.json")):
                for ref in json.loads(path.read_text(encoding="utf-8")).get("evidence_refs", []):
                    revision = ref.get("source_revision")
                    if revision is not None:
                        checkpoints.require(isinstance(revision, str) and checkpoints.REVISION.fullmatch(revision),
                                            f"invalid evidence source revision in {path}")
                        revisions.add(revision)
            for revision in sorted(revisions):
                exists = subprocess.run(["git", "-C", str(root), "cat-file", "-e", revision + "^{commit}"],
                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if exists.returncode:
                    print("Fetching exact evidence revision from origin: " + revision, flush=True)
                    subprocess.run(["git", "-C", str(root), "fetch", "--no-tags", "--no-write-fetch-head", "origin", revision], check=True)
        tracked = set(subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"]).decode().split("\0"))
        for path in sorted((root / "state/checkpoints").glob("*/*.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            if "publication" in record:
                publish_result.validate_publication(record)
                for ref in record["evidence_refs"]:
                    checkpoints.require(ref["path"] in tracked, f"publication evidence is absent from the reviewed Git tree: {ref['path']}")
        run(root, "state/publish_checkpoint.py", "validate", "--immutable-base", args.base_revision)
        run(root, "state/publish_checkpoint.py", "self-test")
        run(root, "-m", "unittest", "discover", "-s", "state", "-p", "test_*.py")
        run(root, "-m", "unittest", "discover", "-s", "frontier", "-p", "test_access.py")
        run(root, "frontier/build_access.py", "check")
        print("Publication structure, evidence integrity, append-only history and generated access checks passed. "
              "Historical exceptions remain explicitly limited; scientific correctness is not certified.")
    except (checkpoints.Invalid, OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
