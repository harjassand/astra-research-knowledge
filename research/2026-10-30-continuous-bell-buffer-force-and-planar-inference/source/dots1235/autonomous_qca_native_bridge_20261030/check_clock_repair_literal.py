#!/usr/bin/env python3
"""Literal local interpretation only. The paper does not fully specify phase/boundary scheduling."""
from itertools import product
from collections import deque
import random,json

def geom(n,m):
 return [(((y+1)%m)*n+x,y*n+(x+1)%n,((y-1)%m)*n+x,y*n+(x-1)%n) for y in range(m) for x in range(n)]
def close(a,b,q):return (a-b)%q in (0,1,q-1)
def valid(s,nb,q):return all(close(s[i],s[j],q) for i in range(len(s)) for j in nb[i][:2])
def march(s,i,nb,q):
 c=(s[i]+1)%q
 if all(close(c,s[j],q) for j in nb[i]):
  o=list(s);o[i]=c;return tuple(o)
 return s
def repair(s,i,nb,q,pairwise=False):
 n,e,so,w=nb[i];c=s[i]
 for _ in range(2):
  ok=close(c,s[n],q) and close(c,s[e],q)
  if pairwise:ok=ok and close(s[n],s[e],q)
  if not ok:
   cand=[v for v in range(q) if close(v,s[n],q) and close(v,s[e],q)]
   c=max(cand) if cand else 0
 mx=max(c,s[so],s[w])
 if not close(c,mx,q):c=mx
 o=list(s);o[i]=c;return tuple(o)

def exhaust(q,pairwise):
 nb=geom(2,2);states=list(product(range(q),repeat=4));idx={s:i for i,s in enumerate(states)}
 rev=[[] for _ in states];good=[];absorbingbad=[]
 for k,s in enumerate(states):
  if valid(s,nb,q):good.append(k)
  changes=False
  for i in range(4):
   for t in [march(s,i,nb,q),repair(s,i,nb,q,pairwise)]:
    rev[idx[t]].append(k);changes|=t!=s
  if not changes and not valid(s,nb,q):absorbingbad.append(s)
 seen=set(good);Q=deque(good)
 while Q:
  for k in rev[Q.popleft()]:
   if k not in seen:seen.add(k);Q.append(k)
 onefault=set()
 for k in good:
  s=states[k]
  for i in range(4):
   for a in range(q):
    t=list(s);t[i]=a;onefault.add(idx[tuple(t)])
 return dict(q=q,pairwise_NE=pairwise,states=len(states),valid=len(good),unhealable=len(states)-len(seen),
             one_fault_unhealable=len(onefault-seen),absorbing_bad=absorbingbad[:10])

def random_trials(q=8,n=10,m=10,trials=50,limit=100000):
 nb=geom(n,m);res=[]
 for seed in range(trials):
  rng=random.Random(seed);s=[0]*(n*m);s[(m//2)*n+n//2]=q//2;s=tuple(s)
  for t in range(limit):
   if valid(s,nb,q):break
   i=rng.randrange(n*m)
   s=repair(s,i,nb,q) if rng.randrange(2) else march(s,i,nb,q)
  res.append(dict(seed=seed,steps=t,healed=valid(s,nb,q),invalid_edges=sum(not close(s[i],s[j],q) for i in range(len(s)) for j in nb[i][:2])))
 return res
q=8;nb=geom(2,2);s=(4,0,0,0);t=march(s,3,nb,q)
report={"scope":"Two literal local interpretations on small periodic patches; not a test of a fully specified source repair scheduler.",
        "guarded_repair_deadlock":{"initial":s,"after_opposite_increment":t,"all_marches_identity":all(march(t,i,nb,q)==t for i in range(4)),
             "unguarded_corrupt_site_repair":repair(s,0,nb,q),"then_corrupt_site_increment":march(repair(s,0,nb,q),0,nb,q)},
        "exhaustive":[exhaust(q,pair) for q in [4,6,8] for pair in [False,True]],
        "random_10x10":random_trials()}
print(json.dumps(report,indent=2))
