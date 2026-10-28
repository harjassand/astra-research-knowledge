"""Guard the acquired observable,correct proof branch and calibration boundary."""
import hashlib,json,re,unittest
from knowledge.model import ROOT,Inputs
BASE='research/2026-10-28-reciprocal-receiver/'
class ReciprocalReceiverScope(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.records={}
  with(ROOT/'knowledge/current/records.jsonl').open()as stream:
   for line in stream:
    row=json.loads(line)
    if row['id'].startswith(('N1129-','U1129-')):cls.records[row['id']]=row
  cls.transfers={v['id']:v for v in json.loads((ROOT/'knowledge/current/transfers.json').read_bytes())if v['id'].startswith('B1129-')}
 def test_actual_originals_and_only_portable_report_locators(self):
  a=json.loads((ROOT/BASE/'source/AVAILABILITY.json').read_bytes());self.assertEqual(len(a['public_files']),5)
  for r in a['public_files']:
   data=(ROOT/BASE/r['path']).read_bytes();self.assertEqual(len(data),r['bytes']);self.assertEqual(hashlib.sha256(data).hexdigest(),r['sha256'])
  report=(ROOT/BASE/'source/CONTINUATION_REPORT_PORTABLE.md').read_text()
  scientific_text=re.sub(r'\]\((?:sandbox:[^)]+|originals/[^)]+|unacquired-archive/[^)]+)\)','](<source-resource>)',report)
  self.assertEqual(hashlib.sha256(scientific_text.encode()).hexdigest(),a['portable_final_report']['non_resource_text_sha256'])
 def test_completed_math_review_does_not_acquire_archive_execution(self):
  self.assertEqual(len(self.records),11)
  for identifier,r in self.records.items():
   accepted=[v for v in r['review_overlays']if v['decision']=='accepted_internally_verified'];self.assertEqual(len(accepted),1)
   self.assertIn({'id':identifier,'content_version':r['content_version']},accepted[0]['subjects'])
   self.assertTrue(any('unacquired' in g.lower()for g in accepted[0]['remaining_gaps']))
  a=json.loads((ROOT/BASE/'source/AVAILABILITY.json').read_bytes());self.assertEqual(a['archive']['status'],'UNACQUIRED_ACCESS_DENIED')
  _,proof=Inputs(ROOT).source(self.records['U1129-clipped-three-load-lipschitz']['evidence'][0]);self.assertIn('F_r` is not convex',proof)
  self.assertIn('K_r=1/r+3r+8',proof)
 def test_returned_counterexample_and_reconstruction_routes_are_correct_branches(self):
  _,failure=Inputs(ROOT).source(self.records['U1129-one-nonzero-load-ambiguity']['evidence'][0]);self.assertIn('S2=[[0,1/5],[1/5,18/25]]',failure);self.assertIn('-1/68',failure)
  _,gram=Inputs(ROOT).source(self.records['U1129-pivot-all-input-gram']['evidence'][0])
  self.assertIn('G_hat=q_hat q_hat*/D',gram);self.assertIn('D<=4delta',gram);self.assertIn('11n delta',gram)
  _,cal=Inputs(ROOT).source(self.records['U1129-shared-calibration-relative-interval']['evidence'][0]);self.assertIn('Theta<1 and gL>0',cal);self.assertIn('Do not cap',cal)
 def test_qualified_scalar_interface_and_phase_commonality_mismatch(self):
  self.assertEqual(len(self.transfers),3)
  for t in self.transfers.values():
   self.assertEqual(t['from_version'],self.records[t['from']]['content_version']);self.assertEqual(t['to_version'],self.records[t['to']]['content_version'])
   for ref in t['evidence']:Inputs(ROOT).source(ref)
   if t['state']=='ESTABLISHED COMPATIBLE INTERFACE':
    self.assertIn('fixed',t['slot_binding']['object']);self.assertIn('simultaneous',t['slot_binding']['qualification']);self.assertEqual(t['slot_binding']['slot'],'uniform_scalar_power')
   else:self.assertEqual(t['state'],'INCOMPATIBLE ASSUMPTIONS');self.assertNotIn('slot_binding',t)
  consumer=self.records['U1129-pivot-all-input-gram'];self.assertEqual(len(consumer['interface_navigation']['bindings']),2)
if __name__=='__main__':unittest.main()
