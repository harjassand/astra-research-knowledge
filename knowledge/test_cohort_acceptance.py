"""A complemented bad-acceptance event must never certify a rejected cohort."""
import hashlib
import json
import subprocess
import sys
import unittest

from knowledge.model import ROOT
from knowledge.retrieve import Library

UNIT = 'U1003-common-error-cohort-certificate'
OLD_CONTENT = '13bb78bd6a69e5d82b0edb733cdda6bb9f3106a73796132cf6506b0e4580cea6'
SOURCE_HASH = '9ebda1f4c3e5bbb955ee4845c8fedf19ccc6b117353a16e29dea59b8e12543c5'


class CohortAcceptance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_rejected_counterexample_is_not_a_good_certificate(self):
        # The reported counterexample is deterministic for every guard address.
        domain = range(3)
        f = lambda x: 0
        candidate = lambda x: 1
        eta = 0.5
        all_match = all(f(x) == candidate(x) for x in domain)
        risk = sum(f(x) != candidate(x) for x in domain) / len(domain)
        bad_acceptance = all_match and risk > eta
        self.assertFalse(bad_acceptance)
        self.assertTrue(not bad_acceptance)  # v1 incorrectly granted this run a certificate.
        self.assertGreater(risk, eta)
        self.assertFalse(all_match and not bad_acceptance)
        unit = self.library.resolve(UNIT)
        self.assertEqual(unit['contract']['provides'], [unit['statement']])
        for passage in [unit['statement'], *unit['contract']['provides']]:
            self.assertIn('Pr[C_r AND sum_i e_i>eta]', passage)
            self.assertIn('On C_r outside that bad event', passage)
            self.assertIn('Rejected cohorts receive no certificate', passage)
            self.assertIn('not conditional-on-acceptance accuracy without a yield bound', passage)
        self.assertIn('f=0 and fixed candidate G=1', unit['body'])
        # Rejection does not imply large true error either: one bad address suffices.
        low_error_source = lambda x: 0 if x == 0 else 1
        small_risk = sum(low_error_source(x) != candidate(x) for x in domain) / len(domain)
        self.assertLessEqual(small_risk, eta)
        self.assertFalse(all(low_error_source(x) == candidate(x) for x in domain))
        self.assertIn('On C_r outside B, sum_i e_i<=eta, so', unit['body'])
        self.assertNotIn('Only on C_r outside B', unit['body'])

    def test_successor_and_current_review_preserve_historical_versions(self):
        old_path = ROOT / f'knowledge/units/{UNIT}/v0001.json'
        second_path = ROOT / f'knowledge/units/{UNIT}/v0002.json'
        second = json.loads(second_path.read_text())
        new = json.loads((ROOT / f'knowledge/units/{UNIT}/v0003.json').read_text())
        self.assertEqual(second['previous'], hashlib.sha256(old_path.read_bytes()).hexdigest())
        self.assertEqual(new['previous'], hashlib.sha256(second_path.read_bytes()).hexdigest())
        self.assertIn('On its complement', json.loads(old_path.read_text())['statement'])
        unit = self.library.resolve(UNIT)
        self.assertEqual(unit['version'], 3)
        self.assertTrue(unit['authority'].endswith('v0003.json'))
        self.assertNotEqual(unit['content_version'], OLD_CONTENT)
        self.assertEqual([h['version'] for h in unit['history']], [1, 2, 3])
        for identifier in [UNIT, 'N1003']:
            record = self.library.resolve(identifier)
            expected_review = 'A1025-cohort-sufficient-event-wording' if identifier == UNIT else 'A1024-cohort-acceptance-correction'
            current = next(r for r in record['review_overlays'] if r['id'] == expected_review)
            self.assertIn({'id': record['id'], 'content_version': record['content_version']}, current['subjects'])
            self.assertTrue(any(r['id'] == 'A1008-cohort-transfer' for r in record['historical_reviews']))
        self.assertTrue(any(r['id'] == 'A1024-cohort-acceptance-correction' for r in unit['historical_reviews']))
        unaffected = self.library.resolve('U1003-native-correction-before-anchor-transfer')
        self.assertTrue(any(r['id'] == 'A1008-cohort-transfer' for r in unaffected['review_overlays']))
        notice = next(n for n in unit['notices'] if n.get('notice_id') == 'SN-U1003-ACCEPTANCE-CONDITION-20261026')
        self.assertEqual(notice['superseded_content_version'], OLD_CONTENT)
        self.assertFalse(notice['whole_claim_invalidated'])

    def test_actual_default_packets_and_unchanged_governing_passage(self):
        for identifier in ['N1003', UNIT]:
            result = subprocess.run([sys.executable, 'knowledge/retrieve.py', 'packet', identifier],
                                    cwd=ROOT, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertLessEqual(len(result.stdout), 32768)
            packet = json.loads(result.stdout)['packets'][0]
            self.assertIn('On C_r outside', packet['statement'])
            self.assertIn('Rejected cohorts receive no certificate', packet['statement'])
        source = self.library.source(UNIT, 0)
        self.assertEqual(source['source']['lines'], [34, 86])
        self.assertEqual(hashlib.sha256((ROOT / source['source']['path']).read_bytes()).hexdigest(), SOURCE_HASH)
        text = ' '.join(source['text'].split())
        self.assertIn('Let C_i be the event that all guards through i match', text)
        self.assertIn('Pr[C_r AND sum_i e_i>eta] <= exp(-q eta) <= delta.', text)
        self.assertIn('not a conditional-on-return guarantee without a lower bound on the return probability', text)
        self.assertIn('outside the SAME E', text)


if __name__ == '__main__':
    unittest.main()
