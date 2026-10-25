"""Guard an actual proposal revision against stale support and audit transfer."""
import hashlib
import json
import unittest
from knowledge.model import ROOT


class ProgressionRevision(unittest.TestCase):
    def test_current_reader_correction_keeps_old_unit_and_binds_new_review(self):
        unit_id = 'U992-reaction-qualified-progression-proposal'
        old = ROOT / f'knowledge/units/{unit_id}/v0001.json'
        new = json.loads((ROOT / f'knowledge/units/{unit_id}/v0002.json').read_text())
        self.assertEqual(new['previous'], hashlib.sha256(old.read_bytes()).hexdigest())
        records = {r['id']: r for r in map(json.loads, (ROOT / 'knowledge/current/records.jsonl').read_text().splitlines())}
        current = records[unit_id]
        self.assertTrue(current['authority'].endswith('v0002.json'))
        self.assertIn('unacquired', current['statement'])
        review = json.loads((ROOT / 'knowledge/reviews/A1005-reaction-progression-correction.json').read_text())
        self.assertIn({'id': unit_id, 'content_version': current['content_version']}, review['subjects'])
        self.assertIn('not component literature independently reverified', review['scope'])
        reference = current['evidence'][0]
        data = (ROOT / reference['path']).read_bytes()
        self.assertEqual(hashlib.sha256(data).hexdigest(), reference['sha256'])
        lines = data.decode().splitlines()
        passage = '\n'.join(lines[reference['lines'][0]-1:reference['lines'][1]])
        self.assertIn('needs a correction', passage)
        self.assertIn('not automatically evidence of the intended organic bond', passage)


if __name__ == '__main__':
    unittest.main()
