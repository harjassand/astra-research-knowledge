"""Exact checks of written conditional models, not unavailable producer simulations."""
from fractions import Fraction as F
import hashlib,json,math,subprocess,sys,unittest
from knowledge.model import ROOT,Inputs
from knowledge.retrieve import Library
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-positional-trapping'
IDS=['U1033-positional-hazard-accumulation','U1033-reversible-trap-first-passage']
OLD='U1025-reversible-mask-irreversible-trap'
DIVERSION='U1025-retained-product-diversion'
NOTICE='SN-N1033-MODEL-AND-SUPPORT-SCOPE-20261026'
SHA='9dd438cc71c80446af1d5ae32c64186a727b4f323662171f8c7526ce3dfb2272'
def hazard_model(a,bs):
 B=F(0);survival=F(1);exposure=F(0)
 for b in [F(0),*bs]:
  B+=b;survival*=a/(a+B);exposure+=B/a
 return survival,exposure
def first_step(a,d,b,r,x,t,j):
 if a<=0 or min(d,b,r,x,t,j)<0 or r+x+t==0:raise ValueError('positive correct rate and nondegenerate trapped exit required')
 A=a+d+j*b;B=-j*b;C=-r;D=r+x+t;det=A*D-B*C
 # Exact two-by-two absorbing-probability system, RHS(a,0).
 return a*D/det,-a*C/det
def lossless_time(a,b,r,j):
 if a<=0 or r<=0:raise ValueError('positive escape required for finite lossless renewal mean')
 A=a+j*b;B=-j*b;C=-r;D=r;det=A*D-B*C
 # Exact first-step time system, RHS(1,1).
 return (D-B)/det,(A-C)/det

class PositionalTrapping(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.library=Library()

 def test_finite_exposure_identity_and_probability_product(self):
  for L in range(1,17):
   for alpha in [0,1,2]:
    a=F(7,3);bs=[F(1,11*k**alpha)for k in range(1,L)]
    prob,S=hazard_model(a,bs)
    expected=sum((L-k)*b/a for k,b in enumerate(bs,1));self.assertEqual(S,expected)
    self.assertGreater(prob,0);self.assertLessEqual(prob,1)
    if L>1:self.assertLessEqual(prob,(a/(a+bs[0]))**(L-1))

 def test_exposure_is_not_exact_log_loss(self):
  for L in range(1,12):
   prob,S=hazard_model(F(1),[F(1)]*(L-1));self.assertEqual(prob,F(1,math.factorial(L)));self.assertEqual(S,F(L*(L-1),2))
  # L3: F=1/6, S=3. A finite rational lower bound e^3>=1+3+9/2>6
  # refutes log(1/F)=S without using floating logarithms.
  self.assertGreater(F(1)+3+F(9,2),6)
  self.assertIn('not exact log loss',self.library.resolve(IDS[0])['contract']['assumptions'][0])

 def test_harmonic_and_summable_exposure_bounds(self):
  for L in range(2,20):
   epsilon=F(1,100)
   _,S=hazard_model(F(1),[epsilon/k for k in range(1,L)])
   H=sum(F(1,k)for k in range(1,L));self.assertEqual(S,epsilon*(L*H-(L-1)))
   _,S2=hazard_model(F(1),[epsilon/(k*k)for k in range(1,L)])
   self.assertGreaterEqual(S2,epsilon*(L-1));self.assertLess(S2,2*epsilon*L)

 def test_two_state_absorption_identity(self):
  for j in [0,1,4,11]:
   for d,x,t in [(F(0),F(0),F(0)),(F(1,13),F(1,9),F(1,11)),(F(0),F(2,7),F(0))]:
    a,b,r=F(7,3),F(2,5),F(5,7);pa,pt=first_step(a,d,b,r,x,t,j)
    expected=a/(a+d+j*b*(x+t)/(r+x+t));self.assertEqual(pa,expected)
    # Explicit prior-law reuse, with failure causes coarsened and harmless loss zero.
    k,w,old_x,h=a,d,x+t,F(0)
    self.assertEqual(pa,k/(k+w+j*b*old_x/(r+old_x+h)))
    self.assertEqual((a+d+j*b)*pa-j*b*pt,a);self.assertEqual(-r*pa+(r+x+t)*pt,0)
    self.assertGreater(pa,0);self.assertLessEqual(pa,1)

 def test_lossless_time_and_zero_escape_boundary(self):
  a,b,r=F(2),F(3),F(1)
  for L in [1,2,7,1024]:
   total=sum(lossless_time(a,b,r,j)[0]for j in range(L));self.assertEqual(total,F(L)/a+b*L*(L-1)/(2*a*r))
  self.assertEqual(first_step(a,0,b,r,0,0,1)[0],1)
  with self.assertRaisesRegex(ValueError,'nondegenerate'):first_step(a,0,b,0,0,0,1)
  with self.assertRaisesRegex(ValueError,'positive escape'):lossless_time(a,b,0,1)
  # With zero escape and accessible T, the first trap is permanent: success2/5.
  self.assertEqual(a/(a+b),F(2,5))
  self.assertIn('r_esc>0',self.library.resolve(IDS[1])['contract']['requires'][1])
  self.assertIn('already supplies',self.library.resolve(IDS[1])['body'])

 def test_refuted_capture_import_and_distinct_old_killing_model(self):
  pa,_=first_step(F(2),0,F(3),F(1),0,0,1);naive=F(2,5)
  self.assertEqual(pa,1);self.assertGreater(pa,naive)
  t=self.library.bridge(IDS[1],IDS[0])['transfers'][0];self.assertEqual(t['state'],'REFUTED TRANSFER')
  old=self.library.bridge(IDS[1],OLD)['transfers'][0];self.assertEqual(old['state'],'INCOMPATIBLE ASSUMPTIONS')
  self.assertIn('c_U',old['scope']);self.assertIn('dS_U/dt',self.library.resolve(OLD)['statement'])
  source=self.library.source(OLD,0);self.assertEqual(source['source']['lines'],[56,71]);self.assertIn('irreversibly damaged',source['text'])

 def test_actual_sources_scoped_acceptance_and_missing_original(self):
  index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes());self.assertEqual(len(index['files']),1);row=index['files'][0]
  self.assertEqual(row['bytes'],9473);self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),SHA)
  for identifier,lines,phrase in [(IDS[0],[35,79],'F_L'),(IDS[1],[81,97],'P_j')]:
   source=self.library.source(identifier,0);self.assertEqual(source['source']['sha256'],SHA);self.assertEqual(source['source']['lines'],lines);self.assertIn(phrase,source['text'])
  for identifier in ['N1033',*IDS]:
   record=self.library.resolve(identifier);review=next(x for x in record['review_overlays']if x['id']=='A1053-positional-trapping');self.assertEqual(review['decision'],'accepted_internally_verified');self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects']);self.assertEqual(review['working_device'],'not established')
   self.assertTrue(any(n['notice_id']==NOTICE and not n['whole_claim_invalidated']for n in record['notices']))
  with self.assertRaisesRegex(ValueError,'INGESTION FAILED: required source bytes missing'):
   Inputs(ROOT).source(dict(path=UPDATE+'/source/xh1/unacquired_producer_program.py',sha256='0'*64,lines=[1,1]))

 def test_versions_and_actual_default_routes(self):
  reused=self.library.bridge(DIVERSION,IDS[1])['transfers'][0]
  self.assertEqual(reused['state'],'ESTABLISHED COMPATIBLE INTERFACE')
  for e in ['from','to']:self.assertEqual(reused[e+'_version'],self.library.resolve(reused[e])['content_version'])
  for to in [IDS[0],OLD]:
   t=self.library.bridge(IDS[1],to)['transfers'][0]
   for e in ['from','to']:self.assertEqual(t[e+'_version'],self.library.resolve(t[e])['content_version'])
  for args in [('packet',i)for i in ['N1033',*IDS,OLD,DIVERSION,'N1025']]+[('bridge',IDS[1],i)for i in [IDS[0],OLD]]+[('bridge',DIVERSION,IDS[1])]:
   p=subprocess.run([sys.executable,'knowledge/retrieve.py',*args],cwd=ROOT,capture_output=True);self.assertEqual(p.returncode,0,p.stderr);self.assertLessEqual(len(p.stdout),32768)

if __name__=='__main__':unittest.main()
