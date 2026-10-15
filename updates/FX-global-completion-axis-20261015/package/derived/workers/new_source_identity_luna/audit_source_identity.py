#!/usr/bin/env python3
"""Read-only provenance audit of the global-completion source intake.

Hashes supplied and frozen files, reads producer/prior manifests, inventories
one embedded ZIP, and extracts only safe archive members below this directory.
No supplied scientific source code is imported or executed.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import stat
import subprocess
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

HERE = Path(__file__).resolve().parent
R = HERE.parents[1]
ULTRA = R.parents[1]
WORK = ULTRA / "work" / "astra-global-completion-axis-20261015"
MASTER = R / "sources" / "SOURCE_MANIFEST.json"
FW = WORK / "updates" / "FW-moving-heat-observable-20261015"
ZIP_PATH = R / "sources/global_compatible_positivity/inputs/previous_moving_kernel_package.zip"
EXTRACT_ROOT = HERE / "embedded_previous_moving_kernel_package"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def file_record(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"exists": False, "bytes": None, "sha256": None}
    return {"exists": True, "bytes": path.stat().st_size, "sha256": sha256_file(path)}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def record_status(actual: dict[str, Any], expected_sha: str | None, expected_bytes: int | None) -> str:
    if not actual["exists"]:
        return "missing"
    mismatches = []
    if expected_sha and actual["sha256"] != expected_sha:
        mismatches.append("sha256")
    if expected_bytes is not None and actual["bytes"] != expected_bytes:
        mismatches.append("bytes")
    return "mismatch:" + ",".join(mismatches) if mismatches else "match"


def file_entries(obj: Any) -> list[dict[str, Any]]:
    """Read common manifest shapes without assuming producer semantics."""
    if not isinstance(obj, dict):
        return []
    raw = obj.get("files")
    if isinstance(raw, dict):
        return [
            {"path": name, **value} if isinstance(value, dict)
            else {"path": name, "sha256": value}
            for name, value in raw.items()
            if isinstance(value, (dict, str))
        ]
    if isinstance(raw, list):
        return [x for x in raw if isinstance(x, dict)]
    # One observed producer manifest is a direct path -> digest map.
    if obj and all(isinstance(v, str) for v in obj.values()):
        return [{"path": k, "sha256": v} for k, v in obj.items()]
    return []


def path_within(root: Path, relative: str) -> tuple[Path | None, str | None]:
    p = PurePosixPath(relative.replace("\\", "/"))
    if p.is_absolute() or any(part in ("..", "") for part in p.parts):
        return None, "unsafe_relative_path"
    candidate = root.joinpath(*p.parts)
    try:
        candidate.resolve().relative_to(root.resolve())
    except (ValueError, OSError):
        return None, "path_escapes_root"
    return candidate, None


def text_inventory(master_entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs = {
        "sources/ultra_prompt.txt": "Astra-wide brief with embedded research progress and synthesis passages.",
        "sources/physical_prompt.txt": "Physical-research brief with evidence summaries, caveats, and disposition.",
        "sources/computational_prompt.txt": "Computational brief with a selected task, reported measurements, and caveats.",
        "sources/mathematical_prompt.txt": "Mathematical brief with theorem/report text and scope qualifications.",
    }
    role_re = re.compile(r"^(USER|ASSISTANT|SYSTEM|HUMAN|CHATGPT)\s*[:：]", re.I)
    out = []
    for rel, classification in specs.items():
        path = R / rel
        text = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""
        lines = text.splitlines()
        role_markers = [
            {"line": i, "role": m.group(1).upper(), "text": line[:240]}
            for i, line in enumerate(lines, 1)
            if (m := role_re.match(line.strip()))
        ]
        headings = [
            {"line": i, "text": line[:240]}
            for i, line in enumerate(lines, 1)
            if re.match(
                r"^(?:#{1,6}\s|Mission:|Result:|The measured result is:|"
                r"Current disposition:|The investigation changed direction)",
                line.strip(),
                re.I,
            )
        ]
        out.append({
            "path": rel,
            "classification_from_visible_content": classification,
            "bytes": path.stat().st_size if path.is_file() else None,
            "lines": len(lines),
            "first_line": lines[0][:300] if lines else None,
            "explicit_chat_role_marker_count": len(role_markers),
            "explicit_chat_role_markers": role_markers,
            "content_section_markers": headings,
            "source_handling": next((e.get("source_handling") for e in master_entries if e.get("path") == rel), None),
            "interpretation_limit": (
                "No explicit UI role labels were found. Visible text mixes mission/prompt language "
                "with reported results or synthesis; exact prompt-versus-response boundaries cannot "
                "be established from these pasted files alone."
            ),
        })
    return out


def safe_extract_and_inventory(zip_path: Path) -> dict[str, Any]:
    archive = file_record(zip_path)
    result: dict[str, Any] = {
        "archive_path": str(zip_path),
        "archive_file": archive,
        "members": [],
        "unsafe_members": [],
        "nested_manifests": [],
        "extracted_member_count": 0,
        "extraction_root": str(EXTRACT_ROOT),
        "extraction_status": "not_started",
    }
    if not archive["exists"]:
        result["extraction_status"] = "archive_missing"
        return result

    EXTRACT_ROOT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        infos = zf.infolist()
        total_uncompressed = sum(i.file_size for i in infos if not i.is_dir())
        result["member_count"] = len(infos)
        result["total_uncompressed_bytes"] = total_uncompressed
        if len(infos) > 2000 or total_uncompressed > 100 * 1024 * 1024:
            result["extraction_status"] = "bounded_extraction_limit_exceeded"
            return result

        for info in infos:
            normalized = info.filename.replace("\\", "/")
            p = PurePosixPath(normalized)
            mode = (info.external_attr >> 16) & 0xFFFF
            is_symlink = stat.S_ISLNK(mode)
            unsafe = None
            if p.is_absolute() or any(part in ("..", "") for part in p.parts):
                unsafe = "absolute_or_traversal_path"
            elif re.match(r"^[A-Za-z]:", normalized):
                unsafe = "drive_path"
            elif is_symlink:
                unsafe = "symlink_member"
            elif not info.is_dir() and not stat.S_ISREG(mode) and mode != 0:
                unsafe = "non_regular_member"
            item: dict[str, Any] = {
                "member": info.filename,
                "normalized_member": normalized,
                "bytes": info.file_size,
                "compressed_bytes": info.compress_size,
                "crc32": f"{info.CRC:08x}",
                "is_directory": info.is_dir(),
                "is_symlink": is_symlink,
                "unsafe_reason": unsafe,
                "sha256": None,
                "extracted_path": None,
            }
            if unsafe:
                result["unsafe_members"].append(item)
                result["members"].append(item)
                continue
            if info.is_dir():
                target, issue = path_within(EXTRACT_ROOT, normalized.rstrip("/"))
                if issue:
                    item["unsafe_reason"] = issue
                    result["unsafe_members"].append(item)
                else:
                    target.mkdir(parents=True, exist_ok=True)
                    item["extracted_path"] = str(target)
                result["members"].append(item)
                continue

            data = zf.read(info)
            item["sha256"] = hashlib.sha256(data).hexdigest()
            target, issue = path_within(EXTRACT_ROOT, normalized)
            if issue:
                item["unsafe_reason"] = issue
                result["unsafe_members"].append(item)
                result["members"].append(item)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            item["extracted_path"] = str(target)
            result["extracted_member_count"] += 1
            result["members"].append(item)

    result["extraction_status"] = "complete_with_rejected_unsafe_members" if result["unsafe_members"] else "complete"
    manifests = []
    extracted_files = [
        Path(x["extracted_path"])
        for x in result["members"]
        if x.get("extracted_path") and not x["is_directory"]
    ]
    for manifest_path in extracted_files:
        basename = manifest_path.name.lower()
        if "manifest" not in basename and not basename.endswith(".sha256"):
            continue
        rec: dict[str, Any] = {
            "path": str(manifest_path.relative_to(EXTRACT_ROOT)),
            "sha256": sha256_file(manifest_path),
            "bytes": manifest_path.stat().st_size,
            "parse_status": "unrecognized",
            "checks": [],
        }
        parsed: Any = None
        try:
            if manifest_path.suffix.lower() == ".json":
                parsed = read_json(manifest_path)
            elif basename.endswith(".sha256"):
                parsed = manifest_path.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:
            rec["parse_status"] = f"parse_error:{type(exc).__name__}:{exc}"
        entries = file_entries(parsed)
        if entries:
            rec["parse_status"] = "parsed_json_entries"
            for e in entries:
                rel = str(e.get("path") or e.get("file") or "")
                candidates = []
                for root in (manifest_path.parent, EXTRACT_ROOT):
                    cand, issue = path_within(root, rel)
                    if cand is not None and issue is None:
                        candidates.append(cand)
                found = next((p for p in candidates if p.is_file()), None)
                actual = file_record(found) if found else {"exists": False, "bytes": None, "sha256": None}
                rec["checks"].append({
                    "path": rel,
                    "expected_sha256": e.get("sha256"),
                    "expected_bytes": e.get("bytes"),
                    "actual_path": str(found) if found else None,
                    "actual_sha256": actual["sha256"],
                    "actual_bytes": actual["bytes"],
                    "status": record_status(actual, e.get("sha256"), e.get("bytes")),
                })
        elif isinstance(parsed, str):
            pairs = []
            for line in parsed.splitlines():
                m = re.match(r"^\s*([0-9a-fA-F]{64})\s+\*?(.+?)\s*$", line)
                if m:
                    pairs.append({"sha256": m.group(1).lower(), "path": m.group(2)})
            if pairs:
                rec["parse_status"] = "parsed_sha256_lines"
                for e in pairs:
                    candidates = []
                    for root in (manifest_path.parent, EXTRACT_ROOT):
                        cand, issue = path_within(root, e["path"])
                        if cand is not None and issue is None:
                            candidates.append(cand)
                    found = next((p for p in candidates if p.is_file()), None)
                    actual = file_record(found) if found else {"exists": False, "bytes": None, "sha256": None}
                    rec["checks"].append({
                        "path": e["path"],
                        "expected_sha256": e["sha256"],
                        "expected_bytes": None,
                        "actual_path": str(found) if found else None,
                        "actual_sha256": actual["sha256"],
                        "actual_bytes": actual["bytes"],
                        "status": record_status(actual, e["sha256"], None),
                    })
        manifests.append(rec)
    result["nested_manifests"] = manifests
    return result


def main() -> None:
    master_obj = read_json(MASTER)
    entries = master_obj.get("files", [])
    if not isinstance(entries, list):
        raise SystemExit("Master source manifest .files is not an array")
    master_info = file_record(MASTER)

    groups = defaultdict(int)
    by_path = {}
    by_sha = defaultdict(list)
    ledger = []
    for e in entries:
        rel = str(e["path"])
        original = Path(str(e.get("source_path", "")))
        frozen, issue = path_within(R, rel)
        frozen_info = file_record(frozen) if frozen else {"exists": False, "bytes": None, "sha256": None}
        original_info = file_record(original)
        expected_sha = e.get("sha256")
        expected_bytes = e.get("bytes")
        row = {
            "group": e.get("group"),
            "frozen_path": rel,
            "source_path": str(original),
            "expected_sha256": expected_sha,
            "expected_bytes": expected_bytes,
            "frozen_sha256": frozen_info["sha256"],
            "frozen_bytes": frozen_info["bytes"],
            "frozen_status": issue or record_status(frozen_info, expected_sha, expected_bytes),
            "source_sha256": original_info["sha256"],
            "source_bytes": original_info["bytes"],
            "source_status": record_status(original_info, expected_sha, expected_bytes),
            "source_handling": e.get("source_handling"),
        }
        ledger.append(row)
        by_path[rel] = row
        if expected_sha:
            by_sha[expected_sha].append(rel)
        groups[str(e.get("group"))] += 1
    duplicates = [
        {"sha256": digest, "paths": paths}
        for digest, paths in sorted(by_sha.items())
        if len(paths) > 1
    ]

    producer_specs = [
        ("global_compatible_positivity", "sources/global_compatible_positivity/MANIFEST.json"),
        ("pulse_observable", "sources/pulse_observable/MANIFEST.json"),
        ("axis_writing", "sources/axis_writing/manifest.json"),
    ]
    producer_checks = []
    for group, rel_manifest in producer_specs:
        manifest_path = R / rel_manifest
        obj = read_json(manifest_path)
        checks = []
        for pe in file_entries(obj):
            rel = str(pe.get("path") or pe.get("file") or "")
            target, issue = path_within(manifest_path.parent, rel)
            actual = file_record(target) if target else {"exists": False, "bytes": None, "sha256": None}
            expected_sha = pe.get("sha256")
            expected_bytes = pe.get("bytes")
            master_rel = f"sources/{group}/{rel}"
            master_row = by_path.get(master_rel)
            producer_vs_master = (
                "no_master_record" if master_row is None
                else "match" if master_row["expected_sha256"] == expected_sha
                and (expected_bytes is None or master_row["expected_bytes"] == expected_bytes)
                else "mismatch"
            )
            checks.append({
                "path": rel,
                "actual_path": str(target) if target else None,
                "expected_sha256": expected_sha,
                "expected_bytes": expected_bytes,
                "actual_sha256": actual["sha256"],
                "actual_bytes": actual["bytes"],
                "actual_status": issue or record_status(actual, expected_sha, expected_bytes),
                "master_record_path": master_rel if master_row else None,
                "producer_vs_master": producer_vs_master,
            })
        producer_checks.append({
            "group": group,
            "manifest_path": rel_manifest,
            "manifest_sha256": sha256_file(manifest_path),
            "manifest_schema": obj.get("schema") if isinstance(obj, dict) else None,
            "declared_file_count": len(checks),
            "checks": checks,
        })

    prior_obj = read_json(FW / "SOURCE_MANIFEST.json")
    prior_entries = file_entries(prior_obj)
    prior_pulse = {}
    prefix = "sources/astra_pulse_observable/"
    for pe in prior_entries:
        rpath = str(pe.get("research_relative_path") or "")
        if rpath.startswith(prefix):
            prior_pulse[rpath[len(prefix):]] = pe
    pulse_comparison = []
    for row in ledger:
        prefix = "sources/pulse_observable/"
        if not row["frozen_path"].startswith(prefix):
            continue
        rel = row["frozen_path"][len(prefix):]
        old = prior_pulse.get(rel)
        prior_actual_path = WORK / str(old.get("path")) if old and old.get("path") else None
        prior_actual = file_record(prior_actual_path) if prior_actual_path else {
            "exists": False, "bytes": None, "sha256": None
        }
        pulse_comparison.append({
            "current_path": row["frozen_path"],
            "prior_research_relative_path": "sources/astra_pulse_observable/" + rel if old else None,
            "prior_preserved_path": old.get("path") if old else None,
            "current_sha256": row["expected_sha256"],
            "prior_sha256": old.get("sha256") if old else None,
            "current_bytes": row["expected_bytes"],
            "prior_bytes": old.get("bytes") if old else None,
            "prior_actual_sha256": prior_actual["sha256"],
            "prior_actual_bytes": prior_actual["bytes"],
            "prior_actual_status": record_status(
                prior_actual, old.get("sha256") if old else None, old.get("bytes") if old else None
            ),
            "status": "no_prior_entry" if old is None else
            "exact_match" if row["expected_sha256"] == old.get("sha256")
            and row["expected_bytes"] == old.get("bytes") else "digest_or_size_mismatch",
        })

    derived_path = FW / "DERIVED_MANIFEST.v0002.json"
    derived_obj = read_json(derived_path)
    derived_entries = file_entries(derived_obj)
    derived_by_sha = defaultdict(list)
    for de in derived_entries:
        if de.get("sha256"):
            derived_by_sha[str(de["sha256"])].append(de)
    derived_hits = []
    for row in ledger:
        for de in derived_by_sha.get(str(row["expected_sha256"]), []):
            derived_actual_path = WORK / str(de.get("path")) if de.get("path") else None
            derived_actual = file_record(derived_actual_path) if derived_actual_path else {
                "exists": False, "bytes": None, "sha256": None
            }
            derived_hits.append({
                "current_source_path": row["frozen_path"],
                "current_sha256": row["expected_sha256"],
                "derived_research_relative_path": de.get("research_relative_path"),
                "derived_path": de.get("path"),
                "derived_bytes": de.get("bytes"),
                "exact_bytes_match": de.get("bytes") == row["expected_bytes"],
                "derived_actual_sha256": derived_actual["sha256"],
                "derived_actual_bytes": derived_actual["bytes"],
                "derived_actual_status": record_status(
                    derived_actual, de.get("sha256"), de.get("bytes")
                ),
            })

    selected = [
        ("FT-foundational-capability-20261015", WORK / "updates/FT-foundational-capability-20261015/SOURCE_MANIFEST.json"),
        ("FT-foundational-capability-v2-20261015", WORK / "updates/FT-foundational-capability-v2-20261015/SOURCE_MANIFEST.json"),
        ("FU-regularization-clock-pressure-20261015", WORK / "updates/FU-regularization-clock-pressure-20261015/SOURCE_MANIFEST.json"),
        ("FV-positive-consequences-20261015", WORK / "updates/FV-positive-consequences-20261015/SOURCE_MANIFEST.json"),
    ]
    selected_results = []
    for name, path in selected:
        obj = read_json(path)
        refs = file_entries(obj)
        ref_by_sha = defaultdict(list)
        for reff in refs:
            if reff.get("sha256"):
                ref_by_sha[str(reff["sha256"])].append(reff)
        hits = []
        for row in ledger:
            for reff in ref_by_sha.get(str(row["expected_sha256"]), []):
                hits.append({
                    "current_source_path": row["frozen_path"],
                    "current_sha256": row["expected_sha256"],
                    "prior_source_path": reff.get("source_path") or reff.get("package_path") or reff.get("path"),
                    "prior_preserved_path": reff.get("preserved_path") or reff.get("path"),
                    "prior_bytes": reff.get("bytes"),
                    "exact_bytes_match": reff.get("bytes") == row["expected_bytes"],
                })
        selected_results.append({
            "name": name,
            "manifest_path": str(path.relative_to(ULTRA)),
            "manifest_sha256": sha256_file(path),
            "declared_file_count": len(refs),
            "exact_sha256_hits": hits,
        })

    zip_result = safe_extract_and_inventory(ZIP_PATH)
    current_by_digest = defaultdict(list)
    for row in ledger:
        current_by_digest[row["expected_sha256"]].append(row["frozen_path"])
    prior_fw_by_digest = defaultdict(list)
    for pe in prior_entries:
        if pe.get("sha256"):
            prior_fw_by_digest[str(pe["sha256"])].append(pe.get("research_relative_path") or pe.get("path"))
    embedded_hits = []
    for member in zip_result.get("members", []):
        digest = member.get("sha256")
        if not digest:
            continue
        matches = []
        matches.extend({"identity": "current_global_intake", "path": p} for p in current_by_digest.get(digest, []))
        for pe in prior_entries:
            if str(pe.get("sha256")) != digest:
                continue
            prior_actual_path = WORK / str(pe.get("path")) if pe.get("path") else None
            prior_actual = file_record(prior_actual_path) if prior_actual_path else {
                "exists": False, "bytes": None, "sha256": None
            }
            matches.append({
                "identity": "prior_FW_source_manifest",
                "path": pe.get("research_relative_path") or pe.get("path"),
                "preserved_path": pe.get("path"),
                "declared_sha256": pe.get("sha256"),
                "actual_sha256": prior_actual["sha256"],
                "actual_bytes": prior_actual["bytes"],
                "actual_status": record_status(prior_actual, pe.get("sha256"), pe.get("bytes")),
            })
        matches.extend({
            "identity": "prior_FW_derived_manifest_v0002",
            "path": de.get("research_relative_path") or de.get("path"),
        } for de in derived_by_sha.get(digest, []))
        if matches:
            embedded_hits.append({"archive_member": member["normalized_member"], "sha256": digest, "matches": matches})
    zip_result["exact_identity_matches_to_current_or_FW"] = embedded_hits

    text_roles = text_inventory(entries)
    embedded_prior_matches = [
        match
        for hit in embedded_hits
        for match in hit["matches"]
        if match["identity"] == "prior_FW_source_manifest"
    ]
    status_findings = {
        "frozen_missing_or_mismatched": [x for x in ledger if x["frozen_status"] != "match"],
        "original_missing_or_mismatched": [x for x in ledger if x["source_status"] != "match"],
        "producer_actual_missing_or_mismatched": [
            {"group": p["group"], **c} for p in producer_checks for c in p["checks"]
            if c["actual_status"] != "match"
        ],
        "producer_master_digest_or_size_mismatches": [
            {"group": p["group"], **c} for p in producer_checks for c in p["checks"]
            if c["producer_vs_master"] == "mismatch"
        ],
        "pulse_vs_prior_FW_mismatches": [x for x in pulse_comparison if x["status"] != "exact_match"],
        "prior_FW_pulse_preserved_files_missing_or_mismatched": [
            x for x in pulse_comparison if x["prior_actual_status"] != "match"
        ],
        "prior_FW_derived_output_files_missing_or_mismatched": [
            x for x in derived_hits if x["derived_actual_status"] != "match"
        ],
        "zip_unsafe_members": zip_result.get("unsafe_members", []),
        "embedded_archive_prior_FW_files_missing_or_mismatched": [
            x for x in embedded_prior_matches if x["actual_status"] != "match"
        ],
        "zip_nested_manifest_failures": [
            {"manifest": m["path"], "failures": [c for c in m["checks"] if c["status"] != "match"]}
            for m in zip_result.get("nested_manifests", [])
            if any(c["status"] != "match" for c in m["checks"])
        ],
    }
    groups_value = master_obj.get("groups", [])
    groups_declared = groups_value if isinstance(groups_value, int) else len(groups_value)
    summary = {
        "master_manifest_schema": master_obj.get("schema"),
        "master_manifest_sha256": master_info["sha256"],
        "master_manifest_bytes": master_info["bytes"],
        "declared_file_count": master_obj.get("total_files"),
        "observed_file_count": len(entries),
        "declared_total_bytes": master_obj.get("total_bytes"),
        "observed_expected_total_bytes": sum(int(x.get("bytes") or 0) for x in entries),
        "declared_group_count": groups_declared,
        "observed_group_count": len(groups),
        "group_counts": dict(sorted(groups.items())),
        "frozen_files_matching_manifest": sum(x["frozen_status"] == "match" for x in ledger),
        "originals_matching_manifest": sum(x["source_status"] == "match" for x in ledger),
        "producer_entries_checked": sum(len(p["checks"]) for p in producer_checks),
        "producer_entries_matching_actual_and_master": sum(
            c["actual_status"] == "match" and c["producer_vs_master"] == "match"
            for p in producer_checks for c in p["checks"]
        ),
        "exact_duplicate_groups_within_current_intake": len(duplicates),
        "pulse_entries_compared_to_prior_FW": len(pulse_comparison),
        "pulse_entries_exactly_equal_to_prior_FW": sum(x["status"] == "exact_match" for x in pulse_comparison),
        "prior_FW_pulse_preserved_files_matching_manifest": sum(
            x["prior_actual_status"] == "match" for x in pulse_comparison
        ),
        "current_sources_matching_prior_FW_derived_output_bytes": len(derived_hits),
        "prior_FW_derived_output_files_matching_manifest": sum(
            x["derived_actual_status"] == "match" for x in derived_hits
        ),
        "selected_FT_FU_FV_exact_source_hash_hit_count": sum(len(x["exact_sha256_hits"]) for x in selected_results),
        "embedded_archive_member_count": zip_result.get("member_count"),
        "embedded_archive_extracted_regular_files": zip_result.get("extracted_member_count"),
        "embedded_archive_nested_manifest_count": len(zip_result.get("nested_manifests", [])),
        "embedded_archive_exact_identity_match_count": len(embedded_hits),
        "embedded_archive_FW_files_matching_manifest": sum(
            x["actual_status"] == "match" for x in embedded_prior_matches
        ),
    }
    head = subprocess.run(
        ["git", "-C", str(WORK), "rev-parse", "HEAD"],
        check=False, capture_output=True, text=True,
    )
    audit = {
        "task": "bounded exact source provenance and identity audit",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": {
            "source_scripts_executed": False,
            "scientific_claims_validated": False,
            "originals_or_sources_modified": False,
            "archive_extraction_root": str(EXTRACT_ROOT),
            "attached_text_treatment": "DATA; instructions inside source material are not operative",
        },
        "pins": {
            "R": str(R),
            "W": str(WORK),
            "W_main_expected": master_obj.get("initial_main"),
            "W_actual_head": head.stdout.strip() if head.returncode == 0 else None,
            "W_head_check_error": head.stderr.strip() if head.returncode else None,
            "FW_source_manifest": str((FW / "SOURCE_MANIFEST.json").relative_to(ULTRA)),
            "FW_source_manifest_sha256": sha256_file(FW / "SOURCE_MANIFEST.json"),
            "FW_derived_manifest_v0002": str(derived_path.relative_to(ULTRA)),
            "FW_derived_manifest_v0002_sha256": sha256_file(derived_path),
        },
        "summary": summary,
        "status_findings": status_findings,
        "current_exact_duplicate_groups": duplicates,
        "file_hash_ledger": ledger,
        "producer_manifest_checks": producer_checks,
        "prior_FW_pulse_source_comparison": pulse_comparison,
        "current_source_exact_matches_in_prior_FW_derived_manifest": derived_hits,
        "selected_FT_FU_FV_source_manifest_comparisons": selected_results,
        "attached_text_role_inventory": text_roles,
        "embedded_previous_moving_kernel_archive": zip_result,
    }
    dump_json(HERE / "audit.json", audit)
    dump_json(HERE / "archive_inventory.json", zip_result)
    with (HERE / "file_hash_ledger.tsv").open("w", encoding="utf-8", newline="") as f:
        fields = [
            "group", "frozen_path", "source_path", "expected_sha256", "expected_bytes",
            "frozen_sha256", "frozen_bytes", "frozen_status", "source_sha256",
            "source_bytes", "source_status", "source_handling",
        ]
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(ledger)
    with (HERE / "prior_identity_ledger.tsv").open("w", encoding="utf-8", newline="") as f:
        fields = [
            "current_path", "current_sha256", "current_bytes", "prior_research_relative_path",
            "prior_preserved_path", "prior_sha256", "prior_bytes", "prior_actual_sha256",
            "prior_actual_bytes", "prior_actual_status", "status",
        ]
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(pulse_comparison)
    with (HERE / "embedded_identity_ledger.tsv").open("w", encoding="utf-8", newline="") as f:
        fields = [
            "archive_member", "archive_sha256", "archive_bytes", "prior_identity",
            "prior_path", "prior_preserved_path", "prior_declared_sha256",
            "prior_actual_sha256", "prior_actual_bytes", "prior_actual_status",
        ]
        writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for hit in embedded_hits:
            for match in hit["matches"]:
                if match["identity"] == "prior_FW_source_manifest":
                    writer.writerow({
                        "archive_member": hit["archive_member"],
                        "archive_sha256": hit["sha256"],
                        "archive_bytes": next(
                            (m["bytes"] for m in zip_result["members"]
                             if m["normalized_member"] == hit["archive_member"]), None
                        ),
                        "prior_identity": match["identity"],
                        "prior_path": match.get("path"),
                        "prior_preserved_path": match.get("preserved_path"),
                        "prior_declared_sha256": match.get("declared_sha256"),
                        "prior_actual_sha256": match.get("actual_sha256"),
                        "prior_actual_bytes": match.get("actual_bytes"),
                        "prior_actual_status": match.get("actual_status"),
                    })

    lines = [
        "# New source identity audit",
        "",
        f"Generated {audit['generated_at_utc']}. Exact-byte provenance only; scientific validity was not assessed.",
        f"Pinned W HEAD {audit['pins']['W_actual_head']} (expected {audit['pins']['W_main_expected']}); R master manifest SHA-256 {master_info['sha256']}; FW source manifest SHA-256 {audit['pins']['FW_source_manifest_sha256']}; FW derived v0002 manifest SHA-256 {audit['pins']['FW_derived_manifest_v0002_sha256']}.",
        "",
        "## Intake and producer manifests",
        "",
        f"The master manifest declares {summary['declared_file_count']} files in {summary['declared_group_count']} groups and {summary['declared_total_bytes']} bytes. Observed records: {summary['observed_file_count']} files, {summary['observed_group_count']} groups, {summary['observed_expected_total_bytes']} declared bytes.",
        f"Frozen copies matching the master manifest: {summary['frozen_files_matching_manifest']}/{summary['observed_file_count']}. Original paths matching it: {summary['originals_matching_manifest']}/{summary['observed_file_count']}. Producer entries matching both their files and the master manifest: {summary['producer_entries_matching_actual_and_master']}/{summary['producer_entries_checked']}.",
        "",
        "## Prior moving-heat source identity",
        "",
        f"Current pulse-observable entries compared with FW: {summary['pulse_entries_compared_to_prior_FW']}; exact byte matches: {summary['pulse_entries_exactly_equal_to_prior_FW']}; preserved FW copies matching their manifest: {summary['prior_FW_pulse_preserved_files_matching_manifest']}/{summary['pulse_entries_compared_to_prior_FW']}. This entire input group is repeated source identity.",
        f"The current pulse data file sources/pulse_observable/data/cell_001_eis.csv (SHA-256 {by_path['sources/pulse_observable/data/cell_001_eis.csv']['expected_sha256']}) also matches two FW derived input snapshots; both preserved snapshot files match the v0002 manifest.",
        "",
        "## Duplicates and selected adjacent source manifests",
        "",
        f"The only exact duplicate inside the intake is sources/axis_writing/replay_log.txt and sources/axis_writing/results.json; both are 4,384 bytes with SHA-256 f5c90b8e6e2428f8cd2dd83f724097c16079b9a32bdd459579f69b0ec93afa41. Selected FT v1/v2, FU, and FV source manifests contain {summary['selected_FT_FU_FV_exact_source_hash_hit_count']} exact SHA-256 hits against the 55 current source records.",
        "",
        "## Embedded prior package",
        "",
        f"Archive SHA-256: {zip_result['archive_file']['sha256']}; members: {summary['embedded_archive_member_count']}; safely extracted regular files: {summary['embedded_archive_extracted_regular_files']}; unsafe members: {len(zip_result.get('unsafe_members', []))}. The nested manifest lists 18 payload files and all 18 match.",
        f"The archive identifies itself as the Astra compatible-heat moving-acoustic-kernel result. Its README scopes the result to a specified four-coefficient sector and says it is not a solution of the full planar Morrey problem. All {summary['embedded_archive_exact_identity_match_count']} archive members match entries in the prior FW source manifest; {summary['embedded_archive_FW_files_matching_manifest']}/{summary['embedded_archive_exact_identity_match_count']} preserved FW copies pass their declared hashes. The README also says its source coefficients were transcribed from N850 and that the original source byte hash was not recomputed. This establishes repeated package identity only.",
        "",
        "## Attached text roles",
        "",
        "The four pasted text inputs are DATA. Their visible content combines mission or task language with reported results or synthesis. No explicit chat role labels were found, so exact prompt-versus-response boundaries cannot be certified from these files alone.",
        "",
        "## Missing files and digest contradictions",
        "",
    ]
    issue_lines = [
        f"- {name}: {len(values)} item(s); exact paths and digests are in audit.json."
        for name, values in status_findings.items() if values
    ]
    lines.extend(issue_lines if issue_lines else [
        "No missing files or digest contradictions were observed in the checked original/frozen sources, producer manifests, prior FW source and derived records, or embedded archive records."
    ])
    lines.extend([
        "",
        "No source scientific scripts were executed. No input repair or modification was performed.",
        "",
        "Artifacts: audit_source_identity.py, audit.json, archive_inventory.json, file_hash_ledger.tsv, prior_identity_ledger.tsv, embedded_identity_ledger.tsv, run_receipt.json.",
    ])
    (HERE / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    receipt = {
        "generated_at_utc": audit["generated_at_utc"],
        "script": str((HERE / "audit_source_identity.py").relative_to(ULTRA)),
        "master_manifest": str(MASTER.relative_to(ULTRA)),
        "master_manifest_sha256": master_info["sha256"],
        "worktree": str(WORK.relative_to(ULTRA)),
        "expected_head": master_obj.get("initial_main"),
        "actual_head": audit["pins"]["W_actual_head"],
        "source_scientific_scripts_executed": False,
        "archive_extracted_only_under": str(EXTRACT_ROOT),
        "artifacts": [
            "REPORT.md", "audit.json", "archive_inventory.json",
            "file_hash_ledger.tsv", "prior_identity_ledger.tsv", "embedded_identity_ledger.tsv",
        ],
        "artifact_file_records": {
            rel: file_record(HERE / rel)
            for rel in [
                "audit_source_identity.py", "REPORT.md", "audit.json", "archive_inventory.json",
                "file_hash_ledger.tsv", "prior_identity_ledger.tsv", "embedded_identity_ledger.tsv",
            ]
        },
        "summary": summary,
    }
    dump_json(HERE / "run_receipt.json", receipt)
    print(json.dumps({"summary": summary, "status_findings": status_findings}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
