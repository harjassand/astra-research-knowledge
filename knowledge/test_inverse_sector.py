"""Protect exact inverse/outer/VI scope and verify acquired rational witnesses."""
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt
from pathlib import Path
import hashlib,json,subprocess,sys,unittest,zipfile
from knowledge.model import ROOT
from knowledge.retrieve import Library
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-inverse-sector'
PACKAGE=ROOT/UPDATE/'source/p3/package'
UNITS=['U1028-inverse-residual-consistency','U1028-sparse-weighted-ball-certificate','U1028-saturation-noise-and-contract-limits','U1028-constrained-projected-equilibrium']
NOTE_HASH='a55753090404201b78a4cacd7718b8a2a337ae867ef0160fdca58ebc3762a303'
def vec(x):return tuple(map(Q,x))
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
def mul(t,x):return tuple(t*a for a in x)
def dot(x,y):return sum((a*b for a,b in zip(x,y)),Q(0))
def sq(x):return dot(x,x)
def load(name):return json.loads((PACKAGE/name).read_bytes())
def ceil_root(v,bits=40):
    scale=1<<bits;n=v.numerator*scale*scale;d=v.denominator;k=isqrt(n//d)
    if k*k*d<n:k+=1
    return Q(k,scale)
def focused_witnesses():
    """No producer code import/execution; recompute saved endpoints from pairs."""
    j=load('astra_pro3_sector_joint_results.json');s=load('astra_pro3_sparse_inverse_certificate_results.json')
    inverse=j['inverse_native_transfer'];p=vec(inverse['target_force']);history=[((Q(0),Q(0)),(Q(0),Q(0)))]+[(vec(r['probe']),vec(r['response']))for r in inverse['iteration']]
    for (x,f),(y,g) in combinations(history,2):assert sq(sub(sub(f,g),mul(Q(3),sub(x,y))))<=sq(sub(x,y))
    cs=[add(x,mul(Q(3,8),sub(p,f)))for x,f in history];rs=[Q(1,64)*sq(sub(p,f))for x,f in history]
    count=0
    for row in s['focused_tasks']:
        direction=vec(row['direction']);cert=row['certificate']
        for key,sign in [('upper_certificate',1),('lower_certificate',-1)]:
            c=cert[key];idx=c['selected'];weights=vec(c['weights']);assert len(idx)==len(weights)<=2 and all(w>=0 for w in weights)and sum(weights)==1
            center=tuple(sum(w*cs[i][k]for i,w in zip(idx,weights))for k in range(2))
            radius2=sum(w*(rs[i]-sq(sub(cs[i],center)))for i,w in zip(idx,weights));assert radius2>=0
            v=mul(Q(sign),direction);upper=dot(v,center)+ceil_root(sq(v)*radius2)
            assert center==vec(c['ball_center'])and radius2==Q(c['ball_radius_squared'])and upper==Q(c['upper'])
            assert c['upper_sqrt_outward_precision_bits']==40
            assert Q(cert['upper'if sign==1 else'lower'])==(upper if sign==1 else-upper)
            assert dot(v,vec(inverse['source_aware_true_equilibrium']))<=upper
            count+=1
    return count

class InverseSector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_completed_square_inverse_equivalence(self):
        m,a=Q(3),Q(1);D=m*m-a*a;c,b=m/D,a/D
        h,d=vec(['7/3','-2/5']),vec(['1/2','1/3'])
        self.assertEqual(D*(sq(sub(d,mul(c,h)))-b*b*sq(h)),sq(sub(h,mul(m,d)))-a*a*sq(d))
        self.assertEqual((c,b),(Q(3,8),Q(1,8)))
        self.assertIn('specific shifted',self.library.resolve('N1028')['contract']['requires'])
        self.assertIn('not every',self.library.resolve(UNITS[0])['contract']['assumptions'][0].lower())

    def test_same_source_future_constraints_are_essential(self):
        p1,p2=vec([2,0]),vec([2,'1/50']);c,b=Q(3,8),Q(1,8)
        relative=mul(c,sub(p2,p1));r=b*Q(1,50)
        self.assertEqual((relative[1]-r,relative[1]+r),(Q(1,200),Q(1,100)))
        self.assertEqual(Q(1)/(2*r),200)
        z1=add(mul(c,p1),vec([0,'1/4']));z2=add(mul(c,p2),vec([0,'-1/4']))
        for p,z in [(p1,z1),(p2,z2)]:self.assertLessEqual(sq(sub(z,mul(c,p))),b*b*sq(p))
        self.assertGreater(sq(sub(sub(z2,z1),mul(c,sub(p2,p1)))),b*b*sq(sub(p2,p1)))
        for slope,endpoint in [(Q(4),Q(1,200)),(Q(2),Q(1,100))]:
            self.assertEqual(Q(1,50)/slope,endpoint)
        bridge=self.library.bridge(UNITS[0],UNITS[1])['transfers'][0]
        self.assertEqual(bridge['state'],'ESTABLISHED COMPATIBLE INTERFACE')

    def test_saved_focused_outer_witnesses_and_bit_scope(self):
        self.assertEqual(focused_witnesses(),8)
        j=load('astra_pro3_sector_joint_results.json');s=load('astra_pro3_sparse_inverse_certificate_results.json')
        self.assertEqual(max(r['max_certificate_bits']for r in s['spatial_bank_tasks']),103)
        self.assertEqual(max(c['max_integer_bits']for r in s['focused_tasks']for c in [r['certificate']['upper_certificate'],r['certificate']['lower_certificate']]),326)
        self.assertEqual(Q(j['inverse_native_transfer']['final_certified_radius']).denominator.bit_length(),582)
        record=self.library.resolve(UNITS[1])
        self.assertIn('nonempty',record['contract']['requires'][0]);self.assertIn('Nonempty interior',record['contract']['requires'][1])
        self.assertIn('582 bits',record['body']);self.assertIn('may be loose',record['contract']['assumptions'][1])

    def test_saturation_noise_and_global_contract_are_different(self):
        for eps in [Q(0),Q(1,100),Q(1,10**8),Q(2)]:
            s=2+eps;center=1-Q(3,8)*s;r=s/8
            self.assertEqual(r*r-center*center,eps*(2-eps)/8)
        e=Q(1,10**8);self.assertGreater(e*(2-e)/8,Q(1,25000)**2)
        rows=load('astra_pro3_sector_saturation_results.json')['controls']
        for row in rows:
            eps=Q(row['epsilon']);self.assertEqual(Q(row['joint_equilibrium_squared_radius']),eps*(2-eps)/8)
            self.assertLessEqual(Q(row['joint_y_radius_lower'])**2,eps*(2-eps)/8)
            self.assertGreaterEqual(Q(row['joint_y_radius_upper'])**2,eps*(2-eps)/8)
        eps=Q(1,1000);m=Q(3);p=Q(1)
        plus,minus=(p-eps)/m,(p+eps)/m
        self.assertEqual(minus-plus,2*eps/m)
        bump=lambda x:max(Q(0),Q(1,4)-(x-10)**2)**4
        f=lambda x:3*x-1000*bump(x)
        self.assertTrue(all(f(x)==3*x for x in map(Q,[-1,0,1])))
        self.assertLess(f(Q(244,25))-f(Q(39,4)),0)
        record=self.library.resolve(UNITS[2]);self.assertIn('not an iid',record['body']);self.assertIn('not exact correlated-noise',record['body'])

    def test_projecting_an_inverse_need_not_solve_vi(self):
        # F=3I+J has shifted residual Lip1; C is the two-dose simplex.
        F=lambda x:(3*x[0]-x[1],x[0]+3*x[1]);p=vec([2,1])
        inverse=vec(['7/10','1/10']);self.assertEqual(F(inverse),p)
        projected=vec(['4/5','1/5']);solution=vec(['5/6','1/6'])
        self.assertLess(dot(sub(F(projected),p),sub(vec([1,0]),projected)),0)
        for z in [vec([1,0]),vec([0,1])]:self.assertEqual(dot(sub(F(solution),p),sub(z,solution)),0)
        self.assertNotEqual(F(solution),p)
        bridge=self.library.bridge(UNITS[0],UNITS[3])['transfers'][0]
        self.assertEqual(bridge['state'],'INCOMPATIBLE ASSUMPTIONS')
        self.assertIn('outer only',self.library.resolve(UNITS[3])['contract']['assumptions'][0])
        self.assertIn('R_next<=(a/m)*R+delta_round',self.library.resolve(UNITS[3])['body'])

    def test_recorded_query_costs_and_equal_information_limit(self):
        j=load('astra_pro3_sector_joint_results.json');v=load('astra_pro3_sector_constrained_vi_results.json')
        self.assertEqual(j['inverse_native_transfer']['native_calls'],6);self.assertEqual(j['inverse_native_transfer']['returned_scalars'],12)
        self.assertEqual(j['cyclic_violation']['probe_count'],32);self.assertEqual(j['unforeseen_batch']['independent_setter_forward_calls'],50)
        self.assertEqual(v['total_native_calls'],24);self.assertEqual(v['independent_reference_source_aware_forward_calls'],4)
        self.assertEqual(v['cyclic_monotonicity_falsification']['native_cycle_calls'],64)
        self.assertEqual(sum(r['baseline_calls']for r in v['tasks']),20)
        for r in v['tasks']:
            a,b=r['solver'],r['same_budget_domain_only_baseline']
            self.assertEqual(a['final_estimate'],b['final_estimate']);self.assertEqual(a['actual_error_squared'],b['actual_error_squared'])
            self.assertEqual(r['new_native_calls'],5)
            for step in a['path']:
                x=vec(step['probe']);self.assertEqual(sum(x),1);self.assertTrue(all(t>=0 for t in x))
        self.assertFalse(v['tasks'][1]['target_is_native_inverse']);self.assertFalse(v['tasks'][2]['target_is_native_inverse'])

    def test_raw_archive_manifest_and_decisive_source_routes(self):
        index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes());self.assertEqual(len(index['files']),13);self.assertEqual(sum(r['bytes']for r in index['files']),179395)
        for row in index['files']:self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])
        manifest=load('astra_pro3_inverse_sector_manifest.json')
        for name,row in manifest['files'].items():self.assertEqual(hashlib.sha256((PACKAGE/name).read_bytes()).hexdigest(),row['sha256'])
        with zipfile.ZipFile(ROOT/UPDATE/'source/p3/ASTRA_PRO3_INVERSE_SECTOR_RESEARCH.zip')as archive:
            self.assertIsNone(archive.testzip())
            for entry in archive.infolist():
                self.assertFalse(Path(entry.filename).is_absolute());self.assertNotIn('..',Path(entry.filename).parts)
                if not entry.is_dir():self.assertEqual(archive.read(entry),(PACKAGE/Path(entry.filename).name).read_bytes())
        for identifier,n,lines,phrase in [(UNITS[0],0,[9,79],'every pair of old or future'),(UNITS[1],1,[83,110],'nonempty interior'),(UNITS[2],1,[114,147],'not an exact description'),(UNITS[3],0,[175,221],'not** the exact joint inverse')]:
            v=self.library.source(identifier,n);self.assertEqual(v['source']['sha256'],NOTE_HASH);self.assertEqual(v['source']['lines'],lines);self.assertIn(phrase,v['text'])

    def test_versioned_acceptance_and_actual_default_commands(self):
        for identifier in ['N1028',*UNITS]:
            record=self.library.resolve(identifier);review=next(r for r in record['review_overlays']if r['id']=='A1047-inverse-sector')
            self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects']);self.assertEqual(review['decision'],'accepted_internally_verified');self.assertEqual(review['working_device'],'not established')
        for a,b in [(0,1),(0,3)]:
            bridge=self.library.bridge(UNITS[a],UNITS[b])['transfers'][0]
            for k in ['from','to']:self.assertEqual(bridge[k+'_version'],self.library.resolve(bridge[k])['content_version'])
        for args in [('packet',i)for i in ['N1028',*UNITS]]+[('bridge',UNITS[a],UNITS[b])for a,b in [(0,1),(0,3)]]:
            p=subprocess.run([sys.executable,'knowledge/retrieve.py',*args],cwd=ROOT,capture_output=True);self.assertEqual(p.returncode,0,p.stderr);self.assertLessEqual(len(p.stdout),32768)

if __name__=='__main__':unittest.main()
