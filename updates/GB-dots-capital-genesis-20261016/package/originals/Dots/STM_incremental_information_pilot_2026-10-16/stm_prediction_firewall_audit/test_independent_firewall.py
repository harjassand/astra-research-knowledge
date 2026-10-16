"""Independent audit. Imports preserved submission; uses synthetic data only except burned schema template."""
import sys,copy,json,unittest
from pathlib import Path
import numpy as np
HERE=Path(__file__).parent
sys.path.insert(0,str(HERE/'submitted'))
import audit,features,train
from sklearn.ensemble import ExtraTreesRegressor,HistGradientBoostingRegressor
BURNED=audit.CONTROL/'acquired/training_data_and_model_parameters/training_data/00000.npy'

def arr(template,values):
    v=copy.deepcopy(template);a=np.asarray(values,dtype='<'+audit.dtype(v.state[2]))
    v.state=(v.state[0],a.shape,v.state[2],False,a.tobytes());return v

def graph(fresh=(False,False,True,False,True), positions=None):
    root=audit.parse(BURNED);e=root.state[4][0];orig=copy.deepcopy(e['transitions']);start=e['episode_start_info']
    template=start['info']['start_absolute_nm'];pos=[0.,0.];goal=[3.,4.]
    for k in start['info']:
        start['info'][k]=arr(template,goal if k.startswith('goal') else pos)
    # Small synthetic image grids and fresh IDs; no diagnostic image values enter features.
    for k in audit.IMAGES:start[k]=arr(start[k],np.zeros((2,2)))
    t={k:[] for k in orig};prev=start
    for j,isfresh in enumerate(fresh):
        info=copy.deepcopy(orig['info'][0])
        if isfresh:
            prev=copy.deepcopy(prev)
            for k in audit.IMAGES:prev[k]=arr(start[k],np.full((2,2),j+1.))
            pos=positions[j] if positions and j in positions else [float(j+1),float(-j)]
        info['img_info']=prev
        for k in info:
            if k.startswith('atom_'):info[k]=arr(template,pos)
        info['current_series']=arr(template,[j*1e-9, (j+1)*1e-9, (j-1)*1e-9])
        info['d']=arr(template,[0.,.2+j*.1,.1])
        info['start_nm']=arr(template,[j*.01,-j*.01]);info['end_nm']=arr(template,[j*.1,-j*.1])
        info['dist_destination']=999.-j
        t['info'].append(info);t['action'].append(arr(orig['action'][0],[j*.1]*6))
        t['state'].append(arr(orig['state'][0],[99,98,97,96]));t['next_state'].append(arr(orig['next_state'][0],[101,102,103,104]))
        t['reward'].append(float(j+500));t['done'].append(j==len(fresh)-1)
    end=copy.deepcopy(e['episode_end_info'])
    for k in audit.IMAGES:end[k]=prev[k]
    end['offset_nm']=prev['offset_nm'];end['len_nm']=prev['len_nm']
    end['atom_absolute_nm']=arr(template,pos);end['atom_relative_nm']=arr(template,pos)
    e['transitions']=t;e['episode_end_info']=end
    return root

def run(root):return audit.episode(None,666,'synthetic',root)

def maps(x):return [features.feature_maps(r) for r in x['rows']]

class BuilderFirewall(unittest.TestCase):
    def test_prefix_reuse_and_anchor_clock(self):
        x=run(graph());self.assertEqual([r['transition_index'] for r in x['routing']],[2,4])
        self.assertEqual([len(r['history']) for r in x['rows']],[3,2])
        np.testing.assert_array_equal(x['rows'][0]['p'],[0,0]);np.testing.assert_array_equal(x['rows'][1]['p'],[3,-2])
        np.testing.assert_array_equal(x['labels'][0]['delta'],[3,-2]);np.testing.assert_array_equal(x['labels'][1]['delta'],[2,-2])
        self.assertEqual(x['rows'][0]['history'][0]['current'],[0,1e-9,-1e-9])
    def test_current_target_not_current_feature(self):
        a=run(graph());b=run(graph(positions={4:[300.,-200.]}))
        for x,y in zip(maps(a),maps(b)):
            for arm in train.ARMS:np.testing.assert_array_equal(x[arm],y[arm])
        self.assertNotEqual(a['labels'][-1],b['labels'][-1])
    def test_prior_target_becomes_next_anchor_only(self):
        a=run(graph());b=run(graph(positions={2:[30.,-20.]}))
        for arm in train.ARMS:np.testing.assert_array_equal(maps(a)[0][arm],maps(b)[0][arm])
        self.assertNotEqual(a['rows'][1]['p'],b['rows'][1]['p'])
        self.assertEqual(a['rows'][1]['history'],b['rows'][1]['history'])
    def test_reward_state_distance_and_routing_invariance(self):
        r=graph();a=run(r);t=r.state[4][0]['transitions']
        for j in range(len(t['action'])):
            t['reward'][j]=-1e100;t['state'][j]=arr(t['state'][j],[-1e9]*4);t['next_state'][j]=arr(t['next_state'][j],[1e10]*4);t['info'][j]['dist_destination']=-1e80
        b=audit.episode(None,999999,'different_routing',r)
        self.assertEqual(a['rows'],b['rows'])
    def test_future_length_invariance(self):
        a=run(graph((False,False,True)));b=run(graph())
        self.assertEqual(a['rows'][0],b['rows'][0]);self.assertEqual(a['labels'][0],b['labels'][0])
    def test_missing_trace_discards_then_reanchors(self):
        r=graph();t=r.state[4][0]['transitions'];t['info'][1]['current_series']=None
        x=run(r);self.assertEqual([r['transition_index'] for r in x['routing']],[4]);self.assertEqual(len(x['rows'][0]['history']),2);self.assertEqual(x['rows'][0]['p'],[3,-2])
    def test_ambiguous_then_reestablish_anchor(self):
        r=graph((False,True,True,True,True));e=r.state[4][0];im=e['transitions']['info'][1]['img_info']
        for k in audit.IMAGES:im[k]=copy.deepcopy(e['episode_start_info'][k])
        x=run(r);self.assertEqual([r['transition_index'] for r in x['routing']],[3,4]);self.assertEqual(x['rows'][0]['p'],[3,-2])
    def test_early_history_current_and_d_survive(self):
        r=graph();a=maps(run(r))[0];t=r.state[4][0]['transitions'];t['info'][0]['current_series']=arr(t['info'][0]['current_series'],[9e-9,2e-9,-8e-9]);b=maps(run(r))[0]
        np.testing.assert_array_equal(a['A'],b['A']);self.assertFalse(np.array_equal(a['A+C'],b['A+C']))
        t['info'][0]['d']=arr(t['info'][0]['d'],[0,.8,.9]);c=maps(run(r))[0]
        self.assertFalse(np.array_equal(b['A'],c['A']))
        for arm in train.ARMS:np.testing.assert_array_equal(c[arm][:382],c['A'])

class Snapshots(unittest.TestCase):
    def test_threshold_neighborhoods(self):
        rng=np.random.default_rng(8128);X=rng.normal(size=(180,5));Y=np.c_[X[:,0]+X[:,1]**2,X[:,3]-X[:,2]**2]
        w=train.episode_weights(np.r_[np.repeat(1,130),np.arange(50)+2])
        et=ExtraTreesRegressor(n_estimators=9,min_samples_leaf=2,random_state=51,n_jobs=1).fit(X,Y,sample_weight=w)
        hg=[HistGradientBoostingRegressor(max_iter=9,min_samples_leaf=5,max_leaf_nodes=8,early_stopping=False,random_state=51).fit(X,Y[:,j],sample_weight=w) for j in (0,1)]
        for model in (et,hg):
            snap=json.loads(train.canonical(train.freeze_model(model)));rows=[*rng.normal(size=(50,5))]
            trees=snap['trees'] if model is et else [t for c in snap['coordinates'] for t in c['trees']]
            for tree in trees:
                for k,(f,threshold) in enumerate(zip(tree['feature'],tree['threshold'])):
                    isleaf=tree['left'][k]==-1 if model is et else tree['leaf'][k]
                    if isleaf:continue
                    for val in (threshold,np.nextafter(threshold,-np.inf),np.nextafter(threshold,np.inf),float(np.float32(threshold))):
                        row=np.zeros(5);row[f]=val;rows.append(row)
            Q=np.asarray(rows);expected=model.predict(Q) if model is et else np.column_stack([m.predict(Q) for m in model])
            np.testing.assert_allclose(train.predict_frozen(snap,Q),expected,atol=1e-12,rtol=1e-12)
    def test_unequal_episode_objective_and_tie_boundary(self):
        ids=[1]*100+[2];w=train.episode_weights(ids)
        self.assertAlmostEqual(sum(w[:100]),w[-1]);self.assertAlmostEqual(w.mean(),1.)
        pred=np.c_[np.r_[np.ones(100),11],np.zeros(101)];self.assertEqual(train.macro_error(pred,np.zeros((101,2)),ids),6.)
        self.assertEqual(train.choose([1.000000002,1.0000000005,1]),1)

if __name__=='__main__':unittest.main(verbosity=2)
