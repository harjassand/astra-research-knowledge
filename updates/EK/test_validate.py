"""Negative evidence guards; no archived scientific program is imported or run."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('ek_validate', Path(__file__).with_name('validate.py'))
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


class EvidenceGuards(unittest.TestCase):
    def setUp(self):
        self.manifest = intake.load('updates/EK/SOURCE_MANIFEST.json')
        self.mapping = intake.load('updates/EK/CLAIMS.json')
        self.trace = intake.load(self.mapping['claims'][0]['workflow_trace'])
        self.status = intake.load('frontier/cards/'+self.mapping['claims'][0]['id']+'.json')

    def test_original_pr_bytes_and_member_hashes(self):
        intake.check_sources(self.manifest)
        self.manifest['originals'][0]['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'bytes'):
            intake.check_sources(self.manifest)

    def test_unique_launches_do_not_supply_turn_count(self):
        intake.check_trace(self.trace, self.manifest)
        self.manifest['reported_team']['follow_up_and_retry_turn_count'] = 20
        with self.assertRaisesRegex(ValueError, 'conflated'):
            intake.check_trace(self.trace, self.manifest)

    def test_unique_launches_do_not_supply_peak_concurrency(self):
        self.trace['resources']['usage']['parallel_workers'] = 20
        with self.assertRaisesRegex(ValueError, 'inferred'):
            intake.check_trace(self.trace, self.manifest)

    def test_launch_timestamps_do_not_supply_inference_seconds(self):
        self.trace['resources']['reported_inference_seconds'] = 100
        with self.assertRaisesRegex(ValueError, 'inferred'):
            intake.check_trace(self.trace, self.manifest)

    def test_mixed_worker_models_do_not_identify_root_backend(self):
        self.trace['model']['model_id'] = 'gpt-6.1-sol'
        with self.assertRaisesRegex(ValueError, 'inferred'):
            intake.check_trace(self.trace, self.manifest)

    def test_reconstructed_handoff_is_not_exact_prompt(self):
        self.trace['prompt_availability'] = 'exact'
        self.trace['prompt_ref_ids'] = ['session']
        with self.assertRaisesRegex(ValueError, 'prompt'):
            intake.check_trace(self.trace, self.manifest)

    def test_informed_internal_review_is_not_independent_receipt(self):
        self.trace['advance']['verification'] = 'independent_receipt'
        with self.assertRaisesRegex(ValueError, 'verification'):
            intake.check_trace(self.trace, self.manifest)

    def test_archival_checks_cannot_promote_scientific_status(self):
        intake.check_status(self.status)
        self.status['claim_status'] = 'externally_verified'
        with self.assertRaisesRegex(ValueError, 'promotion'):
            intake.check_status(self.status)

    def test_family_similarity_is_not_a_proof_dependency(self):
        self.status['depends_on'] = ['N729-cumulative-strain-double-commutator-growth-and-parabolic-closure']
        with self.assertRaisesRegex(ValueError, 'dependency'):
            intake.check_status(self.status)

    def test_open_mesh_question_cannot_become_proved_result(self):
        indexed = {x['original_relative_path']:x for x in self.manifest['originals']}
        intake.check_retained_gates(self.mapping, indexed)
        self.mapping['retained_source_only_claims'][0]['status'] = 'proved'
        with self.assertRaisesRegex(ValueError, 'promoted'):
            intake.check_retained_gates(self.mapping, indexed)


if __name__ == '__main__':
    unittest.main()
