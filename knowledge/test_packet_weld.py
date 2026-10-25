"""Keep the packet-reset and wet-weld models on their actual source branches."""
import hashlib
import json
import subprocess
import sys
import unittest

from knowledge.model import ROOT
from knowledge.retrieve import Library

UPDATE = 'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-packet-and-weld'
SUPPORT = {
    'U1016-wrong-partner-access-bound': ('astra_covalent_island_repair_notes_20261026.md', 'r*(r-1)*beta'),
    'U1016-multivalent-clearance': ('astra_covalent_island_repair_notes_20261026.md', 'absorbs to a perfect wash sink'),
    'U1016-rooted-prefix-waste': ('astra_covalent_island_repair_notes_20261026.md', 'E[wasted already-formed correct links]'),
    'U1016-equal-exposure-pulse-null': ('astra_covalent_island_repair_notes_20261026.md', 'The shape of c(t) cancels'),
    'U1017-two-sided-retained-graft': ('astra_xh2_heteroglucan_weld.py', 'Cleavage alone is NOT'),
    'U1017-common-shutdown-tail': ('COMPLETE_RESPONSE_COPY.txt', "Jensen's inequality"),
    'U1017-contact-before-shutdown': ('COMPLETE_RESPONSE_COPY.txt', 'Even perfect subsequent welding'),
}
HASHES = {
    '434c2a1c63566b4c96e899304fb1eba3f8e5dae89a88be0bec89335ecb4976a7',
    '7547b2752789ef36ca09872131ec2ad30da0fb2d744f49a509504c84daee32cc',
    '957d7e3f96a1f98c1a796b7ed63d012ea74d91da80e8bd5c2d6946bdbd915522',
    '6997f22163fa0619d49331c3d09010485f118f14d96f2f0302e5d70a5d76b709',
    'a1c65542778090b25199a16a3ce798bbadd75a8ef4e4cef0dbcd05ba4e00724a',
}


class PacketWeld(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_exact_sources_and_actual_decisive_branches(self):
        index = json.loads((ROOT / UPDATE / 'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']), 5)
        self.assertEqual({r['sha256'] for r in index['files']}, HASHES)
        self.assertEqual(sum(r['bytes'] for r in index['files']), 91914)
        for row in index['files']:
            raw = (ROOT / UPDATE / row['path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])
            self.assertEqual(len(raw), row['bytes'])
            self.assertNotIn('CONTINUATION', row['path'])
            self.assertNotIn('RECEIPT', row['path'])
        for identifier, (name, decisive) in SUPPORT.items():
            with self.subTest(identifier=identifier):
                passage = self.library.source(identifier, 0)
                self.assertTrue(passage['source']['path'].endswith(name))
                self.assertIn(passage['source']['sha256'], HASHES)
                self.assertIn(decisive, passage['text'])

    def test_current_acceptance_keeps_physical_and_cross_interface_gaps(self):
        for identifier in ['N1016', 'N1017', *SUPPORT]:
            record = self.library.resolve(identifier)
            review_id = 'A1029-packet-assembly' if record['id'].startswith(('N1016', 'U1016')) else 'A1030-cellulose-weld'
            review = next(r for r in record['review_overlays'] if r['id'] == review_id)
            self.assertIn({'id': record['id'], 'content_version': record['content_version']}, review['subjects'])
            self.assertEqual(review['physical_measurement'], 'not established')
            self.assertEqual(review['working_device'], 'not established')
        clearance = self.library.resolve('U1016-multivalent-clearance')
        self.assertIn('absorbing wash sink', clearance['statement'])
        tail = self.library.resolve('U1017-common-shutdown-tail')
        self.assertIn('symmetric old/new access', tail['statement'])
        self.assertIn('guaranteed T0>0', tail['statement'])
        self.assertIn('not just a longer expected access time', ' '.join(tail['contract']['requires']))
        contact = self.library.resolve('U1017-contact-before-shutdown')
        self.assertIn('no new contact can form afterwards', contact['statement'])
        unsupported = self.library.bridge('U1016-rooted-prefix-waste', 'U1017-common-shutdown-tail')
        self.assertIn('NO SUPPORTED CONNECTION', json.dumps(unsupported))

    def test_actual_default_wire_packets_fit_the_existing_budget(self):
        for identifier in ['N1016', 'N1017', *SUPPORT]:
            with self.subTest(identifier=identifier):
                result = subprocess.run([sys.executable, 'knowledge/retrieve.py', 'packet', identifier],
                                        cwd=ROOT, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertLessEqual(len(result.stdout), 32768)
                packet = json.loads(result.stdout)['packets'][0]
                self.assertTrue(packet['review_overlays'])


if __name__ == '__main__':
    unittest.main()
