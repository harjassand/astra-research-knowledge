"""Read-only historical reconstruction preserves receipt bytes and exact-HEAD apply."""
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import test_generator as fixtures
import build_integration as builder
import validate_intake as validator
import fz_common as common


class HistoricalReconstruction(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.GeneratorBoundaries("test_read_only_plan_preserves_every_repository_byte_and_47_originals")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.plan = self.fixture.plan()
        builder.apply_plan(self.plan)  # Disposable synthetic repository only.
        self.original_check = builder.check_baseline
        self.descendant = "b" * 40

    def reconstruct(self, ancestor=True):
        with mock.patch.object(validator.subprocess, "run", return_value=subprocess.CompletedProcess([], 0 if ancestor else 1)):
            return validator.historical_reconstruction_summary(builder, self.fixture.root, self.fixture.curation,
                common.digest(common.encoded(self.fixture.curation)), self.descendant)

    def test_descendant_reconstructs_identical_output_without_writing(self):
        before = self.fixture.snapshot()
        summary, mode = self.reconstruct()
        self.assertEqual(summary["changed_file_count"], 0)
        self.assertEqual(mode, "historical_descendant_read_only_reconstruction")
        self.assertEqual(before, self.fixture.snapshot())
        self.assertIs(builder.check_baseline, self.original_check)
        self.original_check.assert_called_with(self.fixture.root, immutable_base=common.INITIAL_MAIN,
            expected_head=self.descendant, expected_remote_main=common.INITIAL_MAIN, phase="integrated", check_remote=False)

    def test_stale_apply_remains_rejected_after_descendant_reconstruction(self):
        self.reconstruct()
        before = self.fixture.snapshot()
        self.fixture.git.return_value = self.descendant
        with self.assertRaisesRegex(ValueError, "HEAD changed before apply"):
            builder.apply_plan(self.plan)
        self.assertEqual(before, self.fixture.snapshot())
        self.assertIs(builder.check_baseline, self.original_check)

    def test_nonancestor_rejects_before_reconstruction_or_writing(self):
        before = self.fixture.snapshot()
        with mock.patch.object(builder, "build_plan", wraps=builder.build_plan) as build:
            with self.assertRaisesRegex(ValueError, "not an ancestor"):
                self.reconstruct(ancestor=False)
            build.assert_not_called()
        self.assertEqual(before, self.fixture.snapshot())
        self.assertIs(builder.check_baseline, self.original_check)

    def test_failed_reconstruction_restores_exact_mutation_guard(self):
        with mock.patch.object(builder, "build_plan", side_effect=ValueError("fixture failure")):
            with self.assertRaisesRegex(ValueError, "fixture failure"):
                self.reconstruct()
        self.assertIs(builder.check_baseline, self.original_check)


if __name__ == "__main__":
    unittest.main(verbosity=2)
