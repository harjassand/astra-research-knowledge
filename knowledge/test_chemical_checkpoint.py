"""A chemistry update must preserve its governing model and old acceptance scope."""
import hashlib
import json
import subprocess
import sys
import unittest

from knowledge.model import ROOT
from knowledge.retrieve import Library


UNITS = {
    'U992-imine-slow-tail-discrimination': 'This is EXACT for the slow eigenvalue',
    'U992-damage-limited-checkpoint': 'F_stage(t)=p/(p+w+d)',
    'U992-composition-mass-readout-alias': 'full molecule mass reports base composition',
}
HASHES = {
    'astra_imine_checkpoint_notes_20261026.md': 'da3ea96fc0762e9e0b0f14eb5f2633fd76149b13a3312d30351167f254991040',
    'astra_imine_checkpoint_20261026.py': '0ff8a78c020ec6d1dde7df125e3c525440ed0d6176e8c850debe5ea4be24711c',
    'COMPLETE_COPY.txt': 'dec4e7138fb42e78a084a1425830b8750cffe1841f671f4c7d1d946bf333b16a',
}
UPDATE = 'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-chemical-checkpoint'


class ChemicalCheckpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_three_frozen_sources_and_actual_governing_passages(self):
        index = json.loads((ROOT / UPDATE / 'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']), 3)
        for row in index['files']:
            path = ROOT / UPDATE / row['path']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), HASHES[path.name])
            self.assertEqual(path.stat().st_size, row['bytes'])
        for identifier, decisive_text in UNITS.items():
            with self.subTest(unit=identifier):
                passage = self.library.source(identifier, 0)
                self.assertTrue(passage['source']['path'].endswith('astra_imine_checkpoint_notes_20261026.md'))
                self.assertEqual(passage['source']['sha256'], HASHES['astra_imine_checkpoint_notes_20261026.md'])
                self.assertIn(decisive_text, passage['text'])
        slow = self.library.resolve('U992-imine-slow-tail-discrimination')
        self.assertIn('not an exact transient survival law', slow['statement'])
        damage = self.library.resolve('U992-damage-limited-checkpoint')
        self.assertIn('mutually exclusive', damage['statement'])
        self.assertIn('same parent', damage['statement'])
        mass = self.library.resolve('U992-composition-mass-readout-alias')
        self.assertIn('not a promise of35 resolved mass peaks', mass['body'])

    def test_new_card_review_does_not_relabel_the_old_units_or_physical_evidence(self):
        card = self.library.resolve('N992')
        self.assertIn('lambda-exonuclease reset retains', card['body'])
        self.assertIn('P_step=p*v/(p+w+h*alpha)', card['statement'])
        current = next(r for r in card['review_overlays'] if r['id'] == 'A1028-chemical-checkpoint')
        self.assertIn({'id': card['id'], 'content_version': card['content_version']}, current['subjects'])
        self.assertTrue(any(r['id'] == 'A1005-reaction-progression-correction' for r in card['historical_reviews']))
        for identifier in UNITS:
            record = self.library.resolve(identifier)
            self.assertIn({'id': identifier, 'content_version': record['content_version']}, current['subjects'])
        self.assertEqual(current['physical_measurement'], 'not established')
        self.assertEqual(current['working_device'], 'not established')
        old = self.library.resolve('U992-reaction-qualified-progression-proposal')
        self.assertEqual(old['content_version'], '972a4e9177c71165959b8dbd30e9ec2f449777d68370854c8ff76b6ec1a8fec5')
        self.assertEqual(old['version'], 2)
        self.assertTrue(any(r['id'] == 'A1005-reaction-progression-correction' for r in old['review_overlays']))

    def test_actual_default_card_and_unit_output_remains_complete_and_bounded(self):
        for identifier in ['N992', *UNITS]:
            with self.subTest(identifier=identifier):
                result = subprocess.run([sys.executable, 'knowledge/retrieve.py', 'packet', identifier],
                                        cwd=ROOT, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertLessEqual(len(result.stdout), 32768)
                packet = json.loads(result.stdout)['packets'][0]
                self.assertTrue(any(r['id'] == 'A1028-chemical-checkpoint' for r in packet['review_overlays']))


if __name__ == '__main__':
    unittest.main()
