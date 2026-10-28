"""Protect actual proof branches,review versions and incompatible interfaces."""
import hashlib,json,runpy,unittest
from knowledge.model import ROOT,Inputs
B=ROOT/'research/2026-10-28-constructive-matrix-interfaces'

class ConstructiveMatrixScope(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.records={r['id']:r for r in map(json.loads,(ROOT/'knowledge/current/records.jsonl').read_text().splitlines())if r['id'].startswith(('N1130-','N1131-','N1132-','U1130-','U1131-','U1132-'))}

 def test_actual_review_versions_and_guard_only_section_delta(self):
  a=json.loads((B/'source/AVAILABILITY.json').read_bytes())['section_version_relationship']
  for f in a['files']:
   p=B/'source/originals/new_work'/f['path']
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),f['sha256'])
  p=B/'source/originals/new_work/independent_audit/acquired_affine_section.py'
  historical=p.read_bytes().replace(b'sys.dont_write_bytecode = True\n',b'')
  self.assertEqual(hashlib.sha256(historical).hexdigest(),a['section_prior_review_code_sha256'])
  self.assertNotEqual(a['section_current_code_sha256'],a['section_prior_review_code_sha256'])

 def test_math_acceptance_does_not_invent_a_timing_replay(self):
  self.assertEqual(len(self.records),17)
  for identifier,r in self.records.items():
   accepted=[v for v in r['review_overlays']if v['decision']=='accepted_internally_verified']
   if identifier=='U1130-matched-comparison-boundary':self.assertEqual(accepted,[])
   else:
    self.assertEqual(len(accepted),1)
    self.assertIn(dict(id=identifier,content_version=r['content_version']),accepted[0]['subjects'])

 def test_governing_routes_keep_original_translation_and_two_distinct_methods(self):
  r=self.records['U1130-original-affine-reconstruction']
  _,passage=Inputs(ROOT).source(r['evidence'][1])
  self.assertIn('c+L(u_0)',passage)
  self.assertIn('u\'+u_0',passage)
  section=self.records['U1131-one-copy-section-boundary']
  _,passage=Inputs(ROOT).source(section['evidence'][0])
  self.assertIn('unequal sizes',passage)
  self.assertIn('not a uniform full-fiber',passage)
  census=self.records['U1132-two-flag-census']
  _,passage=Inputs(ROOT).source(census['evidence'][0])
  self.assertIn('29',passage)
  self.assertIn('E_1',passage)
  self.assertIn('E_2',passage)

 def test_exact_prefix_binding_and_radical_incompatibility(self):
  transfers=[t for t in json.loads((ROOT/'knowledge/current/transfers.json').read_bytes())if t['id'].startswith('B1130-')]
  self.assertEqual(len(transfers),4)
  for t in transfers:
   self.assertEqual(t['from_version'],self.records[t['from']]['content_version'])
   self.assertEqual(t['to_version'],self.records[t['to']]['content_version'])
   for ref in t['evidence']:Inputs(ROOT).source(ref)
  typed=next(t for t in transfers if 'slot_binding'in t)
  self.assertEqual(typed['slot_binding']['slot'],'conditional_population')
  self.assertIn('nonnegative',typed['slot_binding']['observable'])
  failure=next(t for t in transfers if t['state']=='INCOMPATIBLE ASSUMPTIONS')
  self.assertNotIn('slot_binding',failure)
  self.assertIn('not hardness',failure['remaining_obligations'])

 def test_independent_finite_failure_and_uniformity_controls(self):
  controls=runpy.run_path(str(B/'verify_math_controls.py'))['controls']()
  self.assertEqual(controls,json.loads((B/'evaluation/MATH_CONTROLS.json').read_bytes()))
  self.assertEqual(sum(x['uniform_rational_leaves']for x in controls['rejection_and_uniformity']),188)

if __name__=='__main__':unittest.main()
