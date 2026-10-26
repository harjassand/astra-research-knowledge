"""Independent exact certificate checks and version/source-route regressions.

No producer import, numerical optimizer, model call or optional dependency.
The supplied cases are exposed, not a new held-out study or policy experiment.
"""
from fractions import Fraction as F
import hashlib
import itertools
import json
import math
import subprocess
import sys
import unittest
from knowledge.model import ROOT
from knowledge.retrieve import Library

UPDATE='research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-method-redesign'
SOURCE=ROOT/UPDATE/'source'
U1='U1038-denominator-only-operator-covariance'
U2='U1038-three-lmi-global-interval-evaluator'
U3='U1038-active-two-and-vacuum-lift'
U4='U1042-checked-proposals-to-exact-laws'
U5='U1042-exact-vertex-hull-comparator'

def mat(a):return [[F(x)for x in row]for row in a]
def tr(a):return list(map(list,zip(*a)))
def mul(a,b):return [[sum(x*y for x,y in zip(row,col))for col in zip(*b)]for row in a]
def add(a,b):return [[x+y for x,y in zip(r,s)]for r,s in zip(a,b)]
def scale(c,a):return [[c*x for x in row]for row in a]
def sub(a,b):return add(a,scale(-1,b))
def eye(n):return [[F(i==j)for j in range(n)]for i in range(n)]
def zeros(n,m):return [[F(0)]*m for _ in range(n)]
def total(a,n,m):return sum_matrix(a,zeros(n,m))
def sum_matrix(a,start):
 for x in a:start=add(start,x)
 return start
def diag(v):return [[x if i==j else F(0)for j in range(len(v))]for i,x in enumerate(v)]
def inv(a):
 n=len(a);rows=[r[:]+s for r,s in zip(a,eye(n))]
 for j in range(n):
  k=next(i for i in range(j,n)if rows[i][j]);rows[j],rows[k]=rows[k],rows[j]
  rows[j]=[v/rows[j][j]for v in rows[j]]
  for i in range(n):
   if i!=j:
    c=rows[i][j];rows[i]=[x-c*y for x,y in zip(rows[i],rows[j])]
 return [r[n:]for r in rows]
def psd(a):
 if a!=tr(a)or len(a)not in(1,2):return False
 if len(a)==1:return a[0][0]>=0
 return a[0][0]>=0 and a[1][1]>=0 and a[0][0]*a[1][1]>=a[0][1]**2
def pd(a):return psd(a)and(a[0][0]>0 if len(a)==1 else a[0][0]*a[1][1]>a[0][1]**2)
P=mat([[1,0,0],[0,1,0]]); B=mat([[1,0],[0,1],[-1,-1]])
E=[mat([[1],[0]]),mat([[0],[1]]),mat([[0],[0]])]
def data(k,l):
 r=mul(P,inv(l));d=mul(mul(P,k),B)
 xs=[mul(P,[[row[i]]for row in k])for i in range(3)]
 ts=[sub(diag([v[0]for v in x]),mul(x,tr(x)))for x in xs]
 hs=[sub(mul(mul(r,diag([row[i]for row in l])),tr(r)),mul(e,tr(e)))for i,e in enumerate(E)]
 ss=[mul(mul(d,h),tr(d))for h in hs]
 return xs,ts,ss
def tensor(a,b):return [[x*y for x in row for y in br]for row in a for br in b]
def block(a):
 return [[v for subrow in row for v in subrow]for blocks in a for row in zip(*blocks)]


class MethodRedesign(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.lib=Library()

 def test_all_thirteen_saved_certificates_without_producer_import(self):
  cases=json.loads((SOURCE/'channel/INPUTS.json').read_text())['cases']
  results=json.loads((SOURCE/'channel/RESULTS.json').read_text())['results']
  self.assertEqual(len(cases),13);self.assertEqual([c['id']for c in cases],[r['id']for r in results])
  noncommuting=0
  for case,result in zip(cases,results):
   with self.subTest(case=case['id']):
    k,l=mat(case['K']),mat(case['L'])
    self.assertTrue(all(v>0 for a in[k,l]for row in a for v in row))
    self.assertTrue(all(sum(col)==1 for a in[k,l]for col in zip(*a)))
    xs,ts,ss=data(k,l);cert=result['upper_certificate'];c=F(cert['c']);self.assertGreaterEqual(c,0)
    if cert['regime']=='constant':self.assertEqual(c,0);self.assertEqual(mul(k,B),zeros(3,2))
    else:
     for x,t,s in zip(xs,ts,ss):
      residual=sub(scale(c,t),s)
      if cert['regime']=='subunit':
       self.assertLess(c,1);v=sub([[F(y)]for y in cert['z']],x);residual=sub(residual,scale(1-c,mul(v,tr(v))))
      else:self.assertEqual(cert['regime'],'vertex');self.assertGreaterEqual(c,1)
      self.assertTrue(psd(residual))
    witness=result['lower_witness'];es=[mat(x)for x in witness['effects_unnormalized']];hs=[[[F(y)]for y in x]for x in witness['vectors_unnormalized']];d=len(es[0])
    self.assertIn(d,[1,2]);self.assertTrue(all(psd(x)for x in es));self.assertTrue(pd(total(es,d,d)));self.assertEqual(total(hs,d,1),zeros(d,1))
    def form(a):
     value=F(0)
     for row in a:
      ey=total([scale(v,e)for v,e in zip(row,es)],d,d);hy=total([scale(v,h)for v,h in zip(row,hs)],d,1)
      self.assertTrue(pd(ey));value+=mul(mul(tr(hy),inv(ey)),hy)[0][0]
     return value
    fl=form(l);self.assertGreater(fl,0);lo=form(k)/fl;self.assertEqual(lo,F(result['lower']));self.assertEqual(c,F(result['upper']));self.assertLessEqual(lo,c);self.assertLessEqual(c-lo,max(F(1),lo)/50)
    # Stored E_i are unnormalized Gram effects. Commutation of normalized Q_i
    # is tested by congruence: E_i G^-1 E_j - E_j G^-1 E_i, not [E_i,E_j].
    gi=inv(total(es,d,d))
    if d==2 and mul(mul(es[0],gi),es[1])!=mul(mul(es[1],gi),es[0]):noncommuting+=1
  self.assertGreaterEqual(noncommuting,1)

 def test_ordered_covariance_identity_with_singular_numerator(self):
  k=mat([['1/2','1/4','3/8'],['1/4','1/2','3/8'],['1/4','1/4','1/4']]);l=mat([['3/5','1/5','1/5'],['1/5','3/5','1/5'],['1/5','1/5','3/5']])
  self.assertEqual(k[2][0],k[2][1]);self.assertEqual([row[2]for row in k],[(row[0]+row[1])/2 for row in k])
  qs=[mat([['1/3','1/8'],['1/8','1/3']]),mat([['1/4',0],[0,'1/3']])];qs.append(sub(eye(2),add(*qs)));self.assertNotEqual(mul(qs[0],qs[1]),mul(qs[1],qs[0]));self.assertTrue(all(pd(q)for q in qs))
  def mixes(a):return [total([scale(v,q)for v,q in zip(row,qs)],2,2)for row in a]
  ws=mixes(k);j=block([[add(inv(ws[0]),inv(ws[2])),inv(ws[2])],[inv(ws[2]),add(inv(ws[1]),inv(ws[2]))]])
  w=block([[ws[0]],[ws[1]]]);cov=sub(block([[ws[0],zeros(2,2)],[zeros(2,2),ws[1]]]),mul(w,tr(w)));self.assertEqual(inv(j),cov)
  lb=mul(l,B);wl=mixes(l)
  jl=total([tensor(mul([[v]for v in row],[row]),inv(wy))for row,wy in zip(lb,wl)],4,4)
  xs,ts,ss=data(k,l);d=tensor(mul(mul(P,k),B),eye(2));c=F(2)
  left=sub(scale(c,cov),mul(mul(d,inv(jl)),tr(d)))
  x=total([tensor(xi,q)for xi,q in zip(xs,qs)],4,2)
  v=sub(total([tensor(mul(xi,tr(xi)),q)for xi,q in zip(xs,qs)],4,4),mul(x,tr(x)))
  right=add(total([tensor(sub(scale(c,t),s),q)for t,s,q in zip(ts,ss,qs)],4,4),scale(c-1,v))
  self.assertEqual(left,right)

 def test_selected_posthoc_ordinary_optimum_and_exact_mean(self):
  result=json.loads((SOURCE/'exact_law/POST_HOC_RESULT.json').read_text());case=next(c for c in json.loads((SOURCE/'exact_law/INPUTS.json').read_text())['cases']if c['id']==result['case_id'])
  a=mat(case['A']);p=list(map(F,case['p']));n=len(p);law=[(r['atom'],F(r['weight']))for r in result['law']]
  self.assertTrue(all(w>0 for _,w in law));self.assertEqual(sum(w for _,w in law),1);self.assertLessEqual(len(law),n+1)
  self.assertEqual([sum(F(z[j])*w for z,w in law)for j in range(n)],p)
  meta=result['metadata'];scale_=meta['exact_integer_scale'];cost=F(meta['optimum']);previous=F(meta['predecessor_threshold']);separator=list(map(F,meta['predecessor_certificate']['affine_separator']))
  self.assertEqual(cost,F(26575,172032));self.assertLess(cost,F(80357,172032));self.assertLess(sum(c*v for c,v in zip(separator[:-1],p))+separator[-1],0)
  # Integer row arithmetic is exact after checking every scale identity.
  base=[-sum(row[j]*p[j]for j in range(n))*scale_ for row in a];cols=[[x*scale_ for x in row]for row in a]
  self.assertTrue(all(v.denominator==1 for v in base+[x for row in cols for x in row]))
  base=list(map(int,base));cols=[list(map(int,row))for row in cols]
  def error(z):return F(max(abs(b+sum(c*x for c,x in zip(row,z)))for b,row in zip(base,cols)),scale_)
  self.assertEqual(max(error(z)for z,w in law),cost)
  free=[j for j,v in enumerate(p)if v not in(0,1)];count=0;predecessor_found=False
  for bits in itertools.product((0,1),repeat=len(free)):
   z=[int(v)if v in(0,1)else 0 for v in p]
   for j,b in zip(free,bits):z[j]=b
   value=error(z);count+=1
   if value<cost:self.assertLessEqual(value,previous)
   if value==previous:predecessor_found=True
   if value<=previous:self.assertGreaterEqual(sum(c*v for c,v in zip(separator[:-1],z))+separator[-1],0)
  self.assertEqual(count,16384);self.assertTrue(predecessor_found)

 def test_sources_current_acceptance_and_prior_credit(self):
  index=json.loads((ROOT/UPDATE/'source/INDEX.json').read_text());self.assertEqual(len(index['files']),46)
  for row in index['files']:self.assertEqual(hashlib.sha256((ROOT/UPDATE/row['path']).read_bytes()).hexdigest(),row['sha256'])
  parent=self.lib.resolve('N1038');self.assertTrue(any(r['id']=='A1063-global-channel-evaluator'for r in parent['review_overlays']));self.assertTrue(any(r['id']=='A1058-method-study'for r in parent['historical_reviews']))
  old=self.lib.resolve('U1038-free-umegaki-comparison-formula');self.assertTrue(any(r['id']=='A1058-method-study'for r in old['review_overlays']))
  self.assertIn('N965/N970',parent['contract']['requires']);self.assertIn('UNKNOWN',parent['contract']['assumptions'])
  for i,aid in [(U1,'A1063-global-channel-evaluator'),(U2,'A1063-global-channel-evaluator'),(U3,'A1063-global-channel-evaluator'),(U4,'A1064-checked-exact-law-adapter'),(U5,'A1064-checked-exact-law-adapter')]:
   v=self.lib.resolve(i);r=next(r for r in v['review_overlays']if r['id']==aid);self.assertIn({'id':i,'content_version':v['content_version']},r['subjects']);self.assertEqual(r['working_device'],'not established')
  n24=self.lib.resolve('N24');self.assertFalse(any(r['id']=='A1064-checked-exact-law-adapter'for r in n24['review_overlays']))

 def test_batch_failure_repair_and_method_scopes_remain_separate(self):
  r=json.loads((SOURCE/'repair/INDEPENDENT_REGRESSION_RESULTS.json').read_text());self.assertEqual(len(r['checks']),10);self.assertTrue(all(c['pass']for c in r['checks']));self.assertIn('frozen phase1/phase2',r['credit'])
  source=self.lib.source('N1038',1)['text'];self.assertIn('accepts an empty results list',source);self.assertIn('Separately credited post-review repair',source);self.assertIn('anisotropic_L_1e12',source)
  method=self.lib.resolve('N1043');self.assertIn('not independent policy replications',method['statement']);self.assertIn('No general policy',method['contract']['assumptions'])
  self.assertIn('not a self-contained',self.lib.resolve('N1042')['contract']['requires'])

 def test_actual_default_packets_and_decisive_routes(self):
  ids=['N1038','N1042','N1043',U1,U2,U3,U4,U5,'U1038-free-umegaki-comparison-formula','U1038-post-exposure-numerator-span-cutoff','U1038-biased-reset-index-transfer-failure','N24','N965','N970','N676']
  for i in ids:
   with self.subTest(identifier=i):
    p=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',i],cwd=ROOT,capture_output=True);self.assertEqual(p.returncode,0,p.stderr);self.assertLessEqual(len(p.stdout),32768)
  for i,phrase in [(U1,'No two W\'s are assumed to commute'),(U2,'dual sign convention'),(U3,'additional reference dimension'),(U4,'Arbitrarily biased selection'),(U5,'Ordinary exact global optimisation')]:
   text=self.lib.source(i)['text']
   if i==U3:phrase='active/vacuum'
   self.assertIn(phrase,text)
  transfers=self.lib.bridge(U3,U2)['transfers'];self.assertTrue(any(t['state']=='INCOMPATIBLE ASSUMPTIONS'and'vacuum'in t['scope']for t in transfers))


if __name__=='__main__':unittest.main()
