"""Checks of persisted results without re-executing author code."""
import json, unittest
from pathlib import Path
R=json.loads((Path(__file__).resolve().parent/'results.json').read_text())
class AuditChecks(unittest.TestCase):
 def test_constraints(self):
  for d in R['fits'].values():
   for r in d.values():
    for mode,s in r['sensitivities'].items():
     self.assertGreater(s['tau_ms'],0)
     self.assertGreaterEqual(s['a'],-1e-12);self.assertGreaterEqual(s['c'],-1e-12)
     self.assertLessEqual(s['a']+s['c'],1+1e-12)
     lo,hi=s['delta_SSE_le_1_tau_range_ms'];self.assertLess(lo,s['tau_ms']);self.assertGreater(hi,s['tau_ms'])
 def test_reproduced_fits(self):
  for fn,d in R['fits'].items():
   for series,r in d.items():
    mode='a_ge_0.4_diagnostic' if '4a_' in fn and series=='QEC' else 'simplex'
    self.assertAlmostEqual(r['reported']['weighted_SSE'],r['sensitivities'][mode]['weighted_SSE'],places=6)
    self.assertLess(abs(r['reported']['tau_ms']-r['sensitivities'][mode]['tau_ms']),.001)
 def test_injected_pairs(self):
  for fn,d in R['paired_measured'].items():
   if '4b_' in fn:
    self.assertEqual(len(d),5);self.assertTrue(all(x['difference']>0 for x in d))
 def test_threshold_order(self):
  for d in R['fits'].values():
   for mode in d['QEC']['sensitivities']:
    self.assertGreater(d['QEC']['sensitivities'][mode]['cross_075_ms'],d['phy']['sensitivities'][mode]['cross_075_ms'])
if __name__=='__main__':unittest.main()
