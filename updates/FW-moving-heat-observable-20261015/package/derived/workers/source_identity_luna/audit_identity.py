#!/usr/bin/env python3
"""Hash-only provenance and deduplication audit for the moving-heat intake.

Run from any working directory with:
    python3 research/2026-10-15-moving-heat-observable-power-v1/workers/source_identity_luna/audit_identity.py

The script reads the source manifest, supplied originals, preserved copies,
ZIP members and their declarative SHA manifests. It hashes the five FT/FU/FV
update trees in the pinned capital worktree, the three small candidate intake
folders explicitly listed by FV's duplicate-check manifest, and exact file
paths named by selected metadata manifests. It does not execute supplied
scripts or scan broad Downloads, attachment, or unrelated research roots.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import stat
import subprocess
import zipfile
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
R_REL = Path("research/2026-10-15-moving-heat-observable-power-v1")
W_REL = Path("work/astra-capital-moving-heat-observable-20261015")
R = ROOT / R_REL
W = ROOT / W_REL
OUT = Path(__file__).resolve().parent
SOURCE_MANIFEST = R / "SOURCE_MANIFEST.json"
FV_DUPLICATE_MANIFEST = (
    W
    / "updates/FV-positive-consequences-20261015/package/derived/workers"
    / "intake_acquisition_luna/MANIFEST.json"
)

SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
TEXT_HASH_RE = re.compile(r"^\s*([0-9a-fA-F]{64})\s+\*?(.+?)\s*$")
METADATA_NAMES = (
    "MANIFEST",
    "SOURCE",
    "INPUT_RECEIPT",
    "EVIDENCE_REF",
    "INDEXED_SOURCE",
    "PROVENANCE",
)
SOURCE_PATH_KEYS = {
    "source_absolute_path",
    "original_absolute_path",
    "original_path",
    "original",
    "preserved_path",
    "preserved_absolute_path",
    "preserved",
    "research_preserved_absolute_path",
    "research_path",
    "attachment_path",
    "source_path",
    "path",
    "file_path",
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest_file(path: Path) -> tuple[int, str]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        while True:
            block = f.read(1024 * 1024)
            if not block:
                break
            size += len(block)
            h.update(block)
    return size, h.hexdigest()


def rel_or_abs(path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(ROOT).as_posix()
    except ValueError:
        return str(path.resolve(strict=False))


def within(path: Path, base: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(base.resolve(strict=False))
        return True
    except ValueError:
        return False


def source_group_for(entry: dict[str, Any]) -> str:
    p = PurePosixPath(entry["path"])
    parts = p.parts
    if entry.get("kind") == "supplied_archive":
        return f"archive:{p.name}"
    if entry.get("kind") == "supplied_pasted_text":
        return f"pasted:{p.name}"
    if len(parts) >= 3:
        return f"directory:{parts[1]}"
    return f"unclassified:{p.name}"


def safe_manifest_path(root: Path, value: str) -> tuple[Path | None, str | None]:
    p = PurePosixPath(value.replace("\\", "/"))
    if p.is_absolute() or ".." in p.parts:
        return None, "absolute_or_parent_traversal"
    candidate = root.joinpath(*p.parts)
    if not within(candidate, root):
        return None, "resolved_outside_root"
    return candidate, None


def iter_regular_files(root: Path) -> tuple[list[Path], list[dict[str, str]]]:
    files: list[Path] = []
    symlinks: list[dict[str, str]] = []
    if not root.exists():
        return files, symlinks
    if root.is_symlink():
        symlinks.append({"path": rel_or_abs(root), "target": os.readlink(root)})
        return files, symlinks
    if root.is_file():
        if root.is_symlink():
            symlinks.append({"path": rel_or_abs(root), "target": os.readlink(root)})
        else:
            files.append(root)
        return files, symlinks
    for base, dirs, names in os.walk(root, topdown=True, followlinks=False):
        base_path = Path(base)
        kept_dirs: list[str] = []
        for name in sorted(dirs):
            p = base_path / name
            if p.is_symlink():
                symlinks.append({"path": rel_or_abs(p), "target": os.readlink(p)})
            else:
                kept_dirs.append(name)
        dirs[:] = kept_dirs
        for name in sorted(names):
            p = base_path / name
            try:
                mode = p.lstat().st_mode
            except OSError:
                continue
            if stat.S_ISLNK(mode):
                symlinks.append({"path": rel_or_abs(p), "target": os.readlink(p)})
            elif stat.S_ISREG(mode):
                files.append(p)
    return sorted(files), symlinks


def parse_digest_manifest(data: bytes, filename: str) -> tuple[list[tuple[str, str]], str | None]:
    records: list[tuple[str, str]] = []
    if filename.lower().endswith(".json"):
        try:
            obj = json.loads(data.decode("utf-8"))
        except Exception as exc:  # content is data; malformed manifests are recorded
            return [], f"json_parse_error:{type(exc).__name__}"

        def visit(x: Any) -> None:
            if isinstance(x, dict):
                path_value = next(
                    (x[k] for k in ("path", "file", "filename", "name", "relative_path")
                     if isinstance(x.get(k), str)),
                    None,
                )
                hash_value = next(
                    (x[k] for k in ("sha256", "SHA256", "hash")
                     if isinstance(x.get(k), str) and SHA256_RE.fullmatch(x[k])),
                    None,
                )
                if path_value is not None and hash_value is not None:
                    records.append((path_value, hash_value.lower()))
                for key, value in x.items():
                    if isinstance(value, str) and SHA256_RE.fullmatch(value):
                        # Producer manifests commonly use {relative_path: sha256}.
                        if key.lower() not in {"sha256", "hash", "manifest_sha256"}:
                            records.append((key, value.lower()))
                    else:
                        visit(value)
            elif isinstance(x, list):
                for value in x:
                    visit(value)

        visit(obj)
    else:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            return [], "text_not_utf8"
        for line in text.splitlines():
            match = TEXT_HASH_RE.match(line)
            if match:
                records.append((match.group(2), match.group(1).lower()))
    unique = sorted(set(records))
    return unique, None


def normalize_archive_name(value: str) -> str | None:
    value = value.replace("\\", "/")
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts:
        return None
    return p.as_posix()


def resolve_archive_manifest_path(
    listed: str, manifest_member: str, archive_names: set[str]
) -> tuple[str | None, str | None]:
    normalized = normalize_archive_name(listed)
    if normalized is None:
        return None, "unsafe_listed_path"
    base = PurePosixPath(manifest_member).parent
    candidates = [normalized, (base / normalized).as_posix()]
    # A common source archive wraps files in one package directory while a
    # producer's own manifest is relative to that package root.
    top_levels = sorted({PurePosixPath(n).parts[0] for n in archive_names if PurePosixPath(n).parts})
    if len(top_levels) == 1:
        candidates.append((PurePosixPath(top_levels[0]) / normalized).as_posix())
    for candidate in candidates:
        if candidate in archive_names:
            return candidate, "exact_or_manifest_relative"
    suffix_matches = sorted(n for n in archive_names if n.endswith("/" + normalized))
    if len(suffix_matches) == 1:
        return suffix_matches[0], "unique_exact_suffix"
    return None, "unresolved" if not suffix_matches else "ambiguous_suffix"


def validate_zip_hash_manifests(zip_path: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with zipfile.ZipFile(zip_path) as zf:
        names = {normalize_archive_name(i.filename) for i in zf.infolist() if not i.is_dir()}
        names.discard(None)
        for info in zf.infolist():
            if info.is_dir():
                continue
            base = PurePosixPath(info.filename).name.lower()
            if not ("sha256" in base or "checksum" in base or base in {"checksums.txt"}):
                continue
            data = zf.read(info)
            records, parse_error = parse_digest_manifest(data, info.filename)
            verified = 0
            missing: list[dict[str, str]] = []
            mismatched: list[dict[str, str]] = []
            unresolved: list[dict[str, str]] = []
            for listed, expected in records:
                member, method = resolve_archive_manifest_path(listed, info.filename, names)
                if member is None:
                    unresolved.append({"listed_path": listed, "resolution": method or "unresolved"})
                    continue
                actual = digest_bytes(zf.read(member))
                if actual == expected:
                    verified += 1
                else:
                    mismatched.append({"listed_path": listed, "member": member, "expected": expected, "observed": actual})
            results.append({
                "manifest_member": info.filename,
                "manifest_sha256": digest_bytes(data),
                "manifest_bytes": len(data),
                "record_count": len(records),
                "verified_count": verified,
                "missing_or_unresolved": unresolved,
                "mismatched": mismatched,
                "parse_error": parse_error,
            })
    return results


def validate_directory_hash_manifests(group_root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    files, _ = iter_regular_files(group_root)
    for manifest_path in files:
        base = manifest_path.name.lower()
        if not ("sha256" in base or "checksum" in base or base == "manifest.json"):
            continue
        data = manifest_path.read_bytes()
        records, parse_error = parse_digest_manifest(data, manifest_path.name)
        if not records and parse_error is None:
            continue
        verified = 0
        unresolved: list[dict[str, str]] = []
        mismatched: list[dict[str, str]] = []
        for listed, expected in records:
            target, reason = safe_manifest_path(group_root, listed)
            if target is None or not target.is_file() or target.is_symlink():
                unresolved.append({"listed_path": listed, "resolution": reason or "not_regular_file"})
                continue
            _, observed = digest_file(target)
            if observed == expected:
                verified += 1
            else:
                mismatched.append({"listed_path": listed, "target": rel_or_abs(target), "expected": expected, "observed": observed})
        results.append({
            "manifest_path": rel_or_abs(manifest_path),
            "manifest_sha256": digest_bytes(data),
            "record_count": len(records),
            "verified_count": verified,
            "missing_or_unresolved": unresolved,
            "mismatched": mismatched,
            "parse_error": parse_error,
        })
    return results


def scan_metadata_file_references(update_roots: list[Path]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    refs: list[dict[str, str]] = []
    symlinks: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for update_root in update_roots:
        paths, tree_symlinks = iter_regular_files(update_root)
        symlinks.extend(tree_symlinks)
        for metadata_path in paths:
            upper = metadata_path.name.upper()
            if metadata_path.suffix.lower() != ".json" or not any(token in upper for token in METADATA_NAMES):
                continue
            try:
                obj = json.loads(metadata_path.read_text(encoding="utf-8"))
            except Exception:
                continue

            def walk(value: Any, key: str = "") -> None:
                if isinstance(value, dict):
                    for child_key, child in value.items():
                        walk(child, str(child_key))
                elif isinstance(value, list):
                    for child in value:
                        walk(child, key)
                elif isinstance(value, str) and key.lower() in SOURCE_PATH_KEYS:
                    candidate: Path | None = None
                    if value.startswith("/"):
                        candidate = Path(value)
                    elif value.startswith(("research/", "work/")):
                        candidate = ROOT / value
                    elif value.startswith("updates/"):
                        candidate = W / value
                    if candidate is None or not candidate.exists() or not candidate.is_file() or candidate.is_symlink():
                        return
                    resolved = candidate.resolve(strict=False)
                    row = (str(resolved), rel_or_abs(metadata_path), key)
                    if row not in seen:
                        seen.add(row)
                        refs.append({
                            "path": rel_or_abs(resolved),
                            "referenced_by": rel_or_abs(metadata_path),
                            "field": key,
                        })

            walk(obj)
    return refs, symlinks


def discover_candidate_intake_dirs() -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    if not FV_DUPLICATE_MANIFEST.is_file():
        return [], [{"path": rel_or_abs(FV_DUPLICATE_MANIFEST), "reason": "manifest_missing"}]
    try:
        obj = json.loads(FV_DUPLICATE_MANIFEST.read_text(encoding="utf-8"))
    except Exception as exc:
        return [], [{"path": rel_or_abs(FV_DUPLICATE_MANIFEST), "reason": f"manifest_parse_error:{type(exc).__name__}"}]
    candidates: list[str] = []

    def walk(value: Any, key: str = "") -> None:
        if isinstance(value, dict):
            for child_key, child in value.items():
                walk(child, str(child_key))
        elif isinstance(value, list):
            for child in value:
                walk(child, key)
        elif isinstance(value, str) and key == "candidate_source_folders":
            candidates.append(value)

    walk(obj)
    roots: list[dict[str, Any]] = []
    missing: list[dict[str, str]] = []
    for value in sorted(set(candidates)):
        path = Path(value) if value.startswith("/") else ROOT / value
        if not path.is_dir():
            missing.append({"path": value, "reason": "directory_missing"})
            continue
        files, links = iter_regular_files(path)
        roots.append({
            "path": rel_or_abs(path),
            "declared_by": rel_or_abs(FV_DUPLICATE_MANIFEST),
            "field": "supplied3_duplicate_check.candidate_source_folders",
            "file_count": len(files),
            "symlink_count": len(links),
        })
    return roots, missing


def git_head(path: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def main() -> dict[str, Any]:
    started = utc_now()
    manifest_bytes, manifest_sha = digest_file(SOURCE_MANIFEST)
    manifest = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    entries = manifest.get("files", [])
    declared_group_count = manifest.get("source_groups")

    original_checks: list[dict[str, Any]] = []
    source_artifacts: list[dict[str, Any]] = []
    source_groups: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "manifest_entries": 0,
        "archive_members": 0,
        "declared_bytes": 0,
        "manifest_sha256s": set(),
        "archive_member_sha256s": set(),
    })
    manifest_path_issues: list[dict[str, str]] = []

    for entry in entries:
        group = source_group_for(entry)
        source_groups[group]["manifest_entries"] += 1
        source_groups[group]["declared_bytes"] += int(entry.get("bytes", 0))
        declared_sha = entry.get("sha256")
        if declared_sha:
            source_groups[group]["manifest_sha256s"].add(declared_sha)
        preserved, path_issue = safe_manifest_path(R, entry["path"])
        if path_issue:
            manifest_path_issues.append({"path": entry["path"], "reason": path_issue})
        local = None
        local_size = None
        local_sha = None
        if preserved is not None and preserved.is_file() and not preserved.is_symlink():
            local_size, local_sha = digest_file(preserved)
        original_path = Path(entry["original_path"])
        original_size = None
        original_sha = None
        if original_path.is_file() and not original_path.is_symlink():
            original_size, original_sha = digest_file(original_path)
        original_checks.append({
            "source_group": group,
            "kind": entry.get("kind"),
            "manifest_path": entry["path"],
            "original_path": str(original_path),
            "declared_bytes": int(entry.get("bytes", 0)),
            "declared_sha256": declared_sha,
            "original_exists": original_sha is not None,
            "original_bytes": original_size,
            "original_sha256": original_sha,
            "original_match": original_size == entry.get("bytes") and original_sha == declared_sha,
            "preserved_exists": local_sha is not None,
            "preserved_bytes": local_size,
            "preserved_sha256": local_sha,
            "preserved_match": local_size == entry.get("bytes") and local_sha == declared_sha,
            "original_equals_preserved": original_sha is not None and local_sha is not None and original_sha == local_sha,
        })
        source_artifacts.append({
            "artifact_kind": "manifest_file",
            "source_group": group,
            "path": entry["path"],
            "observed_bytes": local_size,
            "observed_sha256": local_sha,
            "declared_bytes": int(entry.get("bytes", 0)),
            "declared_sha256": declared_sha,
            "preserved_match": local_size == entry.get("bytes") and local_sha == declared_sha,
        })

    archive_results: list[dict[str, Any]] = []
    zip_hash_manifests: list[dict[str, Any]] = []
    directory_hash_manifests: list[dict[str, Any]] = []
    extraction_symlinks: list[dict[str, str]] = []
    for entry in entries:
        if entry.get("kind") != "supplied_archive":
            continue
        archive_path = R / entry["path"]
        archive_group = source_group_for(entry)
        extract_root = R / "sources" / Path(entry["path"]).stem
        observed_names: list[str] = []
        member_rows: list[dict[str, Any]] = []
        unsafe_members: list[dict[str, str]] = []
        archive_symlinks: list[str] = []
        duplicate_member_names: list[str] = []
        with zipfile.ZipFile(archive_path) as zf:
            infos = [i for i in zf.infolist() if not i.is_dir()]
            seen_names: set[str] = set()
            for info in infos:
                normalized = normalize_archive_name(info.filename)
                if normalized is None:
                    unsafe_members.append({"member": info.filename, "reason": "absolute_or_parent_traversal"})
                    continue
                if normalized in seen_names:
                    duplicate_member_names.append(normalized)
                seen_names.add(normalized)
                observed_names.append(normalized)
                mode = (info.external_attr >> 16) & 0o170000
                is_link = mode == stat.S_IFLNK
                if is_link:
                    archive_symlinks.append(normalized)
                expected_bytes = zf.read(info)
                member_sha = digest_bytes(expected_bytes)
                source_groups[archive_group]["archive_members"] += 1
                source_groups[archive_group]["archive_member_sha256s"].add(member_sha)
                extracted, extract_issue = safe_manifest_path(extract_root, normalized)
                if extract_issue:
                    unsafe_members.append({"member": info.filename, "reason": f"extract_{extract_issue}"})
                    extracted_sha = None
                    extracted_size = None
                elif extracted is None or not extracted.is_file() or extracted.is_symlink():
                    extracted_sha = None
                    extracted_size = None
                else:
                    extracted_size, extracted_sha = digest_file(extracted)
                member_rows.append({
                    "artifact_kind": "zip_member",
                    "source_group": archive_group,
                    "path": f"{entry['path']}!/{normalized}",
                    "member_path": normalized,
                    "observed_bytes": len(expected_bytes),
                    "observed_sha256": member_sha,
                    "extracted_path": rel_or_abs(extracted) if extracted is not None else None,
                    "extracted_exists": extracted_sha is not None,
                    "extracted_bytes": extracted_size,
                    "extracted_sha256": extracted_sha,
                    "extraction_match": extracted_size == len(expected_bytes) and extracted_sha == member_sha,
                    "zip_member_is_symlink": is_link,
                })
        extraction_files, links = iter_regular_files(extract_root)
        extraction_symlinks.extend(links)
        extracted_names = sorted(
            p.relative_to(extract_root).as_posix()
            for p in extraction_files
        )
        expected_names = sorted(observed_names)
        extra_names = sorted(set(extracted_names) - set(expected_names))
        missing_names = sorted(set(expected_names) - set(extracted_names))
        archive_size, archive_sha = digest_file(archive_path)
        zip_hash_manifests.extend(validate_zip_hash_manifests(archive_path))
        archive_results.append({
            "source_group": archive_group,
            "archive_path": entry["path"],
            "archive_bytes_match": archive_size == entry.get("bytes"),
            "archive_sha256_match": archive_sha == entry.get("sha256"),
            "member_count": len(member_rows),
            "member_bytes": sum(int(r["observed_bytes"] or 0) for r in member_rows),
            "extracted_files": len(extracted_names),
            "members_all_exactly_extracted": all(r["extraction_match"] for r in member_rows),
            "missing_members": missing_names,
            "extra_extracted_files": extra_names,
            "unsafe_members": unsafe_members,
            "archive_symlink_members": archive_symlinks,
            "duplicate_member_names": sorted(set(duplicate_member_names)),
        })
        source_artifacts.extend(member_rows)

    for group_name in sorted({source_group_for(e) for e in entries if e.get("kind") == "supplied_directory_file"}):
        group_root = R / "sources" / group_name.split(":", 1)[1]
        directory_hash_manifests.extend(validate_directory_hash_manifests(group_root))

    update_roots = sorted(
        (p for p in (W / "updates").iterdir() if p.is_dir() and p.name.startswith(("FT", "FU", "FV"))),
        key=lambda p: p.name,
    )
    candidate_roots, candidate_missing = discover_candidate_intake_dirs()
    direct_refs, metadata_symlinks = scan_metadata_file_references(update_roots)

    targets: dict[str, dict[str, Any]] = {}

    def add_target(path: Path, scope: str, detail: str | None = None) -> None:
        resolved = path.resolve(strict=False)
        key = str(resolved)
        item = targets.setdefault(key, {
            "path": rel_or_abs(resolved),
            "scopes": [],
            "reference_details": [],
        })
        if scope not in item["scopes"]:
            item["scopes"].append(scope)
        if detail and detail not in item["reference_details"]:
            item["reference_details"].append(detail)

    target_symlinks: list[dict[str, str]] = []
    for update_root in update_roots:
        files, links = iter_regular_files(update_root)
        target_symlinks.extend(links)
        for path in files:
            add_target(path, f"update:{update_root.name}")
    for candidate in candidate_roots:
        root_path = Path(candidate["path"])
        if not root_path.is_absolute():
            root_path = ROOT / root_path
        files, links = iter_regular_files(root_path)
        target_symlinks.extend(links)
        for path in files:
            add_target(path, f"candidate_intake:{candidate['path']}")
    for ref in direct_refs:
        path_value = ref["path"]
        path = Path(path_value) if path_value.startswith("/") else ROOT / path_value
        if path.is_file() and not path.is_symlink():
            add_target(path, "explicit_metadata_file_reference", f"{ref['referenced_by']}#{ref['field']}")

    target_rows: list[dict[str, Any]] = []
    target_hash_index: dict[str, list[str]] = defaultdict(list)
    for absolute, item in sorted(targets.items()):
        path = Path(absolute)
        try:
            size, sha = digest_file(path)
        except OSError as exc:
            target_rows.append({**item, "size": None, "sha256": None, "hash_error": type(exc).__name__})
            continue
        row = {**item, "scopes": sorted(item["scopes"]), "reference_details": sorted(item["reference_details"]), "size": size, "sha256": sha}
        target_rows.append(row)
        target_hash_index[sha].append(row["path"])

    # source_artifacts already contains one row per manifest-listed file and
    # one row per extracted ZIP member; do not append manifest rows twice.
    all_source_artifacts = source_artifacts
    distinct_source_hashes = sorted({a["observed_sha256"] for a in all_source_artifacts if a.get("observed_sha256")})
    exact_matches: list[dict[str, Any]] = []
    for sha in distinct_source_hashes:
        targets_for_hash = target_hash_index.get(sha, [])
        if not targets_for_hash:
            continue
        artifacts_for_hash = [
            {"source_group": a["source_group"], "artifact_kind": a["artifact_kind"], "path": a["path"]}
            for a in all_source_artifacts if a.get("observed_sha256") == sha
        ]
        exact_matches.append({
            "sha256": sha,
            "source_artifact_count": len(artifacts_for_hash),
            "source_artifacts": artifacts_for_hash,
            "capital_match_count": len(targets_for_hash),
            "capital_paths": sorted(targets_for_hash),
        })

    source_duplicate_hashes: list[dict[str, Any]] = []
    cross_group_duplicates: list[dict[str, Any]] = []
    by_source_sha: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for artifact in all_source_artifacts:
        sha = artifact.get("observed_sha256")
        if sha:
            by_source_sha[sha].append(artifact)
    for sha, artifacts in sorted(by_source_sha.items()):
        groups = sorted({a["source_group"] for a in artifacts})
        if len(artifacts) > 1:
            duplicate = {
                "sha256": sha,
                "source_groups": groups,
                "paths": [
                    {"source_group": a["source_group"], "artifact_kind": a["artifact_kind"], "path": a["path"]}
                    for a in artifacts
                ],
            }
            source_duplicate_hashes.append(duplicate)
            if len(groups) > 1:
                cross_group_duplicates.append(duplicate)

    group_rows: list[dict[str, Any]] = []
    for group, counts in sorted(source_groups.items()):
        group_hashes = {
            a["observed_sha256"] for a in all_source_artifacts
            if a.get("source_group") == group and a.get("observed_sha256")
        }
        matched_hashes = sorted(h for h in group_hashes if target_hash_index.get(h))
        group_rows.append({
            "source_group": group,
            "manifest_entries": counts["manifest_entries"],
            "archive_members": counts["archive_members"],
            "declared_bytes": counts["declared_bytes"],
            "distinct_observed_sha256": len(group_hashes),
            "matched_distinct_sha256": len(matched_hashes),
            "new_distinct_sha256": len(group_hashes) - len(matched_hashes),
            "matched_sha256s": matched_hashes,
        })

    update_metadata: list[dict[str, Any]] = []
    for update_root in update_roots:
        path = update_root / "SOURCE_MANIFEST.json"
        if not path.is_file():
            update_metadata.append({"update": update_root.name, "source_manifest": None})
            continue
        data = path.read_bytes()
        obj = json.loads(data.decode("utf-8"))
        checkpoint_records: list[dict[str, Any]] = []
        for checkpoint_path in sorted(update_root.glob("CHECKPOINT_RECORD*.json")):
            try:
                checkpoint_obj = json.loads(checkpoint_path.read_text(encoding="utf-8"))
            except Exception:
                continue
            checkpoint_records.append({
                "path": rel_or_abs(checkpoint_path),
                "created_at_utc": checkpoint_obj.get("created_at_utc"),
                "base_revision": checkpoint_obj.get("base_revision"),
                "checkpoint_id": checkpoint_obj.get("checkpoint_id"),
            })
        checkpoint_records.sort(key=lambda x: x.get("created_at_utc") or "")
        keep_keys = (
            "schema", "intake_id", "main_revision", "initial_main", "created_at_utc",
            "observed_freeze_clock_utc", "campaign_manifest_sha256", "original_manifest",
            "source_count", "declared_file_count", "copied_item_count", "total_files",
            "total_bytes", "created_at",
        )
        update_metadata.append({
            "update": update_root.name,
            "source_manifest": rel_or_abs(path),
            "source_manifest_sha256": digest_bytes(data),
            "metadata": {k: obj[k] for k in keep_keys if k in obj},
            "file_records": len(obj.get("files", [])) if isinstance(obj.get("files"), list) else None,
            "checkpoint_records": checkpoint_records,
        })

    declared_group_ids = sorted({source_group_for(e) for e in entries})
    matched_artifact_count = sum(
        1 for a in all_source_artifacts
        if a.get("observed_sha256") and target_hash_index.get(a["observed_sha256"])
    )
    available_artifact_count = sum(1 for a in all_source_artifacts if a.get("observed_sha256"))
    target_scope_matches: list[dict[str, Any]] = []
    for match in exact_matches:
        scopes = sorted({
            scope
            for row in target_rows if row.get("sha256") == match["sha256"]
            for scope in row.get("scopes", [])
        })
        if len(scopes) > 1:
            target_scope_matches.append({"sha256": match["sha256"], "scopes": scopes, "capital_paths": match["capital_paths"]})
    explicit_external_targets = [
        {"path": row["path"], "reference_details": row["reference_details"]}
        for row in target_rows
        if "explicit_metadata_file_reference" in row.get("scopes", [])
        and not any(scope.startswith("update:") or scope.startswith("candidate_intake:") for scope in row.get("scopes", []))
    ]

    report: dict[str, Any] = {
        "schema": "astra.source-identity-audit.v1",
        "audit": {
            "started_at_utc": started,
            "completed_at_utc": None,
            "method": "SHA-256 exact-byte identity; no source code executed",
            "workspace_root": str(ROOT),
            "research_root": str(R),
            "capital_worktree": str(W),
            "capital_worktree_head_at_audit": git_head(W),
            "R_initial_main": manifest.get("initial_main"),
            "selection": {
                "capital_update_roots": [rel_or_abs(p) for p in update_roots],
                "candidate_intake_roots": candidate_roots,
                "candidate_intake_roots_missing": candidate_missing,
                "explicit_file_references_discovered": len(direct_refs),
                "explicit_file_references": direct_refs,
                "explicit_external_target_files": explicit_external_targets,
                "broad_roots_not_recursively_scanned": ["/Users/harjas/Downloads", "/Users/harjas/.codex/attachments", "unrelated research roots"],
                "target_regular_files_hashed": len(target_rows),
                "target_symlinks_skipped": target_symlinks + metadata_symlinks,
            },
            "reference_containment_warning": (
                "Exact SHA-256 matches are allowed across source-group, filename, and capital-directory boundaries. "
                "A match establishes identical bytes only; it does not transfer a source label or provenance claim. "
                "Direct file references outside selected update trees are listed as explicit references. "
                "ZIP member paths were checked for absolute/parent traversal; symlinks were recorded and not followed."
            ),
        },
        "source_manifest": {
            "path": rel_or_abs(SOURCE_MANIFEST),
            "bytes": manifest_bytes,
            "sha256": manifest_sha,
            "declared_schema": manifest.get("schema"),
            "declared_source_groups": declared_group_ids,
            "declared_source_group_count": declared_group_count,
            "computed_source_group_count": len(declared_group_ids),
            "declared_file_count": manifest.get("total_original_files"),
            "computed_file_count": len(entries),
            "declared_total_original_bytes": manifest.get("total_original_bytes"),
            "computed_declared_bytes": sum(int(e.get("bytes", 0)) for e in entries),
            "archive_members_are_derived_extractions": manifest.get("archive_members_are_derived_extractions"),
            "manifest_path_containment_issues": manifest_path_issues,
        },
        "capital_update_metadata": update_metadata,
        "original_and_preserved_file_checks": original_checks,
        "source_group_summary": group_rows,
        "archive_extraction_checks": archive_results,
        "archive_own_sha_manifest_checks": zip_hash_manifests,
        "directory_own_sha_manifest_checks": directory_hash_manifests,
        "exact_hash_dedup": {
            "source_artifacts_with_observed_hash": available_artifact_count,
            "source_artifacts_with_capital_match": matched_artifact_count,
            "distinct_source_sha256_count": len(distinct_source_hashes),
            "distinct_source_sha256_matched": len(exact_matches),
            "distinct_source_sha256_new_vs_selected_scope": len(distinct_source_hashes) - len(exact_matches),
            "exact_matches": exact_matches,
            "cross_source_group_exact_duplicates": cross_group_duplicates,
        "duplicate_source_hashes": source_duplicate_hashes,
            "hashes_matched_across_multiple_capital_scopes": target_scope_matches,
            "target_inventory": target_rows,
        },
    }
    report["audit"]["completed_at_utc"] = utc_now()
    OUT.mkdir(parents=True, exist_ok=True)
    json_path = OUT / "identity_report.json"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path = OUT / "IDENTITY_REPORT.md"
    md_path.write_text(render_markdown(report), encoding="utf-8")
    return report


def render_markdown(report: dict[str, Any]) -> str:
    sm = report["source_manifest"]
    dedup = report["exact_hash_dedup"]
    originals = report["original_and_preserved_file_checks"]
    archive_checks = report["archive_extraction_checks"]
    zip_checks = report["archive_own_sha_manifest_checks"]
    dir_checks = report["directory_own_sha_manifest_checks"]
    metadata = report["capital_update_metadata"]
    lines = [
        "# Source identity and exact-hash dedup audit",
        "",
        "This audit verifies the intake manifest against original and preserved bytes, checks ZIP extractions and declarative SHA manifests, and compares exact SHA-256 values with the selected Astra Capital update/intake paths. It makes no scientific claim.",
        "",
        f"Audit window: {report['audit']['started_at_utc']} to {report['audit']['completed_at_utc']} UTC.",
        f"Research intake pin: `{report['audit']['R_initial_main']}`. Capital worktree HEAD at audit: `{report['audit']['capital_worktree_head_at_audit']}`.",
        f"Source manifest: `{sm['path']}`; SHA-256 `{sm['sha256']}`.",
        "",
        "## Manifest and original-byte checks",
        "",
        f"The manifest declares {sm['declared_source_group_count']} groups and {sm['declared_file_count']} files ({sm['declared_total_original_bytes']:,} bytes). Computed from entries: {sm['computed_source_group_count']} groups, {sm['computed_file_count']} files ({sm['computed_declared_bytes']:,} declared bytes).",
        f"Original paths matching declared bytes and SHA-256: {sum(bool(x['original_match']) for x in originals)}/{len(originals)}. Preserved copies matching: {sum(bool(x['preserved_match']) for x in originals)}/{len(originals)}. Original and preserved bytes equal: {sum(bool(x['original_equals_preserved']) for x in originals)}/{len(originals)}.",
        "",
        "| Source group | Listed files | Extracted ZIP members | Distinct observed hashes | Capital matches | New hashes in selected scope |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in report["source_group_summary"]:
        lines.append(
            f"| `{row['source_group']}` | {row['manifest_entries']} | {row['archive_members']} | {row['distinct_observed_sha256']} | {row['matched_distinct_sha256']} | {row['new_distinct_sha256']} |"
        )
    missing_originals = [x for x in originals if not x["original_exists"]]
    mismatched_originals = [x for x in originals if x["original_exists"] and not x["original_match"]]
    missing_copies = [x for x in originals if not x["preserved_exists"]]
    mismatched_copies = [x for x in originals if x["preserved_exists"] and not x["preserved_match"]]
    lines += [
        "",
        f"Missing original paths: {len(missing_originals)}; original byte/hash mismatches: {len(mismatched_originals)}; missing preserved copies: {len(missing_copies)}; preserved byte/hash mismatches: {len(mismatched_copies)}.",
        f"The artifact inventory has {dedup['source_artifacts_with_observed_hash']} observed file rows and {dedup['distinct_source_sha256_count']} distinct hashes; repeated source hashes: {len(dedup['duplicate_source_hashes'])}.",
    ]
    for duplicate in dedup["duplicate_source_hashes"]:
        lines.append(
            "- Repeated exact bytes `" + duplicate["sha256"] + "` in "
            + "; ".join(f"`{x['path']}` ({x['source_group']})" for x in duplicate["paths"])
            + "."
        )
    for title, rows, field in (
        ("Missing original paths", missing_originals, "original_path"),
        ("Original byte/hash mismatches", mismatched_originals, "manifest_path"),
        ("Missing preserved copies", missing_copies, "manifest_path"),
        ("Preserved byte/hash mismatches", mismatched_copies, "manifest_path"),
    ):
        if rows:
            lines += ["", f"{title}:"]
            lines.extend(f"- `{x[field]}`" for x in rows)

    lines += ["", "## ZIP and embedded hash-manifest checks", ""]
    lines.append(
        f"ZIPs checked: {len(archive_checks)}. Members compared with preserved extraction: "
        f"{sum(x['member_count'] for x in archive_checks)} total; "
        f"{sum(x['members_all_exactly_extracted'] for x in archive_checks)}/{len(archive_checks)} archives have every member extracted byte-for-byte."
    )
    for row in archive_checks:
        lines.append(
            f"- `{row['archive_path']}`: {row['member_count']} members; exact extraction={row['members_all_exactly_extracted']}; missing={len(row['missing_members'])}; extra={len(row['extra_extracted_files'])}; unsafe paths={len(row['unsafe_members'])}; ZIP symlinks={len(row['archive_symlink_members'])}."
        )
        if row["missing_members"]:
            lines.append("  - Missing members: " + ", ".join(f"`{x}`" for x in row["missing_members"]))
        if row["extra_extracted_files"]:
            lines.append("  - Extra extracted files: " + ", ".join(f"`{x}`" for x in row["extra_extracted_files"]))
        if row["unsafe_members"]:
            lines.append("  - Unsafe member paths: " + json.dumps(row["unsafe_members"], sort_keys=True))
    checked_manifests = zip_checks + dir_checks
    record_count = sum(x["record_count"] for x in checked_manifests)
    verified_count = sum(x["verified_count"] for x in checked_manifests)
    issues = sum(len(x["missing_or_unresolved"]) + len(x["mismatched"]) + bool(x["parse_error"]) for x in checked_manifests)
    lines.append(
        f"Embedded source SHA manifests discovered with hash records: {len(checked_manifests)}; listed records: {record_count}; verified: {verified_count}; parse, resolution, or hash issues: {issues}."
    )
    for row in checked_manifests:
        if row["mismatched"]:
            for mismatch in row["mismatched"]:
                lines.append(
                    f"- Internal digest discrepancy: `{mismatch['listed_path']}` in `{row.get('manifest_member', row.get('manifest_path'))}` "
                    f"lists `{mismatch['expected']}`, while the archived member hashes to `{mismatch['observed']}`. "
                    "The ZIP member and its preserved extraction agree byte-for-byte; the source manifest discrepancy is retained as observed."
                )
    for row in checked_manifests:
        name = row.get("manifest_member", row.get("manifest_path"))
        local_issues = len(row["missing_or_unresolved"]) + len(row["mismatched"]) + bool(row["parse_error"])
        lines.append(f"- `{name}`: {row['verified_count']}/{row['record_count']} listed hashes verified; issues={local_issues}.")
        if row["missing_or_unresolved"]:
            lines.append("  - Unresolved: " + json.dumps(row["missing_or_unresolved"], sort_keys=True))
        if row["mismatched"]:
            lines.append("  - Mismatched: " + json.dumps(row["mismatched"], sort_keys=True))
        if row.get("parse_error"):
            lines.append("  - Parse: " + row["parse_error"])

    lines += ["", "## Capital comparison scope and results", ""]
    lines.append(
        f"Hashed {report['audit']['selection']['target_regular_files_hashed']} regular files across the five FT/FU/FV update trees, "
        f"{len(report['audit']['selection']['candidate_intake_roots'])} FV-declared candidate intake directories, and explicit existing file references from selected metadata manifests. "
        f"Metadata contained {report['audit']['selection']['explicit_file_references_discovered']} file-reference records; "
        f"{len(report['audit']['selection']['explicit_external_target_files'])} unique explicit file targets fell outside the selected update and candidate-intake directories. "
        f"The source artifact inventory contains {dedup['source_artifacts_with_observed_hash']} observed files, representing {dedup['distinct_source_sha256_count']} distinct SHA-256 values. "
        f"Exact matches: {dedup['distinct_source_sha256_matched']} distinct hashes ({dedup['source_artifacts_with_capital_match']} source artifact rows). "
        f"New to this selected comparison scope: {dedup['distinct_source_sha256_new_vs_selected_scope']} distinct hashes."
    )
    lines += ["", "| Capital update | Recorded manifest/checkpoint dates | Recorded manifest/checkpoint pins | Listed file records | Source-manifest SHA-256 |", "|---|---|---|---:|---|"]
    for row in metadata:
        m = row.get("metadata", {})
        checkpoint = row.get("checkpoint_records", [])
        latest_checkpoint = checkpoint[-1] if checkpoint else {}
        manifest_date = m.get("created_at_utc") or m.get("observed_freeze_clock_utc")
        checkpoint_date = latest_checkpoint.get("created_at_utc")
        date = "; ".join(x for x in (
            f"manifest {manifest_date}" if manifest_date else None,
            f"checkpoint {checkpoint_date}" if checkpoint_date else None,
        ) if x) or "not recorded"
        manifest_pin = m.get("main_revision") or m.get("initial_main")
        checkpoint_pin = latest_checkpoint.get("base_revision")
        pin = "; ".join(x for x in (
            f"manifest {manifest_pin}" if manifest_pin else None,
            f"checkpoint base {checkpoint_pin}" if checkpoint_pin else None,
        ) if x) or "not recorded"
        lines.append(f"| `{row['update']}` | {date} | `{pin}` | {row.get('file_records')} | `{row.get('source_manifest_sha256', 'missing')}` |")
    lines += ["", "FV-declared candidate intake directories included:", ""]
    for candidate in report["audit"]["selection"]["candidate_intake_roots"]:
        lines.append(f"- `{candidate['path']}` — {candidate['file_count']} regular files.")

    if dedup["exact_matches"]:
        lines += ["", "Exact match hashes:", ""]
        for row in dedup["exact_matches"]:
            src = "; ".join(f"{a['source_group']}:{a['path']}" for a in row["source_artifacts"])
            dst = "; ".join(row["capital_paths"])
            lines.append(f"- `{row['sha256']}` — source: {src}; capital: {dst}")
    if dedup["cross_source_group_exact_duplicates"]:
        lines += ["", "Exact byte duplicates crossing R source-group labels:", ""]
        for row in dedup["cross_source_group_exact_duplicates"]:
            lines.append(f"- `{row['sha256']}` across {', '.join(f'`{g}`' for g in row['source_groups'])}")
    if dedup["hashes_matched_across_multiple_capital_scopes"]:
        lines += ["", "Hashes matching more than one capital scope:", ""]
        for row in dedup["hashes_matched_across_multiple_capital_scopes"]:
            lines.append(f"- `{row['sha256']}` across {', '.join(f'`{s}`' for s in row['scopes'])}")

    lines += ["", "## Reference-containment limits", ""]
    lines.append(report["audit"]["reference_containment_warning"])
    lines.append(
        "The three additional intake folders are taken only from FV's `supplied3_duplicate_check.candidate_source_folders` field. "
        "Broad search roots such as Downloads and the attachment archive were not recursively scanned. "
        "The report preserves the path that produced each match so a same-byte result across folders or labels is visible. "
        f"There are {len(report['audit']['selection']['explicit_external_target_files'])} explicit metadata file targets outside the selected directories; their exact paths and referring metadata are recorded in the JSON ledger."
    )
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    result = main()
    print(json.dumps({
        "report_json": str(OUT / "identity_report.json"),
        "report_markdown": str(OUT / "IDENTITY_REPORT.md"),
        "source_groups": result["source_manifest"]["computed_source_group_count"],
        "source_manifest_files": result["source_manifest"]["computed_file_count"],
        "observed_source_artifacts": result["exact_hash_dedup"]["source_artifacts_with_observed_hash"],
        "distinct_source_hashes": result["exact_hash_dedup"]["distinct_source_sha256_count"],
        "matched_distinct_hashes": result["exact_hash_dedup"]["distinct_source_sha256_matched"],
        "new_distinct_hashes": result["exact_hash_dedup"]["distinct_source_sha256_new_vs_selected_scope"],
    }, indent=2))
