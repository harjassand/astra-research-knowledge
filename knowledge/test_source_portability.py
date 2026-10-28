"""Guard actual source-corruption and original-overwrite failure modes."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from knowledge.source_portability import main, portable_source


def resource(*parts):
    """Synthetic locator assembled here; no real host/account path is saved."""
    return ("/" + "/".join(parts)).encode()


class SourcePortability(unittest.TestCase):
    def test_scientific_slash_phrases_and_relative_source_links_are_exact(self):
        original = (
            b"global coordinate/root theorem; gates/workspace polynomial;\r\n"
            b"product-fidelity/privately framed; discard/privately retain;\r\n"
            b'[{"path":"reviews/root_receipt.json","sha256":"123"},'
            b'{"path":"a/private_framed_checks.py"}]\r\n'
            b"/rooted /privately /workspace /root; alpha/root/subtree\r\n"
        )
        public, ledger = portable_source(original)
        self.assertEqual(public, original)
        self.assertEqual(ledger, [])

    def test_real_absolute_resources_change_without_touching_the_statement(self):
        original = (
            b"Cost gates/workspace grows with H.\r\n"
            b"Reviewer: `" + resource("workspace", "review", "audit.md") + b"`.\r\n"
            b"[proof](sandbox:" + resource("mnt", "data", "source", "PROOF.md") + b")\r\n"
            b'Output="' + resource("Users", "private-person", "Documents", "result.json") + b'"\r\n'
            b"relative: source/root/audit.md\r\n"
        )
        expected = (
            b"Cost gates/workspace grows with H.\r\n"
            b"Reviewer: `producer-workspace/audit.md`.\r\n"
            b"[proof](producer-workspace/PROOF.md)\r\n"
            b'Output="producer-workspace/result.json"\r\n'
            b"relative: source/root/audit.md\r\n"
        )
        public, ledger = portable_source(original)
        self.assertEqual(public, expected)
        self.assertEqual(len(ledger), 3)
        self.assertNotIn("private-person", json.dumps(ledger))
        self.assertEqual(ledger[0]["original_locator_sha256"],
                         hashlib.sha256(resource("workspace", "review", "audit.md")).hexdigest())
        self.assertEqual(portable_source(public), (public, []))

    def test_binary_requires_explicit_other_evidence_route(self):
        with self.assertRaises(UnicodeDecodeError):
            portable_source(b"\xff\x00")

    def test_cli_preserves_original_and_refuses_existing_or_same_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root / "raw.md", root / "public.md"
            original = (b"Accepted coordinate/root statement.\n"
                        + resource("workspace", "run", "proof.md") + b"\n")
            source.write_bytes(original)
            with contextlib.redirect_stdout(io.StringIO()) as result:
                self.assertEqual(main([str(source), str(output)]), 0)
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(json.loads(result.getvalue())["original_sha256"],
                             hashlib.sha256(original).hexdigest())
            saved = output.read_bytes()
            for destination in (source, output):
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    main([str(source), str(destination)])
            self.assertEqual(source.read_bytes(), original)
            self.assertEqual(output.read_bytes(), saved)


if __name__ == "__main__":
    unittest.main()
