"""The historical-index regression must fail before a preflight can pass."""
import contextlib
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest import mock
from state import check_current


class RetainedPreflight(unittest.TestCase):
    def test_pinned_evidence_is_checked_before_preflight_returns(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'indexes/claims.jsonl'
            path.parent.mkdir()
            original = b'{"id":"N1"}\n'
            path.write_bytes(original)
            ref = dict(id='historical-index', path='indexes/claims.jsonl',
                       sha256=hashlib.sha256(original).hexdigest(), lines=[1, 1],
                       status='immutable fixture source')
            def validate(*args):
                check_current.checkpoints.validate_evidence_refs([ref], root)
            with mock.patch('sys.argv', ['check_current.py', '--base-revision', 'a'*40, '--preflight-only']), \
                 mock.patch.object(check_current.checkpoints, 'git'), \
                 mock.patch.object(check_current, 'historical_integrity'), \
                 mock.patch.object(check_current, 'public_path_portability'), \
                 mock.patch.object(check_current, 'publication_membership'), \
                 mock.patch.object(check_current, 'retained_publication', side_effect=validate) as retained, \
                 mock.patch.object(check_current, 'run') as tests, \
                 contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(check_current.main(), 0)
                path.write_bytes(b'{"id":"N1","new":"overwrote history"}\n')
                self.assertEqual(check_current.main(), 1)
                self.assertEqual(retained.call_count, 2)
                tests.assert_not_called()
