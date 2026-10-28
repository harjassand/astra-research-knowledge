"""Snapshot-selected source layouts retain real passages and correction routes."""
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

from knowledge.mcp_adapter import (ResearchAdapter, source_context_layout,
    INLINE_SOURCE_CONTEXT, LINKED_SOURCE_CONTEXT)
from knowledge.model import digest, encoded


class SourceContextLayoutTests(unittest.TestCase):
    def setUp(self):
        self.space=tempfile.TemporaryDirectory()
        self.addCleanup(self.space.cleanup)
        self.root=Path(self.space.name)
        self.text=b'Assume a supplied positive gap.\nA bounded conditional construction.\n'
        (self.root/'proof.txt').write_bytes(self.text)
        self.ref={'path':'proof.txt','sha256':digest(self.text),'lines':[1,2],
                  'quote':'Assume a supplied positive gap.'}
        self.records={}
        for i in range(35):
            name=f'U{i}-synthetic-context'
            # Repeated long source qualifications recreate actual artifact fanout.
            notice={'notice_id':f'SN-{i}','clarification':'Retain the acquired source and calibration assumptions. '*100,
                    'evidence':[self.ref],'conflict_status':'open'if i%2 else'rejected_transfer'}
            self.records[name]={'id':name,'content_version':digest(name.encode()),
                                'notices':[{'inherited_from':'synthetic-parent','notice':notice}]}
        a=self.adapter=ResearchAdapter.__new__(ResearchAdapter)
        a.root,a.paths,a.revision=self.root,{'proof.txt'},'f'*40
        a.version='a'*64
        a.library=SimpleNamespace(records=self.records)
        a.contexts={(self.ref['path'],self.ref['sha256']):set(self.records)}
        a.locators,a.artifact_data={},{}

    def test_only_declared_snapshot_marker_selects_layout_and_unknown_fails(self):
        marker=self.root/'knowledge/current/release.json'
        marker.parent.mkdir(parents=True)
        marker.write_text(json.dumps({'source_context_layout':'unknown-layout'}))
        # An undeclared extra file cannot change an older snapshot's codec.
        self.assertEqual(source_context_layout(self.root,{'outputs':{}}),INLINE_SOURCE_CONTEXT)
        declared={'outputs':{'knowledge/current/release.json':digest(marker.read_bytes())}}
        with self.assertRaisesRegex(ValueError,'Unsupported published source context layout'):
            source_context_layout(self.root,declared)
        marker.write_text('{}')
        declared['outputs']['knowledge/current/release.json']=digest(marker.read_bytes())
        self.assertEqual(source_context_layout(self.root,declared),INLINE_SOURCE_CONTEXT)
        marker.write_text(json.dumps({'source_context_layout':LINKED_SOURCE_CONTEXT}))
        declared['outputs']['knowledge/current/release.json']=digest(marker.read_bytes())
        self.assertEqual(source_context_layout(self.root,declared),LINKED_SOURCE_CONTEXT)

    def test_high_fanout_links_every_exact_current_record_without_blending_notices(self):
        a=self.adapter;a.source_context_layout=INLINE_SOURCE_CONTEXT
        old=a.source_payload(self.ref)
        a.source_context_layout=LINKED_SOURCE_CONTEXT
        new=a.source_payload(self.ref)
        for field in ('source','text','text_selection','citation_locator','full_source_url','extracted_text_lines','scope'):
            self.assertEqual(new[field],old[field])
        self.assertGreater(len(encoded(old)),100000)
        self.assertLess(len(encoded(new)),24000)
        self.assertEqual({r['id']for r in new['current_context']},set(self.records))
        for route in new['current_context']:
            original=self.records[route['id']]
            self.assertEqual(route['content_version'],original['content_version'])
            self.assertEqual(route['notice_count'],len(original['notices']))
            self.assertEqual(route['fetch_id'],a.handle('current',route['id']))
            self.assertNotIn('notices',route)
        self.assertEqual(new['current_context_layout'],LINKED_SOURCE_CONTEXT)
        self.assertIn('every continuation',new['required_context_action'])
        self.assertIn('not a claim-specific proof or acceptance transfer',new['current_context_scope'])

    def test_legacy_source_shape_and_complete_inline_notices_remain_exact(self):
        a=self.adapter;a.source_context_layout=INLINE_SOURCE_CONTEXT
        expected={'scope':'Exact declared source version. Current context notices remain applicable to reuse; coarchive and citation do not confer acceptance. A historical unit document retains its historical status and does not inherit the current review.',
            'source':self.ref,'text_selection':'unchanged_utf8','text':self.text.decode(),
            'citation_locator':a.source_locator(self.ref),'full_source_url':a.source_url(self.ref),
            'extracted_text_lines':[1,2],
            'current_context':[{'id':r['id'],'content_version':r['content_version'],
                'notices':r['notices'],'fetch_id':a.handle('record',r['id'])}
                for _,r in sorted(self.records.items())]}
        self.assertEqual(encoded(a.source_payload(self.ref)),encoded(expected))

    def test_binary_artifact_keeps_its_boundary_and_current_correction_route(self):
        a=self.adapter;a.source_context_layout=LINKED_SOURCE_CONTEXT
        raw=b'\xff\x00binary fixture';(self.root/'binary.dat').write_bytes(raw)
        a.paths.add('binary.dat')
        ref={'path':'binary.dat','sha256':digest(raw),'lines':None}
        a.contexts[(ref['path'],ref['sha256'])]={'U0-synthetic-context'}
        value=a.source_payload(ref)
        self.assertNotIn('text',value)
        self.assertIn('Binary original only',value['scope'])
        self.assertEqual(value['source'],ref)
        self.assertEqual(value['current_context'][0]['fetch_id'],a.handle('current','U0-synthetic-context'))
        self.assertIn('Before reusing',value['required_context_action'])


if __name__=='__main__':unittest.main()
