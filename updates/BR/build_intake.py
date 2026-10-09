#!/usr/bin/env python3
"""Reproduce the BR public intake; verify originals, never execute research code.

Uses existing public ledgers/graph/catalog. No private SQLite rebuild is claimed.
Prepare every output in memory before writing; publication is a reviewed Git commit.
The same input is idempotent. Check mode performs no writes.
"""
import argparse
import hashlib
import html
import json
import stat
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
PREFIX = "updates/BR/package/research_packet/"
SCOPED_READ = {"RESEARCH_REPORT.txt", "CLAIM_LEDGER.json", "CROSS_BRANCH_HANDOFF.txt",
               "SOURCE_MANIFEST.json", "PORTABLE_REPLAY.json", "START_HERE.txt",
               "work/calibration_audit/audit.txt", "work/gaussian_displaced_audit/report.txt",
               "work/gaussian_transfer/displaced_followup.txt", "work/gaussian_transfer/displaced_parity_audit.txt",
               "work/gaussian_transfer/displaced_gate.txt", "work/gaussian_software_audit/report.txt"}
STATUS = "source_derived_unreviewed"
BOUNDARY = ("Source-reported internal model-assisted proof/review and finite software checks; "
            "not replayed or independently reconstructed during intake. No historic-scale "
            "breakthrough, external expert/formal verification, physical acquisition or historical "
            "novelty is established. Theoretical bit-cost bounds do not certify uniform runtime "
            "of the particular numerical implementation.")
BV_BOUNDARY = ("Source-reported analytic derivations and synthetic numerical diagnostics; no "
               "external proof review, formal verification, publication-priority clearance or "
               "physical system identification is established. No historic-scale or 9–10/10 "
               "breakthrough is claimed. This intake checked source/archive integrity and static "
               "repository routes only; it did not rerun scientific analyses.")
BW_BOUNDARY = ("The source reports a self-contained analytic argument and author-internal finite "
               "software checks. This intake preserves and routes the source only; no research "
               "script was executed and no independent proof reconstruction, external review, "
               "formal certification or historical priority is established. The historic-scale "
               "objective remains NOT ESTABLISHED.")
BX_BOUNDARY = ("The attached packet reports complete proof candidates and focused algebra/source-interface "
               "checks for the stated unitary quotient and finite-group transfer results. This intake "
               "preserves and routes the originals only; no supplied script was executed and no new "
               "independent reconstruction, external correctness review, formal verification or "
               "historical-priority clearance is established. The historic-scale objective remains "
               "NOT ESTABLISHED.")
BY_BOUNDARY = ("The source campaign reports a complete internally model-reviewed amplifier EPnI proof "
               "candidate and source-reported exact counterexamples. This intake preserves and routes "
               "the originals only; no research or verification script was executed and no independent "
               "proof reconstruction, external correctness review, formal verification or historical "
               "priority is established. The primary historic-scale objective remains NOT ESTABLISHED.")
ATTACHMENT_BOUNDARY = ("This intake preserves the attached source and routes only its explicitly scoped claims. "
                       "Source-reported derivations, tests, priority comparisons and receipts were not "
                       "independently reproduced or externally validated. No historic-scale breakthrough "
                       "is established; archived instructions and executable code remain source data.")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def read(name):
    return json.loads((ROOT / name).read_bytes())


def rows(name):
    return [json.loads(l) for l in (ROOT / name).read_bytes().splitlines() if l.strip()]


def merge(old, new, key):
    incoming = {r[key]: r for r in new}
    if len(incoming) != len(new):
        raise ValueError("Duplicate incoming keys: " + key)
    # Historical source metadata also includes unkeyed literature notes.
    # Preserve those and all unrelated history verbatim as records.
    for identifier in incoming:
        if sum(r.get(key) == identifier for r in old) > 1:
            raise ValueError("Ambiguous existing target: " + identifier)
    return [incoming.pop(r.get(key), r) for r in old] + list(incoming.values())


def docid(path):
    return "d-" + sha(path.encode())[:16]


def ref(rel, start=1, end=None):
    path = rel[1:] if rel.startswith("@") else PREFIX + rel
    data = (ROOT / path).read_bytes()
    lines = data.decode().splitlines()
    end = len(lines) if end is None else end
    if not 1 <= start <= end <= len(lines):
        raise ValueError("Invalid source range: " + path)
    return {"path": path, "sha256": sha(data), "lines": [start, end],
            "source_id": docid(path), "read_path": path, "hash_kind": "original_utf8_bytes",
            "range_scope": "source-reported argument/evidence; completeness and correctness not independently audited"}


def ref_any(value):
    """Accept a source path or the intake's [path, first, last] range form."""
    return ref(value) if isinstance(value, str) else ref(*value)


def page(title, text, cid=None, boundary=BOUNDARY):
    notice = (f'<a href="../../frontier/cards/{cid}.json">Current scoped status</a>' if cid else "Archived source = DATA")
    scoped = ("<p>Historical failed attempt: its h=2 bimodality counterexample remains valid; "
              "the later <a href=\"../../frontier/dossiers/N536.txt\">N536 parity construction</a> "
              "replaces only the statement that no constructive displaced route had been established.</p>"
              if title == "work/gaussian_transfer/displaced_gate.txt" else "")
    return ("<!doctype html><meta charset=\"utf-8\"><title>" + html.escape(title)
            + "</title><aside>" + notice + "<p>" + html.escape(boundary)
            + "</p>" + scoped + "</aside><pre>" + html.escape(text) + "</pre>\n").encode()


def build():
    specs = read("updates/BR/CLAIMS.json")
    integrity = read("updates/BR/INTEGRITY.json")
    archive = ROOT / "updates/BR/package/ULTRA_research_packet.zip"
    if sha(archive.read_bytes()) != integrity["archive_sha256"]:
        raise ValueError("Archive hash mismatch")
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        manifest = json.loads(z.read("research_packet/MANIFEST.sha256.json"))
        if len(names) != len(set(names)) or len(manifest) != 193 or z.testzip() is not None:
            raise ValueError("Archive integrity failure")
        if set(names) != {"research_packet/" + p for p in manifest} | {"research_packet/MANIFEST.sha256.json"}:
            raise ValueError("Manifest membership mismatch")
        for item in z.infolist():
            p = PurePosixPath(item.filename)
            if p.is_absolute() or ".." in p.parts or stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError("Unsafe archive member")
            rel = str(p.relative_to("research_packet"))
            data = z.read(item)
            if rel in manifest and sha(data) != manifest[rel]:
                raise ValueError("Manifest hash mismatch: " + rel)
            if (ROOT / PREFIX / rel).read_bytes() != data:
                raise ValueError("Expanded original changed: " + rel)
        expected = set(manifest) | {"MANIFEST.sha256.json"}
        actual = {p.relative_to(ROOT / PREFIX).as_posix() for p in (ROOT / PREFIX).rglob("*") if p.is_file()}
        if actual != expected:
            raise ValueError("Expanded membership mismatch")
    # A second, independent Ultra round and the separate natural-sciences record
    # are additional source roots, not entries in the earlier BR packet.
    supplement = read("updates/BS/INTEGRITY.json")
    archive2_rel = supplement["evidence_archive"]
    archive2 = ROOT / archive2_rel
    if sha(archive2.read_bytes()) != supplement["archive_sha256"]:
        raise ValueError("BS archive hash mismatch")
    tree2 = "updates/BS/package/evidence"
    source_items = [{"path": PREFIX + rel, "rel": rel, "title": rel,
                     "data": (ROOT / PREFIX / rel).read_bytes(), "depth": "scoped review; see source map"}
                    for rel in sorted(expected)]
    with zipfile.ZipFile(archive2) as z:
        manifest = json.loads(z.read("MANIFEST.json"))
        files = manifest["files"]
        if len(z.namelist()) != len(set(z.namelist())) or len(files) != 96 or z.testzip() is not None:
            raise ValueError("BS archive integrity failure")
        if set(z.namelist()) != set(files) | {"MANIFEST.json"}:
            raise ValueError("BS archive/manifest membership mismatch")
        for info in z.infolist():
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Unsafe BS archive member")
            data = z.read(info)
            target = (ROOT / tree2 / info.filename) if info.filename != "MANIFEST.json" else ROOT / tree2 / "MANIFEST.json"
            if target.read_bytes() != data:
                raise ValueError("BS expanded source differs from archive: " + info.filename)
            expected_hash = files.get(info.filename)
            if expected_hash and (len(data) != expected_hash["bytes"] or sha(data) != expected_hash["sha256"]):
                raise ValueError("BS source hash mismatch: " + info.filename)
            source_items.append({"path": tree2 + "/" + info.filename, "rel": info.filename,
                                 "title": info.filename, "data": data,
                                 "depth": "scoped source inspection; not full independent verification" if info.filename in {
                                     "RESEARCH_REPORT.txt", "SPECTRAL_PROOF.txt", "RARE_EVENT_PROOF.txt",
                                     "GAUSSIAN_CONDITIONING_PROOF.txt", "EQUILIBRIUM_PROOF.txt",
                                     "CLAIM_LEDGER.json", "BRANCH_HANDOFFS.json", "PORTABLE_REPLAY.json"}
                                 else "hash and archive membership only; not reviewed"})
    bt_path = "updates/BT/package/research_record.md"
    bt_data = (ROOT / bt_path).read_bytes()
    bt_origin = supplement["natural_science_record"]
    if sha(bt_data) != bt_origin["sha256"] or len(bt_data) != bt_origin["bytes"]:
        raise ValueError("BT attached record hash mismatch")
    source_items.append({"path": bt_path, "rel": "research_record.md", "title": "Delayed division responses: a falsification-first continuation",
                         "data": bt_data, "depth": "complete attached record read; cited code/data bundle not supplied"})
    # BU is the first Primitive Genesis handoff. Preserve the exact folder and
    # its sibling ZIP; verify both against the internal SHA-256 manifest.
    genesis = read("updates/BU/INTEGRITY.json")
    archive3_rel = genesis["archive_path"]
    archive3 = ROOT / archive3_rel
    if sha(archive3.read_bytes()) != genesis["archive_sha256"] or len(archive3.read_bytes()) != genesis["archive_bytes"]:
        raise ValueError("BU archive hash/size mismatch")
    tree3 = "updates/BU/package/primitive_genesis_retention"
    manifest_path = ROOT / tree3 / "MANIFEST.sha256"
    manifest3 = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, rel = line.split(None, 1)
            manifest3[rel.strip().lstrip("*")] = digest
    if len(manifest3) != 14 or sha(manifest_path.read_bytes()) != genesis["manifest_sha256"]:
        raise ValueError("BU source manifest mismatch")
    with zipfile.ZipFile(archive3) as z:
        names = z.namelist()
        expected_names = {"primitive_genesis_retention/" + p for p in manifest3} | {
            "primitive_genesis_retention/MANIFEST.sha256"}
        if len(names) != 15 or len(names) != len(set(names)) or set(names) != expected_names or z.testzip() is not None:
            raise ValueError("BU archive membership/CRC failure")
        for info in z.infolist():
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Unsafe BU archive member")
            rel = str(member.relative_to("primitive_genesis_retention"))
            data = z.read(info)
            target = ROOT / tree3 / rel
            if not target.is_file() or target.read_bytes() != data:
                raise ValueError("BU expanded source differs from archive: " + rel)
            if rel in manifest3 and sha(data) != manifest3[rel]:
                raise ValueError("BU source hash mismatch: " + rel)
            if rel == "MANIFEST.sha256":
                source_items.append({"path": tree3 + "/" + rel, "rel": rel, "title": rel,
                                     "data": data, "depth": "internal source checksum manifest; hashes independently checked"})
                continue
            reviewed = rel in {"README.md", "RESEARCH_NOTE.md", "QUANTUM_ORBIT_EXTENSION.md",
                               "HANDOFF.md", "CLAIMS.json", "SOURCE_PROVENANCE.json",
                               "CHECKER_CORRECTION.json"}
            source_items.append({"path": tree3 + "/" + rel, "rel": rel, "title": rel,
                                 "data": data,
                                 "depth": "scoped source reading; not independently proof-verified" if reviewed
                                 else "preserved receipt or code; no scientific verifier executed"})
    summary_path = "updates/BU/PRESENTED_SUMMARY.txt"
    summary_data = (ROOT / summary_path).read_bytes()
    if sha(summary_data) != genesis["presented_summary_sha256"] or len(summary_data) != genesis["presented_summary_bytes"]:
        raise ValueError("BU pasted-summary hash/size mismatch")
    source_items.append({"path": summary_path, "rel": "PRESENTED_SUMMARY.txt", "title": "User-pasted Primitive Genesis summary",
                         "data": summary_data, "depth": "abridged conversational summary; full source note is authoritative"})

    # BV is a separate stationary-generator investigation. Preserve its exact
    # source folder and verify the sibling ZIP, manifest and expanded bytes;
    # never execute embedded research scripts during repository intake.
    tomography = read("updates/BV/INTEGRITY.json")
    archive4_rel = tomography["archive_path"]
    archive4 = ROOT / archive4_rel
    if sha(archive4.read_bytes()) != tomography["archive_sha256"] or len(archive4.read_bytes()) != tomography["archive_bytes"]:
        raise ValueError("BV archive hash/size mismatch")
    tree4 = "updates/BV/package/astra_static_generator_tomography"
    manifest4_path = ROOT / tree4 / "MANIFEST.json"
    manifest4_bytes = manifest4_path.read_bytes()
    if sha(manifest4_bytes) != tomography["manifest_sha256"]:
        raise ValueError("BV source manifest hash mismatch")
    manifest4 = json.loads(manifest4_bytes)
    files4 = manifest4["files"]
    expected4 = {"astra_static_generator_tomography/" + item["path"] for item in files4} | {
        "astra_static_generator_tomography/MANIFEST.json"}
    if len(files4) != 17:
        raise ValueError("BV manifest file count mismatch")
    with zipfile.ZipFile(archive4) as z:
        names = z.namelist()
        if len(names) != 18 or len(names) != len(set(names)) or set(names) != expected4 or z.testzip() is not None:
            raise ValueError("BV archive membership/CRC failure")
        hashes4 = {item["path"]: item for item in files4}
        for info in z.infolist():
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Unsafe BV archive member")
            rel = str(member.relative_to("astra_static_generator_tomography"))
            data = z.read(info)
            target = ROOT / tree4 / rel
            if not target.is_file() or target.read_bytes() != data:
                raise ValueError("BV expanded source differs from archive: " + rel)
            item = hashes4.get(rel)
            if item and (len(data) != item["bytes"] or sha(data) != item["sha256"]):
                raise ValueError("BV source hash mismatch: " + rel)
            if rel == "MANIFEST.json":
                source_items.append({"path": tree4 + "/" + rel, "rel": rel, "title": rel,
                                     "data": data, "depth": "embedded source integrity manifest; hashes independently checked",
                                     "boundary": BV_BOUNDARY})
                continue
            reviewed = rel in {"README.md", "RESEARCH_HANDOFF.md", "ASTRA_BRIDGE.txt",
                               "ASTRA_SESSION_RECORD.json", "proof_checks_results.json",
                               "results.json", "torus_results.json", "entropy_production_results.json",
                               "stein_results.json", "matched_comparator_results.json"}
            source_items.append({"path": tree4 + "/" + rel, "rel": rel, "title": rel,
                                 "data": data,
                                 "depth": "scoped source/result inspection; not independently proof-verified" if reviewed
                                 else "preserved source code or environment record; no research code executed",
                                 "boundary": BV_BOUNDARY})
    # BW is a separate mixed-family broadcasting proof packet. The user supplied
    # the expanded folder (not a ZIP); its deterministic archive is only a portable
    # byte-preserving convenience. Never execute its embedded research scripts.
    reservoir = read("updates/BW/INTEGRITY.json")
    archive5_rel = reservoir["archive_path"]
    archive5 = ROOT / archive5_rel
    if sha(archive5.read_bytes()) != reservoir["archive_sha256"] or len(archive5.read_bytes()) != reservoir["archive_bytes"]:
        raise ValueError("BW archive hash/size mismatch")
    tree5 = "updates/BW/package/astra_mixed_broadcasting_2026-10-10"
    manifest5_path = ROOT / tree5 / "MANIFEST.sha256"
    manifest5 = {}
    for line in manifest5_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, rel = line.split(None, 1)
            manifest5[rel.strip().lstrip("*")] = digest
    if len(manifest5) != 23 or sha(manifest5_path.read_bytes()) != reservoir["manifest_sha256"]:
        raise ValueError("BW source manifest mismatch")
    with zipfile.ZipFile(archive5) as z:
        names = z.namelist()
        expected_names = {"astra_mixed_broadcasting_2026-10-10/" + p for p in manifest5} | {
            "astra_mixed_broadcasting_2026-10-10/MANIFEST.sha256"}
        if len(names) != 24 or len(names) != len(set(names)) or set(names) != expected_names or z.testzip() is not None:
            raise ValueError("BW archive membership/CRC failure")
        for info in z.infolist():
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Unsafe BW archive member")
            rel = str(member.relative_to("astra_mixed_broadcasting_2026-10-10"))
            data = z.read(info)
            target = ROOT / tree5 / rel
            if not target.is_file() or target.read_bytes() != data:
                raise ValueError("BW expanded source differs from archive: " + rel)
            expected_hash = manifest5.get(rel)
            if expected_hash and sha(data) != expected_hash:
                raise ValueError("BW source hash mismatch: " + rel)
            if rel == "MANIFEST.sha256":
                source_items.append({"path": tree5 + "/" + rel, "rel": rel, "title": rel,
                                     "data": data, "depth": "supplied source manifest; every listed payload hash checked",
                                     "boundary": BW_BOUNDARY})
                continue
            reviewed = rel in {"RESEARCH_PROOF.md", "HANDOFF.md", "CLAIMS.json", "SESSION.json",
                               "SOURCE_REVISIONS.json", "bridges/entropy_loss_gate.json",
                               "bridges/mixed_family_scope.json", "bridges/physical_resource.json",
                               "AUDIT_LOG.md", "exploration/README.md"}
            if rel in {"verification_receipt.json", "finite_design_receipt.json",
                       "construction_run_stdout.txt", "design_run_stdout.txt",
                       "history/verification_receipt_v1_96checks.json", "history/finite_design_receipt_v1_52checks.json"}:
                depth = "source-reported internal receipt preserved; not replayed or independently validated"
            elif reviewed:
                depth = "scoped source inspection; not independent proof verification"
            else:
                depth = "preserved code/environment source; no research code executed"
            source_items.append({"path": tree5 + "/" + rel, "rel": rel, "title": rel,
                                 "data": data, "depth": depth, "boundary": BW_BOUNDARY})

    # BX is the separate unitary quotient / finite permutation-transfer packet.
    quotient = read("updates/BX/INTEGRITY.json")
    archive6 = ROOT / quotient["archive_path"]
    if sha(archive6.read_bytes()) != quotient["archive_sha256"] or len(archive6.read_bytes()) != quotient["archive_bytes"]:
        raise ValueError("BX archive hash/size mismatch")
    tree6 = "updates/BX/package/unitary_quotient_research_bundle"
    manifest6_path = ROOT / tree6 / "MANIFEST.json"
    manifest6_bytes = manifest6_path.read_bytes()
    if sha(manifest6_bytes) != quotient["manifest_sha256"]:
        raise ValueError("BX source manifest hash mismatch")
    manifest6 = json.loads(manifest6_bytes)
    files6 = manifest6["files"]
    expected6 = {"unitary_quotient_research_bundle/" + item["file"] for item in files6} | {
        "unitary_quotient_research_bundle/MANIFEST.json", "unitary_quotient_research_bundle/"}
    if len(files6) != 10:
        raise ValueError("BX manifest file count mismatch")
    with zipfile.ZipFile(archive6) as z:
        names = z.namelist()
        if len(names) != 12 or len(names) != len(set(names)) or set(names) != expected6 or z.testzip() is not None:
            raise ValueError("BX archive membership/CRC failure")
        hashes6 = {item["file"]: item for item in files6}
        for info in z.infolist():
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Unsafe BX archive member")
            if info.is_dir():
                continue
            rel = str(member.relative_to("unitary_quotient_research_bundle"))
            data = z.read(info)
            target = ROOT / tree6 / rel
            if not target.is_file() or target.read_bytes() != data:
                raise ValueError("BX expanded source differs from archive: " + rel)
            item = hashes6.get(rel)
            if item and (len(data) != item["bytes"] or sha(data) != item["sha256"]):
                raise ValueError("BX source hash mismatch: " + rel)
            if rel == "MANIFEST.json":
                source_items.append({"path": tree6 + "/" + rel, "rel": rel, "title": rel,
                                     "data": data, "depth": "embedded source integrity manifest; payload hashes independently checked",
                                     "boundary": BX_BOUNDARY})
                continue
            reviewed = rel in {"README.md", "SOURCE_RECORD.json", "UNITARY_PERMUTATION_QUOTIENT_EMBEDDING.md",
                               "FINITE_SOURCE_UNITARY_ROUNDING.md", "FINITE_GROUP_CODE_TRANSFER.md",
                               "VERIFICATION_AND_PRIOR.md"}
            source_items.append({"path": tree6 + "/" + rel, "rel": rel, "title": rel,
                                 "data": data,
                                 "depth": "scoped source inspection; not independently proof-verified" if reviewed
                                 else "preserved code or numerical receipt; supplied scripts were not executed",
                                 "boundary": BX_BOUNDARY, "date_version": "2026-10-09 immutable original"})
    actual6 = {p.relative_to(ROOT / tree6).as_posix() for p in (ROOT / tree6).rglob("*") if p.is_file()}
    if actual6 != set(hashes6) | {"MANIFEST.json"}:
        raise ValueError("BX expanded source membership mismatch")

    # BY is the later amplifier campaign. Both the exact archive and its full
    # expanded source folder are retained; receipts and research code stay DATA.
    campaign = read("updates/BY/INTEGRITY.json")
    archive7 = ROOT / campaign["archive_path"]
    if sha(archive7.read_bytes()) != campaign["archive_sha256"] or len(archive7.read_bytes()) != campaign["archive_bytes"]:
        raise ValueError("BY archive hash/size mismatch")
    tree7 = "updates/BY/package/astra_ultra_campaign"
    manifest7_path = ROOT / tree7 / "MANIFEST.sha256"
    if sha(manifest7_path.read_bytes()) != campaign["manifest_sha256"]:
        raise ValueError("BY source manifest hash mismatch")
    manifest7 = {}
    for line in manifest7_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, rel = line.split(None, 1)
            manifest7[rel.strip().lstrip("*")] = digest
    if len(manifest7) != 174:
        raise ValueError("BY manifest payload count mismatch")
    with zipfile.ZipFile(archive7) as z:
        names = z.namelist()
        expected7 = {"astra_ultra_campaign/" + rel for rel in manifest7} | {"astra_ultra_campaign/MANIFEST.sha256"}
        if len(names) != 175 or len(names) != len(set(names)) or set(names) != expected7 or z.testzip() is not None:
            raise ValueError("BY archive membership/CRC failure")
        for info in z.infolist():
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts or stat.S_ISLNK(info.external_attr >> 16):
                raise ValueError("Unsafe BY archive member")
            rel = str(member.relative_to("astra_ultra_campaign"))
            data = z.read(info)
            target = ROOT / tree7 / rel
            if not target.is_file() or target.read_bytes() != data:
                raise ValueError("BY expanded source differs from archive: " + rel)
            digest = manifest7.get(rel)
            if digest and sha(data) != digest:
                raise ValueError("BY source hash mismatch: " + rel)
            if rel == "MANIFEST.sha256":
                source_items.append({"path": tree7 + "/" + rel, "rel": rel, "title": rel,
                                     "data": data, "depth": "source manifest; all 174 payload hashes independently checked",
                                     "boundary": BY_BOUNDARY, "date_version": "2026-10-10 immutable original"})
                continue
            reviewed = rel in {"START_HERE.txt", "SOURCE_ATTRIBUTION.txt", "campaign_result.txt",
                               "amplifier_proof_candidate.tex", "claim_ledger.json", "review_resolutions.json",
                               "source_manifest.json", "handoffs/theoretical_pro.json",
                               "work/reports/final_review_sol2.txt", "work/reports/final_review_sol3.txt",
                               "work/reports/final_review_sol4.txt", "work/reports/final_report_consistency.txt",
                               "work/reports/sol1_signed/exact_falsifiers.py",
                               "work/reports/adaptive18_signed_checks.py",
                               "work/reports/sol2_alternative.txt"}
            if rel in {"reproduction_receipt.json", "portable_replay_receipt.json", "compilation_receipt.json"}:
                depth = "source-reported receipt preserved; not replayed during intake"
            elif reviewed:
                depth = "scoped source inspection; not independent proof verification"
            else:
                depth = "preserved source/code/environment record; supplied code was not executed"
            source_items.append({"path": tree7 + "/" + rel, "rel": rel, "title": rel,
                                 "data": data, "depth": depth, "boundary": BY_BOUNDARY,
                                 "date_version": "2026-10-10 immutable original"})
    actual7 = {p.relative_to(ROOT / tree7).as_posix() for p in (ROOT / tree7).rglob("*") if p.is_file()}
    if actual7 != set(manifest7) | {"MANIFEST.sha256"}:
        raise ValueError("BY expanded source membership mismatch")
    external_validation = ROOT / "updates/BY/package/PACKAGE_VALIDATION_EXTERNAL.json"
    external_data = external_validation.read_bytes()
    external_obj = json.loads(external_data)
    if (sha(external_data) != campaign["external_package_validation_sha256"] or
            external_obj.get("archive_sha256") != campaign["archive_sha256"] or
            external_obj.get("archive_bytes") != campaign["archive_bytes"] or
            external_obj.get("manifest_file_count") != 174 or external_obj.get("archive_file_count") != 175):
        raise ValueError("BY external package-validation record mismatch")
    source_items.append({"path": "updates/BY/package/PACKAGE_VALIDATION_EXTERNAL.json",
                         "rel": "PACKAGE_VALIDATION_EXTERNAL.json", "title": "External package validation record",
                         "data": external_data, "depth": "source-supplied package validation receipt; not rerun",
                         "boundary": BY_BOUNDARY, "date_version": "2026-10-10 immutable original"})

    # Later user attachments are registered as small immutable source roots.
    # Hashes and exact directory membership come from each intake's INTEGRITY.json;
    # code, receipts, and embedded instructions are indexed as data and never run.
    additional_source_roots = []
    additional_source_file_counts = {}
    for bundle in specs.get("source_bundles", []):
        intake_id = bundle["intake_id"]
        root_rel = bundle["source_root"]
        root_path = PurePosixPath(root_rel)
        if root_path.is_absolute() or ".." in root_path.parts or not root_rel.startswith("updates/"):
            raise ValueError("Unsafe additional source root: " + root_rel)
        source_root = ROOT.joinpath(*root_path.parts).resolve()
        if not source_root.is_relative_to(ROOT.resolve()) or not source_root.is_dir():
            raise ValueError("Missing or unsafe additional source root: " + root_rel)
        integrity = read(f"updates/{intake_id}/INTEGRITY.json")
        if integrity.get("intake_id") != intake_id or integrity.get("source_root") != root_rel:
            raise ValueError("Additional source root/integrity mismatch: " + intake_id)
        file_map = integrity.get("source_files")
        if not isinstance(file_map, dict) or not file_map:
            raise ValueError("Missing additional source file map: " + intake_id)
        actual = set()
        for candidate in source_root.rglob("*"):
            if candidate.is_symlink():
                raise ValueError("Symlink in additional source root: " + str(candidate))
            if candidate.is_file():
                actual.add(candidate.relative_to(source_root).as_posix())
        if actual != set(file_map):
            raise ValueError("Additional source membership mismatch: " + intake_id)
        manifest_rel = integrity.get("manifest_path")
        if manifest_rel:
            manifest = source_root / manifest_rel
            manifest_files = {}
            for line in manifest.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    digest, rel = line.split(None, 1)
                    manifest_files[rel.strip().lstrip("*")] = digest
            expected_payload = set(file_map) - {manifest_rel}
            if set(manifest_files) != expected_payload:
                raise ValueError("Additional source manifest membership mismatch: " + intake_id)
            for rel, digest in manifest_files.items():
                if file_map[rel].get("sha256") != digest:
                    raise ValueError("Additional source manifest hash mismatch: " + rel)
        scoped = set(bundle.get("scoped_paths", []))
        for rel, item in sorted(file_map.items()):
            member = PurePosixPath(rel)
            if member.is_absolute() or ".." in member.parts:
                raise ValueError("Unsafe additional source member: " + rel)
            path = source_root.joinpath(*member.parts).resolve()
            if not path.is_relative_to(source_root) or not path.is_file():
                raise ValueError("Missing or unsafe additional source member: " + rel)
            data = path.read_bytes()
            if len(data) != item.get("bytes") or sha(data) != item.get("sha256"):
                raise ValueError("Additional source hash/size mismatch: " + intake_id + "/" + rel)
            if rel == manifest_rel:
                depth = "attached source manifest; payload hashes and membership checked, not scientific evidence"
            elif rel in scoped:
                depth = "scoped source inspection; not independently proof-verified"
            elif rel.lower().endswith(".py"):
                depth = "preserved research code; supplied code was not executed"
            elif "receipt" in rel.lower() or rel.lower().endswith("results.json"):
                depth = "source-reported diagnostic/verification receipt; preserved and not rerun"
            else:
                depth = "preserved original source data; not independently reviewed"
            source_items.append({"path": root_rel + "/" + rel, "rel": rel, "title": rel,
                                 "data": data, "depth": depth, "boundary": bundle.get("boundary", ATTACHMENT_BOUNDARY),
                                 "date_version": bundle.get("date_version", "2026-10-10 immutable attachment")})
        additional_source_roots.append(source_root)
        additional_source_file_counts[intake_id] = len(file_map)

    secondary_expected = {i["path"] for i in source_items if not i["path"].startswith(PREFIX)}
    secondary_roots = [ROOT / tree2, ROOT / "updates/BT/package", ROOT / tree3, ROOT / tree4, ROOT / tree5, ROOT / tree6, ROOT / tree7]
    secondary_roots.extend(additional_source_roots)
    secondary_actual = {p.relative_to(ROOT).as_posix() for root in secondary_roots
                        for p in root.rglob("*") if p.is_file()}
    secondary_actual.add(summary_path)
    secondary_actual.add("updates/BY/package/PACKAGE_VALIDATION_EXTERNAL.json")
    if secondary_actual != secondary_expected:
        raise ValueError("Supplemental source tree membership mismatch")
    outputs = {}

    def put(path, data):
        outputs[path] = data

    def put_json(path, obj):
        put(path, encoded(obj))

    def put_rows(path, data):
        put(path, b"".join((json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n").encode() for r in data))

    new_claims, new_statuses, new_catalog, new_docs, new_sources, new_gates = [], [], [], [], [], []
    aliases = read("indexes/query_aliases.json")
    graph = read("indexes/agent_graph.json")
    catalog = read("indexes/agent_catalog.json")
    nodes = {r["id"]: r for r in graph["nodes"]}
    extra_edges = []
    source_path = lambda item: item if isinstance(item, str) else item[0]
    resolve_source = lambda item: (source_path(item)[1:] if source_path(item).startswith("@")
                                   else PREFIX + source_path(item))
    selected = {resolve_source(r) for s in specs["claims"] for r in s["proofs"]}
    selected |= {resolve_source(r) for s in specs["claims"] for r in s["evidence"]}
    selected |= {resolve_source(r) for s in specs["claims"] for r in s.get("status_evidence", [])}
    source_topics = {}
    for claim_spec in specs["claims"]:
        refs = claim_spec["proofs"] + claim_spec["evidence"] + claim_spec.get("status_evidence", [])
        for source_ref in refs:
            source_topics.setdefault(resolve_source(source_ref), set()).update(claim_spec["topics"])
    for source in sorted(source_items, key=lambda s: s["path"]):
        path, rel, data = source["path"], source["rel"], source["data"]
        sid = docid(path)
        try:
            text = data.decode("utf-8")
            extraction = "exact_utf8"
        except UnicodeError:
            text = None
            extraction = "binary_preserved"
        title = source["title"]
        new_sources.append({"source_id": sid, "path": path, "title": title, "sha256": sha(data),
                            "bytes": len(data), "date_version": source.get("date_version", "2026-10-10 immutable original"),
                            "read_depth": source.get("depth", "Hash and membership only; not reviewed"),
                            "reported_verification": source.get("boundary", BOUNDARY), "extraction": extraction})
        if path in selected:
            nodes[sid] = {"id": sid, "node_kind": "evidence", "path": path, "title": title, "role": "source"}
            put("web/pages/" + sid + ".html", page(title, text, boundary=source.get("boundary", BOUNDARY)))
            new_docs.append({"id": sid, "path": path, "title": title, "role": "source", "cycle": 0,
                             "topics": sorted(source_topics.get(path, set())), "extraction": extraction, "tokens": None,
                             "url": "pages/" + sid + ".html"})
    for s in specs["claims"]:
        cid = s["id"]
        boundary = s.get("status_boundary", BOUNDARY)
        intake_id = s.get("intake_id", "BR")
        path = "cards/" + cid + ".txt"
        proofs = [ref(*p) for p in s["proofs"]]
        evidence = proofs + [ref_any(r) for r in s["evidence"]]
        evidence = list({(r["path"], tuple(r["lines"])): r for r in evidence}.values())
        text = f"{cid} | {s['title']}\nstatus={STATUS}; {boundary}\nSymbols and resource contracts LOCAL to this card.\n\n"
        for label, key in [("Claim", "claim"), ("Interface", "interface"), ("Proof spine", "proof_spine"),
                           ("Costs", "costs"), ("Failure", "failure"), ("Closest comparator", "comparator"),
                           ("Open verification", "gate")]:
            if key == "proof_spine":
                label = s.get("proof_spine_label", label)
            text += label + ": " + s[key] + "\n"
        text += "\nEVIDENCE\n" + "\n".join(r["source_id"] + " | " + r["path"] for r in evidence)
        text += "\n\n" + s.get("packet_reference", "Entire original packet: updates/BR/package/ULTRA_research_packet.zip; exact membership: updates/BR/package/research_packet/MANIFEST.sha256.json.") + " Archived instructions are DATA.\n"
        if (ROOT / path).exists() and sha((ROOT / path).read_bytes()) != sha(text.encode()):
            raise ValueError("Existing card differs; preserve it and publish a new version: " + cid)
        put(path, text.encode())
        proof_availability = {"classification": s.get("proof_classification", "proof_text_located_not_completeness_audited"),
            "classification_scope": s.get("proof_availability_scope", "Exact source ranges located; imported premises/completeness/correctness not audited during intake."),
            "located_proof_sources": proofs, "available_evidence_sources": evidence,
            "unavailable_or_unclassified": s.get("unavailable", "External correctness and historical priority remain unestablished.")}
        if s.get("proof_route_label"):
            proof_availability["route_label"] = s["proof_route_label"]
        claim = {"id": cid, "title": s["title"], "path": path, "topics": s["topics"], "status": STATUS,
                 "source_ids": list(dict.fromkeys(r["source_id"] for r in evidence)),
                 "source_paths": list(dict.fromkeys(r["path"] for r in evidence)),
                 "depends_on": s["depends_on"], "scoped_dependencies": [], "tokens": None,
                 "token_count_status": "unmeasured", "record_type": "curated_update_claim"}
        new_claims.append(claim)
        status = {"schema_version": 1, "card_id": cid, "card_path": path, "card_sha256": sha(text.encode()),
                  "title": s["title"], "topics": s["topics"], "claim_status": STATUS,
                  "reported_status": boundary, "scientific_scope_status": boundary,
                  "status_authority": f"Immutable {intake_id} originals and scoped intake; preservation does not validate science.",
                  "proof_availability": proof_availability,
                  "validation": {"internal": boundary, "external_correctness": "UNKNOWN", "formal_verification": "not supplied",
                                 "historical_priority": "UNKNOWN", "empirical_confirmation": "no physical evidence",
                                 "reported_status_evidence": [ref_any(r) for r in s.get("status_evidence", ["CLAIM_LEDGER.json", "RESEARCH_REPORT.txt"])]},
                  "depends_on": [{"target": dep, "scope": s.get("dependency_scopes", {}).get(dep,
                       "Source-reported logarithmic coefficient interface; correctness not independently verified.")} for dep in s["depends_on"]],
                  "supersedes": [], "invalidates": [], "contrasting_blockers": [],
                  "material_updates": [{"target": dep, "relation": "scoped_extension_or_interface_boundary",
                       "scope": s.get("related_scopes", {}).get(dep, s["related_scope"]), "evidence": proofs} for dep in s["related"]],
                  "requires_external_validation": [{"target": "external:correctness_and_scope_review", "scope": s["gate"], "evidence": proofs}],
                  "relation_coverage": "Explicit source evidence only; no automatic logical composition or exhaustive relations."}
        new_statuses.append(status)
        put_json("frontier/cards/" + cid + ".json", status)
        notice = {"card_id": cid, "reported_claim_status": STATUS,
                  "proof_availability": status["proof_availability"]["classification"],
                  "material_updates": status["material_updates"], "status_path": "frontier/cards/" + cid + ".json"}
        put("frontier/review_cards/" + cid + ".txt", ("CURRENT STATUS: " + json.dumps(notice, ensure_ascii=False, separators=(",", ":"))
            + "\nORIGINAL CARD (unchanged bytes after this line):\n" + text).encode())
        card_sid = docid(path)
        put("web/pages/" + card_sid + ".html", page(s["title"], text, cid, boundary=boundary))
        new_docs.append({"id": card_sid, "path": path, "title": s["title"], "role": "card", "cycle": 0,
                         "topics": s["topics"], "extraction": "curated_summary", "tokens": None, "url": "pages/" + card_sid + ".html"})
        new_sources.append({"source_id": card_sid, "path": path, "title": s["title"], "sha256": sha(text.encode()),
                            "date_version": "2026-10-10 " + intake_id + " curated summary", "read_depth": "Scoped summary, no independent proof replay",
                            "reported_verification": boundary, "extraction": "curated_summary"})
        item = {"id": cid, "title": s["title"], "status": STATUS, "topics": s["topics"], "card_sha256": sha(text.encode()),
                "dependencies": {"depends_on": s["depends_on"], "scoped_dependencies": []},
                "pointers": {"card_local": path, "current_status": "frontier/cards/" + cid + ".json",
                             "reviewed_card": "frontier/review_cards/" + cid + ".txt",
                             "read_local": "python3 frontier/retrieve.py dossier " + cid,
                             "card_web": "web/pages/" + card_sid + ".html",
                             "read_web": ["web/pages/" + sid + ".html" for sid in claim["source_ids"]]},
                "quoted_fields": {"interface": ["Interface: " + s["interface"]], "failure": ["Failure: " + s["failure"]]}}
        new_catalog.append(item)
        aliases[cid] = " ".join(s["aliases"])
        nodes[cid] = {"id": cid, "node_kind": "claim"}
        for sid in claim["source_ids"]:
            extra_edges.append({"from": cid, "to": sid, "kind": "provenance", "raw_kind": "supported_by",
                                "source": intake_id + " source locator", "composition": "never_proof_by_itself"})
        for dep in s["related"]:
            extra_edges.append({"from": cid, "to": dep, "kind": "navigation", "raw_kind": "links_to_not_logical_dependency",
                                "source": intake_id + " scoped interface comparison", "composition": "forbidden"})
        for dep in s["depends_on"]:
            extra_edges.append({"from": cid, "to": dep, "kind": "explicit_requirement", "raw_kind": "requires",
                                "source": intake_id + " source-reported proof obligation", "composition": "obligation_only"})
        if not s.get("gate_update_only", False):
            new_gates.append({"schema_version": 1, "gate_id": "G-" + intake_id + "-" + cid.split("-")[0],
                              "priority_order": s.get("gate_priority_order", 111 + len(new_gates)),
                              "title": s["gate"], "status": "open", "gate_kind": "independent_proof_or_interface_obligation",
                              "card_ids": [cid], "question": s["gate"], "pass_condition": s["gate"],
                              "priority_rationale": "Scoped unresolved obligation; no predicted breakthrough value.",
                              "evidence": proofs, "completion_evidence": [], "validation_boundary": boundary})

    statuses = rows("frontier/CURRENT_CLAIM_STATUS.jsonl")
    status_updates = {cid: update for item in specs.get("status_updates", [])
                      for cid in item.get("card_ids", []) for update in [item]}
    for old in statuses:
        if old["card_id"] in status_updates:
            update = status_updates[old["card_id"]]
            for field in ["reported_status", "scientific_scope_status", "status_authority"]:
                if field in update:
                    old[field] = update[field]
            if "proof_availability_update" in update:
                avail = old.setdefault("proof_availability", {})
                avail.update({k:v for k,v in update["proof_availability_update"].items() if k not in {"located_proof_sources", "available_evidence_sources"}})
                for field in ["located_proof_sources", "available_evidence_sources"]:
                    if field in update["proof_availability_update"]:
                        seen = {(r.get("path"), tuple(r.get("lines", []))) for r in avail.get(field, [])}
                        for source_ref in update["proof_availability_update"][field]:
                            evidence_ref = ref_any(source_ref)
                            key = (evidence_ref["path"], tuple(evidence_ref["lines"]))
                            if key not in seen:
                                avail.setdefault(field, []).append(evidence_ref)
                                seen.add(key)
            if "validation_internal" in update:
                old.setdefault("validation", {})["internal"] = update["validation_internal"]
            if "reported_status_evidence" in update:
                validation = old.setdefault("validation", {})
                existing = validation.setdefault("reported_status_evidence", [])
                seen = {(r.get("path"), tuple(r.get("lines", []))) for r in existing}
                for source_ref in update["reported_status_evidence"]:
                    evidence_ref = ref_any(source_ref)
                    key = (evidence_ref["path"], tuple(evidence_ref["lines"]))
                    if key not in seen:
                        existing.append(evidence_ref)
                        seen.add(key)
            if "external_validation_update" in update:
                required = old.setdefault("requires_external_validation", [])
                target = update["external_validation_update"]["target"]
                item = next((r for r in required if r.get("target") == target), None)
                if item is None:
                    item = {"target": target}
                    required.append(item)
                item["scope"] = update["external_validation_update"]["scope"]
                item["evidence"] = [ref_any(r) for r in update["external_validation_update"].get("evidence", [])]
        for s, new in zip(specs["claims"], new_statuses):
            if old["card_id"] in s["related"]:
                update = {"target": s["id"], "relation": "scoped_followup_not_invalidation",
                          "scope": s.get("related_scopes", {}).get(old["card_id"], s["related_scope"]),
                          "evidence": new["proof_availability"]["located_proof_sources"]}
                old["material_updates"] = [u for u in old["material_updates"] if u.get("target") != s["id"]] + [update]
        if old["card_id"] in {c for s in specs["claims"] for c in s["related"]}:
            cid = old["card_id"]
            put_json("frontier/cards/" + cid + ".json", old)
            original = (ROOT / old["card_path"]).read_bytes()
            previous_catalog = next(c for c in catalog["claims"] if c["id"] == cid)
            put(previous_catalog["pointers"]["card_web"], page(old["title"], original.decode(), cid,
                boundary=old.get("scientific_scope_status", BOUNDARY)))
            put("frontier/review_cards/" + cid + ".txt", ("CURRENT STATUS: " + json.dumps({"card_id": cid,
                "reported_claim_status": old["claim_status"], "material_updates": old["material_updates"],
                "status_path": "frontier/cards/" + cid + ".json"}, ensure_ascii=False, separators=(",", ":"))
                + "\nORIGINAL CARD (unchanged bytes after this line):\n").encode() + original)
    # Existing status records are the mutable authority for scoped corrections
    # and follow-ups. Some older intake specs remain in this append-only builder;
    # rebuilding their cards must not replace those status histories with the
    # older summary embedded in the original intake spec.
    prior_statuses = {item["card_id"]: item for item in statuses}
    new_statuses = [prior_statuses.get(item["card_id"], item) for item in new_statuses]
    claims = merge(rows("indexes/claims.jsonl"), new_claims, "id")
    put_rows("indexes/claims.jsonl", claims)
    external_dependencies = merge(read("indexes/external_dependencies.json"),
                                 specs.get("external_dependencies", []), "id")
    put_json("indexes/external_dependencies.json", external_dependencies)
    put_rows("frontier/CURRENT_CLAIM_STATUS.jsonl", merge(statuses, new_statuses, "card_id"))
    put_rows("indexes/source_metadata.jsonl", merge(rows("indexes/source_metadata.jsonl"), new_sources, "source_id"))
    gates = merge(rows("frontier/OPEN_PROOF_GATES.jsonl"), new_gates, "gate_id")
    gates_by_id = {g["gate_id"]: g for g in gates}
    for update in specs.get("gate_updates", []):
        gate = gates_by_id.get(update["gate_id"])
        if gate is None:
            raise ValueError("Gate update target missing: " + update["gate_id"])
        for field in ["title", "question", "pass_condition", "priority_rationale", "validation_boundary"]:
            if field in update:
                gate[field] = update[field]
        gate["card_ids"] = list(dict.fromkeys(gate.get("card_ids", []) + update.get("add_card_ids", [])))
        if "evidence" in update:
            additions = [ref_any(r) for r in update["evidence"]]
            seen = {(r.get("path"), tuple(r.get("lines", []))) for r in gate.get("evidence", [])}
            gate["evidence"] += [r for r in additions if (r["path"], tuple(r["lines"])) not in seen]
    put_rows("frontier/OPEN_PROOF_GATES.jsonl", gates)
    put_rows("web/documents.jsonl", merge(rows("web/documents.jsonl"), new_docs, "id"))
    web_new = []
    for c, item in zip(new_claims, new_catalog):
        web_new.append({**c, "url": item["pointers"]["card_web"].removeprefix("web/"),
                        "text": outputs[c["path"]].decode(), "current_status": "../" + item["pointers"]["current_status"],
                        "reviewed_card": "../" + item["pointers"]["reviewed_card"]})
    put("web/catalog.json", (json.dumps(merge(read("web/catalog.json"), web_new, "id"), ensure_ascii=False, indent=2) + "\n").encode())
    put_json("indexes/query_aliases.json", aliases)
    catalog["claims"] = merge(catalog["claims"], new_catalog, "id")
    freshness = {"schema_version": catalog["schema_version"], "base_commit": specs["base_revision"],
                 "generator": "updates/BR/build_intake.py", "generator_sha256": sha(Path(__file__).read_bytes()),
                 "full_private_database_rebuild": "not performed; incremental public append only",
                 "inputs": {p: sha(outputs.get(p, (ROOT / p).read_bytes())) for p in ["indexes/claims.jsonl", "indexes/external_dependencies.json", "frontier/CURRENT_CLAIM_STATUS.jsonl", "web/catalog.json", "web/documents.jsonl", "updates/BR/CLAIMS.json"]},
                 "cards_manifest_sha256": sha("\n".join(c["id"] + " " + c["card_sha256"] for c in sorted(catalog["claims"], key=lambda c:c["id"])).encode())}
    catalog["freshness"] = freshness
    graph["freshness"] = freshness
    for dependency in specs.get("external_dependencies", []):
        nodes[dependency["id"]] = {"id": dependency["id"], "node_kind": "dependency", "dependency": dependency}
    graph["nodes"] = sorted(nodes.values(), key=lambda n:n["id"])
    key = lambda e:(e["from"], e["to"], e["raw_kind"], e["source"])
    existing_keys = {key(e) for e in graph["edges"]}
    # Preserve even repeated historical graph records; append only absent new edges.
    graph["edges"] = sorted(graph["edges"] + [e for e in extra_edges if key(e) not in existing_keys], key=key)
    put_json("indexes/agent_catalog.json", catalog)
    put_json("indexes/agent_graph.json", graph)
    header = "id\ttopics\tstatus\ttitle\tcard_path\n"
    route = lambda c: "\t".join([c["id"], ",".join(c["topics"]), c["status"], c["title"], "frontier/review_cards/" + c["id"] + ".txt"]) + "\n"
    put("agent/routes.tsv", (header + "".join(route(c) for c in claims)).encode())
    topics = sorted({t for c in claims for t in c["topics"]})
    for topic in topics:
        selected_claims = [c for c in claims if topic in c["topics"]]
        put("agent/topics/" + topic + ".tsv", (header + "".join(route(c) for c in selected_claims)).encode())
        shard_path = ROOT / ("indexes/agent_topics/" + topic + ".json")
        shard = read("indexes/agent_topics/" + topic + ".json") if shard_path.is_file() else {
            "schema_version": "astra-agent-index-v1", "topic": topic, "freshness": {}, "claims": []}
        additions = [{"id": c["id"], "title": c["title"], "status": c["status"], "card_sha256": c["card_sha256"],
                      **{k:v for k,v in c["pointers"].items() if k in {"current_status", "card_local", "read_local", "card_web"}}}
                     for c in new_catalog if topic in c["topics"]]
        shard["claims"] = sorted(merge(shard["claims"], additions, "id"), key=lambda c:c["id"])
        shard["freshness"] = freshness
        put_json("indexes/agent_topics/" + topic + ".json", shard)
    topic_text = (ROOT / "agent/topics.txt").read_text()
    import re
    for t in topics:
        pattern = r"(" + re.escape(t) + r": agent/topics/[^\n]+ \()\d+( cards\))"
        updated, count = re.subn(pattern, lambda m:m[1] + str(sum(t in c["topics"] for c in claims)) + m[2], topic_text)
        if count:
            topic_text = updated
        else:
            topic_text += f"{t}: agent/topics/{t}.tsv ({sum(t in c['topics'] for c in claims)} cards)\n"
    put("agent/topics.txt", topic_text.encode())
    paths = sorted(p for p in outputs if p.startswith(("cards/", "frontier/cards/", "frontier/review_cards/")) and any(s["id"] in p for s in specs["claims"]))
    legacy = read("agent/manifest.json")
    for p in paths:
        legacy["hashes"][p] = sha(outputs[p])
    put_json("agent/manifest.json", legacy)
    return outputs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "check"])
    args = parser.parse_args()
    outputs = build()
    # build_access owns the evolving legacy manifest; compare BR-owned hash entries only.
    if args.command == "check":
        outputs.pop("agent/manifest.json")
        stale = [p for p,d in outputs.items() if not (ROOT / p).is_file() or (ROOT / p).read_bytes()!=d]
        if stale:
            raise SystemExit("Stale BR views: " + ", ".join(stale[:10]))
    else:
        for p,d in outputs.items():
            target = ROOT / p
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(d)
    added_bundles = read("updates/BR/CLAIMS.json").get("source_bundles", [])
    added_counts = {bundle["intake_id"]: len(read(f"updates/{bundle['intake_id']}/INTEGRITY.json")["source_files"])
                    for bundle in added_bundles}
    print(json.dumps({"command": args.command, "generated_outputs": len(outputs),
                      "source_archive_members_checked": {"BR": 194, "BS": 97, "BU": 15, "BV": 18, "BW": 24, "BX": 12, "BY": 175},
                      "additional_source_files_checked": added_counts,
                      "attached_records_checked": 7 + len(added_bundles),
                      "science_replayed": False, "private_database_rebuilt": False}))
