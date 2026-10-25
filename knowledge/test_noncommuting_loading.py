"""Guard actual proof routes and the extra-control boundary of a loading repair."""
import hashlib
import json
import subprocess
import sys
import unittest

from knowledge.model import ROOT
from knowledge.retrieve import Library

UNITS = ['U1019-noncommuting-scalar-ramp',
         'U1019-almost-conserved-loading-obstruction',
         'U1019-selective-source-completion']
UPDATE = 'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-noncommuting-loading'
PROOF = '5fae6be2383bae1d413908fa1a62279d6cf587ee8aa833f3ce6dbd5d4a130cf7'


class NoncommutingLoading(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_received_originals_and_decisive_source_branches(self):
        index = json.loads((ROOT / UPDATE / 'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']), 9)
        self.assertEqual(sum(r['bytes'] for r in index['files']), 49358)
        for row in index['files']:
            raw = (ROOT / UPDATE / row['path']).read_bytes()
            self.assertEqual(len(raw), row['bytes'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])
            self.assertFalse(row['path'].endswith(('.zip', '.log')))
        # A bare gap-collapse example cannot support the all-envelope time claim.
        expected = [(10, 116, 'there is no additional bare positive penalty'),
                    (195, 261, 'nearly conserved state'),
                    (263, 312, 'including its cross-blocks')]
        for identifier, (start, end, passage) in zip(UNITS, expected):
            source = self.library.source(identifier, 0)
            self.assertEqual(source['source']['sha256'], PROOF)
            self.assertEqual(source['source']['lines'], [start, end])
            self.assertIn(passage, source['text'])
        obstruction = self.library.source(UNITS[1], 0)['text']
        self.assertIn('T >= sqrt(lambda+1)/a', obstruction)
        self.assertIn('uniformly over all such scalar controls', obstruction)
        repair = self.library.source(UNITS[2], 0)['text']
        self.assertIn('using unitarity on all imperfect/leakage branches', repair)

    def test_actual_acceptance_keeps_physical_and_control_gaps(self):
        for identifier in ['N1019', *UNITS]:
            record = self.library.resolve(identifier)
            review = next(v for v in record['review_overlays'] if v['id'] == 'A1033-noncommuting-code-loading')
            self.assertIn({'id': record['id'], 'content_version': record['content_version']}, review['subjects'])
            self.assertEqual(review['physical_measurement'], 'not established')
            self.assertEqual(review['working_device'], 'not established')
            self.assertIn('No scientific script', review['scope'])
        self.assertIn('no additional positive bare penalty', ' '.join(self.library.resolve(UNITS[0])['contract']['requires']))
        self.assertIn('only the common scalar envelope', ' '.join(self.library.resolve(UNITS[1])['contract']['requires']))
        self.assertIn('independently gate the off-code source', ' '.join(self.library.resolve(UNITS[2])['contract']['requires']))

    def test_version_pinned_repair_bridge_retains_extra_controls(self):
        transfer = self.library.bridge(UNITS[0], UNITS[2])['transfers'][0]
        self.assertEqual(transfer['state'], 'ESTABLISHED COMPATIBLE INTERFACE')
        for endpoint in ['from', 'to']:
            self.assertEqual(transfer[endpoint + '_version'], self.library.resolve(transfer[endpoint])['content_version'])
        self.assertIn('does not inherit fast preparation', transfer['scope'])
        self.assertIn('all matrix cross-counterterms', transfer['scope'])
        evidence = transfer['evidence'][0]
        self.assertEqual(evidence['sha256'], PROOF)
        self.assertEqual(evidence['lines'], [267, 310])
        raw = (ROOT / evidence['path']).read_text().splitlines()
        self.assertIn('Stage I.', '\n'.join(raw[266:310]))
        self.assertIn('relative calibration accuracy', '\n'.join(raw[266:310]))

    def test_actual_default_wire_packets_remain_usable(self):
        for identifier in ['N1019', *UNITS]:
            result = subprocess.run([sys.executable, 'knowledge/retrieve.py', 'packet', identifier],
                                    cwd=ROOT, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertLessEqual(len(result.stdout), 32768)
            self.assertTrue(json.loads(result.stdout)['packets'][0]['review_overlays'])


if __name__ == '__main__':
    unittest.main()
