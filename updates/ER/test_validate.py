"""Repository evidence guards; never imports or runs archived scientific code."""
import copy
import importlib.util
from pathlib import Path
import unittest
from unittest import mock

spec=importlib.util.spec_from_file_location('er_validate',Path(__file__).with_name('validate.py'))
intake=importlib.util.module_from_spec(spec);spec.loader.exec_module(intake)

class EvidenceGuards(unittest.TestCase):
    def setUp(self):
        self.manifest=intake.load('updates/ER/SOURCE_MANIFEST.json')
        self.entries={intake.route(e['id']):e for e in intake.load('updates/ER/CLAIMS.json')['claims']}
    def status(self,r):return intake.load('frontier/cards/'+self.entries[r]['id']+'.json')
    def trace(self,r):return intake.load(self.entries[r]['workflow_trace'])
    def test_exact_legacy_fixture_adaptation(self):
        old=intake.git('show',intake.BASE+':updates/EP/test_validate.py').decode();new=(intake.ROOT/'updates/EP/test_validate.py').read_text()
        intake.check_legacy_test(old,new)
        with self.assertRaisesRegex(ValueError,'beyond exact'):
            intake.check_legacy_test(old,new+'# unscoped change\n')
    def test_exact_sources(self):intake.check_sources(self.manifest)
    def test_paste_tamper(self):
        self.manifest['originals'][0]['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'bytes/hash'):intake.check_sources(self.manifest)
    def test_zip_member_omission(self):
        self.manifest['recovered_packages'][0]['members'].pop()
        with self.assertRaisesRegex(ValueError,'identities'):intake.check_sources(self.manifest)
    def test_directory_member_omission(self):
        self.manifest['supplied_directories'][0]['members'].pop()
        with self.assertRaisesRegex(ValueError,'identities'):intake.check_sources(self.manifest)
    def test_directory_digest_coverage(self):
        self.manifest['supplied_directories'][0]['producer_hashes_checked']=0
        with self.assertRaisesRegex(ValueError,'manifest coverage'):intake.check_sources(self.manifest)
    def test_zip_digest_coverage(self):
        self.manifest['recovered_packages'][0]['producer_hashes_checked']=0
        with self.assertRaisesRegex(ValueError,'manifest coverage'):intake.check_sources(self.manifest)
    def test_integrity_is_not_replay(self):
        self.manifest['supplied_directories'][0]['verification']['scientific_code_execution']='PASS'
        with self.assertRaisesRegex(ValueError,'scientific replay'):intake.check_sources(self.manifest)
    def test_no_independent_validation(self):
        s=self.status('N752');s['validation']['external_correctness']='PASS'
        with self.assertRaisesRegex(ValueError,'scientific promotion'):intake.check_status(s)
    def test_no_novelty_promotion(self):
        s=self.status('N756');s['validation']['historical_priority']='established'
        with self.assertRaisesRegex(ValueError,'scientific promotion'):intake.check_status(s)
    def test_no_prior_card_supersession(self):
        s=self.status('N752');s['supersedes']=[{'target':'P-round'}]
        with self.assertRaisesRegex(ValueError,'correction'):intake.check_status(s)
    def test_no_topical_dependency(self):
        s=self.status('N754');s['depends_on'].append({'target':'N751','scope':'transport'})
        with self.assertRaisesRegex(ValueError,'dependency'):intake.check_status(s)
    def test_known_counting_import_preserved(self):
        s=self.status('N753');s['depends_on']=[]
        with self.assertRaisesRegex(ValueError,'dependency'):intake.check_status(s)
    def test_scoped_continuations_preserved(self):
        s=self.status('N752');s['material_updates'].pop()
        with self.assertRaisesRegex(ValueError,'continuation scope'):intake.check_status(s)
    def test_all_status_boundaries(self):
        for r in self.entries:intake.check_status(self.status(r))
    def test_erased_implementation_limit(self):
        s=self.status('N752');body=(intake.ROOT/s['card_path']).read_text().replace('not implemented','implemented')
        original=Path.read_text
        with mock.patch.object(Path,'read_text',side_effect=lambda *a,**kw:body):
            with self.assertRaisesRegex(ValueError,'scientific boundary'):intake.check_status(s)
    def test_duration_is_reported_only(self):
        t=self.trace('N752');intake.check_trace(t,'N752');t['resources']['usage']['wall_seconds']=2530
        with self.assertRaisesRegex(ValueError,'telemetry'):intake.check_trace(t,'N752')
    def test_bundle_has_no_inferred_duration(self):
        t=self.trace('N753');t['resources']['reported_inference_seconds']=11
        with self.assertRaisesRegex(ValueError,'duration'):intake.check_trace(t,'N753')
    def test_bundle_has_no_invented_prompt(self):
        t=self.trace('N754');t['prompt_availability']='exact';t['prompt_ref_ids']=['output']
        with self.assertRaisesRegex(ValueError,'prompt invented'):intake.check_trace(t,'N754')
    def test_bundle_is_not_four_independent_runs(self):
        t=self.trace('N756');t['context']['retained_context']='Four independent research campaigns'
        with self.assertRaisesRegex(ValueError,'independent runs'):intake.check_trace(t,'N756')
    def test_unknown_workers(self):
        t=self.trace('N752');t['resources']['worker_invocations']=0
        with self.assertRaisesRegex(ValueError,'telemetry'):intake.check_trace(t,'N752')
    def test_unknown_model(self):
        t=self.trace('N752');t['model']['model_id']='gpt-6.1-sol'
        with self.assertRaisesRegex(ValueError,'telemetry'):intake.check_trace(t,'N752')
    def test_no_matched_advantage(self):
        t=self.trace('N752');t['matched_run_id']='invented-run'
        with self.assertRaisesRegex(ValueError,'producer evidence'):intake.check_trace(t,'N752')
    def test_all_trace_boundaries(self):
        for r in self.entries:intake.check_trace(self.trace(r),r)
    def test_family_fit(self):intake.check_families(intake.load('updates/ER/FAMILY_FIT.json'))
    def test_no_topical_polymer_family(self):
        f=intake.load('updates/ER/FAMILY_FIT.json');f['decisions'][3]['comparisons']=[{'card_id':'N707','scope':'energy'}]
        with self.assertRaisesRegex(ValueError,'comparison scope'):intake.check_families(f)
    def test_reciprocal_notices_and_exact_historical_projection(self):intake.check_notices(self.manifest)
    def test_extra_historical_view_rejected(self):
        self.manifest['permitted_historical_navigation_changes'].append('frontier/dossiers/N751.txt')
        with self.assertRaisesRegex(ValueError,'unscoped historical'):intake.check_notices(self.manifest)
    def test_historical_scientific_edit_rejected(self):
        n=next(n for n in intake.rows('agent/SEMANTIC_NOTICES.jsonl') if n['notice_id']=='SN-ER-P-round-N752-SCOPED-CONTINUATION')
        dp,cp='frontier/dossiers/P-round.txt','frontier/connections/P-round.json'
        old=intake.git('show',intake.BASE+':'+dp).decode();new=(intake.ROOT/dp).read_text()
        before=__import__('json').loads(intake.git('show',intake.BASE+':'+cp));after=intake.load(cp)
        with self.assertRaisesRegex(ValueError,'dossier altered'):intake.check_projection(old,new+'Unsupported scientific claim\n',before,after,n)
    def test_historical_graph_edit_rejected(self):
        n=next(n for n in intake.rows('agent/SEMANTIC_NOTICES.jsonl') if n['notice_id']=='SN-ER-P-round-N752-SCOPED-CONTINUATION')
        dp,cp='frontier/dossiers/P-round.txt','frontier/connections/P-round.json'
        before=__import__('json').loads(intake.git('show',intake.BASE+':'+cp));after=intake.load(cp);after['policy']='proof certified'
        with self.assertRaisesRegex(ValueError,'connection altered'):intake.check_projection(intake.git('show',intake.BASE+':'+dp).decode(),(intake.ROOT/dp).read_text(),before,after,n)

if __name__=='__main__':unittest.main()
