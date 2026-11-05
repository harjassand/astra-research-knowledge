"""Independent adversarial checks, not a new confidence experiment.
Run with the existing decoder environment; no prior test data used.
"""
import sys,json,random,time,itertools,hashlib
from pathlib import Path
from fractions import Fraction as F
from math import comb
import numpy as np
from scipy.stats import beta
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'canonical_qec_witness_20261105'))
from sampler import Model,Proposal,exact_cp,cdf_num
start=time.perf_counter();out={}
m=Model(3);N=len(m.edges)
# Enumerate all nonbacktracking absorbing walks independently, preserving vertices.
walks={}
def walk(v,prev,es,vs,limit):
 if v in m.right:
  walks[tuple(es)]=tuple(vs);return
 if v not in m.checkid or len(es)>=limit:return
 for w,eid in m.adj[v]:
  if w!=prev:walk(w,v,es+[eid],vs+[w],limit)
for root in m.left:
 w,eid=m.adj[root][0];walk(w,root,[eid],[root,w],7)
errors=[];best={};failure_by_len={}
for mask in range(1<<N):
 e=np.array([(mask>>i)&1 for i in range(N)],dtype=np.uint8)
 s=tuple(int(z) for z in (m.H@e)%2);w=int(e.sum());best[s]=min(best.get(s,N+1),w)
 errors.append((e,s,w))
for e,s,w in errors:
 c=m.decode(e);assert int(c.sum())==best[s]
 assert np.all((m.H@(e^c))%2==0)
 # A separate residual-component parity check. An odd left component must touch right.
 r=e^c;unseen=set(range(len(m.coords)));odd_components=0
 while unseen:
  root=min(unseen);unseen.remove(root);stack=[root];component={root}
  while stack:
   v=stack.pop()
   for z,eid in m.adj[v]:
    if r[eid] and z in unseen:unseen.remove(z);stack.append(z);component.add(z)
  left_odd=sum(int(r[m.adj[z][0][1]]) for z in component if z in m.left)%2
  if left_odd:
   odd_components+=1;assert component&m.right
 assert (odd_components%2)==(int(r[m.cut].sum())%2)
 wit=m.witness(e)
 if wit is not None:
  assert len(set(walks[wit]))==len(walks[wit])
  assert 2*sum(int(e[z]) for z in wit)>=len(wit)
  failure_by_len[len(wit)]=failure_by_len.get(len(wit),0)+1
out['exhaustive_decoder_and_component_cover']={'errors':len(errors),'syndromes':len(best),'failures_by_canonical_length':failure_by_len}
# Independently reconstruct every random-choice probability, including multiplicity
# and nonsimple rejection. Unlike the original test, this does not assume P(e)/Z.
rows=[]
for p in [F(1,1000),F(1,10),F(1,2)]:
 for Lmax in ([3,4,5,6,7] if p==F(1,1000) else [7]):
  q=Proposal(m,p,Lmax);a,b=p.numerator,p.denominator
  states={(u,v):i for i,(u,v,ei) in enumerate(q.states)};pathprobs={}
  for es,vs in walks.items():
   L=len(es)
   if L>Lmax:continue
   prob=F(q.length_weights[L-1],sum(q.length_weights))
   sid=states[vs[0],vs[1]]
   prob*=F(q.h[L-1][sid],sum(q.h[L-1][i] for i in q.starts))
   for t in range(1,L):
    nid=states[vs[t],vs[t+1]];rem=L-t
    prob*=F(q.h[rem-1][nid],sum(q.h[rem-1][j] for j in q.next[sid]));sid=nid
   pathprobs[es]=prob
   assert prob==sum(F(comb(L,k))*p**k*(1-p)**(L-k) for k in range((L+1)//2,L+1))/q.Z
  assert sum(pathprobs.values())==1
  actual_accept=F(0);truncated_failure=F(0);omitted=F(0);total_failure=F(0)
  for e,s,w in errors:
   wit=m.witness(e)
   if wit is None:continue
   pe=p**w*(1-p)**(N-w);total_failure+=pe
   if len(wit)>Lmax:omitted+=pe;continue
   L=len(wit);k=sum(int(e[z]) for z in wit);outside_w=w-k
   conditional_k=F(q.kweights[L][k-(L+1)//2],sum(q.kweights[L]))
   conditional_subset=F(1,comb(L,k))
   conditional_outside=p**outside_w*(1-p)**(N-L-outside_w)
   joint=pathprobs[wit]*conditional_k*conditional_subset*conditional_outside
   assert joint==pe/q.Z
   actual_accept+=joint;truncated_failure+=pe
  assert actual_accept*q.Z==truncated_failure
  assert omitted<=q.tail
  rows.append({'p':str(p),'Lmax':Lmax,'paths':len(pathprobs),'acceptance_exact':str(actual_accept),'logical_failure_exact':str(total_failure),'omitted_exact':str(omitted),'tail_exact':str(q.tail)})
out['independent_sampler_likelihood_and_truncation']=rows
# Direct binomial sums exercise recurrence independently on all small arguments.
checks=0
for n in range(1,31):
 for k in range(-1,n+1):
  for D in [2,4,8,16]:
   for j in range(D+1):
    direct=sum(comb(n,i)*j**i*(D-j)**(n-i) for i in range(max(0,k+1)))
    assert cdf_num(n,k,j,D)==direct;checks+=1
out['independent_integer_cdf_checks']=checks
# All endpoint cases in small n; independently check exact root inequalities,
# one-grid-unit sharpness, floating quantiles, and full coverage on rational grids.
cpchecks=0;coverage_min=F(1);coverage_arg=None
for n in range(1,65):
 intervals=[]
 for x in range(n+1):
  lo,hi=exact_cp(x,n,bits=12);intervals.append((lo,hi));D=4096
  # Exact binomial tails with independent comb sums.
  def cdf(k,z):return sum(F(comb(n,i))*z**i*(1-z)**(n-i) for i in range(k+1))
  if x:
   assert 1-cdf(x-1,lo)<=F(1,2000)
   assert 1-cdf(x-1,lo+F(1,D))>F(1,2000)
  if x<n:
   assert cdf(x,hi)<=F(1,2000)
   assert cdf(x,hi-F(1,D))>=F(1,2000)
  qlo=0 if not x else beta.ppf(.0005,x,n-x+1)
  qhi=1 if x==n else beta.ppf(.9995,x+1,n-x)
  assert float(lo)<=qlo+1e-14 and float(hi)>=qhi-1e-14
  cpchecks+=1
 for j in range(1,20):
  p=F(j,20);coverage=sum(F(comb(n,x))*p**x*(1-p)**(n-x) for x,(lo,hi) in enumerate(intervals) if lo<=p<=hi)
  assert coverage>=F(999,1000)
  if coverage<coverage_min:coverage_min=coverage;coverage_arg=(n,str(p))
out['confidence_checks']={'intervals':cpchecks,'minimum_grid_coverage':float(coverage_min),'argmin':coverage_arg,'exact_coverage_grids':64*19}
# Published d13 interval numerical crosscheck; do not rerun its confidence trial.
r=json.loads((Path(__file__).resolve().parents[1]/'canonical_qec_witness_20261105/result_d13.json').read_text())
x=r['counts']['accepted'];n=r['shots'];lo,hi=map(F,r['accepted_probability_CP_interval']);z=F(r['Z_exact']);tail=F(r['omitted_canonical_witness_mass_upper_exact'])
reflo=beta.ppf(.0005,x,n-x+1);refhi=beta.ppf(.9995,x+1,n-x)
assert float(lo)<=reflo and float(hi)>=refhi
assert float(z*lo)==r['modeled_logical_failure_interval'][0] and float(z*hi+tail)==r['modeled_logical_failure_interval'][1]
out['published_d13_arithmetic']={'accepted':x,'shots':n,'CP_float_roots':[reflo,refhi],'outward_dyadic':[float(lo),float(hi)],'relative_half_width':(r['modeled_logical_failure_interval'][1]-r['modeled_logical_failure_interval'][0])/(2*r['modeled_logical_failure_estimate'])}
# A separate exact syndrome-T-join DP verifies minimum correction for random
# larger geometries with <= 14 defects, allowing a defect to match a rough boundary.
from functools import lru_cache
rng=random.Random(581637);large=[]
for d in [5,9,13,25,41]:
 mm=Model(d);trials=100
 for trial in range(trials):
  k=rng.randrange(15);nodes=rng.sample(mm.checks,k)
  coords=[mm.coords[v] for v in nodes]
  @lru_cache(None)
  def optimum(mask):
   if not mask:return 0
   bit=mask&-mask;i=bit.bit_length()-1;rest=mask^bit;x,y=coords[i]
   best=min(x,d-x)+optimum(rest)
   remaining=rest
   while remaining:
    bj=remaining&-remaining;j=bj.bit_length()-1;remaining^=bj
    xx,yy=coords[j];best=min(best,abs(x-xx)+abs(y-yy)+optimum(rest^bj))
   return best
  syndrome=np.zeros(len(mm.checks),dtype=np.uint8)
  for node in nodes:syndrome[mm.checkid[node]]=1
  correction=mm.m.decode(syndrome).astype(np.uint8)
  assert int(correction.sum())==optimum((1<<k)-1)
  assert np.array_equal((mm.H@correction)%2,syndrome)
 large.append({'d':d,'syndromes':trials,'max_defects':14})
out['independent_large_decoder_optimality']=large
out['status']='PASS: no in-domain counterexample found; no empirical claim of advantage over splitting.'
out['elapsed_seconds']=time.perf_counter()-start
out['tested_sampler_sha256']=hashlib.sha256((Path(__file__).resolve().parents[1]/'canonical_qec_witness_20261105/sampler.py').read_bytes()).hexdigest()
Path(__file__).with_name('audit_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
