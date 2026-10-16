import unittest
from evaluate import evaluate,sections
class EvaluatorTests(unittest.TestCase):
 def test_structure_and_ratios(self):
  r=evaluate();self.assertEqual(r['conditions']['Fig4a']['counts'],{'phy':8,'noQEC':8,'QEC':8});self.assertEqual(r['conditions']['Fig4b']['counts'],{'phy':18,'noQEC':18,'QEC':11});self.assertAlmostEqual(r['conditions']['Fig4a']['tau_ratio_QEC_over_physical'],1.4520350023369684)
 def test_matched_times_only(self):
  r=evaluate();self.assertEqual(len(r['conditions']['Fig4b']['exact_time_measured_comparisons']),5);self.assertEqual(r['interleaved_pairs']['EDFig4a']['QEC_better'],11)
 def test_chi_incomplete(self):
  r=evaluate();self.assertFalse(r['chi_identity_elements']['Fig3e']['full_complex_process_available']);self.assertAlmostEqual(r['chi_identity_elements']['Fig3e']['real_II'],.9186010327762717)
if __name__=='__main__':unittest.main()
