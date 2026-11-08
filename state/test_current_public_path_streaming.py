"""Publication locator checks remain complete without buffering a corpus diff."""
import unittest
from unittest.mock import patch

from state.check_current import public_path_portability


class IteratedDiff:
    def __init__(self, lines, returncode=0):
        self.stdout = iter(lines)
        self.returncode = returncode

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def wait(self):
        return self.returncode


class PublicPathStreaming(unittest.TestCase):
    def test_relative_scientific_text_and_removed_locator_pass(self):
        lines = ['+++ b/research/result.txt\n',
                 '-Historical locator /Users/old/source.txt\n',
                 '+Read proofs/result.txt; gates/workspace is scientific notation.\n']
        with patch('state.check_current.subprocess.Popen', return_value=IteratedDiff(lines)):
            public_path_portability('a' * 40)

    def test_added_host_locators_keep_each_affected_filename(self):
        lines = ['+++ b/research/first.txt\n', '+Read /Users/research/private.txt\n',
                 '+++ b/knowledge/second.json\n', '+{"source":"file:///home/research/a"}\n']
        with patch('state.check_current.subprocess.Popen', return_value=IteratedDiff(lines)):
            with self.assertRaisesRegex(ValueError, 'knowledge/second.json, research/first.txt'):
                public_path_portability('a' * 40)

    def test_failed_git_diff_never_passes(self):
        import subprocess
        with patch('state.check_current.subprocess.Popen', return_value=IteratedDiff([], returncode=2)):
            with self.assertRaises(subprocess.CalledProcessError):
                public_path_portability('a' * 40)


if __name__ == '__main__':
    unittest.main()
