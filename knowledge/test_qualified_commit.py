"""Keep actual chemical observation classes and missing-code scope in retrieval."""
import hashlib
import json
import subprocess
import sys
import unittest
from knowledge.model import ROOT
from knowledge.retrieve import Library

UNITS=['U1020-postbond-purity-versus-root-yield','U1020-donor-owned-checkpoint-and-chemical-leak',
       'U1020-wrong-site-receipt-information-bound','U1020-clearance-register-and-joint-budget']
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-qualified-chemical-commit'
PROOF='0a621e3ac32610b3d75e4c70fdd405c8ccfd8ba092b31e7261a53c1cf2977a48'

class QualifiedCommit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_source_windows_follow_actual_distinct_models(self):
        index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']),2)
        self.assertEqual(sum(r['bytes'] for r in index['files']),41268)
        for row in index['files']:
            raw=(ROOT/UPDATE/row['path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),row['sha256'])
            self.assertFalse(row['path'].endswith('.py'))
        for identifier,(start,end,decisive) in zip(UNITS,[(13,27,'G = p*A_C'),(29,58,'q_i(n)'),
                                                        (116,128,'TV(P_C, P_W)'),(130,148,'not wrong stable rooted product')]):
            result=self.library.source(identifier,0)
            self.assertEqual(result['source']['sha256'],PROOF)
            self.assertEqual(result['source']['lines'],[start,end])
            self.assertIn(decisive,result['text'])

    def test_negative_transfer_cannot_silently_acquire_wrong_bond_clearance(self):
        link=self.library.bridge(UNITS[2],UNITS[3])['transfers'][0]
        self.assertEqual(link['state'],'INCOMPATIBLE ASSUMPTIONS')
        for endpoint in ['from','to']:
            self.assertEqual(link[endpoint+'_version'],self.library.resolve(link[endpoint])['content_version'])
        self.assertIn('stable wrong-site covalent product',link['scope'])
        self.assertIn('UNJOINED donor',link['scope'])
        self.assertIn('same departing nuisance class',link['scope'])
        ref=link['evidence'][0]
        self.assertEqual(ref['lines'],[116,136])
        text='\n'.join((ROOT/ref['path']).read_text().splitlines()[115:136])
        self.assertIn('for that latter comparison wash signatures may be identical',text)

    def test_acceptance_does_not_promote_missing_numeric_implementations(self):
        for identifier in ['N1020',*UNITS]:
            record=self.library.resolve(identifier)
            review=next(r for r in record['review_overlays'] if r['id']=='A1034-qualified-chemical-commit')
            self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects'])
            self.assertIn('unavailable',review['scope'])
            self.assertEqual(review['physical_measurement'],'not established')
        self.assertIn('complete joint record',self.library.resolve(UNITS[2])['body'])
        self.assertIn('controller-declared',self.library.resolve(UNITS[0])['statement'])
        self.assertIn('Two99% factors give98.01%',self.library.resolve(UNITS[3])['body'])

    def test_actual_default_packets_fit_without_removing_boundaries(self):
        for identifier in ['N1020',*UNITS]:
            result=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',identifier],cwd=ROOT,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertLessEqual(len(result.stdout),32768)
            self.assertIn(b'A1034-qualified-chemical-commit',result.stdout)

if __name__=='__main__':unittest.main()
