"""Small independent exact controls; no imported producer scientific script."""
import itertools,math,unittest
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
def mm(a,b):return [[sum(x*y for x,y in zip(row,col))for col in zip(*b)]for row in a]
def plus(a,b):return [[x+y for x,y in zip(r,s)]for r,s in zip(a,b)]
def scale(a,t):return[[x*t for x in r]for r in a]
def eye(n):return[[F(i==j)for j in range(n)]for i in range(n)]
def inv(a):
 n=len(a);a=[list(r)+e for r,e in zip(a,eye(n))]
 for i in range(n):
  j=next(j for j in range(i,n)if a[j][i]);a[i],a[j]=a[j],a[i];v=a[i][i];a[i]=[x/v for x in a[i]]
  for j in range(n):
   if j!=i:
    v=a[j][i];a[j]=[x-v*y for x,y in zip(a[j],a[i])]
 return[r[n:]for r in a]
class FinalFiveControls(unittest.TestCase):
 def test_stationary_perron_ratio_reparametrization(self):
  k=[[F(2),F(1,4)*3],[F(1,9)*2,F(3)]];x=[F(3),F(2)];c=[x[i]/k[i][i]for i in range(2)]
  self.assertEqual([k[i][1-i]*c[1-i]/(k[i][i]*c[i])for i in range(2)],[F(1,6)]*2)
  for u in[F(1,10),F(1),F(3,2),F(9)]:self.assertGreaterEqual(max(F(1,4)/u,F(1,9)*u),F(1,6))

 def test_ideal_order_cycle_versus_symmetric_cross_hazards(self):
  e=F(1,50)
  def value(k):
   @lru_cache(None)
   def v(s):
    if not s:return F(1)
    return max(v(tuple(i for i in s if i!=j))/(1+sum(k[i][j]for i in s if i!=j))for j in s)
   return v((0,1,2))
  cycle=[[e if j==(i+1)%3 else F(0)for j in range(3)]for i in range(3)]
  sym=[[e if i!=j else F(0)for j in range(3)]for i in range(3)]
  self.assertEqual(value(cycle),1/(1+e));self.assertEqual(value(sym),1/((1+2*e)*(1+e)))

 def test_tip_recovery_from_absorption_equations(self):
  a,u,v,wb,wu,d=map(F,['.05','.02','.08','.00002','.008','.00001'])
  q=[[a+u+wb+d,-u],[-v,v+wu+d]];p=mm(inv(q),[[a],[F(0)]])[0][0]
  self.assertEqual(p,a/(a+wb+d+u*(wu+d)/(v+wu+d)))
  self.assertEqual(F(1,20)/(F(1,20)+F(1,5)),F(1,5)) # no possible redocking: undocking traps

 def test_shared_cleanup_optimality_and_historical_cost(self):
  for l,u,h,d in[(4,F(2),F(0),F(1,100)),(17,F(3),F(1,50),F(1,1000))]:
   k=u+h;q=d/(d+l*k);self.assertEqual(-d+l*k*q/(1-q),0)
   self.assertEqual(sum(range(1,l+1)),l*(l+1)//2)
  self.assertLess(F(9999,10000)**(64*65//2),F(9999,10000)**64)

 def test_registry_retry_kernel_carries_actual_state(self):
  p=F(3,5);w=F(1,100);r=1-p-w;g=F(9,10)
  wash=[[F(4,5),F(1,10)],[F(1,5),F(3,5)]];s=[[F(1),F(0)],[F(1,4),F(3,4)]]
  a=scale(wash,r*g);b=scale(mm(wash,s),p*g);h=mm(inv(plus(eye(2),scale(a,-1))),b)
  self.assertEqual(h,plus(b,mm(a,h)))
  total=[[F(0)]*2 for _ in range(2)];power=eye(2)
  for _ in range(20):total=plus(total,mm(power,b));power=mm(power,a)
  bound=r**20/(1-r)
  self.assertTrue(all(0<=h[i][j]-total[i][j]<=bound for i in range(2)for j in range(2)))
  self.assertNotEqual(mm(h,h)[0],mm(h,h)[1])

 def test_fatal_handle_damage_prices_missed_pulses(self):
  p=F(3,5);w=F(1,1000);s=F(999,1000);r=1-p-w
  exact=p*s/(1-r*s);partial=sum(p*s*(r*s)**n for n in range(30))
  self.assertGreater(exact,partial);self.assertLess(exact,p/(p+w))
  self.assertLess(math.prod(float(p*s**j/(1-r*s**j))for j in range(1,17)),float(exact)**16)

 def test_and_hypergraph_blocker_certificate_and_fresh_restart(self):
  def closure(deps,seeds):
   active=set(seeds)
   while True:
    new=active|{i for i,choices in enumerate(deps)if any(set(p)<=active for p in choices)}
    if new==active:return active
    active=new
  for deps in[[[(2,)],[(0,)],[(1,)]],[[(1,2)],[(0,2)],[(0,1)]],[[],[()],[ (0,1) ]]]:
   subsets=[{i for i in range(3)if mask>>i&1}for mask in range(8)]
   blockers=[u for u in subsets if u and all(all(set(p)&u for p in deps[i])for i in u)]
   for s in subsets:self.assertEqual(len(closure(deps,s))==3,all(bool(s&u)for u in blockers))
  triad=[[(1,2)],[(0,2)],[(0,1)]]
  self.assertEqual(closure(triad,{0,1}),{0,1,2});self.assertEqual(closure(triad,{1}),{1})

 def test_receipt_formula_counts_first_distinct_acceptances(self):
  p,beta,alpha=F(4,5),F(3,4),F(1,4);a=p*beta**2;b=(1-p)*alpha**2;r=1-a-b;n=6;k=2
  exact=sum(math.comb(n,j)*(a+b)**j*r**(n-j)for j in range(k,n+1))*(a/(a+b))**k
  enum=F(0)
  for seq in itertools.product(range(3),repeat=n):
   acc=[x for x in seq if x!=2]
   if len(acc)>=k and all(x==0 for x in acc[:k]):enum+=math.prod([a,b,r][x]for x in seq)
  self.assertEqual(exact,enum)
  self.assertLess((3*F(1,20)**2-2*F(1,20)**3)**4,F(3,10**9))

 def test_ctmc_stationarity_and_constant_indicator_generator(self):
  drift=[[-4,1,2],[2,-4,1],[1,2,-4]]
  for e in[F(1,10),F(1,3),F(4,5)]:
   q=[[F(0)]*4 for _ in range(4)]
   for i in range(1,4):q[0][i]=e/3;q[i][0]=1-e;q[i][1+i%3]=2+e/3;q[i][1+(i-2)%3]=1+e/3
   for i in range(4):q[i][i]=-sum(q[i])
   pi=[1-e,e/3,e/3,e/3];x=[[F(i==j+1)-e/3 for j in range(3)]for i in range(4)]
   self.assertEqual(mm([pi],q),[[0]*4]);self.assertEqual(mm(q,x),mm(x,list(map(list,zip(*drift)))))
   self.assertEqual((1-e)*(e/(1-e))**2+e*(3/e-1)**2,9/e-6+e/(1-e))

 def test_exact_matched_gaussian_rate(self):
  a=[[-F(4),F(1),F(2)],[F(2),-F(4),F(1)],[F(1),F(2),-F(4)]];at=list(map(list,zip(*a)))
  d=scale(plus(a,at),-F(1,2));k=scale(plus(a,scale(at,-1)),F(1,2));kt=list(map(list,zip(*k)))
  z=mm(mm(kt,inv(d)),k);self.assertEqual(sum(z[i][i]for i in range(3)),F(3,11))

 def test_exact_replicate_closure_fixture_and_gain(self):
  vectors=[(1,1,1),(1,1j,-1),(1,-1j,-1)];prob=[F(3,5),F(3,10),F(1,10)];gain=(2+1j,-1+2j,3-2j)
  def statistic(a,b,c):return int(((a[0]*complex(a[1]).conjugate())*(b[1]*complex(b[2]).conjugate())*(c[2]*complex(c[0]).conjugate())).imag)
  mean=second=F(0)
  for ids in itertools.product(range(3),repeat=3):
   a,b,c=[vectors[i]for i in ids];v=statistic(a,b,c);p=math.prod(prob[i]for i in ids);mean+=p*v;second+=p*v*v
   vv=[tuple(g*x for g,x in zip(gain,r))for r in[a,b,c]];self.assertEqual(statistic(*vv),325*v)
  self.assertEqual(mean,-F(6,125));self.assertEqual(second,F(12,25));self.assertEqual(F(2,3)*mean**2/second,F(2,625))

 def test_one_sided_cubic_bound_uses_positive_lagrange_weights(self):
  nodes=[F(1),F(2),F(3),F(4)];q=lambda x:x**3+1
  for x in[F(3,2),F(5,2),F(7,2)]:
   ell=[math.prod((x-nodes[k])/(nodes[j]-nodes[k])for k in range(4)if k!=j)for j in range(4)]
   self.assertTrue(any(v<0 for v in ell));self.assertEqual(sum(v*q(z)for v,z in zip(ell,nodes)),q(x))
   self.assertGreaterEqual(sum(max(0,v)*q(z)for v,z in zip(ell,nodes)),q(x))

 def test_fixture_passivity_and_hidden_motion_limit(self):
  for zs,zf,h in[(2+3j,4+2j,3-1j),(.1-50j,10,2j),(7,1+8j,4)]:
   transfer=-zf*h/(zs+zf);self.assertLessEqual(zf.real/abs(zf)*abs(transfer),abs(h)+1e-14)
  eps=1.;wmax=3.;w0=2.;strokes=[]
  for gamma in[1.,.1,.01,.001]:
   mu=eps*gamma/wmax**3
   for w in[.1,1.,2.,2.9,3.]:self.assertLessEqual(abs(-mu*w**4/(w0*w0-w*w+1j*gamma*w)),eps+1e-14)
   strokes.append(w0/gamma)
  self.assertEqual(strokes,sorted(strokes));self.assertGreater(strokes[-1],1000*strokes[0]-1)

 def test_passive_notch_between_nodes_needs_a_structural_promise(self):
  w0=198.
  def h(w,z):
   s=1j*w
   return -1.21*12.5*s*s/((1.21*s*s+4.56*s+42992)*(1.7+.009*s+z)+12.5**2*s)
  outcomes=[]
  for ln,rn in[(1e-6,1e5),(1e-8,1e7)]:
   cn=1/(w0*w0*ln)
   def z(w):return 1/(1/rn+1/(1j*w*ln)+1j*w*cn)
   error=max(abs(h(w,z(w))/h(w,0)-1)for w in[195.,197.,199.,201.])
   outcomes.append((error,abs(h(w0,rn))))
  self.assertLess(outcomes[1][0],outcomes[0][0]/50)
  self.assertLess(outcomes[1][1],outcomes[0][1]/50)


class FinalFiveCurrentRoutes(unittest.TestCase):
 def test_actual_versions_and_evidence_bound_acceptance(self):
  from knowledge.retrieve import Library
  l=Library()
  for name in ['N1058','N1059','N1060','N1061']:
   r=l.resolve(name);p=l.packet([name])['packets'][0]
   review=p['review_overlays'][0]
   self.assertEqual(review['decision'],'accepted_internally_verified')
   self.assertIn({'id':r['id'],'content_version':r['content_version']},review['subjects'])
   self.assertEqual(review['physical_measurement'],'not established')
   self.assertTrue(p['evidence'] and p['source_excerpts'])

 def test_current_denaturation_and_model_measurement_notices(self):
  from knowledge.retrieve import Library
  l=Library()
  for parent,unit,key in [('N1058','U1058-rooted-prefix-needs-recovered-register','DENATURATION-DOES-NOT-PRESERVE-REGISTER'),('N1060','U1060-same-covariance-vanishing-irreversibility','GAUSSIAN-RATE-NOT-UNIVERSAL'),('N1061','U1061-four-one-sided-readings-intrinsic-cubic','MODEL-CENTRES-NOT-MEASUREMENTS')]:
   for name in [parent,unit]:self.assertTrue(any(key in n['notice_id']for n in l.packet([name])['packets'][0]['notices']))
  for name,phrase in [('U1058-rooted-prefix-needs-recovered-register','fully denaturing wash'),('U1058-open-loop-registry-retry-and-retained-handle-aging','I-(1-p-w)'),('U1060-three-replica-phase-cancelling-kl-bound','three independent replicas'),('U1061-four-one-sided-readings-intrinsic-cubic','no upper gain')]:
   self.assertIn(phrase.lower(),l.source(name)['text'].lower())

 def test_real_default_parent_packets_retain_complete_scope(self):
  import json,subprocess,sys
  root=Path(__file__).resolve().parents[1]
  for name,key in [('N1058','DENATURATION-DOES-NOT-PRESERVE-REGISTER'),('N1059',None),('N1060','GAUSSIAN-RATE-NOT-UNIVERSAL'),('N1061','MODEL-CENTRES-NOT-MEASUREMENTS')]:
   p=subprocess.run([sys.executable,'knowledge/retrieve.py','packet',name],cwd=root,capture_output=True)
   self.assertEqual(p.returncode,0,p.stderr.decode());self.assertLessEqual(len(p.stdout),32768)
   r=json.loads(p.stdout)['packets'][0]
   if key:self.assertTrue(any(key in n['notice_id']for n in r['notices']))
   self.assertTrue(r['review_overlays'] and r['evidence'] and r['source_excerpts'])

if __name__=='__main__':unittest.main()
