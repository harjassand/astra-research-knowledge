"""Small independent interface controls; no producer imports or research rerun."""
from fractions import Fraction as F
from itertools import product
from math import sqrt
import unittest
class CompiledInterfaceControls(unittest.TestCase):
 def test_signed_pin_and_zero_partition_semantics(self):
  self.assertEqual(-1334+1760,426);self.assertLess(F(-1334,426),0);self.assertGreater(F(1760,426),1)
  self.assertEqual(604-604,0);self.assertNotEqual(604,0)
 def test_original_height_and_crt_uniqueness(self):
  H=5;M=15;vals=[i for i in range(-H,H+1)if i%M==(-4)%M];self.assertEqual(vals,[-4])
  self.assertEqual([i for i in range(-H,H+1)if i%7==3],[-4,3])
 def test_fp2_norm_square_scope(self):
  p=3
  def mul(x,y):return((x[0]*y[0]+2*x[1]*y[1])%p,(x[0]*y[1]+x[1]*y[0])%p)
  xs=set(product(range(p),repeat=2))-{(0,0)};squares={mul(x,x)for x in xs}
  for x in xs:
   norm=(1,0)
   for _ in range(4):norm=mul(norm,x)
   self.assertEqual(norm[1],0);self.assertEqual(x in squares,norm[0]==1)
 def test_loaded_cohort_ratio_is_not_feed_recovery(self):
  r=F(1,2);rho=2;q=F(1,100)
  self.assertEqual(q*r/(q*r+r**rho),F(1,51));self.assertLess(F(1,10)*r,r)
 def test_finite_counterflow_recurrences(self):
  M=7
  for p in[F(1,3),F(1,2),F(27,50)]:
   r=(1-p)/p
   h=[F(i,M)if p==F(1,2)else(1-r**i)/(1-r**M)for i in range(M+1)]
   t=[F(i*(M-i))if p==F(1,2)else(M*h[i]-i)/(2*p-1)for i in range(M+1)]
   for i in range(1,M):self.assertEqual(h[i],p*h[i+1]+(1-p)*h[i-1]);self.assertEqual(t[i],1+p*t[i+1]+(1-p)*t[i-1]);self.assertGreater(t[i],0)
 def test_ionic_exact_power_interval_and_conservative_time(self):
  lo,hi=F(451284,10**6),F(451285,10**6);p=F(27,50)
  self.assertLess(lo**103,p**133);self.assertLess(p**133,hi**103)
  i,M=15,90;r=(1-p)/p;h=(1-r**i)/(1-r**M);self.assertGreater(h,F(9,10))
  rn=(1-hi)/hi;hn=(1-rn**i)/(1-rn**M);purity=h/(h+10000*hn);self.assertGreater(purity,F(99,100));self.assertLessEqual((i-M*hn)/(1-2*hi),i/(1-2*hi))
 def test_ladder_atom_weight_and_nonremovable_root_bounds(self):
  # sqrt3>12/7 gives4/sqrt3-2<1/3. Largestcoupling²8/25.
  self.assertLess(F(12,7)**2,3);weight=1/(1+F(8,25)*F(1,3));self.assertEqual(weight,F(75,83));self.assertGreater(weight,F(9,10))
  W=F(81,100);self.assertLess((-W+1-W)/F(3,5),0);self.assertGreater(W/F(3,5)-(1-W)/F(1,2),0)
 def test_ladder_interaction_coefficients_and_parity_roles(self):
  a=4-2*sqrt(3);b=4/sqrt(3)-2
  self.assertAlmostEqual(3*a*b,28*sqrt(3)-48);self.assertGreater(3*a*b,0)
  g=F(1,10);t=(1+sqrt(2))/2*float(g);s=(sqrt(2)-1)/2*float(g)
  self.assertAlmostEqual((t+s)**2,2*float(g*g));self.assertAlmostEqual((t-s)**2,float(g*g));self.assertAlmostEqual(8*a*b*t*s*(t*t+s*s),3*a*b*float(g**4))
  self.assertEqual(F(8)*F(1,5)*0*(F(1,25)+0),0)
 def test_fixed_sector_stability_not_capacity(self):
  g=F(2,5);self.assertEqual(3-2*g*g,F(67,25));self.assertGreater(10-4*sqrt(6),0);self.assertGreater(3-2*float(g*g)*(10-4*sqrt(6)),0)

class CompiledCurrentInterfaces(unittest.TestCase):
 def test_accepted_versions_and_notice_scope(self):
  from knowledge.retrieve import Library
  l=Library()
  for name in['N1077','N1078','N1079','N1080']:
   r=l.resolve(name);p=l.packet([name])['packets'][0];a=p['review_overlays'][0]
   self.assertEqual(a['decision'],'accepted_internally_verified');self.assertIn({'id':r['id'],'content_version':r['content_version']},a['subjects']);self.assertEqual(a['working_device'],'not established')
  self.assertIn('REVIEW-PREFIX',str(l.packet(['N1077'])['packets'][0]['notices']))
  self.assertIn('WRONG-BAND-PRESERVES-PARITY',str(l.packet(['U1080-wrong-band-is-not-parity-breaking-noise'])['packets'][0]['notices']))
 def test_actual_review_prefix_and_core_bindings(self):
  import hashlib,json
  from pathlib import Path
  from knowledge.retrieve import Library
  l=Library();r=l.resolve('N1077');ref=next(e for e in r['evidence']if e['path'].endswith('/ACCEPTED_VERSION.json'));manifest=json.loads((l.root/ref['path']).read_text());directory=(l.root/ref['path']).parent
  reviewref=next(e for e in r['evidence']if e['path'].endswith('/REVIEW.md'));raw=(l.root/reviewref['path']).read_bytes();self.assertEqual(len(raw),7360)
  expected=manifest['review_files_sha256']['REVIEW.md'];self.assertEqual(hashlib.sha256(raw[:6757]).hexdigest(),expected);self.assertNotEqual(hashlib.sha256(raw).hexdigest(),expected)
  for name,digest in manifest['accepted_core_sha256'].items():self.assertEqual(hashlib.sha256((directory/name).read_bytes()).hexdigest(),digest)
  self.assertEqual(hashlib.sha256((directory/'PROOF.md').read_bytes()).hexdigest(),manifest['proof_sha256'])
 def test_real_source_windows_not_neighboring_branch(self):
  from knowledge.retrieve import Library
  l=Library()
  cases=[('U1077-local-quadratic-compatibility-without-global-field','Local quadratic CP'),('U1077-common-quadratic-finite-field-and-fisher-sign','common finite field'),('U1077-original-edge-insertion-and-prefactor','ORIGINAL edge-bit'),('U1077-original-height-crt-and-declared-work-cap','ORIGINAL edge-bit'),('U1078-fresnel-response-and-metal-zero-mode','Model and exact observable'),('U1078-full-charge-additive-sum-rule','Model and exact observable'),('U1078-exact-rational-activity-gate-not-rate','Root exact numerical'),('U1079-closed-bed-and-loaded-cohort-frontiers','Saturation cannot'),('U1079-finite-source-gross-turnover-floor','Saturation cannot'),('U1079-one-source-convex-optimum','optimal ONE-SOURCE'),('U1079-stored-pool-counterflow-and-absorption','Operation and premises'),('U1080-sector-gap-and-nonremovable-pair-root','One connected'),('U1080-spectral-reflection-cancels-interaction','Nonzero fourth-order'),('U1080-positive-schur-all-fixed-n-stability','Complete positivity'),('U1080-sector-adiabatic-echo-and-finite-error-gap','Complete positivity'),('U1080-wrong-band-is-not-parity-breaking-noise','Executed independent checks')]
  for name,phrase in cases:self.assertIn(phrase.lower(),l.source(name)['text'].lower(),name)
 def test_actual_interface_states_and_older_scope(self):
  from knowledge.retrieve import Library
  l=Library()
  for fr,to,state in[('N635','U1077-local-quadratic-compatibility-without-global-field','INCOMPATIBLE ASSUMPTIONS'),('U1079-one-source-convex-optimum','U1079-stored-pool-counterflow-and-absorption','INCOMPATIBLE ASSUMPTIONS'),('U1067-exact-parity-pair-resolvent','U1080-sector-gap-and-nonremovable-pair-root','ESTABLISHED COMPATIBLE INTERFACE'),('U1080-sector-gap-and-nonremovable-pair-root','U1080-spectral-reflection-cancels-interaction','REFUTED TRANSFER')]:
   self.assertEqual(l.bridge(fr,to)['transfers'][0]['state'],state)
  self.assertFalse(l.resolve('N635')['review_overlays'])
 def test_default_new_and_previous_packets_keep_budget(self):
  import subprocess,sys,json
  from pathlib import Path
  root=Path(__file__).resolve().parents[1]
  for name in['N1077','N1078','N1079','N1080','N635','U1067-exact-parity-pair-resolvent']:
   p=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',name],cwd=root,capture_output=True)
   self.assertEqual(p.returncode,0,p.stderr.decode());self.assertLessEqual(len(p.stdout),32768);self.assertTrue(json.loads(p.stdout)['packets'][0]['evidence'])

if __name__=='__main__':unittest.main()
