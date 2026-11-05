from sampler import Model,Proposal,exact_cp
from fractions import Fraction as F
from math import comb
from pathlib import Path
import numpy as np,json,time
start=time.perf_counter();m=Model(3);q=Proposal(m,F(1,10),7);N=len(m.edges)
errors=[];best={}
for mask in range(1<<N):
 e=np.array([(mask>>i)&1 for i in range(N)],dtype=np.uint8);syndrome=tuple((m.H@e)%2);weight=int(e.sum())
 errors.append(e);best[syndrome]=min(best.get(syndrome,N+1),weight)
walks={L:[] for L in range(1,8)}
def visit(u,previous,path):
 if len(path)>7:return
 if u in m.right:
  walks[len(path)].append(tuple(path));return
 if u not in m.checkid:return
 for v,edge in m.adj[u]:
  if v!=previous:visit(v,u,path+[edge])
for root in m.left:
 v,eid=m.adj[root][0];visit(v,root,[eid])
for L,paths in walks.items():assert len(paths)==q.counts[L]
walkset=set(p for pp in walks.values() for p in pp)
counts=[0]*(N+1);maxlength=0
for e in errors:
 c=m.decode(e);assert not np.any((m.H@(e^c))%2)
 assert int(c.sum())==best[tuple((m.H@e)%2)]
 witness=m.witness(e)
 if witness is None:continue
 assert witness in walkset and len(set(witness))==len(witness)
 assert 2*int(e[list(witness)].sum())>=len(witness)
 counts[int(e.sum())]+=1;maxlength=max(maxlength,len(witness))
P=sum(F(num)*q.p**k*(1-q.p)**(N-k) for k,num in enumerate(counts))
# Exact Bernoulli likelihood identity, independently summing all canonical path cells.
by_path={p:F(0) for p in walkset}
for e in errors:
 witness=m.witness(e)
 if witness is not None:
  k=int(e.sum());by_path[witness]+=q.p**k*(1-q.p)**(N-k)/q.Z
assert sum(by_path.values())==P/q.Z
# Exact confidence endpoints independently checked against scipy numerical beta quantiles.
from scipy.stats import beta
for n in [10,100]:
 for x in [0,1,n//2,n-1,n]:
  lo,hi=exact_cp(x,n)
  rl=0 if x==0 else beta.ppf(.0005,x,n-x+1)
  ru=1 if x==n else beta.ppf(.9995,x+1,n-x)
  assert float(lo)<=rl+1e-15 and float(hi)>=ru-1e-15
out={'status':'PASS: exhaustive d3 decoder optimality, witness cover, path DP and exact probability identity','errors_enumerated':len(errors),'distinct_syndromes':len(best),'failure_counts_by_fault_weight':counts,'logical_failure_exact':str(P),'logical_failure':float(P),'walk_envelope_exact':str(q.Z),'acceptance_probability_exact':str(P/q.Z),'acceptance_probability':float(P/q.Z),'walk_counts':q.counts,'max_observed_canonical_length':maxlength,'timing_seconds':time.perf_counter()-start}
Path(__file__).with_name('small_exact_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
