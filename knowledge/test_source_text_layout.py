"""A corrected current JSON projection must not rewrite historical source bytes."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from knowledge.mcp_adapter import ResearchAdapter, INLINE_SOURCE_CONTEXT
from knowledge.model import (LEGACY_SOURCE_TEXT, TYPED_SOURCE_TEXT, digest, encoded,
                             scientific_text, source_text_layout)

class SourceTextLayoutTests(unittest.TestCase):
    def setUp(self):
        self.space = tempfile.TemporaryDirectory()
        self.addCleanup(self.space.cleanup)
        self.root = Path(self.space.name)

    def test_old_generic_cells_payload_is_byte_exact_after_reader_upgrade(self):
        raw = b'{"cells":[{"radius":"1/2"}],"condition":"Require known Gaussian cell masses"}\n'
        (self.root / "detector.json").write_bytes(raw)
        ref = {"path": "detector.json", "sha256": digest(raw), "lines": [1, 1]}
        a = ResearchAdapter.__new__(ResearchAdapter)
        a.root, a.paths, a.revision = self.root, {"detector.json"}, "f" * 40
        a.version, a.source_context_layout = "a" * 64, INLINE_SOURCE_CONTEXT
        a.library = SimpleNamespace(records={})
        a.contexts = {(ref["path"], ref["sha256"]): set()}
        a.locators, a.artifact_data = {}, {}
        expected = {
            "scope": "Exact declared source version. Current context notices remain applicable to reuse; coarchive and citation do not confer acceptance. A historical unit document retains its historical status and does not inherit the current review.",
            "source": ref, "text_selection": "notebook cell sources; outputs not indexed",
            "text": "", "citation_locator": a.source_locator(ref),
            "current_context": [], "full_source_url": a.source_url(ref),
            "extracted_text_lines": [1, 1]}
        self.assertEqual(encoded(a.source_payload(ref)), encoded(expected))
        a.source_text_layout = TYPED_SOURCE_TEXT
        current = a.source_payload(ref)
        self.assertIn("Require known Gaussian cell masses", current["text"])
        self.assertEqual(current["source"], ref)
        a.source_text_layout = LEGACY_SOURCE_TEXT
        self.assertEqual(encoded(a.source_payload(ref)), encoded(expected))
        self.assertEqual((self.root / "detector.json").read_bytes(), raw)

    def test_notebook_sources_and_output_exclusion_match_both_versions(self):
        raw = json.dumps({"nbformat": 4, "cells": [
            {"cell_type": "markdown", "source": ["Retain this assumption."]},
            {"cell_type": "code", "source": "x=1", "outputs": ["saved output"]}]})
        old = scientific_text(raw, layout=LEGACY_SOURCE_TEXT)
        new = scientific_text(raw, layout=TYPED_SOURCE_TEXT)
        self.assertEqual(old, new)
        self.assertNotIn("saved output", new[0])

    def test_only_declared_hash_checked_marker_can_select_new_layout(self):
        name = "knowledge/current/release.json"
        path = self.root / name
        path.parent.mkdir(parents=True)
        path.write_bytes(encoded({"source_text_layout": TYPED_SOURCE_TEXT}))
        self.assertEqual(source_text_layout(self.root, {"outputs": {}}), LEGACY_SOURCE_TEXT)
        manifest = {"outputs": {name: digest(path.read_bytes())}}
        self.assertEqual(source_text_layout(self.root, manifest), TYPED_SOURCE_TEXT)
        path.write_bytes(encoded({"source_text_layout": "future-unsupported"}))
        with self.assertRaisesRegex(ValueError, "Stale source text"):
            source_text_layout(self.root, manifest)
        manifest["outputs"][name] = digest(path.read_bytes())
        with self.assertRaisesRegex(ValueError, "Unsupported source text"):
            source_text_layout(self.root, manifest)
        path.write_bytes(encoded({}))
        manifest["outputs"][name] = digest(path.read_bytes())
        self.assertEqual(source_text_layout(self.root, manifest), LEGACY_SOURCE_TEXT)

    def test_unknown_projection_never_silently_falls_back(self):
        with self.assertRaisesRegex(ValueError, "Unsupported source text"):
            scientific_text('{"condition":"retain"}', layout="future-unsupported")

if __name__ == "__main__":
    unittest.main()

