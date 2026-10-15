#!/usr/bin/env python3
"""Check exact preserved evidence in a Git tree, not just filesystem copies."""
import argparse
import hashlib
import json
import pathlib
import subprocess

PREFIX = "updates/FW-moving-heat-observable-20261015/"


def run(*args):
    return subprocess.check_output(["git", *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", required=True, help="Commit/tree/ref or INDEX")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = pathlib.Path(args.output)
    if out.exists():
        raise ValueError("Refusing to overwrite receipt: " + str(out))
    tree = (run("write-tree") if args.revision == "INDEX" else
            run("rev-parse", args.revision + "^{tree}")).decode().strip()
    objects = {}
    for row in run("ls-tree", "-r", "-z", tree).split(b"\0"):
        if row:
            meta, name = row.split(b"\t", 1)
            mode, kind, oid = meta.split()
            if kind == b"blob":
                objects[name.decode()] = oid.decode()
    proc = subprocess.Popen(["git", "cat-file", "--batch"], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    cache = {}

    def blob(path):
        oid = objects[path]
        if oid not in cache:
            proc.stdin.write((oid + "\n").encode())
            proc.stdin.flush()
            actual_oid, kind, count = proc.stdout.readline().split()
            assert actual_oid.decode() == oid and kind == b"blob"
            data = proc.stdout.read(int(count))
            assert len(data) == int(count) and proc.stdout.read(1) == b"\n"
            cache[oid] = data
        return cache[oid]

    def digest(data):
        return hashlib.sha256(data).hexdigest()

    source_path = PREFIX + "SOURCE_MANIFEST.json"
    derived_path = PREFIX + "DERIVED_MANIFEST.v0002.json"
    source = json.loads(blob(source_path))
    derived = json.loads(blob(derived_path))
    original_manifest = source["original_manifest"]
    assert digest(blob(original_manifest["path"])) == original_manifest["sha256"]
    freeze_ref = derived["source_freeze"]
    assert digest(blob(freeze_ref["path"])) == freeze_ref["sha256"]
    freeze = json.loads(blob(freeze_ref["path"]))
    assert freeze["files"] == derived["files"]
    groups = {}
    for label, manifest in [("supplied_originals_and_zip_members", source),
                            ("selected_internal_research", derived)]:
        total = 0
        for entry in manifest["files"]:
            data = blob(entry["path"])
            assert len(data) == entry["bytes"], entry["path"]
            assert digest(data) == entry["sha256"], entry["path"]
            total += len(data)
        groups[label] = {"files": len(manifest["files"]), "bytes": total,
                         "status": "ALL_GIT_BLOBS_MATCH_SHA256"}
    proc.stdin.close()
    assert proc.wait() == 0
    result = {"schema": "astra.fw.git-tree-evidence.v1", "revision": args.revision,
              "tree": tree, "status": "PASS", "groups": groups,
              "source_manifest_sha256": digest(blob(source_path)),
              "derived_manifest_sha256": digest(blob(derived_path)),
              "scope": "Exact Git-blob evidence integrity only; no scientific correctness or originality certification."}
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
