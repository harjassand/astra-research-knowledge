"""Final source routes must preserve causal contracts, operation scope and failures."""
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

from knowledge.model import ROOT
from knowledge.retrieve import Library

UPDATE = Path('research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-ultra-final-closeout')


class UltraCloseout(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_decisive_learning_and_thermal_source_routes(self):
        frame = self.library.source('U1011-conditional-affine-frame-constructor', 1)['text']
        self.assertIn('return UNKNOWN', frame)
        self.assertIn('g_cond(Q)<=g(Q)', frame)
        census = self.library.source('U1011-fixed-address-win-census', 1)['text']
        self.assertIn('contains the requested x', census)
        self.assertIn('B and Q are fixed before', census)
        self.assertIn('3577 n D_n R', census)
        curve = self.library.source('U1012-nonlinear-curvature-excess', 0)['text']
        self.assertIn('c+S_f(n)', curve)
        self.assertIn('Dropping the contact', curve)
        self.assertIn('exact domination need not survive', curve)
        pulse = self.library.resolve('U1012-full-ladder-finite-pulse')
        self.assertIn('No automatic application to nonlinear', ' '.join(pulse['contract']['assumptions']))
        bridge = self.library.bridge('U1012-finite-aperture-static-dipole', 'U1012-full-ladder-finite-pulse')
        self.assertIn('NO SUPPORTED CONNECTION', json.dumps(bridge))

    def test_actual_audit_versions_and_reported_only_comparison(self):
        learned = self.library.source('N1011', 5)['text']
        for name in ['CONDITIONAL_AFFINE_FRAME_BOOTSTRAP.md', 'ADDRESS_CORRUPTED_COMPARISON_BOOTSTRAP.md']:
            p = ROOT / UPDATE / 'source/learning/warm_incomplete_experience' / name
            self.assertIn(hashlib.sha256(p.read_bytes()).hexdigest(), learned)
        audit = self.library.source('N1012', 4)['text']
        for name in ['ROOT_FINITE_APERTURE_CANONICAL_MEMORY.md', 'ROOT_NONLINEAR_BOUNDED_FORCE_RESOURCE_BOUND.md',
                     'CANONICAL_SECTOR_RESPONSE.md', 'FIXED_NORMAL_GAP_RESOLVENT.md']:
            p = ROOT / UPDATE / 'source/thermal' / name
            self.assertIn(hashlib.sha256(p.read_bytes()).hexdigest(), audit)
        card = self.library.resolve('N1010')
        self.assertTrue(any(r['id'] == 'A1020-N1010-final-successor-route' for r in card['review_overlays']))
        self.assertTrue(any(r['id'] == 'A1019-bounded-force-canonical-memory' for r in card['historical_reviews']))
        old_unit = self.library.resolve('U1010-half-charge-canonical-memory')
        self.assertTrue(any(r['id'] == 'A1019-bounded-force-canonical-memory' for r in old_unit['review_overlays']))
        report = self.library.resolve('U1013-reported-withdrawal-discriminator')
        self.assertEqual(report['review_overlays'], [])
        self.assertIn('not_whole_audited', report['review']['acceptance'])
        self.assertIn('Imax=', report['statement'])

    def test_failed_withdrawal_is_not_first_passage_or_stored_energy_success(self):
        root = ROOT / UPDATE / 'source/frontier'
        cases = json.loads((root / 'light_ion_checks_results.json').read_text())['cases']
        success = next(c for c in cases if c['current_max_pa'] == 150 and c['nat'] == 0 and c['method'] == 'BDF')
        failed = next(c for c in cases if c['current_max_pa'] == 100 and c['nat'] == 0 and c['method'] == 'BDF')
        self.assertTrue(success['handoff_final_ionic_thresholds'])
        self.assertFalse(failed['handoff_final_ionic_thresholds'])
        self.assertGreater(failed['net_light_ion_and_capacitor_free_energy_gain_j'],
                           success['net_light_ion_and_capacitor_free_energy_gain_j'])
        handoff = json.loads((root / 'light_ion_handoff_results.json').read_text())['cases']
        failed = next(c for c in handoff if c['current_max_pa'] == 100 and c['nat_during_light'] == 0 and c['light_s'] == 600)
        self.assertEqual(failed['first_sampled_ionic_return_after_handoff_s'], 0)
        self.assertFalse(failed['handoff_final_passes_provisional_ionic_thresholds'])
        routed = self.library.source('U1013-reported-withdrawal-discriminator', 3)
        self.assertTrue(routed['source']['path'].endswith('light_ion_checks_results.json'))
        self.assertIn('"current_max_pa": 100.0', routed['text'])
        self.assertIn('"handoff_final_ionic_thresholds": false', routed['text'])

    def test_original_bytes_and_actual_default_commands(self):
        rows = json.loads((ROOT / UPDATE / 'source/INDEX.json').read_text())['files']
        self.assertEqual(len(rows), 31)
        for row in rows:
            raw = (ROOT / UPDATE / row['path']).read_bytes()
            self.assertEqual(len(raw), row['bytes'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row['sha256'])
        for number in ['N1010', 'N1011', 'N1012', 'N1013']:
            with self.subTest(card=number):
                result = subprocess.run([sys.executable, 'knowledge/retrieve.py', 'packet', number],
                                        cwd=ROOT, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertLessEqual(len(result.stdout), 32768)
                packet = json.loads(result.stdout)['packets'][0]
                self.assertTrue(packet['review_overlays'])
                for unit in packet['related_units']:
                    self.library.packet([unit['id']])


if __name__ == '__main__':
    unittest.main()
