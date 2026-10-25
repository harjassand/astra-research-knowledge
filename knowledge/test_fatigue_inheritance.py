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
            expected='A1036-periodic-seam-correction' if identifier in ['N1021',UNITS[1]] else 'A1035-interface-work-fatigue'
            review=next(v for v in r['review_overlays'] if v['id']==expected)
            self.assertIn({'id':r['id'],'content_version':r['content_version']},review['subjects'])
            self.assertIn('without execution' if expected.startswith('A1035') else 'No original scientific script',review['scope'])
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
            packet=json.loads(p.stdout)['packets'][0]
            expected='A1036-periodic-seam-correction' if identifier in ['N1021',UNITS[1]] else 'A1035-interface-work-fatigue'
            self.assertTrue(any(v['id']==expected for v in packet['review_overlays']))

    def test_periodic_reset_contract_counts_and_excluded_partition(self):
        record=self.library.resolve(UNITS[1])
        self.assertEqual(record['statement'],record['contract']['provides'][0])
        # Check the scheduling restriction in every exposed contract location.
        for text in [record['statement'],*record['contract']['provides'],' '.join(record['contract']['requires'])]:
            self.assertIn('periodic',text.lower())
            self.assertIn('ONLY',text)
            self.assertIn('m_j=k for j<q',text)
            self.assertIn('m_q=n-k*(q-1)',text)
            self.assertIn('1<=k<=n',text)
            self.assertIn('Arbitrary partitions with blocks at most k are outside this contract',text)
        # Arithmetic oracle for the narrowed schedule, not a new partition model.
        def periodic(n,k):
            self.assertTrue(isinstance(n,int) and isinstance(k,int) and 1<=k<=n)
            q=(n+k-1)//k
            blocks=(k,)*(q-1)+(n-k*(q-1),)
            return blocks,q,sum(m*(m+1)//2 for m in blocks)
        self.assertEqual(periodic(6,3),((3,3),2,12))
        self.assertEqual(periodic(7,3),((3,3,1),3,13))
        for n in range(1,8):
            self.assertEqual(periodic(n,1),((1,)*n,n,n))
            self.assertEqual(periodic(n,n),((n,),1,n*(n+1)//2))
        excluded=(3,2,1)
        self.assertEqual(sum(excluded),6)
        self.assertTrue(all(m<=3 for m in excluded))  # v1 admitted this wrong schedule.
        self.assertNotEqual(excluded,periodic(6,3)[0])
        self.assertNotEqual(len(excluded),periodic(6,3)[1])
        self.assertIn('outside the periodic contract',record['body'])
        self.assertIn('including initial block establishment',record['statement'])
        self.assertIn('not the exact finite-n optimum',record['body'])

    def test_periodic_successor_rejection_and_notice_propagate(self):
        unit=self.library.resolve(UNITS[1])
        old_path=ROOT/f'knowledge/units/{UNITS[1]}/v0001.json'
        old=old_path.read_bytes()
        self.assertEqual(hashlib.sha256(old).hexdigest(),'dbfc1cebc5d92db25763fd7e73aece1e94c6a46560260d40bb6b673574d87906')
        self.assertEqual(hashlib.sha256((ROOT/'knowledge/reviews/A1035-interface-work-fatigue.json').read_bytes()).hexdigest(),
                         '884b5efe3116db143f30ec59f631e38b11160b40b6394d6c144a2017231c412d')
        successor=json.loads((ROOT/f'knowledge/units/{UNITS[1]}/v0002.json').read_bytes())
        self.assertEqual(successor['previous'],hashlib.sha256(old).hexdigest())
        self.assertEqual(unit['version'],2)
        self.assertEqual([r['version'] for r in unit['history']],[1,2])
        self.assertTrue(unit['authority'].endswith('v0002.json'))
        self.assertIn('partition n repairs into blocks m_j<=k',json.loads(old)['statement'])
        rejected=next(r for r in unit['historical_reviews'] if r['id']=='A1036-v1-schedule-rejection')
        self.assertEqual(rejected['decision'],'rejected')
        self.assertIn('HISTORICAL VERSION ONLY',rejected['applicability'])
        self.assertTrue(any(r['id']=='A1035-interface-work-fatigue' for r in unit['historical_reviews']))
        for identifier in ['N1021',*UNITS]:
            record=self.library.resolve(identifier)
            notice=next(v for v in record['notices'] if v.get('notice_id')=='SN-U1021-PERIODIC-RESET-20261026')
            self.assertFalse(notice['whole_claim_invalidated'])
            self.assertTrue(notice['replacement_authority'].endswith('v0002.json'))
            self.assertIn('has3 and is excluded',notice['clarification'])
        bridge=self.library.bridge('N1017','N1021')
        self.assertEqual(bridge['state'],'NO SUPPORTED CONNECTION')
        self.assertTrue(any(v.get('notice_id')=='SN-U1021-PERIODIC-RESET-20261026' for v in bridge['notices']))

if __name__=='__main__':unittest.main()
