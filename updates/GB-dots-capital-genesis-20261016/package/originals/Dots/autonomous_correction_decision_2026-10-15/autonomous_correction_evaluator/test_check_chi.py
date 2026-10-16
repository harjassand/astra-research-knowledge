import unittest
from check_chi import check,eigenvalues_symmetric
class ChiAuditTests(unittest.TestCase):
 def test_jacobi_known_spectrum(self):
  vals=eigenvalues_symmetric([[1.,2.],[2.,1.]])
  self.assertAlmostEqual(vals[0],-1.);self.assertAlmostEqual(vals[1],3.)
 def test_all_exact_central_obstructions(self):
  x=check()
  for v in x.values():
   self.assertFalse(v['exact_central_values_admit_CP_completion'])
   self.assertEqual(len(v['negative_diagonals']),1)
   self.assertLess(v['symmetrized_real_eigenvalues'][0],0)
   self.assertAlmostEqual(sum(v['symmetrized_real_eigenvalues']),v['trace_real'])
   self.assertLess(v['negative_diagonals'][0]['sd_shifts_to_zero'],2.)
if __name__=='__main__':unittest.main()
