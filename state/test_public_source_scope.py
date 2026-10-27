"""Prevent the actual draft-source locator regression before another public push."""
from pathlib import Path
import subprocess
import tempfile
import unittest

from state.check_current import public_path_portability


class PublicSourceScope(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.git("init", "-q")
        (self.root / "research").mkdir()
        self.file = self.root / "research/source.txt"
        self.file.write_text("Scientific statement.\n")
        self.commit()
        self.base = self.git("rev-parse", "HEAD").strip()

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, stderr=subprocess.STDOUT, text=True)

    def commit(self):
        self.git("add", "research")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "fixture")

    def test_added_host_locator_is_rejected_without_printing_its_value(self):
        locator = "/" + "Users" + "/fixture/private/source.md"
        self.file.write_text("Source: " + locator + "\n")
        with self.assertRaises(ValueError) as error:
            public_path_portability(self.base, self.root)
        self.assertIn("research/source.txt", str(error.exception))
        self.assertNotIn(locator, str(error.exception))

    def test_file_url_is_rejected(self):
        self.file.write_text("Source: " + "file" + ":/" + "/local/source.md\n")
        with self.assertRaisesRegex(ValueError, "local locators"):
            public_path_portability(self.base, self.root)

    def test_unchanged_legacy_source_does_not_become_an_idle_gate(self):
        self.file.write_text("Legacy: /" + "home" + "/fixture/source.md\n")
        self.commit()
        base = self.git("rev-parse", "HEAD").strip()
        (self.root / "research/current.txt").write_text("Current source is repository-relative.\n")
        self.commit()
        public_path_portability(base, self.root)


if __name__ == "__main__":
    unittest.main()
