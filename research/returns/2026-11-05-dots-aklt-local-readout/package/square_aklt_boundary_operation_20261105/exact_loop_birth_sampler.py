"""Unbounded-length exact rational thinning sampler for physical loop births.
No length cutoff. Uses integer random choices and exact rational acceptance.
This samples the loop birth MEASURE, not the interacting equilibrium gas.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from bisect import bisect_right
import random,json,time,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'square_aklt_loop_audit_20261105'))
from weighted_trail_bound import build,D,edge

def canonical(vs):
 n=len(vs);out=[]
 for a in (vs,vs[::-1]):
  for k in range(n):out.append(tuple(a[k:]+a[:k]))
 return min(out)

class LoopBirthSampler:
 def __init__(self,seed=0):
  self.rng=random.Random(seed);self.m=6
  self.states,self.to,self.w=build(self.m)
  z=np.load(ROOT/'square_aklt_loop_audit_20261105/trail_certificate_m6.npz')
  vi=z['v'];an=int(z['alpha_num']);ad=int(z['alpha_den'])
  assert np.all((z['weights']*vi[z['targets']]).sum(1)*ad<=5*vi*an)
  self.qnum=[3*ad*int(v) for v in vi];self.qden=(3*ad-an)*int(vi.min())
  self.directions=[];prefix=[]
  for i,h in enumerate(self.states):
   ps=[(0,0)];seen={(0,0)};r=0
   for d in h:
    x,y=ps[-1];p=(x+D[d][0],y+D[d][1]);ps.append(p)
    if p in seen and p!=(0,0):r+=1
    seen.add(p)
   used={edge(ps[k],ps[k+1]) for k in range(self.m)}
   dirs=[]
   for d,(dx,dy) in enumerate(D):
    p=(ps[-1][0]+dx,ps[-1][1]+dy)
    if edge(ps[-1],p) not in used:dirs.append(d)
   self.directions.append(dirs);prefix.append((i,tuple(h),r))
  # All closed trails shorter than memory, with first direction East.
  shorts=[]
  def walk(ds,ps,used):
   n=len(ds)
   if n>=4 and ps[-1]==(0,0):shorts.append((-1,tuple(ds),0))
   if n==self.m-1:return
   for d,(dx,dy) in enumerate(D):
    p=(ps[-1][0]+dx,ps[-1][1]+dy);e=edge(ps[-1],p)
    if e not in used:walk(ds+[d],ps+[p],used|{e})
  walk([0],[(0,0),(1,0)],{((0,0),(1,0))})
  assert len(shorts)==2
  R=max(t[2] for t in prefix+shorts)
  self.den=3**self.m*5**R*self.qden
  self.options=shorts+prefix;self.cumulative=[];s=0
  for i,h,r in self.options:
   weight=3**(self.m-len(h)+r)*5**(R-r)*(self.qden if i<0 else self.qnum[i])
   s+=weight;self.cumulative.append(s)
  self.total=s;self.rate_per_vertex=F(4*s,self.den)
  for i in range(len(self.states)):
   assert 15*self.qnum[i]>=15*self.qden+sum(int(self.w[i,j])*self.qnum[int(self.to[i,j])] for j in range(len(self.directions[i])))

 def propose(self,width,height):
  rng=self.rng;root=(rng.randrange(width),rng.randrange(height));o=rng.randrange(4)
  idx=bisect_right(self.cumulative,rng.randrange(self.total));state,h,rmem=self.options[idx]
  vs=[root];used=set()
  for d in h:
   dx,dy=D[(d+o)%4];p=(vs[-1][0]+dx,vs[-1][1]+dy)
   if not(0<=p[0]<width and 0<=p[1]<height):return None
   e=edge(vs[-1],p)
   if e in used:return None
   used.add(e);vs.append(p)
  if state>=0:
   while True:
    u=rng.randrange(15*self.qnum[state])
    if u<15*self.qden:break
    u-=15*self.qden;chosen=None
    for j,d in enumerate(self.directions[state]):
     target=int(self.to[state,j]);weight=int(self.w[state,j])*self.qnum[target]
     if u<weight:chosen=(j,d,target);break
     u-=weight
    if chosen is None:return None
    j,d,target=chosen;dx,dy=D[(d+o)%4];p=(vs[-1][0]+dx,vs[-1][1]+dy)
    if not(0<=p[0]<width and 0<=p[1]<height):return None
    e=edge(vs[-1],p)
    if e in used:return None
    used.add(e);vs.append(p)
    rmem+=int(self.w[state,j]==3)
    o=(o+self.states[state][1])%4;state=target
  n=len(vs)-1
  if vs[-1]!=root:return None
  degrees=Counter()
  for a,b in used:degrees[a]+=1;degrees[b]+=1
  assert all(v in (2,4) for v in degrees.values())
  rtrue=sum(v==4 for v in degrees.values())
  assert rmem<=rtrue,(n,rmem,rtrue,vs)
  accept=F(3,2*n)*F(3,5)**(rtrue-rmem)
  if rng.randrange(accept.denominator)>=accept.numerator:return None
  return canonical(vs[:-1])

if __name__=='__main__':
 s=LoopBirthSampler(seed=20261105);attempts=int(sys.argv[1]) if len(sys.argv)>1 else 200000
 start=time.monotonic();counts=Counter()
 for _ in range(attempts):
  p=s.propose(3,3)
  if p is not None:counts[p]+=1
 # In a3×3box there are only12physical edges, so the independently
 # enumerated complete≤12catalog is sufficient for an exact intensity sum.
 sys.path.insert(0,str(Path(__file__).resolve().parent))
 from crossed_loop_influence import variants
 cat=json.loads((ROOT/'square_aklt_loop_audit_20261105/loop_catalog_through12.json').read_text())
 exact={}
 for item in cat:
  for p in variants(item['cyclic_vertices']):
   mx=max(x for x,y in p);my=max(y for x,y in p)
   for dx in range(3-mx):
    for dy in range(3-my):
     q=canonical([(x+dx,y+dy) for x,y in p]);exact[q]=F(item['activity'])
 expected=sum(exact.values(),F(0));observed=F(sum(counts.values()),attempts)*9*s.rate_per_vertex
 result={'attempts':attempts,'accepted':sum(counts.values()),'proposal_rate_per_vertex':str(s.rate_per_vertex),
 'number_physical_loop_types_3x3':len(exact),'exact_total_birth_intensity':str(expected),'observed_intensity':float(observed),
 'expected_acceptance_probability':float(expected/(9*s.rate_per_vertex)),
 'elapsed_seconds':time.monotonic()-start,'longest_sampled_loop':max(map(len,counts),default=0),
 'scope':'Exact integer/rational unbounded-length birth sampler. Empirical test checks intensity only; this is not an interacting-gas sampler.'}
 assert set(counts)<=set(exact)
 (Path(__file__).parent/'birth_sampler_test.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
