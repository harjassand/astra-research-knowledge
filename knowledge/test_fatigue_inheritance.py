"""Guard strength/work, load topology and recovery-clock scope in materials routes."""
import hashlib
import json
import subprocess
import sys
import unittest
from knowledge.model import ROOT
from knowledge.retrieve import Library

UNITS=['U1021-load-capacity-versus-interface-work','U1021-series-seam-inheritance-and-reset',
       'U1021-fast-sacrificial-recovery-clock']
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-fatigue-inheritance'
PROOF='eb4e4fb9392f85b8eb9603dde9692fc410726c015c51c4ea89f4ddfd123d3d00'

class FatigueInheritance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_current_scientific_originals_and_actual_model_passages(self):
        j=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes())
        self.assertEqual(len(j['files']),2)
        self.assertEqual(sum(r['bytes'] for r in j['files']),34130)
        for r in j['files']:
            b=(ROOT/UPDATE/r['path']).read_bytes()
            self.assertEqual(hashlib.sha256(b).hexdigest(),r['sha256'])
            self.assertEqual(len(b),r['bytes'])
            self.assertNotIn('single_handle_renewal',r['path'])
        for identifier,(start,end,passage) in zip(UNITS,[(31,117,'not a measured crack energy-release rate'),
                                                       (135,235,'deeper attachment has not been demonstrated'),
                                                       (237,279,'not measured hydrogen-bond recovery rates')]):
            r=self.library.source(identifier,0)
            self.assertEqual(r['source']['sha256'],PROOF)
            self.assertEqual(r['source']['lines'],[start,end])
            self.assertIn(passage,r['text'])

    def test_reset_and_recovery_code_routes_are_the_actual_functions(self):
        seam=self.library.source(UNITS[1],1)
        self.assertEqual(seam['source']['lines'],[117,132])
        self.assertIn('def segmented_exposures',seam['text'])
        self.assertIn('len(blocks)',seam['text'])
        self.assertIn('NEW, unacquired physical direct-host connection',seam['text'])
        rec=self.library.source(UNITS[2],1)
        self.assertEqual(rec['source']['lines'],[163,180])
        self.assertIn('def reversible_dissipation_fraction',rec['text'])
        self.assertIn('def minimal_recovery_for_post_damage',rec['text'])

    def test_scoped_acceptance_keeps_traction_topology_and_clock_limits(self):
        for identifier in ['N1021',*UNITS]:
            r=self.library.resolve(identifier)
            review=next(v for v in r['review_overlays'] if v['id']=='A1035-interface-work-fatigue')
            self.assertIn({'id':r['id'],'content_version':r['content_version']},review['subjects'])
            self.assertIn('without execution',review['scope'])
            self.assertEqual(review['physical_measurement'],'not established')
        self.assertIn('does not bound actual n',self.library.resolve(UNITS[0])['statement'])
        self.assertIn('including initial block establishment',self.library.resolve(UNITS[1])['statement'])
        self.assertIn('R>1-p is impossible',self.library.resolve(UNITS[2])['statement'])
        self.assertIn('does not certify the startup cycles',self.library.resolve(UNITS[2])['body'])

    def test_actual_default_packets_keep_complete_boundaries_within_wire_limit(self):
        for identifier in ['N1021',*UNITS]:
            p=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',identifier],cwd=ROOT,capture_output=True)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertLessEqual(len(p.stdout),32768)
            self.assertIn(b'A1035-interface-work-fatigue',p.stdout)

if __name__=='__main__':unittest.main()
