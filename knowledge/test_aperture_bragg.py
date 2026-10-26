"""Protect rank/geometry/scattering boundaries and exact branch resource scope."""
from fractions import Fraction as Q
import hashlib,json,math,subprocess,sys,unittest
from knowledge.model import ROOT,Inputs
from knowledge.retrieve import Library
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-aperture-bragg'
UNITS=['U1030-static-aperture-rank-bound','U1030-radiation-gram-variation','U1030-bragg-dark-photon-port','U1030-reciprocal-band-slope-obstruction','U1030-cavity-inclusive-error-budget']
OLD='U1027-reciprocal-parity-band-certificate'
NOTICE='SN-N1030-NUMERICAL-SUPPORT-GAP-20261026'
PROOF='267b30c7d36258f9e0bd3f004a4ad556190d78fe74d8d3cb80ab185707ac18cd'
class ApertureBragg(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_finite_fourier_covariance_and_static_rank(self):
        # Exact dyadic DFT4 outer products; centering only rephases each vector.
        cols=[[(1j**(j*k))/2 for j in range(4)]for k in range(4)]
        C=[[sum(u[j]*u[l].conjugate()for u in cols)/4 for l in range(4)]for j in range(4)]
        self.assertEqual(C,[[Q(1,4)if j==l else 0 for l in range(4)]for j in range(4)])
        required=(1-Q(1,10000))*4
        self.assertGreater(required,3);self.assertLess(required,4)
        self.assertEqual(Q(4-3,4),Q(1,4)) # coordinate rank3 has uniform residual^2=1/4.
        record=self.library.resolve(UNITS[0]);self.assertIn('one fixed',record['contract']['requires'][0])
        self.assertIn('not physical emitters or passive poles',record['body'])

    def test_average_capture_is_not_uniform_sufficiency(self):
        # DFT2 covariance I/2: every rank1 subspace optimizes average. The span
        # of (1,1) loses the odd normalized phase vector completely at q=pi.
        average_error2=Q(1,2);epsilon=Q(4,5)
        self.assertLess(average_error2,epsilon**2);self.assertGreater(Q(1),epsilon**2)
        self.assertEqual(sum((Q(j)-Q(3,2))**2 for j in range(4))/4,Q(4*4-1,12))
        record=self.library.resolve(UNITS[0]);self.assertIn('AVERAGE',record['body']);self.assertIn('M>=2',record['contract']['requires'][1])

    def test_angular_variation_requires_normalization_and_true_inputs(self):
        integral=lambda power:Q(2,power+1)if power%2==0 else Q(0)
        self.assertEqual(Q(3,8)*(integral(0)+integral(2)),1)
        self.assertEqual(Q(3,8)*(integral(2)+integral(4)),Q(2,5))
        # ||P u||^2>=1-delta^2 is positive only for delta<1.
        delta=Q(1,10);self.assertEqual(1-delta**2,Q(99,100))
        record=self.library.resolve(UNITS[1]);self.assertIn('delta<1',record['contract']['requires'][0])
        self.assertIn('centered',record['body'])
        self.assertIn('not available outward intervals',record['body'])
        bridge=self.library.bridge(UNITS[1],UNITS[2])['transfers'][0];self.assertEqual(bridge['state'],'INCOMPATIBLE ASSUMPTIONS')

    def test_bragg_null_input_is_unchanged_for_any_internal_response(self):
        W=[[Q(1),Q(1)],[Q(-1),Q(-1)],[Q(1),Q(1)]];phi=[Q(1),Q(-1)]
        self.assertEqual([sum(row[j]*phi[j]for j in range(2))for row in W],[0,0,0])
        # W phi=0 kills every Wdagger R W correction, including extra modes.
        correction=[Q(0),Q(0)];output=[phi[j]-correction[j]for j in range(2)]
        self.assertEqual(sum((output[j]+phi[j])**2 for j in range(2))/sum(p*p for p in phi),4)
        self.assertNotEqual([sum(row)for row in W],[0,0,0]) # even input can couple.
        record=self.library.resolve(UNITS[2]);self.assertIn('relative',record['contract']['requires'][1]);self.assertIn('different operation',record['contract']['assumptions'][0])

    def test_old_away_from_bragg_certificate_is_not_reused(self):
        bridge=self.library.bridge(UNITS[2],OLD)['transfers'][0]
        self.assertEqual(bridge['state'],'INCOMPATIBLE ASSUMPTIONS')
        self.assertIn('both parity radiation halfwidths bounded positive',bridge['scope'])
        self.assertIn('tau=1.1',self.library.resolve(OLD)['contract']['requires'][0])
        self.assertGreater(1-abs(math.cos(1.65)),0);self.assertEqual(1-abs(math.cos(math.pi)),0)
        source=self.library.source(OLD,1);self.assertIn('a_p(E)>5.7491',source['text'])

    def test_reciprocal_band_zero_slope_and_conditional_bypass(self):
        # At q0=pi/2, sin q0=1; v=2 gives exact algebraic value/slope matching.
        v,J,E0=Q(2),Q(-1,4),Q(3,2);bare=E0
        self.assertEqual(-2*J*v,1);self.assertGreater(bare-2*abs(J),0)
        self.assertAlmostEqual(math.cos(math.pi+.2),math.cos(math.pi-.2))
        record=self.library.resolve(UNITS[3]);self.assertIn('nondegenerate',record['contract']['requires'][0])
        self.assertIn('separately checked positive-band',record['contract']['requires'][1]);self.assertIn('not a global impossibility theorem',record['body'])

    def test_cavity_full_output_and_separate_branch_thresholds(self):
        eta=Q(1,100);kappa,loss=Q(39999),Q(1);r=(loss-kappa)/(loss+kappa)
        full=2*(1+r);self.assertEqual(full,eta**2)
        self.assertLess((r+1)**2,full) # reflected amplitude alone discards loss.
        C=Q(39999);r_coupled=1-2/(1+C);self.assertEqual(2*(1-r_coupled),eta**2)
        d=Q(1,20);err2=lambda k:16*d*d/(k*k+4*d*d)
        self.assertLess(err2(Q(20)),eta**2);self.assertGreater(err2(Q(19)),eta**2)
        record=self.library.resolve(UNITS[4]);self.assertIn('lambda=0',record['body']);self.assertIn('strict inequalities',record['body'])
        self.assertIn('not joint sufficient',record['contract']['assumptions'][1])

    def test_support_versions_actual_sources_and_default_routes(self):
        index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes());self.assertEqual(len(index['files']),2);self.assertEqual(sum(r['bytes']for r in index['files']),30500)
        for row in index['files']:self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])
        missing=UPDATE+'/source/p2/astra_collective_aperture_modal_theorem_20261026.py'
        with self.assertRaisesRegex(ValueError,'INGESTION FAILED: required source bytes missing'):Inputs(ROOT).source(dict(path=missing,sha256='0'*64,lines=[1,1]))
        checks=[(0,0,[13,61],'not minimize worst-case'),(1,0,[179,221],'not outward-rounded'),(2,0,[63,80],'S_total(ω0)φ=φ'),(3,0,[82,111],"E_int'(π)=0"),(4,0,[157,175],'λ=0')]
        for i,n,lines,phrase in checks:
            v=self.library.source(UNITS[i],n);self.assertEqual(v['source']['sha256'],PROOF);self.assertEqual(v['source']['lines'],lines);self.assertIn(phrase,v['text'])
        for identifier in ['N1030',*UNITS]:
            record=self.library.resolve(identifier);review=next(r for r in record['review_overlays']if r['id']=='A1050-aperture-bragg')
            self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects']);self.assertEqual(review['decision'],'accepted_internally_verified');self.assertEqual(review['working_device'],'not established')
            self.assertTrue(any(n['notice_id']==NOTICE and not n['whole_claim_invalidated']for n in record['notices']))
        for a,b in [(UNITS[1],UNITS[2]),(UNITS[2],OLD)]:
            t=self.library.bridge(a,b)['transfers'][0]
            for endpoint in ['from','to']:self.assertEqual(t[endpoint+'_version'],self.library.resolve(t[endpoint])['content_version'])
        for args in [('packet',i)for i in ['N1030',*UNITS,OLD]]+[('bridge',UNITS[1],UNITS[2]),('bridge',UNITS[2],OLD)]:
            p=subprocess.run([sys.executable,'knowledge/retrieve.py',*args],cwd=ROOT,capture_output=True);self.assertEqual(p.returncode,0,p.stderr);self.assertLessEqual(len(p.stdout),32768)

if __name__=='__main__':unittest.main()
