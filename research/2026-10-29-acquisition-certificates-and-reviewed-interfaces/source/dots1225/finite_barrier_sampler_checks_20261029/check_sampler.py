"""Author-side exact checks of rational barrier normalization; not receiving acceptance."""
from fractions import Fraction as F
from pathlib import Path
import json,random

def sampler(L,rho,T):
 M=len(L);eta=F(rho)/4;D=8*M*T;mn=min(L);c=[eta*(x-mn) for x in L];lo=F(1);hi=F(M);steps=0
 while hi-lo>F(1,D):
  mid=(lo+hi)/2;value=sum(1/(x+mid) for x in c)
  if value>1:lo=mid
  else:hi=mid
  steps+=1
 lower=[1/(x+hi) for x in c];upper=[1/(x+lo) for x in c]
 assert sum(lower)<=1<=sum(upper)
 weights=[int(v*D)+2 for v in lower];den=sum(weights);q=[F(w,den) for w in weights]
 assert den<=D+2*M and sum(q)==1
 for l,u,v in zip(lower,upper,q):
  assert u-l<=F(1,D)
  assert v>=F(D,D+2*M)*u
  assert v>=F(1,D+2*M)
 return q,steps
r=random.Random(29029);checks=0;maxsteps=0
for M in [1,2,3,7,17]:
 for T in [1,7,1000]:
  for _ in range(8):
   L=[F(r.randrange(10**20),r.randrange(1,1000)) for i in range(M)]
   q,s=sampler(L,F(1,9),T);checks+=1;maxsteps=max(maxsteps,s)
M=7;T=200;rho=F(1,9);L=[F(0)]*M
for t in range(T):
 q,s=sampler(L,rho,T);j=min(range(M),key=lambda i:q[i]);update=1/(rho*q[j]);assert update<=F(8*M*T+2*M,rho);L[j]+=update
maxbits=max(max(x.numerator.bit_length(),x.denominator.bit_length()) for x in L)
result=dict(random_parameter_cases=checks,worst_candidate_updates=T,max_bisections_random=maxsteps,max_final_coefficient_bits=maxbits,scope='Author-side exact rational normalization and importance-bound checks; no full bandit regret/quantum receiving review.')
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
