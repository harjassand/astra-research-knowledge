"""Protect analytic/control classes and absent numeric support, without science replay."""
from fractions import Fraction as Q
import hashlib,json,subprocess,sys,unittest
from knowledge.model import ROOT,Inputs
from knowledge.retrieve import Library

UNITS=['U1026-passive-matrix-jet-compiler','U1026-positive-scalar-moment-obstruction','U1026-energy-form-and-charge-memory','U1026-delay-kernel-static-retuning-limit']
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-passive-matrix-pole'
PROOF='32a8d5fc657d6b0ce4a779adbaa0f3922e204a6a2413a0f1b879a1b2b1b732a7'
NOTICE='SN-N1026-NUMERIC-CERTIFICATE-SUPPORT-GAP-20261026'

class PassiveMatrixPole(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.library=Library()

    def test_local_jet_compiler_and_passivity_conditions(self):
        source=self.library.source(UNITS[0],1)
        self.assertEqual(source['source']['sha256'],PROOF)
        self.assertEqual(source['source']['lines'],[63,137])
        self.assertIn('non-scalar',source['text'])
        # Exact coefficient witness, not the tau3.7 interval calculation.
        tau,dx,eta,F0,F1,F2=map(Q,[2,1,1,1,3,2])
        abar=eta*(F2+tau*tau*F0)*dx**3/2
        h0=-F0+abar/(eta*dx);h1=-F1/tau+abar/(eta*tau*dx**2)
        self.assertEqual(eta*(F0+h0)-abar/dx,0)
        self.assertEqual(eta*(F1+tau*h1)-abar/dx**2,0)
        self.assertEqual(eta*(F2-tau*tau*h0)-abar*(2/dx**3-tau*tau/dx),0)
        K1,K2,ds=map(Q,[-4,-2,1]);gamma=1/(-K1+ds*K2/2);r=-gamma*K2*ds**3/2
        self.assertGreater(gamma,0);self.assertGreater(r,0)
        self.assertEqual(1+gamma*K1+r/ds**2,0)
        self.assertEqual(gamma*K2+2*r/ds**3,0)
        record=self.library.resolve(UNITS[0])
        self.assertIn('abar>0,gamma>0,r>0',record['contract']['requires'][1])
        self.assertIn('not a numerical continuous-band error bound',record['body'])

    def test_positive_scalar_moments_have_restricted_consequences(self):
        source=self.library.source(UNITS[1],0)
        self.assertEqual(source['source']['lines'],[242,268])
        self.assertIn('Cauchy',source['text'])
        alpha,beta,gamma,L3=map(Q,[1,4,2,-10])
        M2=gamma*alpha-1;M3=gamma*beta/2
        self.assertLess(M2,M3/2) # Outside-upper-band poles cannot realize these moments.
        bound=gamma*L3+3*gamma**2*beta**2/(2*M2)
        self.assertGreater(bound,gamma*(L3+3*beta**2/(2*alpha)))
        self.assertGreater(bound,0)
        record=self.library.resolve(UNITS[1])
        self.assertIn('finite positive residues',record['contract']['requires'][0])
        self.assertIn('B=1',record['contract']['requires'][0])
        self.assertIn('alpha<=B*beta/4',record['contract']['units'])
        self.assertIn('not a universal passive-optics bandwidth theorem',record['body'])

    def test_form_margin_is_not_a_continuum_gap_or_molecule(self):
        source=self.library.source(UNITS[2],1)
        self.assertEqual(source['source']['lines'],[200,240])
        self.assertIn('not* a spectral gap',source['text'])
        record=self.library.resolve(UNITS[2])
        self.assertIn('C>=cI,c>0',record['contract']['requires'][0])
        self.assertIn('not an extra bound eigenstate',record['statement'])
        self.assertIn('single-impurity capacity-two proof',record['body'])
        # A photon normalized on(0,epsilon) has mean energy epsilon/2.
        self.assertLess(Q(1,2**11),Q(1,2**6))
        self.assertIn('arbitrarily near zero energy',record['body'])

    def test_collective_charge_does_not_become_a_heterogeneous_shift(self):
        record=self.library.resolve(UNITS[2])
        self.assertIn('Heterogeneous site-conditioned shifts',record['body'])
        T=[[Q(1),Q(-1)],[Q(-1),Q(1)]];D=[[Q(1),Q(0)],[Q(0),Q(2)]]
        mul=lambda a,b:[[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        td,dt=mul(T,D),mul(D,T)
        self.assertNotEqual(td,dt)
        self.assertEqual([sum(row) for row in T],[0,0])
        self.assertIn('collective charge shift',record['contract']['requires'][1])

    def test_delay_limit_is_entire_kernel_not_frequency_local(self):
        source=self.library.source(UNITS[3],0)
        self.assertEqual(source['source']['lines'],[292,317])
        self.assertIn('entire off-axis self-energy',source['text'])
        self.assertIn('not* a universal no-go',source['text'])
        record=self.library.resolve(UNITS[3])
        self.assertIn('large-z limit',record['body'])
        self.assertIn('only allowed repair',record['contract']['requires'][1])
        self.assertIn('gamma>0,1+eta>0,delta_tau!=0',record['contract']['requires'][0])
        self.assertIn('not a manufacturing tolerance',record['body'])

    def test_missing_numeric_companion_fails_required_source_ingestion(self):
        missing=UPDATE+'/source/p2/astra_rankone_crosspole_interval_certificate_20261026.py'
        self.assertFalse((ROOT/missing).exists())
        with self.assertRaisesRegex(ValueError,'INGESTION FAILED: required source bytes missing'):
            Inputs(ROOT).source(dict(path=missing,sha256='0'*64,lines=[1,1]))
        for identifier in ['N1026',*UNITS]:
            record=self.library.resolve(identifier)
            self.assertTrue(any(n['notice_id']==NOTICE and n['status']=='numeric_certificate_unacquired' for n in record['notices']))
            review=next(r for r in record['review_overlays'] if r['id']=='A1045-passive-matrix-pole')
            self.assertIn('conditional analytic scope',review['scope'])
            self.assertIn('unacquired',review['remaining_gaps'][0])

    def test_scalar_obstruction_cannot_rule_out_matrix_control(self):
        bridge=self.library.bridge(UNITS[1],UNITS[0])['transfers'][0]
        self.assertEqual(bridge['state'],'INCOMPATIBLE ASSUMPTIONS')
        self.assertIn('changes the legal auxiliary class',bridge['scope'])
        for endpoint in ['from','to']:
            self.assertEqual(bridge[endpoint+'_version'],self.library.resolve(bridge[endpoint])['content_version'])

    def test_originals_versioned_acceptance_and_default_packets(self):
        index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes())
        self.assertEqual(len(index['files']),2)
        self.assertEqual(sum(r['bytes'] for r in index['files']),34192)
        for row in index['files']:
            self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])
        for identifier in ['N1026',*UNITS]:
            record=self.library.resolve(identifier)
            review=next(r for r in record['review_overlays'] if r['id']=='A1045-passive-matrix-pole')
            self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects'])
            self.assertEqual(review['decision'],'accepted_internally_verified')
            self.assertEqual(review['working_device'],'not established')
        for args in [('packet',i) for i in ['N1026',*UNITS]]+[('bridge',UNITS[1],UNITS[0])]:
            result=subprocess.run([sys.executable,'knowledge/retrieve.py',*args],cwd=ROOT,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertLessEqual(len(result.stdout),32768)

if __name__=='__main__':unittest.main()
