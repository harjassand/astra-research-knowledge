#!/usr/bin/env python3
from pathlib import Path
from functools import lru_cache
import math,itertools,random,json
HERE=Path(__file__).parent
@lru_cache(None)
def completions(m,a,b):
 if a==b==m:return 1
 return (completions(m,a+1,b) if a<m else 0)+(completions(m,a,b+1) if b<a else 0)
def unrank(m,r):
 assert 0<=r<completions(m,0,0);a=b=0;w=[]
 while a+b<2*m:
  n=completions(m,a+1,b) if a<m else 0
  if r<n:w.append(0);a+=1
  else:r-=n;w.append(1);b+=1
 return w
def rank(m,w):
 a=b=r=0
 for x in w:
  if x:
   r+=completions(m,a+1,b) if a<m else 0;b+=1
  else:a+=1
  assert 0<=b<=a<=m
 assert a==b==m
 return r
rows=[];rng=random.Random(31237)
for m in [2,3,5,10,25,50]:
 d=completions(m,0,0);assert d==math.comb(2*m,m)//(m+1)
 rs=[0,d-1]+[rng.randrange(d) for _ in range(100)]
 assert all(rank(m,unrank(m,r))==r for r in rs)
 rows.append({'m':m,'dimension_bits':d.bit_length(),'rank_unrank_checks':len(rs)})
diag=[]
for q in range(2,8):
 D=2**q;seen={};pairs=list(itertools.combinations(range(q),2))
 # The moment survives iff two strings have identical unordered projected
 # bit-pair multisets on every pair of positions.
 for x in range(D):
  for y in range(x,D):
   sig=tuple(tuple(sorted([((x>>i)&1)*2+((x>>j)&1),((y>>i)&1)*2+((y>>j)&1)])) for i,j in pairs)
   assert sig not in seen;seen[sig]=(x,y)
 diag.append({'q':q,'unordered_input_pairs':len(seen),'distinct_signatures':len(seen),'two_qubit_diagonal_gates':len(pairs)})
(HERE/'check_access_v1.json').write_text(json.dumps({'rank_unrank':rows,'diagonal_2design_signature':diag},indent=2)+'\n');print('all access checks passed')
