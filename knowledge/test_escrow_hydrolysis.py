"""Protect the full model, actual source mapping and recovery-time convention."""
import csv
import hashlib
import json
import subprocess
import sys
import unittest
from knowledge.model import ROOT
from knowledge.retrieve import Library

UNITS=['U1020-hydrolysis-protection-and-selectivity','U1020-damaged-donor-replacement']
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-escrow-hydrolysis'
NOTE='0c0dfd0cf3c235ca5af4add9e93e6fa1a2aa1f3ff41871938eb13a33dfa4137a'

class EscrowHydrolysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_full_model_source_retains_active_root_loss(self):
        result=self.library.source(UNITS[0],0)
        self.assertEqual(result['source']['sha256'],NOTE)
        self.assertEqual(result['source']['lines'],[13,48])
        self.assertIn('DA=k+wA+hA+dA+e+r',result['text'])
        self.assertIn('instantaneous replenishment',result['text'])
        record=self.library.resolve(UNITS[0])
        self.assertIn('DA=k+wA+hA+dA+e+r',record['statement'])
        self.assertIn('shorter response omits',record['body'])
        self.assertIn('fixed rates',record['contract']['assumptions'][1])

    def test_recovery_support_preserves_conditional_time_charge(self):
        result=self.library.source(UNITS[1],0)
        self.assertEqual(result['source']['sha256'],NOTE)
        self.assertEqual(result['source']['lines'],[50,71])
        self.assertIn('each successful recovery',result['text'])
        self.assertIn('H*(1-delta)*tau',result['text'])
        record=self.library.resolve(UNITS[1])
        self.assertIn('only on successful nonterminal recovery',record['statement'])
        self.assertIn('no general monotone mean-time improvement when delta>0',record['body'])
        self.assertIn('terminal damage has no separately supplied delay',record['contract']['requires'][1])

    def test_frozen_assets_do_not_substitute_for_missing_code(self):
        index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']),3)
        self.assertEqual(sum(row['bytes'] for row in index['files']),43522)
        for row in index['files']:
            raw=(ROOT/UPDATE/row['path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
            self.assertFalse(row['path'].endswith('.py'))
        with (ROOT/UPDATE/'source/xh1/originals/astra_256_escorts_16nt_20261026.csv').open() as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),256)
        self.assertEqual(list(rows[0]),['donor_id','pna4_payload','dna_escort_5to3','template_address_5to3','GC_count'])

    def test_explicit_model_handoff_preserves_outcome_and_time_classes(self):
        link=self.library.bridge(*UNITS)['transfers'][0]
        self.assertEqual(link['state'],'ESTABLISHED COMPATIBLE INTERFACE')
        for endpoint in ['from','to']:
            self.assertEqual(link[endpoint+'_version'],self.library.resolve(link[endpoint])['content_version'])
        self.assertIn('Droot as terminal root destruction',link['scope'])
        self.assertIn('time tau on successful nonterminal recovery',link['scope'])
        ref=link['evidence'][1]
        self.assertEqual(ref['lines'],[50,64])
        text='\n'.join((ROOT/ref['path']).read_text().splitlines()[49:64])
        self.assertIn('above per-donor probabilities',text)
        self.assertIn('H*(1-delta)*tau',text)

    def test_actual_packets_bind_current_scoped_acceptance_and_fit(self):
        for identifier in ['N1020',*UNITS]:
            record=self.library.resolve(identifier)
            review=next(r for r in record['review_overlays'] if r['id']=='A1037-escrow-hydrolysis')
            self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects'])
            self.assertEqual(review['decision'],'accepted_internally_verified')
            self.assertEqual(review['working_device'],'not established')
            self.assertIn('unavailable',review['scope'])
            process=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',identifier],cwd=ROOT,capture_output=True)
            self.assertEqual(process.returncode,0,process.stderr)
            self.assertLessEqual(len(process.stdout),32768)
            self.assertIn(b'A1037-escrow-hydrolysis',process.stdout)

if __name__=='__main__':unittest.main()
