"""Evidence guards: isolated in-memory corruptions, no scientific script runs."""
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('eg_validate',HERE/'validate.py')
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


class EvidenceGuards(unittest.TestCase):
    def setUp(self):
        self.manifest = intake.load('updates/EG/SOURCE_MANIFEST.json')
        mapping = intake.load('updates/EG/CLAIMS.json')
        self.trace = intake.load(mapping['claims'][0]['workflow_trace'])
        self.status = intake.load('frontier/cards/'+mapping['claims'][0]['id']+'.json')

    def test_producer_member_identity(self):
        intake.check_sources(self.manifest)
        self.manifest['originals'][0]['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError,'bytes'):
            intake.check_sources(self.manifest)

    def test_worker_turns_are_not_unique_worker_count(self):
        intake.check_trace(self.trace,self.manifest)
        self.trace['resources']['worker_invocations'] = 4
        with self.assertRaisesRegex(ValueError,'conflated'):
            intake.check_trace(self.trace,self.manifest)

    def test_clock_span_is_not_inference_expenditure(self):
        self.trace['resources']['reported_inference_seconds'] = 2201
        with self.assertRaisesRegex(ValueError,'telemetry'):
            intake.check_trace(self.trace,self.manifest)

    def test_requested_worker_model_is_not_root_backend(self):
        self.trace['model']['model_id'] = 'gpt-6.1-sol'
        with self.assertRaisesRegex(ValueError,'telemetry'):
            intake.check_trace(self.trace,self.manifest)

    def test_internal_checks_cannot_promote_scientific_status(self):
        intake.check_status(self.status)
        self.status['claim_status'] = 'externally_verified'
        with self.assertRaisesRegex(ValueError,'promotion'):
            intake.check_status(self.status)

    def test_family_similarity_is_not_proof_dependency(self):
        self.status['depends_on'].append({'target':'N708-hidden-corridor-kinetic-acquisition-obstruction',
                                        'scope':'both have hidden channels'})
        with self.assertRaisesRegex(ValueError,'dependency'):
            intake.check_status(self.status)


if __name__ == '__main__':
    unittest.main()
