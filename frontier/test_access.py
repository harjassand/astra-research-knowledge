"""Small integrity fixtures; no inference, benchmark or scientific experiment."""
import contextlib
import hashlib
import html
import importlib.util
import io
import json
from pathlib import Path
import sys
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import build_access as build
import retrieve


class PublicAccessTests(unittest.TestCase):
    def test_source_hash_selects_source_after_banner_and_preserves_cr(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = b'Theorem: forall x.\r\nProof: \\nabla f(x)=0.\n'
            page = '<pre>New correction banner, unrelated line count</pre><pre>' + html.escape(raw.decode()) + '</pre>'
            (root / 'source.html').write_bytes(page.encode())
            ref = {'path': 'not-exported.txt', 'read_path': 'source.html', 'sha256': build.digest(raw)}
            inputs = {}
            result = build.source_text(root, ref, inputs)
            self.assertEqual(result.encode(), raw)
            self.assertEqual(inputs['source.html'], build.digest(page.encode()))
            ref['sha256'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'hash cannot be recovered'):
                build.source_text(root, ref, {})

    def test_paths_cannot_escape_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'outside repository'):
                build.local(Path(directory), '../outside.txt')

    def test_legacy_identifiers_remain_unambiguous(self):
        self.assertEqual(build.route_id('N533-long-title'), 'N533')
        self.assertEqual(build.route_id('L01-title'), 'L01')
        self.assertEqual(build.route_id('P-q-d'), 'P-q-d')
        self.assertEqual(build.route_id('W-frontier-check-lsi'), 'W-frontier-check-lsi')

    def test_optional_technology_route_keeps_current_source_notice(self):
        with patch.object(sys, 'argv', ['retrieve', 'technology', 'N654', '--limit', '2']):
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                retrieve.main()
            result = json.loads(output.getvalue())
        self.assertTrue(result['source_notice']['card_id'].startswith('N654-'))
        self.assertLessEqual(len(result['technology']['routes']), 2)
        self.assertTrue(all(not r['fixture'] for r in result['technology']['routes']))
        self.assertTrue(result['technology']['navigation_is_not_applicability'])

    def test_mathematical_notice_works_without_technology_files(self):
        source = retrieve.ROOT
        card = retrieve.resolve('N654')['card_path']
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ['frontier/retrieve.py', 'frontier/CURRENT_CLAIM_STATUS.jsonl', card]:
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source / name, root / name)
            result = subprocess.run([sys.executable, str(root / 'frontier/retrieve.py'), 'notice', 'N654'],
                                    capture_output=True, text=True, check=True)
            self.assertTrue(json.loads(result.stdout)['card_id'].startswith('N654-'))
            self.assertFalse((root / 'technology').exists())

    def test_problem_level_routes_find_scoped_source_predecessors(self):
        cases = [
            ('predict interacting quantum systems under continuous measurement and feedback', ('N928', 'N927')),
            ('simulate the observed photon-counting history of an interacting open bosonic lattice with adaptive controls', ('N928',)),
            ('positive classical prediction of a lossy quantum optical experiment starting from arbitrary initial states', ('N928',)),
            ('acquire compact models from reaction rules and reuse them for new predictions', ('N930',)),
            ('derive the smallest exact linear set of observables needed to predict a stochastic chemical reaction network', ('N930',)),
            ('reduce a supplied polynomial reaction network while preserving stochastic trajectories of chosen readouts', ('N930',)),
        ]
        for query, expected in cases:
            with self.subTest(query=query):
                routes = retrieve.task_routes(query, 5)['routes']
                ids = [row['id'] for row in routes]
                for card_id in expected:
                    self.assertTrue(any(row.startswith(card_id + '-') for row in ids), ids)

    def test_pasted_closeout_result_families_remain_retrievable(self):
        # This summary is already preserved byte-for-byte in the closeout intake.
        # These paraphrases keep its major result families reachable as metadata.
        cases = [
            ('quadratic communication gain for recurrent quantum memory at small coupling', 'N914'),
            ('inaccessible Bell-pair inventory has an entropy cost', 'N915'),
            ('two adaptive actions identify hidden-star connectivity', 'N916'),
            ('finite-energy heavy-tail quantum amplifier entropy after added heat', 'N917'),
            ('small commutator but no nearby exact commuting repair for conditional expectations', 'N918'),
            ('quadratic range avoidance acquires a codimension-five flat with NP queries', 'N919'),
            ('rank-one gradient compiler uses each original face once', 'N920'),
            ('a five-output quadratic well has a finite laminate-tree barrier', 'N921'),
            ('fixed quantum code covers a factor-two band of unknown gain', 'N923'),
            ('pay to install a public quantum program and reuse code memory', 'N924'),
            ('physical historical searches exposed reset costs and baseline failures', 'N925'),
        ]
        for query, expected in cases:
            with self.subTest(query=query):
                ids = [row['id'] for row in retrieve.task_routes(query, 5)['routes']]
                self.assertTrue(any(row.startswith(expected + '-') for row in ids), ids)

    def test_unrelated_controls_keep_their_existing_routes(self):
        controls = [
            ('local biological signals control multicellular organization', 'N433'),
            ('programmable selective chemical transformations reusable catalysis', 'L04'),
        ]
        for query, expected in controls:
            with self.subTest(query=query):
                ids = [row['id'] for row in retrieve.task_routes(query, 5)['routes']]
                self.assertTrue(any(row.startswith(expected + '-') for row in ids), ids)
                self.assertFalse(any(row.startswith(('N928-', 'N930-')) for row in ids), ids)

    def test_packet_budget_fails_without_partial_output(self):
        content = 'forall ε>0: κόστος\n'.encode()
        with patch.object(retrieve, 'access_manifest', return_value={}), patch.object(retrieve, 'resolve', return_value={'card_id': 'N01'}), patch.object(retrieve, 'view', return_value=content), patch.object(sys, 'argv', ['retrieve', 'packet', 'N01', '--max-bytes', str(len(content) - 1)]):
            output = io.StringIO()
            with contextlib.redirect_stdout(output), self.assertRaisesRegex(ValueError, 'No card, correction or proof locator was truncated'):
                retrieve.main()
            self.assertEqual(output.getvalue(), '')

    def test_stale_input_and_view_refused(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(retrieve, 'ROOT', Path(directory)):
            root = Path(directory)
            (root / 'agent').mkdir()
            (root / 'input.txt').write_bytes(b'original')
            manifest = {'inputs': {'input.txt': build.digest(b'original')}, 'outputs': {}}
            (root / 'agent/access_manifest.json').write_text(json.dumps(manifest))
            self.assertEqual(retrieve.access_manifest(), manifest)
            (root / 'input.txt').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'inputs changed'):
                retrieve.access_manifest()


if __name__ == '__main__':
    unittest.main()
