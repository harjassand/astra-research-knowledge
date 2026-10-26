"""Protect metric, exposure and source-branch boundaries of the completed study.

These are retrieval/provenance regressions; the substantive mathematical audits
are preserved originals. No scientific script or model is launched here.
"""
import hashlib
import json
import subprocess
import sys
import unittest
from knowledge.model import ROOT
from knowledge.retrieve import Library

UPDATE = 'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-completed-method-study'


class CompletedMethodStudy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = Library()

    def test_decisive_source_branches(self):
        # Similar titles/hashes cannot replace the actual relevant passage.
        for identifier, fragment, passage in [
            ('U1035-reciprocal-tree-pulse-frontier', 'q17s1/PROOF.md', 'No generalization of the heat-capacity bound to looped graphs'),
            ('U1035-memoryless-switch-frontier', 'q17s2/SWITCH_PROOF.md', 'Global certificate over arbitrary admissible curves'),
            ('U1036-finite-reverse-transfer-floor', 'q42s2/REVERSE_TRANSFER_PROOF.md', 'terminal-avoiding'),
            ('U1037-capacity-anchored-shunt-calibration', 'q63s2/PROOF_STAGE2.md', 'two *real positive Laplace points*'),
            ('U1039-compatible-force-ceiling-certificate', 'q54s2/GOVERNING_PROOF.md', 'strictly inside every non-anchor measurement interval'),
            ('U1040-one-sided-equilibrium-tolerance', 'q95s2/PROOF.md', 'It cannot certify exact g=0 at finite time'),
        ]:
            with self.subTest(identifier=identifier):
                result = self.library.source(identifier)
                self.assertIn(fragment, result['source']['path'])
                self.assertIn(passage, result['text'])

    def test_frozen_cutoff_and_later_refinement_have_different_sources(self):
        frozen = self.library.source('U1038-free-umegaki-comparison-formula')
        later = self.library.source('U1038-post-exposure-numerator-span-cutoff', 2)
        self.assertIn('q28s2/finite_reference_proof.md', frozen['source']['path'])
        self.assertIn('n+m_K+m_L', frozen['text'])
        self.assertIn('audit/PRIOR_COMPARISON.md', later['source']['path'])
        self.assertIn('post-exposure reviewer inference', later['text'])
        self.assertIn('m_K+1', later['text'])
        failure = self.library.source('U1038-biased-reset-index-transfer-failure')
        self.assertIn('q28s1/binary_channel_proof.md', failure['source']['path'])
        self.assertIn('(19-\\sqrt{105})/32', failure['text'])
        self.assertIn('does not refute N967', failure['text'])
        old = self.library.resolve('N676')
        new = self.library.resolve('U1038-free-umegaki-comparison-formula')
        transfers = self.library.bridge(old['id'], new['id'])['transfers']
        self.assertTrue(any(t['state'] == 'INCOMPATIBLE ASSUMPTIONS' and 'pointwise' in t['scope'] for t in transfers))

    def test_originals_and_excluded_caches(self):
        index = json.loads((ROOT / UPDATE / 'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']), 280)
        for row in index['files']:
            self.assertNotIn('__pycache__', row['path'])
            self.assertFalse(row['path'].endswith(('.pyc', '.html', '.htm')))
            self.assertNotIn('/replay_stage2/', row['path'])
            self.assertEqual(hashlib.sha256((ROOT / UPDATE / row['path']).read_bytes()).hexdigest(), row['sha256'])
        manifest = json.loads((ROOT / UPDATE / 'source/audit/checks/source_manifest.json').read_bytes())
        for name, sha in manifest.items():
            if name.endswith(('.md', '.py', '.json', '.txt')):
                self.assertEqual(hashlib.sha256((ROOT / UPDATE / 'source/q28s2' / name).read_bytes()).hexdigest(), sha)

    def test_six_exact_workflows_do_not_invent_compute_or_fresh_rounds(self):
        for q in ['q17', 'q42', 'q63', 'q28', 'q54', 'q95']:
            trace = json.loads((ROOT / f'evaluation/workflows/records/RW-method-study-{q}/v0001.json').read_bytes())
            self.assertEqual(trace['mode'], 'new_instance')
            self.assertIn('warm continuation', trace['context']['retained_context'])
            self.assertIsNone(trace['matched_run_id'])
            self.assertTrue(all(v is None for v in trace['model'].values()))
            self.assertTrue(all(v is None for v in trace['resources']['usage'].values()))
            self.assertIsNone(trace['resources']['reported_inference_seconds'])
            self.assertEqual(trace['advance']['verification'], 'independent_receipt')
            refs = {r['id']: r for r in trace['refs']}
            self.assertEqual(set(trace['advance']['verification_receipt']['checked_output_sha256']),
                             {refs[k]['sha256'] for k in trace['output_ref_ids']})

    def test_acceptance_remains_version_bound_and_physical_gaps_survive(self):
        for number in range(1034, 1041):
            record = self.library.resolve(f'N{number}')
            review = next(r for r in record['review_overlays'] if r['id'] == f'A{number+20}-method-study')
            self.assertEqual(review['decision'], 'accepted_internally_verified')
            self.assertIn({'id': record['id'], 'content_version': record['content_version']}, review['subjects'])
            self.assertEqual(review['working_device'], 'not established')
            self.assertEqual(review['historical_priority'], 'UNKNOWN')
        source = self.library.source('N1037', 3)['text']
        self.assertIn('0/8', source)
        self.assertIn('ordinary constrained joint fit is stronger', source)

    def test_default_complete_packet_budget_including_wire_metadata(self):
        # Complete corrections, review and transfers must fit, not just a preview.
        identifiers = [r['id'] for r in self.library.records.values()
                       if r['id'].split('-')[0] in
                       {f'{prefix}{n}' for prefix in ['N', 'U'] for n in range(1034, 1041)}]
        self.assertEqual(len(identifiers), 21)
        for identifier in identifiers + ['N965', 'N970', 'N676', 'N967']:
            self.library.packet([identifier])
        for identifier in ['U1038-free-umegaki-comparison-formula',
                           'U1038-post-exposure-numerator-span-cutoff',
                           'N965', 'N970', 'N676', 'N967']:
            result = subprocess.run([sys.executable, 'knowledge/retrieve.py', 'packet', identifier],
                                    cwd=ROOT, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertLessEqual(len(result.stdout), 32768)


if __name__ == '__main__':
    unittest.main()
