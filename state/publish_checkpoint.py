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
    refs = record.get("evidence_refs")
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
                raise Invalid(f"evidence path is absent at source_revision: {path}") from None
            require(hashlib.sha256(pinned_bytes).hexdigest() == expected, f"source revision/hash mismatch: {path}")
        require(isinstance(ref.get("status"), str) and ref["status"].strip(), f"missing evidence status: {path}")
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


def load_records(root, check_evidence=True):
    records = {}
    for path in sorted((root / "state/checkpoints").glob("*/*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if check_evidence:
            validate_record(record, root)
        branch, checkpoint = record["branch_id"], record["checkpoint_id"]
        require(path.parent.name == branch and path.stem == checkpoint, f"checkpoint path/ID mismatch: {path}")
        records.setdefault(branch, {})
        require(checkpoint not in records[branch], "duplicate checkpoint ID in branch")
        records[branch][checkpoint] = record
    for branch, items in records.items():
        for checkpoint, record in items.items():
            require(all(parent in items for parent in record["parent_checkpoint_ids"]), f"missing parent in {branch}/{checkpoint}")
        visiting, visited = set(), set()
        def visit(checkpoint):
            require(checkpoint not in visiting, f"checkpoint cycle in {branch}")
            if checkpoint in visited:
                return
            visiting.add(checkpoint)
            for parent in items[checkpoint]["parent_checkpoint_ids"]:
                visit(parent)
            visiting.remove(checkpoint)
            visited.add(checkpoint)
        for checkpoint in items:
            visit(checkpoint)
    return records


def heads(items):
    parents = {parent for record in items.values() for parent in record["parent_checkpoint_ids"]}
    return sorted(set(items) - parents)


def views(root, records):
    output = {}
    rows = ["branch_id\tpurpose\tstate\thead_checkpoint_ids\tview_path"]
    for branch in sorted(set(BRANCHES) | set(records)):
        items = records.get(branch, {})
        tips = heads(items)
        purpose = BRANCHES.get(branch, items[tips[0]]["branch_purpose"] if tips else "UNKNOWN")
        status = "UNPUBLISHED" if not tips else "CONFLICT" if len(tips) > 1 else "PUBLISHED"
        view_path = f"state/branches/{branch}.txt"
        rows.append("\t".join([branch, purpose.replace("\t", " ").replace("\n", " "), status, ",".join(tips), view_path]))
        text = [f"ASTRA BRANCH | {branch} | {status}", purpose,
                "Derived navigation; checkpoint evidence and scoped current claim notices govern mathematical reuse."]
        if not tips:
            text.append("No shared checkpoint published. Historical records do not establish this branch's current objective.")
        if len(tips) > 1:
            text.append("Concurrent heads preserved. Read relevant heads; reconcile explicitly using every expected parent. No timestamp winner.")
        for checkpoint in tips:
            record = items[checkpoint]
            path = f"state/checkpoints/{branch}/{checkpoint}.json"
            text += ["", f"CHECKPOINT {checkpoint}", f"record: {path}", f"record_sha256: {digest(root / path)}",
                     f"base_revision: {record['base_revision']}", f"created_at_utc: {record['created_at_utc']}"]
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
            text.append("Exact contract, costs, acquired inputs, mechanisms and cross-branch links: open checkpoint record when relevant.")
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
            with self.assertRaisesRegex(Invalid, "absent at source_revision"):
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
    sub.add_parser("self-test")
    args = parser.parse_args()
    try:
        if args.command == "self-test":
            return self_test()
        if args.command == "publish":
            parents = [] if args.expected_parent == ["NONE"] else args.expected_parent
            print(publish(ROOT, json.loads(args.record.read_text(encoding="utf-8")), args.base_revision, parents))
        else:
            baseline = args.immutable_base if args.command == "validate" and args.immutable_base else "HEAD"
            require(baseline == "HEAD" or REVISION.fullmatch(baseline), "immutable-base must be a full commit ID")
            check_tracked_immutability(ROOT, baseline)
            records = load_records(ROOT)
            if args.command == "rebuild":
                with locked(ROOT):
                    rebuild(ROOT, load_records(ROOT))
                print("Rebuilt branch registry and static branch views.")
            else:
                for path, content in views(ROOT, records).items():
                    require((ROOT / path).is_file() and (ROOT / path).read_text(encoding="utf-8") == content, f"stale generated view: {path}")
                print(f"Valid: {sum(len(items) for items in records.values())} immutable checkpoints; references and views consistent.")
    except (Invalid, OSError, json.JSONDecodeError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
