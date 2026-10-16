"""Synthetic-only pre-access feature firewall and serializer tests."""
import copy
import json
import unittest
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor,HistGradientBoostingRegressor
import features as f
import train as t


def synthetic():
    return {'p':[1.,2.],'g_minus_p':[.3,-.4],'prior_disagreement':.02,'history':[{'action':[0.,.1,.2,.3,.4,.5],'start_nm':[.1,.2],'end_nm':[.4,.6],'d':[0.,.2,.1],'current':[1e-9,3e-9,-2e-9]},{'action':[.5,.4,.3,.2,.1,0.],'start_nm':[-.1,.1],'end_nm':[.2,-.3],'d':[0.,.5,.2,.6],'current':[-2e-9,1e-9,4e-9,3e-9]}]}

class Features(unittest.TestCase):
    def test_dimensions_order(self):
        maps=f.feature_maps(synthetic()); schema=f.schema()
        for arm,n in [('A',382),('A+C',457),('A+F',585)]:
            self.assertEqual(len(maps[arm]),n);self.assertEqual(len(schema['arms'][arm]),n)
            self.assertEqual(len(set(schema['arms'][arm])),n)
            self.assertEqual(maps[arm].dtype,np.float64)
        np.testing.assert_array_equal(maps['A'][:7],[1.,2.,.3,-.4,.5,.02,2])
        np.testing.assert_array_equal(maps['A+C'][:382],maps['A'])
        np.testing.assert_array_equal(maps['A+F'][:457],maps['A+C'])
    def test_statistics(self):
        np.testing.assert_allclose(f.S([1.,3.,5.]),[1,5,3,np.sqrt(8/3),1,5,1.4,3,4.6,2,2])
        np.testing.assert_array_equal(f.S([4])[-2:],[0,0])
        np.testing.assert_allclose(f.B([2.,4.]),np.linspace(2,4,32))
        np.testing.assert_array_equal(f.B([2.],16),[2.]*16)
        s=f.current_summary(np.array([0.,0.,0.,10.]))
        self.assertEqual(s[11],.25);self.assertEqual(s[12],.25)
        self.assertEqual(s[13],5.);self.assertEqual(s[14],1e7)
    def test_firewall_all_prohibited(self):
        prohibited=['reward','done','state','next_state','current_state','post_scan_state','atom_absolute_nm','post_scan_coordinates','current_coordinates','distance','current_distance','post_scan_distance','image','img_forward','img_backward','image_extent','terminal','terminal_fields','episode_end_info','scan_trigger_reason','freshness','hash','object_id','image_provenance_id','episode_id','time','regime_index','chronological_index','future_actions','future_episode_length','audit','eligibility','delta','r','y','post_scan_disagreement']
        base=synthetic(); expected=f.feature_maps(base)
        for key in prohibited:
            a=copy.deepcopy(base);a[key]={'sentinel':[float('nan'),float('inf')],'future':'DO NOT READ'}
            for h in a['history']:h[key]=['changed',{'private':-9e99}]
            actual=f.feature_maps(a)
            for arm in t.ARMS:np.testing.assert_array_equal(actual[arm],expected[arm],err_msg=key)
    def test_current_never_changes_action_map(self):
        a=synthetic(); expected=f.feature_maps(a);a['history'][0]['current']=[-9e-9,8e-9,7e-9]
        actual=f.feature_maps(a)
        np.testing.assert_array_equal(actual['A'],expected['A'])
        self.assertFalse(np.array_equal(actual['A+C'],expected['A+C']))
    def test_all_history_included(self):
        a=synthetic();b=copy.deepcopy(a);b['history'][0]['action'][0]=.99
        self.assertFalse(np.array_equal(f.feature_maps(a)['A'],f.feature_maps(b)['A']))
    def test_reject_invalid(self):
        for kind in ('short','unaligned','nonfinite','negative_d','bad_first_d','missing','badshape'):
            a=synthetic();h=a['history'][0]
            if kind=='short':h['d']=[0];h['current']=[0]
            if kind=='unaligned':h['current']=[0,1]
            if kind=='nonfinite':h['current'][0]=float('nan')
            if kind=='negative_d':h['d'][1]=-.1
            if kind=='bad_first_d':h['d'][0]=.01
            if kind=='missing':del h['current']
            if kind=='badshape':h['action']=[1,2]
            with self.assertRaises((ValueError,KeyError)):f.feature_maps(a)
    def test_single_action(self):
        a=synthetic();a['history']=a['history'][:1]
        result=f.feature_maps(a)['A'];names=f.schema()['arms']['A']
        for j in range(6):
            actual=[result[names.index(f'action_B16_action_{j}_{i}')] for i in range(16)]
            np.testing.assert_array_equal(actual,[a['history'][0]['action'][j]]*16)

class Models(unittest.TestCase):
    def test_versions_parameters(self):
        self.assertEqual(t.versions(),t.PINNED)
        p=t.parameters();self.assertEqual(len(p),3)
        self.assertEqual(p[0]['n_estimators'],512);self.assertEqual(p[1]['min_samples_leaf'],8)
        self.assertEqual(p[2]['max_iter'],300);self.assertFalse(p[2]['early_stopping'])
    def test_weights_ties_q_baseline(self):
        np.testing.assert_allclose(t.episode_weights([1,1,2]),[.75,.75,1.5])
        self.assertEqual(t.choose([1+5e-10,1,2]),0)
        self.assertEqual(t.choose([1+2e-9,1,2]),1)
        target=np.zeros((3,2));pred=np.array([[1,0],[2,0],[4,0]])
        self.assertEqual(t.macro_error(pred,target,[1,1,2]),2.75)
        self.assertEqual(t.envelope(pred,target,[1,1,2]),3.8)
        np.testing.assert_array_equal(t.baseline_predictions([synthetic()])['command_request_endpoint'],[[.2,-.3]])
    def test_full_metrics_and_support(self):
        records=[synthetic() for _ in range(3)]
        target=np.zeros((3,2)); pred=np.array([[1,0],[2,0],[4,0]],dtype=float)
        labels=[{'delta':[0,0],'r':.5,'y':0,'disagreement':v} for v in [0.,.2,0.]]
        ids=np.array([1,1,2])
        result=t.metric_summary(pred,target,ids,records,labels)
        self.assertEqual(result['macro_endpoint_error'],2.75)
        self.assertEqual(result['macro_squared_euclidean_error'],9.25)
        self.assertEqual(result['pooled_median_endpoint_error'],2)
        self.assertEqual(result['pooled_p90_endpoint_error'],3.6)
        self.assertEqual(t.quality_strata(pred,target,ids,records,labels)['strata']['above_threshold']['rows'],1)
        paired=t.paired_improvements(pred,target,target,ids)
        self.assertEqual(paired['strict_win_fraction'],1.)
        self.assertEqual(paired['mean'],2.75)
        support=t.classification_support(labels,ids)
        self.assertFalse(support['meets_train_development_requirement'])
        self.assertEqual(support['counts']['0'],{'rows':3,'episodes':2})
    def test_test_access_blocked(self):
        with self.assertRaisesRegex(ValueError,'cannot open test'):t.load_split('/DO_NOT_OPEN','test')
        with self.assertRaisesRegex(RuntimeError,'approval'):t.run('/DO_NOT_OPEN','/DO_NOT_WRITE','bad')
    def test_json_roundtrip_synthetic(self):
        rng=np.random.default_rng(88);X=rng.normal(size=(80,7));Y=np.c_[X[:,0]**2+X[:,1],X[:,2]-X[:,3]];w=t.episode_weights(np.repeat(np.arange(20),4))
        # Serializer implementation checks use synthetic data and small trees only.
        e=ExtraTreesRegressor(n_estimators=7,min_samples_leaf=2,random_state=t.SEED,n_jobs=1).fit(X,Y,sample_weight=w)
        h=[HistGradientBoostingRegressor(max_iter=5,min_samples_leaf=3,early_stopping=False,random_state=t.SEED).fit(X,Y[:,j],sample_weight=w) for j in range(2)]
        for model,expected in [(e,e.predict(X)),(h,np.column_stack([m.predict(X) for m in h]))]:
            snapshot=json.loads(t.canonical(t.freeze_model(model)))
            np.testing.assert_allclose(t.predict_frozen(snapshot,X),expected,atol=1e-12,rtol=1e-12)
            X2=rng.normal(size=(30,7))
            expected=e.predict(X2) if model is e else np.column_stack([m.predict(X2) for m in h])
            np.testing.assert_allclose(t.predict_frozen(snapshot,X2),expected,atol=1e-12,rtol=1e-12)

if __name__=='__main__':unittest.main(verbosity=2)
