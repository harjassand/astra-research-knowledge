"""Adversarial synthetic contract fixtures; no scientific or model evaluation."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from technology.contracts import check_ref, history, immutable, load, public_record, shape, stored_path
from technology.validate import ROOT, SCHEMA_PATH, paths, route, routes, validate


class TechnologyTests(unittest.TestCase):
    def setUp(self):
        self.record = load(ROOT / "technology/fixtures/contraction/record.json")

    def synthetic_independent(self, kind, environment="software", plan="independent-test"):
        item = copy.deepcopy(self.record["evidence"][1])
        item.update(id="synthetic-independent", kind=kind, environment=environment, experiment_id=plan,
                    observations=[{"quantity": "fixture error", "value": 0.0625, "unit": "dimensionless",
                                   "uncertainty": 0, "conditions": "synthetic test data only"}])
        item["independence"] = {"attested": True, "relationship": "synthetic receipt only", "basis_ref_ids": ["mechanism"]}
        self.record["evidence"].append(item)
        return item

    def test_fixture_stops_at_simulation_with_both_handoff_directions(self):
        result = validate(self.record)
        self.assertEqual(result["stage"], "simulation")
        self.assertFalse(result["scientific_truth_checked"])
        self.assertEqual({h["direction"] for h in self.record["handoffs"]}, {"forward", "reverse"})

    def test_lean_lead_needs_no_engineering_dossier(self):
        lead = load(ROOT / "technology/templates/LEAD.json")
        self.assertEqual(validate(lead)["stage"], "opportunity")
        self.assertNotIn("contract", lead)

    def test_stage_cannot_skip_independent_experiment(self):
        self.record["stage"] = "prototype"
        with self.assertRaisesRegex(ValueError, "unmet prior stage: experiment"):
            validate(self.record)

    def test_producer_simulation_cannot_be_renamed_as_measurement(self):
        self.record["evidence"][1]["kind"] = "experimental_measurement"
        with self.assertRaisesRegex(ValueError, "independent evidence"):
            validate(self.record)

    def test_attested_simulation_cannot_be_physical_measurement(self):
        self.synthetic_independent("experimental_measurement", "physical", "toy")
        with self.assertRaisesRegex(ValueError, "simulation cannot become"):
            validate(self.record)

    def test_reproduced_simulation_does_not_close_physical_experiment(self):
        self.record.update(domain="physical", stage="experiment")
        self.synthetic_independent("reproduced_simulation", plan="toy")
        self.record["gates"][-1].update(decision="passed", evidence_ids=["synthetic-independent"])
        with self.assertRaisesRegex(ValueError, "required evidence kind/result"):
            validate(self.record)

    def test_software_benchmark_does_not_validate_physical_device(self):
        self.record.update(domain="physical", stage="experiment")
        self.synthetic_independent("independent_computational_test")
        self.record["gates"][-1].update(decision="passed", evidence_ids=["synthetic-independent"])
        with self.assertRaisesRegex(ValueError, "required evidence kind/result"):
            validate(self.record)

    def test_scoped_software_benchmark_receipt_can_close_software_experiment(self):
        self.record["stage"] = "experiment"
        self.synthetic_independent("independent_computational_test")
        self.record["gates"][-1].update(decision="passed", evidence_ids=["synthetic-independent"])
        self.assertEqual(validate(self.record)["stage"], "experiment")

    def test_benchmark_is_not_a_validated_prototype(self):
        self.record["stage"] = "prototype"
        self.synthetic_independent("independent_computational_test")
        self.record["gates"][-1].update(decision="passed", evidence_ids=["synthetic-independent"])
        self.record["gates"].append({"stage": "prototype", "decision": "passed", "evidence_ids": ["synthetic-independent"],
                                     "rationale": "Synthetic invalid promotion"})
        with self.assertRaisesRegex(ValueError, "required evidence kind/result: prototype"):
            validate(self.record)

    def test_system_demonstration_requires_a_system_plan_and_scaling_assessment(self):
        item = self.synthetic_independent("demonstrated_system")
        with self.assertRaisesRegex(ValueError, "system demonstration plan"):
            validate(self.record)
        self.record["experiments"][1]["kind"] = "system"
        validate(self.record)  # Evidence can exist without promoting the completed stage.
        item["observations"] = []
        with self.assertRaises(ValueError):
            validate(self.record)

    def test_failed_and_unknown_evidence_cannot_pass_a_gate(self):
        for result in ("failed", "unknown"):
            with self.subTest(result=result):
                self.record["evidence"][1]["result"] = result
                with self.assertRaisesRegex(ValueError, "required evidence kind/result"):
                    validate(self.record)

    def test_independent_observations_need_units_and_uncertainty(self):
        item = self.synthetic_independent("independent_computational_test")
        del item["observations"][0]["uncertainty"]
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            validate(self.record)

    def test_undocumented_passed_future_gate_is_rejected(self):
        self.synthetic_independent("independent_computational_test")
        self.record["gates"][-1].update(decision="passed", evidence_ids=["synthetic-independent"])
        with self.assertRaisesRegex(ValueError, "exceeds completed stage"):
            validate(self.record)

    def test_transfer_states_preserve_missing_and_proof_obligations(self):
        bridge = self.record["bridges"][0]
        bridge["missing_operations"] = []
        with self.assertRaisesRegex(ValueError, "missing operations"):
            validate(self.record)
        bridge["state"] = "PROVEN LOGICAL DEPENDENCY"
        with self.assertRaisesRegex(ValueError, "proof references"):
            validate(self.record)

    def test_unknown_source_gate_and_dangling_local_ids_are_rejected(self):
        self.record["bridges"][0]["source_gate_ids"] = ["G-NOT-A-REAL-GATE"]
        with self.assertRaisesRegex(ValueError, "source proof gates"):
            validate(self.record)
        self.record["bridges"][0]["source_gate_ids"] = []
        self.record["gates"][0]["evidence_ids"] = ["missing-evidence"]
        with self.assertRaisesRegex(ValueError, "unresolved/duplicate"):
            validate(self.record)

    def test_hash_and_line_range_and_revision_integrity(self):
        ref = copy.deepcopy(self.record["refs"][0])
        ref["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            check_ref(ROOT, ref)
        ref = copy.deepcopy(self.record["refs"][0])
        ref["lines"] = [1, 100000]
        with self.assertRaisesRegex(ValueError, "invalid reference lines"):
            check_ref(ROOT, ref)
        ref["lines"] = None
        ref["source_revision"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "revision/hash mismatch"):
            check_ref(ROOT, ref)

    def test_external_and_symlink_references_are_rejected(self):
        ref = copy.deepcopy(self.record["refs"][0])
        for path in ("../outside.txt", "/etc/hosts"):
            ref["path"] = path
            with self.assertRaises(ValueError):
                check_ref(ROOT, ref)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outside-link").symlink_to(ROOT / self.record["refs"][0]["path"])
            ref["path"] = "outside-link"
            with self.assertRaisesRegex(ValueError, "unsafe"):
                check_ref(root, ref)
            with self.assertRaisesRegex(ValueError, "external/symlink escape"):
                public_record(root, root / "outside-link")

    def test_abandonment_requires_evidenced_narrow_failure(self):
        self.record["disposition"] = "abandoned"
        with self.assertRaisesRegex(ValueError, "scoped, evidenced failure"):
            validate(self.record)
        self.record["failures"] = [{"attempt": "Beat the equally informed control in this toy",
            "failure_scope": "Exact toy update counts tie; no universal impossibility", "ref_ids": ["result"]}]
        self.assertEqual(validate(self.record)["stage"], "simulation")

    def test_no_confidential_record_or_arbitrary_score_fields(self):
        self.record["disclosure"] = "confidential"
        with self.assertRaisesRegex(ValueError, "expected public"):
            validate(self.record)
        self.record["disclosure"] = "public"
        self.record["assessment"]["potential_significance"]["score"] = 100
        with self.assertRaisesRegex(ValueError, "unexpected fields"):
            validate(self.record)

    def test_nonfinite_boolean_numeric_and_duplicate_json_keys_rejected(self):
        for value in (True, float("inf")):
            with self.subTest(value=value):
                self.record["capability"]["target"]["baseline"] = value
                with self.assertRaises(ValueError):
                    shape(self.record, load(SCHEMA_PATH))
        self.record["capability"]["target"]["baseline"] = 10 ** 1000
        shape(self.record, load(SCHEMA_PATH))  # Exact integers are finite; avoid float-overflow coercion.
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "duplicate.json"
            p.write_text('{"id": 1, "id": 2}')
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                load(p)

    def test_routes_exclude_fixtures_and_are_bounded(self):
        fixture = ROOT / "technology/fixtures/contraction/record.json"
        self.assertNotIn(fixture, paths(ROOT))
        self.assertIn(fixture, paths(ROOT, fixtures=True))
        self.assertTrue(all(not row["fixture"] for row in route()["routes"]))
        self.assertTrue(any(row["id"] == "T-fixture-contraction" for row in
                            route(fixtures=True, role="theoretical-pro", limit=10000)["routes"]))
        self.assertEqual(route(fixtures=True, limit=0)["routes"], [])
        with self.assertRaisesRegex(ValueError, "non-negative"):
            route(limit=-1)

    def test_current_route_does_not_resurrect_removed_historical_link(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            names = ["technology/routes.tsv", "frontier/CURRENT_CLAIM_STATUS.jsonl", "frontier/OPEN_PROOF_GATES.jsonl"]
            names += [ref["path"] for ref in self.record["refs"]]
            names += [r["entry_point"] for r in routes(ROOT).values()]
            for name in set(names):
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, root / name)
            self.record["fixture"] = False
            self.record["bridges"][0]["source_card_ids"] = ["N654"]
            store = root / "technology/records" / self.record["id"]
            store.mkdir(parents=True)
            old = store / "v0001.json"
            old.write_text(json.dumps(self.record))
            self.assertEqual(route(root, card="N654-dark-oxygen-conditional-faradaic-energy-budget")["matching_records"], 1)
            self.record["version"] = 2
            self.record["previous"] = {"id": "previous", "path": old.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(old.read_bytes()).hexdigest(), "lines": None,
                "source_revision": None, "source_id": None, "status": "Synthetic ancestry fixture"}
            self.record["bridges"][0]["source_card_ids"] = []
            (store / "v0002.json").write_text(json.dumps(self.record))
            self.assertEqual(route(root, card="N654")["routes"], [])
            self.assertEqual(route(root)["routes"][0]["version"], 2)
            self.record["version"] = 3
            with self.assertRaisesRegex(ValueError, "invalid version ancestry"):
                history(root, self.record, "technology/records")

    def test_baseline_rejects_committed_and_working_record_edits(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.DEVNULL, text=True).strip()
            git("init")
            path = root / "technology/records/T-fixture/v0001.json"
            path.parent.mkdir(parents=True)
            path.write_text("{}")
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "synthetic baseline")
            base = git("rev-parse", "HEAD")
            patterns = [":(glob)technology/records/**/*.json"]
            immutable(root, base, patterns)
            path.write_text('{"changed": true}')
            with self.assertRaisesRegex(ValueError, "immutable record changed"):
                immutable(root, base, patterns)
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "synthetic tamper")
            with self.assertRaisesRegex(ValueError, "immutable record changed"):
                immutable(root, base, patterns)

    def test_fixture_and_unfilled_template_cannot_enter_live_store(self):
        path = ROOT / "technology/records/T-fixture-contraction/v0001.json"
        with self.assertRaisesRegex(ValueError, "fixtures cannot enter"):
            stored_path(path, ROOT, self.record, "technology/records")
        lead = load(ROOT / "technology/templates/LEAD.json")
        with self.assertRaisesRegex(ValueError, "template placeholders"):
            stored_path(ROOT / "technology/records/T-replace/v0001.json", ROOT, lead, "technology/records")


if __name__ == "__main__":
    unittest.main()
