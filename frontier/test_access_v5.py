"""Deterministic access/integrity fixtures; no scientific replay."""
import json
import hashlib
from pathlib import Path
import subprocess
import sys
import unittest

import retrieve_v5 as retrieve


class CurrentV5AccessTests(unittest.TestCase):
    def test_merged_manifest_and_later_claims(self):
        manifest = retrieve.access_manifest()
        self.assertEqual(manifest['counts']['cards'], 1012)
        identifiers = [
            'N954-p1-positive-quartic-record-bridge',
            'N955-p2-spin-correlation-pair-spectrum-selector',
            'N956-p3-recurrent-reaction-event-inference',
            'N957-xh1-sparse-multireactant-capture',
            'N958-ultra-compiled-canonical-weak-bridge-preparation',
            'N959-ultra-local-preparation-island-learner',
            'N960-ultra-lithium-elastic-ionic-skin-model',
            'N961-ultra-acoustic-thermal-range-lower-bound',
            'N962-ultra-distributed-rod-local-comparator',
            'N963-ultra-cm-compliance-spectral-moment',
        ]
        for identifier in identifiers:
            row = retrieve.resolve(identifier)
            self.assertEqual(row['claim_status'], 'source_derived_unreviewed')
            self.assertIn('CARD | raw=', retrieve.view(identifier).decode())

    def test_new_aliases_route_to_distinct_scopes(self):
        cases = [
            ('positive quartic interaction feedback complete record quantum noise covariance', 'N954'),
            ('nuclear spin RF correlated pair vibrational cross spectrum same atom', 'N955'),
            ('recurrent controller repeated conditioning coupled overlapping hazards reset fixed width', 'N956'),
            ('multireactant dilute feed persistent intermediate first order supply limited', 'N957'),
            ('canonical weak bridge fermion state preparation charge projection', 'N958'),
            ('local preparation island noisy trajectory acquired guard', 'N959'),
            ('lithium deposition elastic ionic skin moving interface anisotropic conductivity', 'N960'),
            ('acoustic thermal quantum range bound periodic mass spring graph displacement', 'N961'),
            ('distributed rods Fejer thermal conductance ordinary pendant comparator', 'N962'),
            ('center of mass compliance negative cubic spectral moment rank one spring', 'N963'),
        ]
        for query, prefix in cases:
            with self.subTest(query=query):
                routes = retrieve.task_routes(query, 12)['routes']
                selected = next((item for item in routes if item['id'].startswith(prefix + '-')), None)
                self.assertIsNotNone(selected, [item['id'] for item in routes])
                self.assertTrue(selected['dossier'].startswith('frontier/dossiers_v5/'), selected)

    def test_scoped_notices_surface_to_prior_cards(self):
        expectations = {
            'N927': 'SN-LATER-N954-P1-20261025',
            'N935': 'SN-LATER-N955-P2-20261025',
            'N937': 'SN-LATER-N956-P3-20261025',
            'N559': 'SN-LATER-N957-XH1-20261025',
            'N948': 'SN-LATER-N958-ULTRA-20261025',
            'N952': 'SN-LATER-N959-ULTRA-20261025',
            'N946': 'SN-LATER-N963-ULTRA-20261025',
        }
        for identifier, expected in expectations.items():
            with self.subTest(identifier=identifier):
                current = retrieve.notice(identifier)
                self.assertIn(expected, {n['notice_id'] for n in current['semantic_notices']})


    def test_v4_route_tree_remains_byte_stable(self):
        prior_path = retrieve.ROOT / 'agent/access_manifest.2026-10-24-constructive-universal-v4.json'
        prior = json.loads(prior_path.read_text())
        for route in ('frontier/dossiers/N950.txt', 'frontier/connections/N950.json',
                      'frontier/dossiers/N946.txt', 'frontier/connections/N946.json'):
            expected = prior['outputs'][route]
            actual = hashlib.sha256((retrieve.ROOT / route).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, route)
        self.assertTrue((retrieve.ROOT / 'frontier/dossiers_v5/N950.txt').is_file())
        self.assertTrue((retrieve.ROOT / 'frontier/connections_v5/N950.json').is_file())

    def test_source_manifest_has_hash_only_withheld_records(self):
        packet = retrieve.ROOT / 'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-25-later-completed-sources'
        manifest = json.loads((packet / 'source_manifest.json').read_text())
        self.assertEqual((manifest['selected_source_files'], manifest['copied_files'], manifest['withheld_files']), (171, 165, 6))
        for item in manifest['withheld']:
            self.assertEqual(set(item), {'id', 'bytes', 'sha256', 'git_blob', 'disposition'})
            self.assertNotIn('source_path', item)
            self.assertNotIn('name', item)

    def test_selected_source_bytes_verify_without_running_source_code(self):
        packet = 'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-25-later-completed-sources/verify_manifest.py'
        result = subprocess.run([sys.executable, str(retrieve.ROOT / packet)], cwd=retrieve.ROOT,
                                capture_output=True, text=True, check=True)
        summary = json.loads(result.stdout)
        self.assertEqual(summary['copied'], 165)
        self.assertEqual(summary['withheld_hash_only'], 6)
        self.assertFalse(summary['source_scripts_executed'])


if __name__ == '__main__':
    unittest.main()
