"""Sharpness belongs to the stated source/oracle class, not every reduction."""
import hashlib
import json
import subprocess
import sys
import unittest

from knowledge.model import ROOT
from knowledge.retrieve import Library

UNITS = ['U1018-signed-spectrum-precision-frontier', 'U1018-exact-loewner-task-transfer',
         'U1018-two-forward-response-reduction', 'U1018-finite-gradient-history-hessian-ambiguity',
         'U1018-scalar-readout-and-future-reuse']
UPDATE = 'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-sharp-precision'
PROOF = '285937091401082a3f6702cb36ebc3bfd535e1a96098d5bcfcb7189bc57aa692'


class SharpPrecision(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_received_science_and_actual_governing_passages(self):
        index = json.loads((ROOT / UPDATE / 'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']), 10)
        self.assertEqual(sum(r['bytes'] for r in index['files']), 193721)
        self.assertEqual(sum(r['path'].endswith('_results.json') for r in index['files']), 4)
        for row in index['files']:
            raw = (ROOT / UPDATE / row['path']).read_bytes()
            self.assertEqual(len(raw), row['bytes'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])
            self.assertNotIn('RECEIPT', row['path'])
            self.assertFalse(row['path'].endswith('.zip'))
        expected = [(13, 120, 'arbitrary'), (153, 203, 'outer approximation'),
                    (216, 250, 'actual forward'), (252, 273, 'globally `C^5`'),
                    (303, 337, 'Future task information-loss theorem')]
        for identifier, (start, end, decisive) in zip(UNITS, expected):
            with self.subTest(unit=identifier):
                result = self.library.source(identifier, 0)
                self.assertEqual(result['source']['sha256'], PROOF)
                self.assertEqual(result['source']['lines'], [start, end])
                self.assertIn(decisive, result['text'])

    def test_current_acceptance_keeps_native_and_posterior_limits(self):
        for identifier in ['N1018', *UNITS]:
            record = self.library.resolve(identifier)
            review = next(r for r in record['review_overlays'] if r['id'] == 'A1032-sharp-symmetric-precision')
            self.assertIn({'id': record['id'], 'content_version': record['content_version']}, review['subjects'])
            self.assertEqual(review['working_device'], 'not established')
            self.assertEqual(review['physical_measurement'], 'not established')
        self.assertIn('ENTIRE exact', self.library.resolve(UNITS[1])['statement'])
        self.assertIn('OUTER interval', self.library.resolve(UNITS[1])['body'])
        self.assertIn('LOWER bound does not transfer', self.library.resolve(UNITS[2])['body'])
        self.assertIn('C5 piecewise-polynomial', self.library.resolve(UNITS[3])['body'])
        scalar = self.library.resolve(UNITS[4])
        self.assertIn('tail_k', scalar['statement'])
        self.assertIn('does not save native scalar bandwidth', scalar['contract']['assumptions'][0])
        self.assertIn('future usefulness are different resources', scalar['body'])
        dependency = self.library.source(UNITS[4], 1)
        self.assertEqual(dependency['source']['lines'], [13, 120])
        self.assertIn('possibly adaptive', dependency['text'])

    def test_upper_only_interface_has_exact_versions_and_source_scope(self):
        link = self.library.bridge(UNITS[2], UNITS[0])['transfers'][0]
        self.assertEqual(link['state'], 'ESTABLISHED COMPATIBLE INTERFACE')
        for endpoint in ['from', 'to']:
            self.assertEqual(link[endpoint + '_version'], self.library.resolve(link[endpoint])['content_version'])
        self.assertIn('UPPER certificate', link['scope'])
        self.assertIn('LOWER bound', link['scope'])
        self.assertIn('do NOT transfer', link['scope'])
        source = link['evidence'][0]
        self.assertEqual(source['lines'], [216, 246])
        lines = (ROOT / source['path']).read_text().splitlines()
        passage = '\n'.join(lines[215:246])
        self.assertIn('Two *actual forward* calls', passage)
        self.assertIn('**not** proof that central differencing is globally optimal', passage)

    def test_actual_default_card_and_unit_outputs_are_complete_and_bounded(self):
        for identifier in ['N1018', *UNITS]:
            with self.subTest(identifier=identifier):
                result = subprocess.run([sys.executable, 'knowledge/retrieve.py', 'packet', identifier],
                                        cwd=ROOT, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertLessEqual(len(result.stdout), 32768)
                self.assertTrue(json.loads(result.stdout)['packets'][0]['review_overlays'])


if __name__ == '__main__':
    unittest.main()
