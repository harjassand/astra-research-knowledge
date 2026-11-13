from fractions import Fraction as F
from collections import defaultdict
import math,json
from pathlib import Path
L=4;n=L*L;K=4096;field=2;kappa=F(1)
edges=[];aug=[]
for y in range(L):
 for x in range(L):
  i=y*L+x
  edges.extend([(i,y*L+(x+1)%L),(i,((y+1)%L)*L+x)])
  aug.extend([(i,y*L+(x+1)%L),(i,((y+1)%L)*L+x),(i,((y+1)%L)*L+(x+1)%L)])
# Core r=1: each augmented plus component is a single site.
A=[x for x in range(1<<n) if not any((x>>i&1) and (x>>j&1) for i,j in aug)]
cache={}
def w(x):
 if x not in cache:
  disagree=sum(((x>>i)&1)!=((x>>j)&1) for i,j in edges)
  cache[x]=F(field**x.bit_count(),K**disagree) # normalize wminus=1
 return cache[x]
ZA=sum(map(w,A),F(0)); order=[]
for s in range(L):
 order += [j*L+s for j in range(s)]+[s*L+i for i in range(s+1)]
assert len(set(order))==n
flows=defaultdict(F); div=defaultdict(F); direct=F(0)
for x in A:
 mass=w(x)/ZA; z=x
 for i in order:
  if z.bit_count()>=n//2:break
  y=z^(1<<i);a,b=sorted((z,y));flows[(a,b)]+=mass if z==a else -mass;z=y
 assert z.bit_count()>=n//2
 # Full, un-stopped path comparison upper.
 z=x
 for i in order:
  y=z^(1<<i)
  direct+=(w(x)/ZA)**2*(1/w(z)+1/w(y));z=y
E=F(0)
for (x,y),f in flows.items():
 div[x]+=f;div[y]-=f
 E+=f*f*(1/w(x)+1/w(y))
for x,v in div.items():
 if x.bit_count()>=n//2:assert v<=0
 elif x in A:assert v==w(x)/ZA
 else:assert v==0
assert E<=direct
Es=1/(kappa*ZA)
def log(x):return math.log(x.numerator)-math.log(x.denominator)
r={'L':L,'n':n,'r':1,'R':12,'theta':math.log(K)/2,'edge_activity':K,'field_activity':field,'core_states':len(A),'queried_states':len(cache),'nonzero_physical_edges':sum(f!=0 for f in flows.values()),'exact_divergence_check':True,'exact_energy_comparison_check':True,'log_ZA':log(ZA),'log_unit_flow_energy_including_source':log(E+Es),'log_direct_full_path_energy_bound':log(direct+Es)}
Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
