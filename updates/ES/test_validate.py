import copy, importlib.util, json, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('es_validator',Path(__file__).with_name('validate.py'))
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class EvidenceGuards(unittest.TestCase):
    def test_originals(self):v.check_sources(v.load('updates/ES/SOURCE_MANIFEST.json'))
    def test_extra_source_rejected(self):
        m=v.load('updates/ES/SOURCE_MANIFEST.json');m['campaign_members'].append(dict(m['campaign_members'][0]))
        with self.assertRaises(ValueError):v.check_sources(m)
    def test_replay_claim_rejected(self):
        m=v.load('updates/ES/SOURCE_MANIFEST.json');m['scientific_scripts_executed']=1
        with self.assertRaises(ValueError):v.check_sources(m)
    def test_families(self):v.check_families(v.load('updates/ES/FAMILY_FIT.json'))
    def test_topical_comparison_removed_rejected(self):
        f=v.load('updates/ES/FAMILY_FIT.json');f['decisions'][0]['comparisons']=[]
        with self.assertRaises(ValueError):v.check_families(f)
    def test_N757_scoped_status(self):
        s=v.load('frontier/cards/N757-conserving-finite-memory-coulomb-and-weighted-pair-acquisition.json');v.check_status(s,(v.ROOT/s['card_path']).read_text())
    def test_N757_external_promotion_rejected(self):
        s=v.load('frontier/cards/N757-conserving-finite-memory-coulomb-and-weighted-pair-acquisition.json');s['validation']['external_correctness']='PASS'
        with self.assertRaises(ValueError):v.check_status(s,(v.ROOT/s['card_path']).read_text())
    def test_N757_dependency_invention_rejected(self):
        s=v.load('frontier/cards/N757-conserving-finite-memory-coulomb-and-weighted-pair-acquisition.json');s['depends_on']=[dict(target='N58')]
        with self.assertRaises(ValueError):v.check_status(s,(v.ROOT/s['card_path']).read_text())
    def test_N757_boundary_erasure_rejected(self):
        s=v.load('frontier/cards/N757-conserving-finite-memory-coulomb-and-weighted-pair-acquisition.json')
        with self.assertRaises(ValueError):v.check_status(s,'A breakthrough was established.')
    def test_N757_unknown_trace(self):v.check_trace(v.load('evaluation/workflows/records/RW-es-n757-campaign-subaccount/v0001.json'))
    def test_N757_worker_count_invention_rejected(self):
        t=v.load('evaluation/workflows/records/RW-es-n757-campaign-subaccount/v0001.json');t['resources']['worker_invocations']=3
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_N757_independent_run_invention_rejected(self):
        t=v.load('evaluation/workflows/records/RW-es-n757-campaign-subaccount/v0001.json');t['context']['retained_context']='Three independent experiments'
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_N757_duration_invention_rejected(self):
        t=v.load('evaluation/workflows/records/RW-es-n757-campaign-subaccount/v0001.json');t['resources']['reported_inference_seconds']=60
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_N757_gate_promotion_rejected(self):
        g=next(g for g in v.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-ES-N757-INDEPENDENT-REVIEW');v.check_gate(g,'N757-conserving-finite-memory-coulomb-and-weighted-pair-acquisition');g['status']='closed'
        with self.assertRaises(ValueError):v.check_gate(g,'N757-conserving-finite-memory-coulomb-and-weighted-pair-acquisition')
    def test_N758_scoped_status(self):
        s=v.load('frontier/cards/N758-signed-lp-block-closure-versus-global-acquisition.json');v.check_status(s,(v.ROOT/s['card_path']).read_text())
    def test_N758_external_promotion_rejected(self):
        s=v.load('frontier/cards/N758-signed-lp-block-closure-versus-global-acquisition.json');s['validation']['external_correctness']='PASS'
        with self.assertRaises(ValueError):v.check_status(s,(v.ROOT/s['card_path']).read_text())
    def test_N758_dependency_invention_rejected(self):
        s=v.load('frontier/cards/N758-signed-lp-block-closure-versus-global-acquisition.json');s['depends_on']=[dict(target='N58')]
        with self.assertRaises(ValueError):v.check_status(s,(v.ROOT/s['card_path']).read_text())
    def test_N758_boundary_erasure_rejected(self):
        s=v.load('frontier/cards/N758-signed-lp-block-closure-versus-global-acquisition.json')
        with self.assertRaises(ValueError):v.check_status(s,'A breakthrough was established.')
    def test_N758_unknown_trace(self):v.check_trace(v.load('evaluation/workflows/records/RW-es-n758-campaign-subaccount/v0001.json'))
    def test_N758_worker_count_invention_rejected(self):
        t=v.load('evaluation/workflows/records/RW-es-n758-campaign-subaccount/v0001.json');t['resources']['worker_invocations']=3
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_N758_independent_run_invention_rejected(self):
        t=v.load('evaluation/workflows/records/RW-es-n758-campaign-subaccount/v0001.json');t['context']['retained_context']='Three independent experiments'
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_N758_duration_invention_rejected(self):
        t=v.load('evaluation/workflows/records/RW-es-n758-campaign-subaccount/v0001.json');t['resources']['reported_inference_seconds']=60
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_N758_gate_promotion_rejected(self):
        g=next(g for g in v.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-ES-N758-INDEPENDENT-REVIEW');v.check_gate(g,'N758-signed-lp-block-closure-versus-global-acquisition');g['status']='closed'
        with self.assertRaises(ValueError):v.check_gate(g,'N758-signed-lp-block-closure-versus-global-acquisition')
    def test_N759_scoped_status(self):
        s=v.load('frontier/cards/N759-acquired-correlated-hopping-gauge-and-charged-response-jets.json');v.check_status(s,(v.ROOT/s['card_path']).read_text())
    def test_N759_external_promotion_rejected(self):
        s=v.load('frontier/cards/N759-acquired-correlated-hopping-gauge-and-charged-response-jets.json');s['validation']['external_correctness']='PASS'
        with self.assertRaises(ValueError):v.check_status(s,(v.ROOT/s['card_path']).read_text())
    def test_N759_dependency_invention_rejected(self):
        s=v.load('frontier/cards/N759-acquired-correlated-hopping-gauge-and-charged-response-jets.json');s['depends_on']=[dict(target='N58')]
        with self.assertRaises(ValueError):v.check_status(s,(v.ROOT/s['card_path']).read_text())
    def test_N759_boundary_erasure_rejected(self):
        s=v.load('frontier/cards/N759-acquired-correlated-hopping-gauge-and-charged-response-jets.json')
        with self.assertRaises(ValueError):v.check_status(s,'A breakthrough was established.')
    def test_N759_unknown_trace(self):v.check_trace(v.load('evaluation/workflows/records/RW-es-n759-campaign-subaccount/v0001.json'))
    def test_N759_worker_count_invention_rejected(self):
        t=v.load('evaluation/workflows/records/RW-es-n759-campaign-subaccount/v0001.json');t['resources']['worker_invocations']=3
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_N759_independent_run_invention_rejected(self):
        t=v.load('evaluation/workflows/records/RW-es-n759-campaign-subaccount/v0001.json');t['context']['retained_context']='Three independent experiments'
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_N759_duration_invention_rejected(self):
        t=v.load('evaluation/workflows/records/RW-es-n759-campaign-subaccount/v0001.json');t['resources']['reported_inference_seconds']=60
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_N759_gate_promotion_rejected(self):
        g=next(g for g in v.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-ES-N759-INDEPENDENT-REVIEW');v.check_gate(g,'N759-acquired-correlated-hopping-gauge-and-charged-response-jets');g['status']='closed'
        with self.assertRaises(ValueError):v.check_gate(g,'N759-acquired-correlated-hopping-gauge-and-charged-response-jets')
if __name__=='__main__':unittest.main()
