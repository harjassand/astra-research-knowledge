import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import unittest

from knowledge.model import ROOT
from knowledge.retrieve import Library


UPDATE = Path('research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-25-completed-science-one')
SHARD = '2026-10-25-completed-science-one'


class CompletedScienceOne(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()
        cls.catalog = json.loads((ROOT / f'indexes/agent_catalog.d/{SHARD}.json').read_text())['claims']

    def test_selected_originals_match_their_source_index(self):
        rows = json.loads((ROOT / UPDATE / 'source/INDEX.json').read_text())['files']
        self.assertEqual(len(rows), 31)
        self.assertEqual(len({row['source_id'] for row in rows}), len(rows))
        for row in rows:
            with self.subTest(path=row['path']):
                data = (ROOT / UPDATE / row['path']).read_bytes()
                self.assertEqual(len(data), row['bytes'])
                self.assertEqual(hashlib.sha256(data).hexdigest(), row['sha256'])

    def test_actual_advertised_commands_and_source_routes(self):
        for entry in self.catalog:
            with self.subTest(identifier=entry['id']):
                pointers = entry['pointers']
                self.assertEqual(pointers['card_web'], pointers['card_local'])
                for path in pointers['read_web']:
                    self.assertTrue((ROOT / path).is_file(), path)
                result = subprocess.run(shlex.split(pointers['read_local']), cwd=ROOT, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                packet = json.loads(result.stdout)['packets'][0]
                self.assertEqual(packet['id'], entry['id'])
                self.assertNotIn('UNKNOWN; read cited source', packet['contract']['costs'])
                self.assertNotEqual(packet['contract']['obstruction'], 'UNKNOWN')
                self.assertTrue(any(review['decision'] == 'accepted_internally_verified' for review in packet['review_overlays']))
                for reference_index in range(len(packet['evidence'])):
                    self.assertTrue(self.library.source(packet['id'], reference_index)['text'].strip())
                for unit in packet['related_units']:
                    unit_packet = self.library.packet([unit['id']])['packets'][0]
                    self.assertTrue(any(review['decision'] == 'accepted_internally_verified' for review in unit_packet['review_overlays']))
                    for reference_index in range(len(unit_packet['evidence'])):
                        self.assertTrue(self.library.source(unit['id'], reference_index)['text'].strip())

    def test_exact_version_acceptance_and_audit_scope(self):
        for number in range(1001, 1005):
            path = next((ROOT / 'knowledge/reviews').glob(f'A{number}-completed-science-*.json'))
            review = json.loads(path.read_text())
            self.assertEqual(review['decision'], 'accepted_internally_verified')
            self.assertIn('not replayed', review['scope'])
            for subject in review['subjects']:
                self.assertEqual(self.library.resolve(subject['id'])['content_version'], subject['content_version'])
        source = ROOT / UPDATE / 'source/ultra/ROOT_THREE_GAP_BOUNDED_ASSAY_DRAFT.md'
        audit = (ROOT / UPDATE / 'source/ultra/ROOT_WHOLE_REVIEW.md').read_text().splitlines()
        self.assertIn(hashlib.sha256(source.read_bytes()).hexdigest(), '\n'.join(audit[805:836]))

    def test_current_semantics_keep_the_named_nontransfer_boundaries(self):
        p3 = self.library.resolve('N997')
        self.assertIn('unrestricted rational completion', p3['statement'])
        self.assertIn('randomized bounded-error', p3['contract']['assumptions'])
        p2 = self.library.resolve('N998')
        self.assertIn('not a full long-time Floquet', p2['contract']['assumptions'])
        p1 = self.library.resolve('N1000')
        self.assertIn('not conditional accepted error', p1['contract']['assumptions'])
        self.assertIn('model-average', p1['statement'])
        current = self.library.resolve('N996')
        self.assertEqual(current['content_version'], 'c7472731bde4c18a0fe478c0699d25e2245b387076c97e77e1325dfa044dfbd3')


if __name__ == '__main__':
    unittest.main()
