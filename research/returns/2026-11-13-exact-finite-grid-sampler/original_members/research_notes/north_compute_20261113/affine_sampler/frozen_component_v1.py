"""Exact Gaussian-integer component trajectory sampler with circuit-level bridge pruning.
No MPS or floating quantum arithmetic. Optional dense validation uses floats only as a test.
"""
import sys,random,time,math
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'bridge_dephasing'))
from check import bridge_indices
class Limit(Exception):pass

def grid_layers(w,h,T):
 lays=[]
 for axis,p in [(0,0),(0,1),(1,0),(1,1)]:
  E=[]
  for y in range(h):
   for x in range(w):
    if axis==0 and x%2==p and x+1<w:E.append((y*w+x,y*w+x+1))
    if axis==1 and y%2==p and y+1<h:E.append((y*w+x,(y+1)*w+x))
  lays.append(E)
 return [lays[t%4] for t in range(T)]

def categories(layers,r,eps,rng):
 den=math.lcm(r.denominator,eps.denominator);R=int(r*den);Q=int(eps*den);events=[]
 for layer in layers:
  for u,v in layer:
   coin=rng.randrange(den);events.append((u,v,'R' if coin<R else 'Q' if coin<R+Q else 'D'))
 return events

def last_sites(n,events,bridges):
 future=[False]*n;last=[[] for _ in events]
 for t in range(len(events)-1,-1,-1):
  u,v,kind=events[t]
  if kind=='R':future[u]=future[v]=False
  elif kind=='Q' and t not in bridges:
   for s in (u,v):
    if not future[s]:last[t].append(s)
    future[s]=True
 return last

def norm(a):return sum(x*x+y*y for x,y in a.values())
class Engine:
 def __init__(self,n,rng,cap,bitcap):
  self.n=n;self.rng=rng;self.cap=cap;self.bitcap=bitcap;self.owner=[None]*n;self.known=[0]*n;self.groups={};self.nextid=0
  self.stats=dict(max_component_entries=0,max_live_entries=0,max_amplitude_integer_bits=0,max_norm_integer_bits=0,max_live_payload_bits=0,measurements=0,inferred_basis_bits=0)
 def record(self):
  live=0;payload=0
  for sites,amp in self.groups.values():
   live+=len(amp);self.stats['max_component_entries']=max(self.stats['max_component_entries'],len(amp))
   for key,(a,b) in amp.items():
    bits=max(abs(a).bit_length(),abs(b).bit_length());self.stats['max_amplitude_integer_bits']=max(self.stats['max_amplitude_integer_bits'],bits)
    if bits>self.bitcap:raise Limit('integer_bit_cap')
    payload+=key.bit_length()+abs(a).bit_length()+abs(b).bit_length()
  self.stats['max_live_entries']=max(self.stats['max_live_entries'],live);self.stats['max_live_payload_bits']=max(self.stats['max_live_payload_bits'],payload)
 def make(self,s):
  if self.owner[s] is not None:return self.owner[s]
  i=self.nextid;self.nextid+=1;self.groups[i]=({s},{self.known[s]<<s:(1,0)});self.owner[s]=i;return i
 def merge(self,u,v):
  i=self.make(u);j=self.make(v)
  if i==j:return i
  A,a=self.groups[i];B,b=self.groups[j]
  if len(a)*len(b)>self.cap:raise Limit('component_entry_cap_before_merge')
  c={}
  for x,(ar,ai) in a.items():
   for y,(br,bi) in b.items():c[x|y]=(ar*br-ai*bi,ar*bi+ai*br)
  sites=A|B;self.groups[i]=(sites,c);del self.groups[j]
  for s in sites:self.owner[s]=i
  return i
 def retire(self,i):
  if i not in self.groups:return
  sites,a=self.groups[i];mask=sum(1<<s for s in sites);both=mask;either=0
  for x in a:both&=x;either|=x
  fixed=mask&~(both^either);removed={s for s in sites if fixed>>s&1}
  if not removed:return
  for s in removed:self.owner[s]=None;self.known[s]=(both>>s)&1
  self.stats['inferred_basis_bits']+=len(removed)
  sites=sites-removed
  if not sites:del self.groups[i];return
  self.groups[i]=(sites,{x&~fixed:z for x,z in a.items()})
 def diagonal(self,u,v):
  if self.owner[u] is None and self.owner[v] is None:return
  if self.owner[u] is None:i=self.owner[v]
  elif self.owner[v] is None:i=self.owner[u]
  else:i=self.merge(u,v)
  sites,a=self.groups[i];signs={}
  for x in a:
   bu=(x>>u)&1 if u in sites else self.known[u];bv=(x>>v)&1 if v in sites else self.known[v];signs[x]=1 if bu==bv else -1
  if len(set(signs.values()))==1:return # global phase irrelevant
  self.groups[i]=(sites,{x:(3*ar-4*signs[x]*ai,4*signs[x]*ar+3*ai) for x,(ar,ai) in a.items()});self.record()
 def q(self,u,v):
  i=self.merge(u,v);sites,a=self.groups[i];mask=(1<<u)|(1<<v)
  if len(set(a)|{x^mask for x in a})>self.cap:raise Limit('component_entry_cap_before_Q')
  c={}
  for x,(ar,ai) in a.items():
   old=c.get(x,(0,0));c[x]=(old[0]+12*ar,old[1]+12*ai);y=x^mask;old=c.get(y,(0,0));c[y]=(old[0]+5*ai,old[1]-5*ar)
  c={x:z for x,z in c.items() if z!=(0,0)};self.groups[i]=(sites,c);self.retire(i);self.record()
 def flip(self,u):
  i=self.owner[u]
  if i is None:self.known[u]^=1;return
  sites,a=self.groups[i];self.groups[i]=(sites,{x^(1<<u):z for x,z in a.items()})
 def measure(self,u):
  self.stats['measurements']+=1;i=self.owner[u]
  if i is None:return self.known[u],F(1)
  sites,a=self.groups[i];total=norm(a);one=sum(ar*ar+ai*ai for x,(ar,ai) in a.items() if x>>u&1);b=int(self.rng.randrange(total)<one);num=one if b else total-one
  self.stats['max_norm_integer_bits']=max(self.stats['max_norm_integer_bits'],total.bit_length())
  self.groups[i]=(sites,{x:z for x,z in a.items() if (x>>u)&1==b});self.retire(i);self.record();return b,F(num,total)

def sample(n,layers,r=F(3,100),eps=F(1,50),seed=1,cap=65536,bitcap=100000,prune=True,early=True,validate=False,events=None):
 start=time.perf_counter();rng=random.Random(seed);events=categories(layers,r,eps,rng) if events is None else list(events);pre=time.perf_counter();bridges=bridge_indices(n,events) if prune else set();last=last_sites(n,events,bridges) if early else [[] for _ in events];prep=time.perf_counter()-pre
 eng=Engine(n,rng,cap,bitcap);stats=dict(n=n,pair_slots=len(events),Q=sum(e[2]=='Q' for e in events),bridges=len(bridges),bridge_preprocessing_seconds=prep,aborted=False)
 if validate:
  import numpy as np
  sys.path.insert(0,str(Path('research_notes/quantum_connected_bridge_20261113/frame_sampler').resolve()));from sampler import bitphase,qgate,project
  dense=np.zeros(1<<n,complex);dense[0]=1;worst=0
 def measured(u):
  nonlocal dense,worst
  b,p=eng.measure(u)
  if validate:
   dense,pd=project(dense,u,b);worst=max(worst,abs(float(p)-pd))
  return b
 try:
  for t,(u,v,kind) in enumerate(events):
   if kind!='R':
    eng.diagonal(u,v)
    if validate:dense*=bitphase(n,[u,v],math.atan2(4,3))
   if kind=='Q':
    if t in bridges:
     if rng.randrange(169)<25:
      eng.flip(u);eng.flip(v)
      if validate:dense=dense[np.arange(1<<n)^((1<<u)|(1<<v))]
    else:
     eng.q(u,v)
     if validate:dense=qgate(dense,(1<<u)|(1<<v))
   for s in last[t]:measured(s)
   if kind=='R':
    for s in (u,v):
     a=measured(s);b=rng.randrange(2)
     if a!=b:
      eng.flip(s)
      if validate:dense=dense[np.arange(1<<n)^(1<<s)]
   eng.record()
  output=0
  for s in range(n):output|=measured(s)<<s
  if validate:stats['max_Born_probability_discrepancy']=worst
 except Limit as e:stats['aborted']=True;stats['reason']=str(e);output=0
 stats.update(eng.stats);stats['seconds']=time.perf_counter()-start
 return output,stats
