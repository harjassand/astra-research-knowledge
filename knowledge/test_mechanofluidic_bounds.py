"""Guard actual port state/force interfaces; no producer suite or device replay."""
from fractions import Fraction as F
import hashlib,json,subprocess,sys,unittest
from knowledge.model import ROOT
from knowledge.retrieve import Library

ENERGY='U1022-prepared-port-and-spring-energy'
FORCE='U1022-pressure-force-placement'
OLD=['U1022-linear-mechanical-comparator','U1022-nutrient-closure-and-precursor-stock','U1022-mechanical-observation-limits']
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-mechanofluidic-bounds'
CODE='e8bf26219e752ef78d7b5829a913ef5951f40e6159fa1dca66b9cddeea4bba97'

class MechanofluidicBounds(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_stationary_energy_is_not_free_work_from_relaxed_state(self):
        source=self.library.source(ENERGY,0)
        self.assertEqual(source['source']['sha256'],CODE)
        self.assertEqual(source['source']['lines'],[29,42])
        self.assertIn('available_energy=delta0*delta0/(2*R)',source['text'])
        record=self.library.resolve(ENERGY)
        self.assertIn('constrained delta=0 state',record['statement'])
        self.assertIn('already relaxed at delta0',record['statement'])
        self.assertIn('if delta0=0 every k stores zero',record['body'])
        self.assertIn('paid preparation/loading/reset',record['contract']['requires'][1])

    def test_source_force_wording_conflict_is_visible(self):
        source=self.library.source(FORCE,1)
        self.assertEqual(source['source']['sha256'],CODE)
        self.assertEqual(source['source']['lines'],[151,171])
        self.assertIn('to one bridge midpoint',source['text'])
        self.assertIn("xx['R']*Fbias",source['text'])
        self.assertIn('abs(biased_readout(d,Fb',source['text'])
        record=self.library.resolve(FORCE)
        self.assertIn('Equal-and-opposite closing forces',record['statement'])
        self.assertIn('only the test midpoint',record['statement'])
        self.assertIn('zero reference force',record['contract']['requires'][1])

    def test_force_placement_counterexample_against_direct_balance(self):
        # One exact finite counterexample from force balance, not the source code.
        # K0=Delta=1,k=1/2,Fb=1/10; ref receives Fr, test receives -Ft.
        def gap(d,Fr,Ft):
            k=F(1,2);A=2+k;B=1+d+k;det=A*B-k*k
            reference=(B*(1+Fr)+k*(1-Ft))/det
            test=(k*(1+Fr)+A*(1-Ft))/det
            return test-reference
        self.assertEqual(gap(F(7,11),F(1,10),F(1,10)),0)
        self.assertNotEqual(gap(F(7,11),0,F(1,10)),0)
        self.assertEqual(gap(F(4,5),0,F(1,10)),0)
        self.assertNotEqual(gap(F(4,5),F(1,10),F(1,10)),0)
        self.assertIn('d=1-2*Fb/(K0*Delta)',self.library.resolve(FORCE)['statement'])

    def test_notice_and_version_bound_acceptance_keep_earlier_scope(self):
        for identifier in ['N1022',ENERGY,FORCE,*OLD]:
            record=self.library.resolve(identifier)
            expected='A1040-growth-overview-continuity' if identifier=='N1022' else ('A1038-mechanical-comparator' if identifier in OLD else 'A1039-mechanofluidic-bounds')
            review=next(r for r in record['review_overlays'] if r['id']==expected)
            self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects'])
            self.assertEqual(review['working_device'],'not established')
            notice=next(n for n in record['notices'] if n.get('notice_id')=='SN-U1022-PORT-AND-FORCE-SCOPE-20261026')
            self.assertFalse(notice['whole_claim_invalidated'])
            self.assertEqual(set(notice['affected_units']),{ENERGY,FORCE})
            self.assertIn('earlier A1038 units remain valid',notice['clarification'])

    def test_original_bytes_and_actual_default_packets(self):
        index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']),2)
        self.assertEqual(sum(r['bytes'] for r in index['files']),40565)
        for row in index['files']:
            self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])
        for identifier in ['N1022',ENERGY,FORCE,*OLD]:
            r=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',identifier],cwd=ROOT,capture_output=True)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertLessEqual(len(r.stdout),32768)

    def test_existing_delayed_maturation_remains_retrievable_after_intake(self):
        # Prior exposed research-use context, not a held-out benchmark.
        query='Growth overshoots even after feedstock switched off. What state must the controller track?'
        results=self.library.search(query,method='lexical')['results']
        supported={'N1022-mechanical-comparator-and-growth-interface','U1022-nutrient-closure-and-precursor-stock'}
        self.assertTrue(supported.intersection(row['id'] for row in results))

if __name__=='__main__':unittest.main()
