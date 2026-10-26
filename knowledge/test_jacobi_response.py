"""Exact finite response witnesses and the intake's consequential transfer boundaries."""
from fractions import Fraction as Q
import hashlib,json,subprocess,sys,unittest
from knowledge.model import ROOT,Inputs
from knowledge.retrieve import Library

UNIT='U1031-real-jacobi-response-compiler'
OLD='U1030-radiation-gram-variation'
UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-jacobi-response'
SHA='44e7479df516667ca020bb26bbe7e371d8d5f1c24e6a7192916c3ffb4d0a55c6'
NOTICE='SN-N1031-UNACQUIRED-SCATTERING-DATA-20261026'
def c(a,b=0):return Q(a),Q(b)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def scale(r,a):return r*a[0],r*a[1]
def real(a,b):return a[0]*b[0]+a[1]*b[1]
def imag(a,b):return a[0]*b[1]-a[1]*b[0]
def action(diag,hops,y):
 return [add(add(scale(diag[j],y[j]),scale(hops[j-1],y[j-1])if j else c(0)),scale(hops[j],y[j+1])if j+1<len(y)else c(0))for j in range(len(y))]
def reconstruct(y,z):
 """Independent exact row-current audit, not a public numerical/physical solver."""
 if len(y)<2 or len(y)!=len(z):raise ValueError('finite N>=2 and paired targets required')
 currents=[imag(y[j],y[j+1])for j in range(len(y)-1)]
 if any(s==0 for s in currents):raise ValueError('zero current requires separate compatibility analysis')
 ts=[imag(a,b)for a,b in zip(y,z)]
 if sum(ts)!=0:raise ValueError('global current compatibility fails')
 hops=[];prefix=Q(0)
 for j,s in enumerate(currents):prefix+=ts[j];hops.append(prefix/s)
 off=action([Q(0)]*len(y),hops,y)
 diag=[real(y[j],add(z[j],scale(-1,off[j])))/real(y[j],y[j])for j in range(len(y))]
 return diag,hops

class JacobiResponse(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.library=Library()

 def test_exact_chain_recovery_and_last_row(self):
  for n in range(2,8):
   y=[c(1,j+1)for j in range(n)] # every adjacent current is one.
   d=[Q((j+1)*(-1)**j,3)for j in range(n)];h=[Q(j+2,5)for j in range(n-1)]
   z=action(d,h,y);self.assertEqual(sum(imag(a,b)for a,b in zip(y,z)),0)
   reconstructed=reconstruct(y,z);self.assertEqual(reconstructed,(d,h));self.assertEqual(action(*reconstructed,y),z)
  record=self.library.resolve(UNIT);self.assertIn('Prefix sums',record['body']);self.assertIn('unique',record['statement'])

 def test_global_condition_is_required(self):
  y=[c(1),c(0,1)];z=[c(0,1),c(0)]
  with self.assertRaisesRegex(ValueError,'global current'):reconstruct(y,z)

 def test_zero_edge_has_nonunique_or_infeasible_cases(self):
  y=[c(1),c(1)];z=[c(0),c(0)]
  for a in [Q(0),Q(1),Q(7,3)]:self.assertEqual(action([a,a],[-a],y),z)
  with self.assertRaisesRegex(ValueError,'zero current'):reconstruct(y,z)
  bad=[c(0,1),c(0,-1)];self.assertEqual(sum(imag(a,b)for a,b in zip(y,bad)),0)
  # Any real matrix acting on real y is real; global compatibility alone fails.
  self.assertTrue(any(b[1]for b in bad));self.assertIn('separate existence',self.library.resolve(UNIT)['contract']['assumptions'][1])

 def test_individually_legal_targets_need_not_share_matrix(self):
  y1,z1=[c(1),c(0,1)],[c(0,1),c(1)]
  y2,z2=[c(1),c(0,2)],[c(0,4),c(2)]
  a,b=reconstruct(y1,z1),reconstruct(y2,z2)
  self.assertEqual(a,([Q(0),Q(0)],[Q(1)]));self.assertEqual(b,([Q(0),Q(0)],[Q(2)]))
  self.assertNotEqual(action(*a,y2),z2);self.assertNotEqual(action(*b,y1),z1)
  self.assertIn('not a common multiport',self.library.resolve(UNIT)['body'])

 def test_bounded_targets_can_force_unbounded_nonpositive_controls(self):
  for d in [Q(1),Q(1,10),Q(1,1000)]:
   y,z=[c(1),c(1,d)],[c(0,1),c(0,-1)];diag,hops=reconstruct(y,z)
   self.assertEqual((diag,hops),([-1/d,-1/d],[1/d]));self.assertEqual(action(diag,hops,y),z)
   self.assertEqual(action(diag,hops,[c(1),c(1)]),[c(0),c(0)])
   self.assertEqual(action(diag,hops,[c(1),c(-1)]),[c(-2/d),c(2/d)])
  self.assertIn('unbounded',self.library.resolve(UNIT)['contract']['assumptions'][1])

 def test_one_point_does_not_set_a_band_derivative(self):
  y,z=[c(1),c(0,1)],[c(0,1),c(1)];diag,hops=reconstruct(y,z)
  shifted=[add(z[j],scale(Q(1,100),y[j]))for j in range(2)]
  self.assertEqual(action(diag,hops,y),z);self.assertNotEqual(action(diag,hops,y),shifted)
  self.assertIn('one design energy',self.library.resolve(UNIT)['contract']['requires'][0])

 def test_actual_sources_acceptance_notice_and_missing_support(self):
  index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes());self.assertEqual(len(index['files']),1);row=index['files'][0]
  self.assertEqual(row['bytes'],5671);self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),SHA)
  source=self.library.source(UNIT,0);self.assertEqual(source['source']['sha256'],SHA);self.assertEqual(source['source']['lines'],[48,66]);self.assertIn('denominators are nonzero',source['text']);self.assertIn('sum',source['text'])
  for identifier in ['N1031',UNIT]:
   r=self.library.resolve(identifier);review=next(x for x in r['review_overlays']if x['id']=='A1051-jacobi-response')
   self.assertEqual(review['decision'],'accepted_internally_verified');self.assertIn({'id':r['id'],'content_version':r['content_version']},review['subjects'])
   self.assertEqual(review['working_device'],'not established');self.assertTrue(any(n['notice_id']==NOTICE and not n['whole_claim_invalidated']for n in r['notices']))
  with self.assertRaisesRegex(ValueError,'INGESTION FAILED: required source bytes missing'):
   Inputs(ROOT).source(dict(path=UPDATE+'/source/p2/unacquired_scattering_target.py',sha256='0'*64,lines=[1,1]))

 def test_old_geometry_bridge_and_actual_default_commands(self):
  t=self.library.bridge(OLD,UNIT)['transfers'][0];self.assertEqual(t['state'],'INCOMPATIBLE ASSUMPTIONS');self.assertIn('target z',t['scope'])
  for endpoint in ['from','to']:self.assertEqual(t[endpoint+'_version'],self.library.resolve(t[endpoint])['content_version'])
  for args in [('packet',i)for i in ['N1031',UNIT,'N1030',OLD,'U1027-reciprocal-parity-band-certificate']]+[('bridge',OLD,UNIT)]:
   p=subprocess.run([sys.executable,'knowledge/retrieve.py',*args],cwd=ROOT,capture_output=True);self.assertEqual(p.returncode,0,p.stderr);self.assertLessEqual(len(p.stdout),32768)

if __name__=='__main__':unittest.main()
