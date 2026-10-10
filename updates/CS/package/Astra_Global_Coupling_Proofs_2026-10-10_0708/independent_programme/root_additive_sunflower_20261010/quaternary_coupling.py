from itertools import product
from random import Random
from collections import Counter
import json

def mul(a,b):
 c=0
 while b:
  if b&1:c^=a
  b>>=1;a<<=1
  if a&4:a^=7
 return c

def dot(a,b):
 z=0
 for x,y in zip(a,b):z^=mul(x,y)
 return z

def kernel(M,m):
 A=[list(row)for row in M];r=0;piv=[]
 for j in range(m):
  k=next((k for k in range(r,len(A))if A[k][j]),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r];iv=next(t for t in range(1,4)if mul(t,A[r][j])==1)
  A[r]=[mul(iv,x)for x in A[r]]
  for k in range(len(A)):
   if k!=r and A[k][j]:
    c=A[k][j];A[k]=[x^mul(c,y)for x,y in zip(A[k],A[r])]
  piv.append(j);r+=1
  if r==len(A):break
 free=[j for j in range(m)if j not in piv];basis=[]
 for j in free:
  v=[0]*m;v[j]=1
  for i,k in enumerate(piv):v[k]=A[i][j]
  basis.append(v)
 return r,basis

def lincomb(cs,B,m):return [dot(cs,[v[j]for v in B])for j in range(m)]
def bits(v,m):return [(v>>j)&1 for j in range(m)]
def asint(v):return sum(x<<j for j,x in enumerate(v))
def output(M,a,m):return tuple(dot(row,bits(a,m))for row in M)

def verify(M,m):
 r,B=kernel(M,m)
 Z=[lincomb(cs,B,m)for cs in product(range(4),repeat=len(B))]
 assert all(all(dot(row,z)==0 for row in M)for z in Z)
 assert len({tuple(z)for z in Z})==4**(m-r)
 maps=[output(M,a,m)for a in range(1<<m)]
 inj=len(set(maps))==1<<m
 cnt=[Counter(),Counter(),Counter()];seen=set()
 for z in Z:
  u=asint([t&1 for t in z]);v=asint([t>>1 for t in z])
  if inj and any(z):assert u and v and u!=v
  for a in range(1<<m):
   trip=(a,a^u,a^v);assert trip not in seen;seen.add(trip)
   for t,x in enumerate(trip):cnt[t][x]+=1
   outs=[maps[x]for x in trip]
   assert all(len({outs[t][i]for t in range(3)})in(1,3)for i in range(len(M)))
 for c in cnt:assert len(c)==1<<m and set(c.values())=={len(Z)}
 assert len(seen)==(1<<m)*4**(m-r)
 return {'m':m,'w':len(M),'gf4_rank':r,'jointly_injective':inj,'valid_distinct_latent_triples_in_coupling_support':len(seen),'likelihood_ratio_against_three_uniform_replicas':4**r}

if __name__=='__main__':
 rng=Random(461010);records=[]
 for m,w in [(4,3),(5,3),(6,4)]:
  for _ in range(20):
   M=[[rng.randrange(4)for _ in range(m)]for _ in range(w)]
   rec=verify(M,m);rec['matrix']=M;records.append(rec)
 print(json.dumps({'status':'all exact finite-field checks passed','seed':461010,'cases':records},indent=2))
