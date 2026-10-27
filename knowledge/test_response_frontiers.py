"""Independent small exact interface controls, no producer imports."""
import unittest
from fractions import Fraction as F

def inv(a):
 n=len(a);m=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
 for i in range(n):
  k=next(k for k in range(i,n) if m[k][i]);m[i],m[k]=m[k],m[i];p=m[i][i];m[i]=[x/p for x in m[i]]
  for j in range(n):
   if j!=i:
    p=m[j][i];m[j]=[x-p*y for x,y in zip(m[j],m[i])]
 return [row[n:] for row in m]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def z(u,vs):
 n=len(vs[0]);a=[[F(i==j)+sum(t*v[i]*v[j] for t,v in zip(u,vs)) for j in range(n)]for i in range(n)];return inv(a)[0][0]
class ResponseFrontierControls(unittest.TestCase):
 def test_semiconvex_bound(self):
  a,b,M=F(-2),F(3),F(4)
  f=lambda x:x**4-M*x*x/2
  for k in range(21):
   x=a+(b-a)*k/20;upper=((b-x)*f(a)+(x-a)*f(b))/(b-a)+M*(x-a)*(b-x)/2;self.assertLessEqual(f(x),upper)
 def test_midpoint_noise_constant(self):
  for k in range(101):
   x=F(k,100);weights=[2*(x-F(1,2))*(x-1),4*x*(1-x),2*x*(x-F(1,2))];self.assertEqual(sum(weights),1);self.assertLessEqual(sum(map(abs,weights)),F(5,4))
 def test_axial_probes_do_not_find_mixed_quadratic(self):
  f=lambda x,y:3*x*y
  self.assertTrue(all(f(t,0)==f(0,t)==0 for t in range(20)));self.assertEqual(f(1,1),3)
 def test_singleton_and_signed_pair(self):
  vs=[[F(1),F(2)],[F(1),F(-1)]];P=[F(1),F(1)];T=[[dot(a,b)for b in vs]for a in vs]
  self.assertLess(T[0][1],0)
  for i in range(2):
   t,s=F(1,20),F(1,10);ls=[1-z([d if j==i else 0 for j in range(2)],vs)for d in[t,s]]
   pi=(1/t-1/s)/(1/ls[0]-1/ls[1]);tii=1/ls[0]-1/(t*pi);self.assertEqual(pi,P[i]);self.assertEqual(tii,T[i][i])
  u,v=F(1,20),F(1,20);A=T[0][0]+1/u;B=T[1][1]+1/v;t=T[0][1];ell=(A+B-2*t)/(A*B-t*t);self.assertEqual(ell,1-z([u,v],vs))
  for a in range(-5,5):
   x,y=F(a,2),F(a+1,2);self.assertGreater((A+B-2*x)/(A*B-x*x),(A+B-2*y)/(A*B-y*y))
 def test_compact_centered_formula(self):
  vs=[[F(1),F(2)],[F(1),F(-1)],[F(2),F(3)]];ss=[F(2),F(-1),F(3,2)];P=[1,1,4];W=F(4);cs=[2*s for s in ss]
  for ds in[[F(1,40)]*3,[0,F(1,30),F(1,50)],[-F(1,40),F(1,40),0]]:
   d=[x*p for x,p in zip(ds,P)];q=dot(d,cs);H=W+dot(d,[c*c for c in cs]);pred=1/(1+sum(d)-q*q/H);self.assertEqual(pred,z(ds,vs))
 def test_dark_joint_and_shift(self):
  vs=[[F(0),F(1)],[F(1),F(1)]];t=F(1,10);self.assertEqual(z([t,0],vs),1);self.assertNotEqual(z([t,t],vs),z([0,t],vs))
  ref=[F(1,40),F(1,40)];a=inv([[F(i==j)+sum(u*v[i]*v[j]for u,v in zip(ref,vs))for j in range(2)]for i in range(2)]);self.assertNotEqual(a[0][1],0)
 def test_exact_rank_is_not_noise_robust(self):
  S=[[F(1),F(2)],[F(2),F(4)]];self.assertEqual(S[1][1]-S[0][1]**2/S[0][0],0);S[0][1]+=F(1,10**8);self.assertLess(S[1][1]-S[0][1]**2/S[0][0],0)
 def test_escape_backward_equations(self):
  u,v,b,c=map(F,[2,3,4,5]);single=(b+c)/(u*c)+1/c;T2=single+1/(2*u)+v*(b+c)/(2*u*u*c);T1=T2-1/(2*u);TU=(1+b*T1)/(b+c)
  self.assertEqual(2*u*(T2-T1),1);self.assertEqual(u*(T1-TU)+v*(T1-T2),1);self.assertEqual(c*TU+b*(TU-T1),1)
 def test_retry_product_and_downstream_first_derivative(self):
  p,w,delta,qchi=F(3,5),F(1,1000),F(1,10000),F(1,1000)
  for m in range(5):
   a=(1-delta)*(1-qchi)**m;r=(1-p-w)*a;s=p*a/(1-r);self.assertEqual(s,p*a+r*s)
  L=7;self.assertEqual(sum(F(m,1)/p for m in range(L)),F(L*(L-1),2)/p)
 def test_identical_second_key_cancels_selectivity(self):
  kc,kw,key=F(13),F(2),F(99);self.assertEqual(kc/kw,(kc*key)/(kw*key))

class ResponseFrontierCurrent(unittest.TestCase):
 def test_version_scoped_acceptance(self):
  from knowledge.retrieve import Library
  l=Library()
  for name in ['N1081','N1082','N1083']:
   r=l.resolve(name);p=l.packet([name])['packets'][0];a=p['review_overlays'][0]
   self.assertEqual(a['decision'],'accepted_internally_verified');self.assertIn({'id':r['id'],'content_version':r['content_version']},a['subjects']);self.assertEqual(a['working_device'],'not established')
 def test_real_governing_source(self):
  from knowledge.retrieve import Library
  l=Library()
  for name,phrase in [('U1081-semiconvex-and-quadratic-envelope','New mathematical construction'),('U1082-exact-singleton-pair-quotient','without assuming the interaction sign'),('U1082-dark-reference-signed-deployment','measure zero'),('U1083-fresh-retry-downstream-exposure','fresh')]:
   self.assertIn(phrase.lower(),l.source(name)['text'].lower())
 def test_corrections_and_incompatible_contracts(self):
  from knowledge.retrieve import Library
  l=Library();p=l.packet(['U1083-product-frontier-not-static-authentication'])['packets'][0];self.assertIn('FUTURE-ADDRESS',str(p['notices']))
  for fr,to,state in [('U1082-affine-physical-regularity-and-prototype-tube','U1081-semiconvex-and-quadratic-envelope','ESTABLISHED COMPATIBLE INTERFACE'),('U1082-adaptive-psd-span-and-response','U1082-noise-rejects-exact-rank-not-source','INCOMPATIBLE ASSUMPTIONS'),('U1083-escape-needs-physical-removal','U1083-product-frontier-not-static-authentication','REFUTED TRANSFER')]:
   self.assertEqual(l.bridge(fr,to)['transfers'][0]['state'],state)

if __name__=='__main__':unittest.main()
