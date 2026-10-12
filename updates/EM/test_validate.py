"""Negative evidence guards; scientific originals are never modified or executed."""
import copy
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('em_validate', HERE/'validate.py')
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


class EvidenceGuards(unittest.TestCase):
    def setUp(self):
        self.manifest = intake.load('updates/EM/SOURCE_MANIFEST.json')
        self.entries = intake.load('updates/EM/CLAIMS.json')['claims']
        self.trace = intake.load(self.entries[0]['workflow_trace'])
        self.status = intake.load('frontier/cards/'+self.entries[2]['id']+'.json')

    def test_exact_source_bytes(self):
        intake.check_sources(self.manifest)
        self.manifest['originals'][0]['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'bytes/hash'):
            intake.check_sources(self.manifest)

    def test_archive_member_omission(self):
        self.manifest['recovered_packages'][0]['members'].pop()
        with self.assertRaisesRegex(ValueError, 'identities'):
            intake.check_sources(self.manifest)

    def test_producer_hash_coverage(self):
        self.manifest['recovered_packages'][2]['producer_hashes_checked'] = 0
        with self.assertRaisesRegex(ValueError, 'manifest coverage'):
            intake.check_sources(self.manifest)

    def test_integrity_does_not_establish_reproduction(self):
        self.manifest['recovered_packages'][0]['verification']['scientific_code_execution'] = 'PASS'
        with self.assertRaisesRegex(ValueError, 'scientific replay'):
            intake.check_sources(self.manifest)

    def test_reported_duration_not_measured_usage(self):
        intake.check_trace(self.trace, 'N739')
        self.trace['resources']['usage']['wall_seconds'] = 2979
        with self.assertRaisesRegex(ValueError, 'telemetry'):
            intake.check_trace(self.trace, 'N739')

    def test_unknown_model_workers(self):
        self.trace['resources']['worker_invocations'] = 0
        self.trace['model']['model_id'] = 'gpt-6.1-sol'
        with self.assertRaisesRegex(ValueError, 'telemetry'):
            intake.check_trace(self.trace, 'N739')

    def test_no_scientific_promotion(self):
        intake.check_status(self.status)
        self.status['claim_status'] = 'externally_verified'
        with self.assertRaisesRegex(ValueError, 'promotion'):
            intake.check_status(self.status)

    def test_import_cannot_be_erased(self):
        self.status['depends_on'] = []
        with self.assertRaisesRegex(ValueError, 'dependency'):
            intake.check_status(self.status)

    def test_no_topical_dependency(self):
        self.status['depends_on'].append({'target':'N730','scope':'both use Gaussian integration'})
        with self.assertRaisesRegex(ValueError, 'dependency'):
            intake.check_status(self.status)

    def test_notice_cannot_be_omitted(self):
        self.manifest['reciprocal_continuation_notices'].pop()
        with self.assertRaisesRegex(ValueError, 'notice coverage'):
            intake.check_notices(self.manifest)

    def test_q4_remains_open(self):
        gate = next(g for g in intake.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EM-N740-Q4')
        intake.check_q4(gate)
        gate['status'] = 'proved'
        with self.assertRaisesRegex(ValueError, 'unproved gate'):
            intake.check_q4(gate)

    def test_notice_does_not_license_older_math_edits(self):
        notice = next(n for n in intake.rows('agent/SEMANTIC_NOTICES.jsonl') if n['notice_id'].startswith('SN-EM-'))
        old = intake.git('show',intake.BASE+':frontier/dossiers/N728.txt').decode()
        new = (intake.ROOT/'frontier/dossiers/N728.txt').read_text()
        old_connection = __import__('json').loads(intake.git('show',intake.BASE+':frontier/connections/N728.json'))
        connection = intake.load('frontier/connections/N728.json')
        intake.check_projection(old,new,old_connection,connection,notice)
        with self.assertRaisesRegex(ValueError, 'historical dossier'):
            intake.check_projection(old,new+'Invented proof claim\n',old_connection,connection,notice)
        mutated = copy.deepcopy(connection)
        mutated['edges'][0]['composition'] = 'Changed historical proof interface'
        with self.assertRaisesRegex(ValueError, 'historical connection'):
            intake.check_projection(old,new,old_connection,mutated,notice)


if __name__ == '__main__':
    unittest.main()
