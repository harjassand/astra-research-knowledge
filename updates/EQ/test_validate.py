"""Intake evidence guards; archived scientific code is never imported or run."""
import importlib.util
from pathlib import Path
import unittest
from unittest import mock
import copy

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('eq_validate',HERE/'validate.py')
intake=importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


class EvidenceGuards(unittest.TestCase):
    def setUp(self):
        self.manifest=intake.load('updates/EQ/SOURCE_MANIFEST.json')
        self.entry=intake.load('updates/EQ/CLAIMS.json')['claims'][0]
        self.status=intake.load('frontier/cards/'+self.entry['id']+'.json')
        self.trace=intake.load(self.entry['workflow_trace'])
        self.gate=next(g for g in intake.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-EQ-N751-CAPABILITY')

    def test_exact_original_sources(self):
        intake.check_sources(self.manifest)
        self.manifest['originals'][0]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'bytes/hash'):
            intake.check_sources(self.manifest)

    def test_witness_file_hash(self):
        member=next(m for m in self.manifest['recovered_packages'][0]['members'] if m['path'].endswith('certificate_19_20.json'))
        member['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'bytes/hash'):
            intake.check_sources(self.manifest)

    def test_omitted_archive_member(self):
        self.manifest['recovered_packages'][0]['members'].pop()
        with self.assertRaisesRegex(ValueError,'identities'):
            intake.check_sources(self.manifest)

    def test_producer_hash_coverage(self):
        self.manifest['recovered_packages'][0]['producer_hashes_checked']=0
        with self.assertRaisesRegex(ValueError,'manifest coverage'):
            intake.check_sources(self.manifest)

    def test_integrity_is_not_replay(self):
        self.manifest['recovered_packages'][0]['verification']['scientific_code_execution']='PASS'
        with self.assertRaisesRegex(ValueError,'scientific replay'):
            intake.check_sources(self.manifest)

    def test_optimizer_independence_is_not_external_review(self):
        intake.check_status(self.status)
        self.status['validation']['external_correctness']='PASS'
        with self.assertRaisesRegex(ValueError,'scientific promotion'):
            intake.check_status(self.status)

    def test_scientific_status_cannot_be_promoted(self):
        self.status['claim_status']='externally_verified'
        with self.assertRaisesRegex(ValueError,'scientific promotion'):
            intake.check_status(self.status)

    def test_imported_cooperative_positivity_is_retained(self):
        self.status['depends_on'].pop()
        with self.assertRaisesRegex(ValueError,'dependency'):
            intake.check_status(self.status)

    def test_no_quantum_G1_proof_dependency(self):
        self.status['depends_on'].append({'target':'N747','scope':'both predict diffusion'})
        with self.assertRaisesRegex(ValueError,'dependency'):
            intake.check_status(self.status)

    def test_reported_duration_not_measured_usage(self):
        intake.check_trace(self.trace,'N751')
        self.trace['resources']['usage']['wall_seconds']=2063
        with self.assertRaisesRegex(ValueError,'telemetry'):
            intake.check_trace(self.trace,'N751')

    def test_unknown_model_and_workers(self):
        self.trace['model']['model_id']='gpt-6.1-sol'
        self.trace['resources']['worker_invocations']=0
        with self.assertRaisesRegex(ValueError,'telemetry'):
            intake.check_trace(self.trace,'N751')

    def test_source_verifier_is_not_intake_verification(self):
        self.trace['advance']['verification']='independently_verified'
        with self.assertRaisesRegex(ValueError,'producer output'):
            intake.check_trace(self.trace,'N751')

    def test_completion_gate_open(self):
        intake.check_capability_gate(self.gate,'N751')
        self.gate['status']='proved'
        with self.assertRaisesRegex(ValueError,'unproved capability'):
            intake.check_capability_gate(self.gate,'N751')

    def test_energy_error_must_be_acquired(self):
        self.gate['required_obligations'].remove('acquired_energy_error')
        with self.assertRaisesRegex(ValueError,'obligations erased'):
            intake.check_capability_gate(self.gate,'N751')

    def test_local_obstruction_and_patch_cost_are_retained(self):
        self.gate['validation_boundary']=self.gate['validation_boundary'].replace('nonpositive dual value under box closure','positive diffusion by patch growth')
        with self.assertRaisesRegex(ValueError,'scientific boundary'):
            intake.check_capability_gate(self.gate,'N751')

    def test_no_topical_historical_edits(self):
        intake.check_notices(self.manifest)
        self.manifest['permitted_historical_navigation_changes']=['frontier/dossiers/N747.txt']
        with self.assertRaisesRegex(ValueError,'historical update'):
            intake.check_notices(self.manifest)

    def test_family_contracts_remain_distinct(self):
        fit=intake.load('updates/EQ/FAMILY_FIT.json')
        intake.check_families(fit)
        fit['decisions'][0]['comparisons'].clear()
        with self.assertRaisesRegex(ValueError,'comparison scope'):
            intake.check_families(fit)

    def test_only_exact_validator_compatibility_patch_allowed(self):
        old=intake.git('show',intake.BASE+':updates/EP/validate.py').decode()
        new=(intake.ROOT/'updates/EP/validate.py').read_text()
        intake.check_validator_compatibility(old,new)
        with self.assertRaisesRegex(ValueError,'beyond cached-output guard'):
            intake.check_validator_compatibility(old,new+'# unscoped change\n')

    def projection_inputs(self):
        spec=importlib.util.spec_from_file_location('ep_live_validator',intake.ROOT/'updates/EP/validate.py')
        ep=importlib.util.module_from_spec(spec);spec.loader.exec_module(ep)
        notice=next(n for n in ep.rows('agent/SEMANTIC_NOTICES.jsonl') if n['notice_id']=='SN-EP-N689-N749-SCOPED-CONTINUATION')
        dp,cp='frontier/dossiers/N689.txt','frontier/connections/N689.json'
        args=[ep.git('show',ep.BASE+':'+dp).decode(),(ep.ROOT/dp).read_text(),
              __import__('json').loads(ep.git('show',ep.BASE+':'+cp)),ep.load(cp),notice]
        return ep,args,cp

    def test_unchanged_cached_connection_accepted(self):
        ep,args,cp=self.projection_inputs()
        self.assertNotEqual(args[3]['snapshot'],ep.load('agent/access_manifest.json')['snapshot'])
        ep.check_projection(*args)

    def test_stale_cache_hash_rejected(self):
        ep,args,cp=self.projection_inputs()
        original_load=ep.load
        manifest=copy.deepcopy(original_load('agent/access_manifest.json'))
        manifest['outputs'][cp]='0'*64
        with mock.patch.object(ep,'load',side_effect=lambda path: manifest if path=='agent/access_manifest.json' else original_load(path)):
            with self.assertRaisesRegex(ValueError,'unexpected generated snapshot'):
                ep.check_projection(*args)


if __name__=='__main__':
    unittest.main()
