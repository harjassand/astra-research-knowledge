"""Independent physical-time interpretation and implementation transfer audit."""
import sys,json,time,random,itertools,hashlib
from pathlib import Path
from collections import deque
from fractions import Fraction as F
from math import comb
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'canonical_qec_witness_20261105'))
from sampler import Model,Proposal,bernoulli_vector
from phenomenological import RepeatedModel
start=time.perf_counter();out={}
# Check the new uniform 16-bit rejection primitive against one complete 16-bit
# domain, including troublesome rejection proportions and boundary denominators.
class Words:
 def __init__(self):self.pos=0
 def randbytes(self,n):
  a=(np.arange(self.pos,self.pos+n//2,dtype=np.uint32)%65536).astype('<u2');self.pos+=n//2;return a.tobytes()
coin=[]
for b in [2,3,7,1000,32768,32769,65535,65536]:
 for a in [1,b//2]:
  p=F(a,b);bb=p.denominator;aa=p.numerator;limit=(65536//bb)*bb
  e=bernoulli_vector(p,limit,Words())
  assert int(e.sum())==aa*(65536//bb)
  assert len(e)==limit
  coin.append({'p':str(p),'accepted_domain_size':limit,'ones':int(e.sum())})
out['exact_full_word_domain_coin_tests']=coin
# Independently derive time-differenced syndrome records from cumulative data
# errors and noisy observations; compare each edge basis vector, then random cases.
rows=[];rng=random.Random(615729)
for d,T in [(3,1),(3,2),(3,3),(5,5),(9,7)]:
 base=Model(d);m=RepeatedModel(d,T);ns=len(base.edges);nc=len(base.checks)
 def physical_observation(e):
  cumulative=np.zeros(ns,dtype=np.uint8);previous=np.zeros(nc,dtype=np.uint8);det=[]
  for t in range(T):
   cumulative^=e[t*ns:(t+1)*ns]
   true=(base.H@cumulative)%2
   observed=true^(e[T*ns+t*nc:T*ns+(t+1)*nc] if t<T-1 else 0)
   det.extend(observed^previous);previous=observed
  parity=int(cumulative[base.cut].sum())%2
  return np.array(det,dtype=np.uint8),parity
 for k in range(len(m.edges)):
  e=np.zeros(len(m.edges),dtype=np.uint8);e[k]=1
  s,l=physical_observation(e);assert np.array_equal(s,(m.H@e)%2);assert l==int(e[m.cut].sum())%2
 for i in range(100):
  e=np.array([rng.randrange(2) for _ in m.edges],dtype=np.uint8);s,l=physical_observation(e)
  assert np.array_equal(s,(m.H@e)%2);assert l==int(e[m.cut].sum())%2
 rows.append({'d':d,'T':T,'fault_basis_checks':len(m.edges),'random_physical_traces':100})
out['independent_cumulative_time_model_checks']=rows
# Exact minimum correction for all d3,T2 detector syndromes, computed by BFS
# over syndrome masks with one edge flip per transition (independent of matching).
m=RepeatedModel(3,2);nc=len(m.checks);N=len(m.edges);cols=[]
for ends in m.edge_checks:
 mask=0
 for c in ends:mask^=1<<c
 cols.append(mask)
best=[-1]*(1<<nc);best[0]=0;todo=deque([0])
while todo:
 s=todo.popleft()
 for col in cols:
  z=s^col
  if best[z]<0:best[z]=best[s]+1;todo.append(z)
for s in range(1<<nc):
 syndrome=np.array([(s>>i)&1 for i in range(nc)],dtype=np.uint8)
 c=m.m.decode(syndrome).astype(np.uint8)
 assert int(c.sum())==best[s];assert np.array_equal((m.H@c)%2,syndrome)
out['exhaustive_repeated_decoder_optimality']={'d':3,'T':2,'edges':N,'detectors':nc,'syndromes':1<<nc}
# Independent DFS counts for short walks and canonical cover of all weight<=4
# faults. This does not claim exhaustive coverage of the 2^32 error space.
Lmax=9;q=Proposal(m,F(1,1000),Lmax);counts=[0]*(Lmax+1);walkset=set()
def visit(v,prev,es):
 if v in m.right:counts[len(es)]+=1;walkset.add(tuple(es));return
 if v not in m.checkid or len(es)==Lmax:return
 for w,k in m.adj[v]:
  if w!=prev:visit(w,v,es+[k])
for root in m.left:
 z,k=m.adj[root][0];visit(z,root,[k])
assert counts==q.counts
checked=0;fails=0;longer=0
for k in range(5):
 for edges in itertools.combinations(range(N),k):
  e=np.zeros(N,dtype=np.uint8);e[list(edges)]=1;wit=m.witness(e);checked+=1
  if wit is not None:
   fails+=1;assert 2*sum(int(e[z]) for z in wit)>=len(wit)
   assert len(wit)<=2*k
   assert wit in walkset
out['repeated_path_cover_low_weight_checks']={'patterns':checked,'failures':fails,'max_fault_weight':4,'Lmax':Lmax,'walk_counts':counts}
# Recompute exact output endpoint arithmetic, not its random experiment.
rpath=Path(__file__).resolve().parents[1]/'canonical_qec_witness_20261105/phenomenological_d21_result.json'
if rpath.exists():
 from scipy.stats import beta
 r=json.loads(rpath.read_text());n=r['shots'];x=r['counts']['accepted'];z=F(r['Z_exact']);tail=F(r['tail_exact']);lo,hi=map(F,r['interval_exact'])
 reflo=beta.ppf(.0005,x,n-x+1);refhi=beta.ppf(.9995,x+1,n-x)
 assert float(lo/z)<=reflo and float((hi-tail)/z)>=refhi
 out['d21_output_arithmetic']={'accepted':x,'shots':n,'modeled_interval':r['interval'],'tail':r['tail_bound'],'minimum_CP_root':reflo,'maximum_CP_root':refhi}
out['status']='PASS: graph equals iid phenomenological data-Z/syndrome-bit model with perfect initial/final closure; not circuit noise.'
out['elapsed_seconds']=time.perf_counter()-start
out['source_sha256']={name:hashlib.sha256((Path(__file__).resolve().parents[1]/'canonical_qec_witness_20261105'/name).read_bytes()).hexdigest() for name in ['sampler.py','phenomenological.py']}
Path(__file__).with_name('phenomenological_audit_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
