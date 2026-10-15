"""FX byte identities and explicit root selection checks; no scientific inference."""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

INTAKE_ID = "FX-global-completion-axis-20261015"
PREFIX = "updates/" + INTAKE_ID + "/"
INITIAL_MAIN = "ab5118e70a7e6a0dd39e75dd563d3a3f50b06b25"
ORIGINAL_MANIFEST_SHA256 = "95bd7cf7e5c94d641344fe1d9028c347893c8fb7d4dddf08c45f4b4f0a139c4a"
RESEARCH_ROOT = Path("/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-global-completion-axis-v1")
ORIGINAL_ROLES = {"supplied_original_file"}
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
# These exclusions concern NEW selected research only. Every supplied file,
# including embedded archives, is preserved without a suffix/content filter.
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


def source_outputs(manifest_raw, read, *, expected_manifest_sha256=ORIGINAL_MANIFEST_SHA256):
    """Preserve every listed input byte without extraction or scientific execution."""
    need(digest(manifest_raw) == expected_manifest_sha256, "Original intake manifest changed")
    original = json.loads(manifest_raw)
    need(original.get("schema") == "astra.source-intake.v1" and original.get("initial_main") == INITIAL_MAIN,
         "Original acquisition schema/pin changed")
    originals = original.get("files")
    need(isinstance(originals, list) and len(originals) == original.get("total_files"), "Original file count mismatch")
    need(sum(x["bytes"] for x in originals) == original.get("total_bytes"), "Original byte total mismatch")
    need(len({x["group"] for x in originals}) == original.get("groups"), "Original group count mismatch")
    outputs = {PREFIX + "package/SOURCE_MANIFEST.json": manifest_raw}
    entries, seen = [], set()
    for item in originals:
        name = item["path"]
        local(Path("/FX-SOURCE-PATH-CHECK"), name)
        need(name.startswith("sources/") and name not in seen, "Duplicate/unsafe original source path")
        seen.add(name)
        raw = read(name)
        need(type(item["bytes"]) is int and len(raw) == item["bytes"] and digest(raw) == item["sha256"], "Original source bytes changed: " + name)
        target = PREFIX + "package/originals/" + name
        outputs[target] = raw
        entries.append({"path": target, "research_relative_path": name,
                        "original_absolute_path": item["source_path"], "group": item["group"],
                        "bytes": len(raw), "sha256": digest(raw), "provenance_role": "supplied_original_file",
                        "original_kind": "supplied_archive" if name.endswith(".zip") else "supplied_file",
                        "source_handling": item["source_handling"]})
    need(len({x["path"].casefold() for x in entries}) == len(entries), "Source destination case collision")
    wrapper = {"schema": "astra.fx-source-manifest.v1", "intake_id": INTAKE_ID, "initial_main": INITIAL_MAIN,
               "original_manifest": {"path": PREFIX + "package/SOURCE_MANIFEST.json", "sha256": expected_manifest_sha256},
               "source_count": len(entries), "original_count": len(entries), "group_count": original["groups"],
               "archive_count": sum(x["original_kind"] == "supplied_archive" for x in entries),
               "extracted_member_count": 0, "original_bytes": original["total_bytes"], "total_bytes": original["total_bytes"],
               "original_acquisition_scope": "Pinned R frozen input copies. Every source remains DATA; prompts and UI exports are not operative instructions.",
               "preservation_scope": "All listed bytes, including repeated inputs and embedded old archive, are preserved exactly. No archive member is promoted into new evidence. No source script executed and no scientific claim adjudicated.",
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
    folder = local(root, PREFIX + "package/originals")
    for path in folder.rglob("*"):
        need(not path.is_symlink(), "Source packet symlink is forbidden")
    observed = {str(p.relative_to(root)) for p in folder.rglob("*") if p.is_file()}
    expected = {x["path"] for x in wrapper["files"]}
    need(observed == expected, "Original source inventory changed")
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
    need(path.startswith(PREFIX + "package/derived/"), "Selected research must be separate from supplied originals")
    local(Path("/FX-DERIVED-PATH-CHECK"), path)
    need(Path(path).suffix.lower() in TEXT_SUFFIXES and Path(path).suffix.lower() not in BANNED_SUFFIXES,
         "Selected research must be a permitted text artifact; acquired fulltexts/binary datasets stay outside the intake")
    need(item.get("provenance_role") in PROVENANCE_ROLES - ORIGINAL_ROLES, "Invalid derived provenance role")
    need(item.get("payload_kind") in PAYLOAD_KINDS, "Derived payload needs an explicit permitted kind")
    need(item.get("contains_external_fulltext") is False and item.get("contains_external_dataset_or_clone") is False,
         "Root must explicitly classify external fulltexts and complete third party datasets/clones")
    if item["provenance_role"] == "acquired_primary_literature_receipt":
        need(item["payload_kind"] in {"receipt", "acquisition_pointer"}, "Acquired literature preserves receipts/pointers only")
    need(isinstance(item.get("sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", item["sha256"]), "Derived file needs full SHA-256")
    need(type(item.get("bytes")) is int and item["bytes"] >= 0, "Derived file needs exact byte count")
    need(isinstance(item.get("selection_reason"), str) and item["selection_reason"].strip()
         and not item["selection_reason"].startswith("REPLACE_"), "Root selection reason is required")


def selection_records(selection, *, research_root=RESEARCH_ROOT, check_research=False):
    need(selection.get("schema") == "astra.fx-selected-freeze.v1", "Unsupported root selection schema")
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
