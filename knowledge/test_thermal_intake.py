"""Protect actual packet budgets and the physically different thermal source routes."""
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import unittest

from knowledge.model import ROOT
from knowledge.retrieve import Library


UPDATE = Path('research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-rolling-thermal-memory')


class ThermalIntake(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_advertised_default_stdout_and_current_acceptance(self):
        entries = json.loads((ROOT / 'indexes/agent_catalog.d/2026-10-26-rolling-thermal-memory.json').read_text())['claims']
        for entry in entries:
            with self.subTest(card=entry['id']):
                command = shlex.split(entry['pointers']['read_local'])
                result = subprocess.run(command, cwd=ROOT, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertLessEqual(len(result.stdout), 32768)
                packet = json.loads(result.stdout)['packets'][0]
                self.assertEqual(packet['id'], entry['id'])
                for item in [packet] + [self.library.packet([u['id']])['packets'][0]
                                         for u in packet['related_units']]:
                    self.assertTrue(any(r['decision'] == 'accepted_internally_verified'
                                        for r in item['review_overlays']))

    def test_source_routes_retain_actual_operation_and_obstruction(self):
        cases = [
            ('U1009-helical-bare-kinetic-cost', 'COMPACT_LOCK_KINETIC_COST.md',
             ['P=p_Y+gL_phi', 'min(x^2,K)', 'There is NO assertion of second-moment convergence']),
            ('U1009-live-contact-spectral-limit', 'LIVE_CONTACT_EQUILIBRIUM.md',
             ['not a comparison of their Hamiltonian', 'partition functions at k and']),
            ('U1010-half-charge-canonical-memory', 'CANONICAL_MEMORY_SYMMETRY.md',
             ['C J C^dagger=-J', 'NONZERO even at the nominal doublet point']),
            ('U1010-conserved-static-force-no-heat', 'BOUNDED_FORCE_FLUCTUATION_PRINCIPLE.md',
             ['S(n)=beta Var(Q) only at n=0', 'it adds no', 'heat scattering']),
        ]
        for identifier, filename, passages in cases:
            with self.subTest(unit=identifier):
                result = self.library.source(identifier, 0)
                self.assertTrue(result['source']['path'].endswith('/' + filename))
                text = ' '.join(result['text'].split())
                for passage in passages:
                    self.assertIn(passage, text)
        dynamics = self.library.source('U1009-live-contact-spectral-limit', 1)['text']
        self.assertIn('not establish asymptotic completeness', ' '.join(dynamics.split()))
        self.assertIn('b=R(log R)^2', dynamics)
        memory = self.library.source('U1010-half-charge-canonical-memory', 1)['text']
        self.assertIn('does NOT have the divergent physical', memory)

    def test_exact_originals_and_reviewed_prefix_are_recoverable(self):
        rows = json.loads((ROOT / UPDATE / 'source/INDEX.json').read_text())['files']
        self.assertEqual(len(rows), 15)
        for row in rows:
            data = (ROOT / UPDATE / row['path']).read_bytes()
            self.assertEqual(len(data), row['bytes'])
            self.assertEqual(hashlib.sha256(data).hexdigest(), row['sha256'])
        geared = ROOT / UPDATE / 'source/geared'
        base = (geared / 'COMPACT_INERTIAL_AMPLIFIER_PRE_CONTACT_e6453da5.md').read_bytes()
        current = (geared / 'COMPACT_INERTIAL_AMPLIFIER.md').read_bytes()
        self.assertTrue(current.startswith(base))
        self.assertGreater(len(current), len(base))
        audit = self.library.source('N1009', 8)['text']
        self.assertIn(hashlib.sha256(base).hexdigest(), audit)
        self.assertNotIn(hashlib.sha256(current).hexdigest(), audit)
        for name in ['NORMAL_BAND_PREPARATION.md', 'LIVE_CONTACT_EQUILIBRIUM.md',
                     'LIVE_CONTACT_DYNAMICS.md', 'FINITE_APERTURE_READOUT.md']:
            self.assertIn(hashlib.sha256((geared / name).read_bytes()).hexdigest(), audit)
        self.assertIn('field-generator', self.library.resolve('N1010')['contract']['costs'])


if __name__ == '__main__':
    unittest.main()
