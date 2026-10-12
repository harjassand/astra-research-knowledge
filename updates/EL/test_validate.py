"""Negative guards for evidence and information interfaces; no scientific replay."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('el_validate',Path(__file__).with_name('validate.py'))
intake=importlib.util.module_from_spec(spec)
spec.loader.exec_module(intake)


class EvidenceGuards(unittest.TestCase):
    def setUp(self):
        self.manifest=intake.load('updates/EL/SOURCE_MANIFEST.json')
        self.mapping=intake.load('updates/EL/CLAIMS.json')
        self.campaign=intake.load(self.mapping['claims'][0]['workflow_trace'])
        self.pdf=intake.load(self.mapping['claims'][3]['workflow_trace'])

    def status(self,route):
        entry=next(x for x in self.mapping['claims'] if x['id'].startswith(route+'-'))
        return intake.load('frontier/cards/'+entry['id']+'.json')

    def test_selected_original_identity_cannot_be_rewritten(self):
        intake.check_sources(self.manifest)
        self.manifest['originals'][0]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'identity'):
            intake.check_sources(self.manifest)

    def test_same_state_copy_is_not_posterior_replica(self):
        s=self.status('N736');intake.check_status(s)
        s['validation']['operational_scope']['posterior_replicas_from_hidden_state_copies']=True
        with self.assertRaisesRegex(ValueError,'scope'):
            intake.check_status(s)

    def test_ideal_crn_random_variates_are_not_a_bit_implementation(self):
        s=self.status('N735');s['validation']['operational_scope']['exact_bit_implementation']='COMPLETE'
        with self.assertRaisesRegex(ValueError,'scope'):
            intake.check_status(s)

    def test_endpoint_additive_tv_is_not_a_history_or_rare_relative_guarantee(self):
        for key in ['fault_history','relative_rare_failure_accuracy']:
            with self.subTest(key=key):
                s=self.status('N738');s['validation']['operational_scope'][key]=True
                with self.assertRaisesRegex(ValueError,'scope'):
                    intake.check_status(s)

    def test_sparse_summary_is_not_the_physical_jump_law(self):
        s=self.status('N738');s['validation']['operational_scope']['summary_replaces_jump_law']=True
        with self.assertRaisesRegex(ValueError,'scope'):
            intake.check_status(s)

    def test_wall_interval_is_not_inference_expenditure(self):
        intake.check_trace(self.campaign,True,self.manifest)
        self.campaign['resources']['reported_inference_seconds']=3968
        with self.assertRaisesRegex(ValueError,'telemetry'):
            intake.check_trace(self.campaign,True,self.manifest)

    def test_unique_workers_do_not_count_all_invocations(self):
        self.campaign['resources']['worker_invocations']=12
        with self.assertRaisesRegex(ValueError,'telemetry'):
            intake.check_trace(self.campaign,True,self.manifest)

    def test_pdf_does_not_inherit_campaign_workers(self):
        intake.check_trace(self.pdf,False,self.manifest)
        self.pdf['resources']['worker_receipt_ref_ids']=['state']
        with self.assertRaisesRegex(ValueError,'attribution'):
            intake.check_trace(self.pdf,False,self.manifest)

    def test_worker_models_do_not_identify_root_backend(self):
        self.campaign['model']['model_id']='gpt-6.1-sol'
        with self.assertRaisesRegex(ValueError,'telemetry'):
            intake.check_trace(self.campaign,True,self.manifest)

    def test_internal_challenges_are_not_independent_verification(self):
        self.campaign['advance']['verification']='independent_receipt'
        with self.assertRaisesRegex(ValueError,'verification'):
            intake.check_trace(self.campaign,True,self.manifest)

    def test_preservation_cannot_promote_correctness(self):
        s=self.status('N735');s['validation']['external_correctness']='VERIFIED'
        with self.assertRaisesRegex(ValueError,'promotion'):
            intake.check_status(s)

    def test_family_continuation_is_not_a_theorem_premise(self):
        s=self.status('N736');s['depends_on']=['N718-intervention-product-completion-of-hidden-predictive-residuals']
        with self.assertRaisesRegex(ValueError,'dependency'):
            intake.check_status(s)


    def test_scoped_notice_cannot_hide_old_dossier_rewrite(self):
        original = Path.read_text
        target = intake.ROOT/'frontier/dossiers/N713.txt'
        notice = next(x for x in intake.rows('agent/SEMANTIC_NOTICES.jsonl')
                      if x['notice_id']=='SN-EL-N713-N736-OCCUPATION-PATH')
        newer = self.mapping['claims'][1]['id']
        intake.check_continuation_projection('N713',newer,notice)
        def changed(path, *args, **kwargs):
            text = original(path, *args, **kwargs)
            return text.replace('TASK-RELEVANT OPEN GATES','ALTERED HISTORICAL CONTENT') if path==target else text
        with patch.object(Path,'read_text',changed), self.assertRaisesRegex(
                ValueError,'earlier dossier mathematics changed'):
            intake.check_continuation_projection('N713',newer,notice)


if __name__=='__main__':
    unittest.main()
