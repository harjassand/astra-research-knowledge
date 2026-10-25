"""Protect proof-route identity where hashes alone can select the wrong branch."""
import json
import subprocess
import sys
import unittest
from knowledge.model import ROOT, encoded


class EntropyReceivingRoutes(unittest.TestCase):
    def test_accepted_card_default_packets_fit_with_historical_reviews(self):
        for identifier in ['N993', 'N994', 'N995']:
            result = subprocess.run([sys.executable, 'knowledge/retrieve.py', 'packet', identifier], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            # The advertised budget is for encoded JSON, before CLI pretty printing.
            self.assertLessEqual(len(encoded(json.loads(result.stdout))), 32768)

    def test_receiver_routes_contain_the_actual_complement_and_interval_arguments(self):
        unit = json.loads((ROOT / 'knowledge/units/U1006-complement-index-and-shifted-interval-payment/v0001.json').read_text())
        passages = {}
        for ref in unit['evidence']:
            lines = (ROOT / ref['path']).read_text().splitlines()
            passages[ref['path'].split('/')[-1]] = '\n'.join(lines[ref['lines'][0]-1:ref['lines'][1]])
        projector = passages['wh3_all_projector_inputs_entropy_theorem.md']
        self.assertIn('I-P<=9E(I-P)=9I-9B', projector)
        self.assertIn('0<=9B-P<=8I', projector)
        shifted = passages['wh3_all_two_level_inputs_entropy_theorem.md']
        self.assertIn('negative unmatched interval', shifted)
        self.assertIn('16 integral_v^(t(u))', shifted)
        self.assertIn('additional non-product kernel', shifted)

    def test_current_binary_cards_display_their_actual_scoped_acceptance(self):
        records = {r['id']: r for r in map(json.loads, (ROOT / 'knowledge/current/records.jsonl').read_text().splitlines())}
        reviews = [json.loads(p.read_text()) for p in (ROOT / 'knowledge/reviews').glob('A1012-binary-family-current-acceptance-N*.json')]
        self.assertEqual(len(reviews), 3)
        for subject in [s for review in reviews for s in review['subjects']]:
            record = records[subject['id']]
            self.assertEqual(record['content_version'], subject['content_version'])
            text = (ROOT / ('cards/' + subject['id'] + '.txt')).read_text()
            self.assertIn('status=accepted_internally_verified', text)
            self.assertNotIn('status=source_derived_unreviewed', text)


if __name__ == '__main__':
    unittest.main()
