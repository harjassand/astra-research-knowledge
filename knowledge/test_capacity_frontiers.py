"""Independent finite interface controls; no producer scientific modules."""
import unittest
from fractions import Fraction as F

def dot(a,b,w):return sum(x*y*z for x,y,z in zip(a,b,w))
def mv(A,v):return[sum(x*y for x,y in zip(row,v))for row in A]
def minus(a,b):return[x-y for x,y in zip(a,b)]
class CapacityFrontierControls(unittest.TestCase):
 def test_reversible_full_residual_and_exit_factor(self):
  H=[[2,-2,0],[-1,2,-1],[0,-2,2]];w=[1,2,1];u=[F(1),F(0),F(-1)];y=[x/3 for x in u];hy=mv(H,y);r=minus(u,hy);L=2*dot(u,y,w)-dot(y,hy,w);I=F(1);self.assertEqual(L,F(8,9));self.assertEqual(L+dot(r,r,w)/2,I);self.assertEqual(1/(2*I),F(1,2))
 def test_projected_residual_misses_neighbors(self):
  H=[[2,-2,0],[-1,2,-1],[0,-2,2]];y=[F(1),0,0];hy=mv(H,y);self.assertNotEqual(hy[1],0);self.assertGreater(dot(hy,hy,[1,2,1]),hy[0]**2)
 def test_predecessor_rate_is_not_forward_scatter(self):
  H=[[2,-2,0],[-1,2,-1],[0,-2,2]];e=[F(1),0,0];self.assertEqual(mv(H,e),[2,-1,0]);self.assertNotEqual(mv(H,e),H[0])
 def test_irreversible_one_sided_failure_and_dual_radius(self):
  H=[[3,-2,-1],[-1,3,-2],[-2,-1,3]];u=[F(1),F(0),F(-1)];y=[3*x/14 for x in u];adj=list(map(list,zip(*H)));r=minus(u,mv(H,y));s=minus(u,mv(adj,y));ihat=dot(u,y,[1]*3)+dot(y,r,[1]*3);I=F(3,7);self.assertEqual(ihat,F(87,196));self.assertGreater(ihat,I);self.assertEqual(dot(r,r,[1]*3),F(1,14));self.assertEqual(dot(s,s,[1]*3),F(1,14));radius=F(1,63);self.assertLessEqual(abs(I-ihat),radius)
 def test_nonreversible_cross_terms_cannot_merge(self):
  P=[[F(1,2),F(1,3),F(1,6)],[F(1,6),F(1,2),F(1,3)],[F(1,3),F(1,6),F(1,2)]];self.assertNotEqual(P[0][2],P[2][0]);self.assertNotEqual(P[0][0]+P[2][2]-P[0][2]-P[2][0],P[0][0]+P[2][2]-2*P[2][0])
 def test_twoD_product_and_count_obstructions(self):
  theta,kappa=F(1,4),F(9,8);self.assertEqual(theta**2*kappa/theta**2,F(9,8));self.assertNotEqual(2/(1+theta*kappa),2/(1+theta));ps=[F(9**k,4*8**k+9**k)for k in range(5)];g=1-4*max(ps[k+1]-ps[k]for k in range(4));self.assertEqual(g,F(57746297,63718265))
 def test_same_path_auxiliary_and_target_have_different_sign(self):
  t=F(2);aux=F(1409,5040)*t*t-F(73,840)*t**4;target=6*t*t+F(33,2)*t**4;self.assertEqual(aux,F(-49,180));self.assertEqual(target,288)
 def test_cartan_error_and_sos_thresholds(self):
  for n in range(1,6):
   k=16*9**n;self.assertEqual(F(16*3**n,k)*F(3,2)**n,F(1,2)**n)
  t=F(1,2);self.assertEqual(max(0,t-F(1,2)),0);self.assertEqual(max(0,(3*t-1)/4),F(1,8));self.assertEqual(max(0,2*(3*t-1)/7),F(1,7))
 def test_finite_channel_degradation_and_upper(self):
  L=[[F(298,300)if i==j else F(1,300)for j in range(3)]for i in range(3)];T=[[F(1,297)if i==j else F(148,297)for j in range(3)]for i in range(3)];P=[[F((j+1)%3==i)for j in range(3)]for i in range(3)];C=[[F(99,100)*T[i][j]+F(1,100)*P[i][j]for j in range(3)]for i in range(3)];K=[[sum(C[i][k]*L[k][j]for k in range(3))for j in range(3)]for i in range(3)];self.assertEqual(K[0],[F(199,30000),F(14752,30000),F(15049,30000)]);self.assertEqual(F(99,100)*F(2401,4917)+F(1,100),F(1838,3725))

class CapacityFrontierCurrent(unittest.TestCase):
 def test_accepted_units_do_not_audit_unreviewed_parent(self):
  from knowledge.retrieve import Library
  l=Library();r=l.resolve('N405');self.assertEqual(r['content_version'],'0412b02fc627929c16d96aaf0badda72b565e1da76a5258495498efb26a7d2f2');self.assertFalse(r['review_overlays'])
  for name in ['U1088-finite-positive-equal-reference-gap','U1088-known-state-signal-copy-sufficiency','N1084','N1085','N1086','N1087']:
   r=l.resolve(name);a=l.packet([name])['packets'][0]['review_overlays'][0];self.assertEqual(a['decision'],'accepted_internally_verified');self.assertIn({'id':r['id'],'content_version':r['content_version']},a['subjects'])
   self.assertEqual(a['working_device'],'not established')
 def test_actual_exit_rate_and_reciprocal_endpoints(self):
  import json
  from knowledge.retrieve import Library
  l=Library()
  def rat(x):
   return F(int(x['num_hex'],16),int(x['den_hex'],16)) if 'num_hex'in x else F(int(x['numerator']),int(x['denominator']))
  for name,ending in [('N1086','M64_CANDIDATE.json'),('N1086','nonproduct_capacity_review_20261027/REPLAY.json'),('N1087','REPLAY_N64.json')]:
   e=next(e for e in l.resolve(name)['evidence']if e['path'].endswith('/'+ending));j=json.loads((l.root/e['path']).read_text());rho,rate=rat(j['rho']),rat(j['R_a']);self.assertEqual(rat(j['p_lower']),rho/(rate*rat(j['I_upper'])));self.assertEqual(rat(j['p_upper']),rho/(rate*rat(j['I_lower'])));self.assertGreater(rat(j['I_lower']),0)
 def test_actual_proof_and_accepted_code_bindings(self):
  from knowledge.retrieve import Library
  import hashlib
  l=Library()
  for name,ending,code,ph,ch in [('N1086','direct_variational/PROOF.md','sparse_galerkin.py','454a1c60727b93e6218c000e5fccab3347e0254449eac6ed11112ef3477ae09d','f2810b19726af9ce6c10a44a83072fdebc16a839784c6f02abebaece7ce9a550'),('N1086','nonproduct_capacity_operation_20261027/PROOF.md','nonproduct_certificate.py','2dbb7513a052d8804ebb97a93eee255957a4b14d39ab206eb0a9640239033cef','c586b0eb864e2495cd0abbc1321f19c7794c4c8a2160070876db7a5632ecf83a'),('N1087','nonreversible_capacity_operation_20261027/PROOF.md','nonreversible.py','597c392ef67d422c91463715660ab729330b794c3190cadd4bd2beae584ed1d0','e801240cf46286879d48ca384eaa12178fb31f98054aef106717946a41478a90')]:
   e=next(e for e in l.resolve(name)['evidence']if e['path'].endswith(ending));p=l.root/e['path'];self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),ph);self.assertEqual(hashlib.sha256((p.parent/code).read_bytes()).hexdigest(),ch)
 def test_actual_sources_and_failure_notices(self):
  from knowledge.retrieve import Library
  l=Library()
  for name,phrase in [('U1088-finite-positive-equal-reference-gap','Concrete ordinary construction'),('U1084-coherent-filter-fixed-output','Bob'),('U1085-convergent-cartan-no-finite-psd-stop','no finite Cartan degree'),('U1086-nonproduct-twoD-source-contract','lumpability'),('U1087-two-sided-primal-dual-residual','87/196')]:self.assertIn(phrase.lower(),l.source(name)['text'].lower())
  self.assertIn('ONE-SIDED-FAILURE',str(l.packet(['U1087-two-sided-primal-dual-residual'])['packets'][0]['notices']))
 def test_same_source_compatibility_and_model_mismatch(self):
  from knowledge.retrieve import Library
  l=Library()
  for fr,to,state in [('U1086-nonproduct-twoD-source-contract','U1086-reversible-full-residual-to-exit-law','ESTABLISHED COMPATIBLE INTERFACE'),('U1086-reversible-full-residual-to-exit-law','U1087-two-sided-primal-dual-residual','REFUTED TRANSFER'),('U1086-nonproduct-twoD-source-contract','U1087-two-sided-primal-dual-residual','INCOMPATIBLE ASSUMPTIONS'),('U1085-free-sos-not-constrained-positivity','U1084-coherent-filter-fixed-output','CANDIDATE CONNECTION')]:self.assertEqual(l.bridge(fr,to)['transfers'][0]['state'],state)

if __name__=='__main__':unittest.main()
