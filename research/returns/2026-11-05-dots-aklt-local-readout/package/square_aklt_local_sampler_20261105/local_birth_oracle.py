"""Exact finite-query loop birth measure on Z² or an open rectangular box.
At rate rate(K), propose(K) emits each loop gamma meeting K at intensity w_gamma.
Rejected/null proposals remain part of the dominating Poisson process.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from bisect import bisect_right
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'square_aklt_boundary_operation_20261105'))
from torus_loop_birth_sampler import TorusLoopBirthSampler,D,edge,canonical

class LocalLoopBirthSampler(TorusLoopBirthSampler):
 def rate(self,K):
  K=frozenset(K)
  return F(3,2)*self.rate_per_vertex*len(K)
 def propose(self,K,box=None):
  """K finite vertices; box None, (width,height), or (xmin,xmax,ymin,ymax)."""
  K=tuple(sorted(set(K)))
  if not K:return None
  if box is not None:
   if len(box)==2:xmin,xmax,ymin,ymax=0,box[0],0,box[1]
   else:xmin,xmax,ymin,ymax=box
   assert all(xmin<=x<xmax and ymin<=y<ymax for x,y in K)
  rng=self.rng;root=K[rng.randrange(len(K))];o=rng.randrange(4)
  idx=bisect_right(self.cumulative,rng.randrange(self.total));state,h,rmem=self.options[idx]
  vs=[root];used=set();N=len(self.states);L=self.side
  def step(d):
   dx,dy=D[(d+o)%4];p=(vs[-1][0]+dx,vs[-1][1]+dy)
   if box is not None and not(xmin<=p[0]<xmax and ymin<=p[1]<ymax):return False
   e=edge(vs[-1],p)
   if e in used:return False
   used.add(e);vs.append(p);return True
  for d in h:
   if not step(d):return None
  if state>=0:
   while True:
    x=(vs[-1][0]-root[0])%L;y=(vs[-1][1]-root[1])%L
    q=int(self.g[o*N+state,x,y]);u=rng.randrange(15*q)
    stop=15*self.scale if x==0 and y==0 else 0
    if u<stop:break
    u-=stop;chosen=None
    for j,d in enumerate(self.directions[state]):
     target=int(self.to[state,j]);dx,dy=D[(d+o)%4];oo=(o+self.states[state][1])%4
     weight=int(self.w[state,j])*int(self.g[oo*N+target,(x+dx)%L,(y+dy)%L])
     if u<weight:chosen=(j,d,target,oo);break
     u-=weight
    if chosen is None:return None
    j,d,target,oo=chosen
    if not step(d):return None
    rmem+=int(self.w[state,j]==3);o=oo;state=target
  if vs[-1]!=root:return None
  deg=Counter()
  for a,b in used:deg[a]+=1;deg[b]+=1
  assert all(x in(2,4) for x in deg.values())
  rtrue=sum(v==4 for v in deg.values());assert rmem<=rtrue
  Ks=frozenset(K);k=sum(v in Ks for v in vs[:-1]);assert k>=1
  acc=F(1,k)*F(3,5)**(rtrue-rmem)
  if rng.randrange(acc.denominator)>=acc.numerator:return None
  return canonical(vs[:-1])
