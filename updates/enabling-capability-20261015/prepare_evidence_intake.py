#!/usr/bin/env python3
"""Copy a curated evidence snapshot without executing or editing worker inputs.

This is preservation tooling, not a scientific validator. Excluded sources and
dependencies remain necessary for some replays. A final resync is root-owned.
"""
from __future__ import annotations

import argparse
import ast
import collections
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys


PRUNE = {
    ".venv": "installed_environment",
    "venv": "installed_environment",
    ".python_packages": "installed_dependencies",
    "deps": "installed_dependencies",
    "wheels": "dependency_wheel_archive",
    "node_modules": "installed_dependencies",
    ".git": "git_metadata",
    "__pycache__": "generated_bytecode_cache",
    "source_code": "third_party_source_repository",
    "kiwiclient": "third_party_source_repository",
    "kozlowski_code": "publisher_source_code",
    "kozlowski_lcms": "extracted_raw_measurement_archive",
    "kozlowski_nmr": "extracted_raw_measurement_archive",
    "magnetstein_data": "extracted_raw_measurement_archive",
    "magnetstein_repository": "third_party_source_repository",
    "mcdonald_data": "extracted_raw_measurement_archive",
    "mcdonald_figure_data": "extracted_publisher_figure_archive",
    "acquired": "acquired_raw_archive_or_extraction_tree",
    "published_data": "publisher_data_and_source_code",
    "tmp": "temporary_extracted_sources",
}

NUMERICAL = {
    "computation_search/fast_vector.npy": "worker_computed_corrected_incumbent_vector",
    "computation_search/reference_vector.npy": "worker_computed_historical_vector",
    "s05_energy_certificates/exact_decimal_hamiltonian.npz": "worker_assembled_compact_exact_input",
    "s09_lif_null/paper_35_55_eV_FROZEN.npz": "worker_frozen_fitted_model",
    "s09_lif_null/script_first_1025_pixels_FROZEN.npz": "worker_frozen_fitted_model",
    "a03_manybody_invention/random_probe_bits.bin": "worker_recorded_random_bits",
    "computation_search/source/data/N2.STO3G.FCIDUMP": "compact_public_source_numerical_input; upstream GPL3 notice retained",
    "s07_remote_control/data/20261015T052637Z_10000000_KFS_current_route_10MHz_iq.wav": "compact_unique_worker_acquired_measurement_record; original bytes and receipt retained",
}

REPORTS = {
    "a01_assay_operation": ["OPERATION_AUDIT.txt", "RESULT.json"],
    "a02_intervention_theory": ["THEORY.txt", "STATUS.json"],
    "a03_manybody_invention": ["THEORY.txt", "RANDOMIZED_SIGNED_CERTIFICATE.json"],
    "a04_spectral_control": ["REPORT.txt", "LIFETIME_PROFILE.json"],
    "a05_energy_matter": ["REPORT.txt", "RESULTS.json"],
    "a06_manufacturing_operations": ["REPORT.txt", "FINAL_CHECK.json"],
    "a07_foundation_independent": ["REPORT.txt", "EXACT_RESULTS.txt"],
    "a08_grouped_werner": ["STATUS.txt", "AUDIT.txt", "UNIFORM_SCHMIDT_PROOF.txt", "uniform_schmidt.json"],
    "a09_photon_invention": ["MEASUREMENT_OPERATION_AND_PROOFS.txt", "EXACT_CHECKS.json"],
    "a10_selection_challenge": ["MATHEMATICAL_MECHANISM.txt", "NETWORK_AUDIT.json"],
    "capital_interface": ["REPORT_v0002.txt", "REPORT_v0002.json"],
    "chemical_information": ["MECHANISM_DECISION.txt", "SUMMARY.json"],
    "chemistry_evidence": ["EVIDENCE_AUDIT.txt", "AUDIT_HANDOFF.json"],
    "chemistry_incumbent": ["INCUMBENT_PROCEDURE.txt", "INCUMBENT_AUDIT.json"],
    "chemistry_search": ["RESULT.txt", "GATES.json"],
    "computation_search": ["OPERATION_AND_FAILURE_v0002.txt", "LATEST.txt", "CORRECTION_004.txt", "FINAL_AMENDMENT_004.txt"],
    "foundation": ["REPORT.txt", "TENSOR_INTERFACE_PROOF.txt"],
    "foundation_audit": ["RESTRICTED_SECTOR_CONSEQUENCE_AUDIT.txt", "AUDIT_STATUS.json"],
    "measurement_search": ["FOLLOW_ON_RECOMMENDATION.txt", "HANDOFF.json"],
    "premise_challenge": ["PREMISE_AUDIT.txt", "SOURCE_SCOPE_CORRECTION_v0001.json", "SYNTHESIS_AUDIT.txt"],
    "s01_chemistry_targets": ["REPORT.txt", "DECISION_OPERATION.json"],
    "s02_assay_access": ["RESULT.txt", "ASSAY_AUDIT_RESULTS.json"],
    "s03_materials_output": ["FROZEN_DIAGNOSTIC.txt", "VALIDATION_AND_COST_RESULTS.json"],
    "s04_scattering": ["CHECKPOINT.txt", "HPM_endpoint_audit.json"],
    "s05_energy_certificates": ["PROOF_AND_DECISION.txt", "CERTIFICATE_RECEIPT.json", "inputs/CORRECTION_004.txt", "inputs/FINAL_AMENDMENT_004.txt"],
    "s06_molecular_kinetics": ["KINETIC_REPLAY.json", "CLOCK_REPRESENTATION_CONTROLS.json", "ACQUIRED_ATOMISTIC_PATHS.json"],
    "s07_remote_control": ["REPORT_v0001.txt", "IDENTIFIABILITY_v0001.txt", "ACTUAL_IQ_AUDIT_v0001.json"],
    "s08_photon_evidence": ["REPORT.txt", "BASELINE_SUMMARY.json"],
    "s09_lif_null": ["HELDOUT_RESULTS.json", "CALIBRATION_AND_LEAKAGE_LEDGER.json"],
    "s10_foundation_compute": ["RESULT.txt", "UNIFORM_AUDIT.txt", "uniform_sharp_audit.json"],
}

SOURCE_LICENSES = {
    "computation_search/source/LICENSE": "upstream_GPL3_license_notice",
    "s08_photon_evidence/AUTHOR_BSD_LICENSE.txt": "upstream_BSD_license_notice",
    "premise_challenge/AUTHOR_LICENSE.txt.txt": "upstream_license_notice",
}

TEXT = {".txt", ".md", ".json", ".jsonl", ".py", ".log", ".csv", ".tsv", ".toml", ".yaml", ".yml", ".ipynb", ".r", ".m"}
RAW_EXT = {".zip", ".gz", ".tgz", ".bz2", ".xz", ".tar", ".parquet", ".h5", ".hdf5", ".wav", ".spc", ".xlsx", ".xls", ".tif", ".tiff", ".mzxml", ".fid"}
ROOT_EXCLUDE = {
    "spectral_deconvolution.py": "copied_publisher_source_code; explicitly excluded by root",
    "PR_BODY.txt": "editorial_publication_metadata; not scientific evidence",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def stable_read(path: Path) -> tuple[bytes, os.stat_result]:
    before = path.stat()
    data = path.read_bytes()
    after = path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise RuntimeError(f"Worker file changed during snapshot: {path}")
    if len(data) != after.st_size:
        raise RuntimeError(f"Size mismatch while copying: {path}")
    return data, after


def directory_stat(path: Path) -> dict:
    count = total = symlinks = 0
    for here, dirs, names in os.walk(path, followlinks=False):
        dirs[:] = [d for d in dirs if not (Path(here) / d).is_symlink()]
        for name in names:
            p = Path(here) / name
            try:
                size = p.lstat().st_size
            except FileNotFoundError:
                continue
            count += 1
            total += size
            symlinks += p.is_symlink()
    return {"files_observed": count, "bytes_from_local_stat": total, "symlinks_observed": symlinks,
            "scope": "Directory metadata only; no archive/dependency content hashed here."}


def provenance_index(update: Path, rows: list[dict]) -> list[dict]:
    """Index existing receipt fields without asserting that they are complete."""
    result = []
    wanted = ("url", "doi", "path", "file", "name", "sha", "md5", "checksum", "byte", "size", "version", "license", "revision", "commit")

    def visit(value, pointer, source):
        if isinstance(value, dict):
            fields = {}
            for key, item in value.items():
                if isinstance(item, (str, int, float, bool)) or item is None:
                    if any(word in key.lower() for word in wanted):
                        if isinstance(item, str) and len(item) > 1200:
                            continue
                        fields[key] = item
            has_url = any(isinstance(v, str) and (v.startswith("http") or v.startswith("doi:")) for v in fields.values())
            has_hash_path = any("sha" in k.lower() or "checksum" in k.lower() or "md5" in k.lower() for k in fields) and any("file" in k.lower() or "path" in k.lower() or "name" in k.lower() for k in fields)
            if has_url or has_hash_path:
                result.append({"included_receipt_path": source, "json_pointer": pointer or "/", "recorded_fields": fields})
            for key, item in value.items():
                visit(item, pointer + "/" + str(key).replace("~", "~0").replace("/", "~1"), source)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                visit(item, pointer + "/" + str(index), source)

    for row in rows:
        if not row["path"].endswith(".json"):
            continue
        try:
            data = json.loads((update / row["path"]).read_text())
        except (UnicodeError, json.JSONDecodeError):
            continue
        visit(data, "", row["path"])
    return result


def decide(rel: str, path: Path) -> tuple[bool, str]:
    lower = path.name.lower()
    parts = Path(rel).parts
    size = path.stat().st_size
    if rel in SOURCE_LICENSES:
        return True, SOURCE_LICENSES[rel]
    if size > 5_000_000:
        return False, "over_5MB_derived_or_source_payload; retained outside intake with receipts"
    if rel in NUMERICAL:
        return True, NUMERICAL[rel]
    if rel.startswith("s05_energy_certificates/inputs/"):
        if path.suffix.lower() in {".npy", ".npz"}:
            return True, "compact_cross_worker_numerical_input_snapshot"
        if path.name == "N2.STO3G.FCIDUMP":
            return True, "compact_public_source_numerical_input; upstream license retained"
        if path.suffix.lower() in TEXT:
            return True, "cross_worker_authored_evidence_snapshot"
    if rel.startswith("s06_molecular_kinetics/") and path.suffix.lower() == ".npz" and len(parts) == 2:
        return True, "compact_worker_reduced_MD_replay_input; source provenance retained"
    if "sources" in parts or "source" in parts:
        if path.suffix.lower() == ".json" and any(w in lower for w in ("receipt", "metadata", "pin", "inventory", "manifest")):
            return True, "source_acquisition_metadata_or_receipt"
        return False, "publisher_source_snapshot_or_raw_input"
    if path.suffix.lower() in RAW_EXT:
        return False, "raw_archive_measurement_or_downloaded_table"
    if path.suffix.lower() in {".html", ".xml", ".pdf", ".png", ".jpg", ".jpeg"}:
        if rel in {"a10_selection_challenge/NETWORK_DIAGNOSTIC.pdf", "a10_selection_challenge/NETWORK_DIAGNOSTIC.png"}:
            return True, "worker_authored_diagnostic_figure"
        return False, "publisher_article_SI_figure_or_web_snapshot"
    if lower.startswith("author_") and "receipt" not in lower:
        return False, "copied_publisher_source_code_or_source_document"
    if path.suffix.lower() == ".txt" and (
        lower.startswith("primary_") or lower.startswith("source_wz_")
        or lower.endswith("_source.txt") or lower.endswith("_plain.txt")
        or "si_text" in lower or lower == "si_text.txt"
        or lower in {"jacs_si_text.txt", "kfs_kiwisdr.js.txt", "kfs_kiwisdr.min.js.txt", "kiwisdr_directory.js.txt"}
        or lower.endswith("_readme.txt") or lower == "deusto_access_lab.txt"
    ):
        return False, "copied_publisher_code_article_SI_or_repository_document"
    if path.suffix.lower() in {".bin", ".npy", ".npz"}:
        return False, "unselected_binary_response_or_source_payload"
    if path.name in {".DS_Store", ".gitignore"} or lower.startswith("._"):
        return False, "operating_system_or_workspace_metadata"
    if path.suffix.lower() in TEXT:
        return True, "worker_authored_report_proof_script_compact_result_or_receipt"
    return False, "unclassified_non_authored_payload; no silent self_containment_claim"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers-root", type=Path, required=True)
    parser.add_argument("--update-root", type=Path, required=True)
    parser.add_argument("--version", type=int, required=True)
    parser.add_argument("--final", action="store_true")
    parser.add_argument("--root-artifacts", type=Path)
    args = parser.parse_args()
    workers = args.workers_root.resolve()
    update = args.update_root.resolve()
    version = f"v{args.version:04d}"
    evidence = update / "evidence" / "workers"
    if update.is_relative_to(workers) or workers.is_relative_to(update):
        raise RuntimeError("Input/output trees must be separate")
    names = sorted(p.name for p in workers.iterdir() if p.is_dir())
    if len(names) != 30:
        raise RuntimeError(f"Expected 30 worker directories, found {len(names)}")
    manifest_path = update / f"EVIDENCE_MANIFEST_{version}.json"
    if manifest_path.exists():
        raise RuntimeError(f"Refusing to overwrite versioned manifest {manifest_path}")
    included, excluded, pruned, history, dependency_rows = [], [], [], [], []
    per_worker = collections.defaultdict(lambda: {"files": 0, "bytes": 0})
    for worker in names:
        for here, dirs, filenames in os.walk(workers / worker, followlinks=False):
            for dirname in list(dirs):
                p = Path(here) / dirname
                rel = str(p.relative_to(workers))
                why = PRUNE.get(dirname)
                special_directory = rel in {
                    "s07_remote_control/data",
                    "computation_search/source/data",
                }
                if dirname == "data" and not special_directory:
                    why = "raw_acquisition_or_extraction_tree"
                if ("sources" in p.relative_to(workers).parts or "source" in p.relative_to(workers).parts) and p.parent.name in {"sources", "source"} and not special_directory:
                    why = "publisher_source_repository_or_extracted_data_tree"
                if p.is_symlink():
                    why = "symlink_not_followed"
                if why:
                    dirs.remove(dirname)
                    record = {"source_path": "workers/" + rel, "kind": "directory", "reason": why}
                    if not p.is_symlink():
                        record.update(directory_stat(p))
                    pruned.append(record)
            for filename in sorted(filenames):
                path = Path(here) / filename
                rel = str(path.relative_to(workers))
                if path.is_symlink():
                    excluded.append({"source_path": "workers/" + rel, "kind": "symlink", "reason": "symlink_not_followed"})
                    continue
                keep, category = decide(rel, path)
                if not keep:
                    st = path.stat()
                    row = {"source_path": "workers/" + rel, "kind": "file", "bytes": st.st_size, "reason": category}
                    if st.st_size <= 5_000_000:
                        row["sha256"] = sha(path.read_bytes())
                    else:
                        row["sha256"] = None
                        row["hash_status"] = "Not rehashed by curation; use included acquisition/source receipts where available."
                    excluded.append(row)
                    continue
                data, stat = stable_read(path)
                digest = sha(data)
                target = evidence / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists() and target.read_bytes() != data:
                    old = target.read_bytes()
                    archive = update / "evidence_history" / f"before-{version}" / "workers" / rel
                    archive.parent.mkdir(parents=True, exist_ok=True)
                    if archive.exists() and archive.read_bytes() != old:
                        raise RuntimeError(f"History path collision {archive}")
                    archive.write_bytes(old)
                    history.append({"path": str(archive.relative_to(update)), "bytes": len(old), "sha256": sha(old), "replaced_current_path": "evidence/workers/" + rel, "new_sha256": digest})
                temporary = target.with_name(target.name + ".curation-tmp")
                temporary.write_bytes(data)
                os.replace(temporary, target)
                included.append({"source_path": "workers/" + rel, "path": "evidence/workers/" + rel, "bytes": len(data), "sha256": digest, "source_mtime_ns": stat.st_mtime_ns, "category": category})
                per_worker[worker]["files"] += 1
                per_worker[worker]["bytes"] += len(data)
                if path.suffix.lower() == ".py":
                    imports, parse_error = set(), None
                    text = data.decode("utf-8", errors="replace")
                    try:
                        tree = ast.parse(text)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                imports.update(x.name.split(".")[0] for x in node.names)
                            elif isinstance(node, ast.ImportFrom) and node.module:
                                imports.add(node.module.split(".")[0])
                    except SyntaxError as exc:
                        parse_error = str(exc)
                    external = sorted(imports - set(sys.stdlib_module_names))
                    literals = []
                    for number, line in enumerate(text.splitlines(), 1):
                        if any(s in line for s in ("/Users/", "../", ".venv", "zipfile", "FCIDUMP", "sources/", "data/", "workers/")):
                            literals.append({"line": number, "text": line[:350]})
                    dependency_rows.append({"path": "evidence/workers/" + rel, "non_stdlib_import_names": external, "parse_error": parse_error, "literal_path_or_archive_hints": literals[:30], "hint_truncated": len(literals) > 30})
    for worker in names:
        if per_worker[worker]["files"] == 0:
            raise RuntimeError(f"No preserved authored evidence for worker {worker}")
    root_rows = []
    if args.final:
        if args.root_artifacts is None:
            raise RuntimeError("Final sync requires explicit root artifact directory")
        root_source = args.root_artifacts.resolve()
        for path in sorted(root_source.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue
            if any(part in PRUNE for part in path.relative_to(root_source).parts):
                continue
            data, stat = stable_read(path)
            rel = str(path.relative_to(root_source))
            if rel in ROOT_EXCLUDE:
                excluded.append({"source_path": "root/" + rel, "kind": "file", "bytes": len(data), "sha256": sha(data), "reason": ROOT_EXCLUDE[rel]})
                continue
            if len(data) > 5_000_000:
                raise RuntimeError(f"Root artifact exceeds compact evidence limit; root decision needed: {path}")
            target = update / "evidence" / "root" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and target.read_bytes() != data:
                old = target.read_bytes()
                archive = update / "evidence_history" / f"before-{version}" / "root" / rel
                archive.parent.mkdir(parents=True, exist_ok=True)
                archive.write_bytes(old)
                history.append({"path": str(archive.relative_to(update)), "bytes": len(old), "sha256": sha(old), "replaced_current_path": "evidence/root/" + rel, "new_sha256": sha(data)})
            temporary = target.with_name(target.name + ".curation-tmp")
            temporary.write_bytes(data)
            os.replace(temporary, target)
            root_rows.append({"source_path": "root/" + rel, "path": "evidence/root/" + rel, "bytes": len(data), "sha256": sha(data), "source_mtime_ns": stat.st_mtime_ns, "category": "root_authored_synthesis_proof_replay_result_or_figure"})
        included.extend(root_rows)
    retained_paths = {row["path"] for row in included}
    unexpected = [str(p.relative_to(update)) for p in (update / "evidence").rglob("*") if p.is_file() and str(p.relative_to(update)) not in retained_paths]
    if unexpected:
        raise RuntimeError(f"Stale/unmanaged files remain in current evidence tree: {unexpected[:10]}")
    receipts = collections.defaultdict(list)
    for row in included:
        name = Path(row["source_path"]).name.lower()
        if any(x in name for x in ("receipt", "acquisition", "source", "pin", "manifest", "inventory", "requirements", "metadata")) or row["source_path"] == "workers/a05_energy_matter/RESULTS.json":
            owner = "__root__" if row["source_path"].startswith("root/") else Path(row["source_path"]).parts[1]
            receipts[owner].append(row["path"])
    for row in excluded + pruned:
        worker = "__root__" if row["source_path"].startswith("root/") else Path(row["source_path"]).parts[1]
        row["included_reacquisition_receipt_pointers"] = receipts[worker]
        row["reacquisition_status"] = "Receipt pointers identify source versions/URLs/hashes where recorded; availability and credentials may still be unresolved. No end-to-end replay or complete rebuild was executed by curation."
    script_texts = {row["path"]: (update / row["path"]).read_text(errors="replace") for row in included if row["path"].endswith(".py")}
    for row in excluded:
        name = Path(row["source_path"]).name
        row["literal_rebuild_or_use_script_candidates"] = [path for path, content in script_texts.items() if name in content]
    manifest = {"schema": "astra-curated-worker-evidence/1", "version": args.version, "created_utc": stamp(), "status": "ROOT_FINAL_SYNC" if args.final else "PRELIMINARY_WAITING_ROOT_FINAL_SIGNAL", "root_final_signal_received": args.final, "workers_root": str(workers), "root_artifacts_source": str(args.root_artifacts.resolve()) if args.root_artifacts else None, "workers": names, "worker_count": len(names), "included_count": len(included), "included_bytes": sum(x["bytes"] for x in included), "root_files": len(root_rows), "per_worker": dict(sorted(per_worker.items())), "files": included, "prior_snapshot_bytes_retained": history, "scope": "Byte-preserving evidence intake only. No worker/root source modified or scientific script executed by curation; no scientific validation, claim promotion or universal self-contained replay is asserted."}
    read_ledger = []
    for worker, documents in REPORTS.items():
        for document in documents:
            p = workers / worker / document
            if p.exists():
                data, _ = stable_read(p)
                read_ledger.append({"source_path": f"workers/{worker}/{document}", "sha256": sha(data), "bytes": len(data), "scope": "Read current scope/outcome, provenance/replay and correction sections for curation; not an independent proof or scientific review."})
    ledger = {"schema": "astra-evidence-exclusion-acquisition-ledger/1", "version": args.version, "created_utc": stamp(), "status": manifest["status"], "source_roots_unchanged": True, "policy": {"preserve": "Worker-authored reports/proofs/scripts/compact results/receipts/corrections, relevant histories, explicitly sourced compact numeric replay inputs and license notices.", "exclude": "Installed environments/dependencies, source repositories, copied publisher code, complete papers/SI/figures/web copies, raw archives/extraction trees and >5MB derived rows.", "bytes_limit": 5_000_000, "root_synthesis": "Separate final evidence/root packet copied only on root's final signal.", "source_licenses": "Retained source notices do not by themselves settle license scope of every numeric extract; source metadata/receipts remain authoritative and any unresolved scope is explicit."}, "excluded_files": excluded, "excluded_directories": pruned, "script_dependency_hints": dependency_rows, "replay_limit": "Some scripts need excluded raw data, other workers, platform-specific runtimes, scientific packages or absolute workspace paths. Static import/literal hints are incomplete. This intake does not falsely claim all scripts are standalone or that every download remains accessible.", "required_final_checks": ["Root final signal and resync after all worker amendments", "Verify all included source/current-copy hashes", "Preserve s05/computation vector provenance correction and fresh-vector receipts", "Preserve a08 uniform-Schmidt extension plus s10 sharp audit", "Root review of license/acquisition gaps before publication"]}
    for output, data in [(manifest_path, manifest), (update / f"EXCLUSION_ACQUISITION_LEDGER_{version}.json", ledger), (update / f"CURATION_READ_LEDGER_{version}.json", {"schema": "astra-curation-read-ledger/1", "version": args.version, "created_utc": stamp(), "documents": read_ledger})]:
        output.write_text(json.dumps(data, indent=2) + "\n")
    reference_index = {"schema": "astra-existing-acquisition-reference-index/1", "version": args.version, "created_utc": stamp(), "records": provenance_index(update, included), "scope": "Literal URLs/DOIs/source hashes and file/version/license fields indexed from copied JSON receipts with exact JSON pointers. This index preserves recorded provenance, not correctness, availability, license adjudication or completeness of reacquisition."}
    (update / f"ACQUISITION_REFERENCE_INDEX_{version}.json").write_text(json.dumps(reference_index, indent=2) + "\n")
    status = (f"{manifest['status']}\n{len(names)} workers; {len(included)} included files; {manifest['included_bytes']} bytes.\n"
              "Current worker paths are preserved under evidence/workers/. Original worker files were not edited.\n"
              "Excluded source data/code/dependencies remain outside the intake with acquisition and dependency pointers.\n"
              "Some worker scripts require excluded inputs or environment setup; no universal standalone replay is claimed.\n"
              "Root scientific synthesis, final validation, staging, commit, push and PR remain root-owned.\n")
    (update / f"EVIDENCE_BUNDLE_STATUS_{version}.txt").write_text(status)
    print(json.dumps({"version": version, "status": manifest["status"], "workers": len(names), "included_files": len(included), "included_bytes": manifest["included_bytes"], "excluded_files": len(excluded), "excluded_directories": len(pruned), "manifest": str(manifest_path)}, indent=2))


if __name__ == "__main__":
    main()
