import copy,importlib.util,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('eu_validator',Path(__file__).with_name('validate.py'))
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class EvidenceGuards(unittest.TestCase):
    def test_sources(self):v.check_sources(v.load('updates/EU/SOURCE_MANIFEST.json'))
    def test_families(self):v.check_families(v.load('updates/EU/FAMILY_FIT.json'))
    def test_status(self):
        s=v.load('frontier/cards/N761-sign-divisor-code-normal-form-and-robust-threshold-mixture-bound.json');v.check_status(s,(v.ROOT/s['card_path']).read_text())
    def test_trace(self):v.check_trace(v.load('evaluation/workflows/records/RW-eu-sign-divisor/v0001.json'))
    def test_gate(self):
        g=next(g for g in v.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-EU-N761-INDEPENDENT-REVIEW');v.check_gate(g,g['card_ids'][0])
    def test_changed_original_digest_rejected(self):
        x=v.load('updates/EU/SOURCE_MANIFEST.json')
        x['originals'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):v.check_sources(x)
    def test_source_range_truncation_rejected(self):
        x=v.load('updates/EU/SOURCE_MANIFEST.json')
        x['originals'][0]['lines']=215
        with self.assertRaises(ValueError):v.check_sources(x)
    def test_missing_member_rejected(self):
        x=v.load('updates/EU/SOURCE_MANIFEST.json')
        x['recovered_packages'][0]['members'].pop()
        with self.assertRaises(ValueError):v.check_sources(x)
    def test_manifest_coverage_rejected(self):
        x=v.load('updates/EU/SOURCE_MANIFEST.json')
        x['recovered_packages'][0]['producer_hashes_checked']=3
        with self.assertRaises(ValueError):v.check_sources(x)
    def test_scientific_replay_invention_rejected(self):
        x=v.load('updates/EU/SOURCE_MANIFEST.json')
        x['scientific_scripts_executed']=1
        with self.assertRaises(ValueError):v.check_sources(x)
    def test_external_promotion_rejected(self):
        x=v.load('frontier/cards/N761-sign-divisor-code-normal-form-and-robust-threshold-mixture-bound.json');text=(v.ROOT/x['card_path']).read_text()
        x['validation']['external_correctness']='PASS'
        with self.assertRaises(ValueError):v.check_status(x,text)
    def test_novelty_promotion_rejected(self):
        x=v.load('frontier/cards/N761-sign-divisor-code-normal-form-and-robust-threshold-mixture-bound.json');text=(v.ROOT/x['card_path']).read_text()
        x['validation']['historical_priority']='established'
        with self.assertRaises(ValueError):v.check_status(x,text)
    def test_topical_dependency_rejected(self):
        x=v.load('frontier/cards/N761-sign-divisor-code-normal-form-and-robust-threshold-mixture-bound.json');text=(v.ROOT/x['card_path']).read_text()
        x['depends_on'].append({'target':'N26'})
        with self.assertRaises(ValueError):v.check_status(x,text)
    def test_old_gate_closure_rejected(self):
        x=v.load('frontier/cards/N761-sign-divisor-code-normal-form-and-robust-threshold-mixture-bound.json');text=(v.ROOT/x['card_path']).read_text()
        x['supersedes']=[{'target':'N26'}]
        with self.assertRaises(ValueError):v.check_status(x,text)
    def test_boundary_erasure_rejected(self):
        x=v.load('frontier/cards/N761-sign-divisor-code-normal-form-and-robust-threshold-mixture-bound.json');text=(v.ROOT/x['card_path']).read_text()
        text='A general sampling breakthrough was established.'
        with self.assertRaises(ValueError):v.check_status(x,text)
    def test_worker_invention_rejected(self):
        x=v.load('evaluation/workflows/records/RW-eu-sign-divisor/v0001.json')
        x['resources']['worker_invocations']=2
        with self.assertRaises(ValueError):v.check_trace(x)
    def test_usage_invention_rejected(self):
        x=v.load('evaluation/workflows/records/RW-eu-sign-divisor/v0001.json')
        x['resources']['usage']['wall_seconds']=2597
        with self.assertRaises(ValueError):v.check_trace(x)
    def test_model_invention_rejected(self):
        x=v.load('evaluation/workflows/records/RW-eu-sign-divisor/v0001.json')
        x['model']['model']='GPT-6.1'
        with self.assertRaises(ValueError):v.check_trace(x)
    def test_conversation_invention_rejected(self):
        x=v.load('evaluation/workflows/records/RW-eu-sign-divisor/v0001.json')
        x['context']['conversation_relation']='same'
        with self.assertRaises(ValueError):v.check_trace(x)
    def test_independent_review_invention_rejected(self):
        x=v.load('evaluation/workflows/records/RW-eu-sign-divisor/v0001.json')
        x['advance']['verification']='independently_verified'
        with self.assertRaises(ValueError):v.check_trace(x)
    def test_duration_overwrite_rejected(self):
        x=v.load('evaluation/workflows/records/RW-eu-sign-divisor/v0001.json')
        x['resources']['reported_inference_seconds']=2600
        with self.assertRaises(ValueError):v.check_trace(x)
    def test_family_loss_rejected(self):
        x=v.load('updates/EU/FAMILY_FIT.json')
        x['decisions'][0]['comparisons'].pop()
        with self.assertRaises(ValueError):v.check_families(x)
    def test_unscoped_family_rejected(self):
        x=v.load('updates/EU/FAMILY_FIT.json')
        x['decisions'][0]['comparisons'][0]['scope']=''
        with self.assertRaises(ValueError):v.check_families(x)
    def test_gate_promotion_rejected(self):
        x=next(g for g in v.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-EU-N761-INDEPENDENT-REVIEW')
        x['status']='closed'
        with self.assertRaises(ValueError):v.check_gate(x,x['card_ids'][0])
if __name__=='__main__':unittest.main()
