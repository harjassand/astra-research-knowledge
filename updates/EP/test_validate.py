"""Negative evidence guards; scientific originals are never modified or executed."""
import copy
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('ep_validate', HERE/'validate.py')
intake = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


class EvidenceGuards(unittest.TestCase):
    def setUp(self):
        self.manifest = intake.load('updates/EP/SOURCE_MANIFEST.json')
        self.entries = intake.load('updates/EP/CLAIMS.json')['claims']
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

    def test_binary_input_hash_cannot_be_replaced(self):
        binary = next(m for p in self.manifest['recovered_packages'] for m in p['members'] if m['path'].endswith('.npz'))
        self.assertNotIn('lines',binary)
        binary['sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError,'bytes/hash'):
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
        intake.check_trace(self.trace, 'N748')
        self.trace['resources']['usage']['wall_seconds'] = 3610
        with self.assertRaisesRegex(ValueError, 'telemetry'):
            intake.check_trace(self.trace, 'N748')

    def test_unknown_model_workers(self):
        self.trace['resources']['worker_invocations'] = 0
        self.trace['model']['model_id'] = 'gpt-6.1-sol'
        with self.assertRaisesRegex(ValueError, 'telemetry'):
            intake.check_trace(self.trace, 'N748')

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
        fit = intake.load('updates/EP/FAMILY_FIT.json')
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
            gate = next(g for g in intake.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id'] == 'G-EP-'+route+'-CAPABILITY')
            intake.check_capability_gate(gate,route)
            gate['status'] = 'proved'
            with self.assertRaisesRegex(ValueError, 'unproved capability gate'):
                intake.check_capability_gate(gate,route)

    def test_scalar_is_not_rational_G1(self):
        gate = self.gate('N748')
        gate['validation_boundary'] = gate['validation_boundary'].replace('literal G1 remains open','literal G1 proved')
        with self.assertRaisesRegex(ValueError,'scientific boundary'):
            intake.check_capability_gate(gate,'N748')

    def test_unexecuted_transport_budget_is_not_lower_bound(self):
        gate = self.gate('N748')
        gate['validation_boundary'] = 'Runtime necessarily exceeds1e74 samples.'
        with self.assertRaisesRegex(ValueError,'scientific boundary'):
            intake.check_capability_gate(gate,'N748')

    def test_finite_size_gate_cannot_be_erased(self):
        gate = self.gate('N748')
        gate['required_obligations'].remove('quantitative_thermodynamic_transfer')
        with self.assertRaisesRegex(ValueError,'obligations erased'):
            intake.check_capability_gate(gate,'N748')

    def test_existing_rounding_classification_is_retained(self):
        gate = self.gate('N749')
        gate['validation_boundary'] = gate['validation_boundary'].replace('N689 already records','This is the first')
        with self.assertRaisesRegex(ValueError,'scientific boundary'):
            intake.check_capability_gate(gate,'N749')

    def test_existential_support_is_not_an_algorithm(self):
        gate = self.gate('N749')
        gate['required_obligations'].remove('polynomial_bit_face_and_barrier_access')
        with self.assertRaisesRegex(ValueError,'obligations erased'):
            intake.check_capability_gate(gate,'N749')

    def test_heat_boundary_is_not_holomorphic_disk(self):
        gate = self.gate('N750')
        gate['validation_boundary'] = gate['validation_boundary'].replace('one-sided continuation','holomorphic disk')
        with self.assertRaisesRegex(ValueError,'scientific boundary'):
            intake.check_capability_gate(gate,'N750')

    def test_selection_event_cannot_be_dropped(self):
        gate = self.gate('N750')
        gate['required_obligations'].remove('selection_event_retention')
        with self.assertRaisesRegex(ValueError,'obligations erased'):
            intake.check_capability_gate(gate,'N750')

    def test_local_resonance_does_not_acquire_global_phase(self):
        gate = self.gate('N750')
        gate['required_obligations'].remove('residual_global_phase')
        with self.assertRaisesRegex(ValueError,'obligations erased'):
            intake.check_capability_gate(gate,'N750')

    def gate(self,route):
        return next(g for g in intake.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-EP-'+route+'-CAPABILITY')

    def test_notices_do_not_license_older_math_edits(self):
        notices = [n for n in intake.rows('agent/SEMANTIC_NOTICES.jsonl') if n['notice_id'].startswith('SN-EP-')]
        self.assertEqual(len(notices),4)
        for notice in notices:
            route = notice['card_ids'][0].split('-',1)[0]
            dp,cp = 'frontier/dossiers/'+route+'.txt','frontier/connections/'+route+'.json'
            old = intake.git('show',intake.BASE+':'+dp).decode()
            new = (intake.ROOT/dp).read_text()
            old_connection = __import__('json').loads(intake.git('show',intake.BASE+':'+cp))
            connection = intake.load(cp)
            intake.check_projection(old,new,old_connection,connection,notice)
            with self.assertRaisesRegex(ValueError,'historical dossier'):
                intake.check_projection(old,new+'Invented proof claim\n',old_connection,connection,notice)
            mutated = copy.deepcopy(connection)
            mutated['edges'][0]['composition'] = 'Changed historical proof interface'
            with self.assertRaisesRegex(ValueError,'historical connection'):
                intake.check_projection(old,new,old_connection,mutated,notice)


if __name__ == '__main__':
    unittest.main()
