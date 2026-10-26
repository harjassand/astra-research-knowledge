"""Independent new-source algebraic controls; no producer/accepted-audit replay."""
import cmath,math,unittest
from fractions import Fraction as F

class RadiativeAccessControls(unittest.TestCase):
 def test_exact_inactive_leaf_moment_independent_antiderivative(self):
  p=[F(0),F(1),-F(1,3),F(1,24),-F(1,432),F(1,20736)]
  def value(q,x):return sum(float(c)*x**i for i,c in enumerate(q))
  q=p[:];at0=0j;at12=0j
  for k in range(6):
   factor=(-1)**k/(1j**(k+1));at0+=factor*value(q,0);at12+=factor*value(q,12)
   q=[(i+1)*q[i+1]for i in range(len(q)-1)]
  integral=(cmath.exp(12j)*at12-at0).real
  exact=(-653+12*math.sin(12)+5*math.cos(12))/864
  self.assertAlmostEqual(integral,exact,places=11)
  self.assertLess(-653+12+5,0)
  self.assertEqual(F(64,4),16);self.assertEqual(F(64,20),F(16,5))
 def test_volterra_solution_and_resource_threshold(self):
  wl=wr=.0314290833832;t=12
  upper=wl/wr*(math.cosh(wr*t)-1)
  self.assertLess(upper,.072);self.assertGreater(upper,.0719)
  self.assertGreater(math.acosh(1+wr/wl)/wr,41.9)
  self.assertGreater(1/(wr*wr*t),t)
  self.assertEqual(math.ceil((math.acosh(2)/(t*math.sqrt(9.6)*.01))**2),13)
  # Series solves R''=wl*wr+wr^2 R with the correct zero initial data.
  series=sum(wl*wr**(2*k-1)*t**(2*k)/math.factorial(2*k)for k in range(1,9))
  self.assertAlmostEqual(series,upper,places=14)
 def test_port_rank_and_one_channel_null_are_different(self):
  for w in[.2,.7,1.5]:
   a=cmath.exp(1j*w*.5);b=cmath.exp(-1j*w*.5)
   self.assertGreater(abs(b-a),.1)
   # One-direction row [1,e^(iw*tau)] admits a nonzero shifted Fourier source.
   q1=complex(.3,.2);q2=-q1/a;self.assertLess(abs(q1+a*q2),1e-14)
   self.assertGreater(abs(q1+b*q2),.01)
 def test_markov_populations_and_full_state_error(self):
  for x in[1.,4.,12.5]:
   q=math.exp(-x);self.assertAlmostEqual(q+(1-q)**2+q-q*q,1)
   self.assertAlmostEqual(2-2*(1-q),2*q)
   self.assertGreater(q,0)
 def test_gapless_arm_form_inverse_and_paid_counterterm(self):
  for j in[F(4),F(8)]:
   green=F(0)
   for m in range(1,50):
    green=1/(2*j-j*j*green);self.assertEqual(green,F(m,1)/(j*(m+1)));self.assertLess(green,1/j)
  eta=F(1,20);j=F(8);delta=eta*eta/j;self.assertEqual(delta,F(1,3200))
  for m in[1,10,7000]:self.assertGreaterEqual(delta-eta*eta*F(m,1)/(j*(m+1)),0)
 def test_rigorous_factorial_tail_is_not_an_ode_bound(self):
  j=F(8);k=F(321,20);t=F(2299,16);m=7000
  # e<2.72 from its factorial series and a geometric tail.
  esum=sum(F(1,math.factorial(n))for n in range(10));etail=F(1,math.factorial(10))*F(11,10)
  self.assertLess(esum+etail,F(68,25))
  ratio=F(68,25)*k*t/m
  bound=j*t*ratio**m/(1-k*t/(m+1))
  self.assertLess(bound,F(1,10**320))
  self.assertGreater(k*t,2300);self.assertLess(k*t,m+1)
 def test_exact_parity_compression_harmonic_mean(self):
  for lp,lm in[(F(2),F(3)),(F(5,7),F(11,13)),(F(-3,2),F(9,4))]:
   m=(lp+lm)/2;n=(lp-lm)/2
   self.assertEqual(m-n*n/m,2*lp*lm/(lp+lm))
   self.assertEqual(1/(m-n*n/m),(1/lp+1/lm)/2)
 def test_zero_form_ssh_import_from_current_bloch_formula(self):
  for delta in[F(1,10),F(1,100),F(1,1000)]:
   t=-3-delta;q=(t+1)*(t+3)/4;a=t*t-5
   lhs=q*q/((a-4)*(a+4));rhs=(t+1)*(t+3)/(16*(t-3)*(t-1))
   self.assertEqual(lhs,rhs);self.assertLess(rhs,delta/100)
  self.assertEqual(F(1,2)-F(1,4),F(1,4))
 def test_connected_shift_cancels_common_retuning(self):
  fp,fm,dp,dm=-F(3,8),-F(5,8),-F(1,6),-F(1,2)
  for a in[-F(3),F(0),F(1,2),F(9,7)]:
   ap=a+fp;am=a+fm;sum4=ap*dp+am*dm;centre4=sum4-(fp-fm)*(dp-dm)
   self.assertEqual(centre4-sum4,-F(1,12))
  self.assertEqual((fp-fm)**2,F(1,16))
 def test_coarea_constants_and_two_linewidth_conventions(self):
  # u=5+4cos(k); primitives evaluated at sqrt(u)=1,3. Values are pi^2*c_sigma.
  def plus(v):return 2*v+4/v-F(2,3)/v**3
  def minus(v):return -54/v**3+36/v+2*v
  cp=(plus(F(3))-plus(F(1)))/256;cm=(minus(F(3))-minus(F(1)))/256
  self.assertEqual(cp,F(5,648));self.assertEqual(cm,F(1,8));c=(cp+cm)/2;self.assertEqual(c,F(43,648))
  # gamma=pi*c_actual/16, c_actual=c/pi^2. Probability coefficient is2gamma.
  self.assertEqual(c/16,F(43,10368));self.assertEqual(2*c/16*12,F(43,432))


class RadiativeAccessCurrentRoutes(unittest.TestCase):
 def test_current_review_scope_not_missing_physical_or_old_proofs(self):
  from knowledge.retrieve import Library
  l=Library()
  for name in ['N1065','N1066','N1067','U1067-phase-only-obstruction-and-matched-cz-comparator']:
   r=l.resolve(name);p=l.packet([name])['packets'][0];self.assertEqual(len(p['review_overlays']),1)
   a=p['review_overlays'][0];self.assertEqual(a['decision'],'accepted_internally_verified')
   self.assertIn({'id':r['id'],'content_version':r['content_version']},a['subjects'])
   self.assertEqual(a['working_device'],'not established');self.assertTrue(a['remaining_gaps'])
  p=l.packet(['N1067'])['packets'][0]
  self.assertTrue(any('5g'in gap for gap in p['review_overlays'][0]['remaining_gaps']))
  p=l.packet(['N1057'])['packets'][0]
  self.assertTrue(any('LOCAL-LEAF'in n['notice_id']for n in p['notices']))
  self.assertTrue(any(a['decision']=='accepted_internally_verified'for a in p['review_overlays']))
  for name in ['N1067','U1067-inclusive-phase-echo-with-declared-controls','U1067-phase-only-obstruction-and-matched-cz-comparator']:
   self.assertTrue(any('PHASE-COMPARATOR'in n['notice_id']for n in l.packet([name])['packets'][0]['notices']))
 def test_actual_sources_open_the_right_construction_branch(self):
  from knowledge.retrieve import Library
  l=Library()
  cases=[('U1065-inactive-leaf-backaction','## 3. The omitted equation'),('U1065-no-bypass-coupling-time-and-exposure','## 4. A universal'),('U1065-full-column-radiation-rank','## 2. An exact terminal-radiation'),('U1066-gapless-arm-form-counterterm','### A genuinely interacting'),('U1066-infinite-arm-truncation-not-solver-error','### Rigorous link'),('U1067-cauchy-pair-scaling-and-shorter-coherent-time','## 6. Long-time spectral theorem'),('U1067-inclusive-phase-echo-with-declared-controls','## 7. An asymptotic')]
  for name,phrase in cases:self.assertTrue(l.source(name)['text'].startswith(phrase),name)
  current=l.source('N1067');self.assertTrue(current['source']['path'].endswith('ASTRA_SSH_EMBEDDED_PAIR_RESONANCE_AND_CZ_20261027.md'))
 def test_actual_default_packets_keep_budget_review_and_corrections(self):
  import subprocess,sys,json
  from pathlib import Path
  root=Path(__file__).resolve().parents[1]
  for name in ['N1065','N1066','N1067','N1057','U1057-boundary-source-support-and-four-point-open-interface']:
   r=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',name],cwd=root,capture_output=True)
   self.assertEqual(r.returncode,0,r.stderr.decode());self.assertLessEqual(len(r.stdout),32768)
   p=json.loads(r.stdout)['packets'][0];self.assertTrue(p['evidence']and p['source_excerpts']and p['review_overlays'])

if __name__=='__main__':unittest.main()
