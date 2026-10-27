"""Small independent interface controls; never imports producer research scripts."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SHARD = '2026-10-27-response-and-physical-interfaces'
UPDATE = ROOT / 'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates' / SHARD


class ResponsePhysicalInterfaces(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = {r['id']: r for r in map(json.loads, (ROOT / 'knowledge/current/records.jsonl').read_text().splitlines())}

    def test_legacy_acquisition_scope_is_preserved(self):
        # Pin the immutable historical extraction, allowing a legitimate v2.
        path = ROOT / 'knowledge/units/U1082-noise-rejects-exact-rank-not-source/v0001.json'
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         '3d02e282e7fe71c25e78a381e1a58e6552b3fa22e4c8135ed56a183e83511dde')
        self.assertIn('is not supplied', json.loads(path.read_text())['statement'])
        relation = json.loads((ROOT / 'knowledge/transfers/B1089-old-noise-to-downstream.json').read_text())
        self.assertEqual(relation['state'], 'CANDIDATE CONNECTION')
        self.assertIn('missing510', relation['scope'])

    def test_psd_saddle_counterexample_and_dual_witness(self):
        # Invert two-by-two matrices directly, independently of source code.
        def response(a, b, d):
            return F(a + d - 2*b, a*d - b*b)
        self.assertEqual(response(30, 40, 110), F(3, 85))
        self.assertEqual(response(30, 20, 110), F(1, 29))
        self.assertEqual(response(30, 30, 110), F(1, 30))
        # x=(1/30,0): 2*1Tx-xT(A+E)x >= 2/30-(20+10)/900.
        lower = 2*F(1, 30) - 30*F(1, 30)**2
        self.assertEqual(lower, F(1, 30))
        self.assertLess(lower, F(1, 29))
        self.assertGreater(F(110-40, 1700), 0)
        self.assertLess(F(30-40, 1700), 0)  # sign guard really fails

    def test_concavity_does_not_supply_monotone_clipping(self):
        x, h = F(1, 10), F(1, 100)
        reward = lambda u: F(1, 2) - 1/(2-u)
        derivative = -1/(2-x)**2
        raw_lower = (reward(x+h)-reward(x))/h
        cap = 2 / F(9, 5)**3  # Q>=1.8 on the .2 domain
        self.assertLessEqual(raw_lower, derivative)
        self.assertLessEqual(derivative, raw_lower + cap*h/2)
        self.assertLess(derivative, 0)
        self.assertGreater(reward(0)-reward(x), 0)
        # Clipping l=0 makes the zero-action tangent term zero, falsely.
        self.assertEqual(-x*max(F(0), raw_lower), 0)
        unit = self.records['U1090-scalar-curvature-audit']
        self.assertIn('l_i=(a0-bi)/hi-ci', unit['statement'])
        self.assertTrue(unit['notices'])

    def test_simplex_certificate_covers_a_full_concave_fixture(self):
        delta, x = F(1, 5), (F(1, 20), F(1, 20))
        reward = lambda u: 2*u[0]+u[1]-u[0]**2-3*u[1]**2
        g = (2-2*x[0], 1-6*x[1])
        lo, hi = [z-F(1, 100) for z in g], [z+F(1, 100) for z in g]
        bound = max([-sum(x[i]*lo[i] for i in range(2))] +
                    [(delta-x[j])*hi[j]-sum(x[i]*lo[i] for i in range(2) if i != j) for j in range(2)])
        for a in range(21):
            for b in range(21-a):
                self.assertLessEqual(reward((F(a, 100), F(b, 100)))-reward(x), bound)

    def test_task_directed_menu_and_changed_pooling_contract(self):
        a, b = F(187, 2650), F(13, 150)
        self.assertEqual(a*b/(a+b), F(2431, 62500))
        self.assertEqual(50*(F(101, 1000)-F(1, 10))**3, F(1, 20_000_000))
        self.assertGreater(F(1, 20_000_000), 2*F(1, 100_000_000))
        ceilings = []
        for dose in [F(2, 5), F(3, 5), F(1)]:
            capacity = dose // F(101, 1000)
            ceilings.append((124+capacity-1)//capacity + (capacity-1).bit_length())
        self.assertEqual(ceilings, [44, 28, 18])
        relation = json.loads((ROOT / 'knowledge/transfers/B1090-threshold-to-pooling.json').read_text())
        self.assertEqual(relation['state'], 'INCOMPATIBLE ASSUMPTIONS')

    def test_reused_boson_review_matches_exact_subject_bytes(self):
        base = UPDATE / 'source/boson/originals/independent_breakthrough_route'
        pins = {'PROOFS.txt': '8f32fd2875c6060a224b86ae09d5ba5c111afe6a16ed6f2a97c66281f62ed355',
                'code/canonical_bafqmc.py': 'b3c4791dd001b6793ee277776503b1e509ab1a8a109e6e426fca178debc06108',
                'canonical_n3_main.json': 'e10b05dfa0873bcf6d9ead73c7c508622223b78365549039c2cdc9cf88374bbb'}
        review = (UPDATE / 'source/boson/originals/parent/canonical_boson_operation_20261027/REVIEW.md').read_text()
        for name, digest in pins.items():
            self.assertEqual(hashlib.sha256((base / name).read_bytes()).hexdigest(), digest)
            self.assertIn(digest, review)
        self.assertIn('complete worker', review)
        self.assertIn('regularization', self.records['N1091-balanced-canonical-boson-operation-and-ensemble-failure']['contract']['assumptions'])

    def test_mean_counts_cannot_supply_covariance_or_layer_overlap(self):
        layers, p = 16, F(5, 8)
        mean = layers*p
        independent_variance = layers*p*(1-p)
        synchronized_variance = layers**2*p*(1-p)
        self.assertEqual(mean, 10)
        self.assertEqual(independent_variance/mean**2, F(3, 80))
        self.assertEqual(synchronized_variance/mean**2, F(3, 5))
        self.assertEqual(synchronized_variance/independent_variance, 16)
        universe = set(range(layers))
        left = set(range(10))
        self.assertEqual(len(left & set(range(6, 16))), 4)
        self.assertEqual(len(left & left), 10)
        self.assertEqual(len(set(range(8)) & (universe-set(range(8)))), 0)

    def test_reviews_accept_scoped_results_without_inventing_measurements(self):
        found = 0
        for path in (ROOT / 'knowledge/reviews').glob('*response-and-physical-interfaces.json'):
            review = json.loads(path.read_text())
            self.assertEqual(review['decision'], 'accepted_internally_verified')
            self.assertEqual(review['physical_measurement'], 'not established')
            self.assertEqual(review['working_device'], 'not established')
            for subject in review['subjects']:
                record = self.records[subject['id']]
                if subject['content_version'] == record['content_version']:
                    self.assertTrue(any(r['id'] == review['id'] for r in record['review_overlays']))
                else:
                    self.assertFalse(any(r['id'] == review['id'] for r in record['review_overlays']))
                    self.assertTrue(any(r['id'] == review['id'] for r in record['historical_reviews']))
                    self.assertTrue(any(r['decision'] == 'accepted_internally_verified' and
                                        {'id': record['id'], 'content_version': record['content_version']} in r['subjects']
                                        for r in record['review_overlays']))
            found += 1
        self.assertEqual(found, 4)

    def test_acquisition_counts_do_not_bleed_between_operations(self):
        revised = [r for r in self.records.values() if r['id'].startswith(('U1089-', 'U1090-'))]
        self.assertEqual(len(revised), 8)
        for record in revised:
            self.assertNotIn('510', record['contract']['units'])
            self.assertGreaterEqual(record['version'], 2)
            original = ROOT / 'knowledge/units' / record['id'] / 'v0001.json'
            revised = json.loads(original.with_name('v0002.json').read_text())
            self.assertEqual(revised['previous'], hashlib.sha256(original.read_bytes()).hexdigest())
            self.assertEqual([r['version'] for r in record['history'][:2]], [1, 2])
        pair_cost = ' '.join(self.records['U1089-one-task-directed-scalar-probe']['contract']['costs'])
        audit_cost = ' '.join(self.records['U1090-scalar-curvature-audit']['contract']['costs'])
        self.assertIn('14 paid historical', pair_cost)
        self.assertIn('one paid pair reaction', pair_cost)
        self.assertIn('n+1 scalar reaction values (129', audit_cost)
        self.assertIn('already-paid valid value at the same dose point', audit_cost)
        self.assertIn('charge each newly queried point once', audit_cost)
        self.assertIn('No510-reading prerequisite', audit_cost)

    def test_cached_reactions_support_new_linear_prices_without_double_charge(self):
        # Two exact stored values of Z for Q=2+u, not a live/source-aware oracle.
        x, h = F(1, 10), F(1, 100)
        stored = {x: 1/(2+x), x+h: 1/(2+x+h)}
        base_lower = (stored[x]-stored[x+h])/h
        intervals = []
        for price in [F(0), F(1, 4)]:
            lower = base_lower-price
            upper = lower+F(1, 4)*h/2
            truth = 1/(2+x)**2-price
            self.assertLessEqual(lower, truth)
            self.assertLessEqual(truth, upper)
            intervals.append((lower, upper))
        self.assertEqual(tuple(z-F(1, 4) for z in intervals[0]), intervals[1])
        self.assertEqual(len(stored), 2)
        unit = self.records['U1090-scalar-curvature-audit']
        self.assertIn('query missing points', unit['body'])
        self.assertIn('same source/dose/reset/calibration', unit['contract']['requires'][0])


if __name__ == '__main__':
    unittest.main()
