"""Synthetic fixtures ONLY. Does not inspect real sanitized/test or sealed data."""
import copy
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import numpy as np
import train
import prediction_stage as stage
import evaluate_once as ev
from seal_labels import seal_labels

class SyntheticStages(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='stm_synthetic_'); self.root=Path(self.tmp.name)
        self.fitdir=self.root/'fits'; self.fitdir.mkdir(); self.data=self.root/'sanitized'; self.data.mkdir(); (self.root/'sealed').mkdir()
        self.protocol=self.root/'protocol.md'; self.protocol.write_text('synthetic protocol fixture')
        self.manifest=self.root/'manifest.json'; train.save_new(self.manifest,{'splits':{'test':{'episodes':[{'episode_id':i} for i in sum(stage.BLOCKS,[])]}}})
        self.audit=self.root/'audit.json'; train.save_new(self.audit,{'status':'PASS','audit_code_sha256':train.digest(stage.HERE/'audit.py'),'counts':{'test':{'eligible_episodes':60,'eligible_boundaries':120}}})
        record={'p':[0.,0.],'g_minus_p':[.1,0.],'prior_disagreement':0.,'history':[{'action':[0.]*6,'start_nm':[0.,0.],'end_nm':[.05,0.],'d':[0.,.1],'current':[1e-9,2e-9]}]}
        self.records=[copy.deepcopy(record) for _ in range(120)]
        self.routing=[{'episode_id':eid,'transition_index':i} for eid in sum(stage.BLOCKS,[]) for i in (0,1)]
        self.labels=[{'delta':[0. if j%2==0 else .5,0.],'r':.1 if j%2==0 else .4,'y':int(j%2==0),'disagreement':0. if j%2==0 else .2} for j in range(120)]
        def write_rows(path,rows): path.write_text(''.join(json.dumps(r)+'\n' for r in rows))
        for split in ('train','development','test'):
            write_rows(self.data/f'{split}_inputs.jsonl',self.records); write_rows(self.data/f'{split}_routing.jsonl',self.routing)
            if split!='test': write_rows(self.data/f'{split}_labels.jsonl',self.labels)
        self.labelpath=self.root/'sealed/test_labels.jsonl'; write_rows(self.labelpath,self.labels); self.labelpath.chmod(0o400)
        train.save_new(self.fitdir/'feature_schema.json',stage.schema())
        model_hashes={}
        for arm in train.ARMS:
            for i in (1,2,3):
                name=f'{arm.replace("+","_")}_{i}.json'
                model={'kind':'extra_trees','n_features':len(stage.schema()['arms'][arm]),'trees':[{'left':[-1],'right':[-1],'feature':[-2],'threshold':[-2.],'value':[[0.,0.]]}]}
                train.save_new(self.fitdir/name,model); model_hashes[name]=train.digest(self.fitdir/name)
        self.fit={'protocol_sha256':train.digest(self.protocol),'audit_report_sha256':train.digest(self.audit),'versions':train.versions(),'schema_hash':stage.schema_hash(),'candidate_parameters':train.parameters(),'model_hashes':model_hashes,'code_hashes':{n:train.digest(stage.HERE/n) for n in ('features.py','train.py','test_features_train.py')},'input_hashes':{f'{s}_{k}.jsonl':train.digest(self.data/f'{s}_{k}.jsonl') for s in ('train','development') for k in ('inputs','routing','labels')},'selected':{a:{'candidate':1,'model_file':f'{a.replace("+","_")}_1.json','q':.5} for a in train.ARMS},'development_candidates':{f'{a}:{i}':{'macro_endpoint_error':1.} for a in train.ARMS for i in (1,2,3)},'classification_support':{s:{'counts':{str(y):{'rows':60,'episodes':60} for y in (0,1)},'meets_train_development_requirement':True} for s in ('train','development')}}
        train.save_new(self.fitdir/'fit_lock.json',self.fit); train.save_new(self.fitdir/'fit_lock.sha256.json',{'sha256':train.digest(self.fitdir/'fit_lock.json')})
        self.lock=self.root/'lock.json'; self.pred=self.root/'predictions.json'; self.out=self.root/'result.json'
        self.seal=self.root/'label_seal.json'; self.sh=seal_labels(self.data,self.seal,'ROOT_LABEL_HASH_ONLY_APPROVED')
        self.lh=stage.freeze(self.fitdir,self.data,self.protocol,self.manifest,self.audit,self.seal,self.sh,self.lock,'ROOT_FREEZE_APPROVED')
    def tearDown(self): self.tmp.cleanup()
    def predict(self): return stage.predict(self.lock,self.lh,self.pred,'ROOT_PREDICTION_APPROVED')
    def evaluate(self,ph,output=None): return ev.evaluate(self.lock,self.lh,self.pred,ph,output or self.out,'ROOT_ONE_SHOT_EVALUATION_APPROVED')
    def test_predict_never_opens_labels_and_end_to_end_metrics(self):
        rb=Path.read_bytes; rt=Path.read_text
        def forbid_bytes(path,*a,**k):
            if path==self.labelpath: raise AssertionError('Prediction opened labels')
            return rb(path,*a,**k)
        def forbid_text(path,*a,**k):
            if path==self.labelpath: raise AssertionError('Prediction opened labels')
            return rt(path,*a,**k)
        with mock.patch.object(Path,'read_bytes',forbid_bytes),mock.patch.object(Path,'read_text',forbid_text): ph=self.predict()
        result_hash=self.evaluate(ph); self.assertEqual(train.digest(self.out),result_hash)
        result=stage.read_json(self.out)
        self.assertAlmostEqual(result['metrics']['A']['macro_endpoint_error'],.25)
        self.assertAlmostEqual(result['metrics']['A']['macro_squared_euclidean_error'],.125)
        self.assertAlmostEqual(result['metrics']['A']['macro_absolute_target_radius_error'],.15)
        self.assertEqual(result['empirical_residual_envelopes']['A']['fraction_episodes_every_residual_within_q'],1.)
        self.assertEqual(result['metrics']['A']['label_quality']['strata']['above_threshold']['rows'],60)
        self.assertEqual(len(result['same_hyperparameter_paired']),3)
        self.assertEqual(result['chronology_blocks']['2']['planned_episode_ids'],stage.BLOCKS[1])
        self.assertEqual(result['classification']['metrics']['A']['balanced_accuracy'],.5)
        self.assertEqual(result['screening']['decision'],'NO-GO')
        with self.assertRaises(FileExistsError): self.evaluate(ph,self.root/'alternate.json')
        self.assertEqual(self.labelpath.stat().st_mode & 0o777,0o400)
    def test_failure_consumes_evaluation(self):
        ph=self.predict(); self.labelpath.chmod(0o600); self.labelpath.write_text('{invalid json}\n'); self.labelpath.chmod(0o400)
        with self.assertRaisesRegex(ValueError,'digest mismatch'): self.evaluate(ph)
        self.assertTrue((self.root/'sealed/TEST_EVALUATION_STARTED.json').exists())
        with self.assertRaises(FileExistsError): self.evaluate(ph,self.root/'another.json')
        self.assertFalse(self.out.exists())
    def test_valid_changed_labels_rejected_before_parsing(self):
        ph=self.predict(); changed=copy.deepcopy(self.labels); changed[0]={'delta':[.5,0.],'r':.4,'y':0,'disagreement':0.}
        self.labelpath.chmod(0o600); self.labelpath.write_text(''.join(json.dumps(r)+'\n' for r in changed)); self.labelpath.chmod(0o400)
        with mock.patch.object(ev,'report',side_effect=AssertionError('Must not score changed labels')):
            with self.assertRaisesRegex(ValueError,'digest mismatch'): self.evaluate(ph)
        with self.assertRaises(FileExistsError): self.evaluate(ph,self.root/'different.json')
        self.assertFalse(self.out.exists())
    def test_label_seal_requires_approval_and_does_not_decode(self):
        output=self.root/'new_seal.json'
        with self.assertRaisesRegex(ValueError,'Separate root hash-only'): seal_labels(self.data,output,'no')
        self.assertFalse(output.exists())
        self.labelpath.chmod(0o600); raw=b'\xff\x00invalid json'; self.labelpath.write_bytes(raw); self.labelpath.chmod(0o400)
        with mock.patch.object(json,'loads',side_effect=AssertionError('Seal must not parse JSON')),mock.patch.object(Path,'read_text',side_effect=AssertionError('Seal must not decode')):
            seal_labels(self.data,output,'ROOT_LABEL_HASH_ONLY_APPROVED')
        self.assertEqual(stage.read_json(output)['label_sha256'],train.hashlib.sha256(raw).hexdigest())
    def test_no_label_access_before_evaluation_marker(self):
        ph=self.predict(); original=Path.read_bytes; calls=[]
        def guard(path,*a,**k):
            if path==self.labelpath:
                self.assertTrue((self.root/'sealed/TEST_EVALUATION_STARTED.json').exists()); calls.append(str(path))
            return original(path,*a,**k)
        with mock.patch.object(Path,'read_bytes',guard):
            stage.verify_lock(self.lock,self.lh)
            self.assertEqual(calls,[])
            self.evaluate(ph)
        self.assertEqual(calls,[str(self.labelpath)])
    def test_hash_mutation_prevents_prediction(self):
        (self.fitdir/'A_3.json').write_text('{}')
        with self.assertRaisesRegex(ValueError,'Hash mismatch'): self.predict()
        self.assertFalse(self.pred.exists())
    def test_prediction_hash_mutation_rejected_before_labels(self):
        ph=self.predict(); self.pred.write_text(self.pred.read_text()+' ')
        with self.assertRaisesRegex(ValueError,'Hash mismatch'): self.evaluate(ph)
        self.assertFalse((self.root/'sealed/TEST_EVALUATION_STARTED.json').exists())
    def test_support_only_unavailable(self):
        fit=copy.deepcopy(self.fit); fit['classification_support']['train']['counts']['0']['rows']=19
        preds={'A':np.zeros((120,2))}
        r=ev.classification(preds,self.records,self.labels,np.array([x['episode_id'] for x in self.routing]),fit)
        self.assertFalse(r['available']); self.assertNotIn('metrics',r); self.assertIn('support',r)
        labels=[{**r,'y':1} for r in self.labels]
        r=ev.classification(preds,self.records,labels,np.array([x['episode_id'] for x in self.routing]),self.fit)
        self.assertFalse(r['available']); self.assertNotIn('metrics',r)
    def test_approval_required_and_prediction_one_shot(self):
        with self.assertRaisesRegex(ValueError,'Root prediction approval'): stage.predict(self.lock,self.lh,self.pred,'no')
        ph=self.predict()
        with self.assertRaises(FileExistsError): stage.predict(self.lock,self.lh,self.root/'second.json','ROOT_PREDICTION_APPROVED')
        with self.assertRaisesRegex(ValueError,'Separate root'): ev.evaluate(self.lock,self.lh,self.pred,ph,self.out,'no')
    def test_macro_episode_weighting_and_pairing(self):
        ids=np.array([2201,2201,2211]); y=np.zeros((3,2)); p=np.array([[1.,0.],[3.,0.],[8.,0.]])
        self.assertEqual(train.macro_error(p,y,ids),5.)
        paired=train.paired_improvements(p,p/2,y,ids)
        self.assertEqual(paired['mean'],2.5); self.assertEqual(paired['strict_win_fraction'],1.)
    def test_fixed_blocks_survive_exclusions(self):
        rows=[0,40,80]; records=[self.records[i] for i in rows]; routing=[self.routing[i] for i in rows]; labels=[self.labels[i] for i in rows]
        preds={f'{a}:{i}':[[0.,0.]]*3 for a in train.ARMS for i in (1,2,3)}; preds.update({'persistence':[[0.,0.]]*3,'command_request_endpoint':[[.05,0.]]*3})
        r=ev.report(preds,records,routing,labels,self.fit)
        for i in (1,2,3): self.assertEqual(r['chronology_blocks'][str(i)]['planned_episode_ids'],stage.BLOCKS[i-1])
        self.assertEqual(r['chronology_blocks']['2']['eligible_episode_ids'],[2401])

if __name__=='__main__': unittest.main()
