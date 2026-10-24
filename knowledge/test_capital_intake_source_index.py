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


def current_unit_entries():
    records = (json.loads(line) for line in (ROOT / "knowledge/current/records.jsonl").read_text().splitlines())
    return [
        (record, ROOT / record["authority"])
        for record in records
        if record.get("authority", "").startswith("knowledge/units/")
    ]


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
        ]
        inputs.extend(Path(record["authority"]) for record, _ in current_unit_entries())
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

    def test_scoped_current_unit_acceptance_has_exact_version_overlay(self):
        for record, authority in current_unit_entries():
            unit = json.loads(authority.read_text())
            self.assertEqual(unit["id"], record["id"])
            self.assertEqual(unit["version"], record["version"])
            overlays = record.get("review_overlays", [])
            for overlay in overlays:
                self.assertTrue(any(
                    subject["id"] == record["id"] and subject["content_version"] == record["content_version"]
                    for subject in overlay.get("subjects", [])
                ), f"stale review overlay applied to {record['id']}")
            if unit.get("review", {}).get("acceptance") == "extracted_with_version_bound_scoped_acceptance":
                self.assertTrue(any(
                    overlay.get("decision") == "accepted_internally_verified"
                    and any(subject["id"] == record["id"] and subject["content_version"] == record["content_version"]
                            for subject in overlay.get("subjects", []))
                    for overlay in overlays
                ), f"scoped acceptance is not bound to current version of {record['id']}")

    def test_receiving_contract_separates_conditional_baseline_from_c_one_exception(self):
        target_ids = {"U675-saturated-reference-filter", "U966-conditional-sld-order-interface"}
        units = [json.loads(path.read_text()) for record, path in current_unit_entries() if record["id"] in target_ids]
        self.assertEqual({unit["id"] for unit in units}, target_ids)
        for unit in units:
            text = " ".join(unit["contract"]["assumptions"] + [unit["body"], unit["contract"]["obstruction"]])
            self.assertIn("different reference marginals", text)
            self.assertIn("c=1", text)
            self.assertIn("does not make the reference marginals equal", text.lower())
        aliases = json.loads((ROOT / "indexes/query_aliases.json").read_text())
        n675_alias = aliases["N675-complete-quantum-channel-information-order-undecidability"].lower()
        self.assertNotIn("compare quantum measurements by relative entropy for every pair of input states", n675_alias)
        self.assertIn("complete relative entropy order for all input state pairs", n675_alias)


if __name__ == "__main__":
    unittest.main()
