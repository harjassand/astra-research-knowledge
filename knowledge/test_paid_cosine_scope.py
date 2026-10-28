"""Evidence/acceptance regressions; never execute acquired scientific code."""
import hashlib
import unittest
from knowledge.retrieve import Library


class PaidCosineScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library=Library()

    def test_reported_numerical_models_do_not_inherit_math_acceptance(self):
        for name in ('N1133','N1134','N1135','U1133-paid-six-control-gate-report',
                     'U1134-moving-field-parallel-report','U1135-preparation-version-and-noise-scope'):
            record=self.library.resolve(name)
            self.assertFalse(any(r.get('decision')=='accepted_internally_verified'
                                 for r in record['review_overlays']),name)
        original=self.library.resolve('N1127')
        self.assertTrue(any(r.get('decision')=='accepted_internally_verified'
                            for r in original['review_overlays']))
        self.assertIn('SN-P2-PAID-COSINE-ARTIFACT-AND-MODEL-BOUNDARY-20261028',
                      [n['notice_id']for n in original['notices']])

    def test_actual_owner_proof_routes_match_their_two_distinct_statements(self):
        for name,heading,anchor in (
                ('U1133-full-output-nojump-channel-bound','## A.','delta + (1-s)/2'),
                ('U1135-off-code-exposure-transparency','## B.','(I-P)BP sends e1 to e3/2')):
            record=self.library.resolve(name)
            self.assertTrue(any(r.get('decision')=='accepted_internally_verified'
                                for r in record['review_overlays']))
            passage=self.library.source(name,0)
            self.assertTrue(passage['text'].startswith(heading))
            self.assertIn(anchor,passage['text'])
            self.assertIn('OWNER_MATHEMATICAL_REVIEW.md',passage['source']['path'])

    def test_rendered_response_is_exact_and_missing_certificate_edge_stays_candidate(self):
        path=self.library.root/'research/2026-10-28-paid-cosine-and-loss/source/P2_FULL_RENDERED_RESPONSE.txt'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         'c9be4bb94fa3cceaa8c2106d454117748ec5a1e05d394e115505743c04f8260e')
        edges=[t for t in self.library.transfers
               if t['id']=='B1133-reported-gate-needs-acquired-channel-premises']
        self.assertEqual(len(edges),1)
        self.assertEqual(edges[0]['state'],'CANDIDATE CONNECTION')
        self.assertIn('no-jump fidelity is insufficient',edges[0]['remaining_obligations'])


if __name__=='__main__':unittest.main()
