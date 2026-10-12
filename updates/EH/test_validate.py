"""Negative evidence guards; mutations are in-memory, never in archived sources."""
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('eh_validate',HERE/'validate.py')
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


class EvidenceGuards(unittest.TestCase):
    def setUp(self):
        self.manifest = intake.load('updates/EH/SOURCE_MANIFEST.json')
        entry = intake.load('updates/EH/CLAIMS.json')['claims'][0]
        self.trace = intake.load(entry['workflow_trace'])
        self.status = intake.load('frontier/cards/'+entry['id']+'.json')

    def test_exact_source_identity(self):
        intake.check_sources(self.manifest)
        self.manifest['originals'][0]['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError,'bytes/hash'):
            intake.check_sources(self.manifest)

    def test_zip_members_cannot_be_silently_omitted(self):
        self.manifest['recovered_packages'][0]['members'].pop()
        with self.assertRaisesRegex(ValueError,'identities'):
            intake.check_sources(self.manifest)

    def test_duration_is_not_usage(self):
        intake.check_trace(self.trace,'N724')
        self.trace['resources']['usage']['wall_seconds'] = 2240
        with self.assertRaisesRegex(ValueError,'telemetry'):
            intake.check_trace(self.trace,'N724')

    def test_worker_and_model_configuration_remain_unknown(self):
        self.trace['resources']['worker_invocations'] = 0
        self.trace['model']['model_id'] = 'gpt-6.1-sol'
        with self.assertRaisesRegex(ValueError,'telemetry'):
            intake.check_trace(self.trace,'N724')

    def test_producer_diagnostics_cannot_promote_science(self):
        intake.check_status(self.status)
        self.status['claim_status'] = 'externally_verified'
        with self.assertRaisesRegex(ValueError,'promotion'):
            intake.check_status(self.status)

    def test_family_similarity_cannot_create_a_proof_dependency(self):
        self.status['depends_on'].append({'target':'N725','scope':'same horizon formula'})
        with self.assertRaisesRegex(ValueError,'dependency'):
            intake.check_status(self.status)


if __name__ == '__main__':
    unittest.main()
