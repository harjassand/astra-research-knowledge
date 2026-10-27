"""Independent source-exposed mathematical controls; no producer programmes."""
import math,unittest
from fractions import Fraction as F

def inv(a):
 n=len(a);v=[[F(x)for x in r]+[F(i==j)for j in range(n)]for i,r in enumerate(a)]
 for j in range(n):
  k=next(i for i in range(j,n)if v[i][j]);v[j],v[k]=v[k],v[j];d=v[j][j];v[j]=[x/d for x in v[j]]
  for i in range(n):
   if i!=j:
    d=v[i][j];v[i]=[x-d*y for x,y in zip(v[i],v[j])]
 return[r[n:]for r in v]
def mv(a,v):return[sum(x*y for x,y in zip(r,v))for r in a]
def det(a):
 a=[[F(x)for x in r]for r in a];out=F(1);n=len(a)
 for j in range(n):
  ks=[i for i in range(j,n)if a[i][j]]
  if not ks:return F(0)
  k=ks[0]
  if k!=j:a[j],a[k]=a[k],a[j];out=-out
  d=a[j][j];out*=d
  for i in range(j+1,n):
   q=a[i][j]/d
   for k in range(j,n):a[i][k]-=q*a[j][k]
 return out
def moment(atoms,k):return sum(w*x**k for x,w in atoms)
def poly(p,x):return sum(a*x**i for i,a in enumerate(p))
def padd(p,q):return[(p[i]if i<len(p)else 0)+(q[i]if i<len(q)else 0)for i in range(max(len(p),len(q)))]
def pmul(p,q):
 v=[F(0)]*(len(p)+len(q)-1)
 for i,a in enumerate(p):
  for j,b in enumerate(q):v[i+j]+=a*b
 return v
def pscale(p,c):return[a*c for a in p]
def schur(q,h,lam):
 k=lam/h;s=[[2+k,1,-k,0],[1,2,0,0],[-k,0,1/q+k,0],[0,0,0,F(5,3)]]
 w=s[0][1:];ii=inv([r[1:]for r in s[1:]])
 return s[0][0]-sum(x*y for x,y in zip(w,mv(ii,w)))

class CausalSpectralControls(unittest.TestCase):
 def test_actual_schur_and_matched_nonlinear_nuisance(self):
  for t in range(1,7):
   q0=F(3,5)+F(t*t,1000);h=F(4,5)+F(t**3,100000);g=F(3,4)**(t-1)/t;delta=F(1,5)
   a=schur(q0+delta*g,h,F(1));b=schur(q0,h,F(1))
   self.assertEqual(a,F(3,2)+1/(q0+delta*g+h))
   self.assertEqual((1/(a-F(3,2))-1/(b-F(3,2)))/delta,g)
 def test_exact_hankel_recurrence_and_prony_dimension(self):
  atoms=[(F(3,4),F(1,10)),(F(1,4),F(1,12)),(-F(1,2),F(1,15))];g=[moment(atoms,k)for k in range(20)]
  h=[[g[i+j]for j in range(3)]for i in range(3)]
  self.assertEqual(det(h),F(1,8192));alpha=mv(inv(h),g[3:6]);self.assertEqual(alpha,[-F(3,32),F(5,16),F(1,2)])
  for k in range(17):self.assertEqual(g[k+3],sum(alpha[j]*g[k+j]for j in range(3)))
  jac=[[x**k for x,w in atoms]+[F(k)*w*x**(k-1)if k else F(0)for x,w in atoms]for k in range(6)]
  self.assertEqual(abs(det(jac)),F(225,8388608))
 def test_reciprocal_error_and_hankel_outer_bound(self):
  eta=F(1,10**8)
  for z in[F(1,3),F(4,5),F(2)]:
   for e in[-eta,eta]:
    zhat=1/(1/z+e);self.assertLessEqual(abs(zhat-z),eta*z*z/(1-eta*z))
  g=[F(1,4),F(1,16),F(5,64),F(9,256),F(37,1024),F(89,4096)];h=[[g[i+j]for j in range(3)]for i in range(3)];hi=inv(h);a=mv(hi,g[3:]);delta=F(1,10**8);l=max(sum(abs(x)for x in row)for row in hi)
  bound=l*delta*(1+sum(abs(x)for x in a))/(1-3*delta*l)
  for mask in range(64):
   true=[x+(delta if mask>>i&1 else-delta)for i,x in enumerate(g)];at=mv(inv([[true[i+j]for j in range(3)]for i in range(3)]),true[3:])
   self.assertLessEqual(max(abs(x-y)for x,y in zip(at,a)),bound)
 def test_stable_negative_mode_not_positive_relaxation(self):
  atoms=[(F(3,4),F(1,10)),(F(1,4),F(1,12)),(-F(1,2),F(1,15))];g=[moment(atoms,k)for k in range(6)]
  self.assertGreater(g[2],g[1]);p=[F(3,16),-F(1),F(1)]
  self.assertEqual(sum(p[i]*p[j]*g[i+j+1]for i in range(3)for j in range(3)),-F(15,512))
 def test_principal_measures_and_signed_task_counterexample(self):
  lo=[(F(0),F(1,4)),(F(1,2),F(3,4))];hi=[(F(1,4),F(3,4)),(F(3,4),F(1,4))]
  for k,m in enumerate([F(1),F(3,8),F(3,16)]):self.assertEqual(moment(lo,k),m);self.assertEqual(moment(hi,k),m)
  self.assertEqual(sum(w/(1-x)for x,w in lo),F(7,4));self.assertEqual(sum(w/(1-x)for x,w in hi),F(2))
  task=lambda a:moment(a,3)-F(2,3)*moment(a,4)
  self.assertEqual(task(lo),F(1,16));self.assertEqual(task(hi),F(1,16))
  lower=[(F(0),F(1,6)),(F(3,8),F(2,3)),(F(3,4),F(1,6))];self.assertEqual(task(lower),F(63,1024))
  upper=[F(1),F(3,8)]
  for k in range(2,5):upper.append(F(3,4)*upper[-1]-F(3,32)*upper[-2])
  self.assertEqual(upper[2],F(3,16));self.assertEqual(upper[3],F(27,256));self.assertEqual(upper[3]-F(2,3)*upper[4],F(33,512))
 def test_exact_signed_duals_and_no_value_next_moment(self):
  f=[F(0),0,0,F(1),-F(2,3)]
  low=padd(f,pscale(pmul(pmul([0,1],pmul([-F(3,8),1],[-F(3,8),1])),[-F(3,4),1]),F(2,3)))
  up=padd(f,pscale(pmul([F(3,32),-F(3,4),1],[F(3,32),-F(3,4),1]),F(2,3)))
  self.assertEqual(low[3:],[0,0]);self.assertEqual(up[3:],[0,0]);m=[F(1),F(3,8),F(3,16)]
  self.assertEqual(sum(a*b for a,b in zip(low,m)),F(63,1024));self.assertEqual(sum(a*b for a,b in zip(up,m)),F(33,512))
  atoms=[(F(0),F(1,6)),(F(3,8),F(2,3)),(F(3,4),F(1,6))];self.assertEqual(moment(atoms,3),F(27,256))
 def test_exact_flat_hankel_not_noisy_rank(self):
  atoms=[(F(1,8),F(1,5)),(F(3,8),F(1,3)),(F(5,8),F(7,15))];g=[moment(atoms,k)for k in range(7)]
  self.assertGreater(det([[g[i+j]for j in range(3)]for i in range(3)]),0);self.assertEqual(det([[g[i+j]for j in range(4)]for i in range(4)]),0)
  e=F(1,10**8);other=[(x,(1-e)*w)for x,w in atoms]+[(F(7,8),e)];gn=[moment(other,k)for k in range(7)]
  self.assertTrue(all(abs(a-b)<=e for a,b in zip(g,gn)));self.assertGreater(det([[gn[i+j]for j in range(4)]for i in range(4)]),0)
 def test_positive_interior_slow_spike_preserves_all_acquired_moments(self):
  a=F(3,4);d=3;g=[[a**(i+j+1)/F(i+j+1)for j in range(d+1)]for i in range(d+1)];gi=inv(g);c=sum(a**i*sum(abs(x)for x in gi[i])for i in range(d+1));eta=(1/a)/(4*c)
  for b in[F(7,8),F(99,100),1-F(1,10**20)]:
   coeff=mv(gi,[b**i for i in range(d+1)])
   self.assertLessEqual(sum(abs(x)*a**i for i,x in enumerate(coeff)),c)
   for k in range(d+1):
    phi=sum(coeff[i]*a**(i+k+1)/F(i+k+1)for i in range(d+1));self.assertEqual(phi,b**k)
    before=a**k/F(k+1);after=before-eta*phi+eta*b**k;self.assertEqual(before,after)
  self.assertGreater(eta/F(1,10**20),10**8)
 def test_same_four_moments_unbounded_dc_and_band_mass(self):
  m=[F(1),F(3,8),F(3,16),F(27,256)]
  for b in[F(7,8),F(31,32),F(255,256),1-F(1,10**8)]:
   a=(m[3]-b*m[2])/(m[2]-b*m[1]);wa=(b*m[1]-m[2])/(a*(b-a));wb=(m[2]-a*m[1])/(b*(b-a));w0=1-wa-wb
   self.assertTrue(0<a<b<1);self.assertTrue(min(wa,wb,w0)>0);atoms=[(F(0),w0),(a,wa),(b,wb)]
   self.assertEqual([moment(atoms,k)for k in range(4)],m);self.assertLessEqual(wb,F(6,77))
  self.assertGreater(wb/(1-b),10**6)
 def test_christoffel_bound_needs_legal_support_for_sharpness(self):
  m=[F(1),F(3,8),F(3,16)];b=m[1];v=[1,b];g=[[m[0],m[1]],[m[1],m[2]]];den=sum(x*y for x,y in zip(v,mv(inv(g),v)))
  self.assertEqual(1/den,1)
  witness=[(F(0),F(1,8)),(b,F(4,5)),(F(1),F(3,40))];self.assertEqual([moment(witness,k)for k in range(3)],m)
  variance=m[2]-b*b;self.assertEqual(1-variance/(b*(1-b)),F(4,5))
  for end in[F(7,8),F(99,100),F(999,1000)]:
   wb=(end-F(1,2))/(end-b);wc=b*(1-wb)/end;w0=1-wb-wc
   self.assertEqual([moment([(0,w0),(b,wb),(end,wc)],k)for k in range(3)],m);self.assertLess(wb,F(4,5))
 def test_total_band_global_dual_and_matching_source(self):
  b=F(7,8);a=F(5,12);q=[0,F(800,847),-F(3840,847),F(4608,847)]
  self.assertEqual(poly(q,b),1);self.assertEqual(poly(q,a),0);self.assertEqual(poly(q,0),0)
  atoms=[(F(0),F(13,70)),(a,F(81,110)),(b,F(6,77))];m=[F(1),F(3,8),F(3,16),F(27,256)]
  self.assertEqual([moment(atoms,k)for k in range(4)],m);self.assertEqual(sum(x*y for x,y in zip(q,m)),F(6,77))
  self.assertEqual(sum(abs(x)for x in q),F(9248,847))
 def test_two_nonnegative_histories_measure_the_signed_functional(self):
  atoms=[(F(0),F(1,4)),(F(1,2),F(3,4))];beta=F(1,10);plus={3:beta};minus={4:F(2,3)*beta};baseline=F(7,5)
  zp=baseline+sum(u*moment(atoms,k)for k,u in plus.items());zm=baseline+sum(u*moment(atoms,k)for k,u in minus.items())
  rp=F(3,2)+1/zp;rm=F(3,2)+1/zm
  self.assertEqual((1/(rp-F(3,2))-1/(rm-F(3,2)))/beta,moment(atoms,3)-F(2,3)*moment(atoms,4))
  self.assertLessEqual(sum(plus.values())+sum(minus.values()),F(1,5))
 def test_three_level_query_affine_drift_and_signed_cancellation(self):
  delta=F(1,5);a=delta/8;edges={(0,1):F(1,8),(2,3):F(1,6)}
  def z(level,time):return F(7,5)+F(time,10000)+sum(F(i+1,30)*a*level for i in range(4))+sum(w*(a*level)**2 for w in edges.values())
  q=(z(2,2)-2*z(1,1)+z(0,0))/(2*a*a);self.assertEqual(q,sum(edges.values()));self.assertEqual(2*a*4,delta)
  self.assertEqual(F(1,8)-F(1,8),0)
 def test_four_corner_quotient_and_session_drift(self):
  anchor=F(1,20);w=F(1,10);beta=F(1,8);gamma=F(5,8)
  def z(x,y,v,time):return 1/(1+v)+x*x/(1+v)+y**3*(2+v)+x*y*(beta+gamma*v)+F(time,10000)
  h=(z(anchor,anchor,w,0)-z(anchor,0,w,1)-z(0,anchor,w,2)+z(0,0,w,3))/(anchor*anchor)
  self.assertEqual(h,beta+gamma*w);self.assertEqual(h,F(3,16));self.assertEqual(2*anchor+w,F(1,5))
 def test_matching_objective_is_not_arbitrary_graph(self):
  beta=F(1,5);delta=F(1,5);matching=beta*delta*delta/4;triangle=3*beta*(delta/3)**2
  self.assertEqual(matching,F(1,500));self.assertGreater(triangle,matching)
 def test_finite_amplitude_tests_do_not_prove_global_quotient(self):
  levels=[F(0),F(1,100),F(1,50),F(1,10)];new=F(1,17);p=[F(1)]
  for x in levels:p=pmul(p,[-x,1])
  p=pscale(p,1/poly(p,new));p=pmul(p,p)
  self.assertEqual(poly(p,new),1)
  for x in levels:self.assertEqual(poly(p,x),0)
 def test_noisy_finite_horizon_threshold_is_not_exact_old_moments(self):
  b=F(7,8);eps=F(1,10**10);dose=F(1,5);h=17
  for j in range(h+1):self.assertLessEqual((b+eps)**j-(b-eps)**j,2*j*eps)
  self.assertLess(2*dose*h*eps,2*F(1,10**8))
 def test_fresh_grid_guard_has_a_degree_promise(self):
  grid=[F(i,25)for i in range(-5,6)];p=[F(1)]
  for x in grid:p=pmul(p,[-x,1])
  for x in grid:self.assertEqual(poly(p,x),0)
  self.assertNotEqual(poly(p,F(1,50)),0);self.assertEqual(F(3,11)**8,F(6561,214358881))


class CausalSpectralCurrentRoutes(unittest.TestCase):
 def test_acceptance_and_distinct_report_notices(self):
  from knowledge.retrieve import Library
  l=Library()
  for name in ['N1068','N1069','N1070','N1071','U1069-positive-interior-slow-spike-and-dc']:
   r=l.resolve(name);p=l.packet([name])['packets'][0];self.assertEqual(len(p['review_overlays']),1)
   a=p['review_overlays'][0];self.assertEqual(a['decision'],'accepted_internally_verified')
   self.assertIn({'id':r['id'],'content_version':r['content_version']},a['subjects'])
   self.assertEqual(a['working_device'],'not established');self.assertTrue(a['remaining_gaps'])
  for name,marker in [('N1068','WIDTH-REPORTS'),('U1068-raw-noise-to-outer-causal-prediction','WIDTH-REPORTS'),('U1069-point-atom-christoffel-needs-support-witness','ATOM-SUPPORT'),('N1070','NOISY-EXACT-DATA'),('U1071-two-anchor-affine-interaction-quotient','FIXED-QUOTIENT')]:
   self.assertTrue(any(marker in n['notice_id']for n in l.packet([name])['packets'][0]['notices']))
 def test_actual_source_branches_and_labelled_constructions(self):
  from knowledge.retrieve import Library
  l=Library()
  cases=[('U1068-raw-noise-to-outer-causal-prediction','## 3. Precision-aware'),('U1068-fresh-degree-guard-not-physical-class-proof','## 6. Fresh guards'),('U1068-reset-free-fir-is-a-different-contract','## 7. Alternative physical'),('U1069-principal-spectra-for-a-function-class','## 2. Theorem'),('U1069-signed-task-dual-and-no-value-observation','## 3. The signed-task'),('U1069-flat-hankel-stopping-without-assumed-order','## 4. Finite-order'),('U1069-positive-interior-slow-spike-and-dc','CURATOR GENERAL CONSTRUCTION'),('U1069-point-atom-christoffel-needs-support-witness','CURATOR WITNESS'),('U1070-total-band-dual-and-four-moment-witness','## 2. Conditional exact slow-band'),('U1071-two-anchor-affine-interaction-quotient','## 3. Learning higher-order')]
  for name,phrase in cases:self.assertTrue(l.source(name)['text'].startswith(phrase),name)
 def test_actual_default_packets_keep_semantic_scope_and_budget(self):
  import json,subprocess,sys
  from pathlib import Path
  root=Path(__file__).resolve().parents[1]
  for name in ['N1068','N1069','N1070','N1071','U1050-noisy-joint-gain-and-precision-design']:
   p=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',name],cwd=root,capture_output=True)
   self.assertEqual(p.returncode,0,p.stderr.decode());self.assertLessEqual(len(p.stdout),32768)
   v=json.loads(p.stdout)['packets'][0];self.assertTrue(v['evidence']and v['source_excerpts']and v['review_overlays'])

if __name__=='__main__':unittest.main()
