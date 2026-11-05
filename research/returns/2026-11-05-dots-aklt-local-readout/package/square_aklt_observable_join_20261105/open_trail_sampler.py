"""Exact rational unbounded open-trail proposal measures for AKLT insertions.
The output probability of each oriented physical path p is a_p / majorant,
with a_p=3^-length*(3/5)^four_line_vertices. None carries rejected mass.
"""
from pathlib import Path
from fractions import Fraction as F
from bisect import bisect_right
from collections import Counter
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'square_aklt_boundary_operation_20261105'))
from exact_loop_birth_sampler import LoopBirthSampler,D,edge
from torus_loop_birth_sampler import TorusLoopBirthSampler

def short_trails(m):
 out=[]
 def visit(ds,ps,used,seen,r):
  out.append((-1,tuple(ds),r))
  if len(ds)==m-1:return
  for d,(dx,dy) in enumerate(D):
   p=(ps[-1][0]+dx,ps[-1][1]+dy);e=edge(ps[-1],p)
   if e not in used:
    rr=r+int(p in seen and p!=(0,0))
    visit(ds+[d],ps+[p],used|{e},seen|{p},rr)
 visit([0],[(0,0),(1,0)],{((0,0),(1,0))},{(0,0),(1,0)},0)
 return out

def true_contact_count(vs):
 assert vs[0]!=vs[-1]
 deg=Counter()
 for a,b in zip(vs,vs[1:]):deg[a]+=1;deg[b]+=1
 ends={vs[0],vs[-1]}
 assert all(d in ((1,3) if v in ends else (2,4)) for v,d in deg.items())
 return sum(d==4 or(v in ends and d==3) for v,d in deg.items())

class OpenTrailSampler(LoopBirthSampler):
 def __init__(self,seed=0,target=None,side=16):
  self.target=target
  if target is None:
   super().__init__(seed);self.spatial=False
  else:
   assert target!=(0,0)
   b=TorusLoopBirthSampler(seed,side)
   self.__dict__.update(b.__dict__);self.target=target;self.spatial=True
  prefixes=[x for x in self.options if x[0]>=0]
  shorts=short_trails(self.m)
  R=max(x[2] for x in prefixes+shorts)
  scale=self.scale if self.spatial else self.qden
  self.den=3**self.m*5**R*scale
  self.options=[];self.cumulative=[];total=0;ns=len(self.states)
  for o in range(4):
   for i,h,r in shorts+prefixes:
    dx=dy=0
    for d in h:
     x,y=D[(d+o)%4];dx+=x;dy+=y
    if i<0:
     if target is not None and(dx,dy)!=target:continue
     q=scale
    elif self.spatial:
     q=int(self.g[o*ns+i,(dx-target[0])%self.side,(dy-target[1])%self.side])
    else:q=self.qnum[i]
    weight=3**(self.m-len(h)+r)*5**(R-r)*q
    if not weight:continue
    self.options.append((o,i,h,r));total+=weight;self.cumulative.append(total)
  self.total=total;self.majorant=F(total,self.den)
 def propose_path(self,width,height,root):
  assert (width is None)==(height is None)
  rng=self.rng
  idx=bisect_right(self.cumulative,rng.randrange(self.total))
  o,state,h,rmem=self.options[idx]
  vs=[root];used=set();ns=len(self.states)
  def step(d):
   dx,dy=D[(d+o)%4];p=(vs[-1][0]+dx,vs[-1][1]+dy)
   if width is not None and not(0<=p[0]<width and 0<=p[1]<height):return False
   e=edge(vs[-1],p)
   if e in used:return False
   used.add(e);vs.append(p);return True
  for d in h:
   if not step(d):return None
  if state>=0:
   while True:
    if self.spatial:
     x=(vs[-1][0]-root[0]-self.target[0])%self.side
     y=(vs[-1][1]-root[1]-self.target[1])%self.side
     q=int(self.g[o*ns+state,x,y]);stop=15*self.scale if x==0 and y==0 else 0
    else:q=self.qnum[state];stop=15*self.qden
    u=rng.randrange(15*q)
    if u<stop:break
    u-=stop;chosen=None
    for j,d in enumerate(self.directions[state]):
     ii=int(self.to[state,j]);oo=(o+self.states[state][1])%4
     if self.spatial:
      dx,dy=D[(d+o)%4]
      weight=int(self.w[state,j])*int(self.g[oo*ns+ii,(x+dx)%self.side,(y+dy)%self.side])
     else:weight=int(self.w[state,j])*self.qnum[ii]
     if u<weight:chosen=(j,d,ii,oo);break
     u-=weight
    if chosen is None:return None
    j,d,ii,oo=chosen
    if not step(d):return None
    rmem+=int(self.w[state,j]==3);o=oo;state=ii
  if vs[-1]==root:return None
  if self.target is not None and(vs[-1][0]-root[0],vs[-1][1]-root[1])!=self.target:return None
  rtrue=true_contact_count(vs)
  assert rmem<=rtrue,(vs,rmem,rtrue)
  acc=F(3,5)**(rtrue-rmem)
  if rng.randrange(acc.denominator)>=acc.numerator:return None
  return tuple(vs)

def suppression(path,loops):
 pe={edge(a,b) for a,b in zip(path,path[1:])};pv=set(path);k=0
 for route in loops:
  le={edge(route[i],route[(i+1)%len(route)]) for i in range(len(route))}
  if pe&le:return F(0)
  k+=len(pv&set(route))
 return F(3,5)**k
