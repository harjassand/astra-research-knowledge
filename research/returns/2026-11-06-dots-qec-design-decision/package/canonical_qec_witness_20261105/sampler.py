"""Canonical-witness rare-failure sampler for a public specified graph noise model.
All proposal choices and path normalizers use integers/rationals. Random.Random is
only a reproducible PRNG implementation; iid confidence assumes ideal random bits.
"""
from fractions import Fraction as F
from math import comb,isqrt
from collections import deque
import random, json, time, argparse
from pathlib import Path
import numpy as np
import pymatching
from scipy.sparse import csr_matrix


def bernoulli_vector(p,n,rng):
 """Exact uniform integer rejection, vectorized; ideal bits inherited from rng."""
 a=p.numerator;b=p.denominator
 if b>65536:return np.array([rng.randrange(b)<a for _ in range(n)],dtype=np.uint8)
 limit=(65536//b)*b;out=np.empty(n,dtype=np.uint8);pos=0
 while pos<n:
  batch=((n-pos)*65536+limit-1)//limit+8
  raw=np.frombuffer(rng.randbytes(2*batch),dtype='<u2').astype(np.uint32)
  raw=raw[raw<limit];take=min(len(raw),n-pos)
  out[pos:pos+take]=(raw[:take]%b)<a;pos+=take
 return out

class Model:
 def __init__(self,d):
  assert d>=3
  self.d=d; self.coords=[(x,y) for x in range(d+1) for y in range(d)]
  self.node={q:i for i,q in enumerate(self.coords)};self.edges=[]
  for x in range(d):
   for y in range(d):self.edges.append((self.node[x,y],self.node[x+1,y]))
  for x in range(1,d):
   for y in range(d-1):self.edges.append((self.node[x,y],self.node[x,y+1]))
  self.adj=[[] for q in self.coords]
  for i,(u,v) in enumerate(self.edges):self.adj[u].append((v,i));self.adj[v].append((u,i))
  for a in self.adj:a.sort(key=lambda x:x[1])
  self.left=[self.node[0,y] for y in range(d)];self.right=set(self.node[d,y] for y in range(d))
  self.checks=[self.node[x,y] for x in range(1,d) for y in range(d)]
  self.checkid={v:i for i,v in enumerate(self.checks)};self.m=pymatching.Matching()
  hrows=[];hcols=[];self.edge_checks=[]
  for i,(u,v) in enumerate(self.edges):
   ends=[self.checkid[z] for z in (u,v) if z in self.checkid]
   hrows.extend(ends);hcols.extend([i]*len(ends));self.edge_checks.append(ends)
   if len(ends)==2:self.m.add_edge(*ends,fault_ids={i},weight=1.)
   else:self.m.add_boundary_edge(ends[0],fault_ids={i},weight=1.)
  self.H=csr_matrix((np.ones(len(hrows),dtype=np.uint8),(hrows,hcols)),shape=(len(self.checks),len(self.edges)))
  self.cut=list(range(d)) # all edges incident to the left rough boundary
 def decode(self,e):
  syndrome=np.zeros(len(self.checks),dtype=np.uint8)
  for edge in np.flatnonzero(e):
   for check in self.edge_checks[edge]:syndrome[check]^=1
  return self.m.decode(syndrome).astype(np.uint8)
 def witness(self,e):
  c=self.decode(e);r=e^c
  if int(r[self.cut].sum())%2==0:return None
  parents={v:None for v in self.left};q=deque(self.left);last=None
  while q:
   u=q.popleft()
   if u in self.right:last=u;break
   for v,edge in self.adj[u]:
    if r[edge] and v not in parents:parents[v]=(u,edge);q.append(v)
  assert last is not None
  path=[]
  while parents[last] is not None:
   last,edge=parents[last];path.append(edge)
  path=tuple(path[::-1]);assert 2*int(e[list(path)].sum())>=len(path)
  return path

class Proposal:
 def __init__(self,model,p,Lmax):
  assert F(0)<p<=F(1,2), "Require 0 < p <= 1/2 for the stated majority-tail bound"
  assert Lmax>=model.d, "The length budget must include a shortest logical path"
  self.model=model;self.p=p;self.Lmax=Lmax;a=p.numerator;b=p.denominator
  self.states=[]
  for e,(u,v) in enumerate(model.edges):self.states.extend([(u,v,e),(v,u,e)])
  stateid={(u,v):i for i,(u,v,e) in enumerate(self.states)}
  self.next=[]
  for u,v,e in self.states:
   self.next.append([stateid[v,w] for w,ee in model.adj[v] if w!=u] if v in model.checkid else [])
  self.h=[[int(v in model.right) for u,v,e in self.states]]
  for rem in range(1,Lmax):self.h.append([sum(self.h[-1][j] for j in nxt) for nxt in self.next])
  self.starts=[stateid[u,model.adj[u][0][0]] for u in model.left]
  self.counts=[0]+[sum(self.h[L-1][i] for i in self.starts) for L in range(1,Lmax+1)]
  self.kweights={};self.A={};self.length_weights=[]
  for L in range(1,Lmax+1):
   ws=[comb(L,k)*a**k*(b-a)**(L-k) for k in range((L+1)//2,L+1)]
   self.kweights[L]=ws;self.A[L]=sum(ws)
   self.length_weights.append(self.counts[L]*self.A[L]*b**(Lmax-L))
  self.Z=F(sum(self.length_weights),b**Lmax)
  # Exact rational Chernoff envelope: Binomial-tail <= (2 sqrt(p(1-p)))^L.
  D=10**12;num=4*a*(b-a)*D*D;den=b*b;t=isqrt(num//den)
  if t*t*den<num:t+=1
  r=F(t,D);assert r*r>=4*p*(1-p)
  if Lmax>=len(model.checks)+1:self.tail=F(0)
  else:
   branching=max(len(model.adj[v])-1 for v in model.checks)
   assert branching*r<1
   self.tail=F(len(model.left),branching)*(branching*r)**(Lmax+1)/(1-branching*r)
 @staticmethod
 def pick(weights,rng):
  k=rng.randrange(sum(weights))
  for i,w in enumerate(weights):
   if k<w:return i
   k-=w
  raise AssertionError
 def trial(self,rng):
  L=1+self.pick(self.length_weights,rng)
  s=self.starts[self.pick([self.h[L-1][i] for i in self.starts],rng)]
  u,v,edge=self.states[s];vertices=[u,v];path=[edge];rem=L-1
  while rem:
   nxt=self.next[s];s=nxt[self.pick([self.h[rem-1][j] for j in nxt],rng)]
   u,v,edge=self.states[s];vertices.append(v);path.append(edge);rem-=1
  assert v in self.model.right
  if len(set(vertices))!=len(vertices):return 0,'nonsimple'
  a=self.p.numerator;b=self.p.denominator
  e=bernoulli_vector(self.p,len(self.model.edges),rng)
  e[path]=0
  k=(L+1)//2+self.pick(self.kweights[L],rng)
  e[rng.sample(path,k)]=1
  witness=self.model.witness(e)
  if witness is None:return 0,'not_failure'
  if witness!=tuple(path):return 0,'other_witness'
  return 1,'accepted'

def cdf_num(n,k,j,D):
 """Exact numerator of P(Bin(n,j/D)<=k), denominator D**n."""
 if k<0:return 0
 if k>=n:return D**n
 if j==0:return D**n
 if j==D:return 0
 term=(D-j)**n;total=term
 for ell in range(k):
  numerator=term*(n-ell)*j;den=(ell+1)*(D-j)
  term,rem=divmod(numerator,den);assert rem==0
  total+=term
 return total

def exact_cp(x,n,alpha=F(1,1000),bits=20):
 """Outward dyadic Clopper-Pearson interval, exact integer comparisons."""
 D=1<<bits;denom=D**n;targetnum=alpha.numerator;targetden=2*alpha.denominator
 if x==0:lower=0
 else:
  lo=0;hi=D
  while hi-lo>1:
   mid=(lo+hi)//2;tail=denom-cdf_num(n,x-1,mid,D)
   if tail*targetden<=targetnum*denom:lo=mid
   else:hi=mid
  lower=lo
 if x==n:upper=D
 else:
  lo=0;hi=D
  while hi-lo>1:
   mid=(lo+hi)//2;cdf=cdf_num(n,x,mid,D)
   if cdf*targetden>=targetnum*denom:lo=mid
   else:hi=mid
  upper=hi
 return F(lower,D),F(upper,D)

def run(d,p,Lmax,shots,seed,out):
 assert shots>0
 start=time.perf_counter();m=Model(d);q=Proposal(m,p,Lmax);setup=time.perf_counter()-start
 rng=random.Random(seed);counts={k:0 for k in ['accepted','nonsimple','not_failure','other_witness']}
 ts=time.perf_counter()
 for i in range(shots):
  value,why=q.trial(rng);counts[why]+=1
 sampletime=time.perf_counter()-ts;tc=time.perf_counter()
 lower,upper=exact_cp(counts['accepted'],shots)
 interval=(q.Z*lower,q.Z*upper+q.tail)
 result={'model':'standard unrotated planar surface-code independent Z noise, ideal syndrome, minimum-weight matching','distance':d,'qubits':len(m.edges),'checks':len(m.checks),'p':str(p),'Lmax':Lmax,'shots':shots,'seed':seed,'counts':counts,'Z_exact':str(q.Z),'Z':float(q.Z),'omitted_canonical_witness_mass_upper_exact':str(q.tail),'tail_bound':float(q.tail),'accepted_probability_CP_interval':[str(lower),str(upper)],'modeled_logical_failure_estimate':float(q.Z*F(counts['accepted'],shots)),'modeled_logical_failure_interval':[float(z) for z in interval],'modeled_logical_failure_interval_exact':[str(z) for z in interval],'confidence':'.999 under independent ideal random bits','arithmetic':'exact integer/rational proposal, normalization, tail, confidence and interval; PyMatching integer-weight optimality assumed and small-instance checked','randomness_caveat':'the executable uses Python Random for reproducibility, not a certificate of independent ideal bits','timing_seconds':{'setup':setup,'sampling':sampletime,'exact_confidence':time.perf_counter()-tc,'total_before_json':time.perf_counter()-start}}
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--distance',type=int,default=13);a.add_argument('--p',default='1/1000');a.add_argument('--length',type=int,default=55);a.add_argument('--shots',type=int,default=10000);a.add_argument('--seed',type=int,default=20261105);a.add_argument('--out',default='result.json');v=a.parse_args();run(v.distance,F(v.p),v.length,v.shots,v.seed,v.out)
