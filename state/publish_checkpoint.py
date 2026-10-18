#!/usr/bin/env python3
"""Publish immutable branch handoffs and rebuild small static views; Python stdlib."""
import argparse
import contextlib
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCHEMA = "astra-branch-checkpoint/1"
ROOT = Path(__file__).resolve().parents[1]
BRANCHES = {
    "theoretical-pro": "Foundational mathematics and theoretical questions",
    "natural-sciences-pro": "New principles of nature and decisive scientific evidence",
    "ultra": "Transformative invention and complementary research coordination",
    "primitive-genesis": "New mathematical objects, operations and theoretical frameworks",
}
SLUG = re.compile(r"[a-z0-9][a-z0-9-]{0,79}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
REVISION = re.compile(r"[0-9a-f]{40}\Z")
HISTORY_PATH = "state/CHECKPOINT_HISTORY_EXCEPTIONS.json"
HISTORY_BASELINE = "b862002a3bf216aa583f49d897bdb1d80c3ac508"
HISTORY_SHA256 = "172e3fd3da2f1534b695bf769e973ec2b7eee2ceeb3ed3711ecd75e7d68c74a3"


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def digest(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def canonical(record):
    return json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


class Records(dict):
    """Usual branch/ID mapping, with validation scope kept outside record bytes."""
    def __init__(self, *, evidence_checked=True):
        super().__init__()
        self.history_exceptions = {}
        self.evidence_checked = evidence_checked


def history_inventory(root):
    path = root / HISTORY_PATH
    if not path.exists():
        return {}
    require(digest(path) == HISTORY_SHA256, "historical exception inventory changed; review its exact pins")
    inventory = json.loads(path.read_text(encoding="utf-8"))
    require(inventory.get("schema") == "astra-checkpoint-history-exceptions/1" and
            inventory.get("baseline_revision") == HISTORY_BASELINE, "unsupported historical exception inventory")
    entries = {}
    for entry in inventory["records"]:
        path = entry["checkpoint_path"]
        require(path not in entries, "duplicate historical exception path")
        require(entry["kind"] == "schema-less-navigation",
                "unknown historical exception kind")
        # Check the reviewed baseline as well as current bytes. Changing an inventory
        # pin cannot retrospectively authorize a changed historical checkpoint.
        original = subprocess.check_output(["git", "-C", str(root), "show", f"{HISTORY_BASELINE}:{path}"], stderr=subprocess.PIPE)
        require(hashlib.sha256(original).hexdigest() == entry["checkpoint_sha256"],
                f"historical baseline pin mismatch: {path}")
        require((root / path).is_file() and digest(root / path) == entry["checkpoint_sha256"],
                f"pinned historical checkpoint changed or absent: {path}")
        entries[path] = entry
    return entries


def validate_evidence_refs(refs, root):
    """Apply the same complete evidence checks to supported and legacy records."""
    require(isinstance(refs, list), "evidence_refs must be a list")
    identifiers = set()
    for ref in refs:
        require(isinstance(ref, dict), "evidence reference must be an object")
        ref_id = ref.get("id")
        require(isinstance(ref_id, str) and ref_id and ref_id not in identifiers, "missing/duplicate evidence id")
        identifiers.add(ref_id)
        path = ref.get("path")
        require(isinstance(path, str) and path and not Path(path).is_absolute(), "evidence path must be repository relative")
        target = (root / path).resolve()
        require(target.is_relative_to(root.resolve()) and target.is_file(), f"missing/unsafe evidence path: {path}")
        require(".git" not in Path(path).parts and not target.is_relative_to((root / ".git").resolve()),
                "Git metadata is not publication evidence")
        expected = ref.get("sha256")
        require(isinstance(expected, str) and DIGEST.fullmatch(expected), f"missing evidence SHA-256: {path}")
        require(digest(target) == expected, f"evidence hash mismatch: {path}")
        lines = ref.get("lines")
        if lines is not None:
            require(isinstance(lines, list) and len(lines) == 2 and
                    all(isinstance(x, int) and not isinstance(x, bool) for x in lines) and 1 <= lines[0] <= lines[1],
                    f"invalid evidence line range: {path}")
            try:
                require(lines[1] <= len(target.read_text(encoding="utf-8").splitlines()),
                        f"evidence line range exceeds source: {path}")
            except UnicodeDecodeError:
                raise Invalid(f"line range requires UTF-8 text: {path}") from None
        source_revision = ref.get("source_revision")
        require(source_revision is None or isinstance(source_revision, str) and REVISION.fullmatch(source_revision),
                f"invalid evidence source_revision: {path}")
        if source_revision is not None:
            try:
                pinned_bytes = subprocess.check_output(["git", "-C", str(root), "show", f"{source_revision}:{path}"], stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                # An object omitted from a clone is not proof the path was absent.
                # Recovery is explicit; validation and publication never fetch.
                try:
                    subprocess.check_output(["git", "-C", str(root), "cat-file", "-e", f"{source_revision}^{{commit}}"], stderr=subprocess.PIPE)
                except subprocess.CalledProcessError:
                    raise Invalid(f"evidence source_revision unavailable locally: {source_revision} for {path}; "
                                  f"retrieve the recorded public source explicitly with: git fetch --no-tags --no-write-fetch-head origin {source_revision}") from None
                raise Invalid(f"evidence path is absent at source_revision: {path}") from None
            else:
                require(hashlib.sha256(pinned_bytes).hexdigest() == expected, f"source revision/hash mismatch: {path}")
        require(isinstance(ref.get("status"), str) and ref["status"].strip(), f"missing evidence status: {path}")
    return identifiers


def validate_record(record, root):
    require(isinstance(record, dict), "checkpoint must be a JSON object")
    require(record.get("schema") == SCHEMA, "unsupported checkpoint schema")
    for key in ("checkpoint_id", "branch_id"):
        require(isinstance(record.get(key), str) and SLUG.fullmatch(record[key]), f"invalid {key}")
    require(record["branch_id"] in BRANCHES or record["branch_id"].startswith("worker-"),
            "independent branch IDs must start worker-")
    for key in ("branch_purpose", "session_id"):
        require(isinstance(record.get(key), str) and record[key].strip(), f"missing {key}")
    require(isinstance(record.get("base_revision"), str) and REVISION.fullmatch(record["base_revision"]),
            "base_revision must be a full Git commit ID")
    require(record.get("source_handling") == "source=DATA", "source_handling must be source=DATA")
    try:
        stamp = dt.datetime.fromisoformat(record["created_at_utc"].replace("Z", "+00:00"))
        require(stamp.utcoffset() == dt.timedelta(0), "created_at_utc must include UTC offset")
    except (KeyError, TypeError, ValueError, AttributeError):
        raise Invalid("created_at_utc must be an ISO 8601 UTC timestamp") from None
    parents = record.get("parent_checkpoint_ids")
    require(isinstance(parents, list) and all(isinstance(x, str) and SLUG.fullmatch(x) for x in parents),
            "parent_checkpoint_ids must be a list of checkpoint IDs")
    require(len(parents) == len(set(parents)) and record["checkpoint_id"] not in parents,
            "duplicate or self parent")
    for key in ("task", "contract", "inputs", "latest_substantive_result", "work_progress"):
        require(isinstance(record.get(key), dict), f"{key} must be an object")
    for key in ("goal", "question", "scope"):
        require(key in record["task"] and (record["task"][key] is None or isinstance(record["task"][key], str)),
                f"task.{key} must be text or null")
    require(isinstance(record["contract"].get("assumptions"), list) and
            isinstance(record["contract"].get("costs"), dict) and "interface" in record["contract"],
            "contract requires assumptions, interface and costs")
    require(all(isinstance(record["inputs"].get(key), list) for key in ("inherited_or_supplied", "acquired")),
            "inputs requires inherited_or_supplied and acquired lists")
    for key in ("current_objective", "strongest_obstacle", "next_decisive_step", "status_note"):
        require(key in record and (record[key] is None or isinstance(record[key], str)), f"invalid {key}")
    for key in ("failed_attempts", "mechanisms_under_investigation", "cross_branch_updates", "unresolved_or_UNKNOWN"):
        require(isinstance(record.get(key), list), f"{key} must be a list")
    progress = record["work_progress"]
    require(progress.get("status") in ("read", "reconstructed", "reviewed", "UNKNOWN"),
            "work_progress.status is exposure/progress, never scientific certification")
    require(isinstance(progress.get("note"), str) and progress["note"].strip(), "work_progress.note is required")
    identifiers = validate_evidence_refs(record.get("evidence_refs"), root)
    result = record["latest_substantive_result"]
    summary = result.get("summary")
    require(summary is None or isinstance(summary, str), "result summary must be text or null")
    linked = result.get("evidence_ref_ids")
    require(isinstance(linked, list) and all(x in identifiers for x in linked), "unresolved result evidence references")
    if summary:
        require(linked and isinstance(result.get("scientific_status"), str) and result["scientific_status"].strip(),
                "a reported result requires evidence and separate scientific_status")
    for failure in record["failed_attempts"]:
        require(isinstance(failure, dict) and all(isinstance(failure.get(key), str) and failure[key].strip()
                for key in ("attempt", "failure_scope")), "failed attempt requires attempt and exact failure_scope")
        require(isinstance(failure.get("evidence_ref_ids"), list) and failure["evidence_ref_ids"] and
                all(x in identifiers for x in failure["evidence_ref_ids"]), "failed attempt requires linked evidence")
    for update in record["cross_branch_updates"]:
        require(isinstance(update, dict) and isinstance(update.get("checkpoint_path"), str) and
                update["checkpoint_path"].startswith("state/checkpoints/"), "cross-branch update needs checkpoint_path")
        target = (root / update["checkpoint_path"]).resolve()
        require(target.is_relative_to((root / "state/checkpoints").resolve()) and target.suffix == ".json" and target.is_file(),
                "cross-branch checkpoint is absent or unsafe")
    require(record["current_objective"] or summary or record["next_decisive_step"], "checkpoint must record substantive state")
    if "publication" in record:
        # The compact extension is optional for historical/manual records, but
        # every entry point must enforce it when present (including raw publish).
        try:
            if __package__:
                from .publish_result import validate_publication
            else:
                from publish_result import validate_publication
            validate_publication(record)
        except (ValueError, KeyError, TypeError) as error:
            raise Invalid(str(error)) from None


def legacy_projection(record):
    """Navigation only: do not supply a schema, parent IDs or proof links."""
    projection = dict(record)
    projection["parent_checkpoint_ids"] = None  # UNKNOWN, not an inferred root.
    projection["latest_substantive_result"] = {
        "summary": record["latest_substantive_result"],
        "scientific_status": record.get("scientific_status"),
        "evidence_ref_ids": None,  # The original did not supply these links.
    }
    return projection


def checkpoint_paths(root):
    """Reject hidden history outside the documented immutable tree layout."""
    base = root / "state/checkpoints"
    if not base.exists():
        return []
    require(base.is_dir() and not base.is_symlink(), "unsafe checkpoint directory")
    paths = []
    for path in sorted(base.rglob("*")):
        relative = path.relative_to(base)
        parts = relative.parts
        require(not path.is_symlink(), f"unsafe checkpoint symlink: {relative}")
        if path.is_dir():
            require(len(parts) == 1 and SLUG.fullmatch(parts[0]), f"unexpected checkpoint directory: {relative}")
        elif parts == ("README.txt",):
            continue
        elif len(parts) == 2 and SLUG.fullmatch(parts[0]) and re.fullmatch(r"\.checkpoint-[a-zA-Z0-9_-]+", parts[1]):
            # immutable_write may leave its private temporary file after a crash;
            # it is never a published record and never enters heads or views.
            continue
        else:
            require(len(parts) == 2 and SLUG.fullmatch(parts[0]) and path.suffix == ".json" and SLUG.fullmatch(path.stem),
                    f"unexpected checkpoint file: {relative}")
            paths.append(path)
    return paths


def load_records(root, check_evidence=True):
    records = Records(evidence_checked=check_evidence)
    inventory = history_inventory(root)
    for path in checkpoint_paths(root):
        record = json.loads(path.read_text(encoding="utf-8"))
        relative = path.relative_to(root).as_posix()
        exception = inventory.get(relative)
        require(isinstance(record, dict), f"checkpoint must be a JSON object: {relative}")
        if exception and exception["kind"] == "schema-less-navigation":
            require("schema" not in record and "parent_checkpoint_ids" not in record,
                    f"legacy shape changed: {relative}")
            if check_evidence:
                validate_evidence_refs(record.get("evidence_refs"), root)
            record = legacy_projection(record)
        else:
            require(record.get("schema") == SCHEMA, f"unsupported checkpoint schema: {relative}")
            if check_evidence:
                validate_record(record, root)
        if exception:
            records.history_exceptions[relative] = exception
        branch, checkpoint = record["branch_id"], record["checkpoint_id"]
        require(path.parent.name == branch and path.stem == checkpoint, f"checkpoint path/ID mismatch: {path}")
        records.setdefault(branch, {})
        require(checkpoint not in records[branch], "duplicate checkpoint ID in branch")
        records[branch][checkpoint] = record
    for branch, items in records.items():
        for checkpoint, record in items.items():
            require(all(parent in items for parent in record["parent_checkpoint_ids"] or ()), f"missing parent in {branch}/{checkpoint}")
        visiting, visited = set(), set()
        def visit(checkpoint):
            require(checkpoint not in visiting, f"checkpoint cycle in {branch}")
            if checkpoint in visited:
                return
            visiting.add(checkpoint)
            for parent in items[checkpoint]["parent_checkpoint_ids"] or ():
                visit(parent)
            visiting.remove(checkpoint)
            visited.add(checkpoint)
        for checkpoint in items:
            visit(checkpoint)
    return records


def heads(items):
    # Legacy records have no *known* incoming ancestry. They remain navigable
    # tips until a later compliant record explicitly names them as a parent.
    parents = {parent for record in items.values() for parent in record["parent_checkpoint_ids"] or ()}
    return sorted(set(items) - parents)


def history_audit(records):
    exceptions = getattr(records, "history_exceptions", {})
    legacy = sum(entry["kind"] == "schema-less-navigation" for entry in exceptions.values())
    total = sum(len(items) for items in records.values())
    evidence_checked = getattr(records, "evidence_checked", False)
    evidence_scope = ("All supplied evidence paths, hashes, ranges and source revisions are checked." if evidence_checked else
                      "Evidence checking was disabled; this load does not validate evidence.")
    return {"schema": "astra-checkpoint-history-audit/1", "inventory_path": HISTORY_PATH,
            "inventory_baseline_revision": HISTORY_BASELINE,
            "current_evidence_checked": evidence_checked,
            "counts": {"records": total, "schema_v1": total - legacy, "legacy_navigation_only": legacy},
            "scope": f"Publication integrity only. {evidence_scope} Pinned legacy records are not schema-compliant handoffs; absent schema and ancestry remain UNKNOWN.",
            "inherited_exceptions": [exceptions[path] for path in sorted(exceptions)]}


def views(root, records):
    output = {}
    rows = ["branch_id\tpurpose\tstate\thead_checkpoint_ids\tview_path"]
    for branch in sorted(set(BRANCHES) | set(records)):
        items = records.get(branch, {})
        tips = heads(items)
        purpose = BRANCHES.get(branch, items[tips[0]]["branch_purpose"] if tips else "UNKNOWN")
        status = ("UNPUBLISHED" if not tips else "CONFLICT" if len(tips) > 1 else
                  "LEGACY" if items[tips[0]].get("schema") != SCHEMA else "PUBLISHED")
        view_path = f"state/branches/{branch}.txt"
        rows.append("\t".join([branch, purpose.replace("\t", " ").replace("\n", " "), status, ",".join(tips), view_path]))
        text = [f"ASTRA BRANCH | {branch} | {status}", purpose,
                "Derived navigation; checkpoint evidence and scoped current claim notices govern mathematical reuse.",
                "current_activity: UNKNOWN; publication records a handoff only; no timestamp or recorded head establishes scientific authority."]
        inherited = [entry for path, entry in getattr(records, "history_exceptions", {}).items()
                     if Path(path).parent.name == branch]
        for entry in inherited:
            text.append(f"historical_exception: {entry['checkpoint_path']} | {entry['kind']} | {entry['limitations']}")
        if inherited:
            text.append(f"Exact pinned exception inventory: {HISTORY_PATH}; audit: python3 state/publish_checkpoint.py audit")
        if not tips:
            text.append("No shared checkpoint published. Historical records do not establish this branch's current objective.")
        if len(tips) > 1:
            text.append("Concurrent heads preserved. Read relevant heads; reconcile explicitly using every expected parent. No timestamp winner.")
        for checkpoint in tips:
            record = items[checkpoint]
            path = f"state/checkpoints/{branch}/{checkpoint}.json"
            legacy = record.get("schema") != SCHEMA
            text += ["", f"{'LEGACY RECEIPT' if legacy else 'CHECKPOINT'} {checkpoint}", f"record: {path}", f"record_sha256: {digest(root / path)}",
                     f"base_revision: {record['base_revision']}", f"created_at_utc: {record['created_at_utc']}"]
            if legacy:
                text.append("validation_scope: READ_ONLY legacy navigation; original schema and ancestry UNKNOWN; not a schema-compliant handoff.")
                text.append("parent_checkpoint_ids: UNKNOWN (absent in original; no parent IDs inferred)")
            for label, value in [("latest_substantive_result", record["latest_substantive_result"]["summary"]),
                                 ("scientific_status", record["latest_substantive_result"].get("scientific_status")),
                                 ("current_objective", record["current_objective"]),
                                 ("strongest_obstacle", record["strongest_obstacle"]),
                                 ("next_decisive_step", record["next_decisive_step"])]:
                text.append(f"{label}: {value if value is not None else 'UNKNOWN'}")
            text.append(f"progress: {record['work_progress']['status']}; {record['work_progress']['note']}")
            for failure in record["failed_attempts"]:
                text.append(f"failed_attempt: {failure['attempt']} | scope: {failure['failure_scope']}")
            for ref in record["evidence_refs"]:
                text.append(f"evidence: {ref['id']} | {ref['path']} | sha256={ref['sha256']} | status={ref['status']}")
            text.append("Open the preserved original for supplied fields and limitations." if legacy else
                        "Exact contract, costs, acquired inputs, mechanisms and cross-branch links: open checkpoint record when relevant.")
        if items:
            text += ["", "RECORDED HISTORY | navigation only; sequence does not imply scientific supersession or current activity."]
            for checkpoint, record in sorted(items.items()):
                kind = record.get("publication", {}).get("kind", "checkpoint" if record.get("schema") == SCHEMA else "legacy-receipt")
                text.append(f"history: {checkpoint} | {record['created_at_utc']} | {kind} | state/checkpoints/{branch}/{checkpoint}.json")
        output[view_path] = "\n".join(text) + "\n"
    output["state/branches.tsv"] = "\n".join(rows) + "\n"
    return output


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        temp = Path(handle.name)
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def immutable_write(path, content):
    """Expose a complete flushed record atomically without replacing any old path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, prefix=".checkpoint-", delete=False) as handle:
            temp = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temp, path)  # Atomic, same filesystem, and fails if path already exists.
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)


@contextlib.contextmanager
def locked(root):
    # The lock is transient repository-local coordination, never scientific state.
    import fcntl
    git_dir = Path(git(root, "rev-parse", "--absolute-git-dir"))
    with (git_dir / "astra-checkpoint.lock").open("a+") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def rebuild(root, records):
    for path, content in views(root, records).items():
        atomic_write(root / path, content)


def check_tracked_immutability(root, baseline="HEAD"):
    changes = git(root, "diff", "--name-status", baseline, "--", ":(glob)state/checkpoints/*/*.json")
    for line in changes.splitlines():
        require(line.startswith("A\t"), "tracked checkpoint modified/deleted: preserve its bytes and append a new record")


def publish(root, record, base_revision, expected_parents):
    require(base_revision == git(root, "rev-parse", "HEAD"), "stale base revision: refresh checked-out HEAD before publication")
    require(record.get("base_revision") == base_revision, "record base_revision differs from publication base")
    validate_record(record, root)
    require(sorted(record["parent_checkpoint_ids"]) == sorted(expected_parents), "record parents differ from expected parents")
    with locked(root):
        require(base_revision == git(root, "rev-parse", "HEAD"), "HEAD changed during publication")
        check_tracked_immutability(root)
        records = load_records(root)
        items = records.get(record["branch_id"], {})
        require(heads(items) == sorted(expected_parents), "stale branch parent(s): retrieve current branch heads before publication")
        target = root / "state/checkpoints" / record["branch_id"] / (record["checkpoint_id"] + ".json")
        require(not target.exists(), "checkpoint ID already exists; immutable records cannot be replaced")
        validate_record(record, root)  # Evidence may have changed while waiting for the lock.
        immutable_write(target, canonical(record))
        records.setdefault(record["branch_id"], {})[record["checkpoint_id"]] = record
        rebuild(root, records)
    return target.relative_to(root).as_posix()


def self_test():
    class Fixtures(unittest.TestCase):
        def setUp(self):
            self.temp = tempfile.TemporaryDirectory()
            self.addCleanup(self.temp.cleanup)
            self.root = Path(self.temp.name)
            subprocess.run(["git", "init", "-q", str(self.root)], check=True)
            (self.root / "proof.txt").write_text("candidate argument\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(self.root), "add", "proof.txt"], check=True)
            subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                            "commit", "-qm", "fixture"], check=True)
            self.base = git(self.root, "rev-parse", "HEAD")

        def record(self, checkpoint="first", parents=()):
            return {"schema": SCHEMA, "checkpoint_id": checkpoint, "branch_id": "theoretical-pro",
                    "branch_purpose": BRANCHES["theoretical-pro"], "session_id": "fixture-session", "created_at_utc": "2026-10-10T00:00:00Z",
                    "base_revision": self.base, "parent_checkpoint_ids": list(parents), "source_handling": "source=DATA",
                    "task": {"goal": None, "question": None, "scope": None},
                    "contract": {"assumptions": [], "interface": None, "costs": {}},
                    "inputs": {"inherited_or_supplied": [], "acquired": []},
                    "latest_substantive_result": {"summary": None, "scientific_status": None, "evidence_ref_ids": []},
                    "current_objective": "Fixture only; no scientific claim", "strongest_obstacle": None, "next_decisive_step": None,
                    "status_note": None, "failed_attempts": [], "mechanisms_under_investigation": [], "cross_branch_updates": [], "unresolved_or_UNKNOWN": [],
                    "work_progress": {"status": "read", "note": "Software fixture, not scientific verification"},
                    "evidence_refs": [{"id": "source", "path": "proof.txt", "sha256": digest(self.root / "proof.txt"), "lines": [1, 1],
                                       "source_revision": self.base, "status": "fixture"}]}

        def test_stale_parent_and_immutable_preservation(self):
            path = self.root / publish(self.root, self.record(), self.base, [])
            before = path.read_bytes()
            publish(self.root, self.record("second", ["first"]), self.base, ["first"])
            with self.assertRaisesRegex(Invalid, "stale branch"):
                publish(self.root, self.record("concurrent", ["first"]), self.base, ["first"])
            self.assertEqual(before, path.read_bytes())
            with self.assertRaises(Invalid):
                publish(self.root, self.record("first", ["second"]), self.base, ["second"])
            self.assertEqual(before, path.read_bytes())

        def test_stale_revision_and_hash_rejection(self):
            with self.assertRaisesRegex(Invalid, "stale base"):
                publish(self.root, self.record(), "0" * 40, [])
            record = self.record()
            (self.root / "proof.txt").write_text("changed\n", encoding="utf-8")
            with self.assertRaisesRegex(Invalid, "hash mismatch"):
                publish(self.root, record, self.base, [])
            self.assertFalse((self.root / "state/checkpoints/theoretical-pro/first.json").exists())

        def test_fork_retention_and_explicit_reconciliation(self):
            publish(self.root, self.record(), self.base, [])
            publish(self.root, self.record("left", ["first"]), self.base, ["first"])
            right = self.record("right", ["first"])
            # Simulate two valid independently published commits meeting in a Git merge.
            target = self.root / "state/checkpoints/theoretical-pro/right.json"
            target.write_text(canonical(right), encoding="utf-8")
            records = load_records(self.root)
            expected = views(self.root, records)
            self.assertIn("CONFLICT", expected["state/branches/theoretical-pro.txt"])
            self.assertEqual(heads(records["theoretical-pro"]), ["left", "right"])
            publish(self.root, self.record("reconciled", ["left", "right"]), self.base, ["left", "right"])
            self.assertEqual(heads(load_records(self.root)["theoretical-pro"]), ["reconciled"])
            self.assertEqual(target.read_text(), canonical(right))

        def test_rebuild_reproducibility_and_invalid_range(self):
            record = self.record()
            record["evidence_refs"][0]["lines"] = [1, 2]
            with self.assertRaisesRegex(Invalid, "exceeds source"):
                publish(self.root, record, self.base, [])
            publish(self.root, self.record(), self.base, [])
            records = load_records(self.root)
            first = views(self.root, records)
            rebuild(self.root, records)
            self.assertEqual(first, views(self.root, records))
            for path, content in first.items():
                self.assertEqual((self.root / path).read_text(), content)

        def test_source_revision_and_tracked_mutation_rejection(self):
            record = self.record()
            record["evidence_refs"][0]["source_revision"] = "0" * 40
            with self.assertRaisesRegex(Invalid, "source_revision unavailable locally"):
                publish(self.root, record, self.base, [])
            path = self.root / publish(self.root, self.record(), self.base, [])
            subprocess.run(["git", "-C", str(self.root), "add", "state"], check=True)
            subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                            "commit", "-qm", "published fixture"], check=True)
            self.base = git(self.root, "rev-parse", "HEAD")
            immutable_base = self.base
            edited = json.loads(path.read_text())
            edited["current_objective"] = "silently changed"
            path.write_text(canonical(edited), encoding="utf-8")
            with self.assertRaisesRegex(Invalid, "tracked checkpoint modified"):
                publish(self.root, self.record("second", ["first"]), self.base, ["first"])
            subprocess.run(["git", "-C", str(self.root), "add", "state/checkpoints"], check=True)
            subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                            "commit", "-qm", "fixture forbidden mutation"], check=True)
            with self.assertRaisesRegex(Invalid, "tracked checkpoint modified"):
                check_tracked_immutability(self.root, immutable_base)

        def test_failed_write_never_exposes_partial_record(self):
            first = self.root / publish(self.root, self.record(), self.base, [])
            before = first.read_bytes()
            with mock.patch.object(os, "fsync", side_effect=OSError("injected write failure")):
                with self.assertRaisesRegex(OSError, "injected write failure"):
                    publish(self.root, self.record("second", ["first"]), self.base, ["first"])
            self.assertFalse((first.parent / "second.json").exists())
            self.assertEqual(first.read_bytes(), before)
            self.assertEqual(sorted(path.name for path in first.parent.iterdir()), ["first.json"])
            self.assertEqual(heads(load_records(self.root)["theoretical-pro"]), ["first"])

        def test_two_concurrent_publishers_accept_only_one_parent_update(self):
            first = self.root / publish(self.root, self.record(), self.base, [])
            before = first.read_bytes()
            worker = (
                "import importlib.util,json,pathlib,sys; "
                "s=importlib.util.spec_from_file_location('publisher',sys.argv[1]); "
                "m=importlib.util.module_from_spec(s); s.loader.exec_module(m); "
                "m.publish(pathlib.Path(sys.argv[2]),json.loads(sys.argv[3]),sys.argv[4],['first'])"
            )
            jobs = [subprocess.Popen([sys.executable, "-c", worker, str(Path(__file__).resolve()), str(self.root),
                                     canonical(self.record(name, ["first"])), self.base], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    for name in ("concurrent-left", "concurrent-right")]
            for job in jobs:
                job.communicate(timeout=15)
            self.assertEqual(sorted(job.returncode for job in jobs), [0, 1])
            self.assertEqual(len(heads(load_records(self.root)["theoretical-pro"])), 1)
            self.assertEqual(first.read_bytes(), before)
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(Fixtures))
    return 0 if result.wasSuccessful() else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    command = sub.add_parser("publish")
    command.add_argument("record", type=Path)
    command.add_argument("--base-revision", required=True)
    command.add_argument("--expected-parent", action="append", required=True, help="repeat for merged heads; NONE for first checkpoint")
    sub.add_parser("rebuild")
    validate = sub.add_parser("validate")
    validate.add_argument("--immutable-base", help="full baseline commit; also reject committed edits/deletions of older checkpoint records")
    audit = sub.add_parser("audit", help="check records and report exact inherited limitations without rebuilding views")
    audit.add_argument("--immutable-base", help="also reject committed edits/deletions since this full baseline commit")
    sub.add_parser("self-test")
    args = parser.parse_args()
    try:
        if args.command == "self-test":
            return self_test()
        if args.command == "publish":
            parents = [] if args.expected_parent == ["NONE"] else args.expected_parent
            print(publish(ROOT, json.loads(args.record.read_text(encoding="utf-8")), args.base_revision, parents))
        else:
            baseline = args.immutable_base if args.command in ("validate", "audit") and args.immutable_base else "HEAD"
            require(baseline == "HEAD" or REVISION.fullmatch(baseline), "immutable-base must be a full commit ID")
            check_tracked_immutability(ROOT, baseline)
            records = load_records(ROOT)
            if args.command == "rebuild":
                with locked(ROOT):
                    rebuild(ROOT, load_records(ROOT))
                print("Rebuilt branch registry and static branch views.")
            elif args.command == "audit":
                print(canonical(history_audit(records)), end="")
            else:
                for path, content in views(ROOT, records).items():
                    require((ROOT / path).is_file() and (ROOT / path).read_text(encoding="utf-8") == content, f"stale generated view: {path}")
                counts = history_audit(records)["counts"]
                print(f"Checked: {counts['schema_v1']} schema-v1 checkpoints; "
                      f"{counts['legacy_navigation_only']} pinned legacy navigation records. "
                      "Evidence paths, hashes, ranges, source revisions and generated views match. "
                      "Legacy records are not schema-compliant handoffs; original schema/ancestry remain UNKNOWN. "
                      "Run audit for the exact limitations.")
    except (Invalid, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
