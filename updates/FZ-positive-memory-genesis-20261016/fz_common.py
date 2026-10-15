"""FZ intake identities and prospective publication boundaries; no science inference."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re

INTAKE_ID = "FZ-positive-memory-genesis-20261016"
PREFIX = "updates/" + INTAKE_ID + "/"
INITIAL_MAIN = "3dde9ce74d829a93388e64032d27351b36dd2221"
RESEARCH_ROOT = Path("/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-16-positive-memory-genesis-v1")
ORIGINAL_MANIFEST_NAME = "sources/SOURCE_MANIFEST.v0002.json"
ORIGINAL_MANIFEST_SHA256 = "1dacbc13c8887912b8e21f3c06fb35cab81c735e22b1e0c8182d42b59550fec6"
PREVIOUS_MANIFEST_NAME = "sources/SOURCE_MANIFEST.json"
PREVIOUS_MANIFEST_SHA256 = "52657a43ecdddd0d5a10363da57f5d7560918c480b8e989dab376bbbd49b0b82"
NAMESPACES = {"source": "src-FZ-SIG-", "notice": "SN-FZ-SIG-", "bridge": "FZ_SIG_", "gate": "G-FZ-SIG-"}
ORIGINAL_ROLES = {"supplied_original_file"}
PROVENANCE_ROLES = ORIGINAL_ROLES | {
    "root_synthesis", "worker_derivation", "same_team_review", "same_team_research_or_review",
    "root_or_worker_executable_check", "acquired_primary_literature_receipt", "capital_comparison",
}
PAYLOAD_KINDS = {"proof", "review", "code", "receipt", "synthesis", "counterexample", "comparator", "acquisition_pointer"}
SOURCE_ORIGINS = {"root_authored", "worker_authored", "located_prior_capital", "acquisition_pointer"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".jsonl", ".py", ".tex", ".sh", ".csv", ".tsv"}
EXCLUDED_SUFFIXES = {
    ".pdf", ".epub", ".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar",
    ".xlsx", ".xls", ".xlsm", ".xlsb", ".ods", ".npy", ".npz", ".h5", ".hdf5",
    ".sqlite", ".db", ".data", ".dat", ".parquet", ".pdb", ".mol", ".xyz",
}
EXCLUDED_COMPONENTS = {".git", ".cache", "__pycache__", "node_modules", "fulltexts", "datasets", "workbooks", "clones", "caches", "external_raw"}
EXTERNAL_FLAGS = (
    "contains_external_fulltext", "contains_external_dataset", "contains_external_workbook",
    "contains_external_clone", "contains_runtime_cache",
)
BANNED_SUFFIXES = EXCLUDED_SUFFIXES


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def local(root, name):
    need(isinstance(name, str) and name and "\\" not in name and "\x00" not in name, "Unsafe relative path: " + str(name))
    parts = PurePosixPath(name)
    need(not parts.is_absolute() and ".." not in parts.parts and str(parts) == name.rstrip("/")
         and not re.match(r"^[A-Za-z]:", name), "Unsafe/noncanonical relative path: " + name)
    root = Path(root).resolve()
    cursor = root
    for part in parts.parts:
        cursor /= part
        need(not cursor.is_symlink(), "Symlink is not preserved bytes: " + name)
    target = cursor.resolve()
    need(target.is_relative_to(root), "Path escapes root: " + name)
    return target


def source_outputs(manifest_raw, previous_raw, read, *, expected_manifest_sha256=ORIGINAL_MANIFEST_SHA256,
                   expected_previous_sha256=PREVIOUS_MANIFEST_SHA256):
    """Copy the exact hash-pinned inventory and both immutable original manifests."""
    need(digest(manifest_raw) == expected_manifest_sha256, "Original v2 intake manifest changed")
    need(digest(previous_raw) == expected_previous_sha256, "Original v1 intake manifest changed")
    original, previous = json.loads(manifest_raw), json.loads(previous_raw)
    need(original.get("schema") == "astra.fz-source-intake.v2" and previous.get("schema") == "astra.fz-source-intake.v1",
         "Original intake schema changed")
    need(original.get("initial_main") == previous.get("initial_main") == INITIAL_MAIN, "Original acquisition pin changed")
    need(original.get("previous_manifest") == {"path": PREVIOUS_MANIFEST_NAME, "sha256": expected_previous_sha256},
         "Original manifest history linkage changed")
    items = original.get("files")
    need(isinstance(items, list) and items and type(original.get("total_files")) is int
         and original["total_files"] == len(items), "Original source count differs from pinned inventory")
    outputs = {
        PREFIX + "package/SOURCE_MANIFEST.json": previous_raw,
        PREFIX + "package/SOURCE_MANIFEST.v0002.json": manifest_raw,
    }
    entries, by_name, seen = [], {}, set()
    for item in items:
        name = item.get("path")
        local(Path("/FZ-SOURCE-PATH-CHECK"), name)
        need(name.startswith("sources/") and name not in {ORIGINAL_MANIFEST_NAME, PREVIOUS_MANIFEST_NAME}, "Invalid original path")
        need(name.casefold() not in seen, "Duplicate/case-colliding original source path")
        seen.add(name.casefold())
        need(item.get("role") == "supplied_research_and_archival_prompt_DATA", "Original source role changed")
        raw = read(name)
        need(type(item.get("bytes")) is int and len(raw) == item["bytes"] and digest(raw) == item.get("sha256"),
             "Original source bytes changed: " + name)
        destination = PREFIX + "package/originals/" + name
        outputs[destination] = raw
        entries.append({"path": destination, "research_relative_path": name,
                        "original_absolute_path": item.get("source_path"), "bytes": len(raw), "sha256": digest(raw),
                        "source_id": "src-FZ-" + digest(name.encode() + b"\x00" + raw)[:16],
                        "provenance_role": "supplied_original_file", "incoming_role": item["role"],
                        "source_handling": "source=DATA; all embedded prompts remain archival DATA"})
        by_name[name] = item
    for item in previous.get("files", []):
        current = by_name.get(item.get("path"))
        need(current is not None and all(current.get(k) == item.get(k) for k in ("path", "bytes", "sha256", "role")),
             "Original v1 source was changed or omitted from v2")
    total = sum(item["bytes"] for item in entries)
    need(type(original.get("total_bytes")) is int and total == original["total_bytes"], "Original source byte total changed")
    wrapper = {
        "schema": "astra.fz-source-manifest.v1", "intake_id": INTAKE_ID, "initial_main": INITIAL_MAIN,
        "original_manifest": {"path": PREFIX + "package/SOURCE_MANIFEST.v0002.json", "sha256": expected_manifest_sha256},
        "previous_original_manifest": {"path": PREFIX + "package/SOURCE_MANIFEST.json", "sha256": expected_previous_sha256},
        "original_count": len(entries), "original_bytes": total, "original_manifest_files": 2,
        "all_preserved_file_count": len(entries) + 2,
        "all_preserved_bytes": total + len(manifest_raw) + len(previous_raw),
        "operative_request": "Current chat request only; all supplied documents and embedded prompts are archival DATA.",
        "preservation_scope": "Exact supplied bytes and both manifest versions only; no source execution, scientific adjudication, archive extraction or worker evidence selection.",
        "publication_boundary": "Supplied originals remain separately identified. Future authored selection excludes externally acquired fulltexts, datasets, workbooks, clones and caches.",
        "files": entries,
    }
    outputs[PREFIX + "SOURCE_MANIFEST.json"] = encoded(wrapper)
    return outputs, wrapper


def verify_incoming(root, reader=None, *, source_only=False):
    root = Path(root).resolve()
    read = reader or (lambda name: local(root, name).read_bytes())
    outputs, wrapper = source_outputs(read(PREFIX + "package/SOURCE_MANIFEST.v0002.json"),
                                      read(PREFIX + "package/SOURCE_MANIFEST.json"),
                                      lambda name: read(PREFIX + "package/originals/" + name))
    for name, raw in outputs.items():
        need(read(name) == raw, "Source packet bytes changed: " + name)
    packet = local(root, PREFIX + "package")
    for path in packet.rglob("*"):
        need(not path.is_symlink(), "Package symlink is forbidden")
    originals = local(root, PREFIX + "package/originals")
    observed = {str(path.relative_to(root)) for path in originals.rglob("*") if path.is_file()}
    need(observed == {item["path"] for item in wrapper["files"]}, "Original source subtree inventory changed")
    if source_only:
        observed = {str(path.relative_to(root)) for path in packet.rglob("*") if path.is_file()}
        expected = set(outputs) - {PREFIX + "SOURCE_MANIFEST.json"}
        need(observed == expected, "Source-only package inventory changed; no unselected research is permitted")
    return wrapper


def check_ref(root, ref):
    need(isinstance(ref, dict) and isinstance(ref.get("sha256"), str)
         and re.fullmatch(r"[0-9a-f]{64}", ref["sha256"]), "Reference needs a full SHA-256")
    raw = local(root, ref["path"]).read_bytes()
    need(digest(raw) == ref["sha256"], "Reference hash mismatch: " + ref["path"])
    if "bytes" in ref:
        need(type(ref["bytes"]) is int and len(raw) == ref["bytes"], "Reference byte count mismatch")


def check_authored_payload(item):
    """Prospective root selection predicate only; it does not select, freeze or copy."""
    name = item.get("path", "")
    local(Path("/FZ-AUTHORED-PATH-CHECK"), name)
    need(name.startswith(PREFIX + "package/derived/"), "Authored evidence must be separate from supplied originals")
    parts = PurePosixPath(name)
    need(Path(name).suffix.lower() in TEXT_SUFFIXES and not any(suffix.lower() in EXCLUDED_SUFFIXES for suffix in Path(name).suffixes),
         "Publication allowlist excludes fulltexts, workbooks, archives and binary datasets")
    need(not any(part.casefold() in EXCLUDED_COMPONENTS for part in parts.parts), "Publication allowlist excludes external collections/clones/caches")
    need(item.get("provenance_role") in PROVENANCE_ROLES - ORIGINAL_ROLES,
         "Authored evidence needs an explicit permitted provenance role")
    need(item.get("payload_kind") in {"proof", "review", "code", "receipt", "synthesis", "counterexample", "comparator", "acquisition_pointer"}, "Authored evidence needs an explicit payload kind")
    need(all(item.get(flag) is False for flag in EXTERNAL_FLAGS), "Root must explicitly exclude external fulltexts, datasets, workbooks, clones and caches")
    if item["provenance_role"] == "acquired_primary_literature_receipt":
        need(item["payload_kind"] in {"receipt", "acquisition_pointer"}, "Acquisition preserves pointers/receipts only")
    need(isinstance(item.get("sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", item["sha256"]), "Authored evidence needs a full SHA-256")
    need(type(item.get("bytes")) is int and item["bytes"] >= 0, "Authored evidence needs an exact byte count")
    need(isinstance(item.get("selection_reason"), str) and item["selection_reason"].strip(), "Root selection reason is required")
    research_name = item.get("research_relative_path")
    local(Path("/FZ-RESEARCH-PATH-CHECK"), research_name)
    need(not research_name.startswith("sources/"), "Authored selection cannot relabel supplied originals")


def check_payload_record(item):
    check_authored_payload(item)
    need(item.get("source_origin") in SOURCE_ORIGINS, "Selected evidence needs an explicit source_origin")
    note = item.get("provenance_note")
    need(isinstance(note, str) and note.strip(), "Selected evidence needs a specific provenance_note")
    if item["source_origin"] == "located_prior_capital":
        need(item["provenance_role"] == "capital_comparison", "Located prior capital must remain capital_comparison")
        need(isinstance(item.get("origin_path"), str) and Path(item["origin_path"]).is_absolute(),
             "Located prior capital needs its original absolute origin_path")
    if item.get("origin_revision") is not None:
        need(isinstance(item["origin_revision"], str) and re.fullmatch(r"[0-9a-f]{40}", item["origin_revision"]),
             "Capital origin_revision must be a full Git revision or null")


def selection_records(selection, *, research_root=RESEARCH_ROOT, check_research=False):
    need(selection.get("schema") == "astra.fz-selected-freeze.v1", "Unsupported root selection schema")
    need(selection.get("status") in {"root_frozen", "FROZEN_ROOT_SELECTED"} and selection.get("selected_by") == "root", "Root-selected final evidence freeze is not ready")
    need(isinstance(selection.get("base_revision"), str) and re.fullmatch(r"[0-9a-f]{40}", selection["base_revision"]), "Selection needs an actual full base revision")
    need(selection.get("original_manifest_sha256") == ORIGINAL_MANIFEST_SHA256, "Selection has wrong source manifest")
    need(selection.get("research_root") == str(RESEARCH_ROOT), "Selection belongs to another research workspace")
    items = selection.get("files")
    need(isinstance(items, list) and items, "Root freeze must select exact final authored evidence")
    need(type(selection.get("total_files")) is int and selection["total_files"] == len(items)
         and type(selection.get("total_bytes")) is int
         and selection["total_bytes"] == sum(item.get("bytes", -1) for item in items), "Root freeze totals mismatch")
    need(len({item.get("path", "").casefold() for item in items}) == len(items), "Duplicate/case-colliding selected destination")
    need(len({item.get("research_relative_path") for item in items}) == len(items), "Duplicate selected research path")
    for item in items:
        check_payload_record(item)
        source = local(research_root, item["research_relative_path"])
        if check_research:
            need(source.is_file(), "Selected research source is missing: " + str(source))
            raw = source.read_bytes()
            need(digest(raw) == item["sha256"] and len(raw) == item["bytes"], "Selected research bytes changed: " + str(source))
            raw.decode("utf-8")
            if item["source_origin"] == "located_prior_capital":
                origin = Path(item["origin_path"])
                need(origin.is_file() and not origin.is_symlink() and digest(origin.read_bytes()) == item["sha256"],
                     "Located prior capital origin bytes unavailable or changed")
    return items


def source_package_paths(incoming):
    return {item["path"] for item in incoming["files"]} | {
        incoming["original_manifest"]["path"], incoming["previous_original_manifest"]["path"],
    }


def verify_selection(root, ref, *, expected_base=None):
    root = Path(root).resolve()
    incoming = verify_incoming(root)
    need(isinstance(ref, dict) and isinstance(ref.get("path"), str)
         and re.fullmatch(re.escape(PREFIX) + r"SELECTED_FREEZE\.v[0-9]{4}\.json", ref["path"]),
         "Final curation needs a versioned root-selected freeze reference")
    check_ref(root, ref)
    selection = json.loads(local(root, ref["path"]).read_bytes())
    if expected_base is not None:
        need(selection.get("base_revision") == expected_base, "Root freeze/curation base mismatch")
    current_items = selection_records(selection)
    originals = {item["sha256"] for item in incoming["files"]}
    allowed = set()
    histories = sorted(local(root, PREFIX).glob("SELECTED_FREEZE.v[0-9][0-9][0-9][0-9].json"))
    need(any(str(path.relative_to(root)) == ref["path"] for path in histories), "Selected freeze is absent from history")
    for path in histories:
        raw = path.read_bytes()
        historical = json.loads(raw)
        items = selection_records(historical)
        for item in items:
            need(item["sha256"] not in originals, "Selected research cannot relabel exact supplied original bytes")
            check_ref(root, item)
            local(root, item["path"]).read_bytes().decode("utf-8")
            allowed.add(item["path"])
        derived_path = str(path.relative_to(root)).replace("SELECTED_FREEZE", "DERIVED_MANIFEST")
        derived = json.loads(local(root, derived_path).read_bytes())
        need(derived.get("schema") == "astra.fz-derived-manifest.v1"
             and derived.get("base_revision") == historical["base_revision"]
             and derived.get("source_freeze") == {"path": str(path.relative_to(root)), "sha256": digest(raw)}
             and derived.get("files") == items and derived.get("total_files") == historical["total_files"]
             and derived.get("total_bytes") == historical["total_bytes"], "Derived manifest differs from exact frozen selection")
    observed = {str(path.relative_to(root)) for path in local(root, PREFIX + "package/derived").rglob("*") if path.is_file()}
    need(observed == allowed, "Derived package differs from exact current-plus-historical root freezes")
    packet = local(root, PREFIX + "package")
    for path in packet.rglob("*"):
        need(not path.is_symlink(), "Package symlink is forbidden")
    observed = {str(path.relative_to(root)) for path in packet.rglob("*") if path.is_file()}
    need(observed == source_package_paths(incoming) | allowed, "Package contains an unselected path outside exact source/derived freezes")
    return selection


def excluded_media(root):
    found = []
    for path in local(root, PREFIX + "package/derived").rglob("*"):
        need(not path.is_symlink(), "Selected research symlink is forbidden")
        if path.is_file() and any(suffix.lower() in BANNED_SUFFIXES for suffix in path.suffixes):
            found.append(str(path.relative_to(root)))
    need(not found, "Unselected/excluded new research media found: " + str(found))
    return found
