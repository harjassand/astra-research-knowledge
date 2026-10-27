from fractions import Fraction as Q
from math import comb
from pathlib import Path
import json
P=Path(__file__).parent
def moment(a,b,c):
 return Q(sum(comb(a,i)*comb(b,j)*comb(c,k) for i in range(a+1)for j in range(b+1)for k in range(c+1)if a-2*i+c-2*k==0 and b-2*j+c-2*k==0),2**(a+b+c))
def mul(p,r):
 out={}
 for a,c in p.items():
  for b,d in r.items():
   e=tuple(x+y for x,y in zip(a,b));out[e]=out.get(e,Q())+c*d
 return out
def E(p):return sum(c*moment(*e)for e,c in p.items())
z=[{tuple(int(i==j)for i in range(3)):Q(1)}for j in range(3)];q={(1,1,0):Q(1),(1,0,1):Q(1),(0,1,1):Q(1)}
assert E(q)==0 and E(mul(q,q))==Q(3,4)
assert [E(mul(q,v))for v in z]==[Q(1,4)]*3
rows=[]
for i in range(3):
 h={}
 for j in range(3):
  for e in z[j]:h[e]=Q(8 if j==i else 2,3)
 for e in q:h[e]=Q(-4,3)
 mean=[E(mul(h,v))for v in z];assert mean==[Q(int(j==i))for j in range(3)] and E(h)==E(mul(q,h))==0
 assert sum(map(abs,h.values()))==8
 rows.append({'axis':i,'coefficients':[[list(e),str(c)]for e,c in h.items()],'mean_direction':list(map(str,mean))})
h={(0,1,0):Q(3),(0,0,1):Q(3),**{e:Q(-2)for e in q}}
v=[E(mul(h,x))for x in z];assert v==[Q(-1,2),Q(1),Q(1)] and E(h)==E(mul(q,h))==0
assert sum(map(abs,h.values()))==12
eps=Q(1,48);times=[-2*eps,eps];weights=[Q(1,3),Q(2,3)];assert sum(w*t for w,t in zip(weights,times))==0
cubic=sum(w*t**3*v[0]*v[1]*v[2]for w,t in zip(weights,times));variance=sum(w*t*t*sum(a*a for a in v)for w,t in zip(weights,times));assert cubic==Q(1,110592) and variance==Q(1,512)
r={'status':'EXACT_POSTERIOR_ROOT_SPLIT_PASS_NOT_EXHAUSTION','epsilon':'1/16','density_interval':['1/2','3/2'],'mean_variance_drop':'1/256','rows':rows,'nonaxis_direction':list(map(str,v)),'asymmetric_epsilon':str(eps),'asymmetric_cubic_acquisition':str(cubic),'asymmetric_variance_drop':str(variance),'scope':'Exact source disintegration and actual null mean-tree prefix only. Conditional terminal laws NOT proved reachable; no completed lamination, source exhaustion or Morrey resolution.'};(P/'root_posterior_split_receipt.json').write_text(json.dumps(r,indent=2));print(r['status'])
