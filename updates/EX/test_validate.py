import copy,importlib.util,json,unittest,re
from pathlib import Path
spec=importlib.util.spec_from_file_location('ex_validator',Path(__file__).with_name('validate.py'))
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class EvidenceGuards(unittest.TestCase):
    def manifest(self):return v.load('updates/EX/SOURCE_MANIFEST.json')
    def status(self,r):
        e=next(e for e in v.load('updates/EX/CLAIMS.json')['claims'] if v.route(e['id'])==r)
        s=v.load('frontier/cards/'+e['id']+'.json');return s,(v.ROOT/s['card_path']).read_text()
    def trace(self,r):
        e=next(e for e in v.load('updates/EX/CLAIMS.json')['claims'] if v.route(e['id'])==r);return v.load(e['workflow_trace'])
    def projection(self):
        p='frontier/dossiers/N764.txt';c='frontier/connections/N764.json'
        return [v.git('show',v.BASE+':'+p).decode(),(v.ROOT/p).read_text(),json.loads(v.git('show',v.BASE+':'+c)),v.load(c),v.NOTICE]
    def test_sources(self):v.check_sources(self.manifest())
    def test_statuses(self):
        for r in v.ROUTES:v.check_status(*self.status(r))
    def test_traces(self):
        for r in v.ROUTES:v.check_trace(self.trace(r))
    def test_families(self):v.check_families(v.load('updates/EX/FAMILY_FIT.json'))
    def test_projection(self):v.check_projection(*self.projection())
    def test_reciprocal_notice(self):v.check_notices(self.manifest())
    def test_gates(self):
        for g in v.rows('frontier/OPEN_PROOF_GATES.jsonl'):
            if g['gate_id'].startswith('G-EX-'):v.check_gate(g,g['card_ids'][0])
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
    def test_binary_loading_invention_rejected(self):
        x=self.manifest();x['recovered_packages'][0]['verification']['binary_array_loading']='performed'
        with self.assertRaises(ValueError):v.check_sources(x)
    def test_correctness_promotion_rejected(self):
        s,t=self.status('N765');s['validation']['external_correctness']='PASS'
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_novelty_promotion_rejected(self):
        s,t=self.status('N765');s['validation']['historical_priority']='established'
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_import_loss_rejected(self):
        s,t=self.status('N765');s['depends_on'].pop()
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_gate_supersession_rejected(self):
        s,t=self.status('N765');s['supersedes']=[{'target':'N765'}]
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_wrong_material_update_rejected(self):
        s,t=self.status('N765');s['material_updates'][0]['target']='N747'
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_residual_order_erasure_rejected(self):
        s,t=self.status('N765');t=t.replace('order M+1','order M only')
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_curvature_erasure_rejected(self):
        s,t=self.status('N765');t=t.replace('CERTIFIED curvature','assumed curvature')
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_worker_invention_rejected(self):
        t=self.trace('N765');t['resources']['worker_invocations']=2
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_usage_invention_rejected(self):
        t=self.trace('N765');t['resources']['usage']['wall_seconds']=3348
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_model_invention_rejected(self):
        t=self.trace('N765');t['model']['model']='GPT-6.1'
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_context_invention_rejected(self):
        t=self.trace('N765');t['context']['conversation_relation']='new'
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_duration_overwrite_rejected(self):
        t=self.trace('N765');t['resources']['reported_inference_seconds']=3746
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_independent_trace_invention_rejected(self):
        t=self.trace('N765');t['advance']['verification']='independently_verified'
        with self.assertRaises(ValueError):v.check_trace(t)
    def test_family_loss_rejected(self):
        f=v.load('updates/EX/FAMILY_FIT.json');f['decisions'][0]['comparisons'].pop()
        with self.assertRaises(ValueError):v.check_families(f)
    def test_unscoped_family_rejected(self):
        f=v.load('updates/EX/FAMILY_FIT.json');f['decisions'][0]['comparisons'][0]['scope']=''
        with self.assertRaises(ValueError):v.check_families(f)
    def test_gate_promotion_rejected(self):
        g=next(g for g in v.rows('frontier/OPEN_PROOF_GATES.jsonl') if g['gate_id']=='G-EX-N765-CAPABILITY');g['status']='closed'
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
    def test_speedup_invention_rejected(self):
        s,t=self.status('N765');t=t.replace('NOT86fold runtime','86fold runtime')
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_acquisition_failure_erasure_rejected(self):
        s,t=self.status('N766');t=re.sub('all7938','Only2014',t,flags=re.I)
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_float_scope_erasure_rejected(self):
        s,t=self.status('N766');t=t.replace('not outward-rounded','outward-rounded')
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_random_bit_invention_rejected(self):
        s,t=self.status('N766');t=t.replace('pseudorandom','independent random')
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_physical_gain_erasure_rejected(self):
        s,t=self.status('N767');t=re.sub('negative real','negative imaginary',t,flags=re.I)
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_cycle_theorem_invention_rejected(self):
        s,t=self.status('N767');t=t.replace('not a proof of stable nonlinear','a proof of stable nonlinear')
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_material_forecast_invention_rejected(self):
        s,t=self.status('N767');t=t.replace('not forecasts for identified materials','forecasts for identified materials')
        with self.assertRaises(ValueError):v.check_status(s,t)
    def test_technology(self):v.check_technology(v.load(v.TECHNOLOGY))
    def test_technology_promotion_rejected(self):
        t=v.load(v.TECHNOLOGY);t['stage']='experiment'
        with self.assertRaises(ValueError):v.check_technology(t)
    def test_independent_simulation_invention_rejected(self):
        t=v.load(v.TECHNOLOGY);t['evidence'][1]['kind']='reproduced_simulation'
        with self.assertRaises(ValueError):v.check_technology(t)
    def test_physical_measurement_invention_rejected(self):
        t=v.load(v.TECHNOLOGY);t['evidence'][1]['kind']='experimental_measurement'
        with self.assertRaises(ValueError):v.check_technology(t)
    def test_physical_gate_close_rejected(self):
        t=v.load(v.TECHNOLOGY);t['gates'][-1]['decision']='passed'
        with self.assertRaises(ValueError):v.check_technology(t)
    def test_established_bridge_invention_rejected(self):
        t=v.load(v.TECHNOLOGY);t['bridges'][0]['state']='ESTABLISHED COMPATIBLE INTERFACE'
        with self.assertRaises(ValueError):v.check_technology(t)
    def test_handoff_acceptance_invention_rejected(self):
        t=v.load(v.TECHNOLOGY);t['handoffs'][0]['decision']='accepted'
        with self.assertRaises(ValueError):v.check_technology(t)
    def test_missing_reverse_handoff_rejected(self):
        t=v.load(v.TECHNOLOGY);t['handoffs'].pop()
        with self.assertRaises(ValueError):v.check_technology(t)
    def test_energy_boundary_erasure_rejected(self):
        t=v.load(v.TECHNOLOGY);t['contract']['energy_balance']='55.29% system efficiency'
        with self.assertRaises(ValueError):v.check_technology(t)
    def test_missing_material_erasure_rejected(self):
        t=v.load(v.TECHNOLOGY);t['contract']['materials']='Known measured catalyst'
        with self.assertRaises(ValueError):v.check_technology(t)
    def test_topic_routes(self):
        for topic in ['chemistry','physics','quantum','analysis','algorithms','optimization','probability','complexity','methods']:
            v.check_topic(topic,(v.ROOT/('agent/topics/'+topic+'.tsv')).read_text(),(v.ROOT/'agent/topics.txt').read_text())
    def test_topic_header_loss_rejected(self):
        text=(v.ROOT/'agent/topics/chemistry.tsv').read_text().split('\n',1)[1]
        with self.assertRaises(ValueError):v.check_topic('chemistry',text,(v.ROOT/'agent/topics.txt').read_text())
    def test_topic_router_loss_rejected(self):
        router=(v.ROOT/'agent/topics.txt').read_text().replace('chemistry:','missing:')
        with self.assertRaises(ValueError):v.check_topic('chemistry',(v.ROOT/'agent/topics/chemistry.tsv').read_text(),router)
if __name__=='__main__':unittest.main()
