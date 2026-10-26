"""Guard whole-memory/coarse-record contracts without replaying producer programs."""
from fractions import Fraction as Q
import hashlib,json,subprocess,sys,unittest
from knowledge.model import ROOT
from knowledge.retrieve import Library

UNITS=['U1023-private-input-role-seal','U1023-complete-coarse-instrument-equivalence','U1023-positive-use-effect-mismatch','U1023-fine-record-and-terminal-failures']
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-quantum-role-sealing'
PROOF='cde7f192676b414f607ea020d8b45c6bb6702b773c2cbef267a9b76e00b4899f'

class RoleSealing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_correlated_role_input_and_one_bit_witness(self):
        source=self.library.source(UNITS[0],0)
        self.assertEqual(source['source']['sha256'],PROOF)
        self.assertEqual(source['source']['lines'],[19,56])
        self.assertIn('all** future-accessible',source['text'])
        record=self.library.resolve(UNITS[0])
        self.assertIn('entire initial DME state',record['contract']['requires'][0])
        self.assertIn('classical random-unitary',record['body'])
        # Exact Bell-sector witness, not a source simulation or hardware check.
        one_bit=[Q(1,2),Q(1,2),Q(0),Q(0)];uniform=[Q(1,4)]*4
        distance=sum(abs(a-b) for a,b in zip(one_bit,uniform))/2
        self.assertEqual(distance,Q(1,2));self.assertEqual((1+distance)/2,Q(3,4))
        self.assertIn('role-guess success3/4',record['statement'])

    def test_complete_instrument_route_is_not_an_effect_only_or_bath_only_check(self):
        coarse=self.library.source(UNITS[1],1)
        self.assertEqual(coarse['source']['lines'],[41,80])
        self.assertTrue(coarse['source']['path'].endswith('ebit_vs_encrypted_instrument.py'))
        self.assertIn('return pas,fail',coarse['text'])
        self.assertIn('def ebit_test',coarse['text'])
        whole=self.library.source(UNITS[1],2)
        self.assertEqual(whole['source']['lines'],[26,83])
        self.assertTrue(whole['source']['path'].endswith('ebit_complete_teleport_reference.py'))
        self.assertIn('def ind5(d,t,c,m,e)',whole['text'])
        self.assertIn('for j in range(8)',whole['text'])
        record=self.library.resolve(UNITS[1])
        self.assertIn('not just failure probabilities',record['statement'])
        self.assertIn('not through histories retaining',record['body'])

    def test_effect_allowance_requires_actual_positive_use(self):
        source=self.library.source(UNITS[2],0)
        self.assertEqual(source['source']['sha256'],PROOF)
        self.assertEqual(source['source']['lines'],[109,152])
        self.assertIn('fictional latent count',source['text'])
        record=self.library.resolve(UNITS[2])
        self.assertIn('one fixed z>1',record['contract']['requires'][1])
        self.assertIn('Coherent/bias leakage in USE',record['contract']['assumptions'][1])
        # One exact scalar coefficient check of the displayed operator algebra.
        p=Q(1,2);nu=Q(2,3);z=Q(6,5);eps=Q(1,10)
        a=1-(1-p)*(z-1)/(p*nu)
        self.assertEqual((1-p)*(z-1)-p*nu*(1-a),0)
        self.assertEqual(1+p*(1-a)*eps,Q(203,200))

    def test_fine_flags_and_terminal_failure_have_actual_governing_passage(self):
        source=self.library.source(UNITS[3],0)
        self.assertEqual(source['source']['lines'],[188,196])
        self.assertIn('flagged',source['text'])
        self.assertIn('unverified logical',source['text'])
        code=self.library.source(UNITS[3],1)
        self.assertEqual(code['source']['lines'],[11,45])
        self.assertIn("'fine_result':lab",code['text'])
        self.assertIn('Last untrusted output X',code['text'])
        self.assertIn('correlated copy',self.library.resolve(UNITS[3])['contract']['assumptions'][1])

    def test_documented_effect_handoff_and_no_automatic_physical_boundary_import(self):
        transfer=self.library.bridge(UNITS[1],UNITS[2])['transfers'][0]
        self.assertEqual(transfer['state'],'ESTABLISHED COMPATIBLE INTERFACE')
        for endpoint in ['from','to']:
            self.assertEqual(transfer[endpoint+'_version'],self.library.resolve(transfer[endpoint])['content_version'])
        self.assertIn('f=epsilon=0,nu=2/3',transfer['scope'])
        self.assertIn('positive virtual-fault',transfer['scope'])
        self.assertEqual(self.library.bridge('N1004',UNITS[0])['state'],'NO SUPPORTED CONNECTION')

    def test_frozen_assets_scoped_acceptance_and_actual_default_packets(self):
        index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']),16)
        self.assertEqual(sum(r['bytes'] for r in index['files']),75941)
        for row in index['files']:
            self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])
        for identifier in ['N1023',*UNITS]:
            record=self.library.resolve(identifier)
            review=next(r for r in record['review_overlays'] if r['id']=='A1041-quantum-role-sealing')
            self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects'])
            self.assertEqual(review['decision'],'accepted_internally_verified')
            self.assertEqual(review['working_device'],'not established')
            self.assertIn('No source scientific code',review['scope'])
            result=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',identifier],cwd=ROOT,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertLessEqual(len(result.stdout),32768)
        result=subprocess.run([sys.executable,'knowledge/retrieve.py','bridge',UNITS[1],UNITS[2]],cwd=ROOT,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr);self.assertLessEqual(len(result.stdout),32768)

if __name__=='__main__':unittest.main()
