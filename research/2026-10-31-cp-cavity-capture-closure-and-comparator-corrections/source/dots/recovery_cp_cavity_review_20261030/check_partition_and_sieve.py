"""Independent finite combinatorial regression; not an all-size proof."""
import math,json,itertools,random
from functools import lru_cache
random.seed(20261030)
maxratio=0.0
trials=100
for trial in range(trials):
 q=3;n=9;eta=10**random.uniform(-5,-2)
 edges=[]
 for layer in range(3):
  vs=list(range(layer*3,layer*3+3))
  for k in range(1,4):
   for A in itertools.combinations(vs,k):edges.append((sum(1<<j for j in A),random.random()))
 inc=max(sum(w for e,w in edges if e>>j&1) for j in range(n))
 edges=[(e,w*eta/inc) for e,w in edges]
 x=(2*3**(q-1)*eta)**(1/q)
 weights={A:2**A.bit_count()*sum(w for e,w in edges if A&e==A) for A in range(1,1<<n)}
 @lru_cache(None)
 def Z(S):
  if not S:return 1.0
  j=S&-S;total=0.0;A=S
  while A:
   if A&j:total+=weights[A]*Z(S^A)
   A=(A-1)&S
  return total
 for S in range(1,1<<n):
  ratio=Z(S)/x**S.bit_count();maxratio=max(maxratio,ratio)
  assert ratio<=1+1e-12
# Exact integer identity and inequality multiplier.
count=0
for L in range(1,21):
 for t in range(1,L+1):
  for k in range(L+1):
   a=sum((-1)**(s-t)*math.comb(s-1,t-1)*math.comb(k,s) for s in range(t,k+1))
   assert a==int(k>=t);count+=1
  for s in range(t,L+1):
   assert math.comb(L,s)*math.comb(s-1,t-1)*s==t*math.comb(L,t)*math.comb(L-t,s-t)
print(json.dumps({'partition_trials':trials,'locations_per_trial':9,'q':3,'tested_nonempty_subsets':trials*511,'max_partition_bound_ratio':maxratio,'exact_sieve_identity_cases':count},indent=2))
