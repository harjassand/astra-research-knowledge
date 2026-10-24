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
import retrieve_v4 as retrieve


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
            for name in ['frontier/retrieve_v4.py', 'frontier/CURRENT_CLAIM_STATUS.jsonl', card]:
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source / name, root / name)
            result = subprocess.run([sys.executable, str(root / 'frontier/retrieve_v4.py'), 'notice', 'N654'],
                                    capture_output=True, text=True, check=True)
            self.assertTrue(json.loads(result.stdout)['card_id'].startswith('N654-'))
            self.assertFalse((root / 'technology').exists())

    def test_problem_level_routes_find_scoped_source_predecessors(self):
        # Development fixtures from supplied diagnostics and scientific sources;
        # they are not independent or held-out validation questions.
        cases = [
            ('predict interacting quantum systems under continuous measurement and feedback', ('N928', 'N927')),
            ('ordinary equal pure loss with a calibrated sparse observation and a finite feedback record', ('N928',)),
            ('weak-bath predictor with scaled rates, coherent hopping, density interactions and a complete feedback record', ('N927',)),
            ('acquire compact models from reaction rules and reuse them for new predictions', ('N930',)),
            ('least rational-linear observable lumping for a nonexplosive polynomial-propensity chemical master equation', ('N930',)),
            ('explicit sparse rational propensities on an integer-jump network yield a reduced generator for supplied observables', ('N930',)),
        ]
        for query, expected in cases:
            with self.subTest(query=query):
                routes = retrieve.task_routes(query, 5)['routes']
                ids = [row['id'] for row in routes]
                for card_id in expected:
                    self.assertTrue(any(row.startswith(card_id + '-') for row in ids), ids)

    def test_coherent_later_cards_are_retrievable_by_their_distinct_scopes(self):
        cases = [
            ('replenishing thermal hot bath bosons port-labelled records', 'N934'),
            ('signed cross spectrum mixed Hessian direct force', 'N935'),
            ('organometallic stored primary alkyl partner tertiary radical', 'N936'),
            ('finite reaction gates next event censored no event', 'N937'),
            ('correlated post-event entrance mixture 73 rules 24 components', 'N938'),
            ('local bath feedback residual cross response cold receiver no advantage', 'N939'),
            ('toy reaction transport signalling synthetic network', 'N940'),
            ('classical replenished field full spatial resolution Hermite', 'N941'),
            ('Mo Ru nitrido transfer per nitrogen hydrogen paired turnovers', 'N942'),
            ('alkaline nitrite nitrate H2 fresh hydrogen ammonia process', 'N943'),
            ('nonflat cyclic clock qutrit static sum counterflow N>=4 d>=2', 'N944'),
        ]
        for query, expected in cases:
            with self.subTest(query=query):
                routes = retrieve.task_routes(query, 12)['routes']
                ids = [row['id'] for row in routes]
                self.assertTrue(any(row.startswith(expected + '-') for row in ids), ids)

    def test_coherent_later_semantic_notices_reach_normal_reader(self):
        hot = retrieve.notice('N934')
        hot_notice_ids = {n['notice_id'] for n in hot['semantic_notices']}
        self.assertIn('SN-COHERENT-N934-p1-hot-bath-20261024', hot_notice_ids)
        self.assertIn('SN-COHERENT-N941-p1-classical-field-20261024', hot_notice_ids)
        hot_scope = next(n for n in hot['semantic_notices'] if n['notice_id'] == 'SN-COHERENT-N934-p1-hot-bath-20261024')
        self.assertIn('N927-p1-weak-bath-positive-predictor-prior', hot_scope['card_ids'])

        # These two older sidecars are pinned by immutable checkpoints; the
        # current shard must still expose the new scoped distinction in reads.
        force = retrieve.notice('N931')
        self.assertIn('SN-COHERENT-N935-p2-cross-force-20261024', [n['notice_id'] for n in force['semantic_notices']])
        partner = retrieve.notice('N932')
        self.assertIn('SN-COHERENT-N936-xh1-partner-memory-20261024', [n['notice_id'] for n in partner['semantic_notices']])

        classical = retrieve.notice('N941')
        self.assertEqual(classical['semantic_notices'][0]['notice_id'], 'SN-COHERENT-N941-p1-classical-field-20261024')
        self.assertEqual({u['target'] for u in classical['material_updates']}, {
            'N927-p1-weak-bath-positive-predictor-prior',
            'N928-p1-ordinary-loss-husimi-record-law',
            'N934-p1-replenishing-quantum-hot-bath',
        })

        p3 = retrieve.notice('N938')
        self.assertIn('SN-COHERENT-N938-p3-correlated-entrance-20261024', [n['notice_id'] for n in p3['semantic_notices']])
        dossier = retrieve.view('N938').decode()
        self.assertIn('3.774e-9', dossier)
        self.assertIn('Rare-event conditioning needs a nonzero denominator lower bound.', dossier)

    def test_checkpoint_pinned_builder_and_frozen_notice_log_remain_unchanged(self):
        self.assertEqual(build.digest((retrieve.ROOT / 'frontier/build_access.py').read_bytes()),
                         '77bbfe292b9117129a212382475307d43da55ad6846c22bd07b744209da8625c')
        self.assertEqual(build.digest((retrieve.ROOT / 'agent/SEMANTIC_NOTICES.jsonl').read_bytes()),
                         'c19e7a935f69e1c049cade4f2030c2140cf70bc02c867f8348d6916dbd92215b')

    def test_pasted_closeout_result_families_remain_retrievable(self):
        # This summary is already preserved byte-for-byte in the closeout intake.
        # These are routing fixtures, not independent validation or a benchmark.
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

    def test_unrelated_named_result_controls_do_not_route_to_p1_or_p3(self):
        controls = [
            ('rank-one gradient laminate compiler uses each original face once', 'N920'),
            ('small commutator conditional expectations have no exact commuting repair', 'N918'),
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
            (root / retrieve.MANIFEST_PATH).parent.mkdir(parents=True, exist_ok=True)
            (root / retrieve.MANIFEST_PATH).write_text(json.dumps(manifest))
            self.assertEqual(retrieve.access_manifest(), manifest)
            (root / 'input.txt').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'inputs changed'):
                retrieve.access_manifest()



class CurrentVersionedRouteTests(unittest.TestCase):
    def test_current_manifest_and_new_cards_are_retrievable(self):
        manifest = retrieve.access_manifest()
        self.assertEqual(manifest["counts"]["cards"], 1002)
        for identifier in ("N945", "N950", "N953"):
            row = retrieve.resolve(identifier)
            self.assertTrue(row["card_id"].startswith(identifier + "-"))
            self.assertIn("CARD | raw=", retrieve.view(identifier).decode())

    def test_new_scoped_notices_reach_existing_cards(self):
        cases = {
            "N932": "SN-XH1-partner-operation-capacity-20261024",
            "N936": "SN-XH1-partner-operation-capacity-20261024",
            "N940": "SN-XH2-abstract-controller-scope-20261024",
            "N953": "SN-XH2-abstract-controller-scope-20261024",
            "N937": "SN-COHERENT-N950-p3-all-input-kernel-20261024",
            "N938": "SN-COHERENT-N950-p3-all-input-kernel-20261024",
        }
        for identifier, expected in cases.items():
            with self.subTest(identifier=identifier):
                result = retrieve.notice(identifier)
                notice_ids = [notice["notice_id"] for notice in result["semantic_notices"]]
                self.assertIn(expected, notice_ids)

    def test_xh2_card_keeps_withheld_source_and_physical_limits_explicit(self):
        row = retrieve.resolve("N953")
        self.assertEqual(row["claim_status"], "source_derived_unreviewed")
        self.assertIn("withheld", row["proof_availability"]["classification"])
        self.assertEqual(row["validation"]["physical_capability"], "NOT_ACQUIRED")
        source_hashes = {ref.get("original_sha256") for ref in row["proof_availability"]["available_evidence_sources"]}
        self.assertIn("3f46c73aaae4e7fd36bf4fa6038e80fb55ace7c749e48686a6d6e0257b42e542", source_hashes)

    def test_xh1_capacity_boundary_points_to_its_completion_report(self):
        row = retrieve.resolve("N936")
        updates = [
            update for update in row["material_updates"]
            if update.get("target") == row["card_id"]
            and update.get("relation") == "scoped_capacity_boundary_not_invalidation"
        ]
        self.assertEqual(len(updates), 1)
        evidence = updates[0]["evidence"]
        self.assertEqual([item["id"] for item in evidence], ["src-xh1-partner-operation-2131"])
        self.assertTrue(evidence[0]["path"].endswith(
            "/source/XH1_completed_partner_operation/XH1_physical_partner_operation_completed_2131_20261024.json"
        ))
        self.assertEqual(evidence[0]["sha256"], "7e3aeb46f94ba8d88ea44a8ec3d1816f3822792d560e50509e06fe3a4128f885")


if __name__ == '__main__':
    unittest.main()
