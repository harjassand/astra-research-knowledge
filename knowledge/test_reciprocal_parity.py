"""Check the acquired bounded certificate and prevent scientifically invalid transfers."""
import ast,contextlib,hashlib,io,json,math,subprocess,sys,tempfile,unittest
from fractions import Fraction as Q
from pathlib import Path
from knowledge.model import ROOT,Inputs
from knowledge.retrieve import Library

UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-reciprocal-parity'
NAME='astra_reciprocal_parity_interval_certificate_20261026'
CODE_HASH='46d3cabf099c693f50a7187e0fe28fe14a702be106806aeedc1d576e8446a8f4'
UNITS=['U1027-reciprocal-parity-band-certificate','U1027-passive-rank-and-inband-pole','U1027-capacity-with-soft-photon-threshold','U1027-independent-radiation-phase-error','U1027-local-side-bus-equivalence']

def replay_certificate():
    """Original proof checker; relocate its sole output path, never edit source bytes."""
    raw=(ROOT/UPDATE/'source/p2'/f'{NAME}.py').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==CODE_HASH
    tree=ast.parse(raw)
    with tempfile.TemporaryDirectory(prefix='astra-rational-certificate-') as scratch:
        target=str(Path(scratch)/(NAME+'.json'));changed=0
        for node in ast.walk(tree):
            if isinstance(node,ast.Constant) and node.value=='/mnt/data/'+NAME+'.json':
                node.value=target;changed+=1
        assert changed==1
        env={'__name__':'__main__'}
        with contextlib.redirect_stdout(io.StringIO()):exec(compile(tree,NAME+'.py','exec'),env)
        return env,json.loads(Path(target).read_bytes())

class ReciprocalParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_rational_checker_output_and_outward_public_bounds(self):
        env,output=replay_certificate()
        self.assertEqual(output,json.loads((ROOT/UPDATE/'source/p2'/f'{NAME}.json').read_bytes()))
        # The source JSON exports nearest floats, not rigorous interval endpoints.
        # Compare original rational upper endpoints to outward public decimals.
        for p in (+1,-1):
            d,r=env['par'][p]['d'],env['par'][p]['r'];w=env['W']
            q=env['gam']*env['M']*w**3/6+r*w**3/(d**3*(d-w))
            self.assertLess((2*q/env['a_min']).hi,Q(9071721,10**9))
            self.assertLess((2*env['a_max']/(env['CHI']-q)).hi,Q(9469018,10**9))
        self.assertLess(env['TAIL'],Q(1814,10**30));self.assertLess(env['M'],Q(415359,1000))
        # Independent alternating rational Machin enclosure for the pi premise.
        def atan(q,n):
            s=sum((-1)**j*q**(2*j+1)/Q(2*j+1) for j in range(n))
            t=(-1)**n*q**(2*n+1)/Q(2*n+1)
            return min(s,s+t),max(s,s+t)
        a,b=atan(Q(1,5),12);c,d=atan(Q(1,239),4)
        self.assertLess(Q(314159,100000),16*a-4*d)
        self.assertLess(16*b-4*c,Q(314160,100000))

    def test_exact_source_passages_and_nontransfer_of_band(self):
        source=self.library.source(UNITS[0],0)
        self.assertEqual(source['source']['lines'],[13,49])
        self.assertIn('V(ω)V(ω)†',source['text'])
        self.assertIn('Both outgoing directions are retained',source['text'])
        proof=self.library.source(UNITS[0],1)
        self.assertIn('0.009071721',proof['text'])
        self.assertIn('asymptotic, stationary',proof['text'])
        record=self.library.resolve(UNITS[0])
        self.assertIn('new certificate',record['body'])
        # Even while parity is fixed, changing theta changes the eigenvalues.
        a,b=math.cos(1.1*1.5),math.cos(1.2*1.5)
        self.assertNotEqual(a,b)

    def test_passive_rank_and_moment_obstruction_has_fixed_family(self):
        env,_=replay_certificate()
        t=env['par'][-1]['t'];u=-env['B'](-1,2)/2
        self.assertGreater((u-2*t).lo,Q(143839,10000))
        # A rank-one update has an exact perpendicular null vector: it cannot
        # equal a positive definite two-direction slope correction.
        g=[Q(2),Q(3)];v=[-g[1],g[0]]
        self.assertEqual(sum(g[i]*v[i] for i in range(2)),0)
        self.assertGreater(sum(v[i]**2 for i in range(2)),0)
        self.assertIn('no other frequency-dependent control',self.library.resolve(UNITS[1])['contract']['requires'][0])

    def test_loss_floor_includes_radiation_and_is_necessary_only(self):
        a,ell=Q(6),Q(1,10000)
        err=lambda x:4*(x+ell*(a+ell))/(x+(a+ell)**2)
        self.assertEqual(err(0),4*ell/(a+ell));self.assertGreater(err(1),err(0))
        # Complete output includes loss; conditioning on surviving guide light
        # would omit this strictly positive term.
        wanted_sq=4*ell**2/(a+ell)**2;loss_sq=4*a*ell/(a+ell)**2
        self.assertEqual(wanted_sq+loss_sq,err(0));self.assertLess(wanted_sq,err(0))
        threshold=(.01**2/(4-.01**2))*(1-abs(math.cos(1.65)))
        self.assertAlmostEqual(threshold,2.302255334366524e-5,places=18)
        self.assertGreater(2*math.sqrt(3e-5/(1-abs(math.cos(1.65))+3e-5)),.01)
        record=self.library.resolve(UNITS[3])
        self.assertIn('necessary only',record['body'])
        source=self.library.source(UNITS[3],0)
        self.assertIn('complete physical output-state',source['text'])
        self.assertIn('not sufficient',source['text'])

    def test_real_bus_identity_and_local_only_resource_cost(self):
        # Exact rational resolvent witness for the general simultaneous-parity
        # algebra, not a new floating sample certificate for source parameters.
        E,op,om,gp,gm=map(Q,[1,4,2,3,1]);o=(op+om)/2;j=(op-om)/2
        gd=(gp+gm)/2;gc=(gp-gm)/2
        mul=lambda a,b:[[sum(a[i][k]*b[k][l] for k in range(2)) for l in range(2)]for i in range(2)]
        den=(o-E)**2-j*j
        inv=[[(o-E)/den,-j/den],[-j/den,(o-E)/den]];G=[[gd,gc],[gc,gd]]
        actual=mul(mul(G,inv),G);rp=gp*gp/(op-E);rm=gm*gm/(om-E)
        self.assertEqual(actual,[[(rp+rm)/2,(rp-rm)/2],[(rp-rm)/2,(rp+rm)/2]])
        self.assertNotEqual(gp*gp,gm*gm)
        record=self.library.resolve(UNITS[4])
        self.assertIn('reflection-symmetric',record['contract']['requires'][1])
        self.assertIn('not all local networks',record['body'])
        bridge=self.library.bridge(UNITS[4],UNITS[0])['transfers'][0]
        self.assertEqual(bridge['state'],'ESTABLISHED COMPATIBLE INTERFACE')

    def test_capacity_is_neither_gap_nor_coherent_operation(self):
        env,_=replay_certificate()
        for p,threshold in [(1,Q(48213,10000)),(-1,Q(37624,10000))]:
            par=env['par'][p]
            exact=par['bare']-4*env['gam']-par['r']/par['Omega']
            self.assertGreater(exact.lo,threshold)
        self.assertGreater(env['a_min'],Q(57491,10000))
        record=self.library.resolve(UNITS[2])
        self.assertIn('soft-photon dissociation',record['statement'])
        self.assertIn('not a global continuum gap',record['body'])
        self.assertIn('[T,K]=0',record['contract']['requires'][1])
        bridge=self.library.bridge(UNITS[0],UNITS[3])['transfers'][0]
        self.assertEqual(bridge['state'],'INCOMPATIBLE ASSUMPTIONS')
        self.assertIn('changes the full output map',bridge['scope'])
        # This different reciprocal model must not erase the old chiral gap.
        old=self.library.resolve('N1026')
        self.assertTrue(any(n['notice_id']=='SN-N1026-NUMERIC-CERTIFICATE-SUPPORT-GAP-20261026' for n in old['notices']))

    def test_missing_companions_stay_missing_and_originals_preserved(self):
        missing=UPDATE+'/source/p2/astra_reciprocal_parity_design_probe_20261026.py'
        self.assertFalse((ROOT/missing).exists())
        with self.assertRaisesRegex(ValueError,'INGESTION FAILED: required source bytes missing'):
            Inputs(ROOT).source(dict(path=missing,sha256='0'*64,lines=[1,1]))
        index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']),8);self.assertEqual(sum(r['bytes']for r in index['files']),51768)
        for row in index['files']:
            self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])

    def test_scoped_versions_bridges_and_actual_default_wire_budget(self):
        for identifier in ['N1027',*UNITS]:
            record=self.library.resolve(identifier)
            review=next(r for r in record['review_overlays']if r['id']=='A1046-reciprocal-parity')
            self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects'])
            self.assertEqual(review['decision'],'accepted_internally_verified')
            self.assertEqual(review['working_device'],'not established')
            self.assertIn('missing-import companion programs',review['scope'])
        for a,b in [(4,0),(0,3)]:
            bridge=self.library.bridge(UNITS[a],UNITS[b])['transfers'][0]
            for key in ['from','to']:
                self.assertEqual(bridge[key+'_version'],self.library.resolve(bridge[key])['content_version'])
        args=[('packet',i)for i in ['N1027',*UNITS]]+[('bridge',UNITS[a],UNITS[b])for a,b in [(4,0),(0,3)]]
        for command in args:
            result=subprocess.run([sys.executable,'knowledge/retrieve.py',*command],cwd=ROOT,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertLessEqual(len(result.stdout),32768)

if __name__=='__main__':unittest.main()
