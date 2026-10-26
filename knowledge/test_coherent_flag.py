"""Exact curator algebra/route guards; no missing producer program is replayed."""
from fractions import Fraction as F
import hashlib,json,subprocess,sys,unittest
from pathlib import Path
from knowledge.model import ROOT
from knowledge.retrieve import Library

UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-26-coherent-check-flag'
PROOF='originals/DECOHERENCE_FREE_COHERENT_CHECK_FLAG.md'
IDS=['U1041-full-memory-dual-rail-check','U1041-accepted-leakage-and-joint-budget','U1041-collective-su2-control-interface']
OLD='U1023-complete-coarse-instrument-equivalence'
def eye(n):return [[F(i==j)for j in range(n)]for i in range(n)]
def scale(a,k):return [[k*x for x in row]for row in a]
def plus(a,b):return [[x+y for x,y in zip(r,s)]for r,s in zip(a,b)]
def mul(a,b):return [[sum(x*y for x,y in zip(row,col))for col in zip(*b)]for row in a]
def tr(a):return list(map(list,zip(*a)))
def kron(a,b):return [[x*y for x in row for y in other]for row in a for other in b]
X=[[F(0),F(1)],[F(1),F(0)]];Z=[[F(1),F(0)],[F(0),F(-1)]]
def filter_branch(k,t,sign=1,flag_z=False):
 # Build the physical four-state flag sandwich; extract normalized encoded +/-.
 n=len(k);e=eye(n);c=[[F(0)for _ in range(4*n)]for _ in range(4*n)]
 for flag in range(4):
  block=e if flag<2 else t
  for i in range(n):
   for j in range(n):c[flag*n+i][flag*n+j]=block[i][j]
 f=eye(4)
 if flag_z:f[2][2]=-1
 full=mul(mul(c,kron(f,k)),c)
 return [[sum(F(sign if a==2 else 1,2)*full[a*n+i][b*n+j]for a in [1,2]for b in [1,2])for j in range(n)]for i in range(n)]

# Unit Pauli phases and dyadic coefficients are exact here; rank is rational.
TABLE={(1,2):(1j,3),(2,3):(1j,1),(3,1):(1j,2),(2,1):(-1j,3),(3,2):(-1j,1),(1,3):(-1j,2)}
def wordmul(a,b):
 phase=1;out=[]
 for x,y in zip(a,b):
  if not x:out.append(y)
  elif not y:out.append(x)
  elif x==y:out.append(0)
  else:p,z=TABLE[x,y];phase*=p;out.append(z)
 return phase,tuple(out)
def opmul(a,b):
 out={}
 for x,c in a.items():
  for y,d in b.items():
   p,z=wordmul(x,y);out[z]=out.get(z,0)+c*d*p
 return {w:c for w,c in out.items()if c}
def opadd(a,b,k=1):
 out=dict(a)
 for w,c in b.items():out[w]=out.get(w,0)+k*c
 return {w:c for w,c in out.items()if c}
def comm(a,b):return opadd(opmul(a,b),opmul(b,a),-1)
def rank(rows):
 a=[list(map(F,row))for row in rows];r=0
 for c in range(27):
  pivot=next((j for j in range(r,len(a))if a[j][c]),None)
  if pivot is None:continue
  a[r],a[pivot]=a[pivot],a[r];v=a[r][c];a[r]=[x/v for x in a[r]]
  for j in range(len(a)):
   if j!=r and a[j][c]:
    v=a[j][c];a[j]=[x-v*y for x,y in zip(a[j],a[r])]
  r+=1
 return r

class CoherentFlag(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.library=Library()

 def test_full_memory_instrument_and_collective_annihilation(self):
  t=kron(Z,eye(2));rotation=[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
  ks=[scale(kron(X,rotation),F(3,5)),scale(kron(Z,X),F(4,5))]
  total=[[F(0)]*4 for _ in range(4)];filtered=[[F(0)]*4 for _ in range(4)]
  for k in ks:
   total=plus(total,mul(tr(k),k))
   for sign in [1,-1]:
    actual=filter_branch(k,t,sign);expected=scale(plus(k,scale(mul(mul(t,k),t),sign)),F(1,2));self.assertEqual(actual,expected)
    filtered=plus(filtered,mul(tr(actual),actual))
  self.assertEqual(total,eye(4));self.assertEqual(filtered,eye(4))
  p=[[F(0)]*4 for _ in range(4)];p[1][1]=p[2][2]=F(1)
  collective=plus(kron(Z,eye(2)),kron(eye(2),Z));self.assertEqual(mul(collective,p),[[0]*4 for _ in range(4)])

 def test_in_code_phase_can_accept_an_odd_fault_with_unit_effect(self):
  t=kron(Z,eye(2));bad=kron(X,eye(2))
  self.assertEqual(filter_branch(bad,t),[[0]*4 for _ in range(4)])
  # Logical flag Z corresponds to differential phase pi/2 up to common phase.
  accepted=filter_branch(bad,t,flag_z=True)
  self.assertEqual(mul(tr(accepted),accepted),eye(4))
  # No physical flag leaves 01/10; perfect code occupancy is insufficient.

 def test_joint_budget_and_conditioning_are_separate(self):
  # Two orthogonal Stinespring success branches: separate bounds do not sum free.
  a=scale(X,F(2,3));b=scale(Z,F(2,3));fault=plus(mul(tr(a),a),mul(tr(b),b))
  self.assertEqual(fault,scale(eye(2),F(8,9)));self.assertGreater(fault[0][0],F(4,9))
  # A rare always-wrong success branch can have small unconditional fault weight.
  success=scale(X,F(3,5));reject=scale(eye(2),F(4,5))
  actual=success+reject;ideal=[[F(0)]*2 for _ in range(2)]+eye(2)
  delta=plus(actual,scale(ideal,-1));delta_effect=mul(tr(delta),delta)
  self.assertEqual(mul(tr(actual),actual),eye(2))
  self.assertEqual(delta_effect,scale(eye(2),F(2,5)))
  p=mul(tr(success),success)[0][0];joint_error_squared=delta_effect[0][0]
  self.assertLessEqual(p,joint_error_squared);self.assertEqual(p/p,1);self.assertLess(joint_error_squared,1)

 def test_restricted_su2_cross_space_and_algebraic_encoded_port(self):
  js=[]
  for axis in [1,2,3]:
   j={}
   for site in range(3):w=[0]*4;w[site]=axis;j[tuple(w)]=1
   js.append(j)
  basis=[]
  for site in range(3):
   for axis in [1,2,3]:
    for target in [1,2,3]:w=[0]*4;w[site]=axis;w[3]=target;basis.append({tuple(w):1})
  rows={}
  for i,h in enumerate(basis):
   for axis,j in enumerate(js):
    for w,c in comm(h,j).items():
     value=c/(2j);self.assertEqual(value.imag,0);self.assertEqual(int(value.real),value.real)
     rows.setdefault((axis,w),[0]*27)[i]=int(value.real)
  self.assertEqual(rank(list(rows.values())),27)
  identity={(0,0,0,0):1};qs={(0,0,0,0):F(1,4),(1,1,0,0):F(-1,4),(2,2,0,0):F(-1,4),(3,3,0,0):F(-1,4)}
  c=opadd(qs,opmul(opadd(identity,qs,-1),{(0,0,0,3):1}))
  self.assertEqual(opmul(c,c),identity)
  for j in js:self.assertEqual(comm(c,j),{})
  self.assertTrue(any(sum(x!=0 for x in w[:3])==2 and w[3]!=0 for w in c))

 def test_actual_source_branches_and_acceptance(self):
  index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_bytes());self.assertEqual(len(index['files']),2);self.assertEqual(sum(r['bytes']for r in index['files']),27354)
  for row in index['files']:self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])
  for identifier,lines,phrase in [(IDS[0],[13,58],'Kraus by Kraus'),(IDS[1],[60,110],'single full-Stinespring'),(IDS[2],[133,171],'27-dimensional physical-Hamiltonian space')]:
   source=self.library.source(identifier);self.assertEqual(source['source']['lines'],lines);self.assertTrue(source['source']['path'].endswith(PROOF));self.assertIn(phrase,source['text'])
  for identifier in ['N1041',*IDS]:
   record=self.library.resolve(identifier);review=next(r for r in record['review_overlays']if r['id']=='A1061-coherent-check-flag');self.assertEqual(review['decision'],'accepted_internally_verified');self.assertIn({'id':record['id'],'content_version':record['content_version']},review['subjects']);self.assertEqual(review['physical_measurement'],'not established')
   self.assertTrue(any(n['notice_id']=='SN-N1041-NOISE-AND-EVIDENCE-SCOPE-20261026'and not n['whole_claim_invalidated']for n in record['notices']))

 def test_complete_call_bridge_and_existing_endpoint_default_budgets(self):
  transfer=self.library.bridge(IDS[0],OLD)['transfers'][0];self.assertEqual(transfer['state'],'ESTABLISHED COMPATIBLE INTERFACE')
  self.assertIn('normalized-success',transfer['scope']);self.assertIn('CPTP',transfer['remaining_obligations'][0])
  for e in ['from','to']:self.assertEqual(transfer[e+'_version'],self.library.resolve(transfer[e])['content_version'])
  for identifier in ['N1041',*IDS,'N1023',OLD,'U1023-fine-record-and-terminal-failures']:
   p=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',identifier],cwd=ROOT,capture_output=True);self.assertEqual(p.returncode,0,p.stderr);self.assertLessEqual(len(p.stdout),32768)

if __name__=='__main__':unittest.main()
