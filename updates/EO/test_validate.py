"""Negative evidence guards; scientific originals are never modified or executed."""
import copy
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('eo_validate', HERE/'validate.py')
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


class EvidenceGuards(unittest.TestCase):
    def setUp(self):
        self.manifest = intake.load('updates/EO/SOURCE_MANIFEST.json')
        self.entries = intake.load('updates/EO/CLAIMS.json')['claims']
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
        intake.check_trace(self.trace, 'N745')
        self.trace['resources']['usage']['wall_seconds'] = 2761
        with self.assertRaisesRegex(ValueError, 'telemetry'):
            intake.check_trace(self.trace, 'N745')

    def test_unknown_model_workers(self):
        self.trace['resources']['worker_invocations'] = 0
        self.trace['model']['model_id'] = 'gpt-6.1-sol'
        with self.assertRaisesRegex(ValueError, 'telemetry'):
            intake.check_trace(self.trace, 'N745')

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

    def test_reciprocal_notice_is_retrievable(self):
        intake.check_notices(self.manifest)

    def test_family_fit_keeps_exact_targets(self):
        fit = intake.load('updates/EO/FAMILY_FIT.json')
        intake.check_families(fit)
        fit['decisions'][0]['comparisons'].clear()
        with self.assertRaisesRegex(ValueError,'comparison scope'):
            intake.check_families(fit)

    def test_notice_cannot_be_omitted(self):
        self.manifest['reciprocal_continuation_notices'].pop()
        with self.assertRaisesRegex(ValueError, 'notice coverage'):
            intake.check_notices(self.manifest)

    def test_capability_gates_remain_open(self):
        for route in intake.EXPECTED:
            gate = next(g for g in intake.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EO-'+route+'-CAPABILITY')
            intake.check_capability_gate(gate,route)
            gate['status'] = 'proved'
            with self.assertRaisesRegex(ValueError, 'unproved capability gate'):
                intake.check_capability_gate(gate,route)

    def test_global_cancellation_obligation_cannot_be_erased(self):
        gate = self.gate('N745')
        gate['required_obligations'].remove('global_predicate_synthesis')
        with self.assertRaisesRegex(ValueError,'obligations erased'):
            intake.check_capability_gate(gate,'N745')

    def test_robust_rank_exponent_cannot_be_strengthened(self):
        gate = self.gate('N745')
        gate['validation_boundary'] = gate['validation_boundary'].replace('2^{Omega(sqrt(n))}','2^{Omega(n)}')
        with self.assertRaisesRegex(ValueError,'scientific boundary'):
            intake.check_capability_gate(gate,'N745')

    def test_unexecuted_upper_budget_is_not_a_lower_bound(self):
        gate = self.gate('N746')
        gate['validation_boundary'] = 'The runtime is necessarily 3.3106e23 calls.'
        with self.assertRaisesRegex(ValueError,'scientific boundary'):
            intake.check_capability_gate(gate,'N746')

    def test_stability_does_not_replace_correct_integral_anchor(self):
        gate = self.gate('N746')
        gate['required_obligations'].remove('correct_integral_anchor')
        with self.assertRaisesRegex(ValueError,'obligations erased'):
            intake.check_capability_gate(gate,'N746')

    def test_finite_ring_does_not_supply_thermodynamic_transfer(self):
        gate = self.gate('N747')
        gate['required_obligations'].remove('quantitative_finite_size_transfer')
        with self.assertRaisesRegex(ValueError,'obligations erased'):
            intake.check_capability_gate(gate,'N747')

    def test_ramsey_fixture_is_not_physical_validation(self):
        gate = self.gate('N747')
        gate['validation_boundary'] = gate['validation_boundary'].replace('synthetic','experimentally confirmed')
        with self.assertRaisesRegex(ValueError,'scientific boundary'):
            intake.check_capability_gate(gate,'N747')

    def gate(self,route):
        return next(g for g in intake.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-EO-'+route+'-CAPABILITY')

    def test_notice_does_not_license_older_math_edits(self):
        notice = next(n for n in intake.rows('agent/SEMANTIC_NOTICES.jsonl') if n['notice_id'].startswith('SN-EO-'))
        old = intake.git('show',intake.BASE+':frontier/dossiers/N742.txt').decode()
        new = (intake.ROOT/'frontier/dossiers/N742.txt').read_text()
        old_connection = __import__('json').loads(intake.git('show',intake.BASE+':frontier/connections/N742.json'))
        connection = intake.load('frontier/connections/N742.json')
        intake.check_projection(old,new,old_connection,connection,notice)
        with self.assertRaisesRegex(ValueError, 'historical dossier'):
            intake.check_projection(old,new+'Invented proof claim\n',old_connection,connection,notice)
        mutated = copy.deepcopy(connection)
        mutated['edges'][0]['composition'] = 'Changed historical proof interface'
        with self.assertRaisesRegex(ValueError, 'historical connection'):
            intake.check_projection(old,new,old_connection,mutated,notice)


if __name__ == '__main__':
    unittest.main()
