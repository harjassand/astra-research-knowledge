import copy,importlib.util,json,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('ew_validator',Path(__file__).with_name('validate.py'))
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class EvidenceGuards(unittest.TestCase):
    def manifest(self):return v.load('updates/EW/SOURCE_MANIFEST.json')
    def status(self,r):
        e=next(e for e in v.load('updates/EW/CLAIMS.json')['claims'] if v.route(e['id'])==r)
        s=v.load('frontier/cards/'+e['id']+'.json');return s,(v.ROOT/s['card_path']).read_text()
    def trace(self,r):
        e=next(e for e in v.load('updates/EW/CLAIMS.json')['claims'] if v.route(e['id'])==r);return v.load(e['workflow_trace'])
    def projection(self):
        p='frontier/dossiers/N754.txt';c='frontier/connections/N754.json'
        return [v.git('show',v.BASE+':'+p).decode(),(v.ROOT/p).read_text(),json.loads(v.git('show',v.BASE+':'+c)),v.load(c),v.NOTICE]
    def test_sources(self):v.check_sources(self.manifest())
    def test_statuses(self):
        for r in v.ROUTES:v.check_status(*self.status(r))
    def test_traces(self):
        for r in v.ROUTES:v.check_trace(self.trace(r))
    def test_families(self):v.check_families(v.load('updates/EW/FAMILY_FIT.json'))
    def test_projection(self):v.check_projection(*self.projection())
    def test_reciprocal_notice(self):v.check_notices(self.manifest())
    def test_gates(self):
        for g in v.rows('frontier/OPEN_PROOF_GATES.jsonl'):
            if g['gate_id'].startswith('G-EW-'):v.check_gate(g,g['card_ids'][0])
    def test_changed_digest_rejected(self):
        x=self.manifest();x['originals'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):v.check_sources(x)
    def test_truncated_paste_rejected(self):
        x=self.manifest();x['originals'][0]['lines']-=1
        with self.assertRaises(ValueError):v.check_sources(x)
    def test_missing_member_rejected(self):
        x=self.manifest();x['recovered_packages'][0]['members'].pop()
        with self.assertRaises(ValueError):v.check_sources(x)
    def test_producer_manifest_count_rejected(self):
        x=self.manifest();x['recovered_packages'][0]['producer_hashes_checked']=8
        with self.assertRaises(ValueError):v.check_sources(x)
    def test_scientific_replay_invention_rejected(self):
        x=self.manifest();x['scientific_scripts_executed']=1
        with self.assertRaises(ValueError):v.check_sources(x)
    def test_independent_proof_invention_rejected(self):
        x=self.manifest();x['recovered_packages'][0]['verification']['independent_proof_review']='PASS'
        with self.assertRaises(ValueError):v.check_sources(x)
    def test_prior_availability_invention_rejected(self):
        x=self.manifest();x['originals'][0]['referenced_but_not_supplied']=[]
        with self.assertRaises(ValueError):v.check_sources(x)
    def test_correctness_promotion_rejected(self):
        s,t=self.status('N764');s['validation']['external_correctness']='PASS'
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_novelty_promotion_rejected(self):
        s,t=self.status('N764');s['validation']['historical_priority']='established'
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_import_loss_rejected(self):
        s,t=self.status('N764');s['depends_on'].pop()
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_gate_supersession_rejected(self):
        s,t=self.status('N764');s['supersedes']=[{'target':'N754'}]
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_wrong_material_update_rejected(self):
        s,t=self.status('N764');s['material_updates'][0]['target']='N747'
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_primitive_l2_erasure_rejected(self):
        s,t=self.status('N764');t=t.replace('l1 alone is insufficient','l1 always suffices')
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_rank_scope_erasure_rejected(self):
        s,t=self.status('N764');t=t.replace('NOT approximate-rank','an approximate-rank impossibility')
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_worker_invention_rejected(self):
        t=self.trace('N764');t['resources']['worker_invocations']=2
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_usage_invention_rejected(self):
        t=self.trace('N764');t['resources']['usage']['wall_seconds']=3348
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_model_invention_rejected(self):
        t=self.trace('N764');t['model']['model']='GPT-6.1'
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_context_invention_rejected(self):
        t=self.trace('N764');t['context']['conversation_relation']='new'
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_duration_overwrite_rejected(self):
        t=self.trace('N764');t['resources']['reported_inference_seconds']=3746
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_independent_trace_invention_rejected(self):
        t=self.trace('N764');t['advance']['verification']='independently_verified'
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_family_loss_rejected(self):
        f=v.load('updates/EW/FAMILY_FIT.json');f['decisions'][0]['comparisons'].pop()
        with self.assertRaises(ValueError):v.check_families(f)
    def test_unscoped_family_rejected(self):
        f=v.load('updates/EW/FAMILY_FIT.json');f['decisions'][0]['comparisons'][0]['scope']=''
        with self.assertRaises(ValueError):v.check_families(f)
    def test_gate_promotion_rejected(self):
        g=next(g for g in v.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-EW-N764-CAPABILITY');g['status']='closed'
        with self.assertRaises(ValueError):v.check_gate(g,g['card_ids'][0])
    def test_old_dossier_rewrite_rejected(self):
        p=self.projection();p[1]+='\nAn old theorem has been changed.\n'
        with self.assertRaises(ValueError):v.check_projection(*p)
    def test_old_connection_rewrite_rejected(self):
        p=self.projection();p[3]['edges'].pop(0)
        with self.assertRaises(ValueError):v.check_projection(*p)
    def test_missing_notice_rejected(self):
        p=self.projection();p[1]=p[0]
        with self.assertRaises(ValueError):v.check_projection(*p)
    def test_pressure_is_not_transport_guard(self):
        s,t=self.status('N764');t=t.replace('E_b, NOT D','the full transport D')
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_comparator_erasure_rejected(self):
        s,t=self.status('N764');t=t.replace('Sparse wins runtime','Compressed wins runtime')
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_vector_error_erasure_rejected(self):
        s,t=self.status('N764');t=t.replace('vector error bound is3.571e-6','vector error bound is1e-11')
        with self.assertRaises(ValueError):v.check_status(s,t)
if __name__=='__main__':unittest.main()
