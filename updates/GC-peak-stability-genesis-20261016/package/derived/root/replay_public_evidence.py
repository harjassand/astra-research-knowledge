#!/usr/bin/env python3
"""Replay the public GC source and selected bounded derived checkers.

This orchestrator uses only the Python standard library. It verifies the four
source ZIPs and all 82 manifest members, rehydrates inputs and frozen derived
checkers into a disposable canonical scratch tree, runs bounded readers only,
and removes the tree on exit. It never calls a source candidate solver or the
Schlogl full-packet wrapper.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import zipfile
import xml.etree.ElementTree as ET

SCHEMA = "astra.gc-public-replay.v1"
ARCHIVE_ONLY_SUFFIX = ".npz"
ARCHIVE_ONLY_MIN_BYTES = 10_000_000
KNOWN_STALE_REPORT_EXPECTED = "fd899d6f5665d95e3e6ca3964f8b280f2464d6116981f91342ec7a3e2fe3496b"
KNOWN_STALE_REPORT_ACTUAL = "128a1e7937204da2ecb1795dffcbc3d1f569ccad657637a2f05d01696f1f222b"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path, relative: str | None = None) -> dict:
    return {
        "path": relative if relative is not None else str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def safe_posix_path(value: str, *, allow_directory_slash: bool = False) -> PurePosixPath:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ValueError(f"unsafe path spelling: {value!r}")
    if allow_directory_slash:
        value = value.rstrip("/")
        if not value:
            raise ValueError("empty ZIP path")
    p = PurePosixPath(value)
    if p.is_absolute() or any(part in ("", ".", "..") for part in p.parts):
        raise ValueError(f"unsafe relative path: {value!r}")
    if p.parts and ":" in p.parts[0]:
        raise ValueError(f"drive-like path rejected: {value!r}")
    return p


def contained_path(root: Path, relative: str) -> Path:
    p = safe_posix_path(relative)
    candidate = root.joinpath(*p.parts)
    resolved_root = root.resolve()
    resolved = candidate.resolve(strict=False)
    if resolved != resolved_root and resolved_root not in resolved.parents:
        raise ValueError(f"path escapes package root: {relative}")
    return candidate


def package_root_from_script() -> Path:
    start = Path(__file__).resolve().parent
    for candidate in (start, *start.parents):
        if (candidate / "originals").is_dir() and any(
            (candidate / name).is_file()
            for name in ("SOURCE_PUBLICATION.json", "SOURCE_MANIFEST.supplied.json", "SOURCE_MANIFEST.json")
        ):
            return candidate
    raise FileNotFoundError("could not locate package root; pass --package-root")


def locate_existing(root: Path, relative_candidates: tuple[str, ...], label: str) -> tuple[Path, str]:
    for relative in relative_candidates:
        path = contained_path(root, relative)
        if path.is_file() and not path.is_symlink():
            return path, relative
    raise FileNotFoundError(f"missing {label}; tried {relative_candidates}")


def locate_worker(root: Path, name: str) -> tuple[Path, str]:
    for rel in (f"workers/{name}", f"derived/workers/{name}"):
        p = contained_path(root, rel)
        if p.is_dir() and not p.is_symlink():
            return p, rel
    raise FileNotFoundError(f"missing worker directory {name}")


def locate_root_dir(root: Path) -> tuple[Path, str]:
    for rel in ("root", "derived/root"):
        p = contained_path(root, rel)
        if p.is_dir() and not p.is_symlink():
            return p, rel
    raise FileNotFoundError("missing root evidence directory")


def read_source_state(root: Path) -> dict:
    supplied_candidates = [root / "SOURCE_MANIFEST.supplied.json", root / "SOURCE_MANIFEST.json"]
    supplied_path = next((p for p in supplied_candidates if p.is_file()), None)
    publication_path = root / "SOURCE_PUBLICATION.json"
    if supplied_path is None and not publication_path.is_file():
        raise FileNotFoundError("need SOURCE_MANIFEST(.supplied).json or SOURCE_PUBLICATION.json")

    supplied = json.loads(supplied_path.read_text()) if supplied_path else None
    publication = json.loads(publication_path.read_text()) if publication_path.is_file() else None
    if supplied is not None:
        members = supplied.get("members")
        base_revision = supplied.get("base_revision")
        if not isinstance(members, list):
            raise ValueError("supplied source manifest has no member list")
    else:
        members = publication.get("members")
        base_revision = publication.get("base_revision")
        if not isinstance(members, list):
            raise ValueError("source publication has no member list")

    rows = []
    seen_paths = set()
    for raw in members:
        row = dict(raw)
        for field in ("archive", "member", "path", "bytes", "sha256", "archive_sha256"):
            if field not in row:
                raise ValueError(f"source member lacks {field}: {row}")
        if Path(row["archive"]).name != row["archive"] or "/" in row["archive"] or "\\" in row["archive"]:
            raise ValueError(f"unsafe archive name: {row['archive']!r}")
        safe_posix_path(row["member"])
        safe_posix_path(row["path"])
        if not row["path"].startswith("originals/"):
            raise ValueError(f"source expansion must stay under originals/: {row['path']}")
        if row["path"] in seen_paths:
            raise ValueError(f"duplicate source expansion path: {row['path']}")
        seen_paths.add(row["path"])
        if not isinstance(row["bytes"], int) or row["bytes"] < 0:
            raise ValueError(f"invalid source member byte count: {row}")
        for digest_field in ("sha256", "archive_sha256"):
            value = row[digest_field]
            if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
                raise ValueError(f"invalid {digest_field}: {value!r}")
        rows.append(row)

    names = sorted({row["archive"] for row in rows})
    if len(rows) != 82 or len(names) != 4:
        raise ValueError(f"expected 82 members in four source ZIPs, got {len(rows)} / {len(names)}")
    if supplied is not None and supplied.get("archives") not in (None, 4):
        raise ValueError("unexpected source archive count")

    publication_archives = {}
    if publication is not None:
        for item in publication.get("archives", []):
            name = Path(item["path"]).name
            if name in publication_archives:
                raise ValueError(f"duplicate archive locator in SOURCE_PUBLICATION.json: {name}")
            if not item["path"].replace("\\", "/").endswith("/package/originals/" + name):
                raise ValueError(f"unrecognized published archive locator: {item['path']}")
            publication_archives[name] = item
        if set(publication_archives) != set(names):
            raise ValueError("SOURCE_PUBLICATION archive list does not match source manifest")
        pub_members = publication.get("members", [])
        if len(pub_members) != len(rows):
            raise ValueError("SOURCE_PUBLICATION member count does not match source manifest")
        pub_by_path = {x.get("path"): x for x in pub_members}
        for row in rows:
            p = pub_by_path.get(row["path"])
            if p is None or any(p.get(k) != row.get(k) for k in ("archive", "member", "bytes", "sha256", "archive_sha256")):
                raise ValueError(f"SOURCE_PUBLICATION row differs from supplied manifest: {row['path']}")
            pub_archive = publication_archives[row["archive"]]
            if pub_archive.get("sha256") != row["archive_sha256"]:
                raise ValueError(f"SOURCE_PUBLICATION archive hash disagrees: {row['archive']}")
            if p.get("published_archive_path") != pub_archive.get("path"):
                raise ValueError(f"member archive locator disagrees: {row['archive']}")
            expected_expanded = row["path"]
            locator = p.get("published_expanded_path")
            if p.get("publication") == "exact_archive_and_expanded_member":
                if not isinstance(locator, str) or not locator.replace("\\", "/").endswith("/package/" + expected_expanded):
                    raise ValueError(f"invalid published expansion locator: {row['path']}")
            elif p.get("publication") != "exact_archive_member_only" or locator is not None:
                raise ValueError(f"unknown source publication mode for {row['path']}")

    archive_hashes = {}
    for row in rows:
        prior = archive_hashes.setdefault(row["archive"], row["archive_sha256"])
        if prior != row["archive_sha256"]:
            raise ValueError(f"inconsistent archive hash for {row['archive']}")
    return {
        "base_revision": base_revision,
        "members": rows,
        "archive_hashes": archive_hashes,
        "archive_names": names,
        "source_manifest_path": supplied_path.name if supplied_path else None,
        "source_manifest_sha256": sha256_file(supplied_path) if supplied_path else None,
        "publication_sha256": sha256_file(publication_path) if publication_path.is_file() else None,
        "publication": publication,
        "supplied": supplied,
    }


def validate_zip_name(info: zipfile.ZipInfo) -> str:
    name = info.filename
    if info.is_dir():
        safe_posix_path(name, allow_directory_slash=True)
        return name
    safe_posix_path(name)
    mode = (info.external_attr >> 16) & 0xFFFF
    if stat.S_ISLNK(mode):
        raise ValueError(f"symlink ZIP member rejected: {name}")
    return name


def iter_member_chunks(zf: zipfile.ZipFile, name: str):
    with zf.open(name, "r") as stream:
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            yield chunk


def verify_archives_and_rehydrate(root: Path, state: dict, scratch: Path, strict_public_layout: bool) -> dict:
    rows_by_archive: dict[str, list[dict]] = {name: [] for name in state["archive_names"]}
    for row in state["members"]:
        rows_by_archive[row["archive"]].append(row)
    archive_records = []
    member_records = []
    archive_only = []
    extracted_paths = set()
    for row in state["members"]:
        if row["path"].lower().endswith(ARCHIVE_ONLY_SUFFIX) and row["bytes"] >= ARCHIVE_ONLY_MIN_BYTES:
            archive_only.append(row["path"])
    if len(archive_only) != 3:
        raise ValueError(f"expected three large archive-only NPZ members, got {len(archive_only)}")

    for name in state["archive_names"]:
        archive = contained_path(root, f"originals/{name}")
        if archive.is_symlink() or not archive.is_file():
            raise FileNotFoundError(f"missing regular source ZIP: {archive}")
        actual_archive_sha = sha256_file(archive)
        expected_archive_sha = state["archive_hashes"][name]
        if actual_archive_sha != expected_archive_sha:
            raise ValueError(f"archive SHA-256 mismatch for {name}: {actual_archive_sha}")
        expected = {x["member"]: x for x in rows_by_archive[name]}
        with zipfile.ZipFile(archive, "r") as zf:
            infos = zf.infolist()
            actual_files = {}
            for info in infos:
                member_name = validate_zip_name(info)
                if info.is_dir():
                    continue
                if member_name in actual_files:
                    raise ValueError(f"duplicate ZIP member name in {name}: {member_name}")
                actual_files[member_name] = info
            if set(actual_files) != set(expected):
                raise ValueError(f"ZIP member set differs from source manifest for {name}")
            bad_crc = zf.testzip()
            if bad_crc is not None:
                raise ValueError(f"CRC failure in {name}: {bad_crc}")
            for member_name, row in expected.items():
                info = actual_files[member_name]
                if info.file_size != row["bytes"]:
                    raise ValueError(f"ZIP member byte count mismatch for {row['path']}")
                digest = hashlib.sha256()
                count = 0
                scratch_path = contained_path(scratch, row["path"])
                archive_only_member = row["path"] in archive_only
                if archive_only_member and strict_public_layout:
                    published = contained_path(root, row["path"])
                    if published.exists():
                        raise ValueError(f"large NPZ must remain archive-only in public package: {row['path']}")
                if not archive_only_member:
                    published = contained_path(root, row["path"])
                    if not published.is_file() or published.is_symlink():
                        raise FileNotFoundError(f"missing expanded source member: {row['path']}")
                    if sha256_file(published) != row["sha256"] or published.stat().st_size != row["bytes"]:
                        raise ValueError(f"expanded source member does not match ZIP manifest: {row['path']}")
                    if row["path"] in extracted_paths:
                        raise ValueError(f"duplicate scratch expansion path: {row['path']}")
                    scratch_path.parent.mkdir(parents=True, exist_ok=True)
                    out = scratch_path.open("wb")
                else:
                    out = None
                try:
                    for chunk in iter_member_chunks(zf, member_name):
                        digest.update(chunk)
                        count += len(chunk)
                        if out is not None:
                            out.write(chunk)
                finally:
                    if out is not None:
                        out.close()
                actual_member_sha = digest.hexdigest()
                if count != row["bytes"] or actual_member_sha != row["sha256"]:
                    raise ValueError(f"ZIP member hash/size mismatch for {row['path']}")
                if not archive_only_member:
                    extracted_paths.add(row["path"])
                    # Independent copy check binds the expanded convenience file to the ZIP.
                    if sha256_file(scratch_path) != row["sha256"]:
                        raise ValueError(f"rehydrated source member mismatch: {row['path']}")
                member_records.append({
                    "path": row["path"], "archive": name, "member": member_name,
                    "bytes": count, "sha256": actual_member_sha,
                    "rehydrated": not archive_only_member,
                    "archive_only_reason": "large NPZ excluded from expanded public tree" if archive_only_member else None,
                })
        archive_records.append({"path": f"originals/{name}", "bytes": archive.stat().st_size,
                               "sha256": actual_archive_sha, "zip_crc": "PASS"})

    # The three archive-only arrays are rehydrated in scratch only for the bounded
    # independent target verifier. They are never written to the published package.
    for row in state["members"]:
        if row["path"] not in archive_only:
            continue
        archive = contained_path(root, f"originals/{row['archive']}")
        scratch_path = contained_path(scratch, row["path"])
        scratch_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive, "r") as zf, zf.open(row["member"], "r") as src, scratch_path.open("wb") as dst:
            shutil.copyfileobj(src, dst, 1024 * 1024)
        if scratch_path.stat().st_size != row["bytes"] or sha256_file(scratch_path) != row["sha256"]:
            raise ValueError(f"scratch NPZ rehydration mismatch: {row['path']}")
    return {
        "archive_count": len(archive_records), "archives": archive_records,
        "member_count": len(member_records), "members": member_records,
        "expanded_count": len(extracted_paths), "archive_only_count": len(archive_only),
        "archive_only_members": archive_only,
        "scratch_npz_rehydration": "PASS; three NPZs exist only inside temporary scratch for bounded target check",
    }


def list_frozen_files(worker_dir: Path, manifest_name: str, worker_name: str) -> tuple[dict, list[dict]]:
    manifest_path = worker_dir / manifest_name
    data = json.loads(manifest_path.read_text())
    expected = []
    if worker_name == "gc_nonsep_genesis":
        items = data.get("files")
        if not isinstance(items, dict):
            raise ValueError("gc_nonsep_genesis FROZEN.json lacks files map")
        for name, digest in sorted(items.items()):
            safe_posix_path(name)
            expected.append({"name": name, "sha256": digest, "bytes": None})
    elif worker_name == "gc_control_adversary":
        items = data.get("files")
        if not isinstance(items, list):
            raise ValueError("gc_control_adversary FROZEN.json lacks file records")
        for item in items:
            name = item["name"]
            safe_posix_path(name)
            expected.append({"name": name, "sha256": item["sha256"], "bytes": item.get("bytes")})
    elif worker_name == "gc_nonsep_adversary":
        items = data.get("files")
        if not isinstance(items, dict):
            raise ValueError(f"{worker_name} FROZEN.json lacks files map")
        for name, digest in sorted(items.items()):
            safe_posix_path(name)
            expected.append({"name": name, "sha256": digest, "bytes": None})
    elif worker_name in ("gc_peak_genesis", "gc_kinetic_adversary"):
        items = data.get("files") if worker_name == "gc_peak_genesis" else data.get("outputs")
        if not isinstance(items, list):
            raise ValueError(f"{worker_name} freeze manifest lacks file list")
        for item in items:
            name = Path(item["path"]).name
            safe_posix_path(name)
            expected.append({"name": name, "sha256": item["sha256"], "bytes": item.get("bytes")})
    else:
        raise ValueError(f"unsupported frozen file schema for {worker_name}")
    names = [x["name"] for x in expected]
    if len(names) != len(set(names)):
        raise ValueError(f"duplicate basenames in {worker_name} freeze manifest")
    for item in expected:
        path = worker_dir / item["name"]
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError(f"missing pinned worker file: {worker_name}/{item['name']}")
        actual_sha = sha256_file(path)
        if actual_sha != item["sha256"]:
            raise ValueError(f"frozen worker hash mismatch: {worker_name}/{item['name']}")
        if item["bytes"] is not None and path.stat().st_size != item["bytes"]:
            raise ValueError(f"frozen worker byte count mismatch: {worker_name}/{item['name']}")
        item["bytes"] = path.stat().st_size
    return data, expected


def list_kinetic_goal_files(worker_dir: Path) -> tuple[dict, list[dict]]:
    """Validate required kinetic-goal artifacts, excluding transient progress snapshots."""
    manifest_path = worker_dir / "FROZEN.json"
    data = json.loads(manifest_path.read_text())
    if data.get("status") != "FROZEN" or data.get("worker") != "gc_kinetic_goal":
        raise ValueError("gc_kinetic_goal FROZEN.json identity/status mismatch")
    rows = data.get("all_required_artifacts")
    if not isinstance(rows, list) or not rows:
        raise ValueError("gc_kinetic_goal FROZEN.json lacks all_required_artifacts")
    result = []
    seen = set()
    for row in rows:
        original_path = row.get("path")
        if not isinstance(original_path, str):
            raise ValueError("kinetic goal artifact has no original path")
        name = Path(original_path).name
        safe_posix_path(name)
        if name.endswith(".progress.json"):
            continue
        if name in seen:
            raise ValueError(f"duplicate basename in kinetic goal freeze: {name}")
        seen.add(name)
        expected_sha = row.get("sha256")
        expected_bytes = row.get("bytes")
        if not isinstance(expected_sha, str) or not re.fullmatch(r"[0-9a-f]{64}", expected_sha):
            raise ValueError(f"invalid kinetic goal SHA-256 for {name}")
        if not isinstance(expected_bytes, int) or expected_bytes < 0:
            raise ValueError(f"invalid kinetic goal byte count for {name}")
        path = worker_dir / name
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError(f"missing pinned kinetic goal artifact: {name}")
        if path.stat().st_size != expected_bytes or sha256_file(path) != expected_sha:
            raise ValueError(f"kinetic goal freeze mismatch: {name}")
        result.append({"name": name, "sha256": expected_sha, "bytes": expected_bytes,
                       "frozen_source_path": original_path})
    return data, result


def copy_verified_file(source: Path, destination: Path, expected_sha: str | None = None) -> dict:
    if not source.is_file() or source.is_symlink():
        raise FileNotFoundError(f"not a regular file: {source}")
    actual_sha = sha256_file(source)
    if expected_sha is not None and actual_sha != expected_sha:
        raise ValueError(f"source changed during staging: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    copied_sha = sha256_file(destination)
    if copied_sha != actual_sha:
        raise ValueError(f"scratch copy mismatch: {source}")
    return {"bytes": destination.stat().st_size, "sha256": copied_sha}


def source_root_files(root: Path, source_state: dict) -> list[dict]:
    result = []
    for name in ("SOURCE_PUBLICATION.json", "SOURCE_MANIFEST.supplied.json", "SOURCE_MANIFEST.json"):
        p = root / name
        if p.is_file():
            result.append(file_record(p, name))
    readme = root / "originals" / "README.md"
    if readme.is_file() and not readme.is_symlink():
        result.append(file_record(readme, "originals/README.md"))
    for name in source_state["archive_names"]:
        p = contained_path(root, f"originals/{name}")
        result.append(file_record(p, f"originals/{name}"))
    for row in source_state["members"]:
        # All 79 non-NPZ member expansions are public convenience files.
        if not (row["path"].lower().endswith(ARCHIVE_ONLY_SUFFIX) and row["bytes"] >= ARCHIVE_ONLY_MIN_BYTES):
            p = contained_path(root, row["path"])
            result.append(file_record(p, row["path"]))
    return result


def selected_derived_files(root: Path) -> tuple[list[dict], dict]:
    selected = []
    locations = {}
    for worker_name, manifest_name in (
        ("gc_nonsep_genesis", "FROZEN.json"),
        ("gc_nonsep_adversary", "FROZEN.json"),
        ("gc_control_adversary", "FROZEN.json"),
        ("gc_peak_genesis", "FROZEN_MANIFEST.json"),
        ("gc_kinetic_adversary", "FROZEN.json"),
    ):
        source_dir, source_rel = locate_worker(root, worker_name)
        freeze, expected = list_frozen_files(source_dir, manifest_name, worker_name)
        manifest_path = source_dir / manifest_name
        selected.append(file_record(manifest_path, f"{source_rel}/{manifest_name}"))
        for item in expected:
            selected.append(file_record(source_dir / item["name"], f"{source_rel}/{item['name']}"))
        locations[worker_name] = {"relative": source_rel, "manifest": manifest_name,
                                  "expected": expected, "status": freeze.get("status")}

    # Select and verify every required kinetic-goal artifact except transient
    # progress snapshots. This includes the checker and its saved JSON/NPZ inputs.
    kinetic_goal, kg_rel = locate_worker(root, "gc_kinetic_goal")
    kg_freeze, kg_expected = list_kinetic_goal_files(kinetic_goal)
    kg_names = [item["name"] for item in kg_expected]
    kg_files = []
    kg_manifest_record = file_record(kinetic_goal / "FROZEN.json", f"{kg_rel}/FROZEN.json")
    selected.append(kg_manifest_record)
    for name in kg_names:
        p = kinetic_goal / name
        expected = next(x for x in kg_expected if x["name"] == name)
        record = file_record(p, f"{kg_rel}/{name}")
        if record["sha256"] != expected["sha256"] or record["bytes"] != expected["bytes"]:
            raise ValueError(f"kinetic goal changed while selecting: {name}")
        kg_files.append(record)
        selected.append(kg_files[-1])
    locations["gc_kinetic_goal"] = {
        "relative": kg_rel, "manifest": kg_manifest_record,
        "status": kg_freeze.get("status"), "files": kg_files,
        "excluded_progress_files": sorted(Path(x["path"]).name
                                           for x in kg_freeze.get("all_required_artifacts", [])
                                           if Path(x.get("path", "")).name.endswith(".progress.json")),
    }

    cat, cat_rel = locate_worker(root, "gc_catalysis_genesis")
    cat_manifest = json.loads((cat / "FROZEN.json").read_text())
    excluded = {"acquire_and_analyze.py", "validate_and_acquire_prior.py", "verify_and_freeze.py"}
    cat_files = []
    for item in cat_manifest.get("files", []):
        name = Path(item["path"]).name
        if name in excluded:
            continue
        p = cat / name
        if not p.is_file() or p.is_symlink():
            raise FileNotFoundError(f"missing catalysis authored pack file: {name}")
        if sha256_file(p) != item["sha256"] or p.stat().st_size != item["bytes"]:
            raise ValueError(f"catalysis frozen file mismatch: {name}")
        record = file_record(p, f"{cat_rel}/{name}")
        cat_files.append(record)
        selected.append(record)
    selected.append(file_record(cat / "FROZEN.json", f"{cat_rel}/FROZEN.json"))
    locations["gc_catalysis_genesis"] = {
        "relative": cat_rel, "status": cat_manifest.get("status"),
        "included": cat_files, "excluded_acquisition_programs": sorted(excluded),
        "producer_model_checker": "electrical_and_fixed_model.py requires external_excluded_from_publication/final_SIFig7.xlsx; preserved as unavailable input, not run",
    }

    root_dir, root_rel = locate_root_dir(root)
    root_assets = ["check_first_slab_target.py", "FIRST_SLAB_TARGET_CERTIFICATE.json",
                   "STOPPED_TARGET_FIRST_SLAB.md", "SCIENTIFIC_SYNTHESIS.md", "WORKER_DEPLOYMENT.json",
                   "ROOT_PROOF_SOURCE_PINS.json"]
    root_records = []
    for name in root_assets:
        p = root_dir / name
        if p.is_file() and not p.is_symlink():
            record = file_record(p, f"{root_rel}/{name}")
            root_records.append(record)
            selected.append(record)
    if not any(Path(x["path"]).name == "check_first_slab_target.py" for x in root_records):
        raise FileNotFoundError("root first-slab checker is missing")
    if not any(Path(x["path"]).name == "FIRST_SLAB_TARGET_CERTIFICATE.json" for x in root_records):
        raise FileNotFoundError("root first-slab certificate is missing")
    locations["root"] = {"relative": root_rel, "assets": root_records}

    # Keep the earlier bounded identity report and receipts as immutable context.
    identity, identity_rel = locate_worker(root, "gc_identity_replay")
    identity_files = []
    for p in sorted(identity.rglob("*")):
        if p.is_file() and not p.is_symlink():
            rel = p.relative_to(identity).as_posix()
            if Path(rel).name.startswith("FROZEN_FOLLOWUP"):
                continue
            rec = file_record(p, f"{identity_rel}/{rel}")
            identity_files.append(rec)
            selected.append(rec)
    locations["gc_identity_replay_existing"] = {"relative": identity_rel, "files": identity_files}

    script = Path(__file__).resolve()
    script_rel = script.relative_to(root.resolve()).as_posix()
    selected.append(file_record(script, script_rel))
    locations["replay_script"] = {"path": script_rel, "sha256": sha256_file(script)}
    # Avoid duplicate records when a selected report is also one of the pinned files.
    dedup = {}
    for item in selected:
        dedup[item["path"]] = item
    return [dedup[k] for k in sorted(dedup)], locations


def build_publication_plan(root: Path, state: dict) -> dict:
    derived, locations = selected_derived_files(root)
    source_records = source_root_files(root, state)
    return {
        "schema": SCHEMA + ".plan",
        "base_revision": state["base_revision"],
        "source_manifests": {
            "supplied_manifest": state["source_manifest_path"],
            "supplied_manifest_sha256": state["source_manifest_sha256"],
            "publication_sha256": state["publication_sha256"],
        },
        "source_counts": {"archives": 4, "members": 82, "expanded_public_members": 79,
                           "archive_only_large_npz_members": 3},
        "source_files": source_records,
        "derived_files": derived,
        "replay_locations": locations,
        "ephemeral_relocations": [
            {
                "path": "workers/gc_nonsep_genesis/check_exact.py",
                "literal": "/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016",
                "scratch_action": "Set W=ROOT and remove the pinned git-show source lookup block only; leave the exact arithmetic/check body unchanged.",
            },
            {
                "path": "workers/gc_peak_genesis/FROZEN_MANIFEST.json and workers/gc_kinetic_adversary/FROZEN.json",
                "literal": "absolute R paths in frozen file/source records",
                "scratch_action": "Treat as provenance data; resolve frozen output names by basename and resolve source inputs only through SOURCE_MANIFEST/SOURCE_PUBLICATION. Do not rewrite either manifest.",
            },
            {
                "path": "workers/gc_kinetic_goal/FROZEN.json and all_required_artifacts",
                "literal": "absolute source input paths in saved JSON receipts",
                "scratch_action": "Verify required artifacts by safe basename and recorded SHA/size, omit progress snapshots, keep source receipts byte-identical, and invoke verify_cluster.py with package-relative rehydrated inputs. Ignore only path/runtime-only fields when comparing replay output.",
            },
            {
                "path": "workers/gc_catalysis_genesis/verify_and_freeze.py and root/preserve_inputs.py",
                "literal": "/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016",
                "scratch_action": "Excluded from replay/public executable selection; they read/write the local worktree and are not run.",
            },
        ],
        "excluded_from_replay": [
            "original producer Schlogl verify_packet.py wrapper and solver/candidate constructors",
            "gc_catalysis_genesis acquisition and git-fetch programs",
            "external fulltexts/clones and external_excluded_from_publication workbooks",
            "three large source NPZ expanded copies in the published tree",
            "kinetic-goal .progress.json snapshots listed in FROZEN.json",
        ],
    }


def snapshot_selected_files(root: Path, records: list[dict]) -> list[dict]:
    snapshot = []
    for record in records:
        relative = record["path"]
        path = contained_path(root, relative)
        if not path.is_file() or path.is_symlink():
            raise FileNotFoundError(f"selected package file disappeared: {relative}")
        snapshot.append(file_record(path, relative))
    return sorted(snapshot, key=lambda x: x["path"])


def freeze_worker_into_scratch(root: Path, scratch: Path, worker_name: str, manifest_name: str) -> tuple[Path, dict, list[dict]]:
    source_dir, _ = locate_worker(root, worker_name)
    freeze, expected = list_frozen_files(source_dir, manifest_name, worker_name)
    dest_dir = scratch / "workers" / worker_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    copy_verified_file(source_dir / manifest_name, dest_dir / manifest_name)
    for item in expected:
        copy_verified_file(source_dir / item["name"], dest_dir / item["name"], item["sha256"])
    return dest_dir, freeze, expected


def freeze_additional_into_scratch(root: Path, scratch: Path, worker_name: str, names: list[str]) -> Path:
    source_dir, _ = locate_worker(root, worker_name)
    dest_dir = scratch / "workers" / worker_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    if worker_name == "gc_catalysis_genesis":
        copy_verified_file(source_dir / "FROZEN.json", dest_dir / "FROZEN.json")
        data = json.loads((source_dir / "FROZEN.json").read_text())
        expected = {Path(x["path"]).name: x["sha256"] for x in data.get("files", [])}
        for name in names:
            copy_verified_file(source_dir / name, dest_dir / name, expected.get(name))
    elif worker_name == "gc_kinetic_goal":
        _, rows = list_kinetic_goal_files(source_dir)
        expected = {x["name"]: x["sha256"] for x in rows}
        copy_verified_file(source_dir / "FROZEN.json", dest_dir / "FROZEN.json")
        for name in names:
            if name not in expected:
                raise ValueError(f"unmanifested kinetic goal replay file: {name}")
            copy_verified_file(source_dir / name, dest_dir / name, expected[name])
    else:
        for name in names:
            copy_verified_file(source_dir / name, dest_dir / name)
    return dest_dir


def freeze_root_into_scratch(root: Path, scratch: Path) -> Path:
    source_root, _ = locate_root_dir(root)
    dest = scratch / "root"
    dest.mkdir(parents=True, exist_ok=True)
    for name in ("check_first_slab_target.py", "FIRST_SLAB_TARGET_CERTIFICATE.json", "STOPPED_TARGET_FIRST_SLAB.md",
                 "ROOT_PROOF_SOURCE_PINS.json"):
        copy_verified_file(source_root / name, dest / name)
    return dest


def run_command(label: str, command: list[str], cwd: Path, timeout: int, env: dict) -> dict:
    start = time.monotonic()
    try:
        result = subprocess.run(command, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=timeout, check=False)
        return {"check": label, "exit_code": result.returncode,
                "elapsed_seconds": round(time.monotonic() - start, 6),
                "stdout": result.stdout, "timed_out": False}
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", "replace")
        return {"check": label, "exit_code": None,
                "elapsed_seconds": round(time.monotonic() - start, 6),
                "stdout": output + "\nTIMEOUT", "timed_out": True}


def patch_nonsep_genesis_checker(path: Path) -> dict:
    original = path.read_text()
    old_path = "W = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016')"
    if original.count(old_path) != 1:
        raise ValueError("unexpected gc_nonsep_genesis checker W path occurrence")
    patched = original.replace(old_path, "W = ROOT")
    pattern = re.compile(r"(?ms)^paths=\[\n.*?(?=^for path in \[ROOT/'originals/stability/PROOF_NOTE\.md)")
    patched, count = pattern.subn("source_records=[]\n", patched, count=1)
    if count != 1 or "['git','show'" in patched or "cwd=W" in patched:
        raise ValueError("failed to remove only the non-portable prior-pin Git lookup")
    path.write_text(patched)
    return {"source_sha256": sha256_bytes(original.encode()),
            "ephemeral_replay_sha256": sha256_file(path),
            "patch": "W reassigned to copied scratch root; removed only the pinned git-show provenance lookup. Exact arithmetic and supplied-input checks are unchanged."}


def check_source_manifest_known_failure(scratch: Path) -> dict:
    manifest = scratch / "originals/kinetic/schlogl_first_slab_packet/verification/SOURCE_MANIFEST.sha256"
    report = scratch / "originals/kinetic/schlogl_first_slab_packet/verification/REPORT.md"
    expected = None
    for line in manifest.read_text().splitlines():
        parts = line.strip().split()
        if len(parts) >= 2 and Path(parts[-1].lstrip("*" )).name == "REPORT.md":
            expected = parts[0]
            break
    if expected is None:
        raise ValueError("known kinetic SOURCE_MANIFEST has no REPORT.md binding")
    actual = sha256_file(report)
    record = {"manifest": "originals/kinetic/schlogl_first_slab_packet/verification/SOURCE_MANIFEST.sha256",
              "member": "originals/kinetic/schlogl_first_slab_packet/verification/REPORT.md",
              "expected_sha256": expected, "actual_sha256": actual}
    if expected != KNOWN_STALE_REPORT_EXPECTED or actual != KNOWN_STALE_REPORT_ACTUAL:
        record["status"] = "CHANGED_FROM_KNOWN_STALE_BINDING"
        raise ValueError(f"kinetic stale binding differs from preserved known mismatch: {record}")
    record["status"] = "KNOWN_STALE_BINDING_PRESERVED"
    return record


def read_xlsx_value(zf: zipfile.ZipFile, sheet_path: str, cells: set[str]) -> dict[str, object]:
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    root = ET.fromstring(zf.read(sheet_path))
    shared = []
    if "xl/sharedStrings.xml" in zf.namelist():
        shared_root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
        shared = ["".join(t.text or "" for t in si.findall(".//m:t", ns)) for si in shared_root.findall("m:si", ns)]
    found = {}
    for cell in root.findall(".//m:c", ns):
        ref = cell.attrib.get("r")
        if ref not in cells:
            continue
        kind = cell.attrib.get("t")
        value = cell.find("m:v", ns)
        if kind == "inlineStr":
            val = "".join(t.text or "" for t in cell.findall(".//m:t", ns))
        elif value is None or value.text is None:
            val = None
        elif kind == "s":
            val = shared[int(value.text)]
        elif kind == "b":
            val = value.text == "1"
        elif kind in (None, "n"):
            raw = value.text
            number = float(raw)
            val = int(number) if number.is_integer() else number
        else:
            val = value.text
        found[ref] = val
    missing = cells - set(found)
    if missing:
        raise ValueError(f"missing workbook cells in {sheet_path}: {sorted(missing)}")
    return found


def stdlib_catalysis_replay(scratch: Path) -> dict:
    """Read only Figure 2 c/d cached values and reproduce the exact duty groups."""
    from fractions import Fraction

    book_path = scratch / "originals/catalysis/final_Fig2.xlsx"
    baseline_path = scratch / "originals/catalysis/equal_duty_results.json"
    ns_main = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    ns_rel = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    ns_pkg = "{http://schemas.openxmlformats.org/package/2006/relationships}"
    with zipfile.ZipFile(book_path) as zf:
        wb = ET.fromstring(zf.read("xl/workbook.xml"))
        rels_root = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rels = {x.attrib["Id"]: x.attrib["Target"] for x in rels_root.findall(f"{ns_pkg}Relationship")}
        sheet_paths = {}
        for sheet in wb.findall(f"{ns_main}sheets/{ns_main}sheet"):
            rid = sheet.attrib[f"{ns_rel}id"]
            target = rels[rid]
            if target.startswith("/"):
                path = target.lstrip("/")
            else:
                path = "xl/" + target.lstrip("/")
            # Normalize without permitting traversal from a workbook relationship.
            path = str(PurePosixPath(path))
            safe_posix_path(path)
            sheet_paths[sheet.attrib["name"]] = path
        if "Figure 2 c" not in sheet_paths or "Figure 2 d" not in sheet_paths:
            raise ValueError("catalysis workbook is missing Figure 2 c/d")
        refs = {f"{col}{row}" for row in range(2, 32) for col in "BCD"}
        c = read_xlsx_value(zf, sheet_paths["Figure 2 c"], refs)
        d = read_xlsx_value(zf, sheet_paths["Figure 2 d"], refs)

    groups: dict[str, list[dict]] = {}
    for row in range(2, 32):
        h, interval, conversion = [c[f"{col}{row}"] for col in "BCD"]
        hb, interval_b, selectivity = [d[f"{col}{row}"] for col in "BCD"]
        if (h, interval) != (hb, interval_b):
            raise AssertionError(f"duty rows do not pair at row {row}")
        duty = str(Fraction(str(h)) / Fraction(str(interval)))
        item = {
            "row": row, "h_s": h, "d_s": interval, "period_s": h + interval,
            "conversion_percent": conversion, "paper_selectivity_percent": selectivity,
            "ethane_per_inlet_A": conversion / 100 * (100 / selectivity - 1),
            "cells": {"h": f"Figure 2 c!B{row}", "d": f"Figure 2 c!C{row}",
                      "X": f"Figure 2 c!D{row}", "S": f"Figure 2 d!D{row}"},
        }
        groups.setdefault(duty, []).append(item)
    for group in groups.values():
        group.sort(key=lambda x: x["period_s"])
    actual = {"groups_with_exact_equal_duty": {k: v for k, v in groups.items() if len(v) > 1},
              "uncertainty": "No replicate IDs, error columns or uncertainty bounds in Figure 2 b/c/d sheets. Conditional point-estimate comparisons only."}
    expected = json.loads(baseline_path.read_text())
    if actual != expected:
        raise AssertionError("stdlib XLSX reconstruction differs from the supplied equal_duty_results.json")
    return {"status": "PASS", "method": "stdlib zipfile+xml.etree cached-cell read; no openpyxl", "rows_checked": 30,
            "equal_duty_groups": len(actual["groups_with_exact_equal_duty"]),
            "compared_to_supplied_json": True, "scope": actual["uncertainty"]}


def run_replays(root: Path, state: dict, package_plan: dict, selected: list[dict], locations: dict,
                python_executable: str, strict_public_layout: bool) -> dict:
    dependency_info = {}
    for module in ("numpy", "sympy", "openpyxl"):
        spec = importlib.util.find_spec(module)
        dependency_info[module] = {"available": spec is not None}
    with tempfile.TemporaryDirectory(prefix="gc-public-replay-") as temp_name:
        scratch = Path(temp_name) / "package"
        scratch.mkdir()
        source_results = verify_archives_and_rehydrate(root, state, scratch, strict_public_layout)
        stale = check_source_manifest_known_failure(scratch)

        # A canonical scratch package layout lets the original relative checkers
        # run without machine-specific source paths.
        manifest_source = root / (state["source_manifest_path"] or "SOURCE_PUBLICATION.json")
        if manifest_source.is_file():
            copy_verified_file(manifest_source, scratch / "SOURCE_MANIFEST.supplied.json")
        publication_source = root / "SOURCE_PUBLICATION.json"
        if publication_source.is_file():
            copy_verified_file(publication_source, scratch / "SOURCE_PUBLICATION.json")

        worker_freezes = {}
        for name, manifest_name in (
            ("gc_nonsep_genesis", "FROZEN.json"),
            ("gc_nonsep_adversary", "FROZEN.json"),
            ("gc_control_adversary", "FROZEN.json"),
            ("gc_peak_genesis", "FROZEN_MANIFEST.json"),
            ("gc_kinetic_adversary", "FROZEN.json"),
        ):
            dest, freeze, expected = freeze_worker_into_scratch(root, scratch, name, manifest_name)
            worker_freezes[name] = {"status": freeze.get("status"), "manifest": manifest_name,
                                    "files": expected, "scratch": str(dest.relative_to(scratch))}
        kg_names = [item["name"] for item in list_kinetic_goal_files(locate_worker(root, "gc_kinetic_goal")[0])[1]]
        kg_dir = freeze_additional_into_scratch(root, scratch, "gc_kinetic_goal", kg_names)
        cat_names = [Path(x["path"]).name for x in locations["gc_catalysis_genesis"]["included"]]
        cat_dir = freeze_additional_into_scratch(root, scratch, "gc_catalysis_genesis", cat_names)
        root_dir = freeze_root_into_scratch(root, scratch)

        # Staging checks before any checker subprocess.
        expected_target = json.loads((root_dir / "FIRST_SLAB_TARGET_CERTIFICATE.json").read_text())
        env = os.environ.copy()
        env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0",
                    "OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})
        checks = []

        def dependency_blocked(label: str, needed: list[str]) -> bool:
            absent = [name for name in needed if not dependency_info[name]["available"]]
            if absent:
                checks.append({"check": label, "status": "ENVIRONMENT_BLOCKED",
                               "reason": "missing modules: " + ", ".join(absent)})
                return True
            return False

        # Exact nonseparated checker: only its old worktree/Git provenance loop
        # is adapted in the disposable copy; source code in the published tree stays byte-identical.
        nonsep_dir = scratch / "workers/gc_nonsep_genesis"
        patch = patch_nonsep_genesis_checker(nonsep_dir / "check_exact.py")
        if not dependency_blocked("gc_nonsep_genesis.check_exact", ["sympy"]):
            r = run_command("gc_nonsep_genesis.check_exact",
                            [python_executable, str(nonsep_dir / "check_exact.py")], scratch, 180, env)
            try:
                receipt = json.loads((nonsep_dir / "CHECK_RECEIPT.json").read_text())
                status = "PASS" if r["exit_code"] == 0 and receipt.get("status") == "PASS" and all(x.get("pass") for x in receipt.get("checks", [])) else "FAIL"
                checks.append({"check": r["check"], "status": status, "exit_code": r["exit_code"],
                               "elapsed_seconds": r["elapsed_seconds"], "checker_patch": patch,
                               "exact_check_groups": len(receipt.get("checks", [])),
                               "generated_receipt_sha256": sha256_file(nonsep_dir / "CHECK_RECEIPT.json"),
                               "stdout": r["stdout"]})
            except Exception as exc:
                checks.append({"check": r["check"], "status": "FAIL", "exit_code": r["exit_code"],
                               "elapsed_seconds": r["elapsed_seconds"], "checker_patch": patch,
                               "error": f"could not validate checker receipt: {exc}", "stdout": r["stdout"]})

        if not dependency_blocked("gc_nonsep_adversary.verify", ["numpy", "sympy"]):
            adv_dir = scratch / "workers/gc_nonsep_adversary"
            r = run_command("gc_nonsep_adversary.verify", [python_executable, str(adv_dir / "verify.py")], scratch, 180, env)
            try:
                receipt = json.loads((adv_dir / "VERIFICATION_RECEIPT.json").read_text())
                status = "PASS" if r["exit_code"] == 0 and receipt.get("checks_passed", 0) > 0 and all(receipt.get("checks", {}).values()) else "FAIL"
                checks.append({"check": r["check"], "status": status, "exit_code": r["exit_code"],
                               "elapsed_seconds": r["elapsed_seconds"], "checks_passed": receipt.get("checks_passed"),
                               "finite_diagnostic_cases": receipt.get("finite_diagnostics", {}).get("cases"),
                               "generated_receipt_sha256": sha256_file(adv_dir / "VERIFICATION_RECEIPT.json"),
                               "stdout": r["stdout"]})
            except Exception as exc:
                checks.append({"check": r["check"], "status": "FAIL", "exit_code": r["exit_code"],
                               "elapsed_seconds": r["elapsed_seconds"], "error": str(exc), "stdout": r["stdout"]})

        if not dependency_blocked("gc_control_adversary.checks", ["numpy"]):
            control = scratch / "workers/gc_control_adversary/checks.py"
            r = run_command("gc_control_adversary.checks", [python_executable, str(control)], scratch, 180, env)
            output_path = control.with_name("checks.json")
            try:
                generated = json.loads(output_path.read_text())
                status = "PASS" if r["exit_code"] == 0 and generated.get("status") == "PASS" else "FAIL"
                checks.append({"check": r["check"], "status": status, "exit_code": r["exit_code"],
                               "elapsed_seconds": r["elapsed_seconds"],
                               "generated_output_sha256": sha256_file(output_path), "stdout": r["stdout"]})
            except Exception as exc:
                checks.append({"check": r["check"], "status": "FAIL", "exit_code": r["exit_code"],
                               "elapsed_seconds": r["elapsed_seconds"], "error": str(exc), "stdout": r["stdout"]})

        if not dependency_blocked("gc_peak_genesis.check", ["numpy"]):
            peak = scratch / "workers/gc_peak_genesis/check.py"
            r = run_command("gc_peak_genesis.check", [python_executable, str(peak)], scratch, 180, env)
            output_path = peak.with_name("CHECK_RESULTS.json")
            try:
                generated = json.loads(output_path.read_text())
                status = "PASS" if r["exit_code"] == 0 and generated.get("status") == "PASS" else "FAIL"
                checks.append({"check": r["check"], "status": status, "exit_code": r["exit_code"],
                               "elapsed_seconds": r["elapsed_seconds"], "generated_output_sha256": sha256_file(output_path),
                               "runtime_python": generated.get("python"), "runtime_numpy": generated.get("numpy"),
                               "stdout": r["stdout"]})
            except Exception as exc:
                checks.append({"check": r["check"], "status": "FAIL", "exit_code": r["exit_code"],
                               "elapsed_seconds": r["elapsed_seconds"], "error": str(exc), "stdout": r["stdout"]})

        if not dependency_blocked("gc_kinetic_adversary.check_actual_target", ["numpy"]):
            target = scratch / "workers/gc_kinetic_adversary/check_actual_target.py"
            # This is the small independent saved-array audit, not the producer's
            # full verify_packet.py wrapper or candidate solver.
            r = run_command("gc_kinetic_adversary.check_actual_target",
                            [python_executable, str(target)], scratch, 240, env)
            output_path = target.with_name("actual_target_checks.json")
            try:
                generated = json.loads(output_path.read_text())
                status = "PASS" if r["exit_code"] == 0 and generated.get("status") == "PASS_BOUNDED_EXACT_ACTUAL_TARGET_AND_SUPPORT_AUDIT" else "FAIL"
                checks.append({"check": r["check"], "status": status, "exit_code": r["exit_code"],
                               "elapsed_seconds": r["elapsed_seconds"], "generated_output_sha256": sha256_file(output_path),
                               "candidate_count": len(generated.get("candidates", [])),
                               "memory_limit_status": generated.get("memory_limit_status"), "stdout": r["stdout"]})
            except Exception as exc:
                checks.append({"check": r["check"], "status": "FAIL", "exit_code": r["exit_code"],
                               "elapsed_seconds": r["elapsed_seconds"], "error": str(exc), "stdout": r["stdout"]})

        if not dependency_blocked("gc_kinetic_goal.verify_cluster", ["numpy"]):
            certificate = kg_dir / "cluster_erlang_saved_64.json"
            model = scratch / "originals/kinetic/schlogl_first_slab_packet/experiments/constrained_test/candidate.json"
            cap = scratch / "originals/kinetic/schlogl_first_slab_packet/references/cap_source/fz_kinetic_cap_certificate_audit_EXACT_AUDIT.json"
            output = kg_dir / "PUBLIC_REPLAY_EXACT_REPLAY.json"
            cmd = [python_executable, str(kg_dir / "verify_cluster.py"), str(certificate),
                   "--model-manifest", str(model), "--cap-certificate", str(cap), "--output", str(output)]
            r = run_command("gc_kinetic_goal.verify_cluster", cmd, scratch, 180, env)
            try:
                generated = json.loads(output.read_text())
                expected = json.loads((kg_dir / "EXACT_REPLAY.json").read_text())
                volatile = {"model_manifest", "cap_certificate", "elapsed_seconds", "peak_rss_native_units", "platform"}
                stable_generated = {k: v for k, v in generated.items() if k not in volatile}
                stable_expected = {k: v for k, v in expected.items() if k not in volatile}
                status = "PASS" if r["exit_code"] == 0 and generated.get("status") == "PASS_EXACT_IMMUTABLE_CLUSTER_REPLAY" and stable_generated == stable_expected else "FAIL"
                checks.append({"check": r["check"], "status": status, "exit_code": r["exit_code"],
                               "elapsed_seconds": r["elapsed_seconds"], "generated_output_sha256": sha256_file(output),
                               "saved_vectors_checked": generated.get("all_saved_resolvent_vectors_checked"),
                               "states_per_vector": generated.get("states_per_vector"),
                               "portable_path_normalization": sorted(volatile), "stdout": r["stdout"]})
            except Exception as exc:
                checks.append({"check": r["check"], "status": "FAIL", "exit_code": r["exit_code"],
                               "elapsed_seconds": r["elapsed_seconds"], "error": str(exc), "stdout": r["stdout"]})

        # Root-level exact stopped first-slab certificate.
        r = run_command("root.check_first_slab_target", [python_executable, str(root_dir / "check_first_slab_target.py")],
                        scratch, 90, env)
        generated_path = root_dir / "FIRST_SLAB_TARGET_CERTIFICATE.json"
        try:
            generated = json.loads(generated_path.read_text())
            status = "PASS" if r["exit_code"] == 0 and generated == expected_target else "FAIL"
            checks.append({"check": r["check"], "status": status, "exit_code": r["exit_code"],
                           "elapsed_seconds": r["elapsed_seconds"],
                           "generated_certificate_sha256": sha256_file(generated_path),
                           "certificate_matches_published": generated == expected_target, "stdout": r["stdout"]})
        except Exception as exc:
            checks.append({"check": r["check"], "status": "FAIL", "exit_code": r["exit_code"],
                           "elapsed_seconds": r["elapsed_seconds"], "error": str(exc), "stdout": r["stdout"]})

        try:
            catalysis = stdlib_catalysis_replay(scratch)
            checks.append({"check": "stdlib_catalysis_workbook_receiver", **catalysis})
        except Exception as exc:
            checks.append({"check": "stdlib_catalysis_workbook_receiver", "status": "FAIL", "error": str(exc)})
        checks.append({"check": "original_catalysis_checker", "status": "ENVIRONMENT_BLOCKED" if not dependency_info["openpyxl"]["available"] else "NOT_RUN",
                       "reason": "producer checker imports openpyxl; independent stdlib workbook receiver above checks the same supplied Figure 2 receiving"})
        checks.append({"check": "catalysis_genesis_external_model_checker", "status": "INPUT_EXCLUDED",
                       "reason": "electrical_and_fixed_model.py requires external_excluded_from_publication/final_SIFig7.xlsx; this acquired workbook is excluded"})
        checks.append({"check": "original_schlogl_full_packet_wrapper", "status": "INSPECTED_NOT_RUN",
                       "reason": "verify_packet.py launches the full slab verifier under the known macOS 512 MiB RLIMIT_AS failure; no solver or wrapper rerun"})

        overall = "PASS" if all(x.get("status") in ("PASS", "ENVIRONMENT_BLOCKED", "INPUT_EXCLUDED", "INSPECTED_NOT_RUN") for x in checks) else "FAIL"
        return {
            "schema": SCHEMA,
            "status": overall,
            "base_revision": state["base_revision"],
            "runtime": {"python": sys.version, "executable": python_executable,
                        "numpy": None, "sympy": None, "openpyxl": None,
                        "dependencies": dependency_info},
            "source_identity": source_results,
            "preserved_known_failure": stale,
            "worker_freezes": worker_freezes,
            "checks": checks,
            "scope": "Byte integrity, exact/algebraic finite worker replays, a bounded saved-array first-slab receiving audit, exact kinetic cluster receiver, standard-library Figure 2 workbook reconstruction, and root stopped-target arithmetic. This is not scientific truth, full-solver validation, physical control, or external mathematical review.",
            "not_run": ["source candidate solvers", "original Schlogl verify_packet.py wrapper", "SciPy-based or networked acquisition programs", "external catalysis workbook model checker"],
            "scratch": "Temporary canonical package; removed on exit",
        }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--package-root", type=Path, default=None,
                    help="published package root (defaults to nearest ancestor containing source locator and originals/)")
    ap.add_argument("--python", default=sys.executable, help="Python executable for bounded checker subprocesses")
    ap.add_argument("--plan-only", action="store_true", help="print manifest-driven selected file list without replay")
    ap.add_argument("--strict-public-layout", action="store_true",
                    help="require 79 expanded source members and no expanded copies of the three large NPZs")
    ap.add_argument("--receipt", type=Path, default=None,
                    help="optional path for a follow-up receipt; default prints JSON only")
    args = ap.parse_args()
    root = (args.package_root or package_root_from_script()).resolve()
    state = read_source_state(root)
    plan = build_publication_plan(root, state)
    if args.plan_only:
        print(json.dumps(plan, indent=2))
        return 0
    selected_records = plan["source_files"] + plan["derived_files"]
    before = snapshot_selected_files(root, selected_records)
    receipt = run_replays(root, state, plan, plan["derived_files"], plan["replay_locations"],
                          args.python, args.strict_public_layout)
    after = snapshot_selected_files(root, selected_records)
    before_by_path = {x["path"]: x for x in before}
    after_by_path = {x["path"]: x for x in after}
    expected_by_path = {x["path"]: x for x in selected_records}
    mismatches = [name for name in sorted(before_by_path)
                  if before_by_path[name] != after_by_path.get(name)
                  or before_by_path[name].get("sha256") != expected_by_path[name].get("sha256")
                  or before_by_path[name].get("bytes") != expected_by_path[name].get("bytes")]
    receipt["selected_inputs_before_after"] = {
        "status": "PASS" if not mismatches else "FAIL",
        "selected_file_count": len(before), "before": before, "after": after,
        "mismatches": mismatches,
        "scope": "All manifest-selected source and derived files were hashed before and after temporary replay; no source/selected input edits were observed.",
    }
    if mismatches:
        receipt["status"] = "FAIL"
    receipt["publication_plan_sha256"] = sha256_bytes(json.dumps(plan, sort_keys=True, separators=(",", ":")).encode())
    receipt["selected_file_count"] = len(plan["source_files"]) + len(plan["derived_files"])
    receipt["selected_files"] = plan["source_files"] + plan["derived_files"]
    receipt["ephemeral_relocations"] = plan["ephemeral_relocations"]
    if args.receipt is not None:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        raw = (json.dumps(receipt, indent=2) + "\n").encode()
        temp_out = args.receipt.with_name(args.receipt.name + ".tmp")
        temp_out.write_bytes(raw)
        os.replace(temp_out, args.receipt)
        receipt["receipt_sha256"] = sha256_file(args.receipt)
        receipt["receipt_path"] = str(args.receipt)
        sidecar = args.receipt.with_suffix(".sha256")
        sidecar.write_text(f"{receipt['receipt_sha256']}  {args.receipt.name}\n")
        receipt["receipt_hash_sidecar"] = str(sidecar)
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
