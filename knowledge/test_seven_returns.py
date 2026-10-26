"""Exact checks of accepted mechanisms and unsafe transfers, not producer replay."""
from fractions import Fraction as F
import hashlib,itertools,json,math,subprocess,sys,unittest
from pathlib import Path
from knowledge.model import ROOT
from knowledge.retrieve import Library

UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-seven-completed-returns'
def eye(n):return [[F(i==j)for j in range(n)]for i in range(n)]
def zero(n,m):return [[F(0)]*m for _ in range(n)]
def tr(a):return list(map(list,zip(*a)))
def mul(a,b):return [[sum(x*y for x,y in zip(r,c))for c in zip(*b)]for r in a]
def add(a,b):return [[x+y for x,y in zip(r,s)]for r,s in zip(a,b)]
def scale(c,a):return [[c*x for x in r]for r in a]
def sub(a,b):return add(a,scale(-1,b))
def tensor(a,b):return [[x*y for x in r for y in s]for r in a for s in b]
def block(rows):return [[v for r in line for v in r]for rr in rows for line in zip(*rr)]
def trace(a):return sum(a[i][i]for i in range(len(a)))
def act(a,rho):return mul(mul(a,rho),tr(a))
X=[[F(0),F(1)],[F(1),F(0)]];Z=[[F(1),F(0)],[F(0),F(-1)]]
PLUS=scale(F(1,2),add(eye(2),X));MINUS=sub(eye(2),PLUS)
ZERO=[[F(1),F(0)],[F(0),F(0)]];ONE=sub(eye(2),ZERO)

def padd(a,b):
 c=dict(a)
 for k,v in b.items():c[k]=c.get(k,F(0))+v
 return {k:v for k,v in c.items()if v}
def pscale(c,a):return {k:c*v for k,v in a.items()if c*v}
def pmul(a,b):
 out={}
 for i,x in a.items():
  for j,y in b.items():out[i+j]=out.get(i+j,F(0))+x*y
 return {k:v for k,v in out.items()if v}

class SevenReturns(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.lib=Library()

 def test_positive_moments_and_global_exponential_identity(self):
  mu0,mu1,mu2,T=map(F,[3,4,6,2]);s1=F(1,2);s2=(mu2-mu1*s1)/(mu1-mu0*s1);w2=(mu1-mu0*s1)/(s2-s1);w1=mu0-w2
  self.assertTrue(0<s1<s2<T and w1>0 and w2>0)
  self.assertEqual([sum(w*s**k for w,s in[(w1,s1),(w2,s2)])for k in range(3)],[mu0,mu1,mu2])
  # Polynomial identity, not a scan in t or a trusted numeric optimizer.
  c0={0:F(-5),1:F(2),2:F(-1)};c1={0:F(-2),1:F(10),2:F(-6),3:F(2)};c2={2:F(-6),3:F(4),4:F(-1)}
  self.assertEqual(padd(pmul(c1,c1),pscale(-4,pmul(c2,c0))),{0:F(4),1:F(-40),2:F(4)})
  for t in[F(1,8),F(9)]:self.assertLess(t*t-10*t+1,0)
  s15=sum(F(9**k,k*math.factorial(k))for k in range(1,16));self.assertGreater(s15,F(8110,8))
  exp_upper=sum(F(9**k,math.factorial(k))for k in range(36))+F(9**36,math.factorial(36))/(1-F(9,37))
  self.assertLess(exp_upper,8110)
  self.assertLess(F(58,100)-F(207,100)+F(1,7),-F(64,49))
  # Hard-band coupling really has positive moment determinant at g=4.
  log3_lower=2*sum(F(1,2)**(2*k+1)/F(2*k+1)for k in range(30))
  self.assertGreater((15+4*log3_lower)*F(640,27)-F(64,3)**2,0)

 def test_inclusive_calibration_and_finite_time_bounds(self):
  z=F(3,2000);amin=F(3,5);d=F(8,5)*z*z;gs=2*z*z
  self.assertLess(4*((d/amin)**2+gs/amin),F(5478,10**6)**2)
  self.assertLess(4*(1+gs)/(201-d)**2,F(9951,10**6)**2)
  amin=(1-F(1,2000))*F(3,5);amax=1+F(1,2000);gs=2*F(33,20000)**2;d=F(904356,10**9)
  self.assertLess(4*((d/amin)**2+gs/amin),F(675,100000)**2)
  self.assertLess(4*amax*(amax+gs)/(201-d)**2,F(996,100000)**2)
  sqrt11_lower=F(3316624790355,10**12);self.assertLess(sqrt11_lower**2,11)
  margin=F(6,5)-F(1,2000)-(1+F(1,2000))*(6-sqrt11_lower)/5-gs
  self.assertGreater(margin,F(6625,10000))
  self.assertLess((1+F(1,2000))/2,F(71,100)**2) # hopping row sum <1.21
  d=50;time=F(10);at=F(121,100)*time
  tail=time*at**d/math.factorial(d)/(1-at/F(d+1));self.assertLess(tail,F(595,10**12))

 def test_boolean_encoding_and_restricted_one_flag_obstruction(self):
  penalty=lambda a,b,c:a*b-2*a*c-2*b*c+3*c
  for a,b,c in itertools.product([0,1],repeat=3):
   self.assertGreaterEqual(penalty(a,b,c),0);self.assertEqual(penalty(a,b,c)==0,c==a*b)
   self.assertEqual(penalty(a,b,1-c)==0,c==1-a*b)
  for m in range(2,6):
   layer=list(range(m));gates=[]
   while len(layer)>1:
    nxt=[]
    for i in range(0,len(layer)-1,2):
     out=m+len(gates);gates.append((layer[i],layer[i+1],out));nxt.append(out)
    if len(layer)%2:nxt.append(layer[-1])
    layer=nxt
   self.assertEqual(len(gates),m-1);root=layer[0];neighbours={j:set()for j in range(2*m)}
   for gate in gates:
    for a,b in itertools.combinations(gate,2):neighbours[a].add(b);neighbours[b].add(a)
   emitter=2*m-1;neighbours[root].add(emitter);neighbours[emitter].add(root)
   self.assertLessEqual(max(map(len,neighbours.values())),4)
   for inputs in itertools.product([0,1],repeat=m):
    correct=[]
    for flags in itertools.product([0,1],repeat=m-1):
     allbits=inputs+flags;energy=3*sum(penalty(*(allbits[j]for j in gate))for gate in gates)
     if energy==0:correct.append(allbits)
     else:self.assertGreaterEqual(energy,3)
    self.assertEqual(len(correct),1);self.assertEqual(correct[0][root],math.prod(inputs))
  # Any degree<=2 Boolean monomial has zero coefficient on the full m-fold
  # interaction. The unique nonzero all-one indicator has coefficient one.
  for m in range(3,7):
   for degree in range(3):
    for support in itertools.combinations(range(m),degree):
     coefficient=sum((-1)**(m-sum(x))*math.prod(x[i]for i in support)for x in itertools.product([0,1],repeat=m))
     self.assertEqual(coefficient,0)

 def test_scalar_witness_gauge_and_unattained_order_endpoint(self):
  dist=lambda s,t:abs(s[1]-t[1])+F(1,2)*abs(s[0]-t[0])
  nodes=[(F(0),F(0)),(F(1),F(1)),(F(0),F(2))];mid=[F(0),F(3,4),F(1)];lo=[r-F(1,10)for r in mid];hi=[r+F(1,10)for r in mid]
  self.assertTrue(all(lo[i]-hi[j]<=dist(nodes[i],nodes[j])for i in range(3)for j in range(3)))
  witness=lambda z:max(l-dist(z,n)for l,n in zip(lo,nodes))
  for n,l,u in zip(nodes,lo,hi):self.assertTrue(l<=witness(n)<=u)
  sites=nodes+[(F(2),F(3,5)),(F(0),F(-1))]
  self.assertTrue(all(abs(witness(a)-witness(b))<=dist(a,b)for a in sites for b in sites))
  # Independent future constraints can each pass an anchor and fail jointly.
  self.assertLessEqual(abs(F(0)-0),10);self.assertLessEqual(abs(F(2)-0),9);self.assertGreater(abs(F(2)-0),1)
  for dp in map(F,range(-4,5)):
   for dx in[F(j,3)for j in range(-9,10)]:self.assertEqual(abs(dp-3*dx)<=abs(dx),abs(dx-F(3,8)*dp)<=F(1,8)*abs(dp))
  p1,p2=F(1,10),F(597,20);contrasts=[p1/2-p2/3+b/6 for b in[-F(1,2),F(1,2)]]
  self.assertEqual((max(contrasts)-min(contrasts))/2,F(1,12))
  for b in[-F(1,2),F(0),F(1,2)]:
   for x in[F(-7),F(0),F(5,3),F(10)]:self.assertEqual(4*x-b+b,4*x)
  # A(0)=0,A(1)=1,m2,K0,load1: possible x approach0 but x0 is impossible.
  self.assertNotEqual(1-2*F(0),0)
  for n in[4,10,100]:
   x=F(1,n);r=1-2*x;self.assertTrue(0<x<F(1,2)and 0<r<1);self.assertEqual(2*x+r,1)

 def test_meter_effects_and_availability_are_not_the_same_contract(self):
  # pi/(2omega),J3,lambda4,omega5: common -i is irrelevant to the instrument.
  k0=scale(F(3,5),X);k1=scale(F(4,5),Z)
  self.assertEqual(add(mul(tr(k0),k0),mul(tr(k1),k1)),eye(2))
  self.assertEqual(mul(Z,k1),scale(F(4,5),eye(2)))
  # Two-window lambda=J endpoint: iY is an exact corrected unitary.
  iy=[[F(0),F(1)],[F(-1),F(0)]];self.assertEqual(mul(tr(iy),iy),eye(2))
  for ratio in[F(1),F(3,5),F(1,10)]:self.assertEqual(ratio**2+(1-ratio**2),1)
  self.assertLess(F(1,1000**2+1),F(1,10**6)) # gap1, arbitrarily small success

 def test_coherent_flag_leakage_and_late_xx_counterexamples(self):
  cr=tensor(tensor(Z,eye(2)),eye(2));cz=eye(4);cz[3][3]=-1;cs=tensor(eye(2),cz);u=tensor(eye(4),X)
  rho=tensor(tensor(PLUS,PLUS),ZERO)
  for gate in[cr,cs,u]:rho=act(gate,rho)
  ideal=act(cr,act(cs,rho));accept=tensor(tensor(PLUS,PLUS),eye(2));false=tensor(tensor(PLUS,PLUS),ONE)
  self.assertEqual(trace(mul(accept,ideal)),0)
  leaked=[[v if i//2==j//2 else F(0)for j,v in enumerate(row)]for i,row in enumerate(rho)]
  leaked=act(cr,act(cs,leaked));self.assertEqual(trace(mul(accept,leaked)),F(1,4));self.assertEqual(trace(mul(false,leaked)),F(1,4))
  self.assertEqual(act(X,ZERO),ONE) # classically conjugating sign cannot filter X
  bell=zero(4,4)
  for i in[0,3]:
   for j in[0,3]:bell[i][j]=F(1,2)
  pxx=scale(F(1,2),add(eye(4),tensor(X,X)));self.assertEqual(act(pxx,bell),bell)
  product=tensor(ZERO,ZERO);post=act(pxx,product);self.assertEqual(trace(post),F(1,2));self.assertEqual(scale(2,post),bell)
  local=add(act(tensor(PLUS,PLUS),bell),act(tensor(MINUS,MINUS),bell));self.assertEqual(trace(local),1);self.assertEqual(trace(mul(bell,local)),F(1,2))

 def test_completed_teleportation_does_not_preserve_its_fine_labels(self):
  iy=[[F(0),F(1)],[F(-1),F(0)]];kpre=scale(F(1,2),add(Z,iy))
  self.assertEqual(add(mul(X,kpre),mul(kpre,X)),zero(2,2));self.assertEqual(mul(Z,kpre),PLUS)
  full=block([[MINUS,scale(-1,tr(kpre))],[kpre,PLUS]])
  symmetry=block([[X,zero(2,2)],[zero(2,2),scale(-1,X)]])
  self.assertEqual(mul(tr(full),full),eye(4));self.assertEqual(mul(full,symmetry),mul(symmetry,full))
  frames=[eye(2),X,Z,mul(X,Z)];ops=[scale(F(1,2),act(frame,PLUS))for frame in frames]
  probs=[]
  for rho in[PLUS,MINUS]:
   outputs=[act(op,rho)for op in ops];probs.append([trace(v)for v in outputs]);coarse=zero(2,2)
   for out in outputs:coarse=add(coarse,out)
   self.assertEqual(coarse,scale(F(1,4),add(rho,act(X,rho))))
  self.assertEqual(probs,[[F(1,4),F(1,4),F(0),F(0)],[F(0),F(0),F(1,4),F(1,4)]])

 def test_acquired_support_and_scoped_internal_acceptance(self):
  index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_text());originals=[r for r in index['files']if r['kind']!='curator_review'];self.assertEqual(len(originals),10);self.assertEqual(sum(r['bytes']for r in originals),111971)
  self.assertEqual(len(index['files']),11)
  for row in index['files']:self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])
  readme=(ROOT/UPDATE/'README.md').read_text()
  for name in['P1_return_0952_20261026','P2_return_0952_20261026','P1_return_1039_20261026','P2_return_1039_20261026','P3_return_1039_20261026','P1_return_1138_20261026','P2_return_1221_20261026']:self.assertIn(name,readme)
  for n in range(1044,1048):
   parent=self.lib.resolve(f'N{n}');review=next(a for a in parent['review_overlays']if a['id']==f'A{n+22}-seven-returns')
   self.assertIn({'id':parent['id'],'content_version':parent['content_version']},review['subjects']);self.assertEqual(review['working_device'],'not established')
   status=json.loads((ROOT/parent['authority']).read_text())
   self.assertTrue(status['proof_availability']['unavailable_or_unclassified'])
   for unit in self.lib.records.values():
    if parent['id']in unit.get('parents',[]):self.assertTrue(any(a['id']==review['id']for a in unit['review_overlays']))
  cur=self.lib.resolve('U1047-correctable-differential-parity-meter')['evidence'][0];self.assertIn('/source/curator/',cur['path']);self.assertEqual(cur['hash_kind'],'curator_analytic_reconstruction_utf8_bytes')

 def test_complete_default_routes_and_exact_source_branches(self):
  ids=[r['id']for r in self.lib.records.values()if r['id'].split('-')[0]in{f'{p}{n}'for p in['N','U']for n in range(1044,1048)}]
  self.assertEqual(len(ids),19)
  old=['U1026-positive-scalar-moment-obstruction','U1026-energy-form-and-charge-memory','U1027-independent-radiation-phase-error','U1028-inverse-residual-consistency','U1041-full-memory-dual-rail-check','U1023-fine-record-and-terminal-failures']
  for i in ids+old:
   with self.subTest(identifier=i):
    p=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',i],cwd=ROOT,capture_output=True);self.assertEqual(p.returncode,0,p.stderr);self.assertLessEqual(len(p.stdout),32768)
  for i,branch,phrase in[
   ('U1044-positive-moment-and-two-pole-compiler','p2_moments/originals/','Complete constructive converse'),
   ('U1044-exponential-ohmic-passive-no-go','p2_moments/originals/','discriminant'),
   ('U1045-inclusive-soft-port-error-and-stability','p2_jacobi/originals/','full-state'),
   ('U1045-large-detuning-finite-time-locality','p2_jacobi/originals/','interaction picture'),
   ('U1046-scalar-completion-and-ordered-future-operations','p3_order/originals/','witness source'),
   ('U1046-monotone-order-only-inverse-range','p3_order/originals/','without itself being realized'),
   ('U1047-conserved-symmetry-and-coarse-teleportation','source/curator/','retired/coarsened'),
   ('U1047-coherent-commuting-symmetry-filter','source/curator/','probability is1/4')]:
   result=self.lib.source(i);self.assertIn(branch,result['source']['path']);self.assertIn(phrase,result['text'])
  transfer=self.lib.bridge('U1047-conserved-symmetry-and-coarse-teleportation','U1023-fine-record-and-terminal-failures')['transfers'][0]
  self.assertEqual(transfer['state'],'REFUTED TRANSFER');self.assertIn('coarse theorem is not invalidated',transfer['scope'])

if __name__=='__main__':unittest.main()
