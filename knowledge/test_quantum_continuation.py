"""Independent curator controls; never an unavailable producer-program replay."""
import cmath,itertools,math,unittest
from fractions import Fraction as F

I=[[1,0],[0,1]];X=[[0,1],[1,0]];Y=[[0,-1j],[1j,0]];Z=[[1,0],[0,-1]]
P=[I,X,Y,Z];SQ=math.sqrt(2);W=complex(1,1)/SQ

def mm(a,b):return[[sum(x*y for x,y in zip(r,c))for c in zip(*b)]for r in a]
def adj(a):return[[complex(x).conjugate()for x in r]for r in zip(*a)]
def add(a,b,scale=1):return[[x+scale*y for x,y in zip(r,s)]for r,s in zip(a,b)]
def mul(a,s):return[[s*x for x in r]for r in a]
def kron(a,b):return[[x*y for x in r for y in t]for r in a for t in b]
def outer(v):return[[x*complex(y).conjugate()for y in v]for x in v]
def error(a,b):return max(abs(x-y)for r,s in zip(a,b)for x,y in zip(r,s))
def inverse(a):
 n=len(a);b=[[F(x)for x in r]+[F(i==j)for j in range(n)]for i,r in enumerate(a)]
 for j in range(n):
  k=next(i for i in range(j,n)if b[i][j]);b[j],b[k]=b[k],b[j];d=b[j][j];b[j]=[x/d for x in b[j]]
  for i in range(n):
   if i!=j:
    d=b[i][j];b[i]=[x-d*y for x,y in zip(b[i],b[j])]
 return[r[n:]for r in b]
def cp_error(a,b):
 o,n=len(a[0]),len(a[0][0]);worst=0
 for i,j in itertools.product(range(n),repeat=2):
  for u,v in itertools.product(range(o),repeat=2):
   x=sum(k[u][i]*complex(k[v][j]).conjugate()for k in a);y=sum(k[u][i]*complex(k[v][j]).conjugate()for k in b);worst=max(worst,abs(x-y))
 return worst

class QuantumControls(unittest.TestCase):
 def test_six_setting_integer_primal_dual(self):
  words=list(itertools.product(range(2),repeat=4));zero=(0,0,0,0)
  def axis(x,z):return 'Y'if x and z else'X'if x else'Z'if z else'I'
  def axes(q):
   x,z,a,b=q;return axis(x,z)+axis(a,b)+axis(x,z^a)+axis(a,b^x)
  def symp(a,b):return(a[0]*b[1]+a[1]*b[0]+a[2]*b[3]+a[3]*b[2])%2
  def detect(setting,error):return any(symp(error,q)and all(x=='I'or x==y for x,y in zip(axes(q),setting))for q in words)
  menus=['XYYX','XZXZ','YXXY','YZYZ','ZXZX','ZYZY']
  for q in words:
   if q!=zero:self.assertEqual(sum(detect(m,q)for m in menus),6 if q in[(1,0,1,0),(1,1,1,1)]else 4)
  dual=[(0,0,0,1),(0,1,0,0),(0,1,0,1)]
  for m in itertools.product('XYZ',repeat=4):self.assertLessEqual(sum(detect(m,q)for q in dual),2)
 def test_triangular_deferred_characters(self):
  words=list(itertools.product(range(4),repeat=3))
  def bits(k):return(k&1,k>>1)
  def bracket(a,b):return(a[0]*b[1]+a[1]*b[0])%2
  def cliff(i,p):return(p[1],p[0])if i!=1 else(p[0],p[1]^p[0])
  chars=[]
  for faults in words:
   vals=[]
   for mus in words:
    f=(0,0);phase=0
    for i,(s,m)in enumerate(zip(faults,mus)):
     u=bits(m);a=(u[0]^f[0],u[1]^f[1]);phase^=bracket(bits(s),a);f=cliff(i,a)
    vals.append(1 if phase==0 else-1)
   chars.append(vals)
  self.assertEqual(len({tuple(v)for v in chars}),64)
  for i in range(64):
   for j in range(64):self.assertEqual(sum(x*y for x,y in zip(chars[i],chars[j])),64 if i==j else 0)
 def test_magic_complete_channel_and_flagged_twirl(self):
  physical=[];virtual=[]
  for m in range(2):
   k=[[0j]*4 for _ in range(2)]
   for d,b in itertools.product(range(2),repeat=2):
    if b^d==m:k[d][2*d+b]=1j**(m*d)
   physical.append(kron(k,I))
  for s in range(2):
   a=[1/SQ,(-1)**s*W/SQ];k=[[0j]*4 for _ in range(2)]
   for d,b in itertools.product(range(2),repeat=2):k[d][2*d+b]=(-1)**(s*d)*W**d*a[b].conjugate()
   virtual.append(kron(k,I))
  self.assertLess(cp_error(physical,virtual),1e-12)
  c=mul(add(X,Y),1/SQ)
  for m in range(2):
   actual=[mul(mm(physical[m],kron(kron(I,p),I)),1/SQ)for p in[I,c]]
   expected=[mul(k,1/SQ)for k in virtual]
   self.assertLess(cp_error(actual,expected),1e-12)
 def test_magic_axis_records_and_five_setting_reconstruction(self):
  a=[1/SQ,W/SQ];z=[1/SQ,-W/SQ]
  def cross(effect):return sum(a[i].conjugate()*effect[i][j]*z[j]for i in range(2)for j in range(2))
  fx=mul(add(I,X,-1),F(1,2));fy=mul(add(I,Y,-1),F(1,2));self.assertGreater(abs(cross(fx)),.3);self.assertLess(abs(cross(add(fx,fy))),1e-14)
  target=[1/SQ,0,0,W/SQ];pi=outer(target);ident=kron(I,I);nu=1/(.5+SQ);f=(SQ-1)*nu/2
  obs=[kron(Z,Z),kron(X,X),kron(X,Y),kron(Y,X),mul(kron(Y,Y),-1)];weights=[nu/2]+[nu/(2*SQ)]*4
  self.assertAlmostEqual(sum(weights),1)
  effect=[[0j]*4 for _ in range(4)]
  for p,w in zip(obs,weights):effect=add(effect,mul(add(ident,p,-1),w/2))
  self.assertLess(error(effect,add(mul(ident,f),mul(add(ident,pi,-1),nu))),1e-14)
 def test_complete_weak_instrument_not_just_povm(self):
  eta=1/SQ;sp=math.sqrt((1+eta)/2);sn=math.sqrt((1-eta)/2);a=(sp+sn)/2;b=(sp-sn)/2;rx=mul(add(I,X,1j),1/SQ)
  actual=[];wrong=[]
  for sign in[1,-1]:
   m=add(mul(I,a),mul(X,sign*b));bad=mm(Z,m);feedback=I if sign==1 else Z
   self.assertLess(error(mm(adj(m),m),mm(adj(bad),bad)),1e-14)
   for r in range(2):
    reset=[[int(i==0 and j==r)for j in range(2)]for i in range(2)]
    actual.append(kron(mm(mm(rx,feedback),mm(m,reset)),I));wrong.append(mm(mm(rx,feedback),mm(bad,reset)))
  magic=[1/SQ,W/SQ];expected=[kron([[magic[i]*int(j==r)for j in range(2)]for i in range(2)],I)for r in range(2)]
  self.assertLess(cp_error(actual,expected),1e-12)
  output=[[0j]*2 for _ in range(2)]
  for k in wrong:output=add(output,outer([k[0][0],k[1][0]]))
  fidelity=sum(magic[i].conjugate()*output[i][j]*magic[j]for i in range(2)for j in range(2));self.assertAlmostEqual(fidelity.real,.5)
 def test_harmonic_cp_downdate_and_square_scope(self):
  h=[[F(1 if((i&j).bit_count()%2)==0 else-1)for j in range(4)]for i in range(4)]
  for p in[[F(26,100),F(24,100),F(1,4),F(1,4)],[F(4,10),F(3,10),F(2,10),F(1,10)]]:
   c=[[sum(p[k]*h[k][i]*h[k][j]for k in range(4))for j in range(4)]for i in range(4)];ci=inverse(c);alpha=F(16)/sum(1/x for x in p);self.assertEqual(1/ci[0][0],alpha);self.assertGreaterEqual(alpha,4*min(p))
   v=[ci[i][0]for i in range(4)];q=sum(v[i]*c[i][j]*v[j]for i in range(4)for j in range(4));self.assertEqual(q-alpha*v[0]**2,0);self.assertLess(q-(alpha+F(1,1000))*v[0]**2,0)
  # Four group keys but only two characters: missing keys need not kill the
  # selected two-sector filter. This is OUTSIDE the accepted square theorem.
  rows=[[1,1],[1,1],[1,-1],[1,-1]];p=[F(1,2),0,F(1,2),0];c=[[sum(p[k]*rows[k][i]*rows[k][j]for k in range(4))for j in range(2)]for i in range(2)];self.assertEqual(c,[[1,0],[0,1]])
 def test_harmonic_to_idle_flag_preserves_only_good_sector(self):
  p=[F(26,100),F(24,100),F(1,4),F(1,4)];alpha=16/sum(1/x for x in p);r=4*min(p);vt=F(4,5);n=10
  refined=n*(1-alpha)+alpha*vt*vt/n;old=n*(1-r)+r*vt*vt/n;self.assertLess(refined,old)
  theta=float(vt/n);bad=1-float(alpha)*math.cos(theta)**2;self.assertLessEqual(n*bad,float(refined)+1e-14)
  # Nonzero character coherence remains: the residual is not a Pauli mixture.
  self.assertNotEqual(p[0]-p[1]+p[2]-p[3],0)
 def test_centered_effect_weights_and_reused_key(self):
  p=.4;z=1.1;rt=.025;nu=1/SQ;f=(1-nu)/2;g=rt/2;scale=1-rt;k=(1-p)*(z-1)*scale/(p*nu);d=(1-p)*(z-1)*g/p;b=1-d+f*k;a=b-k
  for q in[0,.2,1]:self.assertAlmostEqual((1-p)*(1+(z-1)*(g+scale*q))+p*(a*(f+nu*q)+b*(1-f-nu*q)),1)
  # In magic-sector coordinates a reused C⊗C key keeps |00><11| coherence;
  # independent C keys remove it. The two nonzero eigenvalues are +-1/2.
  state=outer([1/SQ,0,0,1/SQ]);zz=kron(Z,Z)
  reused=mul(add(state,mm(mm(zz,state),zz)),.5);fresh=[[0j]*4 for _ in range(4)]
  for a,b in itertools.product([I,Z],repeat=2):
   k=kron(a,b);fresh=add(fresh,mul(mm(mm(k,state),adj(k)),.25))
  diff=add(reused,fresh,-1);self.assertAlmostEqual(diff[0][3].real,.5)
  self.assertAlmostEqual(diff[3][0].real,.5);self.assertTrue(all(abs(diff[i][i])<1e-14 for i in range(4)))
 def test_palindromic_exact_moments_and_constants(self):
  points=[F(0),F(1,4),F(3,4),F(1)];signs=[1,-1,1]
  self.assertEqual(sum(y*(b-a)for y,a,b in zip(signs,points,points[1:])),0)
  self.assertEqual(sum(y*((b*b-a*a)/2-(b-a)/2)for y,a,b in zip(signs,points,points[1:])),0)
  # Exact piecewise integrations, including absolute F across its midpoint zero.
  first=(F(1,4)**2/4-F(1,4)**3/3);second=F(1,4)**3/3
  self.assertEqual(2*(first+second),F(1,32))
  self.assertEqual((F(1,3)-F(1,2)+F(1,4))/2,F(1,24))
  self.assertEqual(F(1,4)**2/2,F(1,32))

 def test_current_scoped_acceptance_and_original_support(self):
  import json
  from pathlib import Path
  from knowledge.retrieve import Library
  l=Library()
  for n,count in[(1052,4),(1053,5),(1054,5)]:
   parent=l.resolve('N'+str(n));units=[r for r in l.records.values()if parent['id']in r['parents']];self.assertEqual(len(units),count)
   for r in[parent]+units:
    review=next(a for a in r['review_overlays']if a['id']==f'A{n+22}-quantum-continuation');self.assertEqual(review['decision'],'accepted_internally_verified');self.assertIn({'id':r['id'],'content_version':r['content_version']},review['subjects'])
  self.assertIn('Exactlyd keys',l.resolve('U1054-harmonic-biased-key-sector-filter')['contract']['requires'][0])
  self.assertIn('ONE bit',l.resolve('N1054')['body'])
  self.assertIn('contrast-optimal',l.source('U1054-magic-tester-and-effect-qualified-audit')['text'])
  p=Path(__file__).resolve().parents[1]/'research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-private-quantum-continuation/source/INDEX.json';rows=json.loads(p.read_text())['files'];original=[r for r in rows if r['kind']=='frozen_original'];self.assertEqual((len(original),sum(r['bytes']for r in original)),(10,139405))

 def test_actual_default_magic_packet_retains_budget_and_corrections(self):
  import json,subprocess,sys
  from pathlib import Path
  root=Path(__file__).resolve().parents[1]
  p=subprocess.run([sys.executable,'knowledge/retrieve.py','packet','N1054'],cwd=root,capture_output=True)
  self.assertEqual(p.returncode,0,p.stderr.decode());self.assertLessEqual(len(p.stdout),32768)
  r=json.loads(p.stdout)['packets'][0];self.assertEqual(len(r['notices']),3);self.assertTrue(r['evidence']);self.assertTrue(r['source_excerpts']);self.assertTrue(r['review_overlays'])

if __name__=='__main__':unittest.main()
