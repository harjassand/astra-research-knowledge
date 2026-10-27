"""Independent small analytic controls, no producer imports or programmes."""
from fractions import Fraction as F
from math import comb,exp,log,sqrt,pi
from itertools import product
import unittest
class FinalOperationControls(unittest.TestCase):
 def test_product_disk_error_expansion(self):
  def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
  a,b,c=(F(1),F(1)),(F(2),F(-1)),(F(1),F(0));e=F(1,10)
  base=mul(mul(a,b),c);ub=[sum(map(abs,z))for z in(a,b,c)];bound=product3([x+e for x in ub])-product3(ub)
  for ds in product([(e,0),(-e,0),(0,e),(0,-e)],repeat=3):
   z=[tuple(x+y for x,y in zip(v,d))for v,d in zip((a,b,c),ds)];v=mul(mul(*z[:2]),z[2]);self.assertLessEqual(sum(abs(x-y)for x,y in zip(v,base)),bound)
 def test_whole_block_zero_stays_in_sample(self):
  vals=[F(1),F(-1),F(0)];mean=sum(vals)/3;var=sum((x-mean)**2 for x in vals)/2
  self.assertEqual((mean,var),(0,1));self.assertNotEqual(var,2)
 def test_affinity_geometry_and_total_bill(self):
  r2=F(1,4);A2=36*r2/(1-r2);self.assertEqual(A2,12);self.assertLess(float(A2),4*pi*pi*float(r2/(1-r2)))
  self.assertEqual(1-F(1,100)-F(1,200)-F(1,200),F(49,50));N=13;self.assertEqual(2*(2*N+N),6*N)
 def test_independent_channel_residual_and_dual(self):
  K=[[F(2,15),F(49,120),F(49,120)],[F(13,30),F(71,240),F(71,240)],[F(13,30),F(71,240),F(71,240)]]
  L=[[F(2,3)if i==j else F(1,6)for j in range(3)]for i in range(3)]
  U=[[0,F(2,5),F(2,5)],[F(2,5),F(11,40),F(11,40)],[F(21,40),F(1,4),F(1,4)]]
  D=[[K[y][x]-sum(U[y][z]*L[z][x]for z in range(3))for x in range(3)]for y in range(3)]
  self.assertTrue(all(v>=0 for row in D for v in row));self.assertEqual([sum(row[x]for row in D)for x in range(3)],[F(3,40)]*3)
  alpha=[[F(5,2),0,0],[0,F(1,2),F(1,2)],[0,F(1,2),F(1,2)]];p=[0,F(1,2),F(1,2)]
  slack=[[sum((alpha[y][x]-p[x])*L[z][x]for x in range(3))for z in range(3)]for y in range(3)]
  self.assertEqual(slack,[[F(3,2),0,0],[0,0,0],[0,0,0]])
  self.assertEqual(1-sum(alpha[y][x]*K[y][x]for y in range(3)for x in range(3)),F(3,40))
  # Unique signed postprocessor first row gives a negative entry yet reproduces K.
  A=[[-F(1,20),F(1,2),F(1,2)],[F(21,40),F(1,4),F(1,4)],[F(21,40),F(1,4),F(1,4)]]
  self.assertEqual([[sum(A[y][z]*L[z][x]for z in range(3))for x in range(3)]for y in range(3)],K)
  rewards=[-6,1,1]
  def best(C):return sum(max(F(0),sum(row[x]*rewards[x]for x in range(3))/3)for row in C)
  self.assertEqual(best(K)-best(L),F(1,180));self.assertEqual((best(K)-best(L))/7,F(1,1260))
 def test_binomial_count_and_common_branch(self):
  q=F(3,40);tail=sum(F(comb(4,k))*q**k*(1-q)**(4-k)for k in range(2,5))
  enumerated=sum(product3([q if b else 1-q for b in bits])for bits in product([0,1],repeat=4)if sum(bits)>1)
  self.assertEqual(tail,enumerated)
  # Positive common branch diag(1-p,0,0), alternatives differ only on disjoint residuals.
  p=F(1,7);rho=[1-p,p,0];sig=[1-p,0,p];self.assertEqual(sum(abs(x-y)for x,y in zip(rho,sig))/2,p)
 def test_finite_wall_constants_and_drift(self):
  d=F(1,1024);k=(65*(1+d)+138+1)/d**3;self.assertEqual(k,219111489536)
  self.assertEqual(1-F(2,4)-65*d,F(447,1024));self.assertEqual(F(1,4)-65*d,F(191,1024));self.assertEqual((2+d)/F(191,1024),F(2049,191))
 def test_hard_stop_rewrite_counts(self):
  for n in range(1,9):
   for old,new in product(range(n+1),repeat=2):
    flips=(4*n+2)+(4*n+2)+(2*n+old+new);self.assertEqual(flips,10*n+4+old+new)
    work=20*(4*n+2)+80*(4*n+2)+26*(2*n+old+new);self.assertEqual(work,452*n+200+26*(old+new))
 def test_pressure_nullspace_cube_and_hexagon(self):
  omega=complex(-.5,sqrt(3)/2)
  for ps in product([-1,1],repeat=3):
   z=sum(ps[j]*omega**j for j in range(3));self.assertLessEqual(abs(z),2+1e-12)
  self.assertAlmostEqual(abs(1+omega+omega**2),0)
  q=.5;self.assertAlmostEqual((1-q)*sqrt(3)/(2*sqrt(1+q*q-q)),.5)
  # Midpoint of a chord between successive hexagon vertices has the exact radius floor.
  w=complex(.5,sqrt(3)/2);c=(1-q)/(w-q);z=1+(c-1)*sqrt(q)
  self.assertGreaterEqual(abs(z),.5-1e-12)
 def test_wrench_does_not_defeat_static_friction(self):
  Ar=F(3,10);maxradius=2;friction=1;self.assertGreaterEqual(friction,Ar*maxradius)
 def test_slow_mixture_jensen_and_feasibility(self):
  t=300;lam=[F(1,100),F(1,10000)];weights=[F(9,10),F(1,10)];surv=sum(float(w)*exp(-float(x)*t)for w,x in zip(weights,lam));self.assertGreaterEqual(surv,exp(-float(sum(w*x for w,x in zip(weights,lam)))*t))
  p,z,f,ls,d,L,eps=.6,.004,.1,.0001,3e-8,1024,.05;theta=(1-eps)**(-1/L)-1
  lower=log(z*f/((p+z)*theta))/ls;upper=-log(1-eps)/(L*d);self.assertGreater(lower,upper)
 def test_finite_depth_stationary_point(self):
  p,w,sc,sw,delta,L=.6,.001,.8,.1,1e-5,1024
  n=log(delta*log(1/sc)/(w*log(sc/sw)))/log(sw);self.assertAlmostEqual(n,2.969,places=3)
  def loss(j):return(w/p)*(sw/sc)**j+(delta/p)*sc**(-j)
  self.assertLess(loss(3),loss(2));self.assertLess(loss(3),loss(4))
 def test_identity_independent_gate_preserves_odds(self):
  C,W,G,damage=F(3,5),F(1,100),F(4,5),F(1,1000)
  self.assertEqual(G*W/(G*C),W/C);self.assertLess(G*C/(G*(C+W)+damage),C/(C+W+damage))
 def test_fixed_wait_jensen_comparator(self):
  kc,kw=.001,.03;T=[100,400];sc=sum(exp(-kc*t)for t in T)/2;sw=sum(exp(-kw*t)for t in T)/2
  self.assertGreaterEqual(sw,sc**(kw/kc));fixed=-log(sc)/kc;self.assertAlmostEqual(exp(-kw*fixed),sc**(kw/kc))
 def test_recapture_leak_renewal_and_limit(self):
  g,k,ell=F(1,100),F(9,100),F(1,100000);s=g/(g+k+ell)
  for n in [1,3,7]:
   terminal=s**n;leak=ell*(1-terminal)/(k+ell);detach=k*(1-terminal)/(k+ell)
   self.assertEqual(terminal+leak+detach,1)
   for r in[0,F(9,10),1]:
    P=(terminal+leak)/(1-r*detach);self.assertEqual(P,terminal+leak+r*detach*P)
    if r==1:self.assertEqual(P,1)
  r=F(99,100);floor=ell/(ell+(1-r)*k);self.assertGreater(floor,0)
 def test_realistic_thousand_round_certified_budget(self):
  T,a,b=1000,3,40
  def tail(B):return F(sum(comb(T,k)*a**k*(b-a)**(T-k)for k in range(B+1,T+1)),b**T)
  self.assertGreater(tail(116),F(1,10**6));self.assertLessEqual(tail(117),F(1,10**6))
 def test_dna_only_indistinguishable_acceptance(self):
  p,w,a=F(3,5),F(1,1000),F(1,9);self.assertEqual(a*p/(a*(p+w)),p/(p+w))
def product3(xs):
 out=F(1)
 for x in xs:out*=x
 return out

class FinalOperationCurrentRoutes(unittest.TestCase):
 def test_actual_version_acceptance_and_missing_numerics(self):
  from knowledge.retrieve import Library
  l=Library()
  for name in['N1072','N1073','N1074','N1075','N1076']:
   r=l.resolve(name);p=l.packet([name])['packets'][0];a=p['review_overlays'][0]
   self.assertEqual(a['decision'],'accepted_internally_verified');self.assertIn({'id':r['id'],'content_version':r['content_version']},a['subjects']);self.assertEqual(a['working_device'],'not established')
  r=l.resolve('U1072-exact-fixed-n-reader-and-eof-guard');self.assertIn('911c9888',r['statement'])
  p=l.packet(['N1076'])['packets'][0];self.assertIn('DEFERRED',str(p));self.assertIn('WASH-ACTIVE-SINK',str(p['notices']))
 def test_corrections_reach_actual_ancestors(self):
  from knowledge.retrieve import Library
  l=Library()
  self.assertIn('AFFINITY-NOT-RATE',str(l.packet(['N1060'])['packets'][0]['notices']))
  for name in['N1058','U1058-open-loop-registry-retry-and-retained-handle-aging']:
   notices=l.packet([name])['packets'][0]['notices'];self.assertIn('WASH-ACTIVE-SINK',str(notices));self.assertIn('9635',str(notices));self.assertIn('9674',str(notices))
 def test_actual_source_branches(self):
  from knowledge.retrieve import Library
  l=Library()
  cases=[('U1072-sector-cone-through-common-prefilter-gate','## Uniform spectral cone'),('U1072-common-gate-mean-phase-reference','## The gate gives'),('U1072-whole-block-clipping-to-unclipped-confidence','## Centering'),('U1072-exact-fixed-n-reader-and-eof-guard','Exact fixed-N'),('U1073-subchannel-lp-and-paid-residual','## One-step'),('U1073-adaptive-cq-count-tail-at-local-interface','## Adaptive exactness'),('U1073-budget-abort-common-positive-branch','## Hard budget'),('U1073-entropy-order-not-decision-or-free-replacement','Entropy comparison'),('U1074-all-n-local-event-induction-and-reset','## Statement'),('U1074-finite-c3-wall-and-event-holds','Finite-compliance continuation'),('U1074-rewrite-work-and-thermal-scope','## Complete ideal-cycle'),('U1075-pressure-space-vector-and-nonvanishing-winding','## Exact pressure-to-wrench'),('U1075-hexagon-filter-witness-and-lag-gate','## Exact pressure-to-wrench'),('U1075-source-data-and-manufacturing-service-ceiling','## Source-scaled'),('U1076-slow-intermediate-mixtures-and-wash-window','A stronger benchmark'),('U1076-active-donor-wash-and-dna-only-blindness','A stronger benchmark'),('U1076-finite-proofreading-depth-and-shared-clock','A missing failure pathway'),('U1076-deterministic-wait-comparator-needs-permanent-removal','A more consequential constraint'),('U1076-recapture-leak-floor-and-activatable-waste','A more consequential constraint')]
  for name,phrase in cases:self.assertIn(phrase.lower(),l.source(name)['text'].lower(),name)
 def test_supported_and_incompatible_interfaces(self):
  from knowledge.retrieve import Library
  l=Library()
  cases=[('U1073-adaptive-cq-count-tail-at-local-interface','U1073-budget-abort-common-positive-branch','ESTABLISHED COMPATIBLE INTERFACE'),('U1038-three-lmi-global-interval-evaluator','U1073-entropy-order-not-decision-or-free-replacement','REFUTED TRANSFER'),('U1074-all-n-local-event-induction-and-reset','U1074-finite-c3-wall-and-event-holds','ESTABLISHED COMPATIBLE INTERFACE'),('U1075-pressure-space-vector-and-nonvanishing-winding','U1075-hexagon-filter-witness-and-lag-gate','INCOMPATIBLE ASSUMPTIONS')]
  for fr,to,state in cases:self.assertEqual(l.bridge(fr,to)['transfers'][0]['state'],state)
  self.assertEqual(l.bridge('U1074-all-n-local-event-induction-and-reset','U1075-hexagon-filter-witness-and-lag-gate')['state'],'NO SUPPORTED CONNECTION')
 def test_actual_default_parent_and_corrected_ancestor_packets(self):
  import json,subprocess,sys
  from pathlib import Path
  root=Path(__file__).resolve().parents[1]
  for name in['N1072','N1073','N1074','N1075','N1076','N1058','N1060']:
   p=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',name],cwd=root,capture_output=True)
   self.assertEqual(p.returncode,0,p.stderr.decode());self.assertLessEqual(len(p.stdout),32768);v=json.loads(p.stdout)['packets'][0];self.assertTrue(v['evidence']and v['source_excerpts']and v['review_overlays'])

if __name__=='__main__':unittest.main()
