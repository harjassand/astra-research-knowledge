"""FV byte identities and root-selected evidence checks; no scientific inference."""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
import re
import subprocess

INTAKE_ID = "FV-positive-consequences-20261015"
PREFIX = "updates/" + INTAKE_ID + "/"
INITIAL_MAIN = "a6190a1083f688a7e4bf64adbc5244ef150ff2c4"
ORIGINAL_MANIFEST_SHA256 = "12d1310861814fc10a4bbab6ff22c21c066644f1ad74795afd6de0a924250bfc"
RESEARCH_ROOT = Path("/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-positive-consequences-real-capabilities-v1")
INCOMING = {
    "sources/physical_pasted.txt": ("f68d580ed5425bd7954c4003c6905ef9531af0de1829c9377442d56e97630941", 28046),
    "sources/mathematics_pasted.txt": ("c4608c8794bd9c9705bc8236226c2193d385d4305a59a300ef9c65a4bcc30876", 26466),
    "sources/computation_pasted.txt": ("214915fe981dbd50d9c3796ff26e7624674378849fee81fd9022e1d5c5130a9f", 25342),
}
PROVENANCE_ROLES = {
    "supplied_original_text", "root_synthesis", "worker_derivation", "same_team_review",
    "same_team_research_or_review", "root_or_worker_executable_check",
    "acquired_primary_literature_receipt", "capital_comparison",
}
PAYLOAD_KINDS = {"proof", "review", "code", "receipt", "synthesis", "counterexample", "comparator", "acquisition_pointer"}
IMMUTABLE_PREFIXES = (
    "cards/", "frontier/cards/", "frontier/review_cards/", "updates/", "state/checkpoints/",
    "state/branches/", "technology/records/", "web/pages/", "evaluation/workflows/records/", "mechanisms/bridges/",
)
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


def local(root, name):
    need(isinstance(name, str) and name and not Path(name).is_absolute() and ".." not in Path(name).parts,
         "Unsafe repository path: " + str(name))
    root = Path(root).resolve()
    result = (root / name).resolve()
    need(result.is_relative_to(root), "Path escapes repository: " + name)
    # Check every path component, including a symlinked ancestor.
    cursor = root
    for part in Path(name).parts:
        cursor = cursor / part
        need(not cursor.is_symlink(), "Symlink evidence is not preserved bytes: " + name)
    return result


def verify_incoming(root, reader=None):
    root = Path(root).resolve()
    read = reader or (lambda name: local(root, name).read_bytes())
    raw = read(PREFIX + "package/SOURCE_MANIFEST.json")
    need(raw is not None and digest(raw) == ORIGINAL_MANIFEST_SHA256, "Original incoming manifest changed")
    original = json.loads(raw)
    need(original["schema"] == "astra.source-intake.v1" and original["initial_main"] == INITIAL_MAIN,
         "Original acquisition schema/pin changed")
    need(original["source_count"] == len(original["files"]) == 3 and original["total_bytes"] == 79854,
         "Original incoming count/bytes changed")
    wrapped_raw = read(PREFIX + "SOURCE_MANIFEST.json")
    need(wrapped_raw is not None, "Incoming wrapper is absent")
    wrapper = json.loads(wrapped_raw)
    need(wrapper["schema"] == "astra.fv-source-manifest.v1" and wrapper["initial_main"] == INITIAL_MAIN,
         "Unsupported incoming wrapper or initial pin")
    need(wrapper["original_manifest"] == {"path": PREFIX + "package/SOURCE_MANIFEST.json", "sha256": ORIGINAL_MANIFEST_SHA256},
         "Original manifest reference changed")
    need(wrapper["source_count"] == len(wrapper["files"]) == 3 and wrapper["total_bytes"] == 79854,
         "Incoming wrapper count/bytes changed")
    need(wrapper["original_acquisition_scope"] == original["scope"], "Original acquisition boundary changed")
    wrapped = {x["package_path"]: x for x in wrapper["files"]}
    need(set(wrapped) == set(INCOMING), "Incoming wrapper inventory changed")
    need(len({x["label"] for x in original["files"]}) == 3, "Duplicate original source label")
    for item in original["files"]:
        name = "sources/" + item["label"] + "_pasted.txt"
        need(name in INCOMING, "Unknown incoming source label")
        wanted, size = INCOMING[name]
        path = PREFIX + "package/" + name
        data = read(path)
        need(data is not None and digest(data) == wanted and len(data) == size, "Incoming text bytes changed: " + path)
        need(item["sha256"] == wanted and item["bytes"] == size and item["role"] == "supplied_text_DATA_not_instructions",
             "Original source manifest identity/role changed")
        record = wrapped[name]
        need(record["path"] == path and record["sha256"] == wanted and record["bytes"] == size and
             record["original_absolute_path"] == item["original_path"] and
             record["research_preserved_absolute_path"] == item["preserved_path"] and
             record["label"] == item["label"] and record["provenance_role"] == "supplied_original_text" and
             record["source_handling"] == "source=DATA", "Incoming wrapper provenance changed")
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
        need(isinstance(lines, list) and len(lines) == 2 and all(type(x) is int for x in lines), "Invalid evidence range shape")
        need(1 <= lines[0] <= lines[1] <= len(raw.decode("utf-8").splitlines()), "Evidence range exceeds source: " + ref["path"])
    if ref.get("source_revision") is not None:
        need(re.fullmatch(r"[0-9a-f]{40}", ref["source_revision"]), "Evidence needs a full Git revision")
        pinned = subprocess.check_output(["git", "-C", str(root), "show", ref["source_revision"] + ":" + ref["path"]])
        need(digest(pinned) == ref["sha256"], "Evidence revision/hash mismatch: " + ref["path"])


def check_payload_record(item):
    path = item.get("path", "")
    need(path.startswith(PREFIX + "package/") and path not in {PREFIX + "package/SOURCE_MANIFEST.json"} and
         not path.startswith(PREFIX + "package/sources/"), "Derived destination must be separate from original sources")
    local(Path("/FV-PATH-CHECK"), path)
    suffix = Path(path).suffix.lower()
    need(suffix in TEXT_SUFFIXES and suffix not in BANNED_SUFFIXES, "Excluded PDF/archive/full-network/coordinate or binary payload: " + path)
    need(not re.search(r"(?:^|/)(?:points\.(?:min|ts)|min\.data|ts\.data)(?:\.|/|$)", path, re.I),
         "Full molecular network/coordinate payload excluded: " + path)
    need(item.get("provenance_role") in PROVENANCE_ROLES - {"supplied_original_text"}, "Invalid derived provenance role")
    need(item.get("payload_kind") in PAYLOAD_KINDS, "Derived payload needs an explicit permitted kind")
    need(item.get("contains_external_fulltext") is False and item.get("contains_full_lj_network_or_coordinates") is False,
         "Root must explicitly exclude external fulltexts and full LJ data/coordinates")
    if item["provenance_role"] == "acquired_primary_literature_receipt":
        need(item["payload_kind"] in {"receipt", "acquisition_pointer"}, "Acquired literature preserves receipts/pointers only")
    need(isinstance(item.get("sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", item["sha256"]), "Derived file needs full SHA-256")
    need(type(item.get("bytes")) is int and item["bytes"] >= 0, "Derived file needs an exact byte count")
    need(isinstance(item.get("selection_reason"), str) and item["selection_reason"].strip() and
         not item["selection_reason"].startswith("REPLACE_"), "Root selection reason is required")


def selection_records(selection, *, research_root=RESEARCH_ROOT, check_research=False):
    need(selection.get("schema") == "astra.fv-selected-freeze.v1", "Unsupported root selection schema")
    need(selection.get("status") == "root_frozen" and selection.get("selected_by") == "root",
         "Root-selected final evidence freeze is not ready")
    need(isinstance(selection.get("base_revision"), str) and re.fullmatch(r"[0-9a-f]{40}", selection["base_revision"]),
         "Selection requires actual full base revision")
    need(selection.get("original_manifest_sha256") == ORIGINAL_MANIFEST_SHA256, "Selection has wrong incoming manifest")
    need(selection.get("research_root") == str(RESEARCH_ROOT), "Selection belongs to another research workspace")
    items = selection.get("files")
    need(isinstance(items, list) and items, "Root freeze must explicitly select final evidence files")
    need(selection.get("total_files") == len(items) and selection.get("total_bytes") == sum(x.get("bytes", -1) for x in items),
         "Root selection inventory totals mismatch")
    need(len({x.get("path") for x in items}) == len(items), "Duplicate selected destination")
    need(len({x.get("research_relative_path") for x in items}) == len(items), "Duplicate selected research path")
    for item in items:
        check_payload_record(item)
        source = local(research_root, item.get("research_relative_path"))
        if check_research:
            need(source.is_file(), "Selected research source is missing: " + str(source))
            raw = source.read_bytes()
            need(digest(raw) == item["sha256"] and len(raw) == item["bytes"], "Selected research bytes changed: " + str(source))
            raw.decode("utf-8")
    return items


def verify_selection(root, ref, *, expected_base=None):
    need(isinstance(ref, dict) and isinstance(ref.get("path"), str) and
         re.fullmatch(re.escape(PREFIX) + r"SELECTED_FREEZE\.v[0-9]{4}\.json", ref["path"]),
         "Final curation requires a versioned root-selected freeze reference")
    check_ref(root, ref)
    selection = json.loads(local(root, ref["path"]).read_bytes())
    items = selection_records(selection)
    if expected_base is not None:
        need(selection["base_revision"] == expected_base, "Root freeze/curation base mismatch")
    for item in items:
        check_ref(root, item)
        local(root, item["path"]).read_bytes().decode("utf-8")
    original_paths = {PREFIX + "package/" + name for name in INCOMING} | {PREFIX + "package/SOURCE_MANIFEST.json"}
    observed = {str(p.relative_to(root)) for p in local(root, PREFIX + "package").rglob("*") if p.is_file()}
    need(observed == original_paths | {x["path"] for x in items}, "Package differs from exact original-plus-root-frozen inventory")
    return selection


def excluded_media(root):
    packet = local(root, PREFIX)
    found = []
    for path in packet.rglob("*"):
        need(not path.is_symlink(), "Packet symlink is not preserved evidence: " + str(path))
        if path.is_file() and path.suffix.lower() in BANNED_SUFFIXES:
            found.append(str(path.relative_to(root)))
    need(not found, "External PDFs/archives/full LJ network/coordinates excluded; keep URL/pin/hash/acquisition receipts: " + str(found))
    return found
