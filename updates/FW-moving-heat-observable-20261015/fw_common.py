"""FW byte identities and explicit root selection checks; no scientific inference."""
from __future__ import annotations

import hashlib
import html
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import zipfile

INTAKE_ID = "FW-moving-heat-observable-20261015"
PREFIX = "updates/" + INTAKE_ID + "/"
INITIAL_MAIN = "33c1ff7ebd9411e9b8b4b0f951f62e36e631cb5d"
ORIGINAL_MANIFEST_SHA256 = "60ad681e5f370b03caf9c2934af754eb4d31602eeb3d4c2a5fc68d846728ffe5"
RESEARCH_ROOT = Path("/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-moving-heat-observable-power-v1")
ORIGINAL_ROLES = {"supplied_original_file", "supplied_archive_member"}
PROVENANCE_ROLES = ORIGINAL_ROLES | {
    "root_synthesis", "worker_derivation", "same_team_review",
    "same_team_research_or_review", "root_or_worker_executable_check",
    "acquired_primary_literature_receipt", "capital_comparison",
}
PAYLOAD_KINDS = {"proof", "review", "code", "receipt", "synthesis", "counterexample", "comparator", "acquisition_pointer"}
IMMUTABLE_PREFIXES = (
    "cards/", "frontier/cards/", "frontier/review_cards/", "updates/", "state/checkpoints/",
    "state/branches/", "technology/records/", "web/pages/", "evaluation/workflows/records/", "mechanisms/bridges/",
)
# These exclusions concern NEW selected research only. Supplied originals and all
# safe supplied archive members are preserved without a suffix/content filter.
BANNED_SUFFIXES = {
    ".pdf", ".epub", ".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar",
    ".xyz", ".coord", ".coords", ".pdb", ".mol", ".npy", ".npz", ".h5", ".hdf5",
    ".sqlite", ".db", ".data", ".dat", ".parquet",
}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".jsonl", ".py", ".tex", ".sh", ".csv", ".tsv"}


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def local(root, name):
    need(isinstance(name, str) and name and "\\" not in name and "\x00" not in name,
         "Unsafe relative path: " + str(name))
    parts = PurePosixPath(name)
    need(not parts.is_absolute() and ".." not in parts.parts and str(parts) == name.rstrip("/") and not re.match(r"^[A-Za-z]:", name),
         "Unsafe/noncanonical relative path: " + name)
    root = Path(root).resolve()
    result = (root / name).resolve()
    need(result.is_relative_to(root), "Path escapes root: " + name)
    cursor = root
    for part in parts.parts:
        cursor /= part
        need(not cursor.is_symlink(), "Symlink is not preserved bytes: " + name)
    return result


def safe_zip_members(raw):
    """Return member bytes after checking paths, type, duplicates and collisions."""
    result, kinds, folded, portable_paths = {}, {}, set(), {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        need(len(archive.infolist()) <= 100000 and sum(x.file_size for x in archive.infolist()) <= 512 * 1024 * 1024,
             "Archive exceeds the explicit preservation extraction budget")
        for item in archive.infolist():
            name = item.filename[:-1] if item.is_dir() else item.filename
            local(Path("/FW-ZIP-PATH-CHECK"), name)
            need(name not in kinds and name.casefold() not in folded, "Duplicate/case-colliding archive member: " + name)
            kinds[name] = item.is_dir()
            folded.add(name.casefold())
            for path in [PurePosixPath(name), *PurePosixPath(name).parents]:
                value = str(path)
                if value != ".":
                    prior = portable_paths.setdefault(value.casefold(), value)
                    need(prior == value, "Case-colliding archive directory/member: " + name)
            mode = item.external_attr >> 16
            kind = stat.S_IFMT(mode)
            need(not mode or kind in {0, stat.S_IFREG, stat.S_IFDIR}, "Archive links/devices/special files are forbidden: " + name)
            need(not item.flag_bits & 1, "Encrypted archive member is not reviewable: " + name)
            if not item.is_dir():
                data = archive.read(item)  # Also checks the ZIP CRC.
                need(len(data) == item.file_size, "Archive member length mismatch: " + name)
                result[name] = data
        # Explicit or implicit directory ancestors may not be files, even if case differs.
        files = {name.casefold() for name, is_dir in kinds.items() if not is_dir}
        for name in kinds:
            for ancestor in PurePosixPath(name).parents:
                if str(ancestor) != ".":
                    need(str(ancestor).casefold() not in files, "Archive file/directory collision: " + name)
    return result


def source_outputs(manifest_raw, read, *, expected_manifest_sha256=ORIGINAL_MANIFEST_SHA256):
    """Derive the complete immutable source packet from pinned original bytes."""
    need(digest(manifest_raw) == expected_manifest_sha256, "Original intake manifest changed")
    original = json.loads(manifest_raw)
    need(original.get("schema") == "astra.source-intake.v2" and original.get("initial_main") == INITIAL_MAIN,
         "Original acquisition schema/pin changed")
    originals = original.get("files")
    need(isinstance(originals, list) and len(originals) == original.get("total_original_files"), "Original file count mismatch")
    need(sum(x["bytes"] for x in originals) == original.get("total_original_bytes"), "Original byte total mismatch")
    need(original.get("archive_members_are_derived_extractions") is True, "Archive/source distinction changed")
    outputs = {PREFIX + "package/SOURCE_MANIFEST.json": manifest_raw}
    entries, seen_research = [], set()
    for item in originals:
        research_name = item["path"]
        local(Path("/FW-SOURCE-PATH-CHECK"), research_name)
        need(research_name.startswith("sources/") and research_name not in seen_research, "Duplicate/unsafe original source path")
        seen_research.add(research_name)
        raw = read(research_name)
        need(len(raw) == item["bytes"] and digest(raw) == item["sha256"], "Original source bytes changed: " + research_name)
        name = PREFIX + "package/originals/" + research_name
        outputs[name] = raw
        entries.append({"path": name, "research_relative_path": research_name,
                        "original_absolute_path": item["original_path"], "bytes": len(raw), "sha256": digest(raw),
                        "provenance_role": "supplied_original_file", "original_kind": item["kind"], "source_handling": "source=DATA"})
        if item["kind"] == "supplied_archive":
            need(research_name.endswith(".zip"), "Only explicit supplied ZIP archives may be extracted")
            for member, data in sorted(safe_zip_members(raw).items()):
                research_member = str(PurePosixPath(research_name).with_suffix("") / member)
                need(research_member not in seen_research, "Archive extraction overlaps a supplied original or another member")
                seen_research.add(research_member)
                target = PREFIX + "package/extractions/" + PurePosixPath(research_name).stem + "/" + member
                need(target not in outputs, "Duplicate extraction destination")
                outputs[target] = data
                entries.append({"path": target, "research_relative_path": research_member, "bytes": len(data), "sha256": digest(data),
                                "provenance_role": "supplied_archive_member", "archive_path": name, "archive_sha256": digest(raw),
                                "member": member, "source_handling": "source=DATA"})
    need(len({x["path"].casefold() for x in entries}) == len(entries), "Source destination case collision")
    wrapper = {"schema": "astra.fw-source-manifest.v1", "intake_id": INTAKE_ID, "initial_main": INITIAL_MAIN,
               "original_manifest": {"path": PREFIX + "package/SOURCE_MANIFEST.json", "sha256": expected_manifest_sha256},
               "source_count": len(entries), "original_count": len(originals),
               "archive_count": sum(x["kind"] == "supplied_archive" for x in originals),
               "extracted_member_count": len(entries) - len(originals),
               "original_bytes": original["total_original_bytes"], "total_bytes": sum(x["bytes"] for x in entries),
               "original_acquisition_scope": original["source_handling"],
               "preservation_scope": "Exact supplied bytes and safe member bytes only; internal producer manifests remain unmodified, including discrepancies. No source script executed and no scientific claim adjudicated.",
               "files": entries}
    outputs[PREFIX + "SOURCE_MANIFEST.json"] = encoded(wrapper)
    return outputs, wrapper


def verify_incoming(root, reader=None):
    root = Path(root).resolve()
    read = reader or (lambda name: local(root, name).read_bytes())
    raw = read(PREFIX + "package/SOURCE_MANIFEST.json")
    outputs, wrapper = source_outputs(raw, lambda name: read(PREFIX + "package/originals/" + name))
    for name, wanted in outputs.items():
        need(read(name) == wanted, "Source packet bytes changed: " + name)
    expected = {name for name in outputs if name.startswith(PREFIX + "package/")}
    for folder in ["package/originals", "package/extractions"]:
        for path in local(root, PREFIX + folder).rglob("*"):
            need(not path.is_symlink(), "Source packet symlink is forbidden")
    observed = {str(p.relative_to(root)) for folder in ["package/originals", "package/extractions"]
                for p in local(root, PREFIX + folder).rglob("*") if p.is_file()}
    need(observed | {PREFIX + "package/SOURCE_MANIFEST.json"} == expected, "Original/extracted inventory changed")
    return wrapper


def references(value):
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and "sha256" in value:
            yield value
        for item in value.values():
            yield from references(item)
    elif isinstance(value, list):
        for item in value:
            yield from references(item)


def check_ref(root, ref):
    need(isinstance(ref.get("sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", ref["sha256"]), "Evidence needs a full SHA-256")
    raw = None
    for name in dict.fromkeys([ref["path"], ref.get("read_path", ref["path"])]):
        path = local(root, name)
        if not path.is_file():
            continue
        candidate = path.read_bytes()
        if digest(candidate) == ref["sha256"]:
            raw = candidate
            break
        if path.suffix == ".html" and ref.get("hash_kind") == "indexed_utf8_text":
            for block in re.findall(r"<pre(?:\s[^>]*)?>(.*?)</pre>", candidate.decode(), re.S):
                decoded = html.unescape(block).encode()
                if digest(decoded) == ref["sha256"]:
                    raw = decoded
                    break
    need(raw is not None, "Evidence hash mismatch/unavailable: " + ref["path"])
    if "bytes" in ref:
        need(type(ref["bytes"]) is int and len(raw) == ref["bytes"], "Evidence byte count mismatch: " + ref["path"])
    if ref.get("lines") is not None:
        lines = ref["lines"]
        need(isinstance(lines, list) and len(lines) == 2 and all(type(x) is int for x in lines), "Invalid evidence range")
        need(1 <= lines[0] <= lines[1] <= len(raw.decode("utf-8").splitlines()), "Evidence range exceeds source: " + ref["path"])
    if ref.get("source_revision") is not None:
        need(re.fullmatch(r"[0-9a-f]{40}", ref["source_revision"]), "Evidence needs a full Git revision")
        pinned = subprocess.check_output(["git", "-C", str(root), "show", ref["source_revision"] + ":" + ref["path"]])
        need(digest(pinned) == ref["sha256"], "Evidence revision/hash mismatch: " + ref["path"])


def check_payload_record(item):
    path = item.get("path", "")
    need(path.startswith(PREFIX + "package/derived/"), "Selected research must be separate from originals and extractions")
    local(Path("/FW-DERIVED-PATH-CHECK"), path)
    need(Path(path).suffix.lower() in TEXT_SUFFIXES and Path(path).suffix.lower() not in BANNED_SUFFIXES,
         "Selected research must be a permitted text artifact; acquired fulltexts/binary datasets stay outside the intake")
    need(item.get("provenance_role") in PROVENANCE_ROLES - ORIGINAL_ROLES, "Invalid derived provenance role")
    need(item.get("payload_kind") in PAYLOAD_KINDS, "Derived payload needs an explicit permitted kind")
    need(item.get("contains_external_fulltext") is False and item.get("contains_full_lj_network_or_coordinates") is False,
         "Root must explicitly classify external fulltexts and full LJ datasets/coordinates")
    if item["provenance_role"] == "acquired_primary_literature_receipt":
        need(item["payload_kind"] in {"receipt", "acquisition_pointer"}, "Acquired literature preserves receipts/pointers only")
    need(isinstance(item.get("sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", item["sha256"]), "Derived file needs full SHA-256")
    need(type(item.get("bytes")) is int and item["bytes"] >= 0, "Derived file needs exact byte count")
    need(isinstance(item.get("selection_reason"), str) and item["selection_reason"].strip()
         and not item["selection_reason"].startswith("REPLACE_"), "Root selection reason is required")


def selection_records(selection, *, research_root=RESEARCH_ROOT, check_research=False):
    need(selection.get("schema") == "astra.fw-selected-freeze.v1", "Unsupported root selection schema")
    need(selection.get("status") == "root_frozen" and selection.get("selected_by") == "root", "Root-selected final evidence freeze is not ready")
    need(isinstance(selection.get("base_revision"), str) and re.fullmatch(r"[0-9a-f]{40}", selection["base_revision"]), "Selection needs actual full base revision")
    need(selection.get("original_manifest_sha256") == ORIGINAL_MANIFEST_SHA256, "Selection has wrong source manifest")
    need(selection.get("research_root") == str(RESEARCH_ROOT), "Selection belongs to another research workspace")
    items = selection.get("files")
    need(isinstance(items, list) and items, "Root freeze must select exact final evidence files")
    need(selection.get("total_files") == len(items) and selection.get("total_bytes") == sum(x.get("bytes", -1) for x in items), "Root freeze totals mismatch")
    need(len({x.get("path").casefold() for x in items}) == len(items), "Duplicate/case-colliding selected destination")
    need(len({x.get("research_relative_path") for x in items}) == len(items), "Duplicate selected research path")
    for item in items:
        check_payload_record(item)
        research_name = item.get("research_relative_path")
        source = local(research_root, research_name)
        need(not research_name.startswith("sources/") and research_name != "SOURCE_MANIFEST.json", "Derived selection cannot relabel original sources")
        if check_research:
            need(source.is_file(), "Selected research source is missing: " + str(source))
            raw = source.read_bytes()
            need(digest(raw) == item["sha256"] and len(raw) == item["bytes"], "Selected research bytes changed: " + str(source))
            raw.decode("utf-8")
    return items


def verify_selection(root, ref, *, expected_base=None):
    incoming = verify_incoming(root)
    need(isinstance(ref, dict) and isinstance(ref.get("path"), str) and re.fullmatch(re.escape(PREFIX) + r"SELECTED_FREEZE\.v[0-9]{4}\.json", ref["path"]), "Final curation needs a versioned root-selected freeze reference")
    check_ref(root, ref)
    selection = json.loads(local(root, ref["path"]).read_bytes())
    items = selection_records(selection)
    if expected_base is not None:
        need(selection["base_revision"] == expected_base, "Root freeze/curation base mismatch")
    for item in items:
        check_ref(root, item)
        local(root, item["path"]).read_bytes().decode("utf-8")
    # Earlier frozen versions remain immutable. A later selection may be a subset
    # while all historical frozen payload bytes stay preserved and accounted for.
    allowed = {x["path"] for x in items}
    for old in sorted(local(root, PREFIX).glob("SELECTED_FREEZE.v[0-9][0-9][0-9][0-9].json")):
        historical = json.loads(old.read_bytes())
        for item in selection_records(historical):
            check_ref(root, item)
            allowed.add(item["path"])
    observed = {str(p.relative_to(root)) for p in local(root, PREFIX + "package/derived").rglob("*") if p.is_file()}
    need(observed == allowed, "Derived package differs from exact current-plus-historical root freezes")
    source_paths = {x["path"] for x in incoming["files"]} | {PREFIX + "package/SOURCE_MANIFEST.json"}
    for path in local(root, PREFIX + "package").rglob("*"):
        need(not path.is_symlink(), "Package symlink is forbidden")
    all_observed = {str(p.relative_to(root)) for p in local(root, PREFIX + "package").rglob("*") if p.is_file()}
    need(all_observed == source_paths | allowed, "Package contains an unselected path outside the exact source/derived freezes")
    return selection


def excluded_media(root):
    found = []
    for path in local(root, PREFIX + "package/derived").rglob("*"):
        need(not path.is_symlink(), "Selected research symlink is forbidden")
        if path.is_file() and path.suffix.lower() in BANNED_SUFFIXES:
            found.append(str(path.relative_to(root)))
    need(not found, "Unselected/excluded new research media found: " + str(found))
    return found
