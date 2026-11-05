from itertools import product
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json,time,sys

def edge(a,b):return tuple(sorted((a,b)))
def canon(seq):
 seq=list(seq);r=list(reversed(seq));return min(tuple(x[i:]+x[:i]) for x in (seq,r) for i in range(len(x)))
def audit(w,h):
 start=time.monotonic();cycle=[]
 for x in range(w-1):
  for y in range(h-1):
   p=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
   cycle.append(set(edge(p[i],p[(i+1)%4]) for i in range(4)))
 histogram=Counter();polyhist=Counter();single={};routing_count=0
 for mask in range(1<<len(cycle)):
  es=set()
  for j,c in enumerate(cycle):
   if mask>>j&1:es.symmetric_difference_update(c)
  adj={}
  for a,b in es:adj.setdefault(a,[]).append(b);adj.setdefault(b,[]).append(a)
  assert all(len(a) in (2,4) for a in adj.values())
  d4=[v for v,a in adj.items() if len(a)==4];n4=len(d4);n2=len(adj)-n4
  base={}
  for v,a in adj.items():
   a.sort()
   if len(a)==2:base[v]={a[0]:a[1],a[1]:a[0]}
  for choices in product(range(3),repeat=n4):
   pairs=base.copy()
   for v,c in zip(d4,choices):
    a=adj[v];j=c+1;rem=[i for i in (1,2,3) if i!=j]
    pairs[v]={a[0]:a[j],a[j]:a[0],a[rem[0]]:a[rem[1]],a[rem[1]]:a[rem[0]]}
   unused=es.copy();loops=[]
   while unused:
    a,b=min(unused);first=(a,b);p=[]
    while True:
     p.append(a);unused.remove(edge(a,b));a,b=b,pairs[b][a]
     if (a,b)==first:break
    loops.append(canon(p))
   nl=len(loops);histogram[(n2,n4,nl)]+=1;polyhist[nl]+=F(3)**nl*F(1,3)**n2*F(1,15)**n4;routing_count+=1
   weight=F(1);geoms=[]
   for p in loops:
    cnt=Counter(p);rr=sum(c==2 for c in cnt.values());l=len(p)
    lw=F(3)**(1-l)*F(3,5)**rr;weight*=lw;single[p]=lw
    geoms.append((set(p),set(edge(p[i],p[(i+1)%l]) for i in range(l))))
   for j in range(nl):
    for k in range(j):
     assert not(geoms[j][1]&geoms[k][1]);weight*=F(3,5)**len(geoms[j][0]&geoms[k][0])
   direct=F(3)**nl*F(1,3)**n2*F(1,15)**n4
   assert weight==direct
 
 if (w,h)==(4,4):Path(__file__).with_name('single_loop_catalog_4x4.json').write_text(json.dumps([{'route':p,'activity':str(a)} for p,a in single.items()]))
 z=sum(polyhist.values(),F(0));mean=sum(k*v for k,v in polyhist.items())/z
 return {'shape':[w,h],'even_edge_subsets':1<<len(cycle),'routed_configurations':routing_count,'distinct_loops':len(single),'Z':str(z),'mean_loops':str(mean),'mean_loops_decimal':float(mean),'distribution':{k:str(v/z) for k,v in polyhist.items()},'all_route_weights_match':True,'elapsed_seconds':time.monotonic()-start}
if __name__=='__main__':
 out=[audit(*s) for s in [(3,3),(4,3),(4,4)]]
 Path(__file__).with_name('scalar_normalization_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
