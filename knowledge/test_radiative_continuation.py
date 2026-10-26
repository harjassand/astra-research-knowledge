"""Independent small controls of the selected analytic premises; no producer replay."""
import cmath, math, unittest
from pathlib import Path
from fractions import Fraction as F

def mm(a,b):return [[sum(x*y for x,y in zip(row,col))for col in zip(*b)]for row in a]
def mv(a,v):return [sum(x*y for x,y in zip(row,v))for row in a]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def transpose(a):return list(map(list,zip(*a)))
def addpoly(*terms):
 out={}
 for p,shift,scale in terms:
  for k,v in p.items():out[k+shift]=out.get(k+shift,0)+scale*v
 return{k:v for k,v in out.items()if v}

class RadiativeControls(unittest.TestCase):
 def test_exact_jacobi_walk_bracket(self):
  v=[F(1)]+[F(0)]*27;moments=[]
  for k in range(27):
   moments.append(dot(v,v));v=[sum((v[j]* (F(7,10)if min(i,j)==0 else F(1,2))for j in[i-1,i+1]if 0<=j<len(v)),F(0))for i in range(len(v))]
  bounds=[]
  for t in[F(2433886050,10**9),F(2433886053,10**9)]:
   p=sum((-1)**k*t**(2*k)*moments[k]/math.factorial(2*k)for k in range(27))
   tail=t**54/math.factorial(54)/(1-t*t/F(55*56));bounds.append((p-tail,p+tail))
  self.assertGreater(bounds[0][0],0);self.assertLess(bounds[1][1],0)
  self.assertEqual(1-2*F(7,10)**2,F(1,50))

 def test_certified_external_source_tail(self):
  t=F(2433886053,10**9);s=sum(t**n/math.factorial(n)for n in range(17,80));remainder=t**80/math.factorial(80)/(1-t/F(81))
  self.assertLess(2*(s+remainder),F(239970522,10**16))

 def test_fresh_child_and_phases(self):
  ident=[[1,0],[0,1]];x=[[0,1],[1,0]];z=[[1,0],[0,-1]]
  def pulse(p,sgn,t,enabled):
   if not enabled:return ident
   return [[cmath.exp(-1j*t)*(math.cos(t)*ident[i][j]-1j*sgn*math.sin(t)*p[i][j])for j in range(2)]for i in range(2)]
  wanted={(0,0):[1,0],(1,0):[1,0],(0,1):[-1j,0],(1,1):[0,1]}
  for (a,b),target in wanted.items():
   v=[1,0]
   for p,sgn,t,enable in[(x,-1,math.pi/4,b),(z,-1,math.pi/2,a),(x,1,math.pi/4,b),(z,-1,math.pi/2,a)]:v=mv(pulse(p,sgn,t,enable),v)
   self.assertLess(sum(abs(s-t)**2 for s,t in zip(v,target)),1e-26)

 def test_relative_phase_allows_any_common_release(self):
  cap=[[F(3,5),-F(4,5),0],[F(4,5),F(3,5),0],[0,0,1]];release=[[0,0,1],[1,0,0],[0,1,0]]
  captured=mv(cap,[1,0,0]);phase=[-captured[0],*captured[1:]]
  summed=[a+b for a,b in zip(mv(release,captured),mv(release,phase))]
  self.assertEqual(dot(summed,summed),4*dot(captured[1:],captured[1:]));self.assertNotEqual(mv(mm(release,cap),[1,0,0]),[1,0,0])

 def test_positive_onsite_phase_is_not_an_untracked_inverse(self):
  mu=2.3;t=.7;k=.8;z=[[1,0],[0,-1]]
  u=[[cmath.exp(-1j*mu*t)*(math.cos(k*t)if i==j else-1j*math.sin(k*t))for j in range(2)]for i in range(2)]
  conj=mm(mm(z,u),z);adj=[[u[j][i].conjugate()for j in range(2)]for i in range(2)]
  self.assertGreater(max(abs(conj[i][j]-adj[i][j])for i in range(2)for j in range(2)),.5)
  self.assertLess(max(abs(cmath.exp(2j*mu*t)*conj[i][j]-adj[i][j])for i in range(2)for j in range(2)),1e-14)

 def test_complete_three_stage_occupation_accounting(self):
  for phi in[.001,.07,.23,.8,1.3]:
   o=3.;t=(math.pi/(2*math.tan(phi))+2*phi)/o
   ae=(math.pi*math.sin(phi)*math.cos(phi)/2+phi-math.sin(2*phi)/2)/o
   aa=(phi/2+math.sin(2*phi)/4+math.pi*math.cos(phi)**3/(4*math.sin(phi)))/o
   self.assertAlmostEqual(2*aa+ae,t,places=11);self.assertGreaterEqual(t*ae*o*o,2)
  phi=1e-5;self.assertAlmostEqual((math.pi/(2*math.tan(phi))+2*phi)*(math.pi*math.sin(phi)*math.cos(phi)/2+phi-math.sin(2*phi)/2),math.pi**2/4,places=8)

 def test_unconditioned_markov_error_and_remainder(self):
  for dose in[.00001,.001,.05,.4]:
   error2=-2*math.expm1(-dose/2)
   self.assertLessEqual(abs(error2-dose),3*dose*dose/4+dose**3/12)
   self.assertGreater(math.sqrt(error2),dose if dose<.4 else 0)

 def test_exact_three_and_four_point_laurent_nulls(self):
  a=[{0:1},{-1:-1,1:-1},{0:1},{}];b=[{}, {0:1},{-1:-1,1:-1},{0:1}]
  for v in[a,b]:
   for sign in[-1,1]:self.assertEqual(addpoly(*[(p,sign*j,1)for j,p in enumerate(v)]),{})
  # The two distinct positions instead have nonzero determinant z-z^-1.
  self.assertEqual(addpoly(({0:1},1,1),({0:1},-1,-1)),{1:1,-1:-1})

 def test_moving_window_retains_transient_field(self):
  f={2:1,3:2,4:3,5:1};middle=addpoly((f,1,-1),(f,-1,-1))
  for t in range(9):
   prefix={k:v for k,v in f.items()if k<t};mid={k:v for k,v in middle.items()if k<t}
   actual=addpoly((prefix,1,1),(prefix,-1,1),(mid,0,1))
   window=addpoly(({k:v for k,v in f.items()if t-1<=k<t},1,1),({k:v for k,v in f.items()if t<=k<t+1},-1,-1))
   self.assertEqual(actual,window)
   if t==4:self.assertTrue(actual)
   if t==8:self.assertFalse(actual)

 def test_sparse_inverse_control_exact_compatibility(self):
  r=[F(3,5),F(4,5)];h=[F(1,4),F(1,2)];y=[F(2,3),-F(1,5)];z=[-F(2,7),F(3,8)]
  rp=[r[i]*dot(h,y)+[-r[1],r[0]][i]*F(2,9)for i in range(2)]
  co=[y[0]*v/dot(r,r)for v in r];cc=[(rp[i]-h[0]*co[i])/h[1]for i in range(2)];c=transpose([co,cc]);qoc=z[0]/h[1];q=[[0,qoc],[qoc,(z[1]-h[0]*qoc)/h[1]]]
  self.assertEqual(mv(c,h),rp);self.assertEqual(mv(transpose(c),r),y);self.assertEqual(mv(q,h),z)
  self.assertGreater(F('6.28')-F('4.71')-F('.104')-F('.0015'),F('1.46'))


class RadiativeCurrentRoutes(unittest.TestCase):
 def test_current_acceptance_and_correction_propagation(self):
  from knowledge.retrieve import Library
  l=Library()
  families=['N1055','N1056','N1057']
  for name in families:
   r=l.resolve(name);p=l.packet([name])['packets'][0]
   self.assertEqual(len(p['review_overlays']),1)
   review=p['review_overlays'][0]
   self.assertEqual(review['decision'],'accepted_internally_verified')
   self.assertIn({'id':r['id'],'content_version':r['content_version']},review['subjects'])
   self.assertEqual(review['working_device'],'not established')
  for name in ['N1055','U1055-relative-phase-release-and-tracked-inverse']:
   p=l.packet([name])['packets'][0]
   self.assertTrue(any('TRACKED-INVERSE-PHASE' in n['notice_id'] for n in p['notices']))
  for name in ['N1057','U1057-boundary-source-support-and-four-point-open-interface']:
   p=l.packet([name])['packets'][0]
   self.assertTrue(any('SOURCE-NULL-NOT-LOCAL-TRANSFER' in n['notice_id'] for n in p['notices']))

 def test_first_sources_open_the_actual_constructions(self):
  from knowledge.retrieve import Library
  l=Library()
  for name,phrase in [('U1056-exact-low-occupation-bridge-and-markov-remainder','## 3. An exact finite-time'),('U1057-positive-on-band-realization-and-reused-review','### Exact real'),('U1057-sparse-inverse-control-and-locality-obstructions','## 3. A reusable sparse'),('U1057-moving-window-radiation-and-control-budget','## 6. Moving-window')]:
   v=l.source(name);self.assertTrue(v['text'].startswith(phrase),(name,v['text'][:100]))

 def test_actual_default_parent_commands_preserve_scope(self):
  import json,subprocess,sys
  root=Path(__file__).resolve().parents[1]
  for name,notices in [('N1055',1),('N1056',0),('N1057',2)]:
   p=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',name],cwd=root,capture_output=True)
   self.assertEqual(p.returncode,0,p.stderr.decode());self.assertLessEqual(len(p.stdout),32768)
   packet=json.loads(p.stdout)['packets'][0]
   self.assertEqual(len(packet['notices']),notices)
   self.assertTrue(packet['evidence'] and packet['source_excerpts'] and packet['review_overlays'])

if __name__=='__main__':unittest.main()
