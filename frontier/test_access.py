"""Small integrity fixtures; no inference, benchmark or scientific experiment."""
import contextlib
import hashlib
import html
import importlib.util
import io
import json
from pathlib import Path
import sys
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
