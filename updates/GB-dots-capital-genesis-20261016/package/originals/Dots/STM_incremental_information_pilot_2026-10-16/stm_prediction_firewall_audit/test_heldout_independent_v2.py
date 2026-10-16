"""Independent synthetic-only held-out evaluator checks. No real pilot files accessed."""
import sys,copy,unittest
from pathlib import Path
from unittest import mock
sys.path.insert(0,str(Path(__file__).parent/'heldout_corrected'))
import numpy as np
import train,prediction_stage as stage,evaluate_once as ev
from test_heldout_stages import SyntheticStages

class Gates(unittest.TestCase):
    def setUp(self):
        self.records=[{'g_minus_p':[.1,0.]} for _ in range(60)]
        self.routing=[{'episode_id':i,'transition_index':0} for i in sum(stage.BLOCKS,[])]
        self.labels=[{'delta':[.5,0.],'r':.4,'y':0,'disagreement':0.} for _ in range(60)]
        self.fit={'selected':{a:{'candidate':1,'q':.1} for a in train.ARMS},'classification_support':{s:{'counts':{str(y):{'rows':30,'episodes':20} for y in (0,1)}} for s in ('train','development')}}
        self.p={f'{a}:{i}':np.tile([v,0.],(60,1)) for a,v in [('A',.3),('A+C',.4),('A+F',.45)] for i in (1,2,3)}
        self.p.update({'persistence':np.zeros((60,2)),'command_request_endpoint':np.tile([.05,0.],(60,1))})
    def result(self):return ev.report(self.p,self.records,self.routing,self.labels,self.fit)
    def change(self,arm,v):
        for i in (1,2,3):self.p[f'{arm}:{i}'][:]=[v,0.]
    def test_all_six_go_conditions(self):
        r=self.result();self.assertEqual(r['screening']['decision'],'GO');self.assertEqual(len(r['screening']['conditions']),6)
        self.assertTrue(all(r['screening']['conditions'].values()));self.assertFalse(r['classification']['available'])
        self.assertAlmostEqual(r['paired']['A+F_versus_A']['mean'],.15)
    def test_relative_gate_independent(self):
        self.change('A',.1);self.change('A+F',.13)
        c=self.result()['screening']['conditions'];self.assertFalse(c['relative_reduction_at_least_10_percent']);self.assertTrue(c['absolute_reduction_at_least_0_02_nm'])
    def test_absolute_gate_independent(self):
        self.change('A',.4);self.change('A+F',.415)
        c=self.result()['screening']['conditions'];self.assertTrue(c['relative_reduction_at_least_10_percent']);self.assertFalse(c['absolute_reduction_at_least_0_02_nm'])
    def test_each_block_and_win_fraction_separate(self):
        for i in (1,2,3):self.p[f'A+F:{i}'][:20]=[.29,0.]
        c=self.result()['screening']['conditions'];self.assertFalse(c['positive_improvement_in_each_fixed_block']);self.assertTrue(c['strict_episode_win_fraction_at_least_60_percent'])
        for i in (1,2,3):
            self.p[f'A+F:{i}'][:]=[.45,0.];self.p[f'A+F:{i}'][::2]=[.29,0.]
        c=self.result()['screening']['conditions'];self.assertTrue(c['positive_improvement_in_each_fixed_block']);self.assertFalse(c['strict_episode_win_fraction_at_least_60_percent'])
    def test_two_paired_candidates_required(self):
        for i in (2,3):self.p[f'A+F:{i}'][:]=[.29,0.]
        c=self.result()['screening']['conditions'];self.assertFalse(c['at_least_two_same_hyperparameter_improvements']);self.assertTrue(c['strict_episode_win_fraction_at_least_60_percent'])
    def test_baseline_strictly_better_required(self):
        self.p['persistence'][:]=[.45,0.]
        self.assertFalse(self.result()['screening']['conditions']['beats_both_baselines'])
    def test_selection_not_rechosen_on_test(self):
        self.p['A+F:1'][:]=[.1,0.]
        r=self.result();self.assertAlmostEqual(r['metrics']['A+F']['macro_endpoint_error'],.4)
        self.assertEqual(r['selected_models']['A+F']['candidate'],1)

class Marker(unittest.TestCase):
    def test_marker_committed_before_label_open_and_failure_burns(self):
        fixture=SyntheticStages();fixture.setUp()
        try:
            ph=fixture.predict();original=Path.read_bytes;opened=[]
            def read(path,*args,**kwargs):
                if path==fixture.labelpath:
                    marker=fixture.root/'sealed/TEST_EVALUATION_STARTED.json'
                    self.assertTrue(marker.is_file());opened.append(path)
                    raise RuntimeError('synthetic failure at first label access')
                return original(path,*args,**kwargs)
            with mock.patch.object(Path,'read_bytes',read):
                with self.assertRaisesRegex(RuntimeError,'synthetic failure'):fixture.evaluate(ph)
                with self.assertRaises(FileExistsError):fixture.evaluate(ph,fixture.root/'alternate.json')
            self.assertEqual(len(opened),1);self.assertFalse(fixture.out.exists())
        finally:fixture.tearDown()

if __name__=='__main__':unittest.main(verbosity=2)
