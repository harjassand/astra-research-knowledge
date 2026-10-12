"""In-memory negative guards; never modifies or executes scientific originals."""
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('ej_validate', HERE/'validate.py')
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


class EvidenceGuards(unittest.TestCase):
    def setUp(self):
        self.manifest = intake.load('updates/EJ/SOURCE_MANIFEST.json')
        self.entries = intake.load('updates/EJ/CLAIMS.json')['claims']
        self.trace = intake.load(self.entries[0]['workflow_trace'])
        self.status = intake.load('frontier/cards/'+self.entries[2]['id']+'.json')

    def test_exact_source_bytes(self):
        intake.check_sources(self.manifest)
        self.manifest['originals'][0]['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'bytes/hash'):
            intake.check_sources(self.manifest)

    def test_no_silent_archive_member_omission(self):
        self.manifest['recovered_packages'][0]['members'].pop()
        with self.assertRaisesRegex(ValueError, 'identities'):
            intake.check_sources(self.manifest)

    def test_no_invented_producer_manifest(self):
        self.manifest['recovered_packages'][2]['producer_hashes_checked'] = 4
        with self.assertRaisesRegex(ValueError, 'manifest coverage'):
            intake.check_sources(self.manifest)

    def test_reported_duration_is_not_measured_usage(self):
        intake.check_trace(self.trace, 'N728')
        self.trace['resources']['usage']['wall_seconds'] = 2249
        with self.assertRaisesRegex(ValueError, 'telemetry'):
            intake.check_trace(self.trace, 'N728')

    def test_unmeasured_model_and_workers_remain_unknown(self):
        self.trace['resources']['worker_invocations'] = 0
        self.trace['model']['model_id'] = 'gpt-6.1-sol'
        with self.assertRaisesRegex(ValueError, 'telemetry'):
            intake.check_trace(self.trace, 'N728')

    def test_diagnostics_cannot_promote_science(self):
        intake.check_status(self.status)
        self.status['claim_status'] = 'externally_verified'
        with self.assertRaisesRegex(ValueError, 'promotion'):
            intake.check_status(self.status)

    def test_conditional_algorithm_cannot_drop_import(self):
        self.status['depends_on'] = []
        with self.assertRaisesRegex(ValueError, 'dependency'):
            intake.check_status(self.status)

    def test_import_does_not_apply_to_self_contained_transfer(self):
        self.status['depends_on'][0]['scope'] = 'All results require N726.'
        with self.assertRaisesRegex(ValueError, 'conditional import scope'):
            intake.check_status(self.status)

    def test_family_similarity_cannot_create_dependency(self):
        self.status['depends_on'].append({'target':'N719','scope':'contraction analogy'})
        with self.assertRaisesRegex(ValueError, 'dependency'):
            intake.check_status(self.status)

    def test_reciprocal_notice_cannot_be_omitted(self):
        self.manifest['reciprocal_continuation_notices'].pop()
        with self.assertRaisesRegex(ValueError, 'notice coverage'):
            intake.check_notices(self.manifest)


if __name__ == '__main__':
    unittest.main()
