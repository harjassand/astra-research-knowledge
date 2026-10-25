"""Keep elastic sign, physical-interface classes and their actual sources aligned."""
import hashlib
import json
import subprocess
import sys
import unittest
from knowledge.model import ROOT
from knowledge.retrieve import Library

UNITS=['U1022-linear-mechanical-comparator','U1022-nutrient-closure-and-precursor-stock','U1022-mechanical-observation-limits']
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-mechanical-comparator'
COPY='78741cf723ec770f71614421a780f657c758b48d6ae76c2ff69c9c0da5e06109'
CODE='fe38ea36fc1ab07f4d4388c76251e34befd75e26674f3c06a4a50aa628161d6b'

class MechanicalComparator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_actual_equilibrium_sources_preserve_finite_probe_coupling(self):
        source=self.library.source(UNITS[0],0)
        self.assertEqual(source['source']['sha256'],COPY)
        self.assertEqual(source['source']['lines'],[25,53])
        self.assertIn('cb-ad',source['text'])
        self.assertIn('zero load',source['text'])
        coupled=self.library.source(UNITS[0],2)
        self.assertEqual(coupled['source']['sha256'],CODE)
        self.assertEqual(coupled['source']['lines'],[90,154])
        self.assertIn('[-k1,-k2,c+d+k1+k2]',coupled['text'])
        self.assertIn('Calibrate both mechanical reference ratios together',coupled['text'])

    def test_completion_source_distinguishes_instantaneous_and_delayed_models(self):
        source=self.library.source(UNITS[1],0)
        self.assertEqual(source['source']['lines'],[55,94])
        self.assertIn('instantaneous biological response',source['text'])
        self.assertIn('minimum nutrient supply',source['text'])
        code=self.library.source(UNITS[1],2)
        self.assertIn('dd=eta*',code['text'])
        record=self.library.resolve(UNITS[1])
        self.assertIn('positive tolerance',record['body'])
        self.assertIn('not the delayed-stock model',record['body'])
        self.assertIn('d(t*)+eta*z(t*)',record['statement'])

    def test_observation_alias_does_not_claim_absolute_or_force_control_certificate(self):
        source=self.library.source(UNITS[2],0)
        self.assertEqual(source['source']['sha256'],COPY)
        self.assertEqual(source['source']['lines'],[258,306])
        self.assertIn('Under prescribed displacement',source['text'])
        self.assertIn('reference itself deteriorates',source['text'])
        record=self.library.resolve(UNITS[2])
        self.assertIn('Include the sensing spring',record['body'])
        self.assertIn('not asserted under fixed force',record['body'])
        self.assertIn('equal priors',record['statement'])
        self.assertIn('partial-action',record['contract']['assumptions'][1])

    def test_staged_feed_handoff_requires_actual_coupled_calibration(self):
        transfer=self.library.bridge(*UNITS[:2])['transfers'][0]
        self.assertEqual(transfer['state'],'ESTABLISHED COMPATIBLE INTERFACE')
        for endpoint in ['from','to']:
            self.assertEqual(transfer[endpoint+'_version'],self.library.resolve(transfer[endpoint])['content_version'])
        self.assertIn('joint positive calibration',transfer['scope'])
        self.assertIn('noiseless comparator signs',transfer['scope'])
        self.assertIn('above any excitation threshold',transfer['scope'])
        self.assertIn('not duplicated independent single-probe',transfer['scope'])
        ref=transfer['evidence'][1]
        self.assertEqual(ref['sha256'],CODE)
        text='\n'.join((ROOT/ref['path']).read_text().splitlines()[ref['lines'][0]-1:ref['lines'][1]])
        self.assertIn('q=q_hi if hgap>0 else (q_lo if fgap>0 else 0.)',text)
        self.assertIn('delta>0 and abs(delta)>minimum_signal',text)

    def test_frozen_assets_and_actual_packets_keep_scoped_acceptance(self):
        index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']),2)
        self.assertEqual(sum(r['bytes'] for r in index['files']),47827)
        for row in index['files']:
            self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])
        for identifier in ['N1022',*UNITS]:
            record=self.library.resolve(identifier)
            expected='A1039-mechanofluidic-bounds' if identifier=='N1022' else 'A1038-mechanical-comparator'
            review=next(r for r in record['review_overlays'] if r['id']==expected)
            self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects'])
            self.assertEqual(review['decision'],'accepted_internally_verified')
            self.assertEqual(review['working_device'],'not established')
            self.assertIn('No scientific code',review['scope'])
            result=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',identifier],cwd=ROOT,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertLessEqual(len(result.stdout),32768)

if __name__=='__main__':unittest.main()
