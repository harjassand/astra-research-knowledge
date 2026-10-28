"""Real ordinary intake, pinned pages, failures and sparse published snapshots."""
import copy
import json
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from knowledge.mcp_adapter import ResearchAdapter
from knowledge.model import digest, encoded
from knowledge.published import GitSnapshots, PublishedAdapter, RELEASE_SCHEMA, release_version, read_release
from knowledge import test_knowledge as fixtures


class Snapshots:
    def __init__(self, roots):
        self.roots, self.staged, self.saved = roots, [], []

    def stage(self, version, historical=False):
        self.staged.append((version, historical))
        return self.roots[version]

    def remember(self, adapter, owned=False):
        self.saved.append((adapter.version, owned))

    def prune(self, retained):
        pass


def complete(adapter, identifier):
    pages = []
    while identifier:
        result = adapter.fetch(identifier)
        pages.append(result)
        identifier = result["metadata"].get("next_id")
    return json.loads("".join(p["text"] for p in pages)), pages


class PublishedRefreshTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = fixtures.Fixture()
        cls.fixture.setUp()
        cls.root = cls.fixture.root
        cls.space = tempfile.TemporaryDirectory()
        cls.old = Path(cls.space.name) / "old"
        unit = cls.fixture.unit()
        unit["statement"] = "A finite source statement. " * 100
        cls.fixture.write("knowledge/units/U1-fixture/v0001.json", encoded(unit))
        cls.fixture.compile()
        cls.git(cls.root, "init", "-q")
        cls.git(cls.root, "add", ".")
        cls.commit()
        cls.git(cls.root, "worktree", "add", "--detach", str(cls.old), "HEAD")
        cls.a = ResearchAdapter(cls.old, page_bytes=1024)
        # Revised source, revised immutable unit, new unit and correction all
        # use the existing intake path, preserving the old statement bytes.
        text = b"A revised finite statement.\nCorrelated noise needs an additional bound.\nThe original independence premise is not granted.\n"
        cls.fixture.write("source-v2.txt", text)
        source = {"path": "source-v2.txt", "sha256": digest(text), "lines": [1, 3],
                  "quote": "Correlated noise needs an additional bound."}
        cls.fixture.body = b"TITLE: Revised finite mechanism\nEXACT CLAIM | A revised finite statement.\n"
        cls.fixture.write("cards/N1-fixture.txt", cls.fixture.body)
        cls.fixture.status["card_sha256"] = digest(cls.fixture.body)
        cls.fixture.status["proof_availability"] = {
            "located_proof_sources": [source], "available_evidence_sources": [cls.fixture.source]}
        cls.fixture.statuses()
        cls.fixture.write("indexes/agent_catalog.json", encoded({"claims": [{
            "id": "N1-fixture", "card_sha256": digest(cls.fixture.body)}]}))
        revised = copy.deepcopy(unit)
        revised.update(version=2, previous=digest((cls.root / "knowledge/units/U1-fixture/v0001.json").read_bytes()),
                       statement="The revised finite statement needs a correlated-noise bound.", evidence=[source])
        cls.fixture.write("knowledge/units/U1-fixture/v0002.json", encoded(revised))
        added = dict(revised, id="U2-new-subresult", version=1, previous=None, title="New conditional subresult")
        cls.fixture.write("knowledge/units/U2-new-subresult/v0001.json", encoded(added))
        notice = {"notice_id": "SN-correlated", "card_ids": ["N1-fixture"],
                  "clarification": "Do not assume independent noise in the revised source.", "source_refs": [source]}
        cls.fixture.write("agent/SEMANTIC_NOTICES.d/revised.jsonl", encoded(notice))
        cls.fixture.compile()
        from knowledge.retrieve import Library
        current = Library(cls.root)
        review = {"id": "synthetic-scoped-review", "decision": "accepted_internally_verified",
                  "scope": "Synthetic fixture acceptance at its exact revised version, not a real scientific audit.",
                  "subjects": [{"id": i, "content_version": current.records[i]["content_version"]}
                               for i in ("U1-fixture", "U2-new-subresult")], "evidence": [source]}
        cls.fixture.write("knowledge/reviews/synthetic.json", encoded(review))
        cls.fixture.compile()
        cls.git(cls.root, "add", ".")
        cls.commit()
        cls.git(cls.root, "branch", "-M", "main")
        cls.b = ResearchAdapter(cls.root, page_bytes=1024)

    @classmethod
    def tearDownClass(cls):
        cls.git(cls.root, "worktree", "remove", str(cls.old))
        cls.space.cleanup()
        cls.fixture.doCleanups()

    @staticmethod
    def git(root, *args):
        return subprocess.check_output(["git", "-C", str(root), *args], text=True,
                                       stderr=subprocess.STDOUT).strip()

    @classmethod
    def commit(cls):
        cls.git(cls.root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                "commit", "-qm", "synthetic intake")

    def setUp(self):
        self.version = self.a.version
        self.now = 0
        self.snapshots = Snapshots({self.a.version: self.old, self.b.version: self.root})
        self.reader = PublishedAdapter(self.old, page_bytes=1024,
            adapter_factory=lambda p: ResearchAdapter(p, page_bytes=1024),
            release_reader=lambda: {"schema": RELEASE_SCHEMA, "input_version": self.version},
            snapshots=self.snapshots, poll_seconds=30, clock=lambda: self.now)

    def update(self):
        self.version = self.b.version
        self.now = 31

    def test_ordinary_intake_updates_release_source_unit_acceptance_and_correction(self):
        before = self.reader.search("finite source")
        self.assertEqual(before["metadata"]["input_version"], self.a.version)
        self.update()
        found = self.reader.search("new conditional subresult correlated noise")
        self.assertEqual(found["metadata"]["input_version"], self.b.version)
        packet, _ = complete(self.reader, self.b.handle("record", "U2-new-subresult"))
        self.assertEqual(packet["notices"][0]["notice_id"], "SN-correlated")
        self.assertEqual(packet["review_overlays"][0]["decision"], "accepted_internally_verified")
        source, _ = complete(self.reader, packet["evidence"][0]["fetch_id"])
        self.assertIn("Correlated noise needs an additional bound", source["text"])
        self.assertEqual(source["source"]["sha256"], digest((self.root / "source-v2.txt").read_bytes()))
        marker = json.loads((self.root / "knowledge/current/release.json").read_bytes())
        self.assertEqual(release_version(marker), self.b.version)

    def test_old_page_chain_keeps_exact_payload_and_names_current_corrections(self):
        first = self.reader.fetch(self.a.handle("record", "U1-fixture"))
        self.assertIsNotNone(first["metadata"]["next_id"])
        self.update()
        tail, identifier = [], first["metadata"]["next_id"]
        while identifier:
            page = self.reader.fetch(identifier); tail.append(page)
            identifier = page["metadata"]["next_id"]
        raw = first["text"] + "".join(p["text"] for p in tail)
        self.assertEqual(digest(raw.encode()), first["metadata"]["payload_sha256"])
        for page in tail:
            freshness = page["metadata"]["freshness"]
            self.assertEqual(freshness["status"], "historical_snapshot")
            self.assertIn(self.b.handle("current", "U1-fixture"), freshness["required_current_context_ids"])
        current, _ = complete(self.reader, self.b.handle("record", "U1-fixture"))
        self.assertEqual(current["notices"][0]["notice_id"], "SN-correlated")

    def test_old_source_is_not_rebound_to_revised_bytes(self):
        handle = self.a.register(self.fixture.source)
        self.update()
        source, pages = complete(self.reader, handle)
        self.assertIn("Assume independent noise.", source["text"])
        self.assertEqual(source["source"]["sha256"], self.fixture.source["sha256"])
        self.assertEqual(pages[0]["metadata"]["freshness"]["status"], "historical_snapshot")
        self.assertTrue(pages[0]["metadata"]["freshness"]["required_current_context_ids"])

    def test_direct_record_ids_resolve_current_and_cached_runtime_is_checked(self):
        self.update()
        packet, pages = complete(self.reader, "U2-new-subresult")
        self.assertEqual(packet["id"], "U2-new-subresult")
        self.assertEqual(pages[0]["metadata"]["input_version"], self.b.version)
        with tempfile.TemporaryDirectory() as temporary:
            bare, cache = Path(temporary) / "origin.git", Path(temporary) / "cache"
            subprocess.run(["git", "clone", "--bare", str(self.root), str(bare)], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            prior = self.git(self.old, "remote", "get-url", "origin") if "origin" in self.git(self.old, "remote").splitlines() else None
            self.git(self.old, "remote", "add" if prior is None else "set-url", "origin", str(bare))
            try:
                self.git(self.old, "fetch", "origin", "main")
                provider = GitSnapshots(self.old, cache, repository_url=str(bare))
                provider.remember(self.b)
                provider.software["plugins/astra-research/server.py"] = "0" * 64
                with self.assertRaisesRegex(ValueError, "runtime code changed"):
                    provider.stage(self.b.version)
                self.assertEqual(provider.stage(self.b.version, historical=True), self.root)
            finally:
                if prior is None:
                    self.git(self.old, "remote", "remove", "origin")
                else:
                    self.git(self.old, "remote", "set-url", "origin", prior)

    def test_failed_release_check_cannot_silently_serve_cached_current_results(self):
        self.reader.search("finite")
        self.now = 31
        self.reader.read_release = lambda: (_ for _ in ()).throw(OSError("network unavailable"))
        for call in (lambda: self.reader.search("finite"),
                     lambda: self.reader.fetch(self.a.handle("record", "N1-fixture"))):
            with self.assertRaisesRegex(ValueError, "published_refresh_failed") as error:
                call()
            self.assertIn(self.a.version, str(error.exception))
        self.assertIs(self.reader.active, self.reader.adapters[self.a.version])

    def test_missing_new_support_fails_without_switching_then_recovers(self):
        self.update()
        source = self.root / "source-v2.txt"; raw = source.read_bytes()
        try:
            source.unlink()
            with self.assertRaisesRegex(ValueError, "published_refresh_failed"):
                self.reader.search("new subresult")
            self.assertEqual(self.reader.active.version, self.a.version)
        finally:
            source.write_bytes(raw)
        self.assertEqual(self.reader.search("new subresult")["metadata"]["input_version"], self.b.version)

    def test_request_polling_and_repeated_intake_are_bounded_and_idempotent(self):
        self.reader.search("finite")
        self.version = self.b.version; self.now = 1
        cached = self.reader.search("finite")
        self.assertEqual(cached["metadata"]["freshness"]["check_interval_seconds"], 30)
        self.assertEqual(cached["metadata"]["input_version"], self.a.version)
        self.now = 31
        self.reader.search("finite"); staged = list(self.snapshots.staged)
        self.now = 62
        self.reader.search("finite")
        self.assertEqual(self.snapshots.staged, staged)
        self.assertEqual(self.reader.active.version, self.b.version)

    def test_release_probe_pins_git_revision_and_rejects_oversized_metadata(self):
        revision = "a" * 40
        class Response(io.BytesIO):
            def geturl(self):
                return "https://raw.githubusercontent.com/harjassand/astra-research-knowledge/" + revision + "/knowledge/current/release.json"
        with patch("knowledge.published.subprocess.run", return_value=SimpleNamespace(stdout=revision + "\trefs/heads/main\n")), \
             patch("knowledge.published.urllib.request.urlopen", return_value=Response(encoded({"schema": RELEASE_SCHEMA, "input_version": self.a.version}))) as opened:
            marker = read_release()
            self.assertEqual(marker["published_revision"], revision)
            self.assertIn("/" + revision + "/", opened.call_args.args[0].full_url)
            self.assertNotIn("/main/", opened.call_args.args[0].full_url)
        with patch("knowledge.published.subprocess.run", return_value=SimpleNamespace(stdout=revision + "\trefs/heads/main\n")), \
             patch("knowledge.published.urllib.request.urlopen", return_value=Response(b"x" * 8193)):
            with self.assertRaisesRegex(ValueError, "metadata budget"):
                read_release()

    def test_sparse_git_snapshot_and_historical_rematerialization(self):
        with tempfile.TemporaryDirectory() as temporary:
            bare, cache = Path(temporary) / "origin.git", Path(temporary) / "cache"
            subprocess.run(["git", "clone", "--bare", str(self.root), str(bare)], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            prior = self.git(self.old, "remote", "get-url", "origin") if "origin" in self.git(self.old, "remote").splitlines() else None
            self.git(self.old, "remote", "add" if prior is None else "set-url", "origin", str(bare))
            self.git(self.old, "fetch", "origin", "main")
            provider = GitSnapshots(self.old, cache, repository_url=str(bare))
            provider.remember(self.a)
            path = provider.stage(self.b.version)
            reader = ResearchAdapter(path)
            self.assertEqual(reader.version, self.b.version)
            self.assertTrue((path / "source-v2.txt").is_file())
            self.assertFalse(any(path.rglob("*.sqlite")))
            provider.remember(reader, owned=True)
            # A committed but unpublished revision must not gain a public URL
            # merely because its unchanged data has a known input identity.
            private = subprocess.check_output(["git", "-C", str(self.root), "-c", "user.name=Fixture",
                "-c", "user.email=fixture@example.invalid", "commit-tree", self.git(self.root, "rev-parse", "HEAD^{tree}"),
                "-p", self.b.revision, "-m", "unpublished"], text=True).strip()
            with self.assertRaisesRegex(ValueError, "published main history"):
                provider.remember(SimpleNamespace(version=self.b.version, revision=private, root=path))
            active = PublishedAdapter(self.old, snapshots=provider,
                release_reader=lambda: {"schema": RELEASE_SCHEMA, "input_version": self.b.version},
                clock=lambda: 0)
            self.assertEqual(active.search("finite")["metadata"]["input_version"], self.b.version)
            provider.prune([self.old])
            self.assertFalse(path.exists())
            self.assertEqual(self.git(self.old, "rev-parse", "refs/astra/served/" + self.b.version), self.b.revision)
            # Simulate another process evicting an idle reader's clean copy.
            # Even within its poll TTL, it must rematerialize before reading.
            self.assertEqual(active.search("finite")["metadata"]["input_version"], self.b.version)
            provider.prune([self.old])
            restored = provider.stage(self.b.version, historical=True)
            self.assertEqual(ResearchAdapter(restored).version, self.b.version)
            self.git(self.old, "worktree", "remove", str(restored))
            if prior is None:
                self.git(self.old, "remote", "remove", "origin")
            else:
                self.git(self.old, "remote", "set-url", "origin", prior)


if __name__ == "__main__":
    unittest.main()
