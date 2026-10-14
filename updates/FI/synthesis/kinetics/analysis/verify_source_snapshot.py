#!/usr/bin/env python3
"""Read-only source snapshot equality and NPZ-header safety audit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import zipfile

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WORKSPACE = ROOT.parent.parent
SOURCE = WORKSPACE / "work/FI-sources/kinetics"
PASTED = WORKSPACE / "work/FI-sources/kinetics_PASTED_SOURCE.txt"
SNAPSHOT = ROOT / "source_snapshot"


def describe(path: Path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def inspect_npz(path: Path):
    members = []
    with zipfile.ZipFile(path) as archive:
        for member in archive.namelist():
            if not member.endswith(".npy"):
                continue
            with archive.open(member) as stream:
                version = np.lib.format.read_magic(stream)
                reader = {
                    (1, 0): np.lib.format.read_array_header_1_0,
                    (2, 0): np.lib.format.read_array_header_2_0,
                    (3, 0): np.lib.format.read_array_header_2_0,
                }[version]
                shape, fortran, dtype = reader(stream)
            members.append({
                "member": member,
                "shape": list(shape),
                "dtype": str(dtype),
                "has_object_dtype": bool(dtype.hasobject),
                "fortran_order": bool(fortran),
            })
    return members


def main():
    source_files = sorted(p for p in SOURCE.rglob("*") if p.is_file())
    snapshot_files = sorted(
        p for p in SNAPSHOT.rglob("*") if p.is_file() and p.name != "PASTED_SOURCE.txt"
    )
    source_rel = {p.relative_to(SOURCE).as_posix(): describe(p) for p in source_files}
    snapshot_rel = {p.relative_to(SNAPSHOT).as_posix(): describe(p) for p in snapshot_files}
    if source_rel != snapshot_rel:
        missing = sorted(set(source_rel) - set(snapshot_rel))
        extra = sorted(set(snapshot_rel) - set(source_rel))
        changed = sorted(k for k in set(source_rel) & set(snapshot_rel) if source_rel[k] != snapshot_rel[k])
        raise AssertionError({"missing": missing, "extra": extra, "changed": changed})
    pasted_source = describe(PASTED)
    pasted_snapshot = describe(SNAPSHOT / "PASTED_SOURCE.txt")
    if pasted_source != pasted_snapshot:
        raise AssertionError("pasted source snapshot differs from input")

    npz_files = sorted(p for p in SNAPSHOT.rglob("*.npz") if p.is_file())
    npz_inventory = {
        p.relative_to(SNAPSHOT).as_posix(): inspect_npz(p) for p in npz_files
    }
    objects = [
        f"{path}:{member['member']}"
        for path, members in npz_inventory.items()
        for member in members
        if member["has_object_dtype"]
    ]
    if objects:
        raise AssertionError({"object_arrays": objects})

    source_audit_bytes = (SNAPSHOT / "audit.py").read_bytes()
    replica_audit_bytes = (ROOT / "replica/audit.py").read_bytes()
    original_loader = b"np.load(ROOT/(name+'.npz'))"
    safe_loader = b"np.load(ROOT/(name+'.npz'),allow_pickle=False)"
    if source_audit_bytes.count(original_loader) != 1:
        raise AssertionError("source replay loader shape changed; inspect before asserting replica scope")
    safe_audit_bytes = source_audit_bytes.replace(original_loader, safe_loader, 1)
    if replica_audit_bytes != safe_audit_bytes:
        raise AssertionError("replica audit.py contains changes beyond the explicit safe loader")
    audit_reverse_unchanged = describe(ROOT / "replica/audit_reverse.py") == describe(SNAPSHOT / "audit_reverse.py")
    if not audit_reverse_unchanged:
        raise AssertionError("audit_reverse.py was changed in the replay copy")

    result = {
        "source_files": len(source_files),
        "source_bytes": sum(p.stat().st_size for p in source_files),
        "pasted_source_bytes": PASTED.stat().st_size,
        "source_tree_exact_snapshot_match": True,
        "pasted_source_exact_snapshot_match": True,
        "npz_file_count": len(npz_files),
        "npz_array_count": sum(map(len, npz_inventory.values())),
        "all_npz_arrays_non_object": True,
        "npz_header_inventory": npz_inventory,
        "replica_audit_reverse_unchanged": audit_reverse_unchanged,
        "replica_audit_py_diff_scope": "the only source-to-replica difference is allow_pickle=False in the replay loader",
        "replica_audit_py_source_sha256": describe(SNAPSHOT / "audit.py")["sha256"],
        "replica_audit_py_bytes": describe(SNAPSHOT / "audit.py")["bytes"],
        "replica_audit_py_sha256": describe(ROOT / "replica/audit.py")["sha256"],
        "replica_audit_py_bytes_actual": describe(ROOT / "replica/audit.py")["bytes"],
        "snapshot_sha256_inventory": source_rel,
    }
    out = HERE / "source_integrity.json"
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in [
        "source_files", "source_bytes", "pasted_source_bytes",
        "source_tree_exact_snapshot_match", "pasted_source_exact_snapshot_match",
        "npz_file_count", "npz_array_count", "all_npz_arrays_non_object",
        "replica_audit_reverse_unchanged", "replica_audit_py_diff_scope",
    ]}, indent=2))


if __name__ == "__main__":
    main()
