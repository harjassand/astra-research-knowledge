"""Fail-closed intake guards using in-memory fixtures; no science is executed."""
import contextlib
import importlib.util
import io
from pathlib import Path
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('ee_intake_validator', Path(__file__).with_name('validate.py'))
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class PreservationGuards(unittest.TestCase):
    def reject(self, patches, message):
        with contextlib.ExitStack() as stack:
            for replacement in patches:
                stack.enter_context(replacement)
            with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(ValueError) as caught:
                VALIDATOR.main()
            self.assertIn(message, str(caught.exception))

    def test_source_hash_cannot_be_relabelled(self):
        original = VALIDATOR.load

        def fixture(path):
            obj = original(path)
            if path == 'updates/EE/SOURCE_MANIFEST.json':
                obj['originals'][0]['sha256'] = '0' * 64
            return obj

        self.reject([patch.object(VALIDATOR, 'load', fixture)], 'original bytes/extent changed')

    def test_producer_manifest_does_not_authenticate_changed_output(self):
        original = VALIDATOR.load

        def fixture(path):
            obj = original(path)
            if path.endswith('/astra_intervention_products/manifest.json'):
                obj['verification_results.json'] = '0' * 64
            return obj

        self.reject([patch.object(VALIDATOR, 'load', fixture)], 'producer hash mismatch')

    def test_continuation_cannot_become_unproved_whole_claim_dependency(self):
        original_load, original_rows = VALIDATOR.load, VALIDATOR.rows

        def dependency(obj):
            if obj.get('card_id', '').startswith('N717-'):
                obj['depends_on'] = [{'target': 'N714-conservation-preserving-sparse-network-damage-resistance-oracle',
                                      'scope': 'fabricated whole-claim premise'}]
            return obj

        def fixture_load(path):
            obj = original_load(path)
            return dependency(obj) if path.startswith('frontier/cards/N717-') else obj

        def fixture_rows(path):
            objects = original_rows(path)
            return [dependency(o) for o in objects] if path == 'frontier/CURRENT_CLAIM_STATUS.jsonl' else objects

        self.reject([patch.object(VALIDATOR, 'load', fixture_load), patch.object(VALIDATOR, 'rows', fixture_rows)],
                    'whole-claim proof dependency invented')

    def test_unknown_model_cannot_be_fabricated(self):
        original = VALIDATOR.load

        def fixture(path):
            obj = original(path)
            if path.startswith('evaluation/workflows/records/RW-ee-theoretical-resonant-lifting/'):
                obj['model']['model_id'] = 'fabricated-measured-model'
            return obj

        self.reject([patch.object(VALIDATOR, 'load', fixture)], 'usage/model/independent validation invented')

    def test_unrelated_historical_navigation_cannot_change(self):
        original = VALIDATOR.sha
        target = (VALIDATOR.ROOT / 'frontier/dossiers/N700.txt').read_bytes()

        def fixture(data):
            return '0' * 64 if data == target else original(data)

        # Exercise this guard directly: later legitimate semantic notices may
        # stop main() at a separate frozen-projection check first.
        scientific = {'frontier/dossiers/N700.txt': original(target)}
        self.assertEqual(VALIDATOR.check_navigation_hashes(scientific, []), set())
        with patch.object(VALIDATOR, 'sha', fixture), self.assertRaisesRegex(
                ValueError, 'unscoped earlier navigation change'):
            VALIDATOR.check_navigation_hashes(scientific, [])


if __name__ == '__main__':
    unittest.main()
