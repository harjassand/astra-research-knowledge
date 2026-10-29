"""Catch required archived bytes omitted by Git ignore rules before publication."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from state.check_current import publication_membership


class PublicationMembership(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.git("init", "-q")
        (self.root / ".gitignore").write_text("__pycache__/\n*.pyc\n")
        self.source = "research/receipt/__pycache__/original.cpython-312.pyc"
        self.view = "knowledge/current/records.jsonl"
        for name, data in [(self.source, b"preserved binary source bytes\x00"), (self.view, b"{}\n")]:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        self.manifest = self.root / "knowledge/current/manifest.json"
        self.manifest.write_text(json.dumps({"inputs": {self.source: "declared"}, "outputs": {self.view: "declared"}}))
        self.git("add", ".gitignore", self.view, str(self.manifest.relative_to(self.root)))

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, stderr=subprocess.STDOUT)

    def test_required_ignored_original_fails_before_publication(self):
        with self.assertRaisesRegex(ValueError, "absent from the Git publication index") as error:
            publication_membership(self.root)
        self.assertIn(self.source, str(error.exception))

    def test_explicitly_staged_original_is_kept_even_with_cache_extension(self):
        self.git("add", "-f", self.source)
        publication_membership(self.root)
        self.assertEqual((self.root / self.source).read_bytes(), b"preserved binary source bytes\x00")

    def test_unstaged_required_view_is_rejected(self):
        self.git("add", "-f", self.source)
        (self.root / self.view).write_text('{"new":true}\n')
        with self.assertRaisesRegex(ValueError, "differ from the Git publication index"):
            publication_membership(self.root)

    def test_unrelated_private_scratch_does_not_block_intake(self):
        self.git("add", "-f", self.source)
        (self.root / "scratch.txt").write_text("unregistered working note\n")
        publication_membership(self.root)

    def test_malformed_manifest_membership_is_not_silently_ignored(self):
        self.manifest.write_text(json.dumps({"inputs": [], "outputs": {}}))
        with self.assertRaisesRegex(ValueError, "Invalid knowledge manifest"):
            publication_membership(self.root)


if __name__ == "__main__":
    unittest.main()
