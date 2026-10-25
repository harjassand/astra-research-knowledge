"""Changed one-hit premises must not replace or inherit an unrelated audit."""
import hashlib
import json
import subprocess
import sys
import unittest

from knowledge.model import ROOT
from knowledge.retrieve import Library

NEW = ['U1017-preanchored-one-hit-window', 'U1017-shared-preanchor-loss-ceiling',
       'U1017-single-end-mass-normalization']
OLD = ['U1017-two-sided-retained-graft', 'U1017-common-shutdown-tail',
       'U1017-contact-before-shutdown']
HASHES = {
    'cbf694692362d6eed23a7e273b949d22c57ebed987a8d3611959461ebc0daebc',
    '46460f55c38030cc657414fd08e94fd0710639642030b4ebc5960c10c36b69b5',
}
UPDATE = 'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-preanchored-weld'


class PreanchoredWeld(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_exact_sources_and_closed_form_not_missing_hybrid_branch(self):
        index = json.loads((ROOT / UPDATE / 'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']), 2)
        self.assertEqual({r['sha256'] for r in index['files']}, HASHES)
        self.assertEqual(sum(r['bytes'] for r in index['files']), 37239)
        for row in index['files']:
            raw = (ROOT / UPDATE / row['path']).read_bytes()
            self.assertEqual(len(raw), row['bytes'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])
            self.assertNotIn('hybrid_weld_test.py', row['path'])
        one = self.library.source(NEW[0], 1)
        self.assertEqual(one['source']['lines'], [154, 172])
        self.assertIn('regular', self.library.resolve(NEW[0])['statement'])
        self.assertIn('sum gammainc(j+1,X)/X', one['text'])
        self.assertIn('later mechanical service interval', one['text'])
        shared = self.library.source(NEW[1], 0)
        self.assertEqual(shared['source']['lines'], [154, 168])
        self.assertIn('entire region delaminates', shared['text'])
        self.assertNotIn('221', shared['text'])
        self.assertIn('independence', self.library.resolve(NEW[1])['body'])
        mass = self.library.source(NEW[2], 0)
        self.assertIn('one nonreducing terminal acceptor', mass['text'])

    def test_new_review_keeps_old_units_accepted_at_their_versions(self):
        card = self.library.resolve('N1017')
        review = next(r for r in card['review_overlays'] if r['id'] == 'A1031-preanchored-weld')
        self.assertIn({'id': card['id'], 'content_version': card['content_version']}, review['subjects'])
        self.assertTrue(any(r['id'] == 'A1030-cellulose-weld' for r in card['historical_reviews']))
        for identifier in NEW:
            record = self.library.resolve(identifier)
            self.assertIn({'id': identifier, 'content_version': record['content_version']}, review['subjects'])
        for identifier in OLD:
            record = self.library.resolve(identifier)
            self.assertEqual(record['version'], 1)
            self.assertTrue(any(r['id'] == 'A1030-cellulose-weld' for r in record['review_overlays']))
            self.assertFalse(any(r['id'] == 'A1031-preanchored-weld' for r in record['review_overlays']))
        self.assertEqual(review['working_device'], 'not established')
        self.assertIn('missing', ' '.join(review['remaining_gaps']))
        self.assertIn('not accepted', card['body'])

    def test_documented_contact_composition_has_exact_versions_and_source_branch(self):
        link = self.library.bridge(OLD[2], NEW[0])['transfers'][0]
        self.assertEqual(link['state'], 'ESTABLISHED COMPATIBLE INTERFACE')
        for endpoint in ['from', 'to']:
            self.assertEqual(link[endpoint + '_version'], self.library.resolve(link[endpoint])['content_version'])
        self.assertIn('p_c*(1-F_m)', link['scope'])
        source = link['evidence'][0]
        self.assertEqual(source['lines'], [225, 234])
        lines = (ROOT / source['path']).read_text().splitlines()
        passage = '\n'.join(lines[source['lines'][0]-1:source['lines'][1]])
        self.assertIn('cap=1-per_tile_target/contact', passage)
        self.assertTrue(any('conditional on contact' in x for x in link['remaining_obligations']))
        self.assertTrue(any('unavailable hybrid' in x for x in link['remaining_obligations']))

    def test_actual_default_packets_fit_without_losing_history(self):
        for identifier in ['N1017', *NEW, *OLD]:
            with self.subTest(identifier=identifier):
                result = subprocess.run([sys.executable, 'knowledge/retrieve.py', 'packet', identifier],
                                        cwd=ROOT, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertLessEqual(len(result.stdout), 32768)
                packet = json.loads(result.stdout)['packets'][0]
                self.assertTrue(packet['review_overlays'])


if __name__ == '__main__':
    unittest.main()
