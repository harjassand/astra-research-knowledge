"""Behavioral publication tests with synthetic evidence; no scientific inference."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import publish_checkpoint as checkpoints
import publish_result as results


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "evidence.txt").write_text("Synthetic receipt only.\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                        "commit", "-qm", "synthetic base"], check=True)
        self.selection = {"checkpoint_id": "selected-result", "branch_id": "worker-fixture", "kind": "result",
                          "summary": "Synthetic result", "scope": "Fixture only; no scientific claim",
                          "evidence": [{"id": "receipt", "path": "evidence.txt", "status": "Synthetic receipt"}],
                          "limitations": ["Software fixture"], "next_step": "Inspect this fixture",
                          "disclosure": "already_public"}

    def test_defaults_do_not_promote_claim_and_no_draft_side_effects(self):
        before = (self.root / "evidence.txt").read_bytes()
        record = results.prepare(self.root, self.selection)
        self.assertTrue(all(v["state"] == "UNKNOWN" for v in record["publication"]["verification"].values()))
        self.assertEqual(record["work_progress"]["status"], "UNKNOWN")
        self.assertFalse((self.root / "state").exists())
        self.assertEqual((self.root / "evidence.txt").read_bytes(), before)

    def test_private_draft_is_rejected_before_writing(self):
        self.selection["disclosure"] = "private"
        record = results.prepare(self.root, self.selection)
        with self.assertRaisesRegex(ValueError, "private draft"):
            results.validate_publication(record)
        with self.assertRaisesRegex(ValueError, "private draft"):
            checkpoints.validate_record(record, self.root)
        with self.assertRaisesRegex(ValueError, "private draft"):
            checkpoints.publish(self.root, record, record["base_revision"], [])
        self.assertFalse((self.root / "state/checkpoints").exists())
        self.selection.pop("disclosure")
        with self.assertRaisesRegex(ValueError, "disclosure"):
            results.prepare(self.root, self.selection)

    def test_drafts_stay_ignored_or_external_and_never_overwrite(self):
        self.selection["disclosure"] = "private"
        record = results.prepare(self.root, self.selection)
        for target in (self.root / "updates/private-draft.json", self.root / "state/checkpoints/worker-fixture/draft.json",
                       self.root / ".astra-local"):
            with self.assertRaisesRegex(ValueError, "ignored .astra-local"):
                results.write_draft(self.root, record, target)
            self.assertFalse(target.exists())
        target = self.root / ".astra-local/review.json"
        results.write_draft(self.root, record, target)
        before = target.read_bytes()
        with self.assertRaises(FileExistsError):
            results.write_draft(self.root, record, target)
        self.assertEqual(before, target.read_bytes())

    def test_git_metadata_and_ignored_evidence_are_rejected(self):
        self.selection["evidence"][0]["path"] = ".git/config"
        with self.assertRaisesRegex(ValueError, "Git metadata"):
            results.prepare(self.root, self.selection)
        (self.root / ".gitignore").write_text(".astra-local/\n")
        (self.root / ".astra-local").mkdir()
        (self.root / ".astra-local/private.txt").write_text("Private fixture")
        self.selection["evidence"][0]["path"] = ".astra-local/private.txt"
        with self.assertRaisesRegex(ValueError, "ignored/private"):
            results.prepare(self.root, self.selection)

    def test_evidence_scoped_status_claims_require_receipts(self):
        claims = {
            "internal": {"state": "checked", "method": "proof", "scope": "Named synthetic lemma"},
            "independent": {"state": "verified", "method": "specialist review", "scope": "Named lemma", "verifier": "Fixture reviewer"},
            "experiment": {"state": "demonstrated", "method": "matched experiment", "scope": "Named output", "controls": "Matched fixture", "cost_boundary": "Complete fixture costs"},
        }
        for axis, entry in claims.items():
            with self.subTest(axis=axis):
                self.selection["verification"] = {axis: entry}
                with self.assertRaisesRegex(ValueError, "requires linked evidence"):
                    results.prepare(self.root, self.selection)
                entry["evidence_ref_ids"] = ["receipt"]
                record = results.prepare(self.root, self.selection)
                self.assertEqual(record["publication"]["verification"][axis]["state"], entry["state"])
                if axis == "internal":
                    self.assertIn("internal=checked (proof)", record["latest_substantive_result"]["scientific_status"])

    def test_experiment_requires_controls_costs_and_independent_verifier(self):
        self.selection["verification"] = {"experiment": {"state": "demonstrated", "method": "measurement",
                                             "scope": "Fixture", "evidence_ref_ids": ["receipt"]}}
        with self.assertRaisesRegex(ValueError, "controls"):
            results.prepare(self.root, self.selection)
        self.selection["verification"]["experiment"]["controls"] = "matched fixture"
        with self.assertRaisesRegex(ValueError, "cost_boundary"):
            results.prepare(self.root, self.selection)
        self.selection["verification"] = {"independent": {"state": "verified", "method": "review",
                                            "scope": "Fixture", "evidence_ref_ids": ["receipt"]}}
        with self.assertRaisesRegex(ValueError, "verifier"):
            results.prepare(self.root, self.selection)

    def test_correction_requires_exact_target_scope_and_preserves_original(self):
        self.selection["kind"] = "correction"
        with self.assertRaisesRegex(ValueError, "exact target"):
            results.prepare(self.root, self.selection)
        self.selection["relates_to"] = [{"path": "evidence.txt", "relation": "corrects", "scope": "Only the fixture label"}]
        before = (self.root / "evidence.txt").read_bytes()
        record = results.prepare(self.root, self.selection)
        results.validate_publication(record)
        checkpoints.publish(self.root, record, record["base_revision"], [])
        self.assertEqual(before, (self.root / "evidence.txt").read_bytes())
        self.assertEqual(record["publication"]["relates_to"][0]["path"], "evidence.txt")

    def test_stale_draft_parent_and_changed_evidence_rejected(self):
        first = results.prepare(self.root, self.selection)
        stale = copy.deepcopy(first)
        stale["checkpoint_id"] = "stale-result"
        checkpoints.publish(self.root, first, first["base_revision"], [])
        with self.assertRaisesRegex(ValueError, "stale branch"):
            checkpoints.publish(self.root, stale, stale["base_revision"], [])
        self.selection["checkpoint_id"] = "fresh-result"
        fresh = results.prepare(self.root, self.selection)
        self.assertEqual(fresh["parent_checkpoint_ids"], ["selected-result"])
        (self.root / "evidence.txt").write_text("Changed after draft review.\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            checkpoints.publish(self.root, fresh, fresh["base_revision"], fresh["parent_checkpoint_ids"])
        self.assertFalse((self.root / "state/checkpoints/worker-fixture/fresh-result.json").exists())

    def test_unknown_field_missing_evidence_and_status_tamper_rejected(self):
        self.selection["verificaton"] = {"internal": {"state": "checked"}}
        with self.assertRaisesRegex(ValueError, "unknown selection"):
            results.prepare(self.root, self.selection)
        self.selection.pop("verificaton")
        self.selection["evidence"][0]["path"] = "../outside.txt"
        with self.assertRaisesRegex(ValueError, "unsafe evidence"):
            results.prepare(self.root, self.selection)
        self.selection["evidence"][0]["path"] = "evidence.txt"
        record = results.prepare(self.root, self.selection)
        record["latest_substantive_result"]["scientific_status"] = "Independently verified"
        with self.assertRaisesRegex(ValueError, "must agree"):
            results.validate_publication(record)

    def test_all_meaningful_event_kinds_share_the_existing_record_format(self):
        for kind in ("result", "negative", "handoff"):
            with self.subTest(kind=kind):
                self.selection["kind"] = kind
                record = results.prepare(self.root, self.selection)
                self.assertEqual(record["schema"], checkpoints.SCHEMA)
                self.assertEqual(record["publication"]["kind"], kind)

    def test_practical_advantage_requires_matched_information_and_costs(self):
        entry = {"state": "demonstrated", "method": "matched test", "scope": "Fixture advantage",
                 "evidence_ref_ids": ["receipt"]}
        self.selection["verification"] = {"advantage": entry}
        for field, value in (("comparator", "Strongest equally informed fixture"),
                             ("information_boundary", "Same acquired inputs"), ("cost_boundary", "Full fixture costs")):
            with self.assertRaisesRegex(ValueError, field):
                results.prepare(self.root, self.selection)
            entry[field] = value
        record = results.prepare(self.root, self.selection)
        self.assertIn("advantage=demonstrated", record["latest_substantive_result"]["scientific_status"])

    def test_multiple_heads_cannot_be_silently_consumed(self):
        first = results.prepare(self.root, self.selection)
        checkpoints.publish(self.root, first, first["base_revision"], [])
        children = []
        for identifier in ("left", "right"):
            child = copy.deepcopy(first)
            child["checkpoint_id"] = identifier
            child["parent_checkpoint_ids"] = ["selected-result"]
            path = self.root / f"state/checkpoints/worker-fixture/{identifier}.json"
            path.write_text(checkpoints.canonical(child))
            children.append(path)
        self.selection["checkpoint_id"] = "reviewed-handoff"
        with self.assertRaisesRegex(ValueError, "conflicting heads"):
            results.prepare(self.root, self.selection)
        self.selection["kind"] = "handoff"
        self.selection["reconcile_parents"] = ["left", "right"]
        with self.assertRaisesRegex(ValueError, "every parent"):
            results.prepare(self.root, self.selection)
        self.selection["relates_to"] = [{"path": str(p.relative_to(self.root)), "relation": "handoff",
                                        "scope": "Retain this independent topic; activity UNKNOWN"} for p in children]
        record = results.prepare(self.root, self.selection)
        checkpoints.publish(self.root, record, record["base_revision"], ["left", "right"])
        rendered = (self.root / "state/branches/worker-fixture.txt").read_text()
        self.assertIn("history: left", rendered)
        self.assertIn("history: right", rendered)
        self.assertIn("current_activity: UNKNOWN", rendered)


if __name__ == "__main__":
    unittest.main()
