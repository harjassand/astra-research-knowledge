"""Closure-aware exact rational birth oracle; torus aliases are rejected."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from bisect import bisect_right
import numpy as np
from exact_loop_birth_sampler import LoopBirthSampler,D,edge,canonical

class TorusLoopBirthSampler(LoopBirthSampler):
 def __init__(self,seed=0,side=16):
  super().__init__(seed)
  data=np.load(Path(__file__).parent/f'torus_green_m6_L{side}.npz')
  self.g=data['q'];self.scale=int(data['scale']);self.side=int(data['side']);N=len(self.states)
  assert self.g.shape==(4*N,side,side)
  R=max(r for _,_,r in self.options);self.den=3**self.m*5**R*self.scale
  cumulative=[];total=0
  for i,h,r in self.options:
   if i<0:q=self.scale
   else:
    x=y=0
    for d in h:x+=D[d][0];y+=D[d][1]
    q=int(self.g[i,x%side,y%side])
    for o in range(4):
     xx,yy=x,y
     for _ in range(o):xx,yy=-yy,xx
     assert q==int(self.g[o*N+i,xx%side,yy%side])
   weight=3**(self.m-len(h)+r)*5**(R-r)*q
   total+=weight;cumulative.append(total)
  self.total=total;self.cumulative=cumulative;self.rate_per_vertex=F(4*total,self.den)
  # Exact full spatial supersolution check, independent of builder history.
  xx,yy=np.indices((side,side))
  for o in range(4):
   for i,h in enumerate(self.states):
    rhs=np.zeros((side,side),dtype=np.int64);rhs[0,0]=15*self.scale
    for j,d in enumerate(self.directions[i]):
     dx,dy=D[(d+o)%4];oo=(o+h[1])%4;ii=int(self.to[i,j])
     rhs+=int(self.w[i,j])*self.g[oo*N+ii,(xx+dx)%side,(yy+dy)%side]
    assert np.all(rhs<=15*self.g[o*N+i])
 def propose(self,width,height):
  rng=self.rng;root=(rng.randrange(width),rng.randrange(height));o=rng.randrange(4)
  idx=bisect_right(self.cumulative,rng.randrange(self.total));state,h,rmem=self.options[idx]
  vs=[root];used=set();N=len(self.states);L=self.side
  for d in h:
   dx,dy=D[(d+o)%4];p=(vs[-1][0]+dx,vs[-1][1]+dy)
   if not(0<=p[0]<width and 0<=p[1]<height):return None
   e=edge(vs[-1],p)
   if e in used:return None
   used.add(e);vs.append(p)
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
    j,d,target,oo=chosen;dx,dy=D[(d+o)%4];p=(vs[-1][0]+dx,vs[-1][1]+dy)
    if not(0<=p[0]<width and 0<=p[1]<height):return None
    e=edge(vs[-1],p)
    if e in used:return None
    used.add(e);vs.append(p);rmem+=int(self.w[state,j]==3);o=oo;state=target
  n=len(vs)-1
  if vs[-1]!=root:return None
  deg=Counter()
  for a,b in used:deg[a]+=1;deg[b]+=1
  assert all(x in(2,4) for x in deg.values())
  rtrue=sum(v==4 for v in deg.values());assert rmem<=rtrue
  acc=F(3,2*n)*F(3,5)**(rtrue-rmem)
  if rng.randrange(acc.denominator)>=acc.numerator:return None
  return canonical(vs[:-1])
if __name__=='__main__':
 import time,json
 s=TorusLoopBirthSampler(20261105);start=time.monotonic();n=100000;accepted=0;lengths=Counter()
 for _ in range(n):
  p=s.propose(3,3)
  if p is not None:accepted+=1;lengths[len(p)]+=1
 z={'proposals':n,'accepted':accepted,'rate_per_vertex':str(s.rate_per_vertex),'rate_decimal':float(s.rate_per_vertex),
 'observed_total_birth_intensity':accepted/n*9*float(s.rate_per_vertex),'exact_total_birth_intensity':str(F(1837,10935)),
 'length_histogram':dict(lengths),'elapsed_seconds':time.monotonic()-start,'scope':'Exact rational closure-aware birth sampler; no physical length cutoff.'}
 (Path(__file__).parent/'torus_birth_test.json').write_text(json.dumps(z,indent=2)+'\n');print(json.dumps(z,indent=2))
