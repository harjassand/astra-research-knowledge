#!/usr/bin/env python3
"""Preserve all predecessor bytes and build the completed twelfth snapshot."""
from __future__ import annotations
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import zipfile

PREDECESSOR_NAME = "Astra_P1_Spatial_Law_and_Passive_Record_20261030.zip"
PREDECESSOR_SHA = "04153f36f7726ce689546abbdd472a02913694ce618ac8546511254042082923"
OUTPUT_NAME = "Astra_P1_Reachable_Ensemble_Learning_and_Information_Cost_20261030.zip"
MANIFEST_NAME = "TWELFTH_CONTINUATION_MANIFEST.json"
PREFIX = "new_science/continuation12_20261030"
RECEIVING_INPUTS_SHA = "e41def41c795472001810704c498c0ef5b229d38ed078c20a4dbecc2c180c88a"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe(name):
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or "\\" in name:
        raise ValueError(f"Unsafe relative path: {name}")
    return path


def describe(path, root):
    data = path.read_bytes()
    return {"path": path.relative_to(root).as_posix(), "bytes": len(data),
            "sha256": digest(data)}


def verify_entry(base, name, sha, size=None):
    path = base.joinpath(*safe(name).parts)
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"Missing/nonregular input: {path}")
    data = path.read_bytes()
    if digest(data) != sha or (size is not None and len(data) != size):
        raise ValueError(f"Pinned input changed: {path}")


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predecessor", type=Path, default=root.parent / PREDECESSOR_NAME)
    parser.add_argument("--output", type=Path, default=root.parent / OUTPUT_NAME)
    args = parser.parse_args()
    predecessor, output = args.predecessor.resolve(), args.output.resolve()
    if output == predecessor or output == root or root in output.parents:
        raise ValueError("Create a separate new archive outside the research tree.")
    if output.exists():
        raise FileExistsError(f"New snapshot path already exists: {output}")
    if digest(predecessor.read_bytes()) != PREDECESSOR_SHA:
        raise ValueError("Predecessor archive identity mismatch.")

    previous, names = [], set()
    with zipfile.ZipFile(predecessor) as archive:
        infos = [i for i in archive.infolist() if not i.is_dir()]
        if len(infos) != 721:
            raise ValueError("Expected exactly 721 predecessor files.")
        for info in infos:
            relative = safe(info.filename)
            if info.filename in names:
                raise ValueError("Duplicate predecessor path.")
            names.add(info.filename)
            path = root.joinpath(*relative.parts)
            if not path.is_file() or path.is_symlink():
                raise ValueError(f"Missing predecessor: {info.filename}")
            original = archive.read(info)
            if path.read_bytes() != original:
                raise ValueError(f"Predecessor changed: {info.filename}")
            previous.append({"path": info.filename, "bytes": len(original),
                             "sha256": digest(original)})

    current = root / PREFIX
    receipt_path = current / "ROOT_RECEIVING_INPUTS.json"
    if digest(receipt_path.read_bytes()) != RECEIVING_INPUTS_SHA:
        raise ValueError("Root receiving manifest changed.")
    receipt = json.loads(receipt_path.read_text())
    for item in receipt["files"]:
        verify_entry(current, item["file"], item["sha256"], item["bytes"])

    role_receipts = []
    for role in ["physical_mechanism", "record_geometry"]:
        path = current / role / "MANIFEST.json"
        data = json.loads(path.read_text())
        for item in data["files"]:
            verify_entry(path.parent, item.get("file", item.get("path")),
                         item["sha256"], item["bytes"])
        role_receipts.append({**describe(path, root), "entries_verified": len(data["files"])})
    record_path = current / "record_geometry/RECEIVING_MANIFEST.json"
    record = json.loads(record_path.read_text())
    for item in record["reviewed_inputs"]:
        verify_entry(record_path.parent, item["snapshot"], item["reviewed_sha256"],
                     item["snapshot_bytes"])
    for item in record["new_authored_files"]:
        verify_entry(record_path.parent, item["file"], item["sha256"], item["bytes"])
    for name, sha in record["preserved_independent_alternative"].items():
        verify_entry(record_path.parent, name, sha)
    role_receipts.append({**describe(record_path, root), "entries_verified":
        len(record["reviewed_inputs"]) + len(record["new_authored_files"])
        + len(record["preserved_independent_alternative"])})

    files = []
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"Unexpected symlink: {path}")
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if relative == MANIFEST_NAME:
            continue
        if "__pycache__" in path.parts and relative not in names:
            continue
        files.append(path)
    files.sort(key=lambda p: p.relative_to(root).as_posix())
    additions = [describe(p, root) for p in files if p.relative_to(root).as_posix() not in names]
    manifest = {
        "schema": "astra_p1.full_snapshot.v12",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "research_directory": PREFIX,
        "role": "Astra P1; same model and existing two complementary roles",
        "predecessor": {"filename": predecessor.name, "sha256": PREDECESSOR_SHA,
                        "archive_bytes": predecessor.stat().st_size,
                        "files_verified_byte_for_byte": len(previous)},
        "unchanged_predecessor_files": sorted(previous, key=lambda x: x["path"]),
        "new_files": additions,
        "root_receiving_manifest": {**describe(receipt_path, root),
                                    "entries_verified": len(receipt["files"])},
        "verified_role_manifests": role_receipts,
        "file_count_including_this_manifest": len(files) + 1,
        "manifest_scope": "All other archive files are hashed; the archive hash is emitted by the builder.",
        "completed_at_declared_interfaces": [
            "chronologically acquired full hidden-ensemble distance for reachable preparations",
            "all-common-future receiver and literal discriminating continuation",
            "finite retained-prefix instrument without conditional hidden copying",
            "weighted adjoints, actual normalization, source and repeat scope",
            "continuous-observation adaptive active-time lower bound with initializer correction",
            "same-source all-available-future versus full-hidden-state metric separation",
            "infinite-rank preparation corollary without finite predictive closure",
            "one executed fresh-validation learning run and corrected fixed-gate deployment selector",
            "strong ordinary response learner and independent sparse-load construction",
            "actual pinned reviews, failed claims and binding corrections"
        ],
        "binding_corrections": [
            "BINDING_RECEIVING_CLARIFICATIONS.md",
            "CALIBRATION_HISTORY_CORRECTION_AND_DEPLOYMENT_RULE.md",
            "physical_mechanism/receiving_review/ADAPTIVE_INFORMATION_COST_RECEIVING_REVIEW.md",
            "record_geometry/receiving_review/ENSEMBLE_ECHO_RECORD_AND_WEIGHTED_RECEIVING_REVIEW.md",
            "record_geometry/receiving_review/ENSEMBLE_LEARNING_RUN_RECEIVING_REVIEW.md",
            "ROOT_RECEIVING_RECEIPT.md"
        ],
        "not_established": [
            "historical priority or civilisation-scale impact",
            "manufactured apparatus or measured complete physical cycle",
            "practical efficiency or total-work advantage over ordinary controllers",
            "hidden initialization or apparatus-record isolation without a supplier",
            "arbitrary hidden-input tomography, uniform channel equivalence or unrelated-device comparison",
            "unconditional calibration bound obtained by adding alpha to one observed random certificate"
        ]
    }
    manifest_path = root / MANIFEST_NAME
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    partial = output.with_suffix(output.suffix + ".partial")
    with zipfile.ZipFile(partial, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files + [manifest_path]:
            archive.write(path, path.relative_to(root).as_posix())
    with zipfile.ZipFile(partial) as archive:
        bad = archive.testzip()
        if bad is not None or len(archive.namelist()) != len(files) + 1:
            raise ValueError(f"Archive integrity failure: {bad}")
    partial.rename(output)
    result = {"archive": str(output), "bytes": output.stat().st_size,
              "sha256": digest(output.read_bytes()),
              "predecessor_files_verified": len(previous),
              "new_files_excluding_manifest": len(additions), "total_files": len(files) + 1,
              "root_receiving_inputs_verified": len(receipt["files"]),
              "role_manifest_entries_verified": sum(x["entries_verified"] for x in role_receipts),
              "archive_crc_check": "passed"}
    (root.parent / "TWELFTH_SNAPSHOT_BUILD_RESULT.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
