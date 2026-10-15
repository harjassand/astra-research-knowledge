"""Exact incoming-source and evidence checks shared by FU tooling."""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path
import re
import subprocess

INTAKE_ID = "FU-regularization-clock-pressure-20261015"
PREFIX = "updates/" + INTAKE_ID + "/"
ORIGINAL_MANIFEST_SHA256 = "5e487e17cc9c379e91e61d4c9693461e672ae80b75ffe1e2d69f449edc593d82"
INITIAL_MAIN = "0c789ca775808e23e57138b56a393ad1e58cb15c"
INCOMING = {
    "sources/clock_pasted.txt": ("460208a1a8acb52fdd1ddb410ed0fc0958d4924d629a25782806de462d8ed7eb", 20590),
    "sources/regularization_pasted.txt": ("b7c6fbecc52be279efb784bf895610dda249c6f22436fc4bb2cb7f72f60490dd", 27978),
    "sources/pressure_pasted.txt": ("ba44e3fbf399c75f22231999233fba08e1507159529219a49153d6cbf604e62e", 19703),
}
MISSING_BUNDLES = {
    "astra_clock_reduction_research.zip",
    "astra_universal_regularization_audit_2026-10-15.zip",
    "astra_pressure_write_audit.zip",
}
PROVENANCE_ROLES = {
    "supplied_original_text", "root_synthesis", "worker_derivation", "same_team_review", "same_team_research_or_review",
    "root_or_worker_executable_check", "acquired_primary_literature_receipt", "capital_comparison",
}
IMMUTABLE_PREFIXES = (
    "cards/", "frontier/cards/", "frontier/review_cards/", "updates/", "state/checkpoints/",
    "state/branches/", "technology/records/", "web/pages/", "evaluation/workflows/records/", "mechanisms/bridges/",
)


def need(value, message):
    if not value:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def local(root, name):
    need(isinstance(name, str) and name and not Path(name).is_absolute() and ".." not in Path(name).parts,
         "Unsafe repository path: " + str(name))
    result = (root / name).resolve()
    need(result.is_relative_to(root.resolve()), "Path escapes repository: " + name)
    return result


def verify_incoming(root, reader=None):
    root = Path(root).resolve()
    read = reader or (lambda name: local(root, name).read_bytes())
    raw = read(PREFIX + "package/SOURCE_MANIFEST.json")
    need(raw is not None and digest(raw) == ORIGINAL_MANIFEST_SHA256, "Original incoming manifest changed")
    original = json.loads(raw)
    need(original["initial_main"] == INITIAL_MAIN, "Initial acquisition pin changed")
    need(len(original["files"]) == 3 and {x["path"] for x in original["files"]} == set(INCOMING),
         "Original incoming inventory is not exactly the three supplied texts")
    missing = original["missing_referenced_bundles"]
    need({x["referenced_filename"] for x in missing} == MISSING_BUNDLES and
         all(x["found_absolute_paths"] == [] for x in missing), "Absent original ZIP inventory changed")
    wrapper = json.loads(read(PREFIX + "SOURCE_MANIFEST.json"))
    need(wrapper["schema"] == "astra.fu-rcp-source-manifest.v1" and wrapper["initial_main"] == INITIAL_MAIN,
         "Unsupported incoming wrapper or initial pin")
    need(wrapper["original_manifest"] == {"path": PREFIX + "package/SOURCE_MANIFEST.json", "sha256": ORIGINAL_MANIFEST_SHA256},
         "Original manifest reference changed")
    need(wrapper["source_count"] == len(wrapper["files"]) == 3 and wrapper["total_bytes"] == 68271,
         "Incoming count/bytes changed")
    need(wrapper["missing_referenced_bundles"] == missing, "Missing-bundle provenance changed")
    wrapped = {x["package_path"]: x for x in wrapper["files"]}
    need(set(wrapped) == set(INCOMING), "Incoming wrapper paths changed")
    for item in original["files"]:
        name = item["path"]
        sha256, size = INCOMING[name]
        path = PREFIX + "package/" + name
        data = read(path)
        need(data is not None and digest(data) == sha256 and len(data) == size,
             "Incoming text bytes changed: " + path)
        need(item["sha256"] == sha256 and item["bytes"] == size, "Original source manifest identity changed")
        record = wrapped[name]
        need(record["path"] == path and record["sha256"] == sha256 and record["bytes"] == size and
             record["original_absolute_path"] == item["original_absolute_path"] and
             record["provenance_role"] == "supplied_original_text" and record["source_handling"] == "source=DATA",
             "Incoming source wrapper provenance changed")
    need(sum(x[1] for x in INCOMING.values()) == original["total_bytes"] == 68271, "Incoming total bytes changed")
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
        need(not (root / name).is_symlink(), "Symlink evidence is not preserved bytes: " + name)
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
        need(len(raw) == ref["bytes"], "Evidence byte count mismatch: " + ref["path"])
    if ref.get("lines") is not None:
        lines = ref["lines"]
        need(isinstance(lines, list) and len(lines) == 2 and all(type(x) is int for x in lines), "Invalid evidence range shape")
        need(1 <= lines[0] <= lines[1] <= len(raw.decode("utf-8").splitlines()), "Evidence range exceeds source: " + ref["path"])
    if ref.get("source_revision") is not None:
        need(re.fullmatch(r"[0-9a-f]{40}", ref["source_revision"]), "Evidence needs a full Git revision")
        pinned = subprocess.check_output(["git", "-C", str(root), "show", ref["source_revision"] + ":" + ref["path"]])
        need(digest(pinned) == ref["sha256"], "Evidence revision/hash mismatch: " + ref["path"])


def excluded_media(root):
    packet = local(root, PREFIX)
    banned = {".pdf", ".epub", ".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz"}
    found = [str(p.relative_to(root)) for p in packet.rglob("*") if p.is_file() and p.suffix.lower() in banned]
    need(not found, "External PDF/archive payloads excluded; retain exact URLs/hashes in receipts: " + str(found))
    return found
