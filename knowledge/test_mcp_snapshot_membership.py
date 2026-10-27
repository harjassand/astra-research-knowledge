"""Requests must reject newly discovered intake before serving a frozen snapshot."""
import subprocess
import unittest
from unittest.mock import patch

from knowledge import test_knowledge as fixtures
from knowledge.build import inventory
from knowledge.mcp_adapter import ResearchAdapter
from knowledge.model import ROOT, encoded


class SnapshotMembershipTests(unittest.TestCase):
    write = fixtures.Fixture.write
    statuses = fixtures.Fixture.statuses
    unit = fixtures.Fixture.unit
    compile = fixtures.Fixture.compile

    def setUp(self):
        fixtures.Fixture.setUp(self)
        unit = self.unit()
        unit["statement"] = "A finite source statement. " * 1100
        self.write("knowledge/units/U1-fixture/v0001.json", encoded(unit))
        self.write("knowledge/mcp_adapter.py", (ROOT / "knowledge/mcp_adapter.py").read_bytes())
        self.compile()
        self.git("init", "-q")
        self.git("add", ".")
        self.commit()
        self.adapter = ResearchAdapter(self.root, page_bytes=1024)
        self.adapter.current()
        self.assertTrue(self.adapter.search("finite source")["results"])
        self.source_handle = self.adapter.register(self.source)
        self.continuation = self.adapter.fetch("U1-fixture")["metadata"]["next_id"]
        self.assertIsNotNone(self.continuation)

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root,
                                       stderr=subprocess.STDOUT, text=True)

    def commit(self, *args):
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "commit", "-qm", "fixture", *args)

    def assert_refuses_requests(self, message):
        requests = {
            "guard": self.adapter.current,
            "search": lambda: self.adapter.search("finite source"),
            "record": lambda: self.adapter.fetch("N1-fixture"),
            "source": lambda: self.adapter.fetch(self.source_handle),
            "continuation": lambda: self.adapter.fetch(self.continuation),
        }
        for name, request in requests.items():
            with self.subTest(request=name):
                with self.assertRaisesRegex(ValueError, message) as error:
                    request()
                self.assertNotIn(str(self.root), str(error.exception))

    def intake_value(self, kind):
        if kind == "review":
            name = "knowledge/reviews/new-review.json"
            value = {"id": "new-review", "decision": "open", "scope": "Inspect the independent-noise premise",
                     "subjects": [{"id": "N1-fixture", "content_version":
                                   self.adapter.library.resolve("N1-fixture")["content_version"]}],
                     "evidence": [self.source]}
        else:
            name = "agent/SEMANTIC_NOTICES.d/new-correction.jsonl"
            value = {"notice_id": "new-correction", "card_ids": ["N1-fixture"],
                     "clarification": "The finite premise assumes independent noise.",
                     "source_refs": [self.source]}
        return name, value

    def add_intake(self, kind, staged):
        name, value = self.intake_value(kind)
        self.write(name, encoded(value))
        if staged:
            self.git("add", name)
        # Reproduce the original gap without mocking Git or discovery: HEAD and
        # manifest are unchanged, and the new path was not in the frozen set.
        self.assertEqual(self.git("rev-parse", "HEAD").strip(), self.adapter.revision)
        self.assertEqual((self.root / "knowledge/current/manifest.json").read_bytes(),
                         self.adapter.manifest_bytes)
        self.assertNotIn(name, self.adapter.frozen_paths)
        self.assertNotEqual(inventory(self.root), self.adapter.library.manifest["discovery"])
        diff = self.git("diff", "--name-only", "HEAD").splitlines()
        self.assertEqual(name in diff, staged)
        self.assert_refuses_requests("discovery membership changed")

    def test_untracked_new_review_blocks_all_requests(self):
        self.add_intake("review", staged=False)

    def test_staged_new_review_blocks_all_requests(self):
        self.add_intake("review", staged=True)

    def test_untracked_new_correction_blocks_all_requests(self):
        self.add_intake("correction", staged=False)

    def test_staged_new_correction_blocks_all_requests(self):
        self.add_intake("correction", staged=True)

    def test_head_change_remains_a_separate_guard(self):
        self.commit("--allow-empty")
        self.assertEqual(inventory(self.root), self.adapter.library.manifest["discovery"])
        self.assertEqual((self.root / "knowledge/current/manifest.json").read_bytes(),
                         self.adapter.manifest_bytes)
        self.assert_refuses_requests("snapshot changed")

    def test_unrelated_untracked_notes_do_not_invalidate_the_snapshot(self):
        self.write("notes/private-draft.txt", b"Not an admitted intake source.\n")
        self.adapter.current()
        self.assertEqual(self.adapter.fetch("N1-fixture")["metadata"]["revision"], self.adapter.revision)

    def test_malformed_new_public_index_fails_closed(self):
        self.write("research/new/source/INDEX.json", b"not JSON\n")
        self.assert_refuses_requests("discovery cannot be validated")
        with patch("knowledge.mcp_adapter.inventory", side_effect=OSError(str(self.root))):
            self.assert_refuses_requests("discovery cannot be validated")

    def test_completed_intake_requires_restart_and_exposes_the_new_correction(self):
        from knowledge.test_mcp_adapter import complete

        self.add_intake("correction", staged=False)
        self.compile()
        self.git("add", ".")
        self.commit()
        self.assert_refuses_requests("snapshot changed")
        fresh = ResearchAdapter(self.root)
        packet = complete(fresh, "N1-fixture")
        self.assertEqual([n["notice_id"] for n in packet["notices"]], ["new-correction"])
        self.assertNotEqual(fresh.version, self.adapter.version)
        with self.assertRaisesRegex(ValueError, "stale snapshot handle"):
            fresh.fetch(self.source_handle)


if __name__ == "__main__":
    unittest.main()
