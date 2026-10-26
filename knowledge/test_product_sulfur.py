"""Check source/model interfaces without executing producer chemistry programs."""
import ast
from fractions import Fraction as Q
import hashlib,json,subprocess,sys,textwrap,unittest
from knowledge.model import ROOT
from knowledge.retrieve import Library

UNITS=['U1025-retained-product-diversion','U1025-reversible-mask-irreversible-trap','U1025-postcapture-chemical-discrimination','U1025-product-state-route-crossover']
OLD='U1024-idempotent-retry-ceiling'
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-product-sulfur-state'
PROOF='931c75f83edfedb558eab01198a9c24a1610c60a1477b58337b507c68ce49a16'

class ProductSulfur(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_trial_loss_and_eventual_odds_are_distinct(self):
        source=self.library.source(UNITS[0],0)
        self.assertEqual(source['source']['sha256'],PROOF)
        self.assertEqual(source['source']['lines'],[14,42])
        self.assertIn('equivalent donors',source['text'])
        code=self.library.source(UNITS[0],2)
        self.assertEqual(code['source']['lines'],[23,50])
        self.assertIn('R.lam',code['text'])
        self.assertIn('def stage_correct_eventually',code['text'])
        # One exact first-step calculation, not a producer parameter sweep.
        k,w,jb,r,x,h=map(Q,[2,1,8,5,1,1]);g=r+x+h
        trials=[]
        for loss in [Q(0),Q(3)]:
            d=k+w+loss+jb*(x+h)/g
            correct,wrong,lost=k/d,(w+jb*x/g)/d,(loss+jb*h/g)/d
            self.assertEqual(correct+wrong+lost,1)
            self.assertEqual(correct/(correct+wrong),Q(14,29))
            trials.append(correct)
        self.assertNotEqual(*trials)
        self.assertIn('not waiting time',self.library.resolve(UNITS[0])['body'])

    def test_detours_do_not_become_permanent_errors(self):
        record=self.library.resolve(UNITS[0])
        self.assertIn('w=x=h=0,r>0',record['contract']['requires'][2])
        self.assertIn('x=0 removes',record['body'])
        self.assertIn('not permanent wrong products',record['body'])
        self.assertEqual(Q(1,2)*3*(3-1)/2,Q(3,2))
        source=self.library.source(UNITS[0],0)
        self.assertIn('Counts do not directly establish permanent wrong products',source['text'])

    def test_mask_is_transient_survival_with_actual_initial_state(self):
        source=self.library.source(UNITS[1],1)
        self.assertEqual(source['source']['lines'],[52,61])
        self.assertIn('initial=np.array([b/(a+b),a/(a+b)])',source['text'])
        self.assertIn('initial@expm(Q*t)',source['text'])
        a,b,c=map(Q,[100,1,2]);pi=[b/(a+b),a/(a+b)]
        row_sums=[(-a-c)+a,b-b]
        self.assertEqual(sum(p*s for p,s in zip(pi,row_sums)),-Q(2,101))
        record=self.library.resolve(UNITS[1])
        self.assertIn('independent site evolutions',record['contract']['requires'][1])
        self.assertIn('not survival accumulated',record['body'])

    def test_actual_chemical_renewal_not_dna_dissociation(self):
        source=self.library.source(UNITS[2],1)
        self.assertEqual(source['source']['lines'],[147,163])
        tree=ast.parse(textwrap.dedent(source['text']))
        fn=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef))
        self.assertEqual([n.arg for n in fn.args.args],['alpha_c','alpha_w','cc','rc','cw','rw'])
        ac,aw,cc,rc,cw,rw=map(Q,[2,1,1,1,1,1]);A=ac*cc/(cc+rc);B=aw*cw/(cw+rw)
        self.assertEqual(B/A,aw/ac)
        self.assertEqual(A/(A+B),Q(2,3))
        self.assertEqual((1+ac/(cc+rc)+aw/(cw+rw))/(A+B),Q(5,3))
        self.assertIn('time in both precursors',self.library.resolve(UNITS[2])['body'])
        self.assertIn('alpha_C>0,c_C>0',self.library.resolve(UNITS[2])['contract']['requires'][0])

    def test_constant_retry_interface_is_not_acquired_from_consumed_nitrogen(self):
        bridge=self.library.bridge(OLD,UNITS[0])['transfers'][0]
        self.assertEqual(bridge['state'],'INCOMPATIBLE ASSUMPTIONS')
        for endpoint in ['from','to']:
            self.assertEqual(bridge[endpoint+'_version'],self.library.resolve(bridge[endpoint])['content_version'])
        self.assertIn('b*x>0',bridge['scope'])
        self.assertIn('does not refute U1024',bridge['scope'])
        self.assertTrue(any(r['id']=='A1042-cooperative-footprints' for r in self.library.resolve(OLD)['review_overlays']))
        self.assertEqual(self.library.resolve('U1024-guide-release-feedback-set')['version'],2)

    def test_route_comparison_preserves_the_required_end_product(self):
        # Exact finite probability witness, not the source482 threshold replay.
        retained=Q(1)/(1*2*3);quiet=Q(2,3)**3
        self.assertLess(Q(2,3),Q(1))
        self.assertGreater(quiet,retained)
        record=self.library.resolve(UNITS[3])
        self.assertIn('same acceptable functional output class',record['contract']['requires'][1])
        self.assertIn('native amide',record['body'])
        self.assertIn('not equal-resource performance',record['contract']['costs'][0])
        source=self.library.source(UNITS[3],0)
        self.assertEqual(source['source']['lines'],[46,54])
        self.assertIn('log(1+ρ_cap)',source['text'])

    def test_originals_acceptance_and_default_publication_packets(self):
        index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']),3)
        self.assertEqual(sum(r['bytes'] for r in index['files']),35837)
        for row in index['files']:
            self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])
        for identifier in ['N1025',*UNITS]:
            record=self.library.resolve(identifier)
            review=next(r for r in record['review_overlays'] if r['id']=='A1044-product-sulfur-state')
            self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects'])
            self.assertEqual(review['decision'],'accepted_internally_verified')
            self.assertEqual(review['physical_measurement'],'not established')
            self.assertIn('No producer scientific program',review['scope'])
        for args in [('packet',i) for i in ['N1025',*UNITS,OLD,'N1024']]+[('bridge',OLD,UNITS[0])]:
            result=subprocess.run([sys.executable,'knowledge/retrieve.py',*args],cwd=ROOT,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertLessEqual(len(result.stdout),32768)

if __name__=='__main__':unittest.main()
