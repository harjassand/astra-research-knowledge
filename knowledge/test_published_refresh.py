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
        orphan = b"An earlier finite statement has an obsolete extension.\nThe old passage remains unchanged.\nIts correction arrived later.\n"
        cls.orphan_source = {"path": "research/late-context/source/orphan.txt",
                             "sha256": digest(orphan), "lines": [1, 3],
                             "quote": "obsolete extension"}
        cls.fixture.write(cls.orphan_source["path"], orphan)
        cls.fixture.write("research/late-context/source/INDEX.json", encoded({
            "schema": "astra.intake-source-index.v1", "files": [{
                "path": "source/orphan.txt", "sha256": digest(orphan),
                "bytes": len(orphan), "kind": "original_scientific_source"}]}))
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
                  "clarification": "Do not assume independent noise in the revised source.",
                  "source_refs": [source, cls.orphan_source]}
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

    def test_old_uncited_source_names_correction_first_added_by_new_record(self):
        key = (self.orphan_source["path"], self.orphan_source["sha256"])
        self.assertFalse(self.a.contexts[key])
        handle = next(self.a.handle("source", ident) for ident, ref in self.a.references.items()
                      if (ref["path"], ref["sha256"]) == key)
        _, before = complete(self.reader, handle)
        self.update()
        source, after = complete(self.reader, handle)
        self.assertEqual("".join(p["text"] for p in before), "".join(p["text"] for p in after))
        self.assertEqual(source["source"]["sha256"], self.orphan_source["sha256"])
        for page in after:
            freshness = page["metadata"]["freshness"]
            self.assertEqual(freshness["status"], "historical_snapshot")
            self.assertIn(self.b.handle("current", "U2-new-subresult"),
                          freshness["required_current_context_ids"])

    def test_historical_source_context_does_not_cross_a_different_branch_hash(self):
        key = (self.orphan_source["path"], self.orphan_source["sha256"])
        handle = next(self.a.handle("source", ident) for ident, ref in self.a.references.items()
                      if (ref["path"], ref["sha256"]) == key)
        self.update()
        self.reader.search("new conditional subresult")
        contexts = dict(self.reader.active.contexts)
        contexts.pop(key, None)
        contexts[(key[0], "0" * 64)] = {"U2-new-subresult"}
        with patch.object(self.reader.active, "contexts", contexts):
            _, pages = complete(self.reader, handle)
        self.assertTrue(all(not p["metadata"]["freshness"]["required_current_context_ids"]
                            for p in pages))

    def test_known_history_pages_share_ttl_but_unknown_newer_handle_forces_check(self):
        with patch.object(self.reader,'read_release',wraps=self.reader.read_release) as checks:
            self.reader.search('finite source')
            self.assertEqual(checks.call_count,1)
            # A newer server can issue this handle before our cached TTL expires.
            self.version=self.b.version;self.now=1
            current,_=complete(self.reader,self.b.handle('current','U2-new-subresult'))
            self.assertEqual(current['id'],'U2-new-subresult')
            self.assertEqual(checks.call_count,2)
            old,pages=complete(self.reader,self.a.handle('record','U1-fixture'))
            self.assertGreater(len(pages),1)
            self.assertEqual(checks.call_count,2)
            self.assertEqual(old,self.a.record_payload(self.a.library.resolve('U1-fixture')))
            self.assertTrue(all(p['metadata']['freshness']['status']=='historical_snapshot'for p in pages))
            self.assertTrue(all(self.b.handle('current','U1-fixture')in
                p['metadata']['freshness']['required_current_context_ids']for p in pages))
            self.now=32
            self.reader.fetch(pages[0]['id'])
            self.assertEqual(checks.call_count,3)

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

    def test_same_input_revision_binding_survives_other_server_restart_and_eviction(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder=Path(temporary);bare=folder/'origin.git';cache=folder/'cache';doc=folder/'doc-only'
            subprocess.run(['git','clone','--bare',str(self.root),str(bare)],check=True,
                           stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            prior=self.git(self.old,'remote','get-url','origin') if 'origin' in self.git(self.old,'remote').splitlines() else None
            self.git(self.old,'remote','add' if prior is None else 'set-url','origin',str(bare))
            try:
                self.git(self.old,'fetch','origin','main')
                provider=GitSnapshots(self.old,cache,repository_url=str(bare))
                first_root=provider.stage(self.b.version)
                first=ResearchAdapter(first_root,page_bytes=1024)
                provider.remember(first,owned=True)
                head=subprocess.check_output(['git','-C',str(self.root),'-c','user.name=Fixture',
                    '-c','user.email=fixture@example.invalid','commit-tree',self.git(self.root,'rev-parse','HEAD^{tree}'),
                    '-p',self.b.revision,'-m','same-input published revision'],text=True).strip()
                self.git(self.old,'push','origin',head+':refs/heads/main')
                self.git(self.old,'fetch','origin','main')
                self.git(self.old,'worktree','add','--detach',str(doc),head)
                later=ResearchAdapter(doc,page_bytes=1024)
                self.assertEqual(later.version,first.version)
                handle=first.handle('record','U1-fixture')
                expected,expected_pages=complete(first,handle)
                self.assertGreater(len(expected_pages),1)
                provider.remember(later)
                self.assertEqual(provider.versions[first.version]['revision'],first.revision)
                self.assertEqual(self.git(self.old,'rev-parse','refs/astra/served/'+first.version),first.revision)
                provider.prune([self.old,doc])
                self.assertFalse(first_root.exists())
                # The permanent ref also prevents rebinding while rebuilding
                # this entry after the local registry itself is lost.
                provider.registry_path.unlink()
                restarted=PublishedAdapter(doc,page_bytes=1024,
                    snapshots=GitSnapshots(doc,cache,repository_url=str(bare)),
                    release_reader=lambda:{'schema':RELEASE_SCHEMA,'input_version':first.version,'published_revision':head},
                    poll_seconds=0)
                actual,actual_pages=complete(restarted,handle)
                self.assertEqual(actual,expected)
                self.assertEqual([p['text']for p in actual_pages],[p['text']for p in expected_pages])
                self.assertEqual(actual_pages[0]['metadata']['payload_sha256'],expected_pages[0]['metadata']['payload_sha256'])
                self.assertEqual(restarted.active.revision,first.revision)
                self.assertEqual(actual_pages[0]['metadata']['freshness']['published_revision'],head)
                self.git(self.old,'worktree','remove',str(first_root))
            finally:
                if doc.exists():self.git(self.old,'worktree','remove',str(doc))
                if prior is None:self.git(self.old,'remote','remove','origin')
                else:self.git(self.old,'remote','set-url','origin',prior)

    def test_interrupted_materialization_is_preserved_and_next_request_recovers(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder=Path(temporary);bare=folder/'origin.git';cache=folder/'cache'
            subprocess.run(['git','clone','--bare',str(self.root),str(bare)],check=True,
                           stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            self.git(self.old,'remote','add','origin',str(bare))
            class InterruptOnce(GitSnapshots):
                interrupted=False
                def git(provider,root,*args,input=None,binary=False):
                    if args[0]=='checkout-index' and not provider.interrupted:
                        provider.interrupted=True
                        (Path(root)/'partial-note.txt').write_text('preserve this interrupted fragment')
                        metadata=Path(super().git(root,'rev-parse','--git-dir'))
                        (metadata/'index.lock').write_bytes(b'')
                        raise ValueError('Published Git operation timed out: checkout-index (budget 120 seconds)')
                    return super().git(root,*args,input=input,binary=binary)
            try:
                self.git(self.old,'fetch','origin','main')
                provider=InterruptOnce(self.old,cache,repository_url=str(bare))
                reader=PublishedAdapter(self.old,snapshots=provider,poll_seconds=0,
                    release_reader=lambda:{'schema':RELEASE_SCHEMA,'input_version':self.b.version})
                with self.assertRaisesRegex(ValueError,'published_refresh_failed'):
                    reader.search('U2-new-subresult')
                self.assertEqual(reader.active.version,self.a.version)
                self.assertFalse((cache/self.b.revision).exists())
                retained=list((cache/'failed-staging').iterdir())
                self.assertEqual(len(retained),1)
                self.assertEqual((retained[0]/'partial-note.txt').read_text(),'preserve this interrupted fragment')
                self.assertEqual(self.git(retained[0],'rev-parse','HEAD'),self.b.revision)
                found=reader.search('U2-new-subresult')
                self.assertEqual(found['metadata']['input_version'],self.b.version)
                packet,_=complete(reader,found['results'][0]['id'])
                self.assertEqual(packet['notices'][0]['notice_id'],'SN-correlated')
                self.assertEqual(packet['review_overlays'][0]['decision'],'accepted_internally_verified')
                for path in [reader.active.root,*retained]:
                    # Only temporary,explicitly injected test artifacts.
                    self.git(self.old,'worktree','remove','--force',str(path))
            finally:
                self.git(self.old,'remote','remove','origin')

    def test_legacy_partial_cache_is_quarantined_but_served_edits_are_not_replaced(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder=Path(temporary);bare=folder/'origin.git';cache=folder/'cache'
            subprocess.run(['git','clone','--bare',str(self.root),str(bare)],check=True,
                           stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            self.git(self.old,'remote','add','origin',str(bare))
            try:
                self.git(self.old,'fetch','origin','main')
                provider=GitSnapshots(self.old,cache,repository_url=str(bare))
                target=cache/self.b.revision
                self.git(self.old,'worktree','add','--detach','--no-checkout',str(target),self.b.revision)
                (target/'partial-note.txt').write_text('legacy partial bytes')
                metadata=Path(self.git(target,'rev-parse','--git-dir'))
                (metadata/'index.lock').write_bytes(b'')
                with self.assertRaisesRegex(ValueError,'Unregistered incomplete cache contains files'):
                    provider.stage(self.b.version)
                self.assertEqual((target/'partial-note.txt').read_text(),'legacy partial bytes')
                # Remove only this explicitly authored test note. The observed
                # production legacy failure had .git alone and an empty lock.
                (target/'partial-note.txt').unlink()
                result=provider.stage(self.b.version)
                self.assertEqual(result,target.resolve())
                self.assertTrue(provider.materialized(result,self.b.revision,self.b.version))
                adapter=ResearchAdapter(result)
                provider.remember(adapter,owned=True)
                retained=list((cache/'failed-staging').iterdir())
                self.assertTrue((retained[0]/'.git').is_file())
                self.git(result,'rm','--cached','source-v2.txt')
                with self.assertRaisesRegex(ValueError,'Retained snapshot is incomplete'):
                    provider.stage(self.b.version,historical=True)
                self.assertTrue((result/'source-v2.txt').exists())
                self.assertEqual(len(list((cache/'failed-staging').iterdir())),1)
                for path in [result,*retained]:
                    self.git(self.old,'worktree','remove','--force',str(path))
            finally:
                self.git(self.old,'remote','remove','origin')

    def test_reuses_only_unchanged_sources_and_keeps_independent_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary); bare = folder / "origin.git"; cache = folder / "cache"
            subprocess.run(["git", "clone", "--bare", str(self.root), str(bare)], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.git(self.old, "remote", "add", "origin", str(bare))
            source = self.old / self.fixture.source["path"]
            before = source.read_bytes()
            result = None
            try:
                provider = GitSnapshots(self.old, cache, repository_url=str(bare))
                original_git = provider.git
                checked_out = set()
                def track(root, *args, **kwargs):
                    if args[0] == "checkout-index":
                        checked_out.update(kwargs["input"].split(b"\0"))
                    return original_git(root, *args, **kwargs)
                with patch.object(provider, "git", side_effect=track):
                    result = provider.stage(self.b.version)
                self.assertNotIn(self.fixture.source["path"].encode(), checked_out)
                self.assertIn(b"source-v2.txt", checked_out)
                self.assertEqual(ResearchAdapter(result).version, self.b.version)
                copied = result / self.fixture.source["path"]
                self.assertFalse(source.samefile(copied))
                source.write_bytes(b"An unrelated edit to the retained working copy.")
                self.assertEqual(copied.read_bytes(), before)
            finally:
                source.write_bytes(before)
                if result and result.exists():
                    self.git(self.old, "worktree", "remove", str(result))
                self.git(self.old, "remote", "remove", "origin")

    def test_modified_cached_source_fails_closed_and_keeps_both_copies(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary); bare = folder / "origin.git"; cache = folder / "cache"
            subprocess.run(["git", "clone", "--bare", str(self.root), str(bare)], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.git(self.old, "remote", "add", "origin", str(bare))
            source = self.old / self.fixture.source["path"]
            before = source.read_bytes()
            altered = b"Preserve this edited historical fixture."
            try:
                provider = GitSnapshots(self.old, cache, repository_url=str(bare))
                source.write_bytes(altered)
                with self.assertRaisesRegex(ValueError, "Cached snapshot bytes differ"):
                    provider.stage(self.b.version)
                self.assertEqual(source.read_bytes(), altered)
                self.assertFalse((cache / self.b.revision).exists())
                retained = list((cache / "failed-staging").iterdir())
                self.assertEqual(len(retained), 1)
                self.assertEqual((retained[0] / self.fixture.source["path"]).read_bytes(), altered)
            finally:
                source.write_bytes(before)
                # Only explicitly created disposable fixture worktrees.
                for marker in cache.rglob(".git"):
                    if marker.is_file():
                        self.git(self.old, "worktree", "remove", "--force", str(marker.parent))
                self.git(self.old, "remote", "remove", "origin")

    def test_reuse_keeps_committed_mode_without_changing_cached_source_mode(self):
        import os
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary); bare = folder / "origin.git"; cache = folder / "cache"
            subprocess.run(["git", "clone", "--bare", str(self.root), str(bare)], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.git(self.old, "remote", "add", "origin", str(bare))
            source = self.old / self.fixture.source["path"]
            old_mode = source.stat().st_mode & 0o777
            result = None
            try:
                source.chmod(old_mode | 0o111)
                provider = GitSnapshots(self.old, cache, repository_url=str(bare))
                result = provider.stage(self.b.version)
                self.assertEqual((result / self.fixture.source["path"]).stat().st_mode & 0o777, 0o644)
                self.assertEqual(source.stat().st_mode & 0o777, old_mode | 0o111)
                self.assertEqual(ResearchAdapter(result).version, self.b.version)
            finally:
                source.chmod(old_mode)
                if result and result.exists():
                    self.git(self.old, "worktree", "remove", str(result))
                self.git(self.old, "remote", "remove", "origin")


    def test_materialization_budget_and_portable_failure_reason(self):
        with tempfile.TemporaryDirectory() as temporary:
            with patch('knowledge.published.subprocess.run',return_value=SimpleNamespace(stdout='https://github.com/harjassand/astra-research-knowledge.git')):
                provider=GitSnapshots(self.old,Path(temporary),software={})
            with patch('knowledge.published.subprocess.run',return_value=SimpleNamespace(stdout=''))as called:
                provider.git(self.old,'checkout','--detach',self.b.revision)
                self.assertEqual(called.call_args.kwargs['timeout'],120)
                provider.git(self.old,'checkout-index','-z','--stdin',input=b'proof.txt\0',binary=True)
                self.assertEqual(called.call_args.kwargs['timeout'],120)
                self.assertFalse(called.call_args.kwargs['text'])
                provider.git(self.old,'fetch','origin','main')
                self.assertEqual(called.call_args.kwargs['timeout'],45)
            with patch('knowledge.published.subprocess.run',side_effect=subprocess.TimeoutExpired('git',120)):
                with self.assertRaisesRegex(ValueError,'timed out: checkout.*120 seconds'):
                    provider.git(self.old,'checkout','--detach',self.b.revision)
            with patch('knowledge.published.subprocess.run',side_effect=subprocess.CalledProcessError(128,'git',stderr='private host detail')):
                with self.assertRaisesRegex(ValueError,'failed: checkout.*exit 128')as error:
                    provider.git(self.old,'checkout','--detach',self.b.revision)
                self.assertNotIn('private host detail',str(error.exception))

    def test_literal_snapshot_paths_keep_metacharacters_and_unrelated_source_work(self):
        from knowledge.build import build, publish, check
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary); doc = folder / 'literal-source'; bare = folder / 'origin.git'
            self.git(self.old, 'worktree', 'add', '--detach', str(doc), self.b.revision)
            paths = ['source/ leading name.txt', 'source/nested/[literal]*?.txt', 'source/Unicode/λ.txt']
            entries = []
            for number, name in enumerate(paths):
                data = ('A literal fixture source ' + str(number) + '.\n').encode()
                target = doc / 'research/literal' / name
                target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
                entries.append({'path': name, 'sha256': digest(data), 'bytes': len(data),
                                'kind': 'original_scientific_source'})
            (doc / 'research/literal/source/INDEX.json').write_bytes(encoded({
                'schema': 'astra.intake-source-index.v1', 'files': entries}))
            (doc / ' leading unselected.txt').write_bytes(b'Keep its committed index entry, not its working copy.')
            outputs, manifest = build(doc); publish(doc, outputs)
            self.git(doc, 'add', '.')
            self.git(doc, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                     'commit', '-qm', 'Literal scientific source paths')
            revision = self.git(doc, 'rev-parse', 'HEAD')
            note = doc / 'UNRELATED_NOTE'; note.write_bytes(b'Unrelated source checkout work remains.')
            subprocess.run(['git', 'clone', '--bare', str(self.root), str(bare)], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.git(doc, 'push', str(bare), 'HEAD:refs/heads/main')
            self.git(self.old, 'remote', 'add', 'origin', str(bare))
            result = None
            try:
                provider = GitSnapshots(self.old, folder / 'cache', repository_url=str(bare))
                result = provider.stage(manifest['input_version'])
                self.assertEqual(check(result, regenerate=False), manifest)
                for name in paths:
                    target = Path('research/literal') / name
                    self.assertEqual((result / target).read_bytes(), (doc / target).read_bytes())
                self.assertFalse((result / ' leading unselected.txt').exists())
                self.assertEqual(self.git(result, 'write-tree'), self.git(doc, 'rev-parse', revision + '^{tree}'))
                self.assertEqual(self.git(result, 'status', '--porcelain'), '')
                self.assertEqual(note.read_bytes(), b'Unrelated source checkout work remains.')
            finally:
                if result and result.exists(): self.git(self.old, 'worktree', 'remove', str(result))
                self.git(self.old, 'remote', 'remove', 'origin')
                # Only the explicitly created fixture note in its disposable worktree.
                self.git(self.old, 'worktree', 'remove', '--force', str(doc))


if __name__ == "__main__":
    unittest.main()
