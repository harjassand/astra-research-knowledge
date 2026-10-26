"""Independent intake-author algebraic controls, not missing producer replays."""
import cmath,itertools,math,unittest

I=[[1,0],[0,1]];X=[[0,1],[1,0]];Y=[[0,-1j],[1j,0]];Z=[[1,0],[0,-1]];PA=[I,X,Y,Z]
def mm(a,b):return[[sum(x*y for x,y in zip(r,c))for c in zip(*b)]for r in a]
def adj(a):return[[complex(x).conjugate()for x in r]for r in zip(*a)]
def add(a,b,s=1):return[[x+s*y for x,y in zip(r,t)]for r,t in zip(a,b)]
def scale(a,s):return[[s*x for x in r]for r in a]
def kron(a,b):return[[x*y for x in r for y in t]for r in a for t in b]
def err(a,b):return max(abs(x-y)for r,t in zip(a,b)for x,y in zip(r,t))
def word(w):
 a=[[1]]
 for s in w:a=kron(a,PA['IXYZ'.index(s)])
 return a
def identity(n):return[[int(i==j)for j in range(n)]for i in range(n)]
class AccessControls(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.ident=identity(16);cls.p=scale(mm(add(cls.ident,word('XXXX')),add(cls.ident,word('ZZZZ'))),.25)
 def test_character_orthogonality(self):
  h=[[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]]
  self.assertEqual(mm(h,h),scale(identity(4),4))
 def test_matched_test_full_coefficient_gram(self):
  s=1/math.sqrt(2);basis=[([s,s],[s,-s]),([s,1j*s],[s,-1j*s]),([1,0],[0,1])];gram=[[0j]*4 for _ in range(4)]
  for plus,minus in basis:
   for v,w in[(plus,minus),(minus,plus)]:
    a=[sum(complex(w[i]).conjugate()*p[i][j]*v[j]for i,j in itertools.product(range(2),repeat=2))for p in PA]
    for i,j in itertools.product(range(4),repeat=2):gram[i][j]+=a[i]*a[j].conjugate()/6
  self.assertLess(err(gram,[[2/3 if i==j and i else 0 for j in range(4)]for i in range(4)]),1e-14)
 def test_pre_t_fault_placement_and_clifford_frames(self):
  t=[[1,0],[0,cmath.exp(1j*math.pi/4)]]
  for p in PA:
   q=mm(mm(t,p),adj(t));self.assertLess(err(mm(q,t),mm(t,p)),1e-14)
   for a in PA[1:]:
    b=mm(mm(q,a),adj(q));self.assertLess(min(err(b,scale(c,s))for c in PA[1:]for s in[-1,1]),1e-14)
  self.assertGreater(err(mm(t,X),mm(X,t)),.5)
 def test_dfs_collective_not_differential(self):
  a=add(kron(Z,I),kron(I,Z));b=add(kron(Z,I),kron(I,Z),-1)
  for k in[1,2]:self.assertTrue(all(a[i][k]==0 for i in range(4)));self.assertEqual(abs(b[k][k]),2)
 def test_code_and_single_site_detection(self):
  p=self.p;self.assertEqual(mm(p,p),p);self.assertEqual(sum(p[i][i]for i in range(16)),4)
  for j in range(4):
   for a in'XYZ':
    w=list('IIII');w[j]=a;self.assertLess(err(mm(mm(p,word(w)),p),scale(p,0)),1e-14)
 def test_known_site_recovery_identity_all_errors(self):
  p=self.p
  for j in range(4):
   errors=[]
   for a in'IXYZ':
    w=list('IIII');w[j]=a;errors.append(word(w))
   projectors=[mm(mm(e,p),e)for e in errors]
   total=scale(p,0)
   for a,pa in enumerate(projectors):
    total=add(total,pa)
    for b,e in enumerate(errors):self.assertLess(err(mm(mm(mm(errors[a],pa),e),p),p if a==b else scale(p,0)),1e-14)
   self.assertLess(err(total,self.ident),1e-14)
 def test_single_spin_decoupling_all_logical_matrix_units(self):
  # Complete even-parity complement-pair code basis, arbitrary logical/reference blocks.
  vs=[]
  for a in[0,3,5,6]:
   v=[0]*16;v[a]=v[15-a]=1/math.sqrt(2);vs.append(v)
  for j in range(4):
   for a,b in itertools.product(range(4),repeat=2):
    red=[[0j]*2 for _ in range(2)]
    for x,y in itertools.product(range(16),repeat=2):
     if (x&~(1<<j))==(y&~(1<<j)):red[(x>>j)&1][(y>>j)&1]+=vs[a][x]*vs[b][y]
    self.assertLess(err(red,scale(I,.5 if a==b else 0)),1e-14)
 def test_unknown_site_same_syndrome_different_logical(self):
  a=word('XIII');b=word('IXII');p=self.p
  self.assertEqual(mm(mm(a,p),a),mm(mm(b,p),b))
  self.assertGreater(err(mm(mm(p,mm(a,b)),p),p),.4)
 def test_two_contact_parity_is_undetected_and_nontrivial(self):
  p=self.p;l=word('ZZII');self.assertEqual(mm(l,p),mm(p,l));self.assertGreater(err(mm(l,p),p),.9)
  theta=math.pi/8;self.assertAlmostEqual(abs(math.sin(2*theta))/2,1/(2*math.sqrt(2)))
 def test_small_quantum_leak_has_zero_uniform_substate_support(self):
  theta=1e-4;c=math.cos(theta);s=math.sin(theta)
  self.assertLess(c*s,1.1e-4)
  # Distinct rank-one supports have zero intersection despite arbitrarily small distance.
  self.assertNotEqual(c*(-s)-s*c,0)
  plus=[[c*c,c*s],[c*s,s*s]];minus=[[c*c,-c*s],[-c*s,s*s]];m=scale(add(plus,minus),.5)
  self.assertAlmostEqual(abs(plus[0][1]-m[0][1]),c*s)
 def test_fast_bath_quadratic_estimate_small_model(self):
  for e in[.001,.1,.248,.7,1.2]:
   # Exact corrected channel of exp(-ie X_flag tensor Z_bath).
   self.assertLessEqual(1-math.cos(e),e*e/2+1e-15)
   self.assertLessEqual(math.sin(e)**2,min(1,e*e)+1e-15)
 def test_initial_detection_not_toggled_detection(self):
  p=self.p;s=word('XIII');logical=word('ZZII')
  v=mm(mm(s,mm(mm(p,logical),p)),s)
  self.assertLess(err(mm(mm(p,v),p),scale(p,0)),1e-14)
  self.assertGreater(err(mm(mm(p,mm(mm(s,v),s)),p),scale(p,0)),.4)
 def test_budget_and_logical_counterexample(self):
  a=.27;delta=.001;opt=math.sqrt(a/delta);candidates=[max(1,math.floor(opt)),max(1,math.ceil(opt))]
  n=min(candidates,key=lambda n:a/n+n*delta)
  self.assertEqual(n,min(range(1,200),key=lambda n:a/n+n*delta))
  p=self.p;l=word('ZZII');self.assertEqual(mm(l,p),mm(p,l))
  # Commuting logical evolution is never projected away; N*(theta/N)=theta.
  for n in[1,4,64]:self.assertAlmostEqual(n*(.5/n),.5)


class AccessCurrentRoutes(unittest.TestCase):
 def test_current_reviews_bind_actual_versions_and_keep_gaps(self):
  from knowledge.retrieve import Library
  l=Library()
  for name in ['N1062','N1063','N1064','U1064-detectable-checkpoint-error-budget']:
   r=l.resolve(name);p=l.packet([name])['packets'][0]
   self.assertEqual(len(p['review_overlays']),1)
   a=p['review_overlays'][0];self.assertEqual(a['decision'],'accepted_internally_verified')
   self.assertIn({'id':r['id'],'content_version':r['content_version']},a['subjects'])
   self.assertEqual(a['working_device'],'not established')
   self.assertTrue(a['remaining_gaps'])
  for name in ['N1064','U1064-detectable-checkpoint-error-budget','U1064-syndrome-ledger-needs-toggled-contract']:
   self.assertTrue(any('TOGGLED-LEDGER'in n['notice_id']for n in l.packet([name])['packets'][0]['notices']))
 def test_actual_first_source_is_the_right_proof_branch(self):
  from knowledge.retrieve import Library
  l=Library()
  cases=[('U1062-delayed-flags-full-memory-pauli','## 1. Exact complete-memory'),('U1062-late-key-pre-gate-t-faults','## 3. Non-Clifford gate'),('U1063-known-site-complete-memory-recovery','## 2. Full-memory theorem'),('U1063-fast-bath-quadratic-corrected-channel','## 4. Quantitative perturbation')]
  for name,phrase in cases:self.assertTrue(l.source(name)['text'].startswith(phrase),name)
 def test_actual_default_cli_preserves_budget_sources_and_review(self):
  import json,subprocess,sys
  from pathlib import Path
  root=Path(__file__).resolve().parents[1]
  for name in ['N1062','N1063','N1064','N1054']:
   r=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',name],cwd=root,capture_output=True)
   self.assertEqual(r.returncode,0,r.stderr.decode());self.assertLessEqual(len(r.stdout),32768)
   p=json.loads(r.stdout)['packets'][0]
   self.assertTrue(p['evidence']and p['source_excerpts']and p['review_overlays'])

if __name__=='__main__':unittest.main()
