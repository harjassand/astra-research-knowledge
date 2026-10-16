"""Synthetic graph mutations of burned data only; no selected episode access."""
import copy, unittest
import audit
P=audit.CONTROL/'acquired/training_data_and_model_parameters/training_data/00000.npy'
class AuditTests(unittest.TestCase):
    def root(self):return audit.parse(P)
    def test_burned_pass(self):
        for eid in (0,1500,2920):
            x=audit.episode(audit.CONTROL/f'acquired/training_data_and_model_parameters/training_data/{eid:05d}.npy',eid,'burned')
            self.assertGreater(len(x['rows']),0)
            self.assertEqual(set(x['rows'][0]),{'p','g_minus_p','prior_disagreement','history'})
    def test_mixed_freshness(self):
        r=self.root();e=r.state[4][0]
        e['transitions']['info'][0]['img_info']['img_forward']=e['episode_start_info']['img_forward']
        with self.assertRaises(audit.GateError):audit.episode(P,0,'burned',r)
    def test_missing_trace_reanchor(self):
        r=self.root();e=r.state[4][0];e['transitions']['info'][0]['current_series']=None;e['transitions']['info'][0]['d']=None
        x=audit.episode(P,0,'burned',r)
        self.assertEqual(x['row_exclusions']['missing_trace'],1)
        self.assertTrue(all(row['transition_index']!=0 for row in x['routing']))
        self.assertGreater(len(x['rows']),0)
    def test_copied_pair_ambiguity(self):
        r=self.root();e=r.state[4][0];im=e['transitions']['info'][0]['img_info'];start=e['episode_start_info']
        for k in audit.IMAGES:im[k]=copy.deepcopy(start[k])
        x=audit.episode(P,0,'burned',r)
        self.assertGreater(x['row_exclusions'].get('copied_or_unchanged_new_pair',0),0)
        self.assertTrue(all(row['transition_index']!=0 for row in x['routing']))
    def test_nonadjacent_copy(self):
        r=self.root();e=r.state[4][0];im=e['transitions']['info'][1]['img_info'];start=e['episode_start_info']
        for k in audit.IMAGES:im[k]=copy.deepcopy(start[k])
        x=audit.episode(P,0,'burned',r)
        self.assertGreater(x['row_exclusions'].get('copied_or_unchanged_new_pair',0),0)
        self.assertTrue(all(row['transition_index']!=1 for row in x['routing']))
    def test_transitive_components(self):
        def ep(i,s,hs):return {'episode_id':i,'split':s,'fingerprints':set(hs)}
        xs=[ep(0,'burned',['a']),ep(1,'train',['a','b']),ep(11,'train',['b','c']),ep(1401,'development',['c']),ep(21,'train',['d']),ep(31,'train',['d']),ep(2201,'test',['e'])]
        eligible,excluded=audit.deduplicate(xs)
        self.assertEqual([x['episode_id'] for x in eligible],[21,2201])
        self.assertEqual(len(excluded),4)
    def test_hash_graph_survives_exclusion(self):
        r=self.root();h,_=audit.collect_images(r);r.state[4][0]['transitions']['action']=[]
        h2,_=audit.collect_images(r);self.assertEqual(h,h2)
        with self.assertRaises(audit.GateError):audit.episode(P,0,'burned',r)
    def test_declared_mapping_not_inferred(self):
        r=self.root();e=r.state[4][0];v=e['transitions']['info'][0]['start_nm'];v.state=(*v.state[:4],audit.struct.pack('<dd',.001,.002))
        x=audit.episode(P,0,'burned',r);self.assertEqual(x['rows'][0]['history'][0]['start_nm'],[.001,.002])
if __name__=='__main__':unittest.main()
