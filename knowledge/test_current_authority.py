"""Current authority, genuine conditions, version drift and old-handle guards."""
import copy
import json
import subprocess
import unittest
from types import SimpleNamespace

from knowledge.build import build
from knowledge.model import encoded
from knowledge.operations import (compile_current_consumers, consumer_contract,
                                  operation_frame, statement_view, CURRENT_CONSUMER_LAYOUT)
from knowledge import test_knowledge as fixture_support
from knowledge.mcp_adapter import ResearchAdapter, consumer_view_layout
from knowledge.test_mcp_adapter import complete
from knowledge.retrieve import Library


def annotations(record, source):
    subject = {"id": record["id"], "content_version": record["content_version"]}
    authority = {"notice_id": "SN-standing", "kind": "human_acceptance_instruction",
        "current_programme_status": "CORRECT_AND_ACCEPTED", "accepted_subjects": [subject],
        "new_audit": False, "legacy_status_fields_are_historical": True, "card_ids": [record["id"]],
        "clarification": "The finite source is accepted at its stated scope; prior review requests are historical.",
        "source_refs": [source]}
    current = {"requires": "Actual finite input and independent noise", "provides": "The qualified finite bound",
        "assumptions": "Independent noise; no extension to correlated noise or a physical measurement",
        "costs": "Paid source acquisition and arithmetic", "units": "seconds", "obstruction": "No free source or precision"}
    projection = {"notice_id": "SN-current-view", "kind": "current_consumer_projection",
        "authority_notice_id": authority["notice_id"], "card_ids": [record["id"]], "source_refs": [source],
        "consumer_views": [{"subject": subject, "statement": "The same finite conditional source result.",
                            "contract": current, "scope": "Current view of the same accepted scope; no new audit."}]}
    return authority, projection


class CurrentAuthorityTests(unittest.TestCase):
    def records(self):
        original = {"id": "N1-finite", "kind": "result", "title": "Finite mechanism",
            "content_version": "1" * 64, "body": "Historical source bytes remain unreviewed at creation.",
            "statement": "A source-reported finite result.", "contract": {key: "Old source unreviewed; external review requested"
                for key in ("requires", "provides", "assumptions", "costs", "units", "obstruction")}, "notices": []}
        authority, projection = annotations(original, {"path": "acceptance.txt", "sha256": "2" * 64,
                                                       "lines": [1, 1], "quote": "Standing instruction"})
        original["notices"] = [authority, projection]
        other = dict(copy.deepcopy(original), id="N2-context-only", content_version="3" * 64)
        return [original, other]

    def test_current_view_precedes_old_status_without_discarding_actual_conditions(self):
        records = self.records();before = copy.deepcopy(records[0])
        compile_current_consumers(records);r = records[0]
        self.assertEqual(r["content_version"], before["content_version"])
        self.assertEqual(r["contract"], before["contract"])
        self.assertEqual(r["body"], before["body"])
        self.assertNotIn("unreviewed", consumer_contract(r)["provides"])
        self.assertIn("Independent noise", consumer_contract(r)["assumptions"])
        self.assertIn("correlated noise", consumer_contract(r)["assumptions"])
        self.assertEqual(statement_view(r, operation_frame(r))["statement"], r["current_consumer"]["statement"])
        self.assertFalse(r["current_acceptance"][0]["new_audit"])
        self.assertNotIn("current_acceptance", records[1])
        self.assertNotIn("current_consumer", records[1])
        expected = copy.deepcopy(records)
        compile_current_consumers(records)
        self.assertEqual(records, expected)
        records[0]["notices"] = []
        records[1]["notices"] = []
        compile_current_consumers(records)
        self.assertNotIn("current_acceptance", records[0])
        self.assertNotIn("current_consumer", records[0])

    def test_stale_current_contract_is_an_ingestion_failure(self):
        records = self.records();records[0]["content_version"] = "4" * 64
        with self.assertRaisesRegex(ValueError, "stale current consumer"):
            compile_current_consumers(records)

    def test_projection_cannot_invent_acceptance_or_bind_another_version(self):
        for change in ("unknown_authority", "wrong_subject"):
            records = self.records()
            for r in records:
                p = r["notices"][1]
                if change == "unknown_authority": p["authority_notice_id"] = "SN-missing"
                else: p["consumer_views"][0]["subject"] = dict(p["consumer_views"][0]["subject"], content_version="5" * 64)
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, "authority|accepted subject"):
                compile_current_consumers(records)

    def test_conflicting_current_contracts_stay_visible_as_failure(self):
        records = self.records();extra = copy.deepcopy(records[0]["notices"][1]);extra["notice_id"] = "SN-conflict"
        extra["consumer_views"][0]["contract"]["units"] = "joules"
        records[0]["notices"].append(extra)
        with self.assertRaisesRegex(ValueError, "conflicting current consumer"):
            compile_current_consumers(records)

    def test_missing_authority_source_or_contract_support_fails(self):
        for field in ("source_refs", "requires"):
            records = self.records()
            for r in records:
                if field == "source_refs": r["notices"][0]["source_refs"] = []
                else: r["notices"][1]["consumer_views"][0]["contract"].pop("requires")
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "source|incomplete"):
                compile_current_consumers(records)


class CurrentAuthorityPipelineTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixture_support.Fixture('runTest');self.fixture.setUp();self.addCleanup(self.fixture.doCleanups)
        self.fixture.compile();self.original = Library(self.fixture.root).resolve('N1')
        self.authority, self.projection = annotations(self.original, self.fixture.source)
        self.fixture.write('agent/SEMANTIC_NOTICES.d/authority.jsonl', encoded(self.authority)+encoded(self.projection))
        self.outputs, self.manifest = self.fixture.compile()

    def test_same_pipeline_updates_packet_catalog_frame_and_search_without_new_identity(self):
        f=self.fixture;lib=Library(f.root);record=lib.resolve('N1');packet=lib.packet(['N1'],max_bytes=100000)['packets'][0]
        self.assertEqual(record['content_version'],self.original['content_version'])
        self.assertEqual(record['contract'],self.original['contract'])
        self.assertEqual(packet['contract'],consumer_contract(record))
        self.assertEqual(packet['current_consumer']['authority_notice'],'SN-standing')
        self.assertNotIn('contract',packet['notices'][1]['consumer_views'][0])
        catalog=json.loads(self.outputs['knowledge/current/catalog.json'])
        self.assertEqual(catalog['records'][0]['acceptance'][0]['status'],'CORRECT_AND_ACCEPTED')
        hit=lib.search('finite',method='content')['results'][0]
        self.assertEqual(hit['contract'],packet['contract']);self.assertEqual(hit['acceptance'][0]['subject']['id'],record['id'])
        self.assertEqual(self.outputs,f.compile()[0])

    def test_actual_adapter_preview_current_capsule_and_original_history_remain_distinct(self):
        f=self.fixture
        for args in [('init','-q'),('add','.'),('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','fixture')]:
            subprocess.run(['git','-C',str(f.root),*args],check=True,capture_output=True)
        a=ResearchAdapter(f.root,page_bytes=1024);found=a.search('N1');hit=found['results'][0]
        self.assertIn('CORRECT_AND_ACCEPTED',json.dumps(hit['metadata']['acceptance']))
        self.assertNotIn('unreviewed',json.dumps(hit['metadata']['operation_preview']))
        current=complete(a,hit['id']);self.assertEqual(current['contract'],consumer_contract(a.library.resolve('N1')))
        self.assertNotIn('source_reported_gaps',current);self.assertIn('historical_source_assessment',current)
        self.assertTrue(current['acceptance']);self.assertEqual(current['review_overlays'],[])
        history=complete(a,current['history']['fetch_id']);self.assertIn('source_derived_unreviewed',json.dumps(history))
        self.assertEqual((f.root/'cards/N1-fixture.txt').read_bytes(),f.body)

    def test_old_layout_keeps_record_navigation_and_new_layout_prefers_compact_current(self):
        a=ResearchAdapter.__new__(ResearchAdapter);a.version='9'*64
        def peers(*args,**kwargs):return {'routes':[dict(provider='U1-provider',consumer='U2-consumer')],
            'consumers':[],'candidates':[]}
        a.library=SimpleNamespace(peers=peers)
        self.assertIn(':record:',a.interface_view('N1')['routes'][0]['provider_fetch_id'])
        a.consumer_view_layout=CURRENT_CONSUMER_LAYOUT
        self.assertIn(':current:',a.interface_view('N1')['routes'][0]['provider_fetch_id'])
        self.assertEqual(consumer_view_layout(self.fixture.root,self.manifest),CURRENT_CONSUMER_LAYOUT)
        self.assertIsNone(consumer_view_layout(self.fixture.root,{'outputs':{}}))
        self.fixture.write('knowledge/current/release.json', encoded({'consumer_view_layout': 'future-unknown'}))
        with self.assertRaisesRegex(ValueError, 'deploy its reviewed reader'):
            consumer_view_layout(self.fixture.root, self.manifest)

if __name__=='__main__':unittest.main()
