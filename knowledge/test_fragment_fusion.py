"""Protect chemical observable, rebuild/size, port and coding interfaces."""
from fractions import Fraction as Q
from itertools import combinations,permutations
from functools import lru_cache
import hashlib,json,math,subprocess,sys,unittest
from knowledge.model import ROOT,Inputs
from knowledge.retrieve import Library
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-fragment-fusion'
SOURCE=ROOT/UPDATE/'source/xh1'
UNITS=['U1029-fragment-rebuild-cost-and-purity','U1029-odd-fragment-storage-parity','U1029-two-click-bridge-selectivity','U1029-unfinished-clock-clean-completion','U1029-position-address-code-scope']
NOTICE='SN-N1029-FUSION-COST-CONVENTIONS-20261026'
NOTE_HASH='3dfb2ee2b3fac65ec9a66505d804427cb4db06adc2c5534c7e3588ba36fbf3bd'

class FragmentFusion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_connection_does_not_identify_junction(self):
        def retained(edges):
            seen={'root'}
            while True:
                more=seen|{v for u,v in edges if u in seen}|{u for u,v in edges if v in seen}
                if more==seen:return 'donor_handle'in seen
                seen=more
        base=[('root','fragment'),('fragment','right_site'),('fragment','wrong_site'),('donor','donor_handle')]
        self.assertFalse(retained(base))
        self.assertTrue(retained(base+[('right_site','donor')]))
        self.assertTrue(retained(base+[('wrong_site','donor')]))
        # Same persistent connectivity outcome in the correct and wrong graph.
        text=self.library.source(UNITS[0],0)['text']
        self.assertIn('WRONG covalent bond',text);self.assertIn('known fragment orientation',text)

    def test_rebuild_material_purity_and_size_conventions(self):
        q=Q(1,2);C=Q(1)
        for _ in range(3):C=2*C/q
        self.assertEqual(C,64) # eight leaves, q=.5: material L^2.
        p,f=Q(9,10),Q(1,100000);q=p+f;C=Q(1)
        for _ in range(10):C=2*C/q
        self.assertAlmostEqual(float(C),2936.4770,places=3)
        purity=(p/q)**1023;self.assertAlmostEqual(float(purity),.98869775,places=8)
        self.assertLess(purity,1);self.assertNotEqual(C,C/purity)
        L=8;products=[2,4,8];children=[1,2,4]
        self.assertEqual(sum(products),2*(L-1));self.assertEqual(sum(children),L-1)
        record=self.library.resolve(UNITS[0]);self.assertIn('TOTAL NEW PRODUCT',record['body'])
        self.assertIn('exp(kappa*(L-1))',record['body'])
        self.assertIn('verified-correct',record['contract']['assumptions'][0])
        self.assertIn('expected consumed resource',record['statement'])
        self.assertIn('unbounded retry support',record['statement'])
        self.assertEqual(record['version'],2)
        current=json.loads((ROOT/'knowledge/units'/UNITS[0]/'v0002.json').read_bytes())
        self.assertEqual(current['previous'],hashlib.sha256((ROOT/'knowledge/units'/UNITS[0]/'v0001.json').read_bytes()).hexdigest())
        self.assertTrue(any(n['notice_id']==NOTICE for n in record['notices']))
        source=self.library.source(UNITS[0],2)
        self.assertEqual(source['source']['lines'],[147,156]);self.assertIn('n=2',source['text']);self.assertIn('n*=2',source['text'])

    def test_ordered_tree_optimization_has_protocol_independent_boundaries(self):
        q=[Q(1,2),Q(3,4),Q(2,3)];c=Q(1,4)
        @lru_cache(None)
        def trees(i,j):
            if i==j:return (i,)
            return tuple((left,right,k)for k in range(i,j)for left in trees(i,k)for right in trees(k+1,j))
        def price(t):return Q(1)if isinstance(t,int)else(price(t[0])+price(t[1])+c)/q[t[2]]
        all_cost=[price(t)for t in trees(0,3)];self.assertEqual(len(all_cost),5)
        dp={(i,i):Q(1)for i in range(4)}
        for width in range(2,5):
            for i in range(5-width):
                j=i+width-1;dp[i,j]=min((dp[i,k]+dp[k+1,j]+c)/q[k]for k in range(i,j))
        self.assertEqual(dp[0,3],min(all_cost))
        self.assertIn('boundary q/c unchanged by subprotocol',self.library.resolve(UNITS[0])['contract']['requires'][1])

    def test_odd_storage_and_four_port_counterconstruction(self):
        for n in range(1,16):
            word=('AB'*n)[:n];self.assertEqual(word[0]==word[-1],n%2==1)
        left,right='ABA','ABABA';out=left+'B'+right
        self.assertTrue(all(a!=b for a,b in zip(out,out[1:])));self.assertEqual(out[0],out[-1]);self.assertEqual(len(out)%2,1)
        ports=['Li','Lo','Ri','Ro'];pairs=list(combinations(ports,2));correct={'Li','Ri'};rings=[{'Li','Lo'},{'Ri','Ro'}]
        counts=[sum(set(x)==correct for x in pairs),sum(set(x)in rings for x in pairs)]
        self.assertEqual([Q(counts[0],6),Q(counts[1],6),Q(6-sum(counts),6)],[Q(1,6),Q(1,3),Q(1,2)])
        def prob(alpha,eta):return alpha/(alpha+eta)*alpha/(alpha+2*eta)
        self.assertEqual(prob(Q(1),Q(1)),Q(1,6));self.assertEqual(prob(Q(1),Q(0)),1)
        self.assertGreater(prob(Q(28),Q(1)),Q(9,10));self.assertLess(prob(Q(27),Q(1)),Q(9,10))
        bridge=self.library.bridge(UNITS[1],UNITS[2])['transfers'][0];self.assertEqual(bridge['state'],'INCOMPATIBLE ASSUMPTIONS')
        self.assertIn('stationary relative hazards',self.library.resolve(UNITS[2])['contract']['requires'][1])

    def test_correct_pair_is_not_acceptance_rate_or_single_bond(self):
        correct=Q(1,6);wrong=Q(5,6)
        # A nondiscriminating covalent reader may accept all these stable links.
        self.assertEqual(correct+wrong,1);self.assertNotEqual(correct,correct+wrong)
        self.assertNotEqual(Q(9,10),Q(9,10)**2)
        bridge=self.library.bridge(UNITS[2],UNITS[0])['transfers'][0]
        self.assertEqual(bridge['state'],'INCOMPATIBLE ASSUMPTIONS');self.assertIn('reader/rejection law',bridge['scope'])
        self.assertTrue(any(n['notice_id']==NOTICE for n in self.library.resolve(UNITS[2])['notices']))

    def test_independent_clock_bound_excludes_finished_hazards(self):
        a=[Q(2),Q(3)];h=[Q(1,4),Q(1,2)];w01,w10=Q(1,10),Q(1,5)
        exact=(a[0]*a[1]/(a[1]+h[1])+a[1]*a[0]/(a[0]+h[0]))/(sum(a)+sum(h)+w01+w10)
        jensen=math.exp(-float(sum(h[i]/a[i]for i in range(2))+(w01+w10)/sum(a)))
        self.assertLessEqual(jensen,float(exact));self.assertLess(float(exact),1)
        a,h,t=2.,1.,1.;p=1-math.exp(-a*t);mu=1/a-t/math.expm1(a*t)
        deadline=p*math.exp(-h*mu);truth=a/(a+h)*(1-math.exp(-(a+h)*t))
        self.assertLessEqual(deadline,truth)
        record=self.library.resolve(UNITS[3]);self.assertIn('No finished-site hazards',record['contract']['assumptions'][0])
        self.assertIn('ordered',record['contract']['requires'][1])

    def test_complete_address_library_and_original_support(self):
        words=' '.join((SOURCE/'astra_chemistry_position_code1023.txt').read_text().splitlines()[1:]).split()
        self.assertEqual(len(words),1023);self.assertEqual(len(set(words)),1023)
        for word in words:
            self.assertEqual(len(word),10);self.assertLessEqual(set(word),set('ACGT'))
            self.assertIn(sum(c in'CG'for c in word),range(4,7));self.assertTrue(all(word[i:i+3]!=word[i]*3 for i in range(8)))
        self.assertEqual(min(sum(a!=b for a,b in zip(u,v))for u,v in combinations(words,2)),3)
        index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes());self.assertEqual(len(index['files']),6);self.assertEqual(sum(r['bytes']for r in index['files']),49157)
        for row in index['files']:self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])
        missing=UPDATE+'/source/xh1/astra_chemistry_distributed_edge_assembly.py';self.assertFalse((ROOT/missing).exists())
        with self.assertRaisesRegex(ValueError,'INGESTION FAILED: required source bytes missing'):Inputs(ROOT).source(dict(path=missing,sha256='0'*64,lines=[1,1]))
        self.assertIn('not a free chemical reader',self.library.resolve(UNITS[4])['contract']['costs'][0])

    def test_versions_default_commands_and_actual_proof_ranges(self):
        for identifier in ['N1029',*UNITS]:
            record=self.library.resolve(identifier);review=next(r for r in record['review_overlays']if r['id']==('A1049-fragment-fusion-expectation'if identifier in ['N1029',UNITS[0]]else'A1048-fragment-fusion'))
            self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects']);self.assertEqual(review['decision'],'accepted_internally_verified');self.assertEqual(review['working_device'],'not established')
        for a,b in [(1,2),(2,0)]:
            bridge=self.library.bridge(UNITS[a],UNITS[b])['transfers'][0]
            for k in ['from','to']:self.assertEqual(bridge[k+'_version'],self.library.resolve(bridge[k])['content_version'])
        for ident,i,lines,phrase in [(UNITS[0],1,[30,46],'p_v+f_v'),(UNITS[1],0,[48,53],'completed'),(UNITS[2],1,[55,61],'not a prediction'),(UNITS[3],0,[12,28],'ordered wrong pair')]:
            v=self.library.source(ident,i);self.assertEqual(v['source']['sha256'],NOTE_HASH);self.assertEqual(v['source']['lines'],lines);self.assertIn(phrase,v['text'])
        for args in [('packet',i)for i in ['N1029',*UNITS]]+[('bridge',UNITS[a],UNITS[b])for a,b in [(1,2),(2,0)]]:
            p=subprocess.run([sys.executable,'knowledge/retrieve.py',*args],cwd=ROOT,capture_output=True);self.assertEqual(p.returncode,0,p.stderr);self.assertLessEqual(len(p.stdout),32768)

if __name__=='__main__':unittest.main()
