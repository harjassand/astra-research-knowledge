"""Old frozen notes must reach their actual premises, laws and compatible bridge."""
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

from knowledge.model import ROOT
from knowledge.retrieve import Library

UPDATE = Path('research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-old-ultra-relations')
NOTES = {
    'GUARDED_RELATION_RETENTION_FIRST_CONSTRUCTION.md': ('U1014-equality-guarded-semantic-relation', 'a4547ca312d20b9f6119a4f378e58b366a8d164934e2741789e4a22b9c969727'),
    'ORDINAL_EXPERIMENT_TRANSFER.md': ('U1014-ordinal-new-law-chart-transfer', '95b7226863a56d4ccc4e25e6d777d65a7638201a1a46db21e887191b281696ee'),
    'FORWARD_COUPLING_ESCAPE_FIRST_CONSTRUCTION.md': ('U1015-forward-joint-cover', 'eed1305ad518b9a1854265c57b01efdd5da198ae5fdbb0513545d687d3de96e6'),
    'JOINT_PREPARATION_FRONTIER.md': ('U1015-claw-free-active-pair-boundary', '0d0ab66adeb254d726ac8e0a0b821be93bc0e18988c5f87da4e88ddb6771c27b'),
}


class OldUltraRelations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_four_actual_hash_links_and_exact_completed_audit(self):
        index = json.loads((ROOT / UPDATE / 'source/INDEX.json').read_text())
        self.assertEqual(len(index['files']), 4)
        audit = index['reused_root_audit']
        raw_audit = (ROOT / audit['path']).read_bytes()
        self.assertEqual(hashlib.sha256(raw_audit).hexdigest(), audit['sha256'])
        self.assertEqual(audit['sha256'], '60ac39bb42d23d8107bf34f1137616d3e1bb8d6a31ce31d230bbf6f17c7bd815')
        passage = '\n'.join(raw_audit.decode().splitlines()[audit['lines'][0]-1:audit['lines'][1]])
        for filename, (identifier, expected_hash) in NOTES.items():
            with self.subTest(note=filename):
                row = next(r for r in index['files'] if r['path'].endswith('/' + filename))
                data = (ROOT / UPDATE / row['path']).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), expected_hash)
                self.assertEqual(len(data), row['bytes'])
                self.assertIn(expected_hash, passage)
                unit = self.library.resolve(identifier)
                self.assertIn(expected_hash, {r['sha256'] for r in unit['evidence']})
                source = self.library.source(identifier, 0)
                self.assertTrue(source['source']['path'].endswith('/' + filename))
                self.assertEqual(source['source']['sha256'], expected_hash)
                self.assertTrue(unit['review_overlays'])
        self.assertNotIn('CURRENT_CONTINUATION', json.dumps(index['files']))

    def test_observation_law_and_joint_interface_are_not_silently_changed(self):
        guarded = self.library.source('U1014-equality-guarded-semantic-relation', 0)['text']
        self.assertIn('Pr[accept AND R>eta]<=delta', guarded)
        self.assertIn('TRUE three-way', guarded)
        self.assertIn('K0(x,.)=nu(.|h=h(x))', guarded)
        unit = self.library.resolve('U1014-equality-guarded-semantic-relation')
        self.assertIn('On acceptance outside the bad event', unit['statement'])
        ordinal = self.library.source('U1014-ordinal-new-law-chart-transfer', 0)['text']
        self.assertIn('NEW finite experimental law', ordinal)
        self.assertIn('L_Y', ordinal)
        self.assertIn('not a claim that arbitrary future tasks are related', ordinal)
        forward = self.library.source('U1015-forward-joint-cover', 0)['text']
        self.assertIn('does NOT accept an arbitrary', forward)
        self.assertIn('charged ONCE here, not r times', forward)
        barrier = self.library.source('U1015-claw-free-active-pair-boundary', 0)['text']
        self.assertIn('not inferred from the mere', barrier)
        self.assertIn('UNKNOWN retained as an extra output', barrier)
        self.assertIn('TV exactly', barrier)
        bridge = self.library.bridge('U1015-forward-joint-cover', 'U1014-equality-guarded-semantic-relation')['transfers'][0]
        self.assertEqual(bridge['state'], 'ESTABLISHED COMPATIBLE INTERFACE')
        for prefix in ['from', 'to']:
            self.assertEqual(bridge[prefix + '_version'], self.library.resolve(bridge[prefix])['content_version'])
        self.assertIn('eta+2epsilon', bridge['scope'])
        self.assertTrue(any('eta_eff=eta+2epsilon' in x for x in bridge['remaining_obligations']))
        unsupported = self.library.bridge('U1015-claw-free-active-pair-boundary', 'U1014-equality-guarded-semantic-relation')
        self.assertIn('NO SUPPORTED CONNECTION', json.dumps(unsupported))

    def test_actual_default_packets_and_unit_budgets(self):
        for identifier in ['N1014', 'N1015', *(value[0] for value in NOTES.values())]:
            with self.subTest(identifier=identifier):
                result = subprocess.run([sys.executable, 'knowledge/retrieve.py', 'packet', identifier],
                                        cwd=ROOT, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertLessEqual(len(result.stdout), 32768)
                packet = json.loads(result.stdout)['packets'][0]
                self.assertTrue(any(r['decision'] == 'accepted_internally_verified' for r in packet['review_overlays']))


if __name__ == '__main__':
    unittest.main()
