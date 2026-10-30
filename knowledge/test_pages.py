"""Real Git snapshots/publication without network, private data or source replay."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from knowledge import pages


class BoundedPages(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.area = Path(temporary.name)
        self.root = self.area / "source"; self.root.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.inputs = {
            "research/original.bin": b"exact source bytes\x00\xff",
            "00_START_HERE.txt": b"Current entry\n",
            "agent/CURRENT.txt": b"Historical interfaces\n",
            "index-historical-20261025.html": b"<p>Unchanged historical source</p>",
            "knowledge/index.html": (pages.ROOT / "knowledge/index.html").read_bytes(),
            "knowledge/search.js": (pages.ROOT / "knowledge/search.js").read_bytes(),
            "knowledge/README.md": b"Read exact sources and conditions.\n",
            "knowledge/INTAKE.md": b"One ordinary intake path.\n",
            "knowledge/PAGES.md": b"Bounded projection, public originals.\n",
            "agent/ACCESS.txt": b"Pinned raw source base.\n",
            "AGENTS.md": b"Preserve sources and scope.\n",
        }
        packet = {"id": "N1-fixture", "title": "Supplied mechanism", "statement": "Conditional result",
                  "contract": {}, "review_overlays": [], "notices": [],
                  "evidence": [{"path": "research/original.bin", "sha256": pages.sha(self.inputs["research/original.bin"])}]}
        shards = sorted({pages.sha(term.encode())[:2] for term in ("probe", "mechanism")})
        self.outputs = {
            "knowledge/current/records.jsonl": pages.encoded({"id": "N1-fixture"}),
            "knowledge/current/packets/N1.json": pages.encoded(packet),
            "knowledge/current/catalog.json": pages.encoded({"records": [{"record_id": "N1-fixture",
                "parents": [], "title": "Supplied mechanism", "kind": "result"}], "concepts": [],
                "documents": [[0, 0]], "shards": shards, "lexical_shards": shards}),
            "knowledge/current/content/00.json": b"{}\n",
            "knowledge/current/postings/00.json": b"{}\n",
            "knowledge/current/browse/index.txt": b"N1\n",
            "knowledge/current/coverage.json": b"{}\n",
        }
        for shard in shards:
            data = pages.encoded({term: [[0, 2]] for term in ("probe", "mechanism") if pages.sha(term.encode())[:2] == shard})
            for folder in ("postings", "lexical"):
                self.outputs["knowledge/current/" + folder + "/" + shard + ".json"] = data
        self.refresh()
        self.revision = self.commit()
        self.output = self.area / "site"

    def git(self, *args, root=None):
        return subprocess.check_output(["git", *args], cwd=root or self.root, stderr=subprocess.STDOUT)

    def put(self, path, data):
        target = self.root / path; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)

    def refresh(self):
        for name, data in {**self.inputs, **self.outputs}.items():
            self.put(name, data)
        search = pages.encoded({"input_version": "a" * 64, "outputs": {
            p: pages.sha(b) for p, b in self.outputs.items() if p != "knowledge/current/search_manifest.json"}})
        self.outputs["knowledge/current/search_manifest.json"] = search
        self.put("knowledge/current/search_manifest.json", search)
        self.put("knowledge/current/manifest.json", pages.encoded({"input_version": "a" * 64,
            "inputs": {p: pages.sha(b) for p, b in self.inputs.items()},
            "outputs": {p: pages.sha(b) for p, b in self.outputs.items()}}))

    def commit(self):
        self.git("add", "--all")
        self.git("commit", "-qm", "snapshot")
        return self.git("rev-parse", "HEAD").decode().strip()

    def remote(self):
        remote = self.area / "remote.git"
        subprocess.run(["git", "init", "--bare", "-q", str(remote)], check=True)
        self.git("remote", "add", "origin", str(remote))
        self.git("push", "-q", "origin", "main")
        return remote

    def test_all_packets_and_exact_views_with_pinned_originals_and_history(self):
        manifest, size = pages.stage(self.revision, self.output, self.root)
        self.assertLess(size, pages.MAX_BYTES)
        self.assertEqual(manifest["scientific_records"], 1)
        for name in self.outputs:
            if name == "knowledge/current/records.jsonl":
                continue
            self.assertEqual((self.output / name).read_bytes(), self.outputs[name])
        self.assertFalse((self.output / "research/original.bin").exists())
        self.assertEqual(self.git("show", self.revision + ":research/original.bin"), self.inputs["research/original.bin"])
        self.assertIn(self.revision, (self.output / "history.html").read_text())
        self.assertIn('id="publication"', (self.output / "knowledge/index.html").read_text())
        self.assertIn(self.revision, (self.output / "404.html").read_text())
        routes = json.loads((self.output / "source-routes.json").read_bytes())
        self.assertIn("research/original.bin", routes["paths"])
        first = (self.output / "publication.json").read_bytes()
        pages.stage(self.revision, self.output, self.root)
        other = self.area / "again"; pages.stage(self.revision, other, self.root)
        self.assertEqual(first, (other / "publication.json").read_bytes())

    def test_working_copy_cannot_change_committed_source_view(self):
        self.put("knowledge/current/packets/N1.json", b"uncommitted wrong branch")
        pages.stage(self.revision, self.output, self.root)
        self.assertEqual((self.output / "knowledge/current/packets/N1.json").read_bytes(), self.outputs["knowledge/current/packets/N1.json"])

    def test_actual_staged_natural_query_uses_both_lanes_and_opens_packet(self):
        pages.stage(self.revision, self.output, self.root)
        subprocess.run(["node", str(pages.ROOT / "knowledge/test_pages_query.cjs"), str(self.output)], check=True)

    def test_missing_query_shard_fails_even_with_self_consistent_file_hashes(self):
        pages.stage(self.revision, self.output, self.root)
        metadata = json.loads((self.output / "publication.json").read_bytes())
        missing = next(p for p in metadata["files"] if p.startswith("knowledge/current/lexical/"))
        (self.output / missing).unlink(); del metadata["files"][missing]
        (self.output / "publication.json").write_bytes(pages.encoded(metadata))
        with self.assertRaisesRegex(ValueError, "query closure is incomplete"):
            pages.validate_site(self.output)
        del self.outputs[missing]
        self.refresh(); revision = self.commit()
        with self.assertRaisesRegex(ValueError, "query closure is incomplete"):
            pages.stage(revision, self.area / "missing-declaration", self.root)

    def test_missing_declared_original_fails_even_when_present_only_locally(self):
        self.git("rm", "--cached", "research/original.bin")
        self.git("commit", "-qm", "omitted original")
        revision = self.git("rev-parse", "HEAD").decode().strip()
        with self.assertRaisesRegex(ValueError, "lacks required inputs"):
            pages.stage(revision, self.output, self.root)
        self.assertFalse(self.output.exists())

    def test_stale_committed_view_and_incomplete_packet_closure_fail(self):
        self.put("knowledge/current/packets/N1.json", b"stale view")
        revision = self.commit()
        with self.assertRaisesRegex(ValueError, "Canonical browser view changed"):
            pages.stage(revision, self.output, self.root)
        self.outputs["knowledge/current/records.jsonl"] += pages.encoded({"id": "N2-missing"})
        self.refresh(); revision = self.commit()
        with self.assertRaisesRegex(ValueError, "complete canonical record set"):
            pages.stage(revision, self.output, self.root)

    def test_budget_and_tamper_protection_do_not_destroy_existing_work(self):
        with self.assertRaisesRegex(ValueError, "byte budget"):
            pages.stage(self.revision, self.output, self.root, max_bytes=8)
        self.assertFalse(self.output.exists())
        self.output.mkdir(); (self.output / "note.txt").write_text("unrelated work")
        with self.assertRaises((OSError, ValueError)):
            pages.stage(self.revision, self.output, self.root)
        self.assertEqual((self.output / "note.txt").read_text(), "unrelated work")
        other = self.area / "valid"; pages.stage(self.revision, other, self.root)
        (other / "knowledge/current/packets/N1.json").write_text("tampered")
        with self.assertRaisesRegex(ValueError, "Changed public-view bytes"):
            pages.validate_site(other)

    def test_staging_inside_source_checkout_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "outside the source checkout"):
            pages.stage(self.revision, self.root / "docs", self.root)

    def test_wrong_branch_metadata_is_rejected_even_when_file_hashes_match(self):
        pages.stage(self.revision, self.output, self.root)
        path = self.output / "publication.json"
        metadata = json.loads(path.read_bytes())
        metadata["source_revision"] = "0" * 40
        path.write_bytes(pages.encoded(metadata))
        with self.assertRaisesRegex(ValueError, "source versions disagree"):
            pages.validate_site(self.output)

    def test_pinned_paths_encode_names_and_reject_escape(self):
        self.assertTrue(pages.source_url(self.revision, "research/a b.md").endswith("/research/a%20b.md"))
        for name in ("../secret", "/absolute", "a//b", "a\\b", "a\nb"):
            with self.assertRaises(ValueError):
                pages.source_url(self.revision, name)

    def test_real_branch_publication_is_idempotent_and_preserves_main_and_index(self):
        remote = self.remote()
        before = self.git("ls-files", "-s")
        (self.root / "scratch.txt").write_text("unrelated work")
        with patch.object(pages, "REMOTE", str(remote)):
            first = pages.publish(self.revision, self.root)
            second = pages.publish(self.revision, self.root)
            self.assertEqual(second["result"], "unchanged")
            self.assertEqual(first["publication_revision"], second["publication_revision"])
            self.assertEqual(pages.remote_revision(self.root, "main"), self.revision)
            self.assertEqual(before, self.git("ls-files", "-s"))
            self.assertEqual((self.root / "scratch.txt").read_text(), "unrelated work")
            self.put("source-note.txt", b"later source-tree version\n"); later = self.commit()
            self.git("push", "-q", "origin", "main")
            third = pages.publish(later, self.root)
            parent = self.git("show", "-s", "--format=%P", third["publication_revision"]).decode().strip()
            self.assertEqual(parent, first["publication_revision"])
            self.assertEqual(pages.remote_revision(self.root, "main"), later)
            with self.assertRaisesRegex(ValueError, "latest reviewed merged main"):
                pages.publish(self.revision, self.root)

    def test_unowned_publication_branch_is_preserved(self):
        remote = self.remote()
        self.git("push", "-q", "origin", "main:refs/heads/" + pages.BRANCH)
        with patch.object(pages, "REMOTE", str(remote)), self.assertRaises((ValueError, subprocess.CalledProcessError)):
            pages.publish(self.revision, self.root)
        self.assertEqual(pages.remote_revision(self.root, pages.BRANCH), self.revision)

    def test_unrelated_file_added_to_owned_branch_is_not_dropped(self):
        remote = self.remote()
        with patch.object(pages, "REMOTE", str(remote)):
            first = pages.publish(self.revision, self.root)
            editor = self.area / "publication-editor"
            self.git("worktree", "add", "--detach", str(editor), first["publication_revision"])
            (editor / "note.txt").write_text("unrelated owner note")
            self.git("add", "note.txt", root=editor)
            self.git("commit", "-qm", "owner note", root=editor)
            self.git("push", "-q", "origin", "HEAD:refs/heads/" + pages.BRANCH, root=editor)
            changed = pages.remote_revision(self.root, pages.BRANCH)
            with self.assertRaisesRegex(ValueError, "unowned or missing files"):
                pages.publish(self.revision, self.root)
            self.assertEqual(pages.remote_revision(self.root, pages.BRANCH), changed)
            self.assertEqual((editor / "note.txt").read_text(), "unrelated owner note")


if __name__ == "__main__":
    unittest.main()
