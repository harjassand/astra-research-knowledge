"""Regressions for the byte-preserving, extension-qualified Capital intake index."""
import hashlib
import json
from pathlib import Path
import unittest

from knowledge.model import ROOT


UPDATE = Path("research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-25-dots-ultra-selected-sources")
INDEX_PATH = UPDATE / "source/INDEX.json"


def indexed_row(rows, path):
    return next((row for row in rows if path == row["path"] or path.endswith("/" + row["path"])), None)


def walk_references(value):
    if isinstance(value, dict):
        path = value.get("path")
        if not isinstance(path, str):
            path = value.get("read_path")
        if isinstance(path, str):
            yield value, path
        for child in value.values():
            yield from walk_references(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_references(child)


class CapitalIntakeSourceIndex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads((ROOT / INDEX_PATH).read_text())
        cls.rows = cls.index["files"]

    def test_all_documents_have_unique_extension_ids_and_explicit_families(self):
        self.assertEqual(len(self.rows), 50)
        source_ids = [row["source_id"] for row in self.rows]
        self.assertEqual(len(source_ids), len(set(source_ids)))
        families = {}
        for row in self.rows:
            suffix = Path(row["path"]).suffix.lstrip(".").lower()
            self.assertTrue(row["source_id"].endswith("-" + suffix), row["path"])
            self.assertIn("family_id", row)
            self.assertNotEqual(row["family_id"], row["source_id"])
            families.setdefault(row["family_id"], []).append(row)
        for family_id, members in families.items():
            self.assertTrue(all(row["family_id"] == family_id for row in members))
            self.assertEqual(len({row["source_id"] for row in members}), len(members))

    def test_frozen_original_source_bytes_still_match_index(self):
        for row in self.rows:
            with self.subTest(path=row["path"]):
                data = (ROOT / UPDATE / row["path"]).read_bytes()
                self.assertEqual(len(data), row["bytes"])
                self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])

    def test_current_document_references_resolve_by_exact_path(self):
        inputs = [
            Path("indexes/claims.d/2026-10-25-dots-ultra.jsonl"),
            Path("frontier/CURRENT_CLAIM_STATUS.d/2026-10-25-dots-ultra.jsonl"),
            Path("agent/SEMANTIC_NOTICES.d/2026-10-25-dots-ultra.jsonl"),
            Path("knowledge/units/U675-saturated-reference-filter/v0002.json"),
            Path("knowledge/units/U966-conditional-sld-order-interface/v0002.json"),
        ]
        status_shard = ROOT / inputs[1]
        for line in status_shard.read_text().splitlines():
            status = json.loads(line)
            inputs.append(Path("frontier/cards") / (status["card_id"] + ".json"))

        for relative in inputs:
            path = ROOT / relative
            objects = [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.suffix == ".jsonl" else [json.loads(path.read_text())]
            for obj in objects:
                for reference, source_path in walk_references(obj):
                    row = indexed_row(self.rows, source_path)
                    if row is None:
                        continue
                    if "source_id" in reference:
                        self.assertEqual(reference["source_id"], row["source_id"], f"{relative}: {source_path}")
                    if str(reference.get("id", "")).startswith("src-"):
                        self.assertEqual(reference["id"], row["source_id"], f"{relative}: {source_path}")

        claims = [json.loads(line) for line in (ROOT / inputs[0]).read_text().splitlines() if line.strip()]
        for claim in claims:
            paths = claim.get("source_paths", [])
            ids = claim.get("source_ids", [])
            self.assertEqual(len(ids), len(paths), claim["id"])
            for source_id, source_path in zip(ids, paths):
                row = indexed_row(self.rows, source_path)
                self.assertIsNotNone(row, f"{claim['id']}: {source_path}")
                self.assertEqual(source_id, row["source_id"], f"{claim['id']}: {source_path}")

    def test_a966_review_binds_exact_current_unit_versions(self):
        review = json.loads((ROOT / "knowledge/reviews/A966-filter-unit-receiving-use-20261025.json").read_text())
        subjects = {subject["id"]: subject["content_version"] for subject in review["subjects"]}
        current = {record["id"]: record for record in (
            json.loads(line) for line in (ROOT / "knowledge/current/records.jsonl").read_text().splitlines()
        )}
        for unit_id in ("U675-saturated-reference-filter", "U966-conditional-sld-order-interface"):
            self.assertEqual(subjects[unit_id], current[unit_id]["content_version"])
            self.assertTrue(any(item["id"] == review["id"] for item in current[unit_id]["review_overlays"]))


if __name__ == "__main__":
    unittest.main()
