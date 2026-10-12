import copy,importlib.util,json,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('et_validator',Path(__file__).with_name('validate.py'));v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class EvidenceGuards(unittest.TestCase):
    def setUp(self):
        self.m=v.load('updates/ET/SOURCE_MANIFEST.json');self.e=v.load('updates/ET/CLAIMS.json')['claims'][0];self.s=v.load('frontier/cards/'+self.e['id']+'.json');self.t=v.load(self.e['workflow_trace'])
    def test_originals(self):v.check_sources(self.m)
    def test_source_hash_tamper(self):
        self.m['originals'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):v.check_sources(self.m)
    def test_archive_member_omission(self):
        self.m['recovered_packages'][0]['members'].pop()
        with self.assertRaises(ValueError):v.check_sources(self.m)
    def test_producer_manifest_coverage(self):
        self.m['recovered_packages'][0]['producer_hashes_checked']=28
        with self.assertRaises(ValueError):v.check_sources(self.m)
    def test_preservation_is_not_replay(self):
        self.m['recovered_packages'][0]['verification']['scientific_code_execution']='PASS'
        with self.assertRaises(ValueError):v.check_sources(self.m)
    def test_preservation_is_not_array_loading(self):
        self.m['recovered_packages'][0]['verification']['binary_array_loading']='PASS'
        with self.assertRaises(ValueError):v.check_sources(self.m)
    def test_status(self):v.check_status(self.s,(v.ROOT/self.s['card_path']).read_text())
    def test_external_promotion(self):
        self.s['validation']['external_correctness']='PASS'
        with self.assertRaises(ValueError):v.check_status(self.s,(v.ROOT/self.s['card_path']).read_text())
    def test_novelty_promotion(self):
        self.s['validation']['historical_priority']='established'
        with self.assertRaises(ValueError):v.check_status(self.s,(v.ROOT/self.s['card_path']).read_text())
    def test_topical_quantum_dependency(self):
        self.s['depends_on']=[dict(target='N754')]
        with self.assertRaises(ValueError):v.check_status(self.s,(v.ROOT/self.s['card_path']).read_text())
    def test_superseding_local_obstruction(self):
        self.s['supersedes']=[dict(target='N751')]
        with self.assertRaises(ValueError):v.check_status(self.s,(v.ROOT/self.s['card_path']).read_text())
    def test_scope_erasure(self):
        with self.assertRaises(ValueError):v.check_status(self.s,'Dense transport solved in polynomial time.')
    def test_trace(self):v.check_trace(self.t)
    def test_regeneration_not_inference(self):
        self.t['resources']['reported_inference_seconds']=11.08
        with self.assertRaises(ValueError):v.check_trace(self.t)
    def test_reported_duration_not_measured_usage(self):
        self.t['resources']['usage']['wall_seconds']=2971
        with self.assertRaises(ValueError):v.check_trace(self.t)
    def test_unknown_workers(self):
        self.t['resources']['worker_invocations']=0
        with self.assertRaises(ValueError):v.check_trace(self.t)
    def test_unknown_model(self):
        self.t['model']['model_id']='gpt-6.1-sol'
        with self.assertRaises(ValueError):v.check_trace(self.t)
    def test_no_matched_advantage(self):
        self.t['matched_run_id']='invented'
        with self.assertRaises(ValueError):v.check_trace(self.t)
    def test_families(self):v.check_families(v.load('updates/ET/FAMILY_FIT.json'))
    def test_unscoped_family(self):
        f=v.load('updates/ET/FAMILY_FIT.json');f['decisions'][0]['comparisons'].pop()
        with self.assertRaises(ValueError):v.check_families(f)
    def test_dense_gate(self):
        g=next(g for g in v.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-ET-N760-CAPABILITY');v.check_capability(g,self.e['id']);g['status']='closed'
        with self.assertRaises(ValueError):v.check_capability(g,self.e['id'])
    def test_reciprocal_notice(self):v.check_notices(self.m)
    def test_unscoped_old_navigation(self):
        self.m['permitted_historical_navigation_changes'].append('frontier/dossiers/N754.txt')
        with self.assertRaises(ValueError):v.check_notices(self.m)
    def test_notice_does_not_license_math_edits(self):
        dp,cp='frontier/dossiers/N751.txt','frontier/connections/N751.json';args=[v.git('show',v.BASE+':'+dp).decode(),(v.ROOT/dp).read_text(),json.loads(v.git('show',v.BASE+':'+cp)),v.load(cp),v.NOTICE];v.check_projection(*args);args[1]+='Changed scientific theorem.\n'
        with self.assertRaises(ValueError):v.check_projection(*args)
    def test_notice_does_not_license_graph_edits(self):
        dp,cp='frontier/dossiers/N751.txt','frontier/connections/N751.json';args=[v.git('show',v.BASE+':'+dp).decode(),(v.ROOT/dp).read_text(),json.loads(v.git('show',v.BASE+':'+cp)),v.load(cp),v.NOTICE];args[3]['edges'][0]['composition']='invented proof transfer'
        with self.assertRaises(ValueError):v.check_projection(*args)
if __name__=='__main__':unittest.main()
